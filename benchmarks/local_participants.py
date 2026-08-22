from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any, Mapping

from equivalence import load_manifest as load_equivalence_manifest


class LocalParticipantError(ValueError):
    pass


SCHEMA = "ruda.local-benchmark-participants/1"
LANGUAGES = ["typescript", "v", "moonbit"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise LocalParticipantError(message)


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
    _require(manifest.get("schema") == SCHEMA, "unsupported local participant schema")
    _require(manifest.get("languages") == LANGUAGES, "local language order drifted")
    _require(manifest.get("scope") == "local-only", "local scope marker drifted")
    participants = manifest.get("participants")
    _require(isinstance(participants, dict), "participants must be an object")
    _require(list(participants) == LANGUAGES, "participant membership drifted")
    for language in LANGUAGES:
        participant = participants[language]
        _require(isinstance(participant, dict), f"{language} participant is invalid")
        for field in ("runtime", "build_profile", "documentation"):
            _require(
                isinstance(participant.get(field), str) and participant[field],
                f"{language}.{field} must be a non-empty string",
            )
        _strings(participant.get("source_paths"), f"{language}.source_paths")
        _strings(
            participant.get("required_fragments"),
            f"{language}.required_fragments",
        )

    workloads = manifest.get("workloads")
    _require(isinstance(workloads, list), "workloads must be a list")
    canonical_workloads = canonical.get("workloads")
    _require(isinstance(canonical_workloads, list), "canonical workloads are invalid")
    expected = [
        (workload["id"], workload["expected_checksum"])
        for workload in canonical_workloads
    ]
    actual = [
        (workload.get("id"), workload.get("expected_checksum"))
        if isinstance(workload, dict)
        else (None, None)
        for workload in workloads
    ]
    _require(actual == expected, "local workload ids/checksums drifted from canonical")
    for workload in workloads:
        identifier = workload["id"]
        fragments = workload.get("required_fragments")
        _require(isinstance(fragments, dict), f"{identifier} fragments are missing")
        _require(list(fragments) == LANGUAGES, f"{identifier} language coverage drifted")
        for language in LANGUAGES:
            _strings(fragments[language], f"{identifier}.{language} fragments")
    return manifest


def load_manifest(path: pathlib.Path, canonical: Mapping[str, Any]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise LocalParticipantError(f"cannot read local participant manifest {path}: {error}") from error
    if not isinstance(value, dict):
        raise LocalParticipantError("local participant manifest must be an object")
    return validate_manifest(value, canonical)


def validate_sources(repository: pathlib.Path, manifest: Mapping[str, Any]) -> None:
    participants = manifest["participants"]
    combined_sources: dict[str, str] = {}
    for language in LANGUAGES:
        participant = participants[language]
        sources: list[str] = []
        for relative in participant["source_paths"]:
            path = repository / relative
            try:
                sources.append(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError) as error:
                raise LocalParticipantError(
                    f"cannot read {language} benchmark source {path}: {error}"
                ) from error
        combined = "\n".join(sources)
        combined_sources[language] = combined
        for fragment in participant["required_fragments"]:
            _require(
                fragment in combined,
                f"{language} source lacks required fragment {fragment!r}",
            )
    for workload in manifest["workloads"]:
        for language in LANGUAGES:
            for fragment in workload["required_fragments"][language]:
                _require(
                    fragment in combined_sources[language],
                    f"{workload['id']}.{language} lacks fragment {fragment!r}",
                )


def load_and_validate(
    repository: pathlib.Path,
) -> tuple[pathlib.Path, dict[str, Any]]:
    canonical = load_equivalence_manifest(
        repository / "benchmarks" / "equivalence.json"
    )
    path = repository / "benchmarks" / "local_participants.json"
    manifest = load_manifest(path, canonical)
    validate_sources(repository, manifest)
    return path, manifest


def manifest_sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
