from __future__ import annotations

import copy
from pathlib import Path
import unittest

from catalog_contract import (
    PARTICIPANTS,
    SCHEMA,
    load_manifest,
    select_workloads,
    validate_result,
)
from catalog_oracle import expected
from catalog_measure import measure_catalog
from catalog_report import markdown_report
from perf_protocol import ProtocolError, load_protocol, schedule, summarize

ROOT = Path(__file__).resolve().parents[1]


class CatalogContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load_manifest(ROOT)
        _, self.protocol = load_protocol(ROOT)

    def result(self):
        participants = PARTICIPANTS
        params = {"size": 32, "rounds": 3}
        identifier = "map-int"
        checksum = expected(identifier, **params)
        events = schedule([identifier], participants, 0, 3)
        for event in events:
            event["elapsed_ms"] = 10.0
            event["status"] = "passed"
        return {
            "schema": SCHEMA,
            "status": "passed",
            "metadata": {
                "comparison_scope": "local-only",
                "profile": "smoke",
                "verify_only": True,
                "participants": participants,
                "samples": 3,
                "warmups": 0,
                "workload_manifest": self.manifest,
                "binaries": {p: "b" * 64 for p in participants} | {"mmay": "c" * 64},
                "source_sha256": {"source": "a" * 64},
                "generated_at": "test",
                "platform": {"system": "test", "machine": "test", "cpu": "test"},
                "timeout_seconds": 300,
                "resource": {"max_heap_bytes": 67108864},
                "limitations": [],
                "toolchains": {},
                "bun_runtime": {"path": "bun", "sha256": "b" * 64, "version": "test"},
                "command": "test",
            },
            "workloads": {
                identifier: {
                    "parameters": params,
                    "description": "test",
                    "expected_checksum": checksum,
                    "go_ratio_target": 1.5,
                    "expected_stdout": f"{identifier} {checksum}\n",
                    "commands": {
                        p: (
                            ["mmay", "run", "--engine", "vm"]
                            if p.endswith("-vm")
                            else [p, "--no-env-file", "--no-install", "run", "catalog.ts"] if p == "bun"
                            else [p]
                        )
                        + [identifier, "32", "3"]
                        for p in participants
                    },
                    "outcomes": {p: {"status": "passed"} for p in participants},
                    "raw_ms": {p: [10.0] * 3 for p in participants},
                    "summary": {p: summarize([10.0] * 3) for p in participants},
                }
            },
            "measurement_order": events,
        }

    def test_complete_application_coverage_and_selection(self):
        self.assertEqual(len(self.manifest["workloads"]), 21)
        self.assertEqual(
            [w["id"] for w in select_workloads(self.manifest, ["catalog-pipeline"])],
            ["catalog-pipeline"],
        )
        for requested in (["missing"], ["map-int", "map-int"]):
            with self.assertRaises(ProtocolError):
                select_workloads(self.manifest, requested)

    def test_independent_singleton_results(self):
        # Book 0 is Available, "Война и мир" occupies 20 UTF-8 bytes.
        self.assertEqual(expected("catalog-match", 1, 1), 21)
        self.assertEqual(expected("map-int", 1, 3), 4)
        self.assertEqual(expected("record-reference-copy", 1, 1), 21)
        self.assertEqual(expected("record-create", 1, 1), 20)
        self.assertEqual(expected("bfs-record", 1, 1), 1)

    def test_pair_semantics_and_uneven_sizes(self):
        for size in (1, 17, 32, 97):
            for left, right in [
                ("report-builder", "report-concat"),
                ("bfs-int", "bfs-record"),
                ("catalog-dotcall", "catalog-interface"),
                ("array-grow", "array-reserved"),
                ("map-int", "map-string"),
            ]:
                self.assertEqual(expected(left, size, 3), expected(right, size, 3))
            self.assertEqual(
                expected("record-reference-copy", size, 3)
                - expected("record-create", size, 3),
                size * 3,
            )

    def test_valid_result_and_no_smoke_parity(self):
        result = self.result()
        validate_result(result, self.protocol)
        report = markdown_report(result)
        self.assertIn("no performance or parity conclusion", report)
        self.assertNotIn("native / Go", report)
        self.assertIn("source loading, checking and lowering", report)

    def test_failure_is_retained_and_other_cells_complete(self):
        result = self.result()
        row = result["workloads"]["map-int"]
        commands = {p: {"map-int": command} for p, command in row["commands"].items()}
        calls = []

        def timed(command, stdout):
            calls.append(command[0])
            if command[0] == "mmay":
                raise ProtocolError("injected VM failure")
            return 10.0

        raw, order, outcomes = measure_catalog(
            commands,
            {"map-int": row["expected_stdout"]},
            PARTICIPANTS,
            ["map-int"],
            0,
            3,
            timed,
        )
        self.assertEqual(calls.count("mmay"), 1)
        self.assertEqual(calls.count("go"), 3)
        row.update(raw_ms=raw["map-int"], outcomes=outcomes["map-int"])
        row["summary"]["marimay-vm"] = None
        result.update(status="failed", measurement_order=order)
        validate_result(result, self.protocol)
        self.assertIn("**FAILED**", markdown_report(result))
        row["summary"]["marimay-vm"] = summarize([1.0, 2.0, 3.0])
        with self.assertRaises(ProtocolError):
            validate_result(result, self.protocol)

    def test_manifest_drives_real_dispatch(self):
        sources = {
            "marimay": (ROOT / "marimay/catalog/main.my").read_text(),
            "go": (ROOT / "go/cmd/catalog/main.go").read_text(),
            "rust": (ROOT / "rust/src/bin/catalog.rs").read_text(),
            "typescript": (ROOT / "typescript/src/catalog/main.ts").read_text(),
        }
        for workload in self.manifest["workloads"]:
            mode = workload["mode"]
            arguments = "n, rounds" + ("" if mode is None else ", " + str(mode).lower())
            for language, source in sources.items():
                self.assertIn('"' + workload["id"] + '"', source)
                self.assertIn(
                    workload["entrypoints"][language] + "(" + arguments + ")", source
                )

    def test_reject_corrupt_observations(self):
        mutations = [
            lambda r: r["workloads"]["map-int"].__setitem__("expected_checksum", 0),
            lambda r: r["workloads"]["map-int"]["summary"]["go"].__setitem__(
                "median_ms", 1
            ),
            lambda r: r["workloads"]["map-int"]["raw_ms"]["rust"].pop(),
            lambda r: r["measurement_order"].pop(),
            lambda r: r["measurement_order"][0].__setitem__("elapsed_ms", float("nan")),
            lambda r: r["workloads"]["map-int"]["commands"].__setitem__(
                "marimay-vm", ["mmay", "run", "--engine", "native"]
            ),
            lambda r: r["metadata"].__setitem__("comparison_scope", "tier1"),
            lambda r: r["metadata"].__setitem__("profile", "standard")
            or r["metadata"].__setitem__("verify_only", False),
        ]
        for mutate in mutations:
            result = copy.deepcopy(self.result())
            mutate(result)
            with self.subTest(mutate=mutate), self.assertRaises(ProtocolError):
                validate_result(result, self.protocol)


if __name__ == "__main__":
    unittest.main()
