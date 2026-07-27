#!/usr/bin/env python3
"""Record a verification receipt at an explicit evidence level."""

from __future__ import annotations

import argparse

from harness_common import (
    EVIDENCE_LEVELS,
    append_event,
    append_unique,
    latest_run_id,
    load_state,
    now_iso,
    project_root,
    save_state,
    update_evidence_level,
)


SOURCE_BY_LEVEL = {
    0: {"static"},
    1: {"local"},
    2: {"integration"},
    3: {"real-path"},
    4: {"dogfood"},
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Record explicit verification evidence.")
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--run-id", default="", help="Run id; defaults to latest.")
    parser.add_argument("--level", type=int, choices=sorted(EVIDENCE_LEVELS), required=True)
    parser.add_argument("--source", choices=sorted({item for values in SOURCE_BY_LEVEL.values() for item in values}), required=True)
    parser.add_argument("--summary", required=True, help="What was verified.")
    parser.add_argument("--artifact", action="append", default=[], help="Evidence path, URL, command, or receipt; repeatable.")
    args = parser.parse_args()

    if args.source not in SOURCE_BY_LEVEL[args.level]:
        expected = ", ".join(sorted(SOURCE_BY_LEVEL[args.level]))
        raise SystemExit(f"level {args.level} requires source: {expected}")

    root = project_root(args.project_root)
    run_id = args.run_id or latest_run_id(root)
    state = load_state(root, run_id)
    evidence = {
        "level": args.level,
        "label": EVIDENCE_LEVELS[args.level],
        "source": args.source,
        "summary": args.summary,
        "artifacts": args.artifact,
        "recorded_at": now_iso(),
    }
    append_unique(state, "verification.evidence", evidence)
    update_evidence_level(state, args.level)
    path = save_state(root, state)
    append_event(root, run_id, "evidence_recorded", {"evidence": evidence, "state": str(path)})
    print(f"evidence: level={args.level} ({EVIDENCE_LEVELS[args.level]})")
    print(f"summary: {args.summary}")
    print(f"state: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
