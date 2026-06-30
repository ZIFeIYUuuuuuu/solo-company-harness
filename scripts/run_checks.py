#!/usr/bin/env python3
"""Run detected or provided verification commands and record results."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from harness_common import (
    append_event,
    append_unique,
    detect_test_commands,
    latest_run_id,
    load_state,
    project_root,
    save_state,
    verification_log_path,
)


def run_command(root: Path, command: str, timeout: int) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=str(root),
        shell=True,
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    return {
        "command": command,
        "exit_code": completed.returncode,
        "passed": completed.returncode == 0,
        "output": output[-8000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run harness verification commands.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root.")
    parser.add_argument("--run-id", default="", help="Run id; defaults to latest.")
    parser.add_argument("--risk", choices=["low", "medium", "high"], default="", help="Risk for auto-detection.")
    parser.add_argument("--auto", action="store_true", help="Use detected commands.")
    parser.add_argument("--command", action="append", default=[], help="Command to run; repeatable.")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout per command in seconds.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    run_id = args.run_id or latest_run_id(root)
    state = load_state(root, run_id)
    risk = args.risk or state.get("risk", {}).get("level", "medium")

    commands = list(args.command)
    if args.auto:
        commands.extend(command["command"] for command in detect_test_commands(root, risk))
    if not commands:
        raise SystemExit("No commands provided. Use --auto or --command.")

    log_path = verification_log_path(root, run_id)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    failures = 0
    with log_path.open("a", encoding="utf-8", newline="\n") as log:
        for command in commands:
            print(f"running: {command}")
            log.write(f"\n$ {command}\n")
            try:
                result = run_command(root, command, args.timeout)
            except subprocess.TimeoutExpired as exc:
                result = {
                    "command": command,
                    "exit_code": -1,
                    "passed": False,
                    "output": f"Timed out after {args.timeout}s\n{exc.stdout or ''}\n{exc.stderr or ''}",
                }
            log.write(str(result["output"]) + "\n")
            append_unique(state, "verification.results", result)
            if not result["passed"]:
                failures += 1
                print(f"failed: {command}")
            else:
                print(f"passed: {command}")

    save_state(root, state)
    append_event(root, run_id, "checks_run", {"commands": commands, "failures": failures, "log": str(log_path)})
    print(f"log: {log_path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
