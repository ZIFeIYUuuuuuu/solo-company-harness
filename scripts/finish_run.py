#!/usr/bin/env python3
"""Finish a harness run, generate case logs, and queue reusable feedback."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from harness_common import (
    append_event,
    append_unique,
    feedback_dir,
    latest_run_id,
    load_state,
    markdown_list,
    project_root,
    save_state,
    slugify,
    today,
    unique_path,
)


def case_log_needed(state: dict, mode: str) -> bool:
    if mode == "always":
        return True
    if mode == "never":
        return False
    risk = state.get("risk", {}).get("level", "low")
    if risk in {"medium", "high"}:
        return True
    if state.get("observe", {}).get("surprises"):
        return True
    if state.get("observe", {}).get("lessons"):
        return True
    results = state.get("verification", {}).get("results", [])
    return any(isinstance(item, dict) and item.get("passed") is False for item in results)


def write_case_log(root: Path, state: dict) -> Path:
    title = state.get("title") or state["run_id"]
    path = unique_path(root / "docs" / "case-log" / f"{today()}-{slugify(title)}.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"""# Case Log: {title}

## Intent
Goal: {state.get("intent", {}).get("goal", "")}

Success criteria:
{markdown_list(state.get("intent", {}).get("success_criteria", []))}

Risk: {state.get("risk", {}).get("level", "unknown")}

## Context
Files read:
{markdown_list(state.get("context", {}).get("files_read", []))}

SSOT used:
{markdown_list(state.get("context", {}).get("ssot_used", []))}

## Gates
First-principles check:
{markdown_list(state.get("gates", {}).get("first_principles", []))}

Assumptions:
{markdown_list(state.get("gates", {}).get("assumptions", []))}

Adversarial findings:
{markdown_list(state.get("gates", {}).get("adversarial_findings", []))}

Edge cases:
{markdown_list(state.get("gates", {}).get("edge_cases", []))}

Rejected options:
{markdown_list(state.get("gates", {}).get("rejected_options", []))}

## Delivery Contract
Status: {state.get("delivery_contract", {}).get("status", "legacy or not initialized")}
Why:
{state.get("delivery_contract", {}).get("why", "")}

Acceptance criteria:
{markdown_list(state.get("delivery_contract", {}).get("acceptance", []))}

Anti-gaming rules:
{markdown_list(state.get("delivery_contract", {}).get("anti_cheat", []))}

Infeasible or blocked paths:
{markdown_list(state.get("delivery_contract", {}).get("infeasible", []))}

Alternatives and trade-offs:
{markdown_list(state.get("delivery_contract", {}).get("alternatives", []))}

## Changes
{markdown_list(state.get("execution", {}).get("changed_files", []))}

## Verification
Commands:
{markdown_list(state.get("verification", {}).get("commands", []))}

Results:
{markdown_list(state.get("verification", {}).get("results", []))}

## Surprises
{markdown_list(state.get("observe", {}).get("surprises", []))}

## Reusable Lessons
{markdown_list(state.get("observe", {}).get("lessons", []))}

## Follow-ups
{markdown_list(state.get("observe", {}).get("followups", []))}
"""
    path.write_text(content, encoding="utf-8", newline="\n")
    return path


def all_lessons(root: Path) -> list[str]:
    lessons: list[str] = []
    for path in (root / ".harness" / "runs").glob("*/state.json"):
        try:
            state = load_state(root, path.parent.name)
        except Exception:
            continue
        lessons.extend(state.get("observe", {}).get("lessons", []))
    return lessons


def repeated_lessons(root: Path) -> list[str]:
    normalized = Counter(slugify(lesson) for lesson in all_lessons(root) if lesson)
    repeated = {key for key, count in normalized.items() if count >= 2}
    return [lesson for lesson in all_lessons(root) if slugify(lesson) in repeated]


def append_feedback(root: Path, state: dict, message: str) -> Path:
    path = feedback_dir(root) / "skill-improvements.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    block = f"""
## {today()} - {state.get("title", state["run_id"])}

Observation:
{message}

Evidence:
- Run: {state["run_id"]}
- Risk: {state.get("risk", {}).get("level", "unknown")}
"""
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(block)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Finish a solo-company harness run.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root.")
    parser.add_argument("--run-id", default="", help="Run id; defaults to latest.")
    parser.add_argument("--status", default="completed", choices=["completed", "blocked", "failed"], help="Final status.")
    parser.add_argument("--summary", default="", help="Short completion summary.")
    parser.add_argument("--surprise", action="append", default=[], help="Add surprise; repeatable.")
    parser.add_argument("--lesson", action="append", default=[], help="Add reusable lesson; repeatable.")
    parser.add_argument("--risk-note", action="append", default=[], help="Add residual risk; repeatable.")
    parser.add_argument("--followup", action="append", default=[], help="Add follow-up; repeatable.")
    parser.add_argument("--case-log", choices=["auto", "always", "never"], default="auto", help="Case log policy.")
    parser.add_argument("--skill-feedback", default="", help="Queue a suggested skill improvement.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    run_id = args.run_id or latest_run_id(root)
    state = load_state(root, run_id)
    contract = state.get("delivery_contract")
    if args.status == "completed" and contract and contract.get("status") != "approved":
        print("cannot complete: delivery contract is not approved")
        print("run contract.py check and contract.py approve after the owner reviews it")
        return 1
    state["status"] = args.status

    if args.summary:
        append_unique(state, "observe.lessons", f"Summary: {args.summary}")
    for value in args.surprise:
        append_unique(state, "observe.surprises", value)
    for value in args.lesson:
        append_unique(state, "observe.lessons", value)
    for value in args.risk_note:
        append_unique(state, "observe.risks", value)
    for value in args.followup:
        append_unique(state, "observe.followups", value)

    if case_log_needed(state, args.case_log):
        case_log = write_case_log(root, state)
        state["distill"]["case_log"] = str(case_log)
        print(f"case_log: {case_log}")

    save_state(root, state)
    repeats = repeated_lessons(root)
    if repeats:
        append_feedback(root, state, "Repeated lessons detected:\n" + markdown_list(repeats))

    if args.skill_feedback:
        feedback = append_feedback(root, state, args.skill_feedback)
        print(f"skill_feedback: {feedback}")

    path = save_state(root, state)
    append_event(root, run_id, "finish", {"status": args.status, "state": str(path)})
    print(f"finished: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
