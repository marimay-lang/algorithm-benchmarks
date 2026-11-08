from __future__ import annotations

import pathlib
import subprocess
import sys
import unittest
from unittest.mock import patch

import run
from perf_protocol import ProtocolError


class RunDiagnosticsTests(unittest.TestCase):
    def test_reports_captured_command_failure(self) -> None:
        error = subprocess.CalledProcessError(
            1,
            ["/tool path/mmay", "fmt", "/corpus path/marimay", "--check"],
            output="build output\n",
            stderr="error[F0004]: file does not match canonical formatting\n",
        )
        with patch.object(run, "main", side_effect=error):
            with self.assertRaises(SystemExit) as failure:
                run.entrypoint()
        self.assertEqual(
            str(failure.exception),
            "benchmark command failed (exit 1): '/tool path/mmay' fmt "
            "'/corpus path/marimay' --check\nbuild output\n"
            "error[F0004]: file does not match canonical formatting",
        )

    def test_reports_command_without_output(self) -> None:
        error = subprocess.CalledProcessError(7, ["compiler", "build"])
        with patch.object(run, "main", side_effect=error):
            with self.assertRaisesRegex(
                SystemExit, r"^benchmark command failed \(exit 7\): compiler build$"
            ):
                run.entrypoint()

    def test_keeps_protocol_diagnostics(self) -> None:
        with patch.object(run, "main", side_effect=ProtocolError("checksum mismatch")):
            with self.assertRaisesRegex(
                SystemExit, "^performance protocol error: checksum mismatch$"
            ):
                run.entrypoint()

    def test_success_returns_normally(self) -> None:
        with patch.object(run, "main") as main:
            self.assertIsNone(run.entrypoint())
        main.assert_called_once_with()

    def test_process_failure_has_diagnostic_and_no_traceback(self) -> None:
        script = (
            "import subprocess, run\n"
            "def fail():\n"
            "    raise subprocess.CalledProcessError(1, ['mmay', 'fmt'], "
            "stderr='error[F0004]: synthetic format failure\\n')\n"
            "run.main = fail\n"
            "run.entrypoint()\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=pathlib.Path(__file__).resolve().parent,
            text=True,
            capture_output=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr,
            "benchmark command failed (exit 1): mmay fmt\n"
            "error[F0004]: synthetic format failure\n",
        )


if __name__ == "__main__":
    unittest.main()
