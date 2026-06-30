#!/usr/bin/env python3
"""Detect task risk from task text and file scope."""

from __future__ import annotations

import argparse
import json

from harness_common import append_event, detect_risk, latest_run_id, load_state, project_root, save_state


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect solo-company harness risk.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root.")
    parser.add_argument("--task", default="", help="Task description.")
    parser.add_argument("--changed-file", action="append", default=[], help="Known changed file; repeatable.")
    parser.add_argument("--run-id", default="", help="Update run id; defaults to latest when --write-run is set.")
    parser.add_argument("--write-run", action="store_true", help="Write detected risk into run state.")
    parser.add_argument("--json", action="store_true", help="Print JSON only.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    risk = detect_risk(args.task, args.changed_file)

    if args.write_run:
        run_id = args.run_id or latest_run_id(root)
        state = load_state(root, run_id)
        state["risk"] = risk
        save_state(root, state)
        append_event(root, run_id, "risk_detected", risk)

    if args.json:
        print(json.dumps(risk, ensure_ascii=False, indent=2))
    else:
        print(f"risk: {risk['level']}")
        for reason in risk.get("reasons", []):
            print(f"- {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
