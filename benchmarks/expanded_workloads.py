from __future__ import annotations

import hashlib
import json
import pathlib
from collections.abc import Mapping
from typing import Any


SCHEMA = "marimay.expanded-algorithm-workloads/1"
LANGUAGES = ["marimay", "go", "rust"]
WORKLOADS = ["frequency-map", "unique-set", "rune-frequency"]


class ExpandedWorkloadError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ExpandedWorkloadError(message)


def _strings(value: object, label: str) -> list[str]:
    _require(
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item for item in value),
        f"{label} must be a non-empty string list",
    )
    return value


def validate_manifest(
    manifest: dict[str, Any], canonical: Mapping[str, Any]
) -> dict[str, Any]:
    _require(manifest.get("schema") == SCHEMA, "unsupported expanded workload schema")
    _require(manifest.get("scope") == "local-only", "expanded scope marker drifted")
    _require(manifest.get("languages") == LANGUAGES, "expanded language matrix drifted")
    source_paths = manifest.get("source_paths")
    _require(isinstance(source_paths, dict), "expanded source paths are missing")
    _require(list(source_paths) == LANGUAGES, "expanded source language coverage drifted")
    for language in LANGUAGES:
        _strings(source_paths[language], f"{language}.source_paths")

    workloads = manifest.get("workloads")
    _require(isinstance(workloads, list), "expanded workloads must be a list")
    ids = [item.get("id") if isinstance(item, dict) else None for item in workloads]
    _require(ids == WORKLOADS, "expanded workload order or membership drifted")
    canonical_checksums = {
        workload["expected_checksum"] for workload in canonical["workloads"]
    }
    seen_checksums: set[int] = set()
    for workload in workloads:
        identifier = workload["id"]
        for field in ("description", "input", "operations", "representation", "checks"):
            _require(
                isinstance(workload.get(field), str) and bool(workload[field]),
                f"{identifier}.{field} must be a non-empty string",
            )
        checksum = workload.get("expected_checksum")
        _require(
            isinstance(checksum, int)
            and not isinstance(checksum, bool)
            and 0 <= checksum < 1_000_000_007,
            f"{identifier}.expected_checksum is outside the checksum domain",
        )
        _require(
            checksum not in canonical_checksums and checksum not in seen_checksums,
            "expanded workload checksums must be distinct",
        )
        seen_checksums.add(checksum)
        implementations = workload.get("implementations")
        _require(isinstance(implementations, dict), f"{identifier}.implementations missing")
        _require(
            list(implementations) == LANGUAGES,
            f"{identifier} must cover exactly marimay, go, rust",
        )
        for language in LANGUAGES:
            implementation = implementations[language]
            _require(
                isinstance(implementation, dict),
                f"{identifier}.{language} implementation must be an object",
            )
            _strings(
                implementation.get("required_fragments"),
                f"{identifier}.{language}.required_fragments",
            )
    return manifest


def validate_sources(repository: pathlib.Path, manifest: Mapping[str, Any]) -> None:
    combined: dict[str, str] = {}
    for language in LANGUAGES:
        sources: list[str] = []
        for relative in manifest["source_paths"][language]:
            path = repository / relative
            try:
                sources.append(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError) as error:
                raise ExpandedWorkloadError(
                    f"cannot read {language} expanded source {path}: {error}"
                ) from error
        combined[language] = "\n".join(sources)
    for workload in manifest["workloads"]:
        for language in LANGUAGES:
            for fragment in workload["implementations"][language]["required_fragments"]:
                _require(
                    fragment in combined[language],
                    f"{workload['id']}.{language} lacks fragment {fragment!r}",
                )


def load_and_validate(
    repository: pathlib.Path, canonical: Mapping[str, Any]
) -> tuple[pathlib.Path, dict[str, Any]]:
    path = repository / "benchmarks" / "expanded_workloads.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ExpandedWorkloadError(f"cannot read expanded workload manifest {path}: {error}") from error
    _require(isinstance(value, dict), "expanded workload manifest root must be an object")
    manifest = validate_manifest(value, canonical)
    validate_sources(repository, manifest)
    return path, manifest


def manifest_sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
