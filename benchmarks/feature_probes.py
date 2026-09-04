#!/usr/bin/env python3

from __future__ import annotations

import argparse
import copy
import json
import os
import pathlib
import sys
from collections.abc import Sequence
from typing import Any

from feature_manifest import (
    SCHEMA as FEATURE_MANIFEST_SCHEMA,
    load_and_validate,
    manifest_sha256,
    source_tree_sha256,
)
from marimay_toolchain import validate_executable
from perf_environment import capture_metadata, finish_metadata, git_revision, run_checked
from perf_protocol import (
    PROBE_RESULT_SCHEMA,
    ProtocolError,
    load_protocol,
    measure_matrix,
    sha256_file,
    summarize_matrix,
    validate_result,
    validate_run_shape,
)
from probes import timed_run


FEATURE_RESULT_SCHEMA = "marimay.feature-probes/1"


def parse_args(protocol: dict[str, Any]) -> argparse.Namespace:
    measurement = protocol["measurement"]
    parser = argparse.ArgumentParser(
        description="Build and measure local-only Marimay language feature probes."
    )
    parser.add_argument(
        "--samples", type=int, default=measurement["minimum_samples"]
    )
    parser.add_argument(
        "--warmups", type=int, default=measurement["minimum_warmups"]
    )
    parser.add_argument(
        "--timeout", type=int, default=measurement["timeout_seconds"]
    )
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--feature", action="append", metavar="ID")
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("benchmarks/results/feature-probes-local.json"),
    )
    args = parser.parse_args()
    try:
        validate_run_shape(protocol, args.warmups, args.samples)
    except ProtocolError as error:
        parser.error(str(error))
    if args.timeout != measurement["timeout_seconds"]:
        parser.error("feature probe timeout must match performance_protocol.json")
    return args


def select_features(
    features: Sequence[dict[str, Any]], requested: Sequence[str] | None
) -> list[dict[str, Any]]:
    if not requested:
        return list(features)
    known = {feature["id"] for feature in features}
    unknown = set(requested) - known
    if unknown:
        names = ", ".join(sorted(unknown))
        raise ProtocolError(f"unknown feature probe: {names}")
    selected = set(requested)
    return [feature for feature in features if feature["id"] in selected]


def build_features(
    repository: pathlib.Path,
    mmay_binary: pathlib.Path,
    features: Sequence[dict[str, Any]],
    build_directory: pathlib.Path,
    max_heap_bytes: int,
) -> dict[str, dict[str, list[str]]]:
    marimay_root = repository / "marimay"
    run_checked([str(mmay_binary), "fmt", str(marimay_root), "--check"], cwd=repository)
    run_checked([str(mmay_binary), "check", str(marimay_root)], cwd=repository)
    commands: dict[str, dict[str, list[str]]] = {"marimay": {}}
    for feature in features:
        feature_id = feature["id"]
        output = build_directory / f"marimay-feature-{feature_id}"
        run_checked(
            [
                str(mmay_binary),
                "build",
                str(repository / feature["source_directory"]),
                "--release",
                "--max-heap-bytes",
                str(max_heap_bytes),
                "--output",
                str(output),
            ],
            cwd=repository,
            timeout=600,
        )
        commands["marimay"][feature_id] = [str(output)]
    return commands


def existing_features(
    features: Sequence[dict[str, Any]], build_directory: pathlib.Path
) -> dict[str, dict[str, list[str]]]:
    commands: dict[str, dict[str, list[str]]] = {"marimay": {}}
    for feature in features:
        path = build_directory / f"marimay-feature-{feature['id']}"
        if not path.is_file() or not os.access(path, os.X_OK):
            raise ProtocolError(f"missing binary for --skip-build: {path}")
        commands["marimay"][feature["id"]] = [str(path)]
    return commands


