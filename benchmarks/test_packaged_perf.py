"""Exercise the actual POSIX executable lookup used by CP41 CI."""

import os
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RESOLVER = ROOT / "tools" / "resolve-packaged-perf"


@unittest.skipUnless(os.name == "posix", "packaged Linux perf uses POSIX tools")
class PackagedPerfTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="mmay perf ü ")
        self.addCleanup(self.temporary.cleanup)
        self.root = pathlib.Path(self.temporary.name)
        self.packages = self.root / "linux tools"
        self.packages.mkdir()

    def resolve(self):
        return subprocess.run(
            [str(RESOLVER), str(self.packages)],
            capture_output=True, text=True, timeout=10, check=False,
        )

    def executable(self, path):
        # Discovery must not execute this fixture.
        path.write_text("#!/bin/sh\nexit 99\n", encoding="utf-8")
        path.chmod(0o755)

    def test_regular_executable(self):
        binary = self.packages / "perf"
        self.executable(binary)
        result = self.resolve()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, str(binary.resolve()) + "\n")
        self.assertEqual(result.stderr, "")

    def test_packaged_relative_symlink(self):
        binary = self.root / "actual perf"
        self.executable(binary)
        (self.packages / "perf").symlink_to("../actual perf")
        result = self.resolve()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, str(binary.resolve()) + "\n")
        self.assertEqual(result.stderr, "")

    def test_missing_broken_nonexecutable_and_directory_fail_closed(self):
        candidate = self.packages / "perf"
        for kind in ("missing", "broken", "nonexecutable", "directory"):
            with self.subTest(kind=kind):
                if kind == "broken":
                    candidate.symlink_to("missing-target")
                elif kind == "nonexecutable":
                    candidate.write_text("not executable", encoding="utf-8")
                elif kind == "directory":
                    candidate.mkdir()
                result = self.resolve()
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertNotEqual(result.stderr, "")
                if kind == "directory":
                    candidate.rmdir()
                elif kind != "missing":
                    candidate.unlink()

    def test_missing_package_directory(self):
        self.packages.rmdir()
        result = self.resolve()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("directory is missing", result.stderr)


if __name__ == "__main__":
    unittest.main()
