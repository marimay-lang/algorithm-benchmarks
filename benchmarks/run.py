#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time
from typing import Sequence

from equivalence import load_and_validate, manifest_sha256
from perf_environment import capture_metadata, finish_metadata, git_revision
from perf_protocol import (
    ALGORITHM_RESULT_SCHEMA,
    ProtocolError,
    load_protocol,
    measure_matrix,
    sha256_file,
    summarize_matrix,
    validate_result,
    validate_run_shape,
)

LANGUAGES = ["ruda", "go", "rust"]


def parse_args(protocol: dict[str, object]) -> argparse.Namespace:
    measurement = protocol["measurement"]
    assert isinstance(measurement, dict)
    parser = argparse.ArgumentParser(
        description="Build and time identical Ruda, Go, and Rust workloads."
    )
    parser.add_argument("--samples", type=int, default=measurement["minimum_samples"])
    parser.add_argument("--warmups", type=int, default=measurement["minimum_warmups"])
    parser.add_argument("--timeout", type=int, default=measurement["timeout_seconds"])
    parser.add_argument(
        "--languages",
        default=",".join(LANGUAGES),
        help="comma-separated subset of ruda,go,rust",
    )
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("benchmarks/results/latest.md"),
    )
    args = parser.parse_args()
    try:
        validate_run_shape(protocol, args.warmups, args.samples)
    except ProtocolError as error:
        parser.error(str(error))
    if args.timeout != measurement["timeout_seconds"]:
        parser.error("Tier 1 benchmark timeout must match performance_protocol.json")
    selected = [item.strip() for item in args.languages.split(",") if item.strip()]
    if not selected or any(item not in LANGUAGES for item in selected):
        parser.error("languages must be a comma-separated subset of ruda,go,rust")
    if selected != LANGUAGES:
        parser.error("Tier 1 algorithm results require ruda,go,rust in protocol order")
    args.languages = selected
    return args


def run_checked(
    command: Sequence[str],
    *,
    cwd: pathlib.Path,
    timeout: int = 300,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )


