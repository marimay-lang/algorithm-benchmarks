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
    validate_candidate_budget,
    validate_budget_files,
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
    parser.add_argument("algorithms", type=pathlib.Path, nargs="?")
    parser.add_argument(
        "--baseline",
        type=pathlib.Path,
        help="optional historical algorithm result used for comparison context",
    )
    parser.add_argument("--retry-probes", type=pathlib.Path)
    parser.add_argument("--retry-algorithms", type=pathlib.Path)
    return parser.parse_args()


def resolve(repository: pathlib.Path, path: pathlib.Path) -> pathlib.Path:
    result = path if path.is_absolute() else repository / path
    return result.with_suffix(".json") if result.suffix == ".md" else result


def validate_current_probe_inputs(
    repository: pathlib.Path, probes: dict[str, object]
) -> None:
    probe_metadata = probes["metadata"]
    actual_probe_hash = probe_manifest_sha256(repository)
    recorded_probe_hash = probe_metadata["probe_manifest"]["sha256"]
    if recorded_probe_hash != actual_probe_hash:
        raise ProtocolError("probe result does not match the current probe manifest")
    _, probe_manifest = load_and_validate_probes(repository)
    actual_source_hash = source_tree_sha256(repository, probe_manifest)
    recorded_source_hash = probe_metadata["probe_manifest"]["source_tree_sha256"]
    if recorded_source_hash != actual_source_hash:
        raise ProtocolError("probe result does not match the current probe sources")


def validate_current_algorithm_inputs(
    repository: pathlib.Path, algorithms: dict[str, object]
) -> None:
    algorithm_metadata = algorithms["metadata"]
    manifest_path = repository / "benchmarks" / "equivalence.json"
    load_and_validate_equivalence(repository)
    actual_equivalence_hash = equivalence_manifest_sha256(manifest_path)
    recorded_equivalence_hash = algorithm_metadata["equivalence_manifest"]["sha256"]
    if recorded_equivalence_hash != actual_equivalence_hash:
        raise ProtocolError(
            "algorithm result does not match the current equivalence manifest"
        )


def probe_result(
    repository: pathlib.Path,
    path: pathlib.Path,
    protocol: dict[str, object],
    protocol_sha: str,
) -> dict[str, object]:
    probes = load_json(resolve(repository, path))
    validate_result(probes, protocol, protocol_sha)
    validate_current_probe_inputs(repository, probes)
    return probes


def algorithm_result(
    repository: pathlib.Path,
    path: pathlib.Path,
    protocol: dict[str, object],
    protocol_sha: str,
) -> dict[str, object]:
    algorithms = load_json(resolve(repository, path))
    validate_result(algorithms, protocol, protocol_sha)
    validate_current_algorithm_inputs(repository, algorithms)
    return algorithms


def result_pair(
    repository: pathlib.Path,
    probes_path: pathlib.Path,
    algorithms_path: pathlib.Path,
    protocol: dict[str, object],
    protocol_sha: str,
) -> tuple[dict[str, object], dict[str, object]]:
    probes = probe_result(repository, probes_path, protocol, protocol_sha)
    algorithms = algorithm_result(
        repository, algorithms_path, protocol, protocol_sha
    )
    validate_compatible_results(probes, algorithms)
    return probes, algorithms


def validate_reference_baseline(
    candidate: dict[str, object], baseline: dict[str, object]
) -> None:
    if baseline.get("schema") != candidate.get("schema"):
        raise ProtocolError("comparison baseline has the wrong result schema")
    candidate_platform = candidate["metadata"]["platform"]["id"]
    baseline_platform = baseline["metadata"]["platform"]["id"]
    if baseline_platform != candidate_platform:
        raise ProtocolError("comparison baseline uses a different platform")
    if set(baseline["workloads"]) != set(candidate["workloads"]):
        raise ProtocolError("comparison baseline workload set is incompatible")


def is_recorded_baseline_pair(
    repository: pathlib.Path,
    budget: dict[str, object],
    probes_path: pathlib.Path,
    algorithms_path: pathlib.Path,
) -> bool:
    baseline = budget["baseline"]
    paths = []
    for path in (probes_path, algorithms_path):
        try:
            resolved = resolve(repository, path).resolve()
            paths.append(resolved.relative_to(repository).as_posix())
        except ValueError:
            return False
    return paths == [baseline["probe_result"], baseline["algorithm_result"]]


def main() -> None:
    args = parse_args()
    repository = pathlib.Path(__file__).resolve().parents[1]
    protocol_file, protocol = load_protocol(repository)
    protocol_sha = sha256_file(protocol_file)
    probes = probe_result(repository, args.probes, protocol, protocol_sha)
    algorithms = None
    if args.algorithms is not None:
        algorithms = algorithm_result(
            repository, args.algorithms, protocol, protocol_sha
        )
        validate_compatible_results(probes, algorithms)
    platform_id = probes["metadata"]["platform"]["id"]
    budget_path = repository / "benchmarks" / "budgets" / f"cp21-{platform_id}.json"
    budget = load_json(budget_path)
    if algorithms is not None and is_recorded_baseline_pair(
        repository, budget, args.probes, args.algorithms
    ):
        validate_budget_files(
            budget,
            repository,
            resolve(repository, args.probes),
            resolve(repository, args.algorithms),
        )
        failures = validate_budget(budget, probes, algorithms, protocol_sha)
    else:
        candidates = {"probes": probes}
        if algorithms is not None:
            candidates["algorithms"] = algorithms
        failures = validate_candidate_budget(budget, candidates, protocol_sha)
    if args.baseline is not None:
        if algorithms is None:
            raise ProtocolError("--baseline requires an algorithm candidate")
        baseline = load_json(resolve(repository, args.baseline))
        validate_result(baseline, protocol, protocol_sha)
        validate_reference_baseline(algorithms, baseline)
    if not failures:
        algorithm_count = len(algorithms["workloads"]) if algorithms else 0
        print(
            f"results valid for {platform_id}; "
            f"{len(probes['workloads'])} probes and "
            f"{algorithm_count} algorithms are within reviewed budgets"
        )
        return
    if algorithms is None and args.retry_algorithms is not None:
        raise ProtocolError("focused probe retry does not accept algorithms")
    if algorithms is not None and (
        (args.retry_probes is None) != (args.retry_algorithms is None)
    ):
        raise ProtocolError("both retry result paths are required")
    if args.retry_probes is None:
        details = "\n".join(f"- {failure}" for failure in failures)
        raise ProtocolError(
            "regression candidate requires one complete cool-down retry:\n" + details
        )
    retry_probes = probe_result(
        repository, args.retry_probes, protocol, protocol_sha
    )
    retry_candidates = {"probes": retry_probes}
    if algorithms is not None:
        retry_algorithms = algorithm_result(
            repository, args.retry_algorithms, protocol, protocol_sha
        )
        validate_compatible_results(retry_probes, retry_algorithms)
        retry_candidates["algorithms"] = retry_algorithms
    retry_failures = validate_candidate_budget(
        budget, retry_candidates, protocol_sha
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
