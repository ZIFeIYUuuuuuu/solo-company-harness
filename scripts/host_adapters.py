#!/usr/bin/env python3
"""Host-neutral metadata for installing and invoking the skill."""

from __future__ import annotations

from pathlib import Path


SKILL_NAME = "solo-company-harness"

HOSTS = {
    "codex": {
        "skill_parent": Path(".codex") / "skills",
        "instruction_file": "AGENTS.md",
        "invocation": "Use $solo-company-harness for this project.",
    },
    "claude-code": {
        "skill_parent": Path(".claude") / "skills",
        "instruction_file": "CLAUDE.md",
        "invocation": "Use the solo-company-harness skill for this project.",
    },
    "opencode": {
        "skill_parent": Path(".config") / "opencode" / "skills",
        "instruction_file": "AGENTS.md",
        "invocation": "Use the solo-company-harness skill for this project.",
    },
    "generic": {
        "skill_parent": None,
        "instruction_file": "AGENTS.md",
        "invocation": "Use the solo-company-harness skill for this project.",
    },
}

HOST_ALIASES = {
    "claude": "claude-code",
    "claude_code": "claude-code",
    "open-code": "opencode",
    "open_code": "opencode",
}


def normalize_host(host: str) -> str:
    value = host.strip().lower()
    value = HOST_ALIASES.get(value, value)
    if value not in HOSTS:
        supported = ", ".join(HOSTS)
        raise ValueError(f"unknown host {host!r}; choose one of: {supported}")
    return value


def host_config(host: str) -> dict[str, object]:
    return HOSTS[normalize_host(host)]


def default_destination(host: str, home: Path | None = None) -> Path | None:
    config = host_config(host)
    parent = config["skill_parent"]
    if parent is None:
        return None
    return (home or Path.home()) / parent / SKILL_NAME


def instruction_file_for_host(host: str, override: str = "") -> str:
    return override.strip() or str(host_config(host)["instruction_file"])


def invocation_for_host(host: str) -> str:
    return str(host_config(host)["invocation"])
