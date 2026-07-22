# Solo Company Harness

English | [中文](#中文)

Solo Company Harness is a Codex skill for solo founders and one-person companies who use AI coding to build, debug, verify, release, and continuously improve software projects.

It turns every AI coding task into a lightweight operating loop:

```text
Intent -> Context -> Contract -> Execute -> Verify -> Release -> Observe -> Distill
```

The goal is simple: ship faster without losing correctness, project memory, verification evidence, or reusable learning.

Before implementation, the harness resolves one of two modes:

- **Design-Locked**: an approved module design and user story with testable acceptance criteria exist, so implementation proceeds without reopening settled decisions.
- **Discovery-Gated**: the module contract is missing, draft, stale, or incomplete; the harness asks targeted questions and allows draft documentation, but blocks production code until the owner approves the contract.

## What It Does

- Initializes a project SSOT (single source of truth) for company, product, customer, and system knowledge.
- Creates or refreshes a project-level `AGENTS.md` contract.
- Starts structured AI coding runs with `.harness/runs/<run-id>/state.json`.
- Detects task risk levels from task text and file scope.
- Detects likely test/build commands from project files.
- Runs verification commands and records results.
- Generates case logs for meaningful work.
- Promotes repeated lessons into playbooks.
- Queues skill improvements for review.
- Promotes user-approved cross-project lessons into skill-level approved experience.

## Install

Copy this folder into your Codex skills directory:

```bash
cp -R solo-company-harness ~/.codex/skills/
```

On Windows PowerShell:

```powershell
Copy-Item -Recurse .\solo-company-harness C:\Users\Administrator\.codex\skills\
```

Then invoke it in Codex:

```text
Use $solo-company-harness for this project.
```

## Project Bootstrap

From a project root, initialize project memory:

```bash
python ~/.codex/skills/solo-company-harness/scripts/init_ssot.py .
```

This creates:

```text
docs/company.md
docs/product.md
docs/customers.md
docs/system.md
docs/playbooks/README.md
docs/case-log/README.md
```

Create or refresh the project `AGENTS.md`:

```bash
python ~/.codex/skills/solo-company-harness/scripts/init_agents.py . --skill-path ~/.codex/skills/solo-company-harness
```

## Typical Workflow

Start a run:

```bash
python ~/.codex/skills/solo-company-harness/scripts/start_run.py . --title "add login" --goal "Add user login"
```

Record decisions or changed files:

```bash
python ~/.codex/skills/solo-company-harness/scripts/update_run.py . --changed-file src/auth/login.ts --decision "Reuse existing auth boundary"
```

Detect tests:

```bash
python ~/.codex/skills/solo-company-harness/scripts/detect_tests.py . --write-run
```

Run checks:

```bash
python ~/.codex/skills/solo-company-harness/scripts/run_checks.py . --auto
```

Resolve a module mode:

```bash
python ~/.codex/skills/solo-company-harness/scripts/resolve_mode.py . --module assembly-planner
```

Finish a run:

```bash
python ~/.codex/skills/solo-company-harness/scripts/finish_run.py . --lesson "Auth changes need focused regression tests"
```

Promote a repeated lesson into a playbook:

```bash
python ~/.codex/skills/solo-company-harness/scripts/update_playbook.py . --topic "auth regression checks"
```

Promote approved cross-project experience into the skill:

```bash
python ~/.codex/skills/solo-company-harness/scripts/promote_experience.py . --skill-root ~/.codex/skills/solo-company-harness --approved-by "you" --lesson "Medium-risk auth changes require regression checks"
```

## Repository Layout

```text
SKILL.md
agents/openai.yaml
references/approved-experience.md
scripts/
  init_ssot.py
  init_agents.py
  start_run.py
  update_run.py
  detect_risk.py
  detect_tests.py
  run_checks.py
  finish_run.py
  update_playbook.py
  propose_skill_update.py
  promote_experience.py
  resolve_mode.py
```

## Design Principles

- Keep project facts in the project SSOT.
- Keep run evidence in `.harness/runs/`.
- Keep one-off lessons in case logs.
- Promote repeated lessons into project playbooks.
- Promote only user-approved cross-project lessons into skill-level approved experience.
- Do not silently mutate the skill from one run.

## 中文

Solo Company Harness 是一个面向独立开发者、一人公司和 solo founder 的 Codex Skill。它帮助你在使用 AI Coding 做项目时，同时保证效率、准确性、验证证据和经验沉淀。

它把每次 AI Coding 任务变成一个轻量状态循环：

```text
Intent -> Context -> Contract -> Execute -> Verify -> Release -> Observe -> Distill
```

目标很简单：让你更快交付，同时不丢失项目知识、验证结果、决策记录和可复用经验。

开始编码前，Harness 会先判断模块是否已经具备批准的设计文档和用户故事：

- **Design-Locked**：设计和用户故事已批准，直接按合同实现。
- **Discovery-Gated**：设计缺失、仍为草稿或验收标准不完整，只能先追问和补齐文档，不能修改生产代码。

## 它能做什么

- 初始化项目 SSOT（单一事实源），保存公司、产品、客户和系统知识。
- 创建或刷新项目级 `AGENTS.md` 契约。
- 为每次 AI Coding 创建 `.harness/runs/<run-id>/state.json` 状态记录。
- 根据任务描述和文件范围自动判断风险等级。
- 根据项目文件自动识别测试、构建、类型检查命令。
- 自动运行验证命令并记录结果。
- 为重要任务生成 case log。
- 把重复经验沉淀成 playbook。
- 把 Skill 改进建议放入审核队列。
- 经用户审核后，把跨项目经验写入 Skill 的 approved experience。

## 安装

把本文件夹复制到 Codex skills 目录：

```bash
cp -R solo-company-harness ~/.codex/skills/
```

Windows PowerShell：

```powershell
Copy-Item -Recurse .\solo-company-harness C:\Users\Administrator\.codex\skills\
```

然后在 Codex 里调用：

```text
使用 $solo-company-harness 开始这个项目。
```

## 初始化项目

在项目根目录初始化 SSOT：

```bash
python ~/.codex/skills/solo-company-harness/scripts/init_ssot.py .
```

它会创建：

```text
docs/company.md
docs/product.md
docs/customers.md
docs/system.md
docs/playbooks/README.md
docs/case-log/README.md
```

创建或刷新项目 `AGENTS.md`：

```bash
python ~/.codex/skills/solo-company-harness/scripts/init_agents.py . --skill-path ~/.codex/skills/solo-company-harness
```

## 常见工作流

开始一次任务：

```bash
python ~/.codex/skills/solo-company-harness/scripts/start_run.py . --title "add login" --goal "Add user login"
```

记录决策或变更文件：

```bash
python ~/.codex/skills/solo-company-harness/scripts/update_run.py . --changed-file src/auth/login.ts --decision "Reuse existing auth boundary"
```

自动识别测试命令：

```bash
python ~/.codex/skills/solo-company-harness/scripts/detect_tests.py . --write-run
```

运行验证：

```bash
python ~/.codex/skills/solo-company-harness/scripts/run_checks.py . --auto
```

结束任务并沉淀经验：

```bash
python ~/.codex/skills/solo-company-harness/scripts/finish_run.py . --lesson "Auth changes need focused regression tests"
```

把重复经验升级成 playbook：

```bash
python ~/.codex/skills/solo-company-harness/scripts/update_playbook.py . --topic "auth regression checks"
```

把用户审核过的跨项目经验写入 Skill：

```bash
python ~/.codex/skills/solo-company-harness/scripts/promote_experience.py . --skill-root ~/.codex/skills/solo-company-harness --approved-by "you" --lesson "Medium-risk auth changes require regression checks"
```

## 设计原则

- 项目事实保存在项目 SSOT。
- 执行证据保存在 `.harness/runs/`。
- 单次经验写入 case log。
- 重复经验沉淀成项目 playbook。
- 只有经过用户审核的跨项目经验，才写入 Skill 级 approved experience。
- 不因为一次运行结果就静默修改 Skill 本体。
