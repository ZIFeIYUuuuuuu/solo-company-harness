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
    return json.loads(path.read_text(encoding="utf-8"))


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
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "run_id": run_id,
        "title": title,
        "project_root": str(root),
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "status": "in_progress",
        "risk": risk,
        "intent": {
            "goal": goal,
            "non_goal": non_goal or [],
            "user_value": "",
            "success_criteria": success_criteria or [],
            "expected_output": expected_output,
        },
        "context": {"files_read": [], "constraints": [], "ssot_used": []},
        "contract": {
            "planned_changes": [],
            "boundaries": [],
            "verification_plan": [],
            "rollback_plan": "",
            "known_risks": [],
        },
        "execution": {"changed_files": [], "decisions": []},
        "verification": {"commands": [], "results": []},
        "release": {"mode": "local-only", "rollback_point": "", "watch": []},
        "observe": {"surprises": [], "risks": [], "lessons": [], "followups": []},
        "distill": {"case_log": "", "playbooks_updated": [], "skill_update_proposed": False},
    }


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
