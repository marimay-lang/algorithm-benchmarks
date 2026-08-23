from __future__ import annotations

import copy
import json
import pathlib
import tempfile
import unittest

from equivalence import EquivalenceError, load_manifest, validate_manifest, validate_sources


class EquivalenceManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = pathlib.Path(__file__).resolve().parents[1]
        cls.manifest_path = cls.repository / "benchmarks" / "equivalence.json"
        cls.manifest = load_manifest(cls.manifest_path)

    def test_committed_manifest_and_sources_are_valid(self) -> None:
        validate_sources(self.repository, self.manifest)

    def test_rejects_generator_drift(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["generator"]["multiplier"] += 1
        with self.assertRaisesRegex(EquivalenceError, "LCG"):
            validate_manifest(manifest)

    def test_rejects_checksum_drift(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["workloads"][0]["expected_checksum"] = -1
        with self.assertRaisesRegex(EquivalenceError, "checksum domain"):
            validate_manifest(manifest)

    def test_rejects_missing_language_contract(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        del manifest["workloads"][0]["implementations"]["rust"]
        with self.assertRaisesRegex(EquivalenceError, "exactly marimay, go, rust"):
            validate_manifest(manifest)

    def test_rejects_missing_reusable_source_fragment(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["global_source_contracts"]["marimay"]["path"] = "marimay/missing.my"
        with self.assertRaisesRegex(EquivalenceError, "cannot read marimay"):
            validate_sources(self.repository, manifest)

    def test_rejects_forbidden_inline_source_fragment(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        marker = "FORBIDDEN_CP20_INLINE_MARKER"
        manifest["global_source_contracts"]["marimay"]["forbidden_fragments"].append(
            marker
        )
        with tempfile.TemporaryDirectory() as directory:
            repository = pathlib.Path(directory)
            self._copy_benchmark_sources(repository, manifest)
            marimay_contract = manifest["global_source_contracts"]["marimay"]
            path = repository / marimay_contract["path"]
            path.write_text(path.read_text(encoding="utf-8") + marker, encoding="utf-8")
            with self.assertRaisesRegex(EquivalenceError, "forbidden inline"):
                validate_sources(repository, manifest)

    def test_rejects_workload_constant_missing_from_source(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["workloads"][0]["implementations"]["go"]["required_fragments"].append(
            "CP20_MISSING_WORKLOAD_CONSTANT"
        )
        with self.assertRaisesRegex(EquivalenceError, "lacks workload fragment"):
            validate_sources(self.repository, manifest)

    def test_rejects_malformed_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "manifest.json"
            path.write_text("{", encoding="utf-8")
            with self.assertRaisesRegex(EquivalenceError, "cannot read"):
                load_manifest(path)

    def test_json_round_trip_preserves_contract(self) -> None:
        reparsed = json.loads(json.dumps(self.manifest))
        self.assertEqual(validate_manifest(reparsed), reparsed)

    def _copy_benchmark_sources(
        self, repository: pathlib.Path, manifest: dict[str, object]
    ) -> None:
        contracts = manifest["global_source_contracts"]
        for contract in contracts.values():
            relative = pathlib.Path(contract["path"])
            destination = repository / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                (self.repository / relative).read_text(encoding="utf-8"),
                encoding="utf-8",
            )


if __name__ == "__main__":
    unittest.main()
