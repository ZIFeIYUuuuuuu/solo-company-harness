from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from contract import validate_contract  # noqa: E402
from harness_common import make_initial_state, migrate_state, resolve_operating_mode  # noqa: E402
from resolve_mode import document_check  # noqa: E402


class HarnessTest(unittest.TestCase):
    def test_risk_maps_to_progressive_modes(self) -> None:
        self.assertEqual(resolve_operating_mode("low"), "explore")
        self.assertEqual(resolve_operating_mode("medium"), "delivery")
        self.assertEqual(resolve_operating_mode("high"), "high-assurance")
        with self.assertRaises(SystemExit):
            resolve_operating_mode("high", "explore")

    def test_explore_contract_is_compact_and_valid(self) -> None:
        state = make_initial_state(
            Path("."),
            "test-run",
            "prototype",
            "Try a local prototype",
            {"level": "low", "source": "test", "reasons": []},
            success_criteria=["The prototype can be exercised"],
            operating_mode="explore",
        )
        self.assertEqual(state["status"], "in_progress")
        self.assertEqual(state["delivery_contract"]["status"], "compact-approved")
        self.assertEqual(validate_contract(state), [])
        self.assertEqual(state["verification"]["required_evidence_level"], 0)

    def test_delivery_contract_requires_full_fields(self) -> None:
        state = make_initial_state(
            Path("."),
            "test-run",
            "feature",
            "Ship a feature",
            {"level": "medium", "source": "test", "reasons": []},
            operating_mode="delivery",
        )
        errors = validate_contract(state)
        self.assertIn("missing contract.why", errors)
        self.assertIn("missing contract.anti_cheat; explicitly record none identified when applicable", errors)
        self.assertEqual(state["verification"]["required_evidence_level"], 1)

    def test_legacy_state_is_marked_without_new_evidence_gate(self) -> None:
        state = migrate_state({"schema_version": 1, "status": "in_progress"})
        self.assertEqual(state["schema_version"], 2)
        self.assertTrue(state["compatibility"]["legacy_state"])

    def test_approved_stale_document_is_not_design_locked(self) -> None:
        path = ROOT / "tests" / "fixtures" / "stale-module.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "Status: approved\nOwner: owner\nUpdated: 2020-01-01\nScope\nNon-goal\nAcceptance\n",
            encoding="utf-8",
        )
        try:
            result = document_check(path, ("scope", "non-goal", "acceptance"), stale_after_days=90)
            self.assertTrue(result["stale"])
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
