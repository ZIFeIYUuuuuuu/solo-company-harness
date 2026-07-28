# Operating Modes

Load this reference only when choosing or explaining a run mode.

## Explore

Use for local prototypes, spikes, one-off scripts, and reversible experiments.

- Do not initialize full SSOT solely for the experiment.
- Do not require owner approval for the compact run card.
- Do not claim production readiness, user adoption, or external reliability.
- Run a focused smoke check when useful.
- Save a case log only when the experiment creates reusable knowledge.

The compact state still records the goal, a local acceptance check, a boundary, and a
rollback reminder. It is deliberately not a full delivery contract.

## Delivery

Use for user-facing behavior, shared code, data shape, integrations, project structure,
or deployment configuration.

- Read relevant SSOT and project rules.
- Complete and approve the delivery contract before production edits.
- Run local verification at minimum L1.
- Record a release mode and residual risks.

## High-Assurance

Use for auth, payments, production data, migrations, public release, security, or work
that is difficult to reverse.

- Complete first-principles and adversarial gates.
- Include rollback or recovery boundaries.
- Require at least L2 evidence, or explicitly report why it is unavailable.
- Prefer staging, dogfood, or seed-user release before broad release.

## Mode Selection

`start_run.py --mode auto` maps:

```text
low risk    -> explore
medium risk -> delivery
high risk   -> high-assurance
```

A caller can choose a stricter mode. It cannot choose a weaker mode than the detected
risk requires.
