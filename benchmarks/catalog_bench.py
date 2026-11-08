#!/usr/bin/env python3
"""Build, verify and measure the application matrix without changing Tier 1 budgets."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from catalog_bun import bun_path, pin_bun, bun_command
from catalog_contract import (
    ENGINE_MATRICES,
    SCHEMA,
    load_manifest,
    require,
    select_workloads,
    source_hashes,
    validate_result,
)
from catalog_oracle import expected
from catalog_measure import measure_catalog
from catalog_report import console_report, markdown_report
from catalog_session import RunJournal, show_journal, verify_inputs
from catalog_snapshot import compiler_path, create_workspace, pin_toolchain, pin_external_executables
from equivalence import load_and_validate as load_anchors
from expanded_workloads import load_and_validate as load_expanded
from marimay_toolchain import validate_executable
from perf_environment import (
    capture_metadata,
    finish_metadata,
    git_revision,
    run_checked,
)
from perf_protocol import (
    ProtocolError,
    load_json,
    load_protocol,
    sha256_file,
    summarize,
    validate_run_shape,
)
from run import build_binaries, measured_run


def parse_args(protocol):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["smoke", "standard"], default="standard")
    parser.add_argument("--engine", choices=list(ENGINE_MATRICES), default="both",
                        help="both: all five participants; native: Marimay/Go/Rust; vm or bun: one runtime")
    parser.add_argument(
        "--workload", action="append", help="select a catalogue workload; repeatable"
    )
    parser.add_argument(
        "--anchors",
        action="store_true",
        help="also run the historical 11 algorithm workloads with their fixed inputs",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="three checksum runs per participant; no performance conclusion",
    )
    parser.add_argument("--samples", type=int)
    parser.add_argument("--warmups", type=int)
    output = parser.add_mutually_exclusive_group()
    output.add_argument(
        "--output", type=Path, default=Path("benchmarks/results/catalog-local.md")
    )
    output.add_argument(
        "--console",
        action="store_true",
        help="print a compact timing table without writing Markdown/JSON reports",
    )
    parser.add_argument(
        "--validate", type=Path, help="validate an existing JSON result, then exit"
    )
    parser.add_argument(
        "--show-journal", type=Path,
        help="print saved observations from a completed or interrupted run; no rerun",
    )
    args = parser.parse_args()
    diagnostic = args.verify_only or args.profile == "smoke"
    args.samples = (
        args.samples
        if args.samples is not None
        else (3 if diagnostic else protocol["measurement"]["minimum_samples"])
    )
    args.warmups = (
        args.warmups
        if args.warmups is not None
        else (0 if diagnostic else protocol["measurement"]["minimum_warmups"])
    )
    require(
        args.samples >= 3 and args.warmups >= 0,
        "at least three samples are required and warmups nonnegative",
    )
    if not diagnostic:
        validate_run_shape(protocol, args.warmups, args.samples)
    require(
        args.output.suffix == ".md",
        "--output must end in .md; companion JSON is written automatically",
    )
    require(
        not (args.anchors and args.profile == "smoke"),
        "anchors have fixed full-size inputs; use --profile standard --anchors",
    )
    return args


def build_catalog(repository, mmay, build_dir, participants, heap, bun=None):
    commands = {}
    if "bun" in participants:
        commands["bun"] = bun_command(bun, repository / "typescript/src/catalog/main.ts")
    if "go" in participants:
        output = build_dir / "go-catalog"
        run_checked(
            ["go", "build", "-trimpath", "-o", str(output), "./cmd/catalog"],
            cwd=repository / "go",
        )
        commands["go"] = [str(output)]
    if "rust" in participants:
        run_checked(
            ["cargo", "build", "--release", "--bin", "catalog"], cwd=repository / "rust"
        )
        commands["rust"] = [str(repository / "rust/target/release/catalog")]
    target = repository / "marimay/catalog"
    if any(p.startswith("marimay-") for p in participants):
        run_checked([str(mmay), "fmt", str(target), "--check"], cwd=repository)
        run_checked([str(mmay), "check", str(target)], cwd=repository)
    if "marimay-native" in participants:
        output = build_dir / "marimay-catalog"
        run_checked(
            [
                str(mmay),
                "build",
                str(target),
                "--release",
                "--max-heap-bytes",
                str(heap),
                "--output",
                str(output),
            ],
            cwd=repository,
            timeout=600,
        )
        commands["marimay-native"] = [str(output)]
    if "marimay-vm" in participants:
        commands["marimay-vm"] = [
            str(mmay),
            "run",
            str(target),
            "--engine",
            "vm",
            "--max-heap-bytes",
            str(heap),
            "--",
        ]
    return commands


def append_anchors(repository, mmay, build_dir, participants, heap, commands, rows, bun=None):
    canonical_path, canonical = load_anchors(repository)
    expanded_path, expanded = load_expanded(repository, canonical)
    anchors = canonical["workloads"] + expanded["workloads"]
    names = [w["id"] for w in anchors]
    languages = ["marimay" if p == "marimay-native" else p for p in participants
                 if p in ("marimay-native", "go", "rust")]
    native = build_binaries(repository, build_dir, languages, mmay, names, heap)
    for workload in anchors:
        name = workload["id"]
        rows[name] = {
            "anchor": True,
            "description": workload["description"],
            "expected_checksum": workload["expected_checksum"],
        }
        if name in ("stack", "queue", "min-heap", "heap-sort", "dijkstra"):
            rows[name]["go_ratio_target"] = 1.3
        for p in participants:
            if p == "bun":
                commands[p][name] = bun_command(bun, repository / "typescript/src/benchmark.ts") + [name]
            elif p == "marimay-vm":
                commands[p][name] = [
                    str(mmay),
                    "run",
                    str(repository / "marimay/benchmarks" / name.replace("-", "_")),
                    "--engine",
                    "vm",
                    "--max-heap-bytes",
                    str(heap),
                ]
            else:
                commands[p][name] = native["marimay" if p == "marimay-native" else p][
                    name
                ]
    # Include all sources and entrypoints which contribute to historical anchors.
    paths = {canonical_path, expanded_path}
    for pattern in ("marimay/**/*.my", "go/**/*.go", "rust/src/**/*.rs", "typescript/src/**/*.ts"):
        paths.update(repository.glob(pattern))
    return {
        str(p.relative_to(repository)): sha256_file(p)
        for p in sorted(paths)
        if ".mmay" not in p.parts
    }


def main():
    repository = Path(__file__).resolve().parents[1]
    protocol_path, protocol = load_protocol(repository)
    args = parse_args(protocol)
    if args.show_journal:
        print(show_journal(args.show_journal))
        return
    if args.validate:
        result = load_json(args.validate)
        validate_result(result, protocol)
        print(
            f"valid catalogue result: {args.validate} (benchmark status: {result['status']})"
        )
        return
    manifest = load_manifest(repository)
    workloads = select_workloads(manifest, args.workload)
    participants = ENGINE_MATRICES[args.engine]
    bun_source = bun_path() if "bun" in participants else None
    mmay = compiler_path(repository)
    validate_executable(repository, mmay)
    build_root = repository / "benchmarks/.build/catalog"
    build_dir = create_workspace(build_root / "runs")
    heap = protocol["resource"]["max_heap_bytes"]
    print(f"Building catalogue matrix: {', '.join(participants)}", flush=True)
    before = source_hashes(repository)
    metadata = capture_metadata(
        repository,
        mmay,
        warmups=args.warmups,
        samples=args.samples,
        timeout_seconds=protocol["measurement"]["timeout_seconds"],
        max_heap_bytes=heap,
        command=sys.argv,
    )
    mmay, toolchain_hashes = pin_toolchain(mmay, build_dir, metadata)
    validate_executable(repository, mmay)
    metadata["build_directory"] = str(build_dir)
    bun = pin_bun(bun_source, build_dir, metadata) if bun_source else None
    base_commands = build_catalog(repository, mmay, build_dir, participants, heap, bun)
    commands = {p: {} for p in participants}
    rows = {}
    for workload in workloads:
        name = workload["id"]
        params = workload["parameters"][args.profile]
        rows[name] = {
            "category": workload["category"],
            "description": workload["description"],
            "parameters": params,
            "expected_checksum": expected(name, **params),
        }
        if "go_ratio_target" in workload:
            rows[name]["go_ratio_target"] = workload["go_ratio_target"]
        for p in participants:
            commands[p][name] = base_commands[p] + [
                name,
                str(params["size"]),
                str(params["rounds"]),
            ]
    anchor_hashes = (
        append_anchors(repository, mmay, build_dir, participants, heap, commands, rows, bun)
        if args.anchors
        else {}
    )
    metadata.update(
        {
            "comparison_scope": "local-only",
            "profile": args.profile,
            "verify_only": args.verify_only,
            "participants": participants,
            "workload_manifest": manifest,
            "anchor_checksums": {
                name: row["expected_checksum"]
                for name, row in rows.items()
                if row.get("anchor")
            },
            "corpus_revision": git_revision(repository, repository),
            "source_sha256": before | anchor_hashes,
            "limitations": manifest["limitations"],
            "protocol_sha256": sha256_file(protocol_path),
            "engine_boundaries": {
                "native": "release executable; compilation excluded",
                "vm": "source run; checking/lowering included",
                "bun": "TypeScript source run; process startup, transpilation and JIT included; fresh process per observation",
            },
            "build_commands": {
                "go": "go build -trimpath ./cmd/catalog",
                "rust": "cargo build --release --bin catalog",
                "marimay-native": "mmay build marimay/catalog --release --max-heap-bytes 67108864",
            },
            "environment_overrides": {
                key: os.environ.get(key)
                for key in (
                    "GOFLAGS",
                    "GOGC",
                    "GOMEMLIMIT",
                    "RUSTFLAGS",
                    "CARGO_ENCODED_RUSTFLAGS",
                    "CC",
                    "CFLAGS",
                )
            },
        }
    )
    metadata["isolation"]["mode"] = "local-unverified"
    pin_external_executables(commands, build_dir)
    metadata["binaries"] = {
        command[0]: sha256_file(Path(command[0]))
        for per_workload in commands.values()
        for command in per_workload.values()
    }
    for path, digest in toolchain_hashes.items():
        require(
            sha256_file(Path(path)) == digest,
            "compiler/runtime changed while building; rerun",
        )
    expected_stdout = {
        name: f"{name} {row['expected_checksum']}\n" for name, row in rows.items()
    }
    print(
        f"Checking and measuring {len(rows)} workloads; {args.samples} samples + {args.warmups} warmups",
        flush=True,
    )
    def checkpoint(current, total):
        verify_inputs(repository, before, metadata["binaries"] | toolchain_hashes, anchor_hashes)
        print(f"Completed matrix round {current}/{total}", flush=True)

    with RunJournal(build_root / "journals", metadata, rows, commands) as journal:
        raw, order, outcomes = measure_catalog(
            commands,
            expected_stdout,
            participants,
            list(rows),
            args.warmups,
            args.samples,
            lambda command, stdout: measured_run(
                command, stdout, repository, metadata["timeout_seconds"]
            ),
            checkpoint,
            journal.observe,
        )
        finish_metadata(metadata)
        summaries = {
            w: {
                p: summarize(raw[w][p]) if outcomes[w][p]["status"] == "passed" else None
                for p in participants
            }
            for w in rows
        }
        for name, row in rows.items():
            row.update(
                {
                    "outcomes": outcomes[name],
                    "expected_stdout": expected_stdout[name],
                    "commands": {p: commands[p][name] for p in participants},
                    "raw_ms": raw[name],
                    "summary": summaries[name],
                }
            )
        status = (
            "failed"
            if any(
                o["status"] == "failed" for row in outcomes.values() for o in row.values()
            )
            else "passed"
        )
        result = {
            "schema": SCHEMA,
            "status": status,
            "metadata": metadata,
            "workloads": rows,
            "measurement_order": order,
        }
        validate_result(result, protocol)
        print(console_report(result), flush=True)
        if not args.console:
            output = args.output if args.output.is_absolute() else repository / args.output
            output.parent.mkdir(parents=True, exist_ok=True)
            output.with_suffix(".json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
            )
            output.write_text(markdown_report(result))
            print(f"Wrote {output} and {output.with_suffix('.json')}")
        journal.complete(status)

    if status == "failed":
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("catalog benchmark interrupted", file=sys.stderr)
        raise SystemExit(130)
    except (ProtocolError, OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"catalog benchmark failed: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError):
            print(error.stdout or "", file=sys.stderr)
            print(error.stderr or "", file=sys.stderr)
        raise SystemExit(1)
