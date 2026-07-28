#!/usr/bin/env python3
"""Install the portable skill payload into a supported Agent host."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from host_adapters import HOSTS, SKILL_NAME, default_destination, normalize_host


PAYLOAD = (
    "SKILL.md",
    "PLATFORM.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "agents",
    "references",
    "scripts",
)


def _ignore(_directory: str, names: list[str]) -> set[str]:
    ignored = {".git", ".github", ".pytest_cache", "__pycache__", "tests"}
    return {name for name in names if name in ignored or name.endswith(".pyc")}


def _is_inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def install_skill(source: Path, destination: Path, update: bool = False) -> Path:
    source = source.expanduser().resolve()
    destination = destination.expanduser().resolve()
    if source == destination or _is_inside(destination, source):
        raise ValueError("destination must not be the source directory or one of its children")
    if not (source / "SKILL.md").is_file():
        raise FileNotFoundError(f"SKILL.md not found in source directory: {source}")
    if destination.exists() and not update:
        raise FileExistsError(f"destination already exists; use --update to refresh it: {destination}")
    if destination.exists() and not destination.is_dir():
        raise NotADirectoryError(f"destination is not a directory: {destination}")

    destination.mkdir(parents=True, exist_ok=True)
    for relative in PAYLOAD:
        source_item = source / relative
        if not source_item.exists():
            continue
        destination_item = destination / relative
        if source_item.is_dir():
            shutil.copytree(source_item, destination_item, dirs_exist_ok=True, ignore=_ignore)
        else:
            destination_item.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_item, destination_item)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description="Install solo-company-harness for an Agent host.")
    parser.add_argument(
        "--host",
        default="generic",
        help="Host adapter: codex, claude-code, opencode, or generic.",
    )
    parser.add_argument("--source", default=str(Path(__file__).resolve().parents[1]), help="Skill source directory.")
    parser.add_argument("--dest", default="", help="Explicit destination; required for generic hosts.")
    parser.add_argument("--update", action="store_true", help="Refresh an existing destination.")
    args = parser.parse_args()

    try:
        host = normalize_host(args.host)
        destination = Path(args.dest).expanduser() if args.dest else default_destination(host)
        if destination is None:
            parser.error("--dest is required when --host generic is used")
        installed = install_skill(Path(args.source), destination, update=args.update)
    except (FileExistsError, FileNotFoundError, NotADirectoryError, ValueError) as exc:
        parser.error(str(exc))

    print(f"host: {host}")
    print(f"skill: {SKILL_NAME}")
    print(f"installed: {installed}")
    print(f"next: generate project instructions with scripts/init_agents.py --host {host}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
