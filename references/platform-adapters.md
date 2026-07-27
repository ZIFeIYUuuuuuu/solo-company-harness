# Platform Adapters

Load this reference when installing the Skill on a host other than Codex.

The portable core is:

- `SKILL.md` routing rules;
- `.harness/runs/` state and events;
- delivery-contract fields;
- evidence levels and receipts;
- case logs and playbook promotion.

The Codex adapter is:

- installation under `~/.codex/skills/solo-company-harness`;
- invocation through `$solo-company-harness`;
- `agents/openai.yaml` metadata;
- Codex-specific README examples.

Another host needs an adapter for discovery, installation, invocation, and metadata.
Do not describe it as supported until the adapter preserves the state format and passes
the repository tests and smoke flow. External operations such as DNS, CI/CD, payments,
or compliance belong in separate project or platform integrations, not in this base
Skill.
