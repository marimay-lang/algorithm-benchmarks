from __future__ import annotations

import copy
import pathlib
import unittest

from feature_manifest import load_and_validate
from feature_probes import (
    FEATURE_RESULT_SCHEMA,
    select_features,
    validate_feature_result,
)
from perf_protocol import ProtocolError, load_json, load_protocol, sha256_file


class FeatureProbeSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repository = pathlib.Path(__file__).resolve().parents[1]
        _, manifest = load_and_validate(repository)
        cls.repository = repository
        cls.features = manifest["features"]
        _, cls.protocol = load_protocol(repository)
        cls.protocol_sha = sha256_file(
            repository / "benchmarks" / "performance_protocol.json"
        )

    def feature_result(self) -> dict[str, object]:
        result = load_json(
            self.repository
            / "benchmarks"
            / "results"
            / "cp21-probes-macos-arm64-apple-m2.json"
        )
        result["schema"] = FEATURE_RESULT_SCHEMA
        metadata = result["metadata"]
        metadata["comparison_scope"] = "local-only"
        metadata["feature_manifest"] = copy.deepcopy(metadata["probe_manifest"])
        metadata["feature_manifest"]["schema"] = "marimay.feature-probes-manifest/1"
        return result

    def ids(self, requested: list[str] | None) -> list[str]:
        return [feature["id"] for feature in select_features(self.features, requested)]

    def test_no_selector_keeps_manifest_order(self) -> None:
        self.assertEqual(self.ids(None), ["dynamic-text"])

    def test_repeated_selector_is_deduplicated(self) -> None:
        self.assertEqual(
            self.ids(["dynamic-text", "dynamic-text"]), ["dynamic-text"]
        )

    def test_unknown_selector_is_rejected(self) -> None:
        with self.assertRaisesRegex(ProtocolError, "unknown feature probe"):
            select_features(self.features, ["missing"])

    def test_result_reuses_the_strict_raw_measurement_contract(self) -> None:
        validate_feature_result(
            self.feature_result(), self.protocol, self.protocol_sha
        )

    def test_result_must_remain_local_only(self) -> None:
        result = self.feature_result()
        result["metadata"]["comparison_scope"] = "tier1"
        with self.assertRaisesRegex(ProtocolError, "local-only"):
            validate_feature_result(result, self.protocol, self.protocol_sha)

    def test_result_rejects_wrong_feature_manifest_schema(self) -> None:
        result = self.feature_result()
        result["metadata"]["feature_manifest"]["schema"] = "wrong"
        with self.assertRaisesRegex(ProtocolError, "manifest schema"):
            validate_feature_result(result, self.protocol, self.protocol_sha)


if __name__ == "__main__":
    unittest.main()
