# Solo Company Harness

面向独立开发者、一人公司和 AI Coding 工作流的项目交付 Skill。

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-2563EB?style=flat-square)](https://agentskills.io)
[![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square)](https://github.com/openai/codex)
[![License](https://img.shields.io/badge/License-TBD-F59E0B?style=flat-square)](#许可证)

这个仓库把一人公司使用 AI 编写软件时反复遇到的工作方法，整理成一个可以被 Agent 直接加载的结构化 Skill。

It turns every AI coding task into a lightweight operating loop:

```text
Intent -> Context -> Contract -> Execute -> Verify -> Release -> Observe -> Distill
```

目标很简单：更快交付，同时不丢失正确性、项目记忆、验证证据和可复用经验。

Before implementation, the harness resolves one of two modes:

- **Design-Locked**: an approved module design and user story with testable acceptance criteria exist, so implementation proceeds without reopening settled decisions.
- **Discovery-Gated**: the module contract is missing, draft, stale, or incomplete; the harness asks targeted questions and allows draft documentation, but blocks production code until the owner approves the contract.

它不是一个代码生成模板，也不是一套强制性的企业流程。它提供的是一组轻量门禁，让 Agent 在真正改代码前先确认合同，在交付前证明真实路径。

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

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/ZIFeIYUuuuuuu/solo-company-harness.git ~/.codex/skills/solo-company-harness
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

## 用户约束门

这个 Skill 不只约束 Agent，也会在用户请求违反项目合同的时候主动提醒用户，避免错误反复发生。

- **硬约束**：安全、隐私、密钥、数据不可变性、来源追溯、法律合规和真实验收。违反时阻止执行，说明风险并给出替代方案；用户坚持也不能绕过。
- **可协商约束**：MVP 范围、TTL、模型选择、成本和质量取舍。先说明影响，再采用可逆修正；如果需要改变批准合同，要求用户明确批准并记录例外。
- **建议约束**：只影响效率或工程质量。主动提醒，但不无故阻塞任务。

任何自动修正都必须先告知用户。已批准的合同不能被静默改变，项目例外也不能自动升级成跨项目规则。

## 真实链路门禁

涉及 AI Provider、上传、回调、认证、同步或公网资源时，必须优先验证一条真实端到端路径：

```text
真实输入 -> 本地应用 -> 外部服务 -> 真实结果 -> 本地持久化 -> 用户可见结果
```

局部测试、模拟 Provider、构建成功或浏览器页面能打开，都不能单独证明产品路径可用。

跨服务配置也是系统代码的一部分，必须在 `.env`、Docker、启动脚本、反向代理、远端存储、文档和测试命令之间保持一致。一个生产能力只保留一个 canonical path，避免重复网关、重复存储和重复 secret。

先完成一个可证明的 MVP 闭环，再增加多窗口、replay、审计、策略和质量优化。传输可用性必须先于模型语义质量。

## 安装

把仓库克隆到 Codex skills 目录：

```bash
git clone https://github.com/ZIFeIYUuuuuuu/solo-company-harness.git ~/.codex/skills/solo-company-harness
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

## 贡献

欢迎提交 Issue、Pull Request 和跨项目实践经验。

适合贡献的内容包括：

- 可复用的 Harness 工作流；
- 针对真实失败模式的验证脚本；
- 不依赖特定项目的 playbook；
- 对用户约束、风险门禁和验收流程的改进。

提交前请确认：

- 不包含 API Key、secret、个人路径或项目私有数据；
- 修改有清晰的使用场景、边界和验证方式；
- README、SKILL.md 和脚本行为保持一致。

## 许可证

当前仓库暂未声明许可证。正式开源发布前，请在仓库根目录补充明确的 `LICENSE` 文件，并同步更新上方徽章。

由 [ZIFeIYUuuuuuu](https://github.com/ZIFeIYUuuuuuu) 维护。
