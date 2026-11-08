from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from catalog_measure import measure_catalog
from catalog_session import RunJournal, show_journal, verify_inputs
from perf_protocol import ProtocolError, sha256_file


class CatalogSessionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "work.my"
        self.source.write_text("original")
        self.before = {"work.my": sha256_file(self.source)}
        self.participants = ["marimay-native", "go", "rust", "marimay-vm"]
        self.metadata = {"participants": self.participants, "samples": 3}
        self.workloads = {"work": {}}
        self.commands = {p: {"work": [p]} for p in self.participants}

    def journal(self):
        return RunJournal(self.root / "journals", self.metadata, self.workloads, self.commands)

    def measure(self, journal, timed, progress=None):
        return measure_catalog(
            self.commands, {"work": "ok\n"}, self.participants, ["work"],
            0, 3, timed, progress, journal.observe,
        )

    def records(self, journal):
        return [json.loads(line) for line in journal.path.read_text().splitlines()]

    def test_changed_source_stops_at_first_round_and_retains_observations(self):
        calls = []

        def timed(command, stdout):
            calls.append(command)
            self.source.write_text("changed during measurement")
            return 12.5

        def checkpoint(current, total):
            verify_inputs(self.root, self.before, {}, {})

        with patch("catalog_session.source_hashes", side_effect=lambda root: {
            "work.my": sha256_file(self.source)
        }), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaisesRegex(ProtocolError, "work.my"):
                with self.journal() as journal:
                    self.measure(journal, timed, checkpoint)
                    self.fail("changed inputs must not reach final publication")
        self.assertEqual(len(calls), 4)  # 1 round, not all 3 rounds.
        records = self.records(journal)
        self.assertEqual(len([r for r in records if r["kind"] == "observation"]), 4)
        self.assertEqual(records[-1]["kind"], "aborted")
        self.assertFalse(any(r["kind"] == "complete" for r in records))
        display = show_journal(journal.path)
        self.assertIn("diagnostic only", display)
        self.assertIn("work.my", display)
        self.assertIn("12.50 ms [1/3]", display)

    def test_observation_is_readable_before_next_measurement_and_after_interrupt(self):
        calls = 0

        def timed(command, stdout):
            nonlocal calls
            calls += 1
            if calls == 2:
                self.assertEqual(self.records(journal)[-1]["event"]["elapsed_ms"], 7.0)
                raise KeyboardInterrupt()
            return 7.0

        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(KeyboardInterrupt):
                with self.journal() as journal:
                    self.measure(journal, timed)
        self.assertEqual(self.records(journal)[-1]["error"], "KeyboardInterrupt")
        self.assertIn("7.00 ms [1/3]", show_journal(journal.path))

    def test_failed_and_skipped_cells_are_journaled(self):
        def timed(command, stdout):
            if command == ["marimay-vm"]:
                raise ProtocolError("wrong checksum")
            return 5.0

        with contextlib.redirect_stdout(io.StringIO()):
            with self.journal() as journal:
                _, order, _ = self.measure(journal, timed)
                journal.complete("failed")
        saved = [r["event"] for r in self.records(journal) if r["kind"] == "observation"]
        self.assertEqual(saved, order)
        self.assertEqual(len(saved), 12)
        self.assertIn("marimay-vm=FAILED", show_journal(journal.path))
        self.assertIn("go=5.00 ms [3/3]", show_journal(journal.path))

    def test_incomplete_tail_does_not_destroy_earlier_rows(self):
        with contextlib.redirect_stdout(io.StringIO()):
            with self.journal() as journal:
                self.measure(journal, lambda command, stdout: 3.0)
        with journal.path.open("a") as target:
            target.write('{"kind":')
        display = show_journal(journal.path)
        self.assertIn("Incomplete run", display)
        self.assertIn("3.00 ms [3/3]", display)

    def test_executable_changes_and_missing_anchor_remain_rejections(self):
        binary = self.root / "binary"
        binary.write_text("original binary")
        binaries = {str(binary): sha256_file(binary)}
        with patch("catalog_session.source_hashes", return_value=self.before):
            verify_inputs(self.root, self.before, binaries, {})
            binary.write_text("new binary")
            with self.assertRaisesRegex(ProtocolError, "binary"):
                verify_inputs(self.root, self.before, binaries, {})
            with self.assertRaisesRegex(ProtocolError, "missing.my"):
                verify_inputs(self.root, self.before, {}, {"missing.my": "a" * 64})


if __name__ == "__main__":
    unittest.main()
