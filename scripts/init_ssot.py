#!/usr/bin/env python3
"""Initialize a lightweight SSOT for solo-company AI coding projects."""

from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATES = {
    "docs/company.md": """# Company SSOT

## Identity
- Name: TBD
- One-line description: TBD
- Owner: TBD

## Mission
TBD

## Business Model
- Customers: TBD
- Offer: TBD
- Pricing: TBD
- Revenue model: TBD

## Operating Principles
- TBD

## Constraints
- Time:
- Budget:
- Legal/compliance:
- Technical:

## Current Priorities
- TBD
""",
    "docs/product.md": """# Product SSOT

## Product
- Name: TBD
- Category: TBD
- Promise: TBD

## Target Users
- Primary user: TBD
- Buyer, if different: TBD
- Jobs to be done: TBD

## Scope
### In Scope
- TBD

### Out of Scope
- TBD

## Core Workflows
- TBD

## Roadmap
### Now
- TBD

### Next
- TBD

### Later
- TBD

## Success Metrics
- TBD
""",
    "docs/customers.md": """# Customer SSOT

## Segments
- TBD

## Pain Points
- TBD

## Feedback
| Date | Source | Signal | Decision |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

## Objections
- TBD

## Success Signals
- TBD
""",
    "docs/system.md": """# System SSOT

## Architecture
TBD

## Tech Stack
- Frontend: TBD
- Backend: TBD
- Data: TBD
- Infrastructure: TBD

## Important Commands
```bash
# install
TBD

# dev
TBD

# test
TBD

# build
TBD
```

## Data Model
TBD

## Integrations
- TBD

## Deployment
TBD

## Guardrails
- Auth/security: TBD
- Data safety: TBD
- Cost/latency: TBD
- Rollback: TBD
""",
    "docs/playbooks/README.md": """# Playbooks

Reusable workflows live here.

Create a playbook when the same pattern appears more than once.

Format:

```md
# Playbook: <topic>

## When To Use
<trigger>

## Steps
1. <step>

## Verification
<checks>

## Failure Modes
<known risks>
```
""",
    "docs/case-log/README.md": """# Case Logs

Significant one-off execution records live here.

Create a case log when a task teaches something reusable or carries meaningful risk.

Filename:

```text
YYYY-MM-DD-short-title.md
```

Format:

```md
# Case Log: <title>

## Intent
<goal and success criteria>

## Context
<important constraints and files>

## Changes
<what changed>

## Verification
<checks run and results>

## Surprises
<unexpected issues>

## Reusable Lessons
<what should be reused>

## Follow-ups
<optional next actions>
```
""",
}


def init_ssot(root: Path, force: bool, dry_run: bool) -> int:
    created = 0
    skipped = 0
    for relative_path, content in TEMPLATES.items():
        path = root / relative_path
        if path.exists() and not force:
            print(f"skip existing: {path}")
            skipped += 1
            continue

        action = "overwrite" if path.exists() else "create"
        print(f"{action}: {path}")
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
        created += 1

    print(f"done: {created} created/updated, {skipped} skipped")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize solo-company SSOT markdown files.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root to initialize.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing SSOT files.")
    parser.add_argument("--dry-run", action="store_true", help="Show planned writes without changing files.")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    return init_ssot(root, force=args.force, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
