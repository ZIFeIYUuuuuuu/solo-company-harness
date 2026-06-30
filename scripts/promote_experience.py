#!/usr/bin/env python3
"""Promote user-approved project lessons into the skill's approved experience reference."""

from __future__ import annotations

import argparse
from pathlib import Path

from harness_common import load_state, project_root, today


def append_entry(skill_root: Path, entry: str) -> Path:
    path = skill_root / "references" / "approved-experience.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(
            "# Approved Experience\n\n"
            "User-approved cross-project lessons live here.\n\n"
            "## Entries\n\n",
            encoding="utf-8",
            newline="\n",
        )
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(entry.rstrip() + "\n")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote approved lessons into the skill folder.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root containing .harness runs.")
    parser.add_argument("--skill-root", required=True, help="Path to the solo-company-harness skill folder.")
    parser.add_argument("--approved-by", required=True, help="User/reviewer who approved promotion.")
    parser.add_argument("--run-id", default="", help="Optional run id to promote lessons from.")
    parser.add_argument("--lesson", action="append", default=[], help="Approved lesson; repeatable.")
    parser.add_argument("--scope", default="cross-project", help="Scope where this lesson applies.")
    parser.add_argument("--evidence", action="append", default=[], help="Evidence link/path; repeatable.")
    parser.add_argument("--update-skill-md", action="store_true", help="Record that SKILL.md should be updated manually.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    skill_root = project_root(args.skill_root)
    lessons = list(args.lesson)
    evidence = list(args.evidence)
    run_id = args.run_id

    if run_id:
        state = load_state(root, run_id)
        lessons.extend(state.get("observe", {}).get("lessons", []))
        if state.get("distill", {}).get("case_log"):
            evidence.append(state["distill"]["case_log"])

    if not lessons:
        raise SystemExit("No lessons provided. Use --lesson or --run-id with recorded lessons.")

    lesson_lines = "\n".join(f"- {lesson}" for lesson in lessons)
    evidence_lines = "\n".join(f"- {item}" for item in evidence) if evidence else "- Not provided"
    skill_md_note = (
        "\n- SKILL.md update requested: yes. Review and patch the core workflow if this changes operating behavior."
        if args.update_skill_md
        else "\n- SKILL.md update requested: no. Keep this as reference experience."
    )

    entry = f"""### {today()} - Approved Lesson

Approved by: {args.approved_by}
Scope: {args.scope}
Source run: {run_id or "manual"}

Lessons:
{lesson_lines}

Evidence:
{evidence_lines}
{skill_md_note}

"""
    path = append_entry(skill_root, entry)
    print(f"approved_experience: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
