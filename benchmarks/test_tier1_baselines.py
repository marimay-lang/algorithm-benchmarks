from __future__ import annotations

import copy
import pathlib
import unittest

from perf_protocol import ProtocolError, TIER1_TARGETS, load_json
from tier1_baselines import (
    REGISTRY_SCHEMA,
    registry_path,
    resolve_registry_path,
    validate_registry_shape,
    validate_tier1_registry,
)


class Tier1BaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = pathlib.Path(__file__).resolve().parents[1]
        cls.registry = load_json(registry_path(cls.repository))

    def complete_registry(self) -> dict[str, object]:
        return {
            "schema": REGISTRY_SCHEMA,
            "protocol_sha256": "1" * 64,
            "required_targets": list(TIER1_TARGETS),
            "baselines": [
                {
                    "target": target,
                    "platform_id": target,
                    "probes": f"benchmarks/results/{target}-probes.json",
                    "algorithms": f"benchmarks/results/{target}-algorithms.json",
                    "budget": f"benchmarks/budgets/{target}.json",
                }
                for target in TIER1_TARGETS
            ],
        }

    def test_complete_shape_requires_every_tier1_target_once(self) -> None:
        registry = self.complete_registry()
        self.assertEqual(
            len(validate_registry_shape(registry, require_complete=True)), 5
        )
        registry["baselines"].pop()
        with self.assertRaisesRegex(ProtocolError, "incomplete; missing"):
            validate_registry_shape(registry, require_complete=True)

    def test_rejects_duplicate_target_and_target_contract_drift(self) -> None:
        duplicate = self.complete_registry()
        duplicate["baselines"][1]["target"] = duplicate["baselines"][0]["target"]
        duplicate["baselines"][1]["platform_id"] = duplicate["baselines"][0][
            "platform_id"
        ]
        with self.assertRaisesRegex(ProtocolError, "duplicate Tier 1"):
            validate_registry_shape(duplicate, require_complete=True)
        drifted = self.complete_registry()
        drifted["required_targets"] = list(TIER1_TARGETS[:-1])
        with self.assertRaisesRegex(ProtocolError, "target contract drifted"):
            validate_registry_shape(drifted, require_complete=True)

    def test_registry_paths_cannot_escape_owned_directories(self) -> None:
        with self.assertRaisesRegex(ProtocolError, "escapes"):
            resolve_registry_path(
                self.repository,
                "benchmarks/results/../performance_protocol.json",
                pathlib.Path("benchmarks/results"),
            )

    def test_current_entries_are_valid_but_do_not_claim_tier1_completion(self) -> None:
        count, targets = validate_tier1_registry(
            self.repository, require_complete=False
        )
        self.assertEqual(count, len(self.registry["baselines"]))
        self.assertEqual(
            targets, [entry["target"] for entry in self.registry["baselines"]]
        )
        with self.assertRaisesRegex(ProtocolError, "registry is incomplete"):
            validate_tier1_registry(self.repository)

    def test_rejects_platform_id_drift_before_loading_artifacts(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["baselines"][0]["platform_id"] = "windows-x86_64"
        with self.assertRaisesRegex(ProtocolError, "inconsistent with target"):
            validate_registry_shape(registry, require_complete=False)


if __name__ == "__main__":
    unittest.main()
