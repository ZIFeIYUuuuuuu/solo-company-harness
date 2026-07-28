#!/usr/bin/env python3
"""Shared helpers for the solo-company harness scripts."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HIGH_RISK_KEYWORDS = {
    "auth",
    "authentication",
    "authorization",
    "login",
    "logout",
    "password",
    "token",
    "secret",
    "permission",
    "role",
    "payment",
    "payments",
    "billing",
    "invoice",
    "subscription",
    "security",
    "encrypt",
    "decrypt",
    "migration",
    "migrate",
    "delete",
    "drop",
    "truncate",
    "production",
    "prod",
    "deploy",
    "database",
    "schema",
    "backup",
    "restore",
}

MEDIUM_RISK_KEYWORDS = {
    "api",
    "endpoint",
    "integration",
    "webhook",
    "model",
    "prompt",
    "skill",
    "mcp",
    "data",
    "cache",
    "queue",
    "config",
    "settings",
    "route",
    "ui",
    "workflow",
    "refactor",
}

HIGH_RISK_PATH_PARTS = {
    ".env",
    "auth",
    "billing",
    "payment",
    "payments",
    "security",
    "secrets",
    "migrations",
    "migration",
    "infra",
    "deploy",
    "terraform",
    "schema",
}

MEDIUM_RISK_PATH_PARTS = {
    "api",
    "routes",
    "components",
    "models",
    "stores",
    "db",
    "database",
    "config",
    "settings",
    "workflows",
}

OPERATING_MODE_ORDER = {
    "explore": 0,
    "delivery": 1,
    "high-assurance": 2,
}

EVIDENCE_LEVELS = {
    0: "static",
    1: "local",
    2: "integration",
    3: "real-path",
    4: "dogfood",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def slugify(value: str, fallback: str = "run") -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug[:80] or fallback


def project_root(path: str | Path | None = None) -> Path:
    return Path(path or ".").expanduser().resolve()


def harness_dir(root: Path) -> Path:
    return root / ".harness"


def runs_dir(root: Path) -> Path:
    return harness_dir(root) / "runs"


def feedback_dir(root: Path) -> Path:
    return harness_dir(root) / "feedback"


def state_path(root: Path, run_id: str) -> Path:
    return runs_dir(root) / run_id / "state.json"


def events_path(root: Path, run_id: str) -> Path:
    return runs_dir(root) / run_id / "events.jsonl"


def delivery_contract_path(root: Path, run_id: str) -> Path:
    return runs_dir(root) / run_id / "delivery-contract.md"


def verification_log_path(root: Path, run_id: str) -> Path:
    return runs_dir(root) / run_id / "verification.log"


def ensure_harness(root: Path) -> None:
    runs_dir(root).mkdir(parents=True, exist_ok=True)
    feedback_dir(root).mkdir(parents=True, exist_ok=True)


def latest_run_id(root: Path) -> str:
    candidates = [p for p in runs_dir(root).glob("*") if (p / "state.json").exists()]
    if not candidates:
        raise SystemExit("No harness runs found. Start one with start_run.py first.")
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0].name


def load_state(root: Path, run_id: str | None = None) -> dict[str, Any]:
    run_id = run_id or latest_run_id(root)
    path = state_path(root, run_id)
    if not path.exists():
        raise SystemExit(f"Run state not found: {path}")
    return migrate_state(json.loads(path.read_text(encoding="utf-8")))


def migrate_state(state: dict[str, Any]) -> dict[str, Any]:
    version = int(state.get("schema_version", 1))
    if version < 2:
        state["schema_version"] = 2
        state.setdefault("compatibility", {})["legacy_state"] = True
        state["compatibility"]["migrated_from"] = version
    return state


def save_state(root: Path, state: dict[str, Any]) -> Path:
    state["updated_at"] = now_iso()
    path = state_path(root, state["run_id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def append_event(root: Path, run_id: str, event_type: str, payload: dict[str, Any]) -> None:
    path = events_path(root, run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    event = {"at": now_iso(), "type": event_type, "payload": payload}
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def ensure_list(state: dict[str, Any], dotted_path: str) -> list[Any]:
    target: Any = state
    parts = dotted_path.split(".")
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    return target.setdefault(parts[-1], [])


def append_unique(state: dict[str, Any], dotted_path: str, value: Any) -> None:
    items = ensure_list(state, dotted_path)
    if value not in items:
        items.append(value)


def set_value(state: dict[str, Any], dotted_path: str, value: Any) -> None:
    target: Any = state
    parts = dotted_path.split(".")
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = value


def detect_risk(task: str, changed_files: list[str] | None = None) -> dict[str, Any]:
    text = task.lower()
    files = [f.replace("\\", "/").lower() for f in changed_files or []]
    reasons: list[str] = []
    score = 0

    for word in sorted(HIGH_RISK_KEYWORDS):
        if re.search(rf"\b{re.escape(word)}\b", text):
            score = max(score, 3)
            reasons.append(f"high keyword: {word}")

    for word in sorted(MEDIUM_RISK_KEYWORDS):
        if re.search(rf"\b{re.escape(word)}\b", text):
            score = max(score, 2)
            reasons.append(f"medium keyword: {word}")

    for file_path in files:
        parts = set(Path(file_path).parts)
        if any(part in file_path for part in HIGH_RISK_PATH_PARTS) or parts & HIGH_RISK_PATH_PARTS:
            score = max(score, 3)
            reasons.append(f"high-risk path: {file_path}")
        elif any(part in file_path for part in MEDIUM_RISK_PATH_PARTS) or parts & MEDIUM_RISK_PATH_PARTS:
            score = max(score, 2)
            reasons.append(f"medium-risk path: {file_path}")

    if score >= 3:
        level = "high"
    elif score == 2:
        level = "medium"
    else:
        level = "low"
        if not reasons:
            reasons.append("no high or medium risk signals found")

    return {"level": level, "source": "auto", "reasons": reasons}


def resolve_operating_mode(risk_level: str, requested: str = "auto") -> str:
    required = {
        "low": "explore",
        "medium": "delivery",
        "high": "high-assurance",
    }.get(risk_level, "delivery")
    mode = required if requested == "auto" else requested
    if mode not in OPERATING_MODE_ORDER:
        raise SystemExit(f"Unknown operating mode: {mode}")
    if OPERATING_MODE_ORDER[mode] < OPERATING_MODE_ORDER[required]:
        raise SystemExit(
            f"{risk_level} risk requires {required} mode or stricter; received {mode}"
        )
    return mode


def required_evidence_level(operating_mode: str) -> int:
    return {
        "explore": 0,
        "delivery": 1,
        "high-assurance": 2,
    }.get(operating_mode, 1)


def evidence_label(level: int) -> str:
    return EVIDENCE_LEVELS.get(level, f"unknown-{level}")


def update_evidence_level(state: dict[str, Any], level: int) -> None:
    verification = state.setdefault("verification", {})
    current = int(verification.get("evidence_level_achieved", 0))
    verification["evidence_level_achieved"] = max(current, level)


def load_package_json(root: Path) -> dict[str, Any] | None:
    path = root / "package.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def node_runner(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    return "npm"


def node_command(root: Path, script: str) -> str:
    runner = node_runner(root)
    if runner == "npm":
        return "npm test" if script == "test" else f"npm run {script}"
    return f"{runner} {script}"


def detect_test_commands(root: Path, risk: str = "medium") -> list[dict[str, str]]:
    commands: list[dict[str, str]] = []
    package = load_package_json(root)
    if package:
        scripts = package.get("scripts", {})
        for script in ("lint", "typecheck", "test", "build"):
            if script in scripts:
                commands.append(
                    {
                        "command": node_command(root, script),
                        "category": script,
                        "reason": f"package.json defines {script}",
                    }
                )

    if (root / "pytest.ini").exists() or (root / "pyproject.toml").exists() or (root / "setup.cfg").exists():
        commands.append({"command": "python -m pytest", "category": "test", "reason": "Python test config found"})

    if (root / "go.mod").exists():
        commands.append({"command": "go test ./...", "category": "test", "reason": "go.mod found"})

    if (root / "Cargo.toml").exists():
        commands.append({"command": "cargo test", "category": "test", "reason": "Cargo.toml found"})

    if (root / "pom.xml").exists():
        commands.append({"command": "mvn test", "category": "test", "reason": "pom.xml found"})

    if (root / "build.gradle").exists() or (root / "build.gradle.kts").exists():
        commands.append({"command": "gradle test", "category": "test", "reason": "Gradle build file found"})

    if list(root.glob("*.sln")) or list(root.glob("*.csproj")):
        commands.append({"command": "dotnet test", "category": "test", "reason": ".NET project file found"})

    seen: set[str] = set()
    unique = []
    for item in commands:
        if item["command"] not in seen:
            unique.append(item)
            seen.add(item["command"])

    if risk == "low":
        preferred = [c for c in unique if c["category"] in {"test", "typecheck", "lint"}]
        return preferred[:2] or unique[:1]
    if risk == "medium":
        return [c for c in unique if c["category"] in {"lint", "typecheck", "test", "build"}]
    return unique


def make_initial_state(
    root: Path,
    run_id: str,
    title: str,
    goal: str,
    risk: dict[str, Any],
    success_criteria: list[str] | None = None,
    non_goal: list[str] | None = None,
    expected_output: str = "",
    operating_mode: str = "delivery",
) -> dict[str, Any]:
    evidence_required = required_evidence_level(operating_mode)
    compact_acceptance = success_criteria or ["Prototype can be exercised locally"]
    compact_contract = {
        "status": "compact-approved" if operating_mode == "explore" else "draft",
        "mode": operating_mode,
        "approved_by": "system: explore mode",
        "approved_at": now_iso() if operating_mode == "explore" else "",
        "why": goal if operating_mode == "explore" else "",
        "approach": "Use the smallest reversible path and keep the result explicitly exploratory"
        if operating_mode == "explore"
        else "",
        "acceptance": [
            {
                "criterion": criterion,
                "evidence": "Local smoke check or direct manual exercise",
                "prohibited": "Do not present a prototype or fixture as production-ready",
            }
            for criterion in compact_acceptance
        ]
        if operating_mode == "explore"
        else [],
        "boundaries": non_goal or ["No production release or irreversible data change"]
        if operating_mode == "explore"
        else [],
        "anti_cheat": ["Do not claim production readiness from an exploratory result"]
        if operating_mode == "explore"
        else [],
        "infeasible": ["Production readiness is outside explore mode"]
        if operating_mode == "explore"
        else [],
        "alternatives": ["A full delivery contract is available by starting in delivery mode"]
        if operating_mode == "explore"
        else [],
        "divergence": ["Explore the smallest useful path before committing to architecture"]
        if operating_mode == "explore"
        else [],
        "verification": ["Run a focused local smoke check"] if operating_mode == "explore" else [],
        "rollback": "Discard local changes; do not release exploratory output"
        if operating_mode == "explore"
        else "",
    }
    return {
        "schema_version": 2,
        "run_id": run_id,
        "title": title,
        "project_root": str(root),
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "status": "in_progress" if operating_mode == "explore" else "contract_pending",
        "operating_mode": operating_mode,
        "risk": risk,
        "intent": {
            "goal": goal,
            "non_goal": non_goal or [],
            "user_value": "",
            "success_criteria": success_criteria or [],
            "expected_output": expected_output,
        },
        "context": {"files_read": [], "constraints": [], "ssot_used": []},
        "gates": {
            "first_principles": [],
            "assumptions": [],
            "adversarial_findings": [],
            "edge_cases": [],
            "rejected_options": [],
        },
        "delivery_contract": compact_contract,
        "contract": {
            "planned_changes": [],
            "boundaries": [],
            "verification_plan": [],
            "rollback_plan": "",
            "known_risks": [],
        },
        "execution": {"changed_files": [], "decisions": []},
        "verification": {
            "commands": [],
            "results": [],
            "evidence": [],
            "required_evidence_level": evidence_required,
            "evidence_level_achieved": 0,
        },
        "release": {"mode": "local-only", "rollback_point": "", "watch": []},
        "observe": {"surprises": [], "risks": [], "lessons": [], "followups": []},
        "distill": {"case_log": "", "playbooks_updated": [], "skill_update_proposed": False},
    }


def markdown_contract(state: dict[str, Any]) -> str:
    contract = state.get("delivery_contract", {})
    status = contract.get("status", "draft")
    approved_by = contract.get("approved_by") or "TBD"
    approved_at = contract.get("approved_at") or "TBD"

    acceptance = contract.get("acceptance", [])
    if acceptance:
        acceptance_text = []
        for index, item in enumerate(acceptance, start=1):
            if isinstance(item, dict):
                acceptance_text.append(
                    f"{index}. **标准**：{item.get('criterion', '')}\n"
                    f"   **证据**：{item.get('evidence', '')}\n"
                    f"   **不算通过**：{item.get('prohibited', '') or 'TBD'}"
                )
            else:
                acceptance_text.append(f"{index}. {item}")
        acceptance_text = "\n".join(acceptance_text)
    else:
        acceptance_text = "- TBD"

    def section(items: Any) -> str:
        return markdown_list(items if isinstance(items, list) else [])

    return f"""# Delivery Contract: {state.get('title', state.get('run_id', 'run'))}

