from __future__ import annotations

import sys
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from contract import validate_contract  # noqa: E402
from harness_common import make_initial_state, migrate_state, resolve_operating_mode  # noqa: E402
from host_adapters import default_destination, normalize_host  # noqa: E402
from init_agents import upsert_instruction  # noqa: E402
from install_host import install_skill  # noqa: E402
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

    def test_explore_start_does_not_write_full_contract_file(self) -> None:
        with self.subTest(mode="explore"):
            import tempfile

            with tempfile.TemporaryDirectory() as project:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "scripts" / "start_run.py"),
                        project,
                        "--title",
                        "prototype",
                        "--goal",
                        "Try a local idea",
                        "--mode",
                        "explore",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                run_id = next(line.split(":", 1)[1].strip() for line in result.stdout.splitlines() if line.startswith("run_id:"))
                run_dir = Path(project) / ".harness" / "runs" / run_id
                self.assertTrue((run_dir / "state.json").exists())
                self.assertTrue((run_dir / "events.jsonl").exists())
                self.assertFalse((run_dir / "delivery-contract.md").exists())

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

    def test_host_aliases_and_default_destinations_are_stable(self) -> None:
        self.assertEqual(normalize_host("claude"), "claude-code")
        self.assertEqual(normalize_host("open-code"), "opencode")
        home = Path("/tmp/agent-home")
        self.assertEqual(
            default_destination("claude-code", home),
            home / ".claude" / "skills" / "solo-company-harness",
        )
        self.assertIsNone(default_destination("generic", home))

    def test_init_agents_uses_claude_instruction_file_and_preserves_content(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as project:
            root = Path(project)
            claude = root / "CLAUDE.md"
            claude.write_text("# Project rules\n\nKeep this paragraph.\n", encoding="utf-8")
            path = upsert_instruction(root, "/tmp/skill", "claude-code")
            self.assertEqual(path.name, "CLAUDE.md")
            content = path.read_text(encoding="utf-8")
            self.assertIn("Keep this paragraph.", content)
            self.assertIn("Host: claude-code", content)
            self.assertIn("Use the solo-company-harness skill", content)

    def test_install_skill_copies_portable_payload_and_requires_update(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as target:
            destination = Path(target) / "skill"
            installed = install_skill(ROOT, destination)
            self.assertEqual(installed, destination.resolve())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "scripts" / "install_host.py").is_file())
            self.assertFalse((installed / "tests").exists())
            with self.assertRaises(FileExistsError):
                install_skill(ROOT, destination)
            install_skill(ROOT, destination, update=True)


if __name__ == "__main__":
    unittest.main()
