#!/usr/bin/env python3
"""Create a skill improvement proposal from the feedback queue."""

from __future__ import annotations

import argparse

from harness_common import feedback_dir, project_root, today


def main() -> int:
    parser = argparse.ArgumentParser(description="Propose, but do not apply, skill updates.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root.")
    parser.add_argument("--skill-path", default="", help="Path to the skill being improved.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    queue = feedback_dir(root) / "skill-improvements.md"
    proposal = feedback_dir(root) / "proposed-skill-update.md"

    if not queue.exists():
        raise SystemExit(f"No feedback queue found: {queue}")

    content = f"""# Proposed Skill Update - {today()}

Skill path: {args.skill_path or "TBD"}

## Evidence

The following feedback was collected from harness runs:

{queue.read_text(encoding="utf-8").strip()}

## Proposed Change

TBD: Convert the repeated feedback above into a minimal SKILL.md or script change.

## Review Checklist

- Does this change improve repeated behavior rather than one-off preference?
- Is the change general enough for future projects?
- Does it keep the skill concise?
- Does it avoid silently weakening verification?

## Apply Policy

Do not apply automatically. Patch the skill only after review.
"""
    proposal.write_text(content, encoding="utf-8", newline="\n")
    print(f"proposal: {proposal}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
