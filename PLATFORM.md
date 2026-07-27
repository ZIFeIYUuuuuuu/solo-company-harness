# Platform Notes

## Current Support

The primary verified host is Codex. The repository uses the Agent Skills standard
for discovery and keeps the workflow logic in plain Python scripts, so the core ideas
can be adapted to other agents that support `SKILL.md`.

Codex-specific pieces currently include:

- installation under `~/.codex/skills/solo-company-harness`;
- the `$solo-company-harness` invocation name;
- `agents/openai.yaml` metadata;
- the examples in `README.md` and `SKILL.md`.

The run state, delivery contract, evidence model, and case-log formats are intended to
remain host-neutral. A future adapter for another agent should preserve those formats
and only change discovery, installation, and invocation instructions.

## Adapting to Another Agent

1. Install or expose the folder using that agent's skill mechanism.
2. Point the agent at `SKILL.md`.
3. Keep the bundled scripts runnable with Python 3.10 or newer.
4. Preserve `.harness/runs/` state and evidence fields.
5. Replace only the host-specific invocation and metadata examples.

Compatibility is not automatic. Test the adapter with the repository's smoke commands
before describing another host as supported.
