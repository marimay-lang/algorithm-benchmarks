"""Manifest and result integrity for the local application matrix."""

from __future__ import annotations

import json
import math

from catalog_oracle import expected
from perf_protocol import (
    ProtocolError,
    load_json,
    sha256_file,
    schedule,
    summarize,
    validate_run_shape,
)

SCHEMA = "marimay.catalog-benchmark/1"
LEGACY_PARTICIPANTS = ["marimay-native", "go", "rust", "marimay-vm"]
PARTICIPANTS = [*LEGACY_PARTICIPANTS, "bun"]
ENGINE_MATRICES = {
    "both": PARTICIPANTS,
    "native": ["marimay-native", "go", "rust"],
    "vm": ["marimay-vm"],
    "bun": ["bun"],
}
SOURCE_PATTERNS = [
    "marimay/catalog/**/*.my",
    "go/catalog/*.go",
    "go/cmd/catalog/*.go",
    "rust/src/catalog/*.rs",
    "rust/src/bin/catalog.rs",
    "typescript/src/**/*.ts",
]
HARNESS_FILES = [
    "benchmarks/catalog_workloads.json",
    "benchmarks/catalog_oracle.py",
    "benchmarks/catalog_measure.py",
    "benchmarks/catalog_session.py",
    "benchmarks/catalog_snapshot.py",
    "benchmarks/catalog_bun.py",
    "benchmarks/catalog_contract.py",
    "benchmarks/catalog_report.py",
    "benchmarks/catalog_bench.py",
    "benchmarks/perf_protocol.py",
    "benchmarks/perf_environment.py",
    "benchmarks/marimay_toolchain.py",
    "benchmarks/marimay-toolchain.json",
    "benchmarks/performance_protocol.json",
    "go/go.mod",
    "rust/Cargo.toml",
    "rust/Cargo.lock",
    "rust/src/lib.rs",
    "marimay/mmay.mod",
]


def require(condition, message):
    if not condition:
        raise ProtocolError(message)


def load_manifest(repository):
    path = repository / "benchmarks/catalog_workloads.json"
    manifest = load_json(path)
    return validate_manifest(manifest)


def validate_manifest(manifest):
    require(
        manifest.get("schema") == "marimay.catalog-workloads/1",
        "catalog manifest schema",
    )
    require(
        manifest.get("scope") == "local-only", "catalog scope must remain local-only"
    )
    require(
        manifest.get("participants") in (PARTICIPANTS, LEGACY_PARTICIPANTS),
        "catalog participants drifted",
    )
    require(
        manifest.get("profiles") == ["smoke", "standard"], "catalog profiles drifted"
    )
    seen = set()
    for row in manifest["workloads"]:
        identifier = row["id"]
        require(
            identifier not in seen and isinstance(identifier, str), "duplicate workload"
        )
        seen.add(identifier)
        for profile in manifest["profiles"]:
            params = row["parameters"][profile]
            require(set(params) == {"size", "rounds"}, "unknown workload parameter")
            require(
                all(type(v) is int and 0 < v <= 1_000_000 for v in params.values()),
                "invalid workload size/rounds",
            )
            require(
                params["size"] * params["rounds"] <= 20_000_000,
                "workload exceeds bounded operation count",
            )
            expected(identifier, **params)
    require(bool(seen), "empty workload manifest")
    return manifest


def source_hashes(repository):
    paths = {repository / p for p in HARNESS_FILES}
    for pattern in SOURCE_PATTERNS:
        paths.update(repository.glob(pattern))
    return {str(p.relative_to(repository)): sha256_file(p) for p in sorted(paths)}


def select_workloads(manifest, requested):
    if not requested:
        return list(manifest["workloads"])
    known = {row["id"] for row in manifest["workloads"]}
    require(len(requested) == len(set(requested)), "duplicate workload selection")
    require(
        set(requested) <= known, f"unknown workloads: {sorted(set(requested) - known)}"
    )
    return [row for row in manifest["workloads"] if row["id"] in requested]


def validate_result(result, protocol):
    try:
        _validate_result(result, protocol)
    except (KeyError, TypeError, IndexError) as error:
        raise ProtocolError(f"malformed catalogue result: {error}") from error


