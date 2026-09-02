from __future__ import annotations

import unittest

from perf_protocol import ProtocolError
from cp41_perf import EVENTS, parse_perf_csv, summarize


class Checkpoint41PerfTests(unittest.TestCase):
    def test_parses_every_required_counter(self) -> None:
        text = "".join(
            f"{index + 100},,{event},100.00,100.00,\n"
            for index, event in enumerate(EVENTS)
        )
        parsed = parse_perf_csv(text)
        self.assertEqual(set(parsed), set(EVENTS))
        self.assertEqual(parsed["cycles"], 100)

    def test_rejects_unavailable_counter(self) -> None:
        text = "<not supported>,,cycles,0.00,0.00,\n"
        with self.assertRaises(ProtocolError):
            parse_perf_csv(text)

    def test_summarizes_without_discarding_samples(self) -> None:
        result = summarize([100, 101, 102, 103, 104])
        self.assertEqual(result["median"], 102.0)
        self.assertEqual(result["min"], 100.0)
        self.assertEqual(result["max"], 104.0)


if __name__ == "__main__":
    unittest.main()
