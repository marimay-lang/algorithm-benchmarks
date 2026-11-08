from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from catalog_snapshot import compiler_path, create_workspace, pin_external_executables, pin_toolchain
from perf_protocol import ProtocolError, sha256_file


class SnapshotTests(unittest.TestCase):
    def test_compiler_selection_prefers_override_then_system_path(self):
        repository = Path("/workspace/algorithm-benchmarks")
        with patch.dict("os.environ", {}, clear=True), patch("shutil.which", return_value="/installed/mmay"):
            self.assertEqual(compiler_path(repository), Path("/installed/mmay"))
            with patch.dict("os.environ", {"MMAY": "/candidate/mmay"}):
                self.assertEqual(compiler_path(repository), Path("/candidate/mmay"))
        with patch.dict("os.environ", {}, clear=True), patch("shutil.which", return_value=None):
            self.assertEqual(compiler_path(repository), Path("/workspace/marimay/build/release/mmay"))
            self.assertEqual(compiler_path(Path("/workspace/benchmarks/algorithm-benchmarks")), Path("/workspace/marimay/build/release/mmay"))

    def fixture(self, root, installed=False):
        prefix = root / "origin"
        compiler = prefix / ("bin/mmay" if installed else "build/mmay")
        compiler.parent.mkdir(parents=True)
        compiler.write_bytes(b"compiler-v1")
        compiler.chmod(0o755)
        archive = compiler.parent / "native-runtime/release/runtime.a"
        archive.parent.mkdir(parents=True)
        archive.write_bytes(b"runtime-v1")
        manifest = archive.parent / "mmay-native-runtime.manifest"
        manifest.write_text("manifest-v1")
        if installed:
            include = prefix / "include"
            (include / "mmay/base").mkdir(parents=True)
            (include / "mmay/base/allocator.h").write_text("allocator-v1")
        else:
            includes = [prefix / "bootstrap/include", prefix / "runtime/include"]
            for index, include in enumerate(includes):
                (include / "mmay").mkdir(parents=True)
                (include / f"mmay/header{index}.h").write_text(f"header-{index}")
            config = compiler.parent / "generated/mmay/build_config.h"
            config.parent.mkdir(parents=True)
            config.write_text("\n".join(
                f"#define MMAY_NATIVE_{name} {json.dumps(str(path))}"
                for name, path in zip(["BOOTSTRAP_INCLUDE", "RUNTIME_INCLUDE"], includes)
            ))
        metadata = {"artifacts": {
            "mmay_compiler": {"path": str(compiler), "sha256": sha256_file(compiler), "revision": "language-revision"},
            "runtime": {"runtime": "0.1.0-alpha.1", "path": str(archive), "sha256": sha256_file(archive),
                        "manifest_path": str(manifest), "manifest_sha256": sha256_file(manifest)},
        }}
        return compiler, metadata

    def test_binary_runtime_headers_survive_origin_replacement(self):
        for installed in [False, True]:
            with self.subTest(installed=installed), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                compiler, metadata = self.fixture(root, installed)
                workspace = create_workspace(root / "runs")
                frozen, hashes = pin_toolchain(compiler, workspace, metadata)
                for path in (root / "origin").rglob("*"):
                    if path.is_file():
                        path.write_bytes(b"changed-origin")
                self.assertEqual(frozen.read_bytes(), b"compiler-v1")
                self.assertEqual(frozen.stat().st_mode & 0o111, 0o111)
                self.assertEqual(metadata["artifacts"]["mmay_compiler"]["revision"], "language-revision")
                self.assertTrue(Path(metadata["artifacts"]["runtime"]["path"]).is_relative_to(workspace))
                self.assertTrue(all(sha256_file(Path(path)) == digest for path, digest in hashes.items()))
                self.assertTrue(all(Path(path).stat().st_nlink == 1 for path in hashes))
                self.assertGreater(len(hashes), 3)

    def test_changed_version_before_snapshot_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            compiler, metadata = self.fixture(root)
            compiler.write_bytes(b"new-compiler")
            with self.assertRaisesRegex(ProtocolError, "changed while preparing"):
                pin_toolchain(compiler, create_workspace(root / "runs"), metadata)

    def test_mutation_during_copy_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            compiler, metadata = self.fixture(root)
            from shutil import copy2
            def replace_source(source, destination):
                result = copy2(source, destination)
                if source == compiler:
                    source.write_bytes(b"changed-during-copy")
                return result
            with patch("catalog_snapshot.shutil.copy2", side_effect=replace_source):
                with self.assertRaisesRegex(ProtocolError, "changed while copying"):
                    pin_toolchain(compiler, create_workspace(root / "runs"), metadata)

    def test_external_executables_are_unique_copies_and_vm_keeps_its_layout(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            external = root / "rust-target/catalog"
            external.parent.mkdir()
            external.write_bytes(b"rust-v1")
            workspaces = [create_workspace(root / "runs") for _ in range(2)]
            snapshots = []
            for workspace in workspaces:
                vm = workspace / "toolchain/bin/mmay"
                vm.parent.mkdir(parents=True)
                vm.write_bytes(b"vm-v1")
                commands = {"rust": {"a": [str(external), "a"], "b": [str(external), "b"]},
                            "marimay-vm": {"a": [str(vm), "run"]}}
                pin_external_executables(commands, workspace)
                self.assertEqual(commands["rust"]["a"][0], commands["rust"]["b"][0])
                self.assertEqual(commands["marimay-vm"]["a"][0], str(vm))
                snapshots.append(Path(commands["rust"]["a"][0]))
            external.write_bytes(b"new-rust-binary")
            self.assertNotEqual(snapshots[0], snapshots[1])
            self.assertTrue(all(path.read_bytes() == b"rust-v1" for path in snapshots))

    def test_missing_headers_fail_before_measurement(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            compiler, metadata = self.fixture(root)
            (compiler.parent / "generated/mmay/build_config.h").unlink()
            with self.assertRaisesRegex(ProtocolError, "cannot pin compiler headers"):
                pin_toolchain(compiler, create_workspace(root / "runs"), metadata)


if __name__ == "__main__":
    unittest.main()