def _validate_result(result, protocol):
    require(result.get("schema") == SCHEMA, "unsupported catalog result schema")
    meta = result["metadata"]
    require(meta["comparison_scope"] == "local-only", "catalog results are local-only")
    require(meta["profile"] in ("smoke", "standard"), "unknown profile")
    manifest = validate_manifest(meta["workload_manifest"])
    contract = {row["id"]: row for row in manifest["workloads"]}
    participants = meta["participants"]
    require(
        participants in [manifest["participants"], *list(ENGINE_MATRICES.values())[1:]]
        and set(participants) <= set(manifest["participants"]),
        "invalid engine matrix",
    )
    if "bun" in participants:
        require(isinstance(meta["bun_runtime"]["version"], str)
                and bool(meta["bun_runtime"]["version"]), "missing Bun version")
        require(meta["binaries"].get(meta["bun_runtime"]["path"])
                == meta["bun_runtime"]["sha256"], "Bun runtime identity mismatch")
    if meta["profile"] == "standard" and not meta["verify_only"]:
        validate_run_shape(protocol, meta["warmups"], meta["samples"])
    require(type(meta["samples"]) is int and meta["samples"] >= 3, "invalid samples")
    require(type(meta["warmups"]) is int and meta["warmups"] >= 0, "invalid warmups")
    require(type(meta["verify_only"]) is bool, "invalid verify-only marker")
    require(
        meta["timeout_seconds"] == protocol["measurement"]["timeout_seconds"],
        "timeout protocol drifted",
    )
    require(
        meta["resource"]["max_heap_bytes"] == protocol["resource"]["max_heap_bytes"],
        "heap budget drifted",
    )
    require(bool(meta["source_sha256"]), "missing source hashes")
    for path, digest in meta["source_sha256"].items():
        require(
            isinstance(path, str)
            and len(digest) == 64
            and all(c in "0123456789abcdef" for c in digest),
            "invalid source hash",
        )
    workloads = result["workloads"]
    require(bool(workloads), "empty results")
    ids = list(workloads)
    events = schedule(ids, participants, meta["warmups"], meta["samples"])
    require(
        len(events) == len(result["measurement_order"]), "incomplete measurement order"
    )
    observed = {w: {p: [] for p in participants} for w in ids}
    failures = {}
    for want, got in zip(events, result["measurement_order"]):
        require(
            all(got.get(k) == v for k, v in want.items()), "measurement order drifted"
        )
        key = (got["workload"], got["participant"])
        if key in failures:
            require(
                got.get("status") == "skipped-after-failure"
                and "elapsed_ms" not in got,
                "failed cell was measured again",
            )
            continue
        if got.get("status") == "failed":
            require(
                isinstance(got.get("error"), str)
                and bool(got["error"])
                and "elapsed_ms" not in got,
                "failure lacks diagnostic",
            )
            failures[key] = got["error"]
            continue
        require(got.get("status") == "passed", "unknown observation status")
        # Validate warmups too; they are excluded from summary statistics.
        require(
            type(got["elapsed_ms"]) in (int, float)
            and math.isfinite(got["elapsed_ms"])
            and got["elapsed_ms"] > 0,
            "invalid elapsed time",
        )
        if got["phase"] == "sample":
            observed[got["workload"]][got["participant"]].append(got["elapsed_ms"])
    require(
        result.get("status") == ("failed" if failures else "passed"),
        "overall status mismatch",
    )
    for identifier, row in workloads.items():
        if row.get("anchor"):
            require(
                identifier in meta["anchor_checksums"]
                and row["expected_checksum"] == meta["anchor_checksums"][identifier],
                "invalid anchor checksum",
            )
        else:
            require(identifier in contract, "unknown workload")
            require(
                row["parameters"]
                == contract[identifier]["parameters"][meta["profile"]],
                "profile input drifted",
            )
            require(
                row.get("go_ratio_target")
                == contract[identifier].get("go_ratio_target"),
                "ratio target drifted",
            )
            require(
                row["expected_checksum"] == expected(identifier, **row["parameters"]),
                "oracle checksum mismatch",
            )
        require(
            row["expected_stdout"] == f"{identifier} {row['expected_checksum']}\n",
            "stdout contract drifted",
        )
        for field in ("commands", "raw_ms", "summary", "outcomes"):
            require(
                list(row[field]) == participants, f"incomplete {identifier}.{field}"
            )
        for participant in participants:
            command = row["commands"][participant]
            require(
                isinstance(command, list)
                and bool(command)
                and all(isinstance(s, str) for s in command),
                "invalid command",
            )
            require(command[0] in meta["binaries"], "missing executable identity")
            require(len(meta["binaries"][command[0]]) == 64, "invalid executable hash")
            if participant == "marimay-vm":
                require(
                    "--engine" in command
                    and command[command.index("--engine") + 1] == "vm",
                    "VM command engine mismatch",
                )
            if participant == "bun":
                require(command[0] == meta["bun_runtime"]["path"]
                        and command[1:4] == ["--no-env-file", "--no-install", "run"]
                        and command[4].endswith(".ts"), "Bun command engine mismatch")
            if not row.get("anchor"):
                require(
                    command[-3:]
                    == [
                        identifier,
                        str(row["parameters"]["size"]),
                        str(row["parameters"]["rounds"]),
                    ],
                    "command input drifted",
                )
            require(
                row["raw_ms"][participant] == observed[identifier][participant],
                "raw/order mismatch",
            )
            outcome = row["outcomes"][participant]
            failure = failures.get((identifier, participant))
            if failure:
                require(
                    outcome == {"status": "failed", "error": failure},
                    "failure diagnostic mismatch",
                )
                require(
                    row["summary"][participant] is None,
                    "failed cell must not have a performance summary",
                )
                continue
            require(outcome == {"status": "passed"}, "passed cell outcome mismatch")
            require(
                len(row["raw_ms"][participant]) == meta["samples"],
                "missing measured samples",
            )
            require(
                row["summary"][participant] == summarize(row["raw_ms"][participant]),
                "summary mismatch",
            )
    # JSON serialization rejects NaN/Infinity anywhere else in metadata.
    json.dumps(result, allow_nan=False)
