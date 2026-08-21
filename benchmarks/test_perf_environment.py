from __future__ import annotations

import pathlib
import tempfile
import unittest

from perf_environment import locate_runtime, platform_id
from perf_protocol import ProtocolError


class PerformanceEnvironmentTests(unittest.TestCase):
    def write_runtime(self, root: pathlib.Path, profile: str) -> pathlib.Path:
        compiler = root / "ruda"
        compiler.write_bytes(b"compiler")
        directory = root / "native-runtime" / "release"
        directory.mkdir(parents=True)
        (directory / "libruda_native_runtime_release.a").write_bytes(b"archive")
        (directory / "ruda-native-runtime.manifest").write_text(
            "ruda-native-runtime-v1\n"
            f"profile={profile}\n"
            "runtime=0.0.0-dev\n"
            "host=Test\n"
            "processor=test\n"
            "compiler=Test-1\n",
            encoding="utf-8",
        )
        return compiler

    def test_platform_id_is_stable_and_nonempty(self) -> None:
        self.assertRegex(platform_id(), r"^[a-z0-9_-]+(?:-[a-z0-9_-]+)+$")

    def test_locates_release_runtime_and_rejects_debug_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            compiler = self.write_runtime(root, "release")
            manifest, archive, values = locate_runtime(
                compiler, ["runtime 0.0.0-dev"]
            )
            self.assertTrue(manifest.is_file())
            self.assertTrue(archive.is_file())
            self.assertEqual(values["profile"], "release")
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            compiler = self.write_runtime(root, "debug")
            with self.assertRaisesRegex(ProtocolError, "wrong runtime profile"):
                locate_runtime(compiler, ["runtime 0.0.0-dev"])

    def test_rejects_incomplete_runtime_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            compiler = self.write_runtime(root, "release")
            manifest = root / "native-runtime" / "release" / "ruda-native-runtime.manifest"
            manifest.write_text(
                "ruda-native-runtime-v1\nprofile=release\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ProtocolError, "incomplete"):
                locate_runtime(compiler, ["runtime 0.0.0-dev"])


if __name__ == "__main__":
    unittest.main()
