#!/usr/bin/env python3
"""Start a harness run and create .harness/runs/<run-id>/state.json."""

from __future__ import annotations

import argparse
from datetime import datetime

from harness_common import (
    append_event,
    detect_risk,
    ensure_harness,
    make_initial_state,
    project_root,
    save_state,
    slugify,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Start a solo-company harness run.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root.")
    parser.add_argument("--title", default="", help="Short run title.")
    parser.add_argument("--goal", default="", help="Goal for this run.")
    parser.add_argument("--non-goal", action="append", default=[], help="Non-goal; repeatable.")
    parser.add_argument("--success", action="append", default=[], help="Success criterion; repeatable.")
    parser.add_argument("--expected-output", default="", help="Expected output.")
    parser.add_argument("--risk", choices=["auto", "low", "medium", "high"], default="auto", help="Risk level.")
    parser.add_argument("--changed-file", action="append", default=[], help="Known file scope for risk detection.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    ensure_harness(root)
    title = args.title or args.goal or "harness run"
    goal = args.goal or title
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id = f"{timestamp}-{slugify(title)}"

    if args.risk == "auto":
        risk = detect_risk(goal, args.changed_file)
    else:
        risk = {"level": args.risk, "source": "manual", "reasons": ["provided by caller"]}

    state = make_initial_state(
        root=root,
        run_id=run_id,
        title=title,
        goal=goal,
        risk=risk,
        success_criteria=args.success,
        non_goal=args.non_goal,
        expected_output=args.expected_output,
    )
    path = save_state(root, state)
    append_event(root, run_id, "start", {"title": title, "goal": goal, "risk": risk})
    print(f"run_id: {run_id}")
    print(f"risk: {risk['level']}")
    for reason in risk.get("reasons", []):
        print(f"- {reason}")
    print(f"state: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
