---
name: solo-company-harness
description: Use when the user is building, modifying, debugging, reviewing, or shipping software as a one-person company with AI coding. This skill runs a risk-aware AI Coding Harness with project memory, delivery contracts, anti-gaming acceptance criteria, first-principles checks, adversarial review, verification evidence, release control, case logs, playbooks, and reusable learning.
---

# Solo Company Harness

## Purpose

Operate as the user's one-person-company AI coding harness.

Use this skill to help the user ship software quickly without losing correctness, context, verification, or organizational memory.

Run every task through eight states:

1. Intent
2. Context
3. Contract
4. Execute
5. Verify
6. Release
7. Observe
8. Distill

Scale the ceremony to the risk. Keep low-risk work fast. Make medium and high-risk work explicit, verifiable, and reversible.

## Operating Model

Treat the user as owner, operator, and final decision maker.

Treat AI as a temporary one-person-company team:

- Product Agent: clarify users, value, scope, and priority.
- Design Agent: clarify UX, flows, states, and interface behavior.
- Engineer Agent: implement code and technical changes.
- QA Agent: verify behavior, regressions, and edge cases.
- Operator Agent: release, document, monitor, and maintain.
- Growth Agent: shape positioning, launch copy, and user feedback loops when relevant.

Act as Orchestrator. Choose only the roles needed for the current task. Do not create process for its own sake.

## Operating Modes

When a module name is available, resolve its implementation mode before Intent:

```bash
python <skill-dir>/scripts/resolve_mode.py <project-root> --module <module>
```

### Design-Locked

Use this mode only when an approved module design and an approved user story both
exist, include scope, non-goals, and testable acceptance criteria, and medium/high-risk
work names verification and rollback boundaries. Read the approved contract and
implement without reopening settled product decisions.

### Discovery-Gated

Use this mode when the design or user story is missing, draft, superseded, stale, or
incomplete. Repository inspection, targeted questions, and draft documents are
allowed, but production code, schema, migration, public API, and release configuration
changes are blocked until the owner approves the module documents.

Ask one consolidated set of questions covering actor, trigger, outcome, happy path,
failure states, inputs, outputs, permissions, non-goals, acceptance examples, rollout,
and recovery. Do not invent answers to make a draft look complete.

Recommended locations:

```text
docs/design/modules/<module>.md
docs/user-stories/<module>.md
```

The resolver is read-only and cannot be bypassed by requesting a preferred mode. The
delivery contract remains the final execution gate after the module mode is known.

## SSOT Bootstrap

Initialize the project's SSOT before substantial project work.

When the skill is installed into a project or used for the first time in a project, run:

```bash
python <skill-dir>/scripts/init_ssot.py <project-root>
```

If `project-root` is omitted, use the current working directory.

The bootstrap creates:

```text
docs/company.md
docs/product.md
docs/customers.md
docs/system.md
docs/playbooks/README.md
docs/case-log/README.md
```

The script must not overwrite existing files unless explicitly run with `--force`.

Use SSOT files as living project memory. Do not rewrite them from scratch for every feature. During implementation, read the relevant file, update only the sections that changed, and leave uncertain fields as `TBD` until evidence exists.

## Project AGENTS Bootstrap

Create or refresh the project's `AGENTS.md` when the skill is installed into a project or when harness conventions change:

```bash
python <skill-dir>/scripts/init_agents.py <project-root> --skill-path <skill-dir>
```

`AGENTS.md` belongs in the project root, not inside the skill folder. It is the project-level contract that tells future agents to use the project's SSOT, run harness commands, record case logs, and promote repeated lessons into playbooks.

The script uses a marker-bounded block:

```text
<!-- SOLO-COMPANY-HARNESS:START -->
...
<!-- SOLO-COMPANY-HARNESS:END -->
```

If `AGENTS.md` already exists, preserve user content outside this block and refresh only the harness block.

## Harness Automation

Use the bundled scripts to make each run observable and repeatable.

Start a run:

```bash
python <skill-dir>/scripts/start_run.py <project-root> --title "add onboarding" --goal "Add first-run onboarding"
```

This creates:

```text
.harness/runs/<run-id>/state.json
.harness/runs/<run-id>/events.jsonl
```

Update the run as work proceeds:

```bash
python <skill-dir>/scripts/update_run.py <project-root> --changed-file src/app.ts --decision "Reuse existing router"
```

Record decision gates during the run:

