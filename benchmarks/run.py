#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import platform
import shutil
import statistics
import subprocess
import sys
import time
from typing import Sequence

from equivalence import load_and_validate, manifest_sha256

LANGUAGES = ["ruda", "go", "rust"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and time identical Ruda, Go, and Rust workloads."
    )
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--warmups", type=int, default=1)
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
    if args.samples < 1 or args.warmups < 0:
        parser.error("samples must be positive and warmups must be non-negative")
    selected = [item.strip() for item in args.languages.split(",") if item.strip()]
    if not selected or any(item not in LANGUAGES for item in selected):
        parser.error("languages must be a comma-separated subset of ruda,go,rust")
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


def cpu_name() -> str:
    if sys.platform == "darwin":
        try:
            return subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
            ).strip()
        except (OSError, subprocess.SubprocessError):
            pass
    return platform.processor() or platform.machine()


def source_revision(executable: pathlib.Path, cwd: pathlib.Path) -> str:
    for candidate in executable.parents:
        if (candidate / ".git").exists():
            return tool_version(
                ["git", "-C", str(candidate), "rev-parse", "HEAD"], cwd
            )
    return "unavailable"


def build_binaries(
    repository: pathlib.Path,
    build_dir: pathlib.Path,
    languages: Sequence[str],
    ruda_binary: pathlib.Path,
    benchmark_names: Sequence[str],
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


def measured_run(command: Sequence[str], expected: str, cwd: pathlib.Path) -> float:
    started = time.perf_counter_ns()
    completed = run_checked(command, cwd=cwd, timeout=180)
    elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
    actual = completed.stdout.strip()
    if actual != expected:
        raise RuntimeError(
            f"checksum output mismatch for {' '.join(command)}: {actual!r} != {expected!r}"
        )
    return elapsed_ms


def measure(
    repository: pathlib.Path,
    commands: dict[str, dict[str, list[str]]],
    languages: Sequence[str],
    warmups: int,
    samples: int,
    workloads: Sequence[dict[str, object]],
) -> dict[str, dict[str, list[float]]]:
    raw: dict[str, dict[str, list[float]]] = {
        str(workload["id"]): {language: [] for language in languages}
        for workload in workloads
    }
    for workload in workloads:
        name = str(workload["id"])
        expected = f"{name} {workload['expected_checksum']}"
        for _ in range(warmups):
            for language in languages:
                measured_run(commands[language][name], expected, repository)
        for sample in range(samples):
            offset = sample % len(languages)
            order = list(languages[offset:]) + list(languages[:offset])
            for language in order:
                elapsed = measured_run(commands[language][name], expected, repository)
                raw[name][language].append(elapsed)
        medians = ", ".join(
            f"{language}={statistics.median(raw[name][language]):.2f} ms"
            for language in languages
        )
        print(f"{name}: {medians}", flush=True)
    return raw


def summary(raw: dict[str, dict[str, list[float]]]) -> dict[str, dict[str, dict[str, float]]]:
    return {
        name: {
            language: {
                "median_ms": statistics.median(samples),
                "min_ms": min(samples),
                "max_ms": max(samples),
            }
            for language, samples in language_samples.items()
        }
        for name, language_samples in raw.items()
    }


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
        f"Host: `{metadata['platform']}`; CPU: `{metadata['cpu']}`.",
        "",
        f"Ruda compiler executable: `{metadata['ruda_compiler']}`.",
        "",
        f"Ruda source revision: `{metadata['ruda_revision']}`.",
        "",
        f"Algorithm corpus revision: `{metadata['corpus_revision']}`.",
        "",
        f"Equivalence manifest: `{metadata['equivalence_manifest']}` "
        f"(`{metadata['equivalence_sha256']}`).",
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
    args = parse_args()
    repository = pathlib.Path(__file__).resolve().parents[1]
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
        )

    raw = measure(
        repository,
        commands,
        args.languages,
        args.warmups,
        args.samples,
        workloads,
    )
    summarized = summary(raw)
    metadata: dict[str, object] = {
        "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "platform": platform.platform(),
        "cpu": cpu_name(),
        "samples": args.samples,
        "warmups": args.warmups,
        "languages": args.languages,
        "ruda_compiler": str(ruda_binary),
        "ruda_revision": source_revision(ruda_binary, repository),
        "corpus_revision": tool_version(
            ["git", "-C", str(repository), "rev-parse", "HEAD"], repository
        ),
        "equivalence_manifest": str(manifest_path.relative_to(repository)),
        "equivalence_schema": manifest["schema"],
        "equivalence_sha256": manifest_sha256(manifest_path),
        "toolchains": {
            "Ruda": tool_version([str(ruda_binary), "--version"], repository),
            "Go": tool_version(["go", "version"], repository),
            "Rust": tool_version(["rustc", "--version"], repository),
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        markdown_report(metadata, summarized, args.languages, workloads),
        encoding="utf-8",
    )
    json_output = output.with_suffix(".json")
    json_output.write_text(
        json.dumps(
            {"metadata": metadata, "summary": summarized, "raw_ms": raw},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Markdown report: {output}")
    print(f"Raw JSON report: {json_output}")


if __name__ == "__main__":
    main()