def validate_feature_result(
    result: dict[str, Any], protocol: dict[str, Any], protocol_sha: str
) -> None:
    if result.get("schema") != FEATURE_RESULT_SCHEMA:
        raise ProtocolError("unsupported feature probe result schema")
    metadata = result.get("metadata")
    if not isinstance(metadata, dict):
        raise ProtocolError("feature probe result has no metadata")
    if metadata.get("comparison_scope") != "local-only":
        raise ProtocolError("feature probes must remain local-only")
    manifest = metadata.get("feature_manifest")
    if not isinstance(manifest, dict):
        raise ProtocolError("feature probe result has no feature manifest")
    if manifest.get("schema") != FEATURE_MANIFEST_SCHEMA:
        raise ProtocolError("feature probe result has the wrong manifest schema")
    compatibility = copy.deepcopy(result)
    compatibility["schema"] = PROBE_RESULT_SCHEMA
    compatibility["metadata"]["probe_manifest"] = manifest
    validate_result(compatibility, protocol, protocol_sha)


def main() -> None:
    repository = pathlib.Path(__file__).resolve().parents[1]
    protocol_file, protocol = load_protocol(repository)
    args = parse_args(protocol)
    manifest_file, manifest = load_and_validate(repository)
    features = select_features(manifest["features"], args.feature)
    output = args.output if args.output.is_absolute() else repository / args.output
    if output.suffix != ".json":
        raise SystemExit("feature probe --output must use the .json suffix")
    build_directory = repository / "benchmarks" / ".build" / "features"
    build_directory.mkdir(parents=True, exist_ok=True)
    default_mmay = repository.parent / "marimay" / "build" / "release" / "mmay"
    mmay_binary = pathlib.Path(os.environ.get("MMAY", str(default_mmay))).resolve()
    validate_executable(repository, mmay_binary)
    max_heap_bytes = protocol["resource"]["max_heap_bytes"]
    commands = (
        existing_features(features, build_directory)
        if args.skip_build
        else build_features(
            repository, mmay_binary, features, build_directory, max_heap_bytes
        )
    )
    metadata = capture_metadata(
        repository,
        mmay_binary,
        warmups=args.warmups,
        samples=args.samples,
        timeout_seconds=args.timeout,
        max_heap_bytes=max_heap_bytes,
        command=sys.argv,
    )
    metadata["corpus_revision"] = git_revision(repository, repository)
    metadata["comparison_scope"] = "local-only"
    metadata["feature_manifest"] = {
        "path": str(manifest_file.relative_to(repository)),
        "schema": manifest["schema"],
        "sha256": manifest_sha256(repository),
        "source_tree_sha256": source_tree_sha256(repository, manifest),
    }
    workload_ids = [feature["id"] for feature in features]
    expected = {
        feature["id"]: f"{feature['id']} {feature['expected_checksum']}\n"
        for feature in features
    }
    raw, order = measure_matrix(
        commands,
        expected,
        ["marimay"],
        workload_ids,
        args.warmups,
        args.samples,
        lambda command, stdout: timed_run(
            command, stdout, repository, args.timeout
        ),
    )
    finish_metadata(metadata)
    summarized = summarize_matrix(raw)
    workloads = {
        feature["id"]: {
            "category": feature["category"],
            "description": feature["description"],
            "expected_checksum": feature["expected_checksum"],
            "expected_stdout": expected[feature["id"]],
            "commands": {"marimay": commands["marimay"][feature["id"]]},
            "raw_ms": raw[feature["id"]],
            "summary": summarized[feature["id"]],
        }
        for feature in features
    }
    result = {
        "schema": FEATURE_RESULT_SCHEMA,
        "protocol": {
            "schema": protocol["schema"],
            "path": str(protocol_file.relative_to(repository)),
            "sha256": sha256_file(protocol_file),
        },
        "metadata": metadata,
        "workloads": workloads,
        "order": order,
    }
    protocol_sha = sha256_file(protocol_file)
    validate_feature_result(result, protocol, protocol_sha)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for workload in workload_ids:
        stats = summarized[workload]["marimay"]
        print(
            f"{workload}: median={stats['median_ms']:.3f} ms, "
            f"MAD={stats['mad_ms']:.3f} ms, IQR={stats['iqr_ms']:.3f} ms"
        )
    print(f"Raw feature probe report: {output}")


if __name__ == "__main__":
    try:
        main()
    except ProtocolError as error:
        raise SystemExit(f"feature probe error: {error}") from error
