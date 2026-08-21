from __future__ import annotations

import pathlib
import tempfile
import unittest
from unittest import mock

from perf_environment import locate_runtime, native_tool_version, platform_id
from perf_protocol import ProtocolError


class PerformanceEnvironmentTests(unittest.TestCase):
    def write_runtime(
        self,
        root: pathlib.Path,
        profile: str,
        archive_name: str = "libruda_native_runtime_release.a",
    ) -> pathlib.Path:
        compiler = root / "ruda"
        compiler.write_bytes(b"compiler")
        directory = root / "native-runtime" / "release"
        directory.mkdir(parents=True)
        (directory / archive_name).write_bytes(b"archive")
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

    def test_platform_id_normalizes_every_tier1_architecture(self) -> None:
        cases = (
            ("Linux", "x86_64", "test cpu", "linux-x86_64"),
            ("Linux", "aarch64", "test cpu", "linux-arm64"),
            ("Darwin", "arm64", "Apple M2", "macos-arm64-apple-m2"),
            ("Darwin", "x86_64", "Intel CPU", "macos-x86_64"),
            ("Windows", "AMD64", "test cpu", "windows-x86_64"),
        )
        for system, machine, cpu, expected in cases:
            with self.subTest(system=system, machine=machine), mock.patch(
                "perf_environment.platform.system", return_value=system
            ), mock.patch(
                "perf_environment.platform.machine", return_value=machine
            ), mock.patch(
                "perf_environment.cpu_name", return_value=cpu
            ):
                self.assertEqual(platform_id(), expected)

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

    def test_locates_windows_release_library(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            compiler = self.write_runtime(
                root, "release", "ruda_native_runtime_release.lib"
            )
            _, archive, _ = locate_runtime(compiler, ["runtime 0.0.0-dev"])
            self.assertEqual(archive.suffix, ".lib")

    @mock.patch("perf_environment.tool_version", return_value="unavailable")
    def test_msvc_version_falls_back_to_cmake_metadata(
        self, version: mock.Mock
    ) -> None:
        result = native_tool_version(
            pathlib.Path("cl.exe"),
            pathlib.Path("."),
            {
                "RUDA_NATIVE_C_COMPILER_ID": "MSVC",
                "RUDA_NATIVE_C_COMPILER_VERSION": "19.40",
            },
            "Windows",
        )
        self.assertEqual(result, "MSVC 19.40")
        version.assert_called_once_with(
            ["cl.exe", "/Bv"], pathlib.Path("."), accept_nonzero_output=True
        )

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
