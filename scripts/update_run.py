#!/usr/bin/env python3
"""Append structured observations to the current harness run."""

from __future__ import annotations

import argparse
import json

from harness_common import append_event, append_unique, latest_run_id, load_state, project_root, save_state, set_value


APPEND_MAP = {
    "file_read": "context.files_read",
    "changed_file": "execution.changed_files",
    "ssot_used": "context.ssot_used",
    "constraint": "context.constraints",
    "planned_change": "contract.planned_changes",
    "boundary": "contract.boundaries",
    "verification_plan": "contract.verification_plan",
    "known_risk": "contract.known_risks",
    "decision": "execution.decisions",
    "surprise": "observe.surprises",
    "lesson": "observe.lessons",
    "risk_note": "observe.risks",
    "followup": "observe.followups",
    "watch": "release.watch",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Update a solo-company harness run.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root.")
    parser.add_argument("--run-id", default="", help="Run id; defaults to latest.")
    parser.add_argument("--status", default="", help="Set run status.")
    parser.add_argument("--rollback-plan", default="", help="Set rollback plan.")
    parser.add_argument("--release-mode", default="", help="Set release mode.")
    parser.add_argument("--command", action="append", default=[], help="Verification command; repeatable.")
    parser.add_argument("--result", action="append", default=[], help="Verification result JSON or text; repeatable.")
    for arg_name in APPEND_MAP:
        parser.add_argument(f"--{arg_name.replace('_', '-')}", action="append", default=[], help=f"Append {arg_name}.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    run_id = args.run_id or latest_run_id(root)
    state = load_state(root, run_id)

    if args.status:
        state["status"] = args.status
    if args.rollback_plan:
        set_value(state, "contract.rollback_plan", args.rollback_plan)
    if args.release_mode:
        set_value(state, "release.mode", args.release_mode)

    for arg_name, dotted_path in APPEND_MAP.items():
        for value in getattr(args, arg_name):
            append_unique(state, dotted_path, value)

    for command in args.command:
        append_unique(state, "verification.commands", {"command": command, "source": "manual"})

    for result in args.result:
        try:
            parsed = json.loads(result)
        except json.JSONDecodeError:
            parsed = {"summary": result}
        append_unique(state, "verification.results", parsed)

    path = save_state(root, state)
    append_event(root, run_id, "update", {"state": str(path)})
    print(f"updated: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
