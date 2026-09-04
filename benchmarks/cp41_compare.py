#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from typing import Any

from cp41_codegen import SCHEMA as CODEGEN_SCHEMA, TARGETS, WORKLOADS
from cp41_perf import EVENTS, SCHEMA as COUNTER_SCHEMA, summarize
from perf_protocol import ProtocolError


SCHEMA = "marimay.cp41-comparison/1"
PROBE_SCHEMA = "marimay.array-probes/1"
ALGORITHM_SCHEMA = "marimay.algorithm-benchmark/2"
PROBES = (
    "scalar-get",
    "scalar-set",
    "proven-bounds",
    "unproven-bounds",
    "growth",
    "reserved-growth",
    "density",
    "nested-traversal",
    "checked-loop",
)
ALGORITHMS = (
    "insertion",
    "heap-sort",
    "stack",
    "queue",
    "min-heap",
    "dsu",
    "bfs",
    "dijkstra",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProtocolError(message)


def load_report(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ProtocolError(f"cannot read CP41 report {path}: {error}") from error
    require(isinstance(value, dict), f"CP41 report is not an object: {path}")
    return value


def positive_float(value: Any, description: str) -> float:
    require(
        isinstance(value, (int, float)) and not isinstance(value, bool),
        f"{description} is not numeric",
    )
    result = float(value)
    require(math.isfinite(result) and result > 0.0, f"{description} is not positive")
    return result


def nonnegative_float(value: Any, description: str) -> float:
    require(
        isinstance(value, (int, float)) and not isinstance(value, bool),
        f"{description} is not numeric",
    )
    result = float(value)
    require(
        math.isfinite(result) and result >= 0.0,
        f"{description} is negative or non-finite",
    )
    return result


def wall_metric(report: dict[str, Any], workload: str) -> tuple[float, float]:
    try:
        raw = report["workloads"][workload]["raw_ms"]["marimay"]
        summary = report["workloads"][workload]["summary"]["marimay"]
    except (KeyError, TypeError) as error:
        raise ProtocolError(f"missing Marimay wall-clock data for {workload}") from error
    require(isinstance(raw, list) and len(raw) == 11, f"{workload} needs 11 wall samples")
    for index, value in enumerate(raw):
        positive_float(value, f"{workload} wall sample {index}")
    median = positive_float(summary.get("median_ms"), f"{workload} wall median")
    noise = positive_float(summary.get("noise_fraction"), f"{workload} wall noise")
    return median, noise


def validate_wall_report(
    report: dict[str, Any], schema: str, workloads: tuple[str, ...], revision: str
) -> str:
    require(report.get("schema") == schema, f"unexpected wall-clock schema: {report.get('schema')}")
    require(set(report.get("workloads", {})) == set(workloads), "wall-clock workload set drifted")
    metadata = report.get("metadata")
    require(isinstance(metadata, dict), "wall-clock metadata is missing")
    require(metadata.get("warmups") == 3, "wall-clock report needs three warmups")
    require(metadata.get("samples") == 11, "wall-clock report needs eleven samples")
    platform = metadata.get("platform")
    require(
        isinstance(platform, dict) and platform.get("id") == "linux-x86_64",
        "wall-clock report is not Linux x86_64",
    )
    try:
        actual_revision = metadata["artifacts"]["mmay_compiler"]["revision"]
        corpus_revision = metadata["corpus_revision"]
    except (KeyError, TypeError) as error:
        raise ProtocolError("wall-clock artifact identity is incomplete") from error
    require(actual_revision == revision, f"wall-clock compiler revision is {actual_revision}, expected {revision}")
    require(isinstance(corpus_revision, str) and len(corpus_revision) == 40, "invalid corpus revision")
    for workload in workloads:
        wall_metric(report, workload)
    return corpus_revision


def validate_counter_report(
    report: dict[str, Any], phase: str, revision: str
) -> tuple[str, dict[str, str], str]:
    require(report.get("schema") == COUNTER_SCHEMA, "unexpected hardware-counter schema")
    require(report.get("phase") == phase, f"counter phase is not {phase}")
    require(report.get("compiler_revision") == revision, f"{phase} counter revision drifted")
    require(set(report.get("raw", {})) == set(WORKLOADS), "counter workload set drifted")
    protocol = report.get("protocol")
    require(isinstance(protocol, dict), "counter protocol is missing")
    require(protocol.get("warmups") == 3, "counter report needs three warmups")
    require(protocol.get("samples") == 11, "counter report needs eleven samples")
    perf = report.get("perf")
    require(isinstance(perf, dict), "perf identity is missing")
    require(perf.get("logical_events") == list(EVENTS), "logical counter set drifted")
    profile = perf.get("event_profile")
    event_map = perf.get("event_map")
    require(isinstance(profile, str) and profile, "counter event profile is missing")
    require(
        isinstance(event_map, dict)
        and set(event_map) == set(EVENTS)
        and len(set(event_map.values())) == len(EVENTS),
        "counter physical event map is invalid",
    )
    summary = report.get("summary")
    require(isinstance(summary, dict), "counter summary is missing")
    for workload in WORKLOADS:
        require(set(report["raw"][workload]) == set(EVENTS), f"{workload} counter set drifted")
        for event in EVENTS:
            values = report["raw"][workload][event]
            require(
                isinstance(values, list) and len(values) == 11,
                f"{workload}/{event} needs eleven counter samples",
            )
            require(
                all(isinstance(value, int) and not isinstance(value, bool) and value > 0 for value in values),
                f"{workload}/{event} contains an invalid counter sample",
            )
            calculated = summarize(values)
            recorded = summary.get(workload, {}).get(event, {})
            for field, expected in calculated.items():
                description = f"{workload}/{event} {field}"
                actual = (
                    nonnegative_float(recorded.get(field), description)
                    if field == "mad"
                    else positive_float(recorded.get(field), description)
                )
                require(
                    math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-9),
                    f"{workload}/{event} {field} does not match raw samples",
                )
    corpus_revision = report.get("corpus_revision")
    require(isinstance(corpus_revision, str) and len(corpus_revision) == 40, "invalid counter corpus revision")
    return profile, {str(key): str(value) for key, value in event_map.items()}, corpus_revision


def validate_codegen_report(
    report: dict[str, Any], phase: str, revision: str
) -> None:
    require(report.get("schema") == CODEGEN_SCHEMA, "unexpected code-generation schema")
    require(report.get("phase") == phase, f"code-generation phase is not {phase}")
    require(report.get("compiler_revision") == revision, f"{phase} code-generation revision drifted")
    workloads = report.get("workloads")
    require(isinstance(workloads, dict) and set(workloads) == set(WORKLOADS), "code-generation workload set drifted")
    for workload in WORKLOADS:
        targets = workloads[workload].get("targets", {})
        require(set(targets) == set(TARGETS), f"{workload} code-generation targets drifted")
        for target in TARGETS:
            count = targets[target].get("stack_addressed_operations")
            require(
                isinstance(count, int) and not isinstance(count, bool) and count >= 0,
                f"{workload}/{target} has an invalid stack-operation count",
            )


def reduction(before: float, after: float) -> float:
    return (before - after) / before


def improvement_gate(
    before: float, after: float, before_noise: float, after_noise: float, floor: float
) -> dict[str, Any]:
    threshold = max(floor, before_noise, after_noise)
    actual = reduction(before, after)
    return {
        "before": before,
        "after": after,
        "reduction_fraction": actual,
        "required_fraction_exclusive": threshold,
        "passed": actual > threshold,
    }


def compare_reports(
    before_probe: dict[str, Any],
    after_probe: dict[str, Any],
    before_algorithm: dict[str, Any],
    after_algorithm: dict[str, Any],
    before_counter: dict[str, Any],
    after_counter: dict[str, Any],
    before_codegen: dict[str, Any],
    after_codegen: dict[str, Any],
    before_revision: str,
    after_revision: str,
) -> dict[str, Any]:
    corpus_revisions = {
        validate_wall_report(before_probe, PROBE_SCHEMA, PROBES, before_revision),
        validate_wall_report(after_probe, PROBE_SCHEMA, PROBES, after_revision),
        validate_wall_report(before_algorithm, ALGORITHM_SCHEMA, ALGORITHMS, before_revision),
        validate_wall_report(after_algorithm, ALGORITHM_SCHEMA, ALGORITHMS, after_revision),
    }
    before_profile, before_map, before_counter_corpus = validate_counter_report(
        before_counter, "before", before_revision
    )
    after_profile, after_map, after_counter_corpus = validate_counter_report(
        after_counter, "after", after_revision
    )
    corpus_revisions.update((before_counter_corpus, after_counter_corpus))
    require(len(corpus_revisions) == 1, "before/after corpus revisions are not identical")
    require(before_profile == after_profile, "before/after counter profiles differ")
    require(before_map == after_map, "before/after physical counter maps differ")
    validate_codegen_report(before_codegen, "before", before_revision)
    validate_codegen_report(after_codegen, "after", after_revision)

    failures: list[str] = []
    affected: dict[str, Any] = {}
    for workload in ("stack", "queue"):
        before_wall, before_wall_noise = wall_metric(before_algorithm, workload)
        after_wall, after_wall_noise = wall_metric(after_algorithm, workload)
        wall_gate = improvement_gate(
            before_wall, after_wall, before_wall_noise, after_wall_noise, 0.15
        )
        before_instructions = positive_float(
            before_counter["summary"][workload]["instructions"]["median"],
            f"before {workload} instructions",
        )
        after_instructions = positive_float(
            after_counter["summary"][workload]["instructions"]["median"],
            f"after {workload} instructions",
        )
        before_instruction_noise = positive_float(
            before_counter["summary"][workload]["instructions"]["noise_fraction"],
            f"before {workload} instruction noise",
        )
        after_instruction_noise = positive_float(
            after_counter["summary"][workload]["instructions"]["noise_fraction"],
            f"after {workload} instruction noise",
        )
        instruction_gate = improvement_gate(
            before_instructions,
            after_instructions,
            before_instruction_noise,
            after_instruction_noise,
            0.15,
        )
        affected[workload] = {"wall_clock": wall_gate, "retired_instructions": instruction_gate}
        if not wall_gate["passed"]:
            failures.append(f"{workload} wall-clock reduction did not clear its exclusive threshold")
        if not instruction_gate["passed"]:
            failures.append(f"{workload} retired-instruction reduction did not clear its exclusive threshold")

    heap: dict[str, Any] = {}
    heap_improved = False
    for workload in ("heap-sort", "min-heap"):
        before_wall, before_noise = wall_metric(before_algorithm, workload)
        after_wall, after_noise = wall_metric(after_algorithm, workload)
        tolerance = max(0.10, before_noise, after_noise)
        improvement = reduction(before_wall, after_wall)
        no_regression = after_wall <= before_wall * (1.0 + tolerance)
        materially_improved = improvement > tolerance
        heap[workload] = {
            "before": before_wall,
            "after": after_wall,
            "reduction_fraction": improvement,
            "noise_or_regression_fraction": tolerance,
            "no_regression": no_regression,
            "materially_improved": materially_improved,
        }
        heap_improved = heap_improved or materially_improved
        if not no_regression:
            failures.append(f"{workload} exceeded its noise-aware regression envelope")
    if not heap_improved:
        failures.append("neither heap-sort nor min-heap cleared the exclusive improvement threshold")

    before_x86 = sum(
        before_codegen["workloads"][workload]["targets"]["x86_64"]["stack_addressed_operations"]
        for workload in ("stack", "queue")
    )
    after_x86 = sum(
        after_codegen["workloads"][workload]["targets"]["x86_64"]["stack_addressed_operations"]
        for workload in ("stack", "queue")
    )
    require(before_x86 > 0, "before x86_64 stack-operation total is zero")
    x86_reduction = reduction(float(before_x86), float(after_x86))
    arm64 = {
        workload: {
            "before": before_codegen["workloads"][workload]["targets"]["arm64"]["stack_addressed_operations"],
            "after": after_codegen["workloads"][workload]["targets"]["arm64"]["stack_addressed_operations"],
        }
        for workload in ("stack", "queue")
    }
    arm64_no_increase = all(value["after"] <= value["before"] for value in arm64.values())
    if x86_reduction < 0.20:
        failures.append("combined x86_64 stack-addressed operations fell by less than 20%")
    if not arm64_no_increase:
        failures.append("an arm64 stack-addressed operation count increased")

    return {
        "schema": SCHEMA,
        "passed": not failures,
        "failures": failures,
        "revisions": {"before": before_revision, "after": after_revision},
        "corpus_revision": next(iter(corpus_revisions)),
        "counter_profile": {"name": before_profile, "event_map": before_map},
        "affected_workloads": affected,
        "heap_workloads": heap,
        "code_generation": {
            "x86_64": {
                "before_stack_operations": before_x86,
                "after_stack_operations": after_x86,
                "reduction_fraction": x86_reduction,
                "required_fraction_inclusive": 0.20,
                "passed": x86_reduction >= 0.20,
            },
            "arm64": {"workloads": arm64, "no_increase": arm64_no_increase},
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the complete CP41 before/after acceptance contract.")
    for name in (
        "before-probes",
        "after-probes",
        "before-algorithms",
        "after-algorithms",
        "before-counters",
        "after-counters",
        "before-codegen",
        "after-codegen",
    ):
        parser.add_argument(f"--{name}", type=pathlib.Path, required=True)
    parser.add_argument("--before-revision", required=True)
    parser.add_argument("--after-revision", required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    try:
        result = compare_reports(
            load_report(args.before_probes),
            load_report(args.after_probes),
            load_report(args.before_algorithms),
            load_report(args.after_algorithms),
            load_report(args.before_counters),
            load_report(args.after_counters),
            load_report(args.before_codegen),
            load_report(args.after_codegen),
            args.before_revision,
            args.after_revision,
        )
    except ProtocolError as error:
        parser.error(str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result["passed"]:
        for failure in result["failures"]:
            print(f"CP41 acceptance failure: {failure}", file=sys.stderr)
        return 1
    print("CP41 acceptance: all measured gates passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