def tool_version(command: Sequence[str], cwd: pathlib.Path) -> str:
    try:
        completed = run_checked(command, cwd=cwd, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return "unavailable"
    text = completed.stdout.strip() or completed.stderr.strip()
    return text.splitlines()[0] if text else "unknown"


def build_binaries(
    repository: pathlib.Path,
    build_dir: pathlib.Path,
    languages: Sequence[str],
    ruda_binary: pathlib.Path,
    benchmark_names: Sequence[str],
    max_heap_bytes: int,
) -> dict[str, dict[str, list[str]]]:
    commands: dict[str, dict[str, list[str]]] = {language: {} for language in languages}
    if "go" in languages:
        go_output = build_dir / "go-benchmark"
        run_checked(
            ["go", "build", "-trimpath", "-o", str(go_output), "./cmd/benchmark"],
            cwd=repository / "go",
        )
        for name in benchmark_names:
            commands["go"][name] = [str(go_output), name]

    if "rust" in languages:
        run_checked(
            ["cargo", "build", "--release", "--bin", "benchmark"],
            cwd=repository / "rust",
        )
        rust_output = repository / "rust" / "target" / "release" / "benchmark"
        for name in benchmark_names:
            commands["rust"][name] = [str(rust_output), name]

    if "ruda" in languages:
        if not ruda_binary.is_file() or not os.access(ruda_binary, os.X_OK):
            raise SystemExit(
                f"Ruda executable not found: {ruda_binary}\n"
                "Build Ruda or set RUDA=/absolute/path/to/ruda."
            )
        ruda_root = repository / "ruda"
        run_checked([str(ruda_binary), "fmt", str(ruda_root), "--check"], cwd=repository)
        run_checked([str(ruda_binary), "check", str(ruda_root)], cwd=repository)
        directory_names = {
            "insertion": "insertion",
            "heap-sort": "heap_sort",
            "stack": "stack",
            "queue": "queue",
            "min-heap": "min_heap",
            "dsu": "dsu",
            "bfs": "bfs",
            "dijkstra": "dijkstra",
        }
        for name in benchmark_names:
            output = build_dir / f"ruda-{name}"
            run_checked(
                [
                    str(ruda_binary),
                    "build",
                    str(ruda_root / "benchmarks" / directory_names[name]),
                    "--release",
                    "--max-heap-bytes",
                    str(max_heap_bytes),
                    "--output",
                    str(output),
                ],
                cwd=repository,
                timeout=600,
            )
            commands["ruda"][name] = [str(output)]
    return commands


def existing_commands(
    repository: pathlib.Path,
    build_dir: pathlib.Path,
    languages: Sequence[str],
    benchmark_names: Sequence[str],
) -> dict[str, dict[str, list[str]]]:
    commands: dict[str, dict[str, list[str]]] = {language: {} for language in languages}
    for language in languages:
        for name in benchmark_names:
            if language == "go":
                command = [str(build_dir / "go-benchmark"), name]
            elif language == "rust":
                command = [
                    str(repository / "rust" / "target" / "release" / "benchmark"),
                    name,
                ]
            else:
                command = [str(build_dir / f"ruda-{name}")]
            if not pathlib.Path(command[0]).is_file():
                raise SystemExit(f"missing binary for --skip-build: {command[0]}")
            commands[language][name] = command
    return commands


def measured_run(
    command: Sequence[str], expected: str, cwd: pathlib.Path, timeout: int
) -> float:
    started = time.perf_counter_ns()
    try:
        completed = run_checked(command, cwd=cwd, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise ProtocolError(
            f"benchmark timed out after {timeout} seconds: {' '.join(command)}"
        ) from error
    except subprocess.CalledProcessError as error:
        raise ProtocolError(
            f"benchmark exited {error.returncode}: {' '.join(command)}\n{error.stderr}"
        ) from error
    elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
    if completed.stdout != expected or completed.stderr != "":
        raise ProtocolError(
            f"checksum observation mismatch for {' '.join(command)}: "
            f"stdout={completed.stdout!r}, stderr={completed.stderr!r}, "
            f"expected stdout={expected!r}"
        )
    return elapsed_ms


def measure(
    repository: pathlib.Path,
    commands: dict[str, dict[str, list[str]]],
    languages: Sequence[str],
    warmups: int,
    samples: int,
    timeout: int,
    workloads: Sequence[dict[str, object]],
) -> tuple[dict[str, dict[str, list[float]]], list[dict[str, object]]]:
    names = [str(workload["id"]) for workload in workloads]
    expected = {
        str(workload["id"]): (
            f"{workload['id']} {workload['expected_checksum']}\n"
        )
        for workload in workloads
    }
    return measure_matrix(
        commands,
        expected,
        languages,
        names,
        warmups,
        samples,
        lambda command, stdout: measured_run(command, stdout, repository, timeout),
    )


def markdown_report(
    metadata: dict[str, object],
    summarized: dict[str, dict[str, dict[str, float]]],
    languages: Sequence[str],
    workloads: Sequence[dict[str, object]],
) -> str:
    warmup_label = "warm-up run" if metadata["warmups"] == 1 else "warm-up runs"
    ratio_languages = [
        language
        for language in ("go", "rust")
        if "ruda" in languages and language in languages
    ]
    table_headers = [
        "Algorithm",
        "Workload",
        *(language.capitalize() + " median" for language in languages),
        *("Ruda / " + language.capitalize() for language in ratio_languages),
        "Fastest",
    ]
    lines = [
        "# Latest algorithm benchmark",
        "",
        f"Generated: `{metadata['generated_at']}`",
        "",
        f"Host: `{metadata['platform']['system']} {metadata['platform']['release']} "
        f"{metadata['platform']['machine']}`; CPU: `{metadata['platform']['cpu']}`.",
        "",
        f"Ruda compiler executable: `{metadata['artifacts']['ruda_compiler']['path']}`.",
        "",
        f"Ruda source revision: `{metadata['artifacts']['ruda_compiler']['revision']}`.",
        "",
        f"Algorithm corpus revision: `{metadata['corpus_revision']}`.",
        "",
        f"Equivalence manifest: `{metadata['equivalence_manifest']['path']}` "
        f"(`{metadata['equivalence_manifest']['sha256']}`).",
        "",
        f"Samples: {metadata['samples']} measured after {metadata['warmups']} {warmup_label}. "
        "Reported times include process startup and one fixed checksum line; compilation is excluded.",
        "",
        "| " + " | ".join(table_headers) + " |",
        "|---|---|"
        + "---:|" * len(languages)
        + "---:|" * len(ratio_languages)
        + "---:|",
    ]
    for workload in workloads:
        name = str(workload["id"])
        timings = summarized[name]
        fastest_language = min(languages, key=lambda language: timings[language]["median_ms"])
        row = [name, str(workload["description"])]
        row.extend(f"{timings[language]['median_ms']:.2f} ms" for language in languages)
        row.extend(
            f"{timings['ruda']['median_ms'] / timings[language]['median_ms']:.1f}×"
            for language in ratio_languages
        )
        row.append(fastest_language.capitalize())
        lines.append("| " + " | ".join(row) + " |")
    lines.extend(
        [
            "",
            "## Range (min–max)",
            "",
            "| Algorithm | " + " | ".join(language.capitalize() for language in languages) + " |",
            "|---|" + "---:|" * len(languages),
        ]
    )
    for workload in workloads:
        name = str(workload["id"])
        row = [name]
        row.extend(
            f"{summarized[name][language]['min_ms']:.2f}–{summarized[name][language]['max_ms']:.2f} ms"
            for language in languages
        )
        lines.append("| " + " | ".join(row) + " |")
    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- Checksums prove matching selected results, not identical abstraction boundaries.",
            "- All three languages call reusable sorting, structures, and graph packages.",
            "- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;",
            "  Ruda and Rust model absence with Option while Go returns a value/bool pair.",
            "- Checksums cover selected results and do not prove equal compiler optimization maturity.",
            "",
        ]
    )
    lines.extend(
        [
            "",
            "## Toolchains",
            "",
            *[f"- {name}: `{version}`" for name, version in metadata["toolchains"].items()],
            "",
            "Checksums are identical across every language and every measured run. "
            "These are local comparative numbers, not stable language performance claims.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    repository = pathlib.Path(__file__).resolve().parents[1]
    protocol_file, protocol = load_protocol(repository)
    args = parse_args(protocol)
    manifest_path, manifest = load_and_validate(repository)
    workloads = manifest["workloads"]
    benchmark_names = [str(workload["id"]) for workload in workloads]
    output = args.output
    if not output.is_absolute():
        output = repository / output
    build_dir = repository / "benchmarks" / ".build"
    build_dir.mkdir(parents=True, exist_ok=True)
    default_ruda = repository.parent / "Ma" / "build" / "release" / "ruda"
    ruda_binary = pathlib.Path(os.environ.get("RUDA", str(default_ruda))).resolve()
    max_heap_bytes = protocol["resource"]["max_heap_bytes"]
    if args.skip_build:
        commands = existing_commands(
            repository, build_dir, args.languages, benchmark_names
        )
    else:
        commands = build_binaries(
            repository,
            build_dir,
            args.languages,
            ruda_binary,
            benchmark_names,
            max_heap_bytes,
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
    metadata["equivalence_manifest"] = {
        "path": str(manifest_path.relative_to(repository)),
        "schema": manifest["schema"],
        "sha256": manifest_sha256(manifest_path),
    }
    raw, order = measure(
        repository,
        commands,
        args.languages,
        args.warmups,
        args.samples,
        args.timeout,
        workloads,
    )
    finish_metadata(metadata)
    metadata["languages"] = args.languages
    summarized = summarize_matrix(raw)
    expected = {
        str(workload["id"]): (
            f"{workload['id']} {workload['expected_checksum']}\n"
        )
        for workload in workloads
    }
    result_workloads = {
        str(workload["id"]): {
            "description": workload["description"],
            "expected_checksum": workload["expected_checksum"],
            "expected_stdout": expected[str(workload["id"])],
            "commands": {
                language: commands[language][str(workload["id"])]
                for language in args.languages
            },
            "raw_ms": raw[str(workload["id"])],
            "summary": summarized[str(workload["id"])],
        }
        for workload in workloads
    }
    result = {
        "schema": ALGORITHM_RESULT_SCHEMA,
        "protocol": {
            "schema": protocol["schema"],
            "path": str(protocol_file.relative_to(repository)),
            "sha256": sha256_file(protocol_file),
        },
        "metadata": metadata,
        "workloads": result_workloads,
        "order": order,
    }
    validate_result(result, protocol, sha256_file(protocol_file))
    for name in benchmark_names:
        medians = ", ".join(
            f"{language}={summarized[name][language]['median_ms']:.2f} ms"
            for language in args.languages
        )
        print(f"{name}: {medians}", flush=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        markdown_report(metadata, summarized, args.languages, workloads),
        encoding="utf-8",
    )
    json_output = output.with_suffix(".json")
    json_output.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Markdown report: {output}")
    print(f"Raw JSON report: {json_output}")


if __name__ == "__main__":
    try:
        main()
    except ProtocolError as error:
        raise SystemExit(f"performance protocol error: {error}") from error
