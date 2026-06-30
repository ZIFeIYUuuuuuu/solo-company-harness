#!/usr/bin/env python3
"""Create or update a playbook from a harness run or explicit lessons."""

from __future__ import annotations

import argparse

from harness_common import append_event, append_unique, latest_run_id, load_state, markdown_list, project_root, save_state, slugify, today


def main() -> int:
    parser = argparse.ArgumentParser(description="Update a solo-company playbook.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root.")
    parser.add_argument("--run-id", default="", help="Run id; defaults to latest.")
    parser.add_argument("--topic", default="", help="Playbook topic.")
    parser.add_argument("--lesson", action="append", default=[], help="Lesson to add; repeatable.")
    parser.add_argument("--verification", action="append", default=[], help="Verification guidance; repeatable.")
    parser.add_argument("--failure-mode", action="append", default=[], help="Failure mode; repeatable.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    run_id = args.run_id or latest_run_id(root)
    state = load_state(root, run_id)
    topic = args.topic or state.get("title") or run_id
    path = root / "docs" / "playbooks" / f"{slugify(topic)}.md"
    path.parent.mkdir(parents=True, exist_ok=True)

    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    lessons = args.lesson or state.get("observe", {}).get("lessons", [])
    verification = args.verification or [
        item.get("command", str(item)) if isinstance(item, dict) else str(item)
        for item in state.get("verification", {}).get("commands", [])
    ]
    failure_modes = args.failure_mode or state.get("observe", {}).get("risks", [])

    if not existing:
        content = f"""# Playbook: {topic}

## When To Use
Use when a future task resembles the observed run `{run_id}`.

## Steps
- TBD

## Verification
{markdown_list(verification)}

## Failure Modes
{markdown_list(failure_modes)}

## Reusable Lessons
{markdown_list(lessons)}

## Observed Runs
- {today()}: {run_id}
"""
    else:
        content = existing.rstrip() + f"""

## Update {today()} - {run_id}

### Reusable Lessons
{markdown_list(lessons)}

### Verification
{markdown_list(verification)}

### Failure Modes
{markdown_list(failure_modes)}
"""

    path.write_text(content, encoding="utf-8", newline="\n")
    append_unique(state, "distill.playbooks_updated", str(path))
    save_state(root, state)
    append_event(root, run_id, "playbook_updated", {"path": str(path)})
    print(f"playbook: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
