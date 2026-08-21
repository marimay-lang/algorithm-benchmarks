from __future__ import annotations

import pathlib
import hashlib
from typing import Any

from perf_protocol import ProtocolError, load_json, sha256_file


SCHEMA = "ruda.array-probes-manifest/1"
REQUIRED_CATEGORIES = {
    "access",
    "bounds",
    "growth",
    "storage",
    "nested",
    "checked-arithmetic",
}


def manifest_path(repository: pathlib.Path) -> pathlib.Path:
    return repository / "benchmarks" / "probes.json"


def load_and_validate(
    repository: pathlib.Path,
) -> tuple[pathlib.Path, dict[str, Any]]:
    path = manifest_path(repository)
    manifest = load_json(path)
    validate_manifest(manifest)
    validate_sources(repository, manifest)
    return path, manifest


def validate_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("schema") != SCHEMA:
        raise ProtocolError("unsupported probe manifest schema")
    core_source = manifest.get("core_source")
    if not isinstance(core_source, str) or not core_source.endswith(".ruda"):
        raise ProtocolError("probe core_source must name a Ruda file")
    probes = manifest.get("probes")
    if not isinstance(probes, list) or not probes:
        raise ProtocolError("probe manifest must contain probes")
    ids: set[str] = set()
    functions: set[str] = set()
    categories: set[str] = set()
    required_keys = {
        "id",
        "category",
        "description",
        "function",
        "source_directory",
        "expected_checksum",
    }
    for probe in probes:
        if not isinstance(probe, dict) or set(probe) != required_keys:
            raise ProtocolError("probe metadata is incomplete")
        for key in ("id", "category", "description", "function", "source_directory"):
            if not isinstance(probe[key], str) or not probe[key]:
                raise ProtocolError(f"probe {key} must be a non-empty string")
        checksum = probe["expected_checksum"]
        if isinstance(checksum, bool) or not isinstance(checksum, int):
            raise ProtocolError("probe checksum must be an integer")
        if probe["id"] in ids or probe["function"] in functions:
            raise ProtocolError("probe ids and functions must be unique")
        ids.add(probe["id"])
        functions.add(probe["function"])
        categories.add(probe["category"])
    if categories != REQUIRED_CATEGORIES:
        raise ProtocolError("probe category coverage is incomplete")


def validate_sources(repository: pathlib.Path, manifest: dict[str, Any]) -> None:
    core_path = repository / manifest["core_source"]
    try:
        core = core_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ProtocolError(f"cannot read probe core source: {error}") from error
    for probe in manifest["probes"]:
        function_marker = f"public fn {probe['function']}(): int"
        if function_marker not in core:
            raise ProtocolError(f"probe core lacks {function_marker}")
        main_path = repository / probe["source_directory"] / "main.ruda"
        try:
            source = main_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise ProtocolError(f"cannot read probe entrypoint {main_path}: {error}") from error
        expected_line = f'{probe["id"]} {probe["expected_checksum"]}'
        if probe["function"] not in source or expected_line not in source:
            raise ProtocolError(f"probe entrypoint drifted: {probe['id']}")


def manifest_sha256(repository: pathlib.Path) -> str:
    return sha256_file(manifest_path(repository))


def source_tree_sha256(repository: pathlib.Path, manifest: dict[str, Any]) -> str:
    digest = hashlib.sha256()
    paths = [repository / manifest["core_source"]] + [
        repository / probe["source_directory"] / "main.ruda"
        for probe in manifest["probes"]
    ]
    for path in sorted(paths):
        relative = path.relative_to(repository).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(bytes.fromhex(sha256_file(path)))
    return digest.hexdigest()
