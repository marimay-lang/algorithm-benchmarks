#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any


SCHEMA = "marimay.algorithm-equivalence/1"
EXPECTED_LANGUAGES = ["marimay", "go", "rust"]
EXPECTED_WORKLOADS = [
    "insertion",
    "heap-sort",
    "stack",
    "queue",
    "min-heap",
    "dsu",
    "bfs",
    "dijkstra",
]


class EquivalenceError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise EquivalenceError(message)


def _required_strings(value: Any, label: str) -> list[str]:
    _require(isinstance(value, list) and value, f"{label} must be a non-empty list")
    _require(
        all(isinstance(item, str) and item for item in value),
        f"{label} entries must be non-empty strings",
    )
    return value


def validate_manifest(manifest: Any) -> dict[str, Any]:
    _require(isinstance(manifest, dict), "manifest root must be an object")
    _require(manifest.get("schema") == SCHEMA, f"schema must be {SCHEMA}")
    _require(
        manifest.get("languages") == EXPECTED_LANGUAGES,
        "languages must be exactly marimay, go, rust",
    )
    generator = manifest.get("generator")
    _require(isinstance(generator, dict), "generator must be an object")
    _require(
        (
            generator.get("kind"),
            generator.get("multiplier"),
            generator.get("increment"),
            generator.get("modulus"),
        )
        == ("lcg", 25173, 13849, 65536),
        "generator constants drifted from the checkpoint-20 LCG",
    )
    checksum = manifest.get("checksum")
    _require(isinstance(checksum, dict), "checksum must be an object")
    _require(
        checksum.get("modulus") == 1_000_000_007,
        "checksum modulus must be 1000000007",
    )
    _require(
        checksum.get("stdout") == "{id} {checksum}\n",
        "checksum stdout contract must be exact",
    )

    global_contracts = manifest.get("global_source_contracts")
    _require(isinstance(global_contracts, dict), "global_source_contracts missing")
    _require(
        list(global_contracts) == EXPECTED_LANGUAGES,
        "global source contracts must cover exactly marimay, go, rust",
    )
    for language in EXPECTED_LANGUAGES:
        contract = global_contracts[language]
        _require(isinstance(contract, dict), f"{language} source contract must be an object")
        _require(
            isinstance(contract.get("path"), str) and contract["path"],
            f"{language} source path missing",
        )
        _required_strings(contract.get("required_fragments"), f"{language} required fragments")
        _required_strings(contract.get("forbidden_fragments"), f"{language} forbidden fragments")

    workloads = manifest.get("workloads")
    _require(isinstance(workloads, list), "workloads must be a list")
    ids = [item.get("id") if isinstance(item, dict) else None for item in workloads]
    _require(ids == EXPECTED_WORKLOADS, "workload order or membership drifted")
    checksums: set[int] = set()
    for workload in workloads:
        identifier = workload["id"]
        for field in ("description", "input", "operations", "representation", "checks"):
            _require(
                isinstance(workload.get(field), str) and workload[field],
                f"{identifier}.{field} must be a non-empty string",
            )
        expected_checksum = workload.get("expected_checksum")
        _require(
            isinstance(expected_checksum, int) and 0 <= expected_checksum < 1_000_000_007,
            f"{identifier}.expected_checksum is outside the checksum domain",
        )
        _require(expected_checksum not in checksums, "workload checksums must be distinct")
        checksums.add(expected_checksum)
        implementations = workload.get("implementations")
        _require(isinstance(implementations, dict), f"{identifier}.implementations missing")
        _require(
            list(implementations) == EXPECTED_LANGUAGES,
            f"{identifier} must cover exactly marimay, go, rust",
        )
        for language in EXPECTED_LANGUAGES:
            implementation = implementations[language]
            _require(
                isinstance(implementation, dict),
                f"{identifier}.{language} implementation must be an object",
            )
            _required_strings(
                implementation.get("required_fragments"),
                f"{identifier}.{language} required fragments",
            )
    return manifest


def load_manifest(path: pathlib.Path) -> dict[str, Any]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise EquivalenceError(f"cannot read equivalence manifest {path}: {error}") from error
    return validate_manifest(manifest)


def manifest_sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_sources(repository: pathlib.Path, manifest: dict[str, Any]) -> None:
    for language, contract in manifest["global_source_contracts"].items():
        source_path = repository / contract["path"]
        try:
            source = source_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise EquivalenceError(f"cannot read {language} benchmark source {source_path}: {error}") from error
        for fragment in contract["required_fragments"]:
            _require(
                fragment in source,
                f"{language} benchmark source lacks required reusable fragment {fragment!r}",
            )
        for fragment in contract["forbidden_fragments"]:
            _require(
                fragment not in source,
                f"{language} benchmark source retains forbidden inline fragment {fragment!r}",
            )
        for workload in manifest["workloads"]:
            for fragment in workload["implementations"][language]["required_fragments"]:
                _require(
                    fragment in source,
                    f"{workload['id']}.{language} lacks workload fragment {fragment!r}",
                )


def load_and_validate(repository: pathlib.Path) -> tuple[pathlib.Path, dict[str, Any]]:
    manifest_path = repository / "benchmarks" / "equivalence.json"
    manifest = load_manifest(manifest_path)
    validate_sources(repository, manifest)
    return manifest_path, manifest
