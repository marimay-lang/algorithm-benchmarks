from __future__ import annotations

import copy
import pathlib
import unittest

from perf_protocol import ProtocolError
from probe_manifest import (
    load_and_validate,
    source_tree_sha256,
    validate_manifest,
    validate_sources,
)


class ProbeManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = pathlib.Path(__file__).resolve().parents[1]
        _, cls.manifest = load_and_validate(cls.repository)

    def test_committed_probe_manifest_and_sources_are_valid(self) -> None:
        validate_manifest(self.manifest)
        validate_sources(self.repository, self.manifest)
        self.assertRegex(source_tree_sha256(self.repository, self.manifest), r"^[0-9a-f]{64}$")

    def test_rejects_missing_cost_category(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["probes"] = [
            probe for probe in manifest["probes"] if probe["category"] != "nested"
        ]
        with self.assertRaisesRegex(ProtocolError, "category coverage"):
            validate_manifest(manifest)

    def test_rejects_checksum_drift_against_entrypoint(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["probes"][0]["expected_checksum"] += 1
        with self.assertRaisesRegex(ProtocolError, "entrypoint drifted"):
            validate_sources(self.repository, manifest)

    def test_rejects_missing_core_function(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["probes"][0]["function"] = "missingProbeFunction"
        with self.assertRaisesRegex(ProtocolError, "probe core lacks"):
            validate_sources(self.repository, manifest)


if __name__ == "__main__":
    unittest.main()
