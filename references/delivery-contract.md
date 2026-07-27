# Delivery Contract

Load this reference for `delivery` and `high-assurance` runs.

The contract is a short decision record, not a design essay. It must answer:

- Why does this work exist?
- What user or business outcome matters?
- What approach is selected?
- What is explicitly out of scope?
- What observable evidence proves each acceptance criterion?
- Which shortcuts satisfy a metric without delivering the outcome?
- Which paths are infeasible right now?
- Which alternatives were considered and rejected?
- How will the change be verified, released, and recovered?

Each acceptance item uses:

```text
criterion || evidence || prohibited shortcut
```

Before approving, ask:

> If an agent optimized only for the metric, how could it fake completion?

Convert each answer into an anti-gaming rule and a verification action. Examples of
invalid substitutes include hardcoded output, fixture-only success, fake Provider
responses, disabled authentication, manual database edits, hidden errors, and a page
that opens without the real user path.

The owner approves the contract. An approved contract is immutable until the owner
reviews the changed boundary again. A run that cannot meet its contract is `blocked`,
not completed with a weaker claim.

The current CLI workflow is:

```bash
python <skill-dir>/scripts/contract.py update <project-root> --why "<why>" --approach "<how>"
python <skill-dir>/scripts/contract.py validate <project-root>
python <skill-dir>/scripts/contract.py approve <project-root> --approved-by "<owner>"
```

The script validates structure and explicit fields. It cannot judge product truth by
itself; project-specific verification recipes and evidence are still required.
