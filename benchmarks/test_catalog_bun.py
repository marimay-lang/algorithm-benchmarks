"""Bun catalogue coverage, engine integrity and immutable runtime tests."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from catalog_bun import bun_command, bun_path, pin_bun
from catalog_contract import ENGINE_MATRICES, LEGACY_PARTICIPANTS, load_manifest, source_hashes, validate_result
from catalog_oracle import expected
from catalog_report import console_report
from perf_protocol import ProtocolError, schedule
import test_catalog

ROOT = Path(__file__).resolve().parents[1]
BUN = os.environ.get("BUN") or shutil.which("bun")


class BunHarnessTests(unittest.TestCase):
    def test_selection_keeps_native_and_vm_boundaries(self):
        self.assertEqual(ENGINE_MATRICES["native"], ["marimay-native", "go", "rust"])
        self.assertEqual(ENGINE_MATRICES["vm"], ["marimay-vm"])
        self.assertEqual(ENGINE_MATRICES["bun"], ["bun"])
        self.assertEqual(ENGINE_MATRICES["both"], [*LEGACY_PARTICIPANTS, "bun"])

    def test_missing_bun_is_actionable(self):
        with patch.dict(os.environ, {}, clear=True), patch("catalog_bun.shutil.which", return_value=None):
            with self.assertRaisesRegex(ProtocolError, "Bun not found"):
                bun_path()

    def test_runtime_copy_survives_source_replacement(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "original-bun"
            source.write_text("#!/bin/sh\nprintf 'test-bun-version\\n'\n")
            source.chmod(0o755)
            metadata = {"toolchains": {}}
            target = pin_bun(source, root / "workspace", metadata)
            source.write_text("replaced original")
            self.assertNotEqual(source.stat().st_ino, target.stat().st_ino)
            self.assertIn("test-bun-version", target.read_text())
            self.assertEqual(metadata["toolchains"]["bun"], "test-bun-version")

    def test_runtime_mutation_during_copy_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "original"
            source.write_bytes(b"before")
            real_copy = shutil.copy2
            def copy_then_mutate(src, dst):
                real_copy(src, dst)
                src.write_bytes(b"after")
            with patch("catalog_bun.shutil.copy2", side_effect=copy_then_mutate):
                with self.assertRaisesRegex(ProtocolError, "Bun changed"):
                    pin_bun(source, root / "workspace", {"toolchains": {}})

    def test_typescript_sources_and_adapter_are_hashed(self):
        hashes = source_hashes(ROOT)
        for file in (ROOT / "typescript/src").rglob("*.ts"):
            self.assertIn(str(file.relative_to(ROOT)), hashes)
        self.assertIn("benchmarks/catalog_bun.py", hashes)

    def fixture(self):
        fixture = test_catalog.CatalogContractTests()
        fixture.setUp()
        return fixture.result(), fixture.protocol

    def test_bun_label_and_command_integrity(self):
        result, protocol = self.fixture()
        validate_result(result, protocol)
        self.assertIn("Bun / TypeScript", console_report(result))
        for mutate in (
            lambda r: r["metadata"]["bun_runtime"].__setitem__("sha256", "0" * 64),
            lambda r: r["metadata"]["bun_runtime"].__setitem__("version", ""),
            lambda r: r["workloads"]["map-int"]["commands"]["bun"].__setitem__(4, "catalog.js"),
            lambda r: r["workloads"]["map-int"]["commands"]["bun"].__setitem__(3, "build"),
        ):
            broken = copy.deepcopy(result)
            mutate(broken)
            with self.assertRaises(ProtocolError):
                validate_result(broken, protocol)

    def test_historical_four_participant_report_still_validates(self):
        result, protocol = self.fixture()
        meta = result["metadata"]
        meta["participants"] = LEGACY_PARTICIPANTS
        meta["workload_manifest"]["participants"] = LEGACY_PARTICIPANTS
        del meta["bun_runtime"]
        for field in ("commands", "raw_ms", "summary", "outcomes"):
            del result["workloads"]["map-int"][field]["bun"]
        events = schedule(["map-int"], LEGACY_PARTICIPANTS, 0, 3)
        for event in events:
            event.update(elapsed_ms=10.0, status="passed")
        result["measurement_order"] = events
        validate_result(result, protocol)
        self.assertNotIn("Bun / TypeScript", console_report(result))


@unittest.skipUnless(BUN, "Bun is needed for TypeScript execution checks")
class BunWorkloadTests(unittest.TestCase):
    def run_ts(self, path, args):
        return subprocess.run(bun_command(Path(BUN), ROOT / path) + args,
                              cwd=ROOT, text=True, capture_output=True, timeout=60)

    def test_all_catalogue_boundaries_against_independent_oracle(self):
        for row in load_manifest(ROOT)["workloads"]:
            cases = [(1, 1), (17, 3), (97, 2), tuple(row["parameters"]["smoke"].values())]
            for size, rounds in cases:
                with self.subTest(workload=row["id"], size=size, rounds=rounds):
                    result = self.run_ts("typescript/src/catalog/main.ts", [row["id"], str(size), str(rounds)])
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, "")
                    self.assertEqual(result.stdout, f"{row['id']} {expected(row['id'], size, rounds)}\n")

    def test_all_eleven_fixed_anchors(self):
        for filename in ("equivalence.json", "expanded_workloads.json"):
            for row in json.loads((ROOT / "benchmarks" / filename).read_text())["workloads"]:
                with self.subTest(workload=row["id"]):
                    result = self.run_ts("typescript/src/benchmark.ts", [row["id"]])
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, "")
                    self.assertEqual(result.stdout, f"{row['id']} {row['expected_checksum']}\n")

    def test_invalid_catalogue_arguments_fail_without_checksum(self):
        for args in (["map-int", "0", "1"], ["map-int", "1x", "1"],
                     ["map-int", "1000001", "1"], ["map-int", "1000000", "1000000"],
                     ["missing", "1", "1"], ["map-int"]):
            with self.subTest(args=args):
                result = self.run_ts("typescript/src/catalog/main.ts", list(args))
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
