# Platform Adapters

Load this reference when installing the Skill on a specific Agent host or when the
host's discovery behavior is unclear.

The core is host-neutral. A compatible host needs to discover a folder containing
`SKILL.md`, expose its scripts, and let the user invoke the skill by name or by
instruction. The run state, delivery contract, evidence levels, and case logs do not
depend on the host. The host supplies model access, shell/file tools, permissions,
MCP servers, and any external integrations.

## Supported Installation Shapes

| Host | Recommended skill directory | Project instruction file | Invocation |
| --- | --- | --- | --- |
| Codex | `~/.codex/skills/solo-company-harness` | `AGENTS.md` | `Use $solo-company-harness` |
| Claude Code | `~/.claude/skills/solo-company-harness` or `.claude/skills/solo-company-harness` | `CLAUDE.md` | Ask Claude Code to use `solo-company-harness` |
| OpenCode | `~/.config/opencode/skills/solo-company-harness` or `.opencode/skills/solo-company-harness` | `AGENTS.md` | Ask OpenCode to use `solo-company-harness` |
| Other Agent Skills hosts | Host-defined skill directory | Host-defined or `AGENTS.md` | Host-defined |

Paths are defaults, not guarantees. Check the host's current skill discovery rules
before publishing an adapter as supported.

## Install From An Agent

The preferred installation flow is conversational. Ask the target Agent to install
the repository and report the destination it used:

```text
Install and enable this Agent Skill:
https://github.com/ZIFeIYUuuuuuu/solo-company-harness

I am using <Codex / Claude Code / OpenCode / another Agent Skills host>.
Use that host's current Skill discovery rules, do not put the Skill inside the
project source tree, and confirm that SKILL.md can be loaded after installation.
```

For a project-local install, ask the Agent to use the host's project skill directory
and preserve existing project rules. Do not ask the user to guess a global path.

## Scripted Install Fallback

The repository includes a local installer for the common directory shapes. Run it
only for CI, packaging, or a host that cannot perform the conversational install:

```bash
python scripts/install_host.py --host codex
python scripts/install_host.py --host claude-code
python scripts/install_host.py --host opencode
```

Use an explicit destination for another host:

```bash
python scripts/install_host.py --host generic --dest /path/to/agent/skills/solo-company-harness
```

The installer copies only the portable Skill payload, refuses to overwrite an
existing destination, and requires `--update` for a refresh. For a project-local
installation, pass a host-specific destination such as `.claude/skills/` or
`.opencode/skills/`.
Normal users should not need to run these commands themselves.

## Project Instructions

`AGENTS.md` is the portable default. Generate the right project instruction file for
the host:

```bash
python scripts/init_agents.py <project-root> \
  --host claude-code \
  --skill-path /path/to/solo-company-harness
```

Use `--host codex`, `--host opencode`, or `--host generic` for `AGENTS.md`. Use
`--instruction-file` when a compatible host uses another filename.

The managed block is marker-bounded and preserves user content outside the block.

## Adapter Boundary

The core Skill does not configure DNS, CI/CD, payments, cloud resources, browsers,
finance, or compliance. Those capabilities belong in project recipes, MCP servers,
or host-specific skills. An adapter changes discovery, installation, invocation, and
project instruction conventions; it must not silently change run state semantics.

CI tests the Python scripts, host paths, installation behavior, and state
transitions. It does not prove that every client discovers a skill correctly. Test
each host adapter in its own client before calling that host production-supported.
