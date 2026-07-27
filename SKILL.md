---
name: solo-company-harness
description: Use when building, modifying, debugging, reviewing, or shipping software as a one-person company with AI coding. It provides progressive project delivery control with context memory, delivery contracts, evidence gates, release control, and reusable learning.
---

# Solo Company Harness

Use this Skill as a lightweight delivery control layer for AI Coding. It helps an
owner keep the goal, boundary, evidence, and lessons visible without pretending that
the Skill itself can operate every external system.

## First Rule: Scale the Weight

Choose the smallest mode that is safe for the task:

- `explore`: a local prototype, spike, one-off script, or reversible experiment.
  Keep the run compact. Do not present the result as production-ready.
- `delivery`: normal user-facing work. Use a full delivery contract before production
  edits and prove at least the required local evidence.
- `high-assurance`: auth, payments, migrations, production data, deployment, public
  release, or hard-to-reverse changes. Require stronger evidence and recovery.

`start_run.py --mode auto` maps low, medium, and high risk to these modes. Never use a
lower mode to bypass a higher-risk requirement.

Load only the reference for the selected path:

- [operating-modes.md](references/operating-modes.md) for routing and ceremony.
- [delivery-contract.md](references/delivery-contract.md) for delivery and high-risk
  contract rules.
- [evidence-levels.md](references/evidence-levels.md) for verification receipts.
- [platform-adapters.md](references/platform-adapters.md) when changing host support.
- `approved-experience.md` only when the task resembles a promoted cross-project
  lesson.

## Module Readiness

When a module name is available, resolve it before implementation:

```bash
python <skill-dir>/scripts/resolve_mode.py <project-root> --module <module>
```

Missing, draft, stale, or incomplete module documents mean discovery is allowed but
production code, schema, public API, and release configuration are blocked until the
owner approves the module documents.

## Default Loop

Use this eight-state loop, but keep the output proportional to the selected mode:

```text
Intent -> Context -> Contract -> Execute -> Verify -> Release -> Observe -> Distill
```

1. **Intent**: capture goal, user value, success criteria, non-goals, and risk.
2. **Context**: read only relevant project files, SSOT, tests, and prior decisions.
3. **Contract**: for delivery/high-assurance, agree on approach, acceptance evidence,
   boundaries, anti-gaming rules, alternatives, and recovery.
4. **Execute**: make the smallest reversible change and record important decisions.
5. **Verify**: run relevant checks and record the evidence level actually achieved.
6. **Release**: choose local-only, dogfood, seed-user, beta, or full.
7. **Observe**: record surprises, residual risks, and follow-ups.
8. **Distill**: save a case log, playbook, or approved cross-project lesson only when
   the experience is worth preserving.

Do not create process for its own sake. A typo fix does not need a company review.
An external integration does.

## Project Memory

For substantial work, initialize or read the project SSOT:

```bash
python <skill-dir>/scripts/init_ssot.py <project-root>
python <skill-dir>/scripts/init_agents.py <project-root> --skill-path <skill-dir>
```

Canonical project memory:

```text
docs/company.md
docs/product.md
docs/customers.md
docs/system.md
docs/playbooks/
docs/case-log/
```

Keep project facts in the project, not in the global Skill. Leave uncertain facts as
`TBD` until evidence exists.

## Run Commands

Start a run:

```bash
python <skill-dir>/scripts/start_run.py <project-root> \
  --title "<title>" --goal "<goal>" --mode auto
```

For `explore`, work locally and keep the compact state. For `delivery` and
`high-assurance`, complete and approve the contract before production edits:

```bash
python <skill-dir>/scripts/contract.py update <project-root> --why "<why>" --approach "<how>"
python <skill-dir>/scripts/contract.py validate <project-root>
python <skill-dir>/scripts/contract.py approve <project-root> --approved-by "<owner>"
```

Record work and run checks:

```bash
python <skill-dir>/scripts/update_run.py <project-root> --changed-file <path> --decision "<decision>"
python <skill-dir>/scripts/detect_tests.py <project-root> --write-run
python <skill-dir>/scripts/run_checks.py <project-root> --auto
python <skill-dir>/scripts/record_evidence.py <project-root> --level 3 --source real-path --summary "<receipt>"
```

Finish only when the contract and required evidence gate pass:

```bash
python <skill-dir>/scripts/finish_run.py <project-root> --lesson "<lesson>"
```

## Guardrails

Before execution, compare the request with the approved scope, security boundaries,
data-integrity rules, and release gates:

- **Hard**: security, privacy, secrets, immutable source data, provenance, compliance,
  and truthful verification. Block and offer a compliant alternative.
- **Negotiable**: scope, TTL, provider, cost, or quality trade-offs. Warn first and
  record owner approval when the contract changes.
- **Advisory**: efficiency or quality suggestions. Inform the owner and continue.

For every delivery criterion, ask:

> If an agent optimized only for the metric, how could it fake completion?

Write each shortcut into the contract and attach a check that rules it out. Hardcoded
output, fixture-only success, fake Provider responses, disabled auth, manual database
edits, hidden errors, and a page that only opens are not proof of a real outcome.

Do not silently change an approved contract. If new evidence changes the goal or
boundary, return to Contract, record the reason, and obtain approval again.

## Evidence Boundary

`run_checks.py` can run local commands. `record_evidence.py` can record a receipt for
integration, real-path, or dogfood verification. Neither script can independently
prove a third-party payment, callback, async job, production configuration, or user
outcome. Those require a project-specific verification recipe, sandbox, credentials,
and artifacts. See [evidence-levels.md](references/evidence-levels.md).

## Risk and Learning

Use `detect_risk.py` as a signal, not as an oracle. Combine its result with file scope,
data flow, permissions, reversibility, and project-specific rules.

Use this promotion path:

```text
single event -> case log -> repeated issue -> project playbook
-> user-approved cross-project lesson -> Skill proposal
```

Never silently mutate this Skill from one run.

## Final Report

Keep the final report short and state:

- changed files and user-visible result;
- checks run and evidence level achieved;
- release mode;
- remaining risks or blocked paths;
- durable lesson, if any.

## Host Boundary

The core loop, run state, contract, evidence, and case-log formats are intended to be
portable. Installation, invocation, `agents/openai.yaml`, and current examples are
Codex adapters. Do not claim another Agent host is supported until its adapter passes
the repository tests and smoke flow.
