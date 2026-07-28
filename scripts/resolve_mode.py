#!/usr/bin/env python3
"""Resolve a project's implementation mode from approved module documents."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path


APPROVED = "approved"
REQUIRED_DESIGN_SECTIONS = ("scope", "non-goal", "acceptance")
REQUIRED_STORY_SECTIONS = ("as a", "when", "i want", "so that", "acceptance")
REQUIRED_METADATA = ("owner", "updated")


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve Design-Locked or Discovery-Gated mode.")
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--module", required=True, help="Module slug, for example assembly-planner.")
    parser.add_argument("--json", action="store_true", help="Print a JSON result.")
    parser.add_argument("--stale-after-days", type=int, default=90, help="Days after which an approved document is stale.")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    module = slug(args.module)
    design = first_existing((root / "docs" / "design" / "modules" / f"{module}.md", root / "docs" / "design" / f"{module}.md"))
    story = first_existing((root / "docs" / "user-stories" / f"{module}.md", root / "docs" / "user-stories" / f"{module}.mdx"))

    reasons: list[str] = []
    checks = {
        "design": document_check(design, REQUIRED_DESIGN_SECTIONS, args.stale_after_days),
        "user_story": document_check(story, REQUIRED_STORY_SECTIONS, args.stale_after_days),
    }
    if checks["design"]["status"] != APPROVED:
        reasons.append(f"design {checks['design']['status']}")
    if checks["user_story"]["status"] != APPROVED:
        reasons.append(f"user_story {checks['user_story']['status']}")
    if checks["design"]["missing"]:
        reasons.append("design missing required sections: " + ", ".join(checks["design"]["missing"]))
    if checks["design"]["metadata_missing"]:
        reasons.append("design missing metadata: " + ", ".join(checks["design"]["metadata_missing"]))
    if checks["design"]["stale"]:
        reasons.append("design stale")
    if checks["user_story"]["missing"]:
        reasons.append("user story missing required sections: " + ", ".join(checks["user_story"]["missing"]))
    if checks["user_story"]["metadata_missing"]:
        reasons.append("user story missing metadata: " + ", ".join(checks["user_story"]["metadata_missing"]))
    if checks["user_story"]["stale"]:
        reasons.append("user story stale")

    mode = "design-locked" if not reasons else "discovery-gated"
    result = {"mode": mode, "module": module, "design": checks["design"], "user_story": checks["user_story"], "reasons": reasons or ["approved module contract is complete"]}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"mode={mode}")
        print(f"module={module}")
        for reason in result["reasons"]:
            print(f"reason={reason}")
    return 0


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    if not normalized:
        raise SystemExit("module must contain letters or numbers")
    return normalized


def first_existing(candidates: tuple[Path, ...]) -> Path | None:
    return next((path for path in candidates if path.is_file()), None)


def document_check(path: Path | None, required_sections: tuple[str, ...], stale_after_days: int = 90) -> dict[str, object]:
    if path is None:
        return {
            "path": None,
            "status": "missing",
            "missing": list(required_sections),
            "metadata_missing": list(REQUIRED_METADATA),
            "stale": False,
        }
    text = path.read_text(encoding="utf-8")
    status_match = re.search(r"^\s*status\s*:\s*([^\s#]+)", text, re.IGNORECASE | re.MULTILINE)
    status = status_match.group(1).lower() if status_match else "missing-status"
    lowered = text.lower()
    missing = [section for section in required_sections if section not in lowered]
    metadata_missing = [field for field in REQUIRED_METADATA if not re.search(rf"^\s*{field}\s*:", text, re.IGNORECASE | re.MULTILINE)]
    updated_match = re.search(r"^\s*updated\s*:\s*([^\s#]+)", text, re.IGNORECASE | re.MULTILINE)
    stale = False
    if updated_match:
        updated = parse_date(updated_match.group(1))
        stale = bool(updated and updated < date.today() - timedelta(days=max(stale_after_days, 0)))
    return {
        "path": str(path),
        "status": status,
        "missing": missing,
        "metadata_missing": metadata_missing,
        "stale": stale,
    }


def parse_date(value: str) -> date | None:
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


if __name__ == "__main__":
    raise SystemExit(main())