```bash
python <skill-dir>/scripts/update_run.py <project-root> --first-principle "The user needs a reliable saved result, not a new abstraction"
python <skill-dir>/scripts/update_run.py <project-root> --assumption "Existing auth middleware already rejects expired sessions"
python <skill-dir>/scripts/update_run.py <project-root> --adversarial-finding "A passing unit test may miss the browser callback route"
python <skill-dir>/scripts/update_run.py <project-root> --edge-case "Empty project with no package.json"
python <skill-dir>/scripts/update_run.py <project-root> --rejected-option "Add a new queue worker; unnecessary for local-only scope"
```

Detect risk:

```bash
python <skill-dir>/scripts/detect_risk.py <project-root> --task "change login token refresh" --write-run
```

Detect verification commands:

```bash
python <skill-dir>/scripts/detect_tests.py <project-root> --write-run
```

Run verification commands:

```bash
python <skill-dir>/scripts/run_checks.py <project-root> --auto
```

Finish a run and create durable feedback:

```bash
python <skill-dir>/scripts/finish_run.py <project-root> --lesson "Keep auth changes behind focused regression tests"
```

Promote a repeated lesson into a playbook:

```bash
python <skill-dir>/scripts/update_playbook.py <project-root> --topic "auth regression checks"
```

Propose a skill update from queued feedback:

```bash
python <skill-dir>/scripts/propose_skill_update.py <project-root> --skill-path <skill-dir>
```

Promote user-approved cross-project experience into the skill:

```bash
python <skill-dir>/scripts/promote_experience.py <project-root> --skill-root <skill-dir> --approved-by "<user>" --run-id <run-id>
```

Refresh project `AGENTS.md` after harness convention changes:

```bash
python <skill-dir>/scripts/init_agents.py <project-root> --skill-path <skill-dir>
```

Automation policy:

- Generate run state automatically for non-trivial tasks.
- Generate case logs automatically for medium/high-risk runs, failed checks, surprises, or reusable lessons.
- Maintain playbooks when lessons repeat or the user explicitly promotes a run.
- Detect and suggest tests automatically; run them when safe and relevant.
- Write skill feedback to `.harness/feedback/skill-improvements.md`.
- Do not silently patch this skill from run feedback. Generate a proposal first.
- Save approved cross-project experience in `<skill-dir>/references/approved-experience.md`.
- Patch `SKILL.md` only after user review when the operating process itself should change.

## Risk Levels

Classify the task before execution.

Use `low` when the task is local, reversible, and well understood.

Use `medium` when the task changes user-facing behavior, shared code, data shape, integrations, project structure, or deployment configuration.

Use `high` when the task affects payments, auth, security, production data, migrations, irreversible operations, broad architecture, public release, or anything hard to roll back.

Risk controls:

- Low: use compact run card, optional decision gates, focused verification, concise final report.
- Medium: write a clear contract before edits, run a brief first-principles gate, run a brief adversarial review, run relevant checks, report risks.
- High: require first-principles and adversarial gates, include rollback plan, stronger verification, release mode, and explicit residual risk.

## Decision Gates

Use two lightweight gates to improve accuracy before the model commits to a path.

First-principles gate asks what must be true, what is actually necessary, and which assumptions are being smuggled in by habit. Use it before the Contract state for medium/high-risk work, or when the task feels vague, over-engineered, or copied from a prior pattern.

Adversarial review asks how the plan could fail, which evidence could be misleading, and which edge cases would embarrass the solution after release. Use it before the Verify state for medium/high-risk work, or when the change touches auth, data, payments, external integrations, deployment, user-facing workflows, or irreversible operations.

Keep both gates compact:

- First principles: necessary user outcome, hard constraints, assumptions, simpler rejected options.
- Adversarial review: likely failure modes, false confidence signals, edge cases, missing checks.
- Record important gate outputs with `update_run.py` so they appear in the case log.

## User Constraint Gate

Before executing a request, compare it with the approved user story, design contract,
security boundaries, data-integrity rules, and release gates.

Classify conflicts as:

- **Hard constraint**: security, privacy, secrets, immutable source data, provenance,
  legal/compliance, or truthful verification. Block the request and provide a compliant
  alternative. User insistence does not override it.
- **Negotiable constraint**: MVP scope, TTL, provider choice, quality/cost trade-offs,
  or other approved-contract changes. Warn first, state the impact, and require owner
  approval if the contract itself changes.
- **Advisory constraint**: a recommendation that affects efficiency or quality but not
  correctness or safety. Inform the user and continue.

