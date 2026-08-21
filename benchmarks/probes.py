#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import time
from collections.abc import Sequence
from typing import Any

from perf_environment import (
    capture_metadata,
    finish_metadata,
    git_revision,
    run_checked,
)
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
from probe_manifest import load_and_validate, manifest_sha256, source_tree_sha256


def parse_args(protocol: dict[str, Any]) -> argparse.Namespace:
    measurement = protocol["measurement"]
    parser = argparse.ArgumentParser(
        description="Build and measure focused Ruda managed-array probes."
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
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("benchmarks/results/cp21-probes-local.json"),
    )
    args = parser.parse_args()
    try:
        validate_run_shape(protocol, args.warmups, args.samples)
    except ProtocolError as error:
        parser.error(str(error))
    if args.timeout != measurement["timeout_seconds"]:
        parser.error("Tier 1 probe timeout must match performance_protocol.json")
    return args


def build_probes(
    repository: pathlib.Path,
    ruda_binary: pathlib.Path,
    probes: Sequence[dict[str, Any]],
    build_directory: pathlib.Path,
    max_heap_bytes: int,
) -> dict[str, dict[str, list[str]]]:
    ruda_root = repository / "ruda"
    run_checked([str(ruda_binary), "fmt", str(ruda_root), "--check"], cwd=repository)
    run_checked([str(ruda_binary), "check", str(ruda_root)], cwd=repository)
    commands: dict[str, dict[str, list[str]]] = {"ruda": {}}
    for probe in probes:
        probe_id = probe["id"]
        output = build_directory / f"ruda-probe-{probe_id}"
        run_checked(
            [
                str(ruda_binary),
                "build",
                str(repository / probe["source_directory"]),
                "--release",
                "--max-heap-bytes",
                str(max_heap_bytes),
                "--output",
                str(output),
            ],
            cwd=repository,
            timeout=600,
        )
        commands["ruda"][probe_id] = [str(output)]
    return commands


def existing_probes(
    probes: Sequence[dict[str, Any]], build_directory: pathlib.Path
) -> dict[str, dict[str, list[str]]]:
    commands: dict[str, dict[str, list[str]]] = {"ruda": {}}
    for probe in probes:
        path = build_directory / f"ruda-probe-{probe['id']}"
        if not path.is_file() or not os.access(path, os.X_OK):
            raise ProtocolError(f"missing binary for --skip-build: {path}")
        commands["ruda"][probe["id"]] = [str(path)]
    return commands


def timed_run(
    command: Sequence[str], expected_stdout: str, repository: pathlib.Path, timeout: int
) -> float:
    started = time.perf_counter_ns()
    try:
        completed = run_checked(command, cwd=repository, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise ProtocolError(
            f"probe timed out after {timeout} seconds: {' '.join(command)}"
        ) from error
    except subprocess.CalledProcessError as error:
        raise ProtocolError(
            f"probe exited {error.returncode}: {' '.join(command)}\n{error.stderr}"
        ) from error
    elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
    if completed.stdout != expected_stdout or completed.stderr != "":
        raise ProtocolError(
            f"probe observation mismatch for {' '.join(command)}: "
            f"stdout={completed.stdout!r}, stderr={completed.stderr!r}"
        )
    return elapsed_ms


def main() -> None:
    repository = pathlib.Path(__file__).resolve().parents[1]
    protocol_file, protocol = load_protocol(repository)
    args = parse_args(protocol)
    manifest_file, manifest = load_and_validate(repository)
    probes = manifest["probes"]
    output = args.output if args.output.is_absolute() else repository / args.output
    if output.suffix != ".json":
        raise SystemExit("probe --output must use the .json suffix")
    build_directory = repository / "benchmarks" / ".build" / "probes"
    build_directory.mkdir(parents=True, exist_ok=True)
    default_ruda = repository.parent / "Ma" / "build" / "release" / "ruda"
    ruda_binary = pathlib.Path(os.environ.get("RUDA", str(default_ruda))).resolve()
    max_heap_bytes = protocol["resource"]["max_heap_bytes"]
    commands = (
        existing_probes(probes, build_directory)
        if args.skip_build
        else build_probes(
            repository, ruda_binary, probes, build_directory, max_heap_bytes
        )
    )
    metadata = capture_metadata(
        repository,
        ruda_binary,
        warmups=args.warmups,
        samples=args.samples,
        timeout_seconds=args.timeout,
        max_heap_bytes=max_heap_bytes,
        command=sys.argv,
    )
    metadata["corpus_revision"] = git_revision(repository, repository)
    metadata["probe_manifest"] = {
        "path": str(manifest_file.relative_to(repository)),
        "schema": manifest["schema"],
        "sha256": manifest_sha256(repository),
        "source_tree_sha256": source_tree_sha256(repository, manifest),
    }
    workload_ids = [probe["id"] for probe in probes]
    expected = {
        probe["id"]: f"{probe['id']} {probe['expected_checksum']}\n"
        for probe in probes
    }
    raw, order = measure_matrix(
        commands,
        expected,
        ["ruda"],
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
        probe["id"]: {
            "category": probe["category"],
            "description": probe["description"],
            "expected_checksum": probe["expected_checksum"],
            "expected_stdout": expected[probe["id"]],
            "commands": {"ruda": commands["ruda"][probe["id"]]},
            "raw_ms": raw[probe["id"]],
            "summary": summarized[probe["id"]],
        }
        for probe in probes
    }
    result = {
        "schema": PROBE_RESULT_SCHEMA,
        "protocol": {
            "schema": protocol["schema"],
            "path": str(protocol_file.relative_to(repository)),
            "sha256": sha256_file(protocol_file),
        },
        "metadata": metadata,
        "workloads": workloads,
        "order": order,
    }
    validate_result(result, protocol, sha256_file(protocol_file))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for workload in workload_ids:
        stats = summarized[workload]["ruda"]
        print(
            f"{workload}: median={stats['median_ms']:.3f} ms, "
            f"MAD={stats['mad_ms']:.3f} ms, IQR={stats['iqr_ms']:.3f} ms"
        )
    print(f"Raw probe report: {output}")


if __name__ == "__main__":
    try:
        main()
    except ProtocolError as error:
        raise SystemExit(f"performance protocol error: {error}") from error
