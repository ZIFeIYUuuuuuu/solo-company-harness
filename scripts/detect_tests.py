#!/usr/bin/env python3
"""Detect likely verification commands for a project."""

from __future__ import annotations

import argparse
import json

from harness_common import append_event, append_unique, detect_test_commands, latest_run_id, load_state, project_root, save_state


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect verification commands.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root.")
    parser.add_argument("--risk", choices=["low", "medium", "high"], default="", help="Risk level.")
    parser.add_argument("--run-id", default="", help="Run id; defaults to latest when --write-run is set.")
    parser.add_argument("--write-run", action="store_true", help="Write commands into run state.")
    parser.add_argument("--json", action="store_true", help="Print JSON only.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    risk = args.risk
    if not risk and args.write_run:
        state = load_state(root, args.run_id or latest_run_id(root))
        risk = state.get("risk", {}).get("level", "medium")
    risk = risk or "medium"
    commands = detect_test_commands(root, risk)

    if args.write_run:
        run_id = args.run_id or latest_run_id(root)
        state = load_state(root, run_id)
        for command in commands:
            append_unique(state, "verification.commands", {**command, "source": "auto-detected"})
        save_state(root, state)
        append_event(root, run_id, "tests_detected", {"commands": commands})

    if args.json:
        print(json.dumps(commands, ensure_ascii=False, indent=2))
    else:
        if not commands:
            print("No verification commands detected.")
        for command in commands:
            print(f"{command['command']}  # {command['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
