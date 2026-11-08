from __future__ import annotations

import copy
import pathlib
import tempfile
import unittest
from unittest.mock import patch

from marimay_toolchain import load_contract, resolve_compiler, validate_contract, validate_version
from perf_protocol import ProtocolError


class MarimayToolchainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = pathlib.Path(__file__).resolve().parents[1]
        _, cls.contract = load_contract(cls.repository)
        cls.version = {
            "schema": cls.contract["version_schema"],
            "compiler": cls.contract["compiler"],
            "runtime": cls.contract["runtime"],
            "language": cls.contract["language"],
            "standardLibrary": {"version": cls.contract["standard_library"]},
            "commands": {"available": cls.contract["required_commands"]},
        }

    def test_compiler_discovery_supports_grouped_and_sibling_workspaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, patch.dict("os.environ", {}, clear=True):
            root = pathlib.Path(temporary)
            repository = root / "benchmarks/algorithm-benchmarks"
            repository.mkdir(parents=True)
            grouped = root / "marimay/build/release/mmay"
            sibling = repository.parent / "marimay/build/release/mmay"
            for binary in (grouped, sibling):
                binary.parent.mkdir(parents=True)
                binary.write_bytes(b"compiler fixture")
            self.assertEqual(resolve_compiler(repository), grouped.resolve())
            with patch.dict("os.environ", {"MMAY": str(root / "candidate/mmay")}):
                self.assertEqual(resolve_compiler(repository), (root / "candidate/mmay").resolve())
            grouped.unlink()
            self.assertEqual(resolve_compiler(repository), sibling.resolve())
            sibling.unlink()
            self.assertEqual(resolve_compiler(repository), grouped.resolve())
            grouped.write_bytes(b"compiler fixture")
            self.assertEqual(resolve_compiler(root / "algorithm-benchmarks"), grouped.resolve())

    def test_committed_contract_accepts_matching_version(self) -> None:
        validate_version(self.contract, self.version)

    def test_rejects_an_old_compiler(self) -> None:
        version = copy.deepcopy(self.version)
        version["compiler"] = "0.0.0-dev"
        with self.assertRaisesRegex(ProtocolError, "compiler mismatch"):
            validate_version(self.contract, version)

    def test_rejects_a_missing_command(self) -> None:
        version = copy.deepcopy(self.version)
        version["commands"]["available"].remove("test")
        with self.assertRaisesRegex(ProtocolError, "lacks required commands: test"):
            validate_version(self.contract, version)

    def test_rejects_unsorted_required_commands(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["required_commands"] = list(reversed(contract["required_commands"]))
        with self.assertRaisesRegex(ProtocolError, "unique sorted names"):
            validate_contract(contract)


if __name__ == "__main__":
    unittest.main()
