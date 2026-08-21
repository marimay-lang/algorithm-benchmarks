from __future__ import annotations

import pathlib
from collections.abc import Mapping
from typing import Any

from perf_protocol import (
    ProtocolError,
    TIER1_TARGETS,
    load_json,
    load_protocol,
    sha256_file,
    tier1_target,
    validate_budget,
    validate_budget_files,
)
from validate_results import result_pair

REGISTRY_SCHEMA = "ruda.tier1-performance-baselines/2"
CHECKPOINT_21_GATE = "checkpoint-21"
PUBLIC_ALPHA_GATE = "public-alpha"
CHECKPOINT_21_TARGETS = ("linux-x86_64",)
REGISTRY_FIELDS = {
    "schema",
    "protocol_sha256",
    "checkpoint_21_targets",
    "public_alpha_targets",
    "baselines",
}
ENTRY_FIELDS = {"target", "platform_id", "probes", "algorithms", "budget"}


def registry_path(repository: pathlib.Path) -> pathlib.Path:
    return repository / "benchmarks" / "tier1-baselines.json"


def _string(mapping: Mapping[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise ProtocolError(f"Tier 1 registry {key} must be a non-empty string")
    return value


def required_targets_for_gate(
    registry: Mapping[str, Any], gate: str
) -> tuple[str, ...]:
    checkpoint_targets = registry.get("checkpoint_21_targets")
    if checkpoint_targets != list(CHECKPOINT_21_TARGETS):
        raise ProtocolError("checkpoint 21 target contract drifted")
    public_alpha_targets = registry.get("public_alpha_targets")
    if public_alpha_targets != list(TIER1_TARGETS):
        raise ProtocolError("public alpha target contract drifted")
    if gate == CHECKPOINT_21_GATE:
        return CHECKPOINT_21_TARGETS
    if gate == PUBLIC_ALPHA_GATE:
        return TIER1_TARGETS
    raise ProtocolError(f"unsupported performance baseline gate: {gate}")


def validate_registry_shape(
    registry: Mapping[str, Any], *, gate: str
) -> list[Mapping[str, Any]]:
    if set(registry) != REGISTRY_FIELDS:
        raise ProtocolError("Tier 1 registry fields are incomplete or unknown")
    if registry.get("schema") != REGISTRY_SCHEMA:
        raise ProtocolError("unsupported Tier 1 baseline registry schema")
    protocol_hash = _string(registry, "protocol_sha256")
    if len(protocol_hash) != 64 or any(
        character not in "0123456789abcdef" for character in protocol_hash
    ):
        raise ProtocolError("Tier 1 registry protocol hash is not a SHA-256")
    required_targets = required_targets_for_gate(registry, gate)
    entries = registry.get("baselines")
    if not isinstance(entries, list):
        raise ProtocolError("Tier 1 registry baselines must be a list")
    checked: list[Mapping[str, Any]] = []
    seen_targets: set[str] = set()
    seen_platforms: set[str] = set()
    for value in entries:
        if not isinstance(value, dict) or set(value) != ENTRY_FIELDS:
            raise ProtocolError("Tier 1 baseline entry fields are incomplete or unknown")
        target = _string(value, "target")
        platform_id = _string(value, "platform_id")
        for key in ("probes", "algorithms", "budget"):
            _string(value, key)
        if target not in TIER1_TARGETS:
            raise ProtocolError(f"unsupported Tier 1 baseline target: {target}")
        if platform_id != target and not platform_id.startswith(target + "-"):
            raise ProtocolError("Tier 1 platform id is inconsistent with target")
        if target in seen_targets:
            raise ProtocolError(f"duplicate Tier 1 baseline target: {target}")
        if platform_id in seen_platforms:
            raise ProtocolError(f"duplicate Tier 1 baseline platform: {platform_id}")
        seen_targets.add(target)
        seen_platforms.add(platform_id)
        checked.append(value)
    missing = [target for target in required_targets if target not in seen_targets]
    if missing:
        raise ProtocolError(
            f"{gate} performance baseline registry is incomplete; missing: "
            + ", ".join(missing)
        )
    return checked


def resolve_registry_path(
    repository: pathlib.Path, recorded: str, expected_directory: pathlib.Path
) -> pathlib.Path:
    candidate = pathlib.Path(recorded)
    if candidate.is_absolute():
        raise ProtocolError("Tier 1 registry paths must be repository-relative")
    resolved = (repository / candidate).resolve()
    expected = (repository / expected_directory).resolve()
    try:
        resolved.relative_to(expected)
    except ValueError as error:
        raise ProtocolError(
            f"Tier 1 registry path escapes {expected_directory.as_posix()}"
        ) from error
    if not resolved.is_file():
        raise ProtocolError(f"Tier 1 registry file is missing: {recorded}")
    return resolved


def validate_tier1_registry(
    repository: pathlib.Path, *, gate: str = CHECKPOINT_21_GATE
) -> tuple[int, list[str]]:
    repository = repository.resolve()
    protocol_file, protocol = load_protocol(repository)
    protocol_sha = sha256_file(protocol_file)
    registry = load_json(registry_path(repository))
    entries = validate_registry_shape(registry, gate=gate)
    if registry["protocol_sha256"] != protocol_sha:
        raise ProtocolError("Tier 1 registry references an incompatible protocol")
    targets: list[str] = []
    for entry in entries:
        probes_path = resolve_registry_path(
            repository,
            _string(entry, "probes"),
            pathlib.Path("benchmarks/results"),
        )
        algorithms_path = resolve_registry_path(
            repository,
            _string(entry, "algorithms"),
            pathlib.Path("benchmarks/results"),
        )
        budget_path = resolve_registry_path(
            repository,
            _string(entry, "budget"),
            pathlib.Path("benchmarks/budgets"),
        )
        probes, algorithms = result_pair(
            repository, probes_path, algorithms_path, protocol, protocol_sha
        )
        budget = load_json(budget_path)
        validate_budget_files(
            budget, repository, probes_path, algorithms_path
        )
        failures = validate_budget(budget, probes, algorithms, protocol_sha)
        if failures:
            raise ProtocolError(
                f"Tier 1 baseline {_string(entry, 'platform_id')} exceeds its "
                "reviewed budget: " + "; ".join(failures)
            )
        platform = probes["metadata"]["platform"]
        target = tier1_target(platform["system"], platform["machine"])
        if target != entry["target"]:
            raise ProtocolError("Tier 1 registry target does not match result metadata")
        if platform["id"] != entry["platform_id"]:
            raise ProtocolError("Tier 1 registry platform id does not match results")
        targets.append(target)
    return len(entries), targets
