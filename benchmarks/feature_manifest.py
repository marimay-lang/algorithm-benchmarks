from __future__ import annotations

import hashlib
import pathlib
from typing import Any

from perf_protocol import ProtocolError, load_json, sha256_file


SCHEMA = "marimay.feature-probes-manifest/1"


def manifest_path(repository: pathlib.Path) -> pathlib.Path:
    return repository / "benchmarks" / "feature_probes.json"


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
        raise ProtocolError("unsupported feature probe manifest schema")
    core_source = manifest.get("core_source")
    if not isinstance(core_source, str) or not core_source.endswith(".my"):
        raise ProtocolError("feature probe core_source must name a Marimay file")
    features = manifest.get("features")
    if not isinstance(features, list) or not features:
        raise ProtocolError("feature probe manifest must contain features")
    required_keys = {
        "id",
        "category",
        "description",
        "function",
        "source_directory",
        "expected_checksum",
    }
    ids: set[str] = set()
    functions: set[str] = set()
    for feature in features:
        if not isinstance(feature, dict) or set(feature) != required_keys:
            raise ProtocolError("feature probe metadata is incomplete")
        for key in ("id", "category", "description", "function", "source_directory"):
            if not isinstance(feature[key], str) or not feature[key]:
                raise ProtocolError(f"feature probe {key} must be a non-empty string")
        checksum = feature["expected_checksum"]
        if isinstance(checksum, bool) or not isinstance(checksum, int):
            raise ProtocolError("feature probe checksum must be an integer")
        if feature["id"] in ids or feature["function"] in functions:
            raise ProtocolError("feature probe ids and functions must be unique")
        ids.add(feature["id"])
        functions.add(feature["function"])


def validate_sources(repository: pathlib.Path, manifest: dict[str, Any]) -> None:
    core_path = repository / manifest["core_source"]
    try:
        core = core_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ProtocolError(f"cannot read feature probe core source: {error}") from error
    for feature in manifest["features"]:
        marker = f"public fn {feature['function']}(): int"
        if marker not in core:
            raise ProtocolError(f"feature probe core lacks {marker}")
        main_path = repository / feature["source_directory"] / "main.my"
        try:
            source = main_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise ProtocolError(
                f"cannot read feature probe entrypoint {main_path}: {error}"
            ) from error
        expected_line = f'{feature["id"]} {feature["expected_checksum"]}'
        if feature["function"] not in source or expected_line not in source:
            raise ProtocolError(f"feature probe entrypoint drifted: {feature['id']}")


def manifest_sha256(repository: pathlib.Path) -> str:
    return sha256_file(manifest_path(repository))


def source_tree_sha256(repository: pathlib.Path, manifest: dict[str, Any]) -> str:
    digest = hashlib.sha256()
    paths = [repository / manifest["core_source"]] + [
        repository / feature["source_directory"] / "main.my"
        for feature in manifest["features"]
    ]
    for path in sorted(paths):
        relative = path.relative_to(repository).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(bytes.fromhex(sha256_file(path)))
    return digest.hexdigest()