Status: {status}
Run: {state.get('run_id', '')}
Owner approval: {approved_by}
Approved at: {approved_at}

## Why
{contract.get('why') or 'TBD'}

## Approach
{contract.get('approach') or 'TBD'}

## Acceptance Criteria
{acceptance_text}

## Boundaries and Non-goals
{section(contract.get('boundaries'))}

## Anti-gaming Rules
Every shortcut that reaches the metric without delivering the user outcome is invalid.
{section(contract.get('anti_cheat'))}

## Infeasible or Blocked Paths
{section(contract.get('infeasible'))}

## Alternatives and Trade-offs
{section(contract.get('alternatives'))}

## Divergent Options Considered
{section(contract.get('divergence'))}

## Verification Plan
{section(contract.get('verification'))}

## Rollback or Recovery
{contract.get('rollback') or 'TBD'}
"""


def write_delivery_contract(root: Path, state: dict[str, Any]) -> Path:
    path = delivery_contract_path(root, state["run_id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown_contract(state), encoding="utf-8", newline="\n")
    return path


def markdown_list(items: list[Any]) -> str:
    if not items:
        return "- None"
    lines = []
    for item in items:
        if isinstance(item, dict):
            text = item.get("summary") or item.get("command") or item.get("message") or json.dumps(item, ensure_ascii=False)
        else:
            text = str(item)
        lines.append(f"- {text}")
    return "\n".join(lines)


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for index in range(2, 1000):
        candidate = path.with_name(f"{stem}-{index}{suffix}")
        if not candidate.exists():
            return candidate
    raise SystemExit(f"Could not create unique path near {path}")
