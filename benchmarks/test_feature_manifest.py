from __future__ import annotations

import copy
import pathlib
import unittest

from feature_manifest import (
    load_and_validate,
    source_tree_sha256,
    validate_manifest,
    validate_sources,
)
from perf_protocol import ProtocolError


class FeatureManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = pathlib.Path(__file__).resolve().parents[1]
        _, cls.manifest = load_and_validate(cls.repository)

    def test_committed_manifest_and_sources_are_valid(self) -> None:
        validate_manifest(self.manifest)
        validate_sources(self.repository, self.manifest)
        self.assertRegex(
            source_tree_sha256(self.repository, self.manifest), r"^[0-9a-f]{64}$"
        )

    def test_rejects_incomplete_metadata(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        del manifest["features"][0]["description"]
        with self.assertRaisesRegex(ProtocolError, "metadata is incomplete"):
            validate_manifest(manifest)

    def test_rejects_checksum_drift_against_entrypoint(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["features"][0]["expected_checksum"] += 1
        with self.assertRaisesRegex(ProtocolError, "entrypoint drifted"):
            validate_sources(self.repository, manifest)

    def test_rejects_missing_core_function(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["features"][0]["function"] = "missingFeatureProbe"
        with self.assertRaisesRegex(ProtocolError, "core lacks"):
            validate_sources(self.repository, manifest)


if __name__ == "__main__":
    unittest.main()
