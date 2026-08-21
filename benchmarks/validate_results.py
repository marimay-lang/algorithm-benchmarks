#!/usr/bin/env python3

from __future__ import annotations

import argparse
import pathlib

from perf_protocol import (
    ProtocolError,
    load_json,
    load_protocol,
    sha256_file,
    validate_budget,
    validate_compatible_results,
    validate_result,
)
from probe_manifest import (
    load_and_validate as load_and_validate_probes,
    manifest_sha256 as probe_manifest_sha256,
    source_tree_sha256,
)
from equivalence import (
    load_and_validate as load_and_validate_equivalence,
    manifest_sha256 as equivalence_manifest_sha256,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate checkpoint-21 probes, algorithms, and reviewed budgets."
    )
    parser.add_argument("probes", type=pathlib.Path)
    parser.add_argument("algorithms", type=pathlib.Path)
    parser.add_argument("--retry-probes", type=pathlib.Path)
    parser.add_argument("--retry-algorithms", type=pathlib.Path)
    return parser.parse_args()


def resolve(repository: pathlib.Path, path: pathlib.Path) -> pathlib.Path:
    result = path if path.is_absolute() else repository / path
    return result.with_suffix(".json") if result.suffix == ".md" else result


def validate_current_inputs(
    repository: pathlib.Path, probes: dict[str, object], algorithms: dict[str, object]
) -> None:
    probe_metadata = probes["metadata"]
    algorithm_metadata = algorithms["metadata"]
    actual_probe_hash = probe_manifest_sha256(repository)
    recorded_probe_hash = probe_metadata["probe_manifest"]["sha256"]
    if recorded_probe_hash != actual_probe_hash:
        raise ProtocolError("probe result does not match the current probe manifest")
    _, probe_manifest = load_and_validate_probes(repository)
    actual_source_hash = source_tree_sha256(repository, probe_manifest)
    recorded_source_hash = probe_metadata["probe_manifest"]["source_tree_sha256"]
    if recorded_source_hash != actual_source_hash:
        raise ProtocolError("probe result does not match the current probe sources")
    manifest_path = repository / "benchmarks" / "equivalence.json"
    load_and_validate_equivalence(repository)
    actual_equivalence_hash = equivalence_manifest_sha256(manifest_path)
    recorded_equivalence_hash = algorithm_metadata["equivalence_manifest"]["sha256"]
    if recorded_equivalence_hash != actual_equivalence_hash:
        raise ProtocolError(
            "algorithm result does not match the current equivalence manifest"
        )


def result_pair(
    repository: pathlib.Path,
    probes_path: pathlib.Path,
    algorithms_path: pathlib.Path,
    protocol: dict[str, object],
    protocol_sha: str,
) -> tuple[dict[str, object], dict[str, object]]:
    probes = load_json(resolve(repository, probes_path))
    algorithms = load_json(resolve(repository, algorithms_path))
    validate_result(probes, protocol, protocol_sha)
    validate_result(algorithms, protocol, protocol_sha)
    validate_compatible_results(probes, algorithms)
    validate_current_inputs(repository, probes, algorithms)
    return probes, algorithms


def main() -> None:
    args = parse_args()
    repository = pathlib.Path(__file__).resolve().parents[1]
    protocol_file, protocol = load_protocol(repository)
    protocol_sha = sha256_file(protocol_file)
    probes, algorithms = result_pair(
        repository, args.probes, args.algorithms, protocol, protocol_sha
    )
    platform_id = probes["metadata"]["platform"]["id"]
    budget_path = repository / "benchmarks" / "budgets" / f"cp21-{platform_id}.json"
    budget = load_json(budget_path)
    failures = validate_budget(budget, probes, algorithms, protocol_sha)
    if not failures:
        print(
            f"checkpoint-21 results valid for {platform_id}; "
            f"{len(probes['workloads'])} probes and "
            f"{len(algorithms['workloads'])} algorithms are within reviewed budgets"
        )
        return
    if (args.retry_probes is None) != (args.retry_algorithms is None):
        raise ProtocolError("both retry result paths are required")
    if args.retry_probes is None:
        details = "\n".join(f"- {failure}" for failure in failures)
        raise ProtocolError(
            "regression candidate requires one complete cool-down retry:\n" + details
        )
    retry_probes, retry_algorithms = result_pair(
        repository,
        args.retry_probes,
        args.retry_algorithms,
        protocol,
        protocol_sha,
    )
    retry_failures = validate_budget(
        budget, retry_probes, retry_algorithms, protocol_sha
    )
    if retry_failures:
        details = "\n".join(f"- {failure}" for failure in retry_failures)
        raise ProtocolError(
            "reviewed regression: original and complete retry exceed budget:\n"
            + details
        )
    print("original candidate did not reproduce in the one permitted complete retry")


if __name__ == "__main__":
    try:
        main()
    except (ProtocolError, KeyError, TypeError) as error:
        raise SystemExit(f"result validation error: {error}") from error
