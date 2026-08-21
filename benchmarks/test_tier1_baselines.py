from __future__ import annotations

import copy
import pathlib
import unittest

from perf_protocol import ProtocolError, TIER1_TARGETS, load_json
from tier1_baselines import (
    CHECKPOINT_21_GATE,
    CHECKPOINT_21_TARGETS,
    PUBLIC_ALPHA_GATE,
    REGISTRY_SCHEMA,
    registry_path,
    required_targets_for_gate,
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
            "checkpoint_21_targets": list(CHECKPOINT_21_TARGETS),
            "public_alpha_targets": list(TIER1_TARGETS),
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

    def test_checkpoint_and_public_alpha_gates_have_distinct_completion(self) -> None:
        registry = self.complete_registry()
        self.assertEqual(
            len(validate_registry_shape(registry, gate=PUBLIC_ALPHA_GATE)), 5
        )
        registry["baselines"] = registry["baselines"][:1]
        self.assertEqual(
            len(validate_registry_shape(registry, gate=CHECKPOINT_21_GATE)), 1
        )
        with self.assertRaisesRegex(
            ProtocolError, "public-alpha.*incomplete; missing: linux-arm64"
        ):
            validate_registry_shape(registry, gate=PUBLIC_ALPHA_GATE)

    def test_rejects_duplicate_target(self) -> None:
        duplicate = self.complete_registry()
        duplicate["baselines"][1]["target"] = duplicate["baselines"][0]["target"]
        duplicate["baselines"][1]["platform_id"] = duplicate["baselines"][0][
            "platform_id"
        ]
        with self.assertRaisesRegex(ProtocolError, "duplicate Tier 1"):
            validate_registry_shape(duplicate, gate=PUBLIC_ALPHA_GATE)

    def test_rejects_checkpoint_and_public_alpha_target_contract_drift(self) -> None:
        checkpoint_drift = self.complete_registry()
        checkpoint_drift["checkpoint_21_targets"] = ["macos-arm64"]
        with self.assertRaisesRegex(ProtocolError, "checkpoint 21 target contract"):
            validate_registry_shape(checkpoint_drift, gate=CHECKPOINT_21_GATE)
        public_alpha_drift = self.complete_registry()
        public_alpha_drift["public_alpha_targets"] = list(TIER1_TARGETS[:-1])
        with self.assertRaisesRegex(ProtocolError, "public alpha target contract"):
            validate_registry_shape(public_alpha_drift, gate=PUBLIC_ALPHA_GATE)

    def test_rejects_unknown_gate(self) -> None:
        with self.assertRaisesRegex(ProtocolError, "unsupported.*gate"):
            required_targets_for_gate(self.complete_registry(), "nightly")

    def test_registry_paths_cannot_escape_owned_directories(self) -> None:
        with self.assertRaisesRegex(ProtocolError, "escapes"):
            resolve_registry_path(
                self.repository,
                "benchmarks/results/../performance_protocol.json",
                pathlib.Path("benchmarks/results"),
            )

    def test_current_entries_complete_checkpoint_but_not_public_alpha(self) -> None:
        count, targets = validate_tier1_registry(self.repository)
        self.assertEqual(count, len(self.registry["baselines"]))
        self.assertEqual(
            targets, [entry["target"] for entry in self.registry["baselines"]]
        )
        with self.assertRaisesRegex(
            ProtocolError, "public-alpha.*registry is incomplete"
        ):
            validate_tier1_registry(self.repository, gate=PUBLIC_ALPHA_GATE)

    def test_rejects_platform_id_drift_before_loading_artifacts(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["baselines"][0]["platform_id"] = "windows-x86_64"
        with self.assertRaisesRegex(ProtocolError, "inconsistent with target"):
            validate_registry_shape(registry, gate=CHECKPOINT_21_GATE)


if __name__ == "__main__":
    unittest.main()
