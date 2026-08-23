from __future__ import annotations

import pathlib
import unittest

from perf_protocol import ProtocolError
from probe_manifest import load_and_validate
from probes import select_probes


class FocusedProbeSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = pathlib.Path(__file__).resolve().parents[1]
        _, manifest = load_and_validate(cls.repository)
        cls.probes = manifest["probes"]

    def ids(self, requested: list[str] | None) -> list[str]:
        return [probe["id"] for probe in select_probes(self.probes, requested)]

    def test_checkpoint_groups_select_manifest_order(self) -> None:
        self.assertEqual(self.ids(["scalar-storage"]), ["density"])
        self.assertEqual(
            self.ids(["capacity"]), ["growth", "reserved-growth"]
        )
        self.assertEqual(
            self.ids(["nested-traversal", "checked-integer"]),
            ["nested-traversal", "checked-loop"],
        )

    def test_repeated_groups_are_deduplicated(self) -> None:
        self.assertEqual(
            self.ids(["capacity", "growth"]),
            ["growth", "reserved-growth"],
        )

    def test_no_selector_keeps_complete_manifest(self) -> None:
        self.assertEqual(len(self.ids(None)), len(self.probes))

    def test_unknown_selector_is_rejected(self) -> None:
        with self.assertRaisesRegex(ProtocolError, "unknown probe"):
            select_probes(self.probes, ["missing"])


if __name__ == "__main__":
    unittest.main()
