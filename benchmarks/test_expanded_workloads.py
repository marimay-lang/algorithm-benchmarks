from __future__ import annotations

import copy
import pathlib
import unittest

from equivalence import load_manifest as load_equivalence
from expanded_workloads import (
    ExpandedWorkloadError,
    load_and_validate,
    validate_manifest,
    validate_sources,
)


class ExpandedWorkloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = pathlib.Path(__file__).resolve().parents[1]
        cls.canonical = load_equivalence(
            cls.repository / "benchmarks" / "equivalence.json"
        )
        _, cls.manifest = load_and_validate(cls.repository, cls.canonical)

    def test_committed_manifest_and_sources_are_valid(self) -> None:
        validate_sources(self.repository, self.manifest)

    def test_rejects_workload_membership_drift(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["workloads"].pop()
        with self.assertRaisesRegex(ExpandedWorkloadError, "membership"):
            validate_manifest(manifest, self.canonical)

    def test_rejects_checksum_collision_with_canonical_suite(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["workloads"][0]["expected_checksum"] = self.canonical["workloads"][0][
            "expected_checksum"
        ]
        with self.assertRaisesRegex(ExpandedWorkloadError, "distinct"):
            validate_manifest(manifest, self.canonical)

    def test_rejects_missing_source_fragment(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["workloads"][0]["implementations"]["marimay"][
            "required_fragments"
        ].append("MISSING_EXPANDED_MARKER")
        with self.assertRaisesRegex(ExpandedWorkloadError, "lacks fragment"):
            validate_sources(self.repository, manifest)


if __name__ == "__main__":
    unittest.main()
