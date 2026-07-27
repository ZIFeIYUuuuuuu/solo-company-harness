#!/usr/bin/env python3
"""Create, challenge, validate, and approve a run delivery contract."""

from __future__ import annotations

import argparse
import re
from typing import Any

from harness_common import (
    append_event,
    delivery_contract_path,
    latest_run_id,
    load_state,
    now_iso,
    project_root,
    save_state,
    write_delivery_contract,
)


LIST_FIELDS = (
    "boundaries",
    "anti_cheat",
    "infeasible",
    "alternatives",
    "divergence",
    "verification",
)
PLACEHOLDER_RE = re.compile(r"\b(?:tbd|todo|todo:|待填写|待补充|未决定|unknown)\b", re.IGNORECASE)


def ensure_contract(state: dict[str, Any]) -> dict[str, Any]:
    contract = state.setdefault("delivery_contract", {})
    defaults: dict[str, Any] = {
        "status": "draft",
        "approved_by": "",
        "approved_at": "",
        "why": "",
        "approach": "",
        "acceptance": [],
        "boundaries": [],
        "anti_cheat": [],
        "infeasible": [],
        "alternatives": [],
        "divergence": [],
        "verification": [],
        "rollback": "",
    }
    for key, value in defaults.items():
        contract.setdefault(key, value)
    return contract


def parse_acceptance(value: str) -> dict[str, str]:
    parts = [part.strip() for part in value.split("||", 2)]
    if len(parts) != 3 or not all(parts):
        raise SystemExit(
            "--acceptance format: criterion || evidence || prohibited shortcut"
        )
    return {"criterion": parts[0], "evidence": parts[1], "prohibited": parts[2]}


def contains_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return bool(PLACEHOLDER_RE.search(value))
    if isinstance(value, dict):
        return any(contains_placeholder(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_placeholder(item) for item in value)
    return False


def validate_contract(state: dict[str, Any], require_approval: bool = False) -> list[str]:
    contract = ensure_contract(state)
    errors: list[str] = []

    for field in ("why", "approach", "rollback"):
        if not str(contract.get(field, "")).strip():
            errors.append(f"missing contract.{field}")

    acceptance = contract.get("acceptance", [])
    if not acceptance:
        errors.append("missing contract.acceptance")
    else:
        for index, item in enumerate(acceptance, start=1):
            if not isinstance(item, dict):
                errors.append(f"acceptance[{index}] must include criterion, evidence, and prohibited shortcut")
                continue
            for field in ("criterion", "evidence", "prohibited"):
                if not str(item.get(field, "")).strip():
                    errors.append(f"acceptance[{index}] missing {field}")

    for field in LIST_FIELDS:
        if not contract.get(field):
            errors.append(f"missing contract.{field}; explicitly record none identified when applicable")

    if contains_placeholder(contract):
        errors.append("contract contains a placeholder such as TBD or TODO")

    if require_approval and contract.get("status") != "approved":
        errors.append(f"contract status is {contract.get('status', 'missing')}, expected approved")
    return errors


def print_errors(errors: list[str]) -> None:
    if errors:
        print("contract: blocked")
        for error in errors:
            print(f"- {error}")
    else:
        print("contract: valid")


def load_run(root: Any, run_id: str) -> dict[str, Any]:
    state = load_state(root, run_id)
    ensure_contract(state)
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage a run delivery contract.")
    parser.add_argument("action", choices=["init", "update", "validate", "check", "approve"])
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--run-id", default="", help="Run id; defaults to latest.")
    parser.add_argument("--why", default="", help="Why this work matters.")
    parser.add_argument("--approach", default="", help="Chosen implementation approach.")
    parser.add_argument(
        "--acceptance",
        action="append",
        default=[],
        help="criterion || evidence || prohibited shortcut; repeatable.",
    )
    for field in LIST_FIELDS:
        option = f"--{field.replace('_', '-')}"
        aliases = [option]
        if field == "boundaries":
            aliases.append("--boundary")
        parser.add_argument(*aliases, dest=field, action="append", default=[], help=f"Contract {field}; repeatable.")
    parser.add_argument("--rollback", default="", help="Rollback or recovery boundary.")
    parser.add_argument("--approved-by", default="", help="Owner approving the contract.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    run_id = args.run_id or latest_run_id(root)
    state = load_run(root, run_id)
    contract = state["delivery_contract"]

    if args.action == "init":
        path = write_delivery_contract(root, state)
        save_state(root, state)
        print(f"contract: {path}")
        return 0

    if args.action == "update":
        changed = False
        if args.why:
            contract["why"] = args.why
            changed = True
        if args.approach:
            contract["approach"] = args.approach
            changed = True
        if args.rollback:
            contract["rollback"] = args.rollback
            changed = True
        for field in LIST_FIELDS:
            values = getattr(args, field)
            if values:
                contract[field].extend(value for value in values if value not in contract[field])
                changed = True
        if args.acceptance:
            for value in args.acceptance:
                item = parse_acceptance(value)
                if item not in contract["acceptance"]:
                    contract["acceptance"].append(item)
                    changed = True
        if not changed:
            raise SystemExit("update requires at least one contract field")
        if contract.get("status") == "approved":
            contract["status"] = "draft"
            contract["approved_by"] = ""
            contract["approved_at"] = ""
            state["status"] = "contract_pending"
            print("contract: approval invalidated by substantive update")
        write_delivery_contract(root, state)
        path = save_state(root, state)
        append_event(root, run_id, "contract_update", {"state": str(path)})
        print(f"contract: {delivery_contract_path(root, run_id)}")
        return 0

    errors = validate_contract(state, require_approval=args.action == "check")
    if args.action == "validate":
        print_errors(errors)
        return 1 if errors else 0

    if args.action == "check":
        print_errors(errors)
        return 1 if errors else 0

    if not args.approved_by.strip():
        raise SystemExit("approve requires --approved-by")
    if errors:
        print_errors(errors)
        return 1
    contract["status"] = "approved"
    contract["approved_by"] = args.approved_by.strip()
    contract["approved_at"] = now_iso()
    state["status"] = "in_progress"
    write_delivery_contract(root, state)
    path = save_state(root, state)
    append_event(
        root,
        run_id,
        "contract_approved",
        {"approved_by": contract["approved_by"], "state": str(path)},
    )
    print(f"contract: approved by {contract['approved_by']}")
    print(f"contract: {delivery_contract_path(root, run_id)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
