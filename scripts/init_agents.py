#!/usr/bin/env python3
"""Create or refresh a project AGENTS.md harness block."""

from __future__ import annotations

import argparse
from pathlib import Path

from harness_common import now_iso, project_root


START = "<!-- SOLO-COMPANY-HARNESS:START -->"
END = "<!-- SOLO-COMPANY-HARNESS:END -->"


def managed_block(root: Path, skill_path: str) -> str:
    skill_line = skill_path or "TBD"
    return f"""{START}
# Solo Company Harness

This project uses the solo-company-harness workflow for AI coding.

Generated/updated: {now_iso()}

## Operating Contract

- Treat the user as the owner, operator, and final decision maker.
- Use the project SSOT before substantial work.
- Keep changes small, reversible, and verified.
- Record non-trivial work in `.harness/runs/`.
- Create case logs for medium/high-risk work, failed verification, surprises, or reusable lessons.
- Promote repeated lessons into `docs/playbooks/`.
- Do not silently update the harness skill from one-off feedback; write proposals first.

## Project SSOT

Read and update these files as living project memory:

- `docs/company.md` - company identity, business model, operating constraints.
- `docs/product.md` - product promise, users, scope, workflows, roadmap.
- `docs/customers.md` - segments, pains, feedback, objections, success signals.
- `docs/system.md` - architecture, stack, commands, data model, integrations, deployment.
- `docs/playbooks/` - repeated workflows and fixes.
- `docs/case-log/` - significant execution records.

Do not rewrite SSOT files from scratch during normal feature work. Update only changed sections and leave unknowns as `TBD`.

## Harness Commands

Skill path:

```text
{skill_line}
```

Initialize SSOT:

```bash
python <skill-dir>/scripts/init_ssot.py <project-root>
```

Start a run:

```bash
python <skill-dir>/scripts/start_run.py <project-root> --title "<title>" --goal "<goal>"
```

Before production edits, complete and approve the delivery contract created for the run:

```bash
python <skill-dir>/scripts/contract.py update <project-root> --why "<why>" --approach "<how>"
python <skill-dir>/scripts/contract.py validate <project-root>
python <skill-dir>/scripts/contract.py approve <project-root> --approved-by "<owner>"
```

The contract must include observable acceptance evidence, boundaries, prohibited
shortcuts, infeasible paths, alternatives, divergent options, verification, and
rollback or recovery. Do not treat fixtures, mocks, hardcoded output, manual data
edits, or a passing build as proof when the real user path is required.

Update a run:

```bash
python <skill-dir>/scripts/update_run.py <project-root> --changed-file <path> --decision "<decision>"
```

Detect tests and run checks:

```bash
python <skill-dir>/scripts/detect_tests.py <project-root> --write-run
python <skill-dir>/scripts/run_checks.py <project-root> --auto
```

Finish a run:

```bash
python <skill-dir>/scripts/finish_run.py <project-root> --lesson "<lesson>"
```

Refresh this block:

```bash
python <skill-dir>/scripts/init_agents.py <project-root> --skill-path <skill-dir>
```

## Risk Rules

- `low`: local, reversible, well-understood changes.
- `medium`: user-facing behavior, shared code, APIs, data shape, integrations, project structure, or deployment config.
- `high`: auth, payments, security, production data, migrations, irreversible operations, broad architecture, or public release.

For every run, require an approved delivery contract before production edits. For
medium/high risk, require a clear verification plan, rollback or recovery story, and
residual-risk report. If the contract changes, re-approval is required.
{END}
"""


def upsert_agents(root: Path, skill_path: str) -> Path:
    path = root / "AGENTS.md"
    block = managed_block(root, skill_path)

    if path.exists():
        content = path.read_text(encoding="utf-8")
        if START in content and END in content:
            before = content.split(START, 1)[0].rstrip()
            after = content.split(END, 1)[1].lstrip()
            new_content = f"{before}\n\n{block}\n"
            if after:
                new_content += f"\n{after}"
        else:
            new_content = content.rstrip() + "\n\n" + block + "\n"
    else:
        new_content = block + "\n"

    path.write_text(new_content, encoding="utf-8", newline="\n")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or refresh project AGENTS.md for solo-company harness.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root.")
    parser.add_argument("--skill-path", default="", help="Path to solo-company-harness skill.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    path = upsert_agents(root, args.skill_path)
    print(f"agents: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
