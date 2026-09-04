from __future__ import annotations

import copy
import unittest

from cp41_codegen import SCHEMA as CODEGEN_SCHEMA, TARGETS, WORKLOADS
from cp41_compare import (
    ALGORITHMS,
    ALGORITHM_SCHEMA,
    PROBES,
    PROBE_SCHEMA,
    compare_reports,
)
from cp41_perf import EVENTS, SCHEMA as COUNTER_SCHEMA, summarize
from perf_protocol import ProtocolError


BEFORE_REVISION = "a" * 40
AFTER_REVISION = "b" * 40
CORPUS_REVISION = "c" * 40


def wall_report(
    schema: str,
    workloads: tuple[str, ...],
    revision: str,
    medians: dict[str, float] | None = None,
) -> dict[str, object]:
    medians = medians or {}
    return {
        "schema": schema,
        "metadata": {
            "warmups": 3,
            "samples": 11,
            "platform": {"id": "linux-x86_64"},
            "corpus_revision": CORPUS_REVISION,
            "artifacts": {"mmay_compiler": {"revision": revision}},
        },
        "workloads": {
            workload: {
                "raw_ms": {"marimay": [medians.get(workload, 100.0)] * 11},
                "summary": {
                    "marimay": {
                        "median_ms": medians.get(workload, 100.0),
                        "noise_fraction": 0.02,
                    }
                },
            }
            for workload in workloads
        },
    }


def counter_report(phase: str, revision: str, instruction_value: int) -> dict[str, object]:
    raw = {
        workload: {
            event: [
                instruction_value
                if event == "instructions" and workload in ("stack", "queue")
                else 100
            ]
            * 11
            for event in EVENTS
        }
        for workload in WORKLOADS
    }
    return {
        "schema": COUNTER_SCHEMA,
        "phase": phase,
        "compiler_revision": revision,
        "corpus_revision": CORPUS_REVISION,
        "protocol": {"warmups": 3, "samples": 11},
        "perf": {
            "logical_events": list(EVENTS),
            "event_profile": "perf-generic-v1",
            "event_map": {event: event for event in EVENTS},
        },
        "raw": raw,
        "summary": {
            workload: {
                event: summarize(values) for event, values in events.items()
            }
            for workload, events in raw.items()
        },
    }


def codegen_report(phase: str, revision: str, x86_count: int) -> dict[str, object]:
    return {
        "schema": CODEGEN_SCHEMA,
        "phase": phase,
        "compiler_revision": revision,
        "workloads": {
            workload: {
                "targets": {
                    target: {
                        "stack_addressed_operations": (
                            x86_count
                            if target == "x86_64" and workload in ("stack", "queue")
                            else 10
                        )
                    }
                    for target in TARGETS
                }
            }
            for workload in WORKLOADS
        },
    }


class Checkpoint41ComparisonTests(unittest.TestCase):
    def reports(self) -> list[dict[str, object]]:
        return [
            wall_report(PROBE_SCHEMA, PROBES, BEFORE_REVISION),
            wall_report(PROBE_SCHEMA, PROBES, AFTER_REVISION),
            wall_report(ALGORITHM_SCHEMA, ALGORITHMS, BEFORE_REVISION),
            wall_report(
                ALGORITHM_SCHEMA,
                ALGORITHMS,
                AFTER_REVISION,
                {"stack": 70.0, "queue": 70.0, "heap-sort": 85.0},
            ),
            counter_report("before", BEFORE_REVISION, 100),
            counter_report("after", AFTER_REVISION, 70),
            codegen_report("before", BEFORE_REVISION, 50),
            codegen_report("after", AFTER_REVISION, 40),
        ]

    def test_accepts_every_checkpoint_threshold_at_once(self) -> None:
        result = compare_reports(*self.reports(), BEFORE_REVISION, AFTER_REVISION)
        self.assertTrue(result["passed"])
        self.assertEqual(result["failures"], [])
        self.assertAlmostEqual(
            result["code_generation"]["x86_64"]["reduction_fraction"], 0.20
        )

    def test_reports_all_failed_measured_gates(self) -> None:
        reports = self.reports()
        reports[3] = wall_report(
            ALGORITHM_SCHEMA,
            ALGORITHMS,
            AFTER_REVISION,
            {"stack": 90.0, "queue": 90.0},
        )
        reports[5] = counter_report("after", AFTER_REVISION, 90)
        reports[7] = codegen_report("after", AFTER_REVISION, 45)
        result = compare_reports(*reports, BEFORE_REVISION, AFTER_REVISION)
        self.assertFalse(result["passed"])
        self.assertGreaterEqual(len(result["failures"]), 6)

    def test_rejects_cross_profile_counter_comparison(self) -> None:
        reports = self.reports()
        after = copy.deepcopy(reports[5])
        after["perf"]["event_profile"] = "linux-l1d-loads-v1"
        after["perf"]["event_map"]["cache-references"] = "L1-dcache-loads"
        after["perf"]["event_map"]["cache-misses"] = "L1-dcache-load-misses"
        reports[5] = after
        with self.assertRaises(ProtocolError):
            compare_reports(*reports, BEFORE_REVISION, AFTER_REVISION)


if __name__ == "__main__":
    unittest.main()
