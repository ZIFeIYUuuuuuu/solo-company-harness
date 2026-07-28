# Platform Notes

Solo Company Harness follows the [Agent Skills](https://agentskills.io) folder
convention. The portable unit is a directory containing `SKILL.md`, references, and
optional scripts. The host is responsible for discovering and invoking that folder.

## Included Adapters

| Host | Included path | What is covered here |
| --- | --- | --- |
| Codex | `~/.codex/skills/` | `agents/openai.yaml` UI metadata and `AGENTS.md` instructions |
| Claude Code | `~/.claude/skills/` or `.claude/skills/` | `CLAUDE.md` instructions |
| OpenCode | `~/.config/opencode/skills/` or `.opencode/skills/` | `AGENTS.md` instructions |
| Agent Skills-compatible host | host-defined destination | Portable `SKILL.md`, references, and scripts |

The Python scripts, `.harness/runs/` state, delivery contracts, evidence receipts,
case logs, and playbooks are host-neutral. `agents/openai.yaml` is optional metadata
for Codex and is not required by the core Skill.

## What Is Tested

The repository CI tests Python syntax, state transitions, mode routing, contracts,
evidence gates, legacy migration, host selection, installation, and instruction-file
generation. It does not launch every Agent client. Client-specific discovery and
invocation should still be smoke-tested in that client's own environment.

## Adapting Another Host

1. Install the folder using the host's documented skill directory or
   `scripts/install_host.py`.
2. Make the host load `SKILL.md` and the selected `references/` files on demand.
3. Use `AGENTS.md`, `CLAUDE.md`, or the host's instruction file without changing the
   managed contract semantics. Generate it with `scripts/init_agents.py --host ...`.
4. Keep the bundled scripts runnable with Python 3.10 or newer.
5. Run the repository tests and a real host smoke flow before calling the adapter
   production-ready.

External operations such as DNS, CI/CD, payments, or compliance require separate
project or platform integrations. This Skill is the delivery control layer around
those tools, not a replacement for them.