Never change an approved contract silently. Record violations, warnings, corrections,
and explicit exceptions in the run or case log. Do not promote a project-specific
exception into a cross-project rule without user approval.

## State 0: Intent

Lock the direction before coding.

Capture:

- Goal
- Non-goal
- User or customer value
- Success criteria
- Expected output
- Risk level

If the request is clear, infer these briefly and proceed. Ask only when ambiguity would materially change the implementation or create risky work.

## State 1: Context

Gather only the context needed to act correctly.

Inspect:

- Relevant files
- Existing patterns
- Product constraints
- Data model
- Tests and build commands
- Prior docs, ADRs, case logs, or playbooks if present
- External docs only when the task depends on current or unfamiliar APIs

Prefer existing codebase conventions over new abstractions.

The project's SSOT should already exist from bootstrap:

```text
docs/company.md
docs/product.md
docs/customers.md
docs/system.md
docs/playbooks/README.md
docs/case-log/README.md
```

Use these files as the first stop for durable context. If they are missing, run:

```bash
python <skill-dir>/scripts/init_ssot.py <project-root>
```

Also read `<skill-dir>/references/approved-experience.md` when the task resembles a previously approved cross-project lesson.

For each task, update only the durable knowledge that changed:

- Company changes: positioning, business model, operating constraints.
- Product changes: users, promise, scope, roadmap, feature boundaries.
- Customer changes: target segments, feedback, pains, objections, success signals.
- System changes: architecture, data model, integrations, commands, deployment.
- Playbooks: repeated workflows or fixes.
- Case logs: significant one-off execution records.

Do not turn every task into a documentation pass. Preserve speed by updating SSOT only when it improves future accuracy.

Canonical SSOT locations:

```text
docs/company.md
docs/product.md
docs/customers.md
docs/system.md
docs/playbooks/
docs/case-log/
```

## State 2: Contract

Before meaningful edits, state the execution contract.

Every new run also has a delivery contract at
`.harness/runs/<run-id>/delivery-contract.md`. Treat it as the owner's definition
of real completion, not as optional planning prose. Before State 3, complete and
approve it with:

```bash
python <skill-dir>/scripts/contract.py update <project-root> --run-id <run-id> \
  --why "The user needs a reliable saved result" \
  --approach "Reuse the existing provider boundary" \
  --acceptance "User sees a real result || real input, provider response, persistence, and UI evidence || mock output, hardcoded response, or manual database edit" \
  --boundaries "Keep the existing auth boundary; no unrelated redesign" \
  --anti-cheat "Do not bypass the provider or count fixtures as production data" \
  --infeasible "Cannot support offline processing until the provider contract exists" \
  --alternative "Use a queued job later; rejected for this MVP because it adds operational scope" \
  --divergence "Compared direct request, queue, and batch replay; selected direct request for the MVP" \
  --verification "Run the real user path with a non-fixture input and inspect persisted evidence" \
  --rollback "Revert the change and preserve the previous successful result"
python <skill-dir>/scripts/contract.py validate <project-root> --run-id <run-id>
python <skill-dir>/scripts/contract.py approve <project-root> --run-id <run-id> --approved-by "owner"
```

The `--acceptance` value must use this format:
`criterion || evidence || prohibited shortcut`. Every criterion needs observable
evidence and an explicit statement of what does not count as success.

The contract must answer, at the same granularity as a company delivery brief:

- Why the work exists and which user or business outcome matters.
- The chosen implementation approach and what is deliberately out of scope.
- Testable acceptance criteria, each mapped to evidence and a counterexample.
- Boundaries, non-goals, security or data constraints, and rollback or recovery.
- Anti-gaming rules: the shortest paths that satisfy a metric without delivering the
  real outcome. Examples include hardcoded output, fixture-only success, mocked
  provider evidence, disabled auth, manual database edits, hidden errors, or a page
  that opens without the real user path working.
- Infeasible paths, unresolved dependencies, divergent options considered, and the
  trade-off behind the selected approach.

Ask: “If an agent optimized only for the metric, how could it fake completion?”
Turn each answer into a prohibited shortcut and a verification check. Do not claim
completion from a proxy when the contract requires a real path.

The contract is a gate. A new run starts as `contract_pending`; production code,
schema, migration, public API, release configuration, and user-facing workflow
changes must wait for owner approval. `contract.py check` must pass before Execute.
If an approved contract changes, the tool automatically returns it to `draft` and
blocks completion until it is approved again. If the goal cannot be met, mark the
run `blocked` and report the failed approaches, closest alternatives, trade-offs,
and the decision needed from the owner. Never silently relax the contract.

