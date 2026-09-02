#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import pathlib
import re
from typing import Any

from perf_protocol import sha256_file


SCHEMA = "marimay.cp41-codegen/1"
WORKLOADS = ("stack", "queue", "heap-sort", "min-heap")
TARGETS = ("x86_64", "arm64")
SYMBOL = re.compile(r"^_?mmay_g_f_[0-9a-f]{32}$")
LABEL = re.compile(r"^\s*[0-9a-fA-F]+\s+<([^>]+)>:\s*$")


def parse_nm(text: str) -> dict[str, int]:
    symbols: dict[str, int] = {}
    for line in text.splitlines():
        fields = line.split()
        if len(fields) < 4 or fields[1].lower() != "t":
            continue
        name = fields[0]
        if not SYMBOL.fullmatch(name):
            continue
        try:
            size = int(fields[3], 16)
        except ValueError as error:
            raise ValueError(f"invalid symbol size in nm output: {line!r}") from error
        symbols[name.lstrip("_")] = size
    if not symbols:
        raise ValueError("nm output contains no generated Marimay text symbols")
    return symbols


def parse_disassembly(text: str) -> dict[str, list[str]]:
    functions: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        match = LABEL.match(line)
        if match is not None:
            name = match.group(1).lstrip("_")
            current = name if SYMBOL.fullmatch(name) else None
            if current is not None:
                functions.setdefault(current, [])
            continue
        if current is not None and line.strip():
            functions[current].append(line)
    if not functions:
        raise ValueError("disassembly contains no generated Marimay functions")
    return functions


def stack_addressed_operations(lines: list[str], target: str) -> int:
    if target == "x86_64":
        pattern = re.compile(r"\[(?:r|e)?(?:sp|bp)(?:\s*[+\-\]])", re.IGNORECASE)
    elif target == "arm64":
        pattern = re.compile(r"\[(?:sp|x29)(?:\s*,|\])", re.IGNORECASE)
    else:
        raise ValueError(f"unsupported target: {target}")
    return sum(pattern.search(line) is not None for line in lines)


def analyze_target(directory: pathlib.Path, workload: str, target: str) -> dict[str, Any]:
    paths = {
        "object": directory / f"{workload}.{target}.o",
        "symbols": directory / f"{workload}.{target}.nm",
        "disassembly": directory / f"{workload}.{target}.disasm",
        "optimization_remarks": directory / f"{workload}.{target}.opt.yaml",
        "command": directory / f"{workload}.{target}.command.txt",
    }
    for path in paths.values():
        if not path.is_file():
            raise ValueError(f"missing CP41 code-generation artifact: {path}")
    symbols = parse_nm(paths["symbols"].read_text(encoding="utf-8"))
    functions = parse_disassembly(
        paths["disassembly"].read_text(encoding="utf-8")
    )
    hot_symbol, code_bytes = max(symbols.items(), key=lambda item: item[1])
    if hot_symbol not in functions:
        raise ValueError(f"hot symbol {hot_symbol} is absent from disassembly")
    lines = functions[hot_symbol]
    return {
        "hot_symbol": hot_symbol,
        "code_bytes": code_bytes,
        "instruction_lines": len(lines),
        "stack_addressed_operations": stack_addressed_operations(lines, target),
        "artifacts": {
            name: {
                "path": path.relative_to(directory).as_posix(),
                "sha256": sha256_file(path),
            }
            for name, path in paths.items()
        },
    }


def build_report(directory: pathlib.Path, phase: str, compiler_revision: str) -> dict[str, Any]:
    workloads: dict[str, Any] = {}
    for workload in WORKLOADS:
        source = directory / f"{workload}.c"
        if not source.is_file():
            raise ValueError(f"missing retained generated C: {source}")
        workloads[workload] = {
            "generated_c": {
                "path": source.relative_to(directory).as_posix(),
                "sha256": sha256_file(source),
            },
            "targets": {
                target: analyze_target(directory, workload, target)
                for target in TARGETS
            },
        }
    return {
        "schema": SCHEMA,
        "phase": phase,
        "compiler_revision": compiler_revision,
        "workloads": workloads,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize retained CP41 cross-target code-generation artifacts."
    )
    parser.add_argument("--input", type=pathlib.Path, required=True)
    parser.add_argument("--phase", choices=("before", "after"), required=True)
    parser.add_argument("--compiler-revision", required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    try:
        report = build_report(args.input.resolve(), args.phase, args.compiler_revision)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
