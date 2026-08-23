#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
from typing import Any

from perf_protocol import (
    BUDGET_SCHEMA,
    ProtocolError,
    budget_for_summary,
    load_json,
    load_protocol,
    sha256_file,
    validate_compatible_results,
    validate_result,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Derive a reviewable workload-specific budget candidate."
    )
    parser.add_argument("probes", type=pathlib.Path)
    parser.add_argument("algorithms", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    return parser.parse_args()


def resolved_result(repository: pathlib.Path, path: pathlib.Path) -> pathlib.Path:
    candidate = path if path.is_absolute() else repository / path
    if candidate.suffix == ".md":
        candidate = candidate.with_suffix(".json")
    return candidate


def suite_budgets(
    protocol: dict[str, Any], result: dict[str, Any]
) -> dict[str, dict[str, float]]:
    budgets: dict[str, dict[str, float]] = {}
    for workload, observation in result["workloads"].items():
        try:
            marimay_summary = observation["summary"]["marimay"]
        except (KeyError, TypeError) as error:
            raise ProtocolError(
                f"cannot derive a Marimay budget for workload {workload}"
            ) from error
        budgets[workload] = budget_for_summary(protocol, marimay_summary)
    return budgets


def main() -> None:
    args = parse_args()
    repository = pathlib.Path(__file__).resolve().parents[1]
    protocol_file, protocol = load_protocol(repository)
    probes_path = resolved_result(repository, args.probes)
    algorithms_path = resolved_result(repository, args.algorithms)
    probes = load_json(probes_path)
    algorithms = load_json(algorithms_path)
    protocol_sha = sha256_file(protocol_file)
    validate_result(probes, protocol, protocol_sha)
    validate_result(algorithms, protocol, protocol_sha)
    validate_compatible_results(probes, algorithms)
    platform_id = probes["metadata"]["platform"]["id"]
    budget = {
        "schema": BUDGET_SCHEMA,
        "protocol_sha256": protocol_sha,
        "platform_id": platform_id,
        "created_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "review": {
            "status": "candidate",
            "reviewed_at": "pending",
            "rationale": "pending engineering review of raw samples and noise",
        },
        "baseline": {
            "probe_result": str(probes_path.relative_to(repository)),
            "probe_result_sha256": sha256_file(probes_path),
            "algorithm_result": str(algorithms_path.relative_to(repository)),
            "algorithm_result_sha256": sha256_file(algorithms_path),
            "marimay_revision": probes["metadata"]["artifacts"]["mmay_compiler"][
                "revision"
            ],
            "corpus_revision": probes["metadata"]["corpus_revision"],
            "probe_manifest_sha256": probes["metadata"]["probe_manifest"][
                "sha256"
            ],
            "equivalence_manifest_sha256": algorithms["metadata"][
                "equivalence_manifest"
            ]["sha256"],
        },
        "suites": {
            "probes": suite_budgets(protocol, probes),
            "algorithms": suite_budgets(protocol, algorithms),
        },
    }
    output = args.output if args.output.is_absolute() else repository / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(budget, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Budget candidate: {output}")
    print("Review every raw distribution, then change review.status to reviewed.")


if __name__ == "__main__":
    try:
        main()
    except ProtocolError as error:
        raise SystemExit(f"performance protocol error: {error}") from error
