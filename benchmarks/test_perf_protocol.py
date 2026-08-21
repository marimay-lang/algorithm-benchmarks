from __future__ import annotations

import copy
import json
import math
import pathlib
import tempfile
import unittest

from perf_protocol import (
    ALGORITHM_RESULT_SCHEMA,
    BUDGET_SCHEMA,
    PROBE_RESULT_SCHEMA,
    ProtocolError,
    budget_for_summary,
    load_json,
    load_protocol,
    measure_matrix,
    schedule,
    sha256_file,
    summarize,
    validate_budget,
    validate_compatible_results,
    validate_result,
    validate_run_shape,
)


class PerformanceProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = pathlib.Path(__file__).resolve().parents[1]
        cls.protocol_path, cls.protocol = load_protocol(cls.repository)
        cls.protocol_sha = sha256_file(cls.protocol_path)

    def valid_result(self, schema: str = PROBE_RESULT_SCHEMA) -> dict[str, object]:
        raw = [float(value) for value in range(100, 111)]
        events = schedule(["workload"], ["ruda"], 3, 11)
        for index, event in enumerate(events):
            event["elapsed_ms"] = float(index + 1)
        result = {
            "schema": schema,
            "protocol": {
                "schema": self.protocol["schema"],
                "path": "benchmarks/performance_protocol.json",
                "sha256": self.protocol_sha,
            },
            "metadata": {
                "generated_at": "2026-08-21T00:00:00+00:00",
                "warmups": 3,
                "samples": 11,
                "timeout_seconds": 300,
                "clock": "perf_counter_ns",
                "order": "rotating-balanced-v1",
                "command": "unit-test",
                "platform": {
                    "id": "linux-x86_64",
                    "system": "Linux",
                    "release": "test",
                    "machine": "x86_64",
                    "cpu": "test cpu",
                    "logical_cpus": 8,
                },
                "isolation": {
                    "mode": "dedicated-runner-contract",
                    "load_average_at_start": [0.0, 0.0, 0.0],
                    "load_average_at_end": [0.0, 0.0, 0.0],
                    "power_source": "runner-policy",
                    "affinity": "not-requested",
                    "sample_selection": "none",
                },
                "resource": {"max_heap_bytes": 67108864},
                "artifacts": {
                    "ruda_compiler": {
                        "path": "/tmp/ruda",
                        "sha256": "1" * 64,
                        "revision": "test-revision",
                        "version": "Ruda test",
                    },
                    "runtime": {
                        "path": "/tmp/runtime.a",
                        "sha256": "2" * 64,
                        "manifest_path": "/tmp/runtime.manifest",
                        "manifest_sha256": "3" * 64,
                        "profile": "release",
                        "runtime": "test",
                        "host": "Test",
                        "processor": "test",
                        "compiler": "Test-1",
                    },
                    "native_c": {
                        "compiler_path": "/usr/bin/cc",
                        "compiler_version": "cc test",
                        "linker_path": "/usr/bin/cc",
                        "linker_version": "cc test",
                        "output_profile": "release",
                        "flags": ["-std=c17", "-O2"],
                    },
                },
                "toolchains": {
                    "python": "test",
                    "ruda": "test",
                    "go": "test",
                    "rust": "test",
                },
                "corpus_revision": "test-corpus-revision",
                "probe_manifest": {
                    "path": "benchmarks/probes.json",
                    "schema": "ruda.array-probes-manifest/1",
                    "sha256": "4" * 64,
                    "source_tree_sha256": "5" * 64,
                },
            },
            "workloads": {
                "workload": {
                    "description": "unit workload",
                    "expected_checksum": 7,
                    "expected_stdout": "workload 7\n",
                    "commands": {"ruda": ["probe"]},
                    "raw_ms": {"ruda": raw},
                    "summary": {"ruda": summarize(raw)},
                }
            },
            "order": events,
        }
        if schema == ALGORITHM_RESULT_SCHEMA:
            result["metadata"]["languages"] = ["ruda", "go", "rust"]
            result["metadata"]["equivalence_manifest"] = {
                "path": "benchmarks/equivalence.json",
                "schema": "ruda.algorithm-equivalence/1",
                "sha256": "6" * 64,
            }
            del result["metadata"]["probe_manifest"]
            raw_by_language = {
                "ruda": raw,
                "go": [value + 20.0 for value in raw],
                "rust": [value + 40.0 for value in raw],
            }
            result["workloads"]["workload"]["raw_ms"] = raw_by_language
            result["workloads"]["workload"]["summary"] = {
                key: summarize(values) for key, values in raw_by_language.items()
            }
            result["workloads"]["workload"]["commands"] = {
                "ruda": ["ruda-probe"],
                "go": ["go-probe"],
                "rust": ["rust-probe"],
            }
            algorithm_events = schedule(
                ["workload"], ["ruda", "go", "rust"], 3, 11
            )
            for index, event in enumerate(algorithm_events):
                event["elapsed_ms"] = float(index + 1)
            result["order"] = algorithm_events
        return result

    def valid_budget(self, result: dict[str, object]) -> dict[str, object]:
        summary_value = result["workloads"]["workload"]["summary"]["ruda"]
        entry = budget_for_summary(self.protocol, summary_value)
        return {
            "schema": BUDGET_SCHEMA,
            "protocol_sha256": self.protocol_sha,
            "platform_id": "linux-x86_64",
            "review": {
                "status": "reviewed",
                "reviewed_at": "2026-08-21T00:00:00+00:00",
                "rationale": "unit-test review",
            },
            "suites": {
                "probes": {"workload": copy.deepcopy(entry)},
                "algorithms": {"workload": copy.deepcopy(entry)},
            },
        }

    def test_protocol_and_minimum_run_shape_are_valid(self) -> None:
        validate_run_shape(self.protocol, 3, 11)
        with self.assertRaisesRegex(ProtocolError, "insufficient warmups"):
            validate_run_shape(self.protocol, 2, 11)
        with self.assertRaisesRegex(ProtocolError, "insufficient samples"):
            validate_run_shape(self.protocol, 3, 9)
        with self.assertRaisesRegex(ProtocolError, "odd sample"):
            validate_run_shape(self.protocol, 3, 12)

    def test_median_mad_iqr_and_noise_are_exact(self) -> None:
        result = summarize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.assertEqual(result["median_ms"], 6.0)
        self.assertEqual(result["mad_ms"], 3.0)
        self.assertEqual(result["q1_ms"], 3.0)
        self.assertEqual(result["q3_ms"], 9.0)
        self.assertEqual(result["iqr_ms"], 6.0)
        self.assertEqual(result["noise_fraction"], 1.5)
        with self.assertRaisesRegex(ProtocolError, "finite positive"):
            summarize([1.0, math.inf, 2.0])

    def test_schedule_rotates_and_covers_each_cell(self) -> None:
        events = schedule(["a", "b", "c"], ["ruda", "go", "rust"], 3, 11)
        self.assertEqual(len(events), 14 * 3 * 3)
        first_workloads = [
            event["workload"]
            for event in events
            if event["participant"] == "ruda" and event["round"] == 0
        ]
        self.assertGreater(len(set(first_workloads)), 1)
        counts: dict[tuple[str, str, str], int] = {}
        for event in events:
            key = (event["phase"], event["workload"], event["participant"])
            counts[key] = counts.get(key, 0) + 1
        self.assertEqual(counts[("warmup", "a", "go")], 3)
        self.assertEqual(counts[("sample", "c", "rust")], 11)

    def test_measure_matrix_publishes_every_sample_and_order(self) -> None:
        counter = 0

        def measured(command: list[str], expected: str) -> float:
            nonlocal counter
            self.assertEqual(command, ["probe"])
            self.assertEqual(expected, "ok\n")
            counter += 1
            return float(counter)

        raw, order = measure_matrix(
            {"ruda": {"w": ["probe"]}},
            {"w": "ok\n"},
            ["ruda"],
            ["w"],
            3,
            11,
            measured,
        )
        self.assertEqual(len(order), 14)
        self.assertEqual(raw["w"]["ruda"], [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0])

    def test_valid_probe_and_algorithm_results(self) -> None:
        probes = self.valid_result()
        algorithms = self.valid_result(ALGORITHM_RESULT_SCHEMA)
        validate_result(probes, self.protocol, self.protocol_sha)
        validate_result(algorithms, self.protocol, self.protocol_sha)
        validate_compatible_results(probes, algorithms)

    def test_rejects_wrong_profile_and_insufficient_samples(self) -> None:
        wrong_profile = self.valid_result()
        wrong_profile["metadata"]["artifacts"]["runtime"]["profile"] = "debug"
        with self.assertRaisesRegex(ProtocolError, "wrong runtime profile"):
            validate_result(wrong_profile, self.protocol, self.protocol_sha)
        short = self.valid_result()
        short["metadata"]["samples"] = 9
        with self.assertRaisesRegex(ProtocolError, "insufficient samples"):
            validate_result(short, self.protocol, self.protocol_sha)

    def test_rejects_incomplete_metadata_and_summary_drift(self) -> None:
        incomplete = self.valid_result()
        del incomplete["metadata"]["platform"]["cpu"]
        with self.assertRaisesRegex(ProtocolError, "cpu"):
            validate_result(incomplete, self.protocol, self.protocol_sha)
        drift = self.valid_result()
        drift["workloads"]["workload"]["summary"]["ruda"]["median_ms"] += 1
        with self.assertRaisesRegex(ProtocolError, "summary drift"):
            validate_result(drift, self.protocol, self.protocol_sha)

    def test_strict_json_rejects_non_finite_and_duplicate_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "bad.json"
            path.write_text('{"value": NaN}', encoding="utf-8")
            with self.assertRaisesRegex(ProtocolError, "non-finite"):
                load_json(path)
            path.write_text('{"value": 1, "value": 2}', encoding="utf-8")
            with self.assertRaisesRegex(ProtocolError, "duplicate"):
                load_json(path)

    def test_rejects_incompatible_result_pair(self) -> None:
        probes = self.valid_result()
        algorithms = self.valid_result(ALGORITHM_RESULT_SCHEMA)
        algorithms["metadata"]["platform"]["id"] = "windows-x86_64"
        with self.assertRaisesRegex(ProtocolError, "incompatible platform"):
            validate_compatible_results(probes, algorithms)

    def test_reviewed_budget_is_platform_and_workload_specific(self) -> None:
        probes = self.valid_result()
        algorithms = self.valid_result(ALGORITHM_RESULT_SCHEMA)
        budget = self.valid_budget(probes)
        self.assertEqual(
            validate_budget(budget, probes, algorithms, self.protocol_sha), []
        )
        budget["platform_id"] = "macos-arm64"
        with self.assertRaisesRegex(ProtocolError, "platform"):
            validate_budget(budget, probes, algorithms, self.protocol_sha)

    def test_budget_candidate_and_regression_are_rejected(self) -> None:
        probes = self.valid_result()
        algorithms = self.valid_result(ALGORITHM_RESULT_SCHEMA)
        budget = self.valid_budget(probes)
        budget["review"]["status"] = "candidate"
        with self.assertRaisesRegex(ProtocolError, "not been reviewed"):
            validate_budget(budget, probes, algorithms, self.protocol_sha)
        budget["review"]["status"] = "reviewed"
        budget["suites"]["probes"]["workload"]["maximum_median_ms"] = 1.0
        failures = validate_budget(budget, probes, algorithms, self.protocol_sha)
        self.assertEqual(len(failures), 1)
        self.assertIn("probes/workload", failures[0])


if __name__ == "__main__":
    unittest.main()
