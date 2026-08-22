from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
from collections.abc import Callable, Sequence


CORE_LANGUAGES = ["ruda", "go", "rust"]
LOCAL_LANGUAGES = ["typescript", "v", "moonbit"]


def parse_language_selection(value: str) -> list[str]:
    selected = [item.strip() for item in value.split(",") if item.strip()]
    if len(set(selected)) != len(selected):
        raise ValueError("languages must not contain duplicates")
    if selected[: len(CORE_LANGUAGES)] != CORE_LANGUAGES:
        raise ValueError("benchmark results require ruda,go,rust in protocol order")
    extras = selected[len(CORE_LANGUAGES) :]
    if any(language not in LOCAL_LANGUAGES for language in extras):
        raise ValueError("optional local languages are typescript,v,moonbit")
    expected_order = [language for language in LOCAL_LANGUAGES if language in extras]
    if extras != expected_order:
        raise ValueError("optional local languages must use typescript,v,moonbit order")
    return selected


def is_local_comparison(languages: Sequence[str]) -> bool:
    return list(languages) != CORE_LANGUAGES


def _tool(environment_name: str, default_name: str) -> pathlib.Path:
    configured = os.environ.get(environment_name)
    resolved = configured or shutil.which(default_name)
    if not resolved:
        raise SystemExit(
            f"{default_name} is required for the selected local participant; "
            f"install it or set {environment_name}=/absolute/path/to/{default_name}"
        )
    path = pathlib.Path(resolved).expanduser().resolve()
    if not path.is_file() or not os.access(path, os.X_OK):
        raise SystemExit(f"{environment_name} tool is not executable: {path}")
    return path


def _moonbit_binary(repository: pathlib.Path) -> pathlib.Path:
    build_root = repository / "moonbit" / "_build" / "native" / "release"
    candidates = [
        path
        for path in build_root.rglob("*")
        if path.is_file()
        and (
            os.access(path, os.X_OK)
            or path.suffix.lower() in {".exe", ""}
        )
        and "benchmark" in path.name.lower()
        and path.suffix.lower() not in {".c", ".d", ".o", ".obj"}
    ]
    if not candidates:
        raise SystemExit(
            "moon build completed but the native benchmark executable was not found "
            f"under {build_root}"
        )
    candidates.sort(key=lambda path: (path.suffix.lower() != ".exe", len(path.parts)))
    return candidates[0]


def build_local_binaries(
    repository: pathlib.Path,
    build_dir: pathlib.Path,
    languages: Sequence[str],
    benchmark_names: Sequence[str],
    run_checked: Callable[..., subprocess.CompletedProcess[str]],
) -> dict[str, dict[str, list[str]]]:
    commands: dict[str, dict[str, list[str]]] = {}
    if "typescript" in languages:
        bun = _tool("BUN", "bun")
        output = build_dir / "typescript-benchmark"
        run_checked(
            [
                str(bun),
                "build",
                "--compile",
                "--minify",
                "--outfile",
                str(output),
                "typescript/src/benchmark.ts",
            ],
            cwd=repository,
        )
        commands["typescript"] = {
            name: [str(output), name] for name in benchmark_names
        }
    if "v" in languages:
        compiler = _tool("V", "v")
        output = build_dir / "v-benchmark"
        run_checked(
            [str(compiler), "-prod", "-o", str(output), "cmd/benchmark"],
            cwd=repository / "v",
            timeout=600,
        )
        commands["v"] = {name: [str(output), name] for name in benchmark_names}
    if "moonbit" in languages:
        moon = _tool("MOON", "moon")
        run_checked(
            [str(moon), "build", "--release", "--target", "native"],
            cwd=repository / "moonbit",
            timeout=600,
        )
        output = _moonbit_binary(repository)
        commands["moonbit"] = {
            name: [str(output), name] for name in benchmark_names
        }
    return commands


def existing_local_commands(
    repository: pathlib.Path,
    build_dir: pathlib.Path,
    languages: Sequence[str],
    benchmark_names: Sequence[str],
) -> dict[str, dict[str, list[str]]]:
    outputs = {
        "typescript": build_dir / "typescript-benchmark",
        "v": build_dir / "v-benchmark",
    }
    commands: dict[str, dict[str, list[str]]] = {}
    for language in LOCAL_LANGUAGES:
        if language not in languages:
            continue
        output = (
            _moonbit_binary(repository)
            if language == "moonbit"
            else outputs[language]
        )
        if not output.is_file():
            raise SystemExit(f"missing binary for --skip-build: {output}")
        commands[language] = {
            name: [str(output), name] for name in benchmark_names
        }
    return commands


def local_toolchain_versions(
    repository: pathlib.Path,
    languages: Sequence[str],
    tool_version: Callable[[Sequence[str], pathlib.Path], str],
) -> dict[str, str]:
    versions: dict[str, str] = {}
    if "typescript" in languages:
        versions["typescript"] = "Bun " + tool_version(
            [str(_tool("BUN", "bun")), "--version"], repository
        )
    if "v" in languages:
        versions["v"] = tool_version([str(_tool("V", "v")), "version"], repository)
    if "moonbit" in languages:
        versions["moonbit"] = tool_version(
            [str(_tool("MOON", "moon")), "version"], repository
        )
    return versions