For medium/high-risk work, run the first-principles gate before writing the contract:

- What user or business outcome is truly required?
- What constraints are real rather than inherited from the current implementation?
- What assumptions need verification?
- What simpler option was rejected and why?

For low-risk work, keep it to a few bullets.

For medium or high-risk work, include:

- Planned changes
- Files or areas likely to change
- Boundaries and non-goals
- Verification plan
- Rollback or recovery plan
- Known risks

Proceed after writing the contract unless user input is truly required.

## State 3: Execute

Implement in small, reversible steps.

Rules:

- Prefer deletion and simplification over new layers.
- Reuse existing utilities, patterns, and architecture.
- Keep diffs narrow and reviewable.
- Avoid new dependencies unless explicitly justified.
- Preserve user changes.
- Keep generated code observable, testable, and easy to review.
- Record important decisions as they happen.

Use subagents only for independent bounded work such as code search, review, test design, or parallel implementation slices.

## State 4: Verify

Do not claim completion without evidence.

Before running checks for medium/high-risk work, run the adversarial review gate:

- How could this fail in the real user path?
- Which passing check could create false confidence?
- Which edge cases, empty states, permissions, network failures, data states, or platform constraints matter?
- What evidence would change the release decision?

Choose checks based on risk:

- Low: run the most relevant focused test, lint, typecheck, build, or manual check.
- Medium: run focused tests plus typecheck, lint, or build when available. Manually verify changed UI or workflow behavior.
- High: run the full relevant test suite where feasible. Verify rollback or recovery story. Check security, data, auth, migration, and production-impact assumptions.

If verification fails, fix and rerun.

Report any check that could not be run and why.

## State 5: Release

Choose a release mode when the task affects real users or deployment.

Use one of:

- `local-only`: change stays local.
- `dogfood`: user tries it first.
- `seed-user`: share with one or a few trusted users.
- `beta`: limited public use.
- `full`: broad release.

For solo-company work, prefer `dogfood` or `seed-user` before `full` when the change affects real users.

Record:

- Release mode
- Rollback point
- What to watch
- Known risk

## State 6: Observe

At the end of each task, capture useful observations.

Include:

- What changed
- What worked
- What surprised us
- What failed or nearly failed
- What remains risky
- What evidence proves completion

For significant tasks, create a case log with `finish_run.py`. The script should generate the file automatically when the task is medium or high risk, contains surprises or lessons, or has failed verification.

```text
docs/case-log/YYYY-MM-DD-short-title.md
```

Use this format:

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

Do not create case logs for trivial edits unless the task revealed reusable knowledge.

## State 7: Distill

Convert repeated lessons into reusable assets.

Use this rule:

```text
single event -> case log
repeated event -> playbook
stable playbook -> skill or automation
```

When a pattern appears more than once, update or create:

- `docs/playbooks/<topic>.md`
- Project conventions
- Regression tests
- Reusable prompts
- Child skills
- Checklist items

Do not update this skill on every run. Queue feedback first, then generate a proposal with `propose_skill_update.py`. Update the skill only when the operating process changes.

Experience promotion path:

```text
project run -> case log -> project playbook -> skill feedback proposal -> user approval -> approved-experience.md -> optional SKILL.md patch
```

Use `promote_experience.py` only after user approval. Promote only lessons that are reusable across projects. Keep project facts in the project SSOT.

## Compact Run Card

Use this for low-risk tasks:

```text
Intent: What are we trying to achieve?
Context: What must be known before changing code?
First Principles: What is truly necessary, and what are we assuming?
Contract: What will change, and what is out of bounds?
Execute: Make the smallest correct change.
Adversarial Review: How could this fail, and what proof would catch it?
Verify: Prove it works.
Release: Choose local-only, dogfood, seed-user, beta, or full.
Observe: Record what happened.
Distill: Save reusable learning only if useful.
```

## Required Final Report

End each task with a concise report:

- Changed files
- Verification run
- Release mode, if relevant
- Remaining risks
- Distilled lesson, if any

Keep the report short for small tasks.

## Anti-Patterns

Avoid:

- Coding before intent is clear.
- Letting AI redesign unrelated architecture.
- Accepting model output without verification.
- Treating prompt, skill, model, MCP, or data changes as casual configuration.
- Losing decisions in chat history.
- Shipping directly to all users when dogfood is possible.
- Repeating the same fix without turning it into a playbook.
