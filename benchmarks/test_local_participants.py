from __future__ import annotations

import copy
import pathlib
import tempfile
import unittest

from equivalence import load_manifest as load_equivalence
from local_languages import CORE_LANGUAGES, is_local_comparison, parse_language_selection
from local_participants import (
    LocalParticipantError,
    load_and_validate,
    load_manifest,
    validate_manifest,
    validate_sources,
)


class LocalParticipantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = pathlib.Path(__file__).resolve().parents[1]
        cls.canonical = load_equivalence(
            cls.repository / "benchmarks" / "equivalence.json"
        )
        cls.manifest_path = cls.repository / "benchmarks" / "local_participants.json"
        cls.manifest = load_manifest(cls.manifest_path, cls.canonical)

    def test_committed_manifest_and_sources_are_valid(self) -> None:
        validate_sources(self.repository, self.manifest)
        path, manifest = load_and_validate(self.repository)
        self.assertEqual(path, self.manifest_path)
        self.assertEqual(manifest, self.manifest)

    def test_language_selection_preserves_tier1_default(self) -> None:
        self.assertEqual(parse_language_selection("ruda,go,rust"), CORE_LANGUAGES)
        self.assertFalse(is_local_comparison(CORE_LANGUAGES))
        selected = parse_language_selection(
            "ruda,go,rust,typescript,v,moonbit"
        )
        self.assertEqual(selected[3:], ["typescript", "v", "moonbit"])
        self.assertTrue(is_local_comparison(selected))

    def test_language_selection_rejects_partial_reordered_and_duplicate_sets(self) -> None:
        cases = (
            "ruda,go",
            "go,ruda,rust",
            "ruda,go,rust,moonbit,v",
            "ruda,go,rust,v,v",
            "ruda,go,rust,node",
        )
        for value in cases:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_language_selection(value)

    def test_manifest_is_bound_to_canonical_workloads_and_checksums(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["workloads"][0]["expected_checksum"] += 1
        with self.assertRaisesRegex(LocalParticipantError, "canonical"):
            validate_manifest(manifest, self.canonical)

    def test_manifest_requires_all_local_languages(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        del manifest["participants"]["moonbit"]
        with self.assertRaisesRegex(LocalParticipantError, "membership"):
            validate_manifest(manifest, self.canonical)

    def test_source_validation_rejects_missing_fragment(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["participants"]["typescript"]["required_fragments"].append(
            "LOCAL_PARTICIPANT_MISSING_FRAGMENT"
        )
        with self.assertRaisesRegex(LocalParticipantError, "required fragment"):
            validate_sources(self.repository, manifest)

    def test_manifest_reader_rejects_malformed_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "local.json"
            path.write_text("{", encoding="utf-8")
            with self.assertRaisesRegex(LocalParticipantError, "cannot read"):
                load_manifest(path, self.canonical)


if __name__ == "__main__":
    unittest.main()
