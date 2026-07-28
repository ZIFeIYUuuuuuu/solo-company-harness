<div align="center">

# Solo Company Harness

### 面向独立开发者的一人公司 AI Coding 交付 Skill

[![License](https://img.shields.io/badge/License-MIT-2563EB?style=for-the-badge)](./LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-7C3AED?style=for-the-badge)](https://agentskills.io)
[![Codex](https://img.shields.io/badge/Codex-compatible-059669?style=for-the-badge)](https://github.com/openai/codex)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-D97757?style=for-the-badge)](https://docs.anthropic.com/en/docs/claude-code)
[![OpenCode](https://img.shields.io/badge/OpenCode-compatible-111827?style=for-the-badge)](https://opencode.ai)

**让 AI 不只会写代码，还能按目标、合同、证据和复盘把项目交付出来。**

[快速开始](#快速开始) · [它解决什么](#它解决什么) · [工作流](#工作流) · [许可证](#许可证)

</div>

## 它解决什么

AI Coding 已经可以在几分钟内生成页面、接口和测试，但一个真正能交付的产品还需要回答：

- 为什么做这个功能？
- 谁会使用它？
- 什么算完成？
- 哪些实现方式虽然能让指标通过，但不算交付？
- 用什么证据证明真实路径可用？
- 这次的经验如何避免下次重复踩坑？

Solo Company Harness 把这些问题变成 Agent 可以持续执行的项目工作流，适合独立开发者、solo founder、一人公司和使用 AI Coding 的小团队。

它不是代码生成模板，也不是一份越来越长的 Prompt。它更准确地说是一层 AI 软件交付控制层：保留项目记忆，约束任务边界，记录决策和证据，并把重复经验沉淀成可复用规则。

核心规则保持在轻量的 `SKILL.md` 中，交付合同、证据等级和平台说明放在 `references/`，按任务模式按需读取，避免简单任务承担完整流程的上下文成本。

## 核心工作流

```text
Intent -> Context -> Contract -> Execute -> Verify -> Release -> Observe -> Distill
```

| 阶段 | 解决的问题 | 典型产物 |
| --- | --- | --- |
| Intent | 为什么做，成功是什么 | 目标、用户价值、非目标、风险等级 |
| Context | 做之前必须知道什么 | 项目 SSOT、代码上下文、约束、历史决策 |
| Contract | 准备怎么做，什么不算完成 | 交付合同、验收标准、反作弊规则、回滚方案 |
| Execute | 如何保持小步、可逆和可审查 | 变更文件、执行决策 |
| Verify | 如何证明真实可用 | 测试命令、真实路径、验证结果 |
| Release | 如何控制发布风险 | local-only、dogfood、beta 或 full |
| Observe | 这次实际发生了什么 | 意外、残余风险、证据、后续事项 |
| Distill | 哪些经验值得保留 | case log、playbook、Skill 改进提案 |

## 两种实现模式

当任务对应一个明确模块时，Harness 可以先判断模块是否具备批准的设计合同：

- **Design-Locked**：模块设计和用户故事都已批准，范围、非目标和验收标准完整，Agent 可以按合同实现。
- **Discovery-Gated**：设计缺失、仍是草稿、已过期或验收不完整，Agent 可以调研和补文档，但不能直接修改生产代码、数据库结构、公开 API 或发布配置。

在 Agent 对话中直接说：

```text
请使用 solo-company-harness 检查当前项目的 upload 模块是否已经 Design-Locked。
只做检查和报告，不要修改生产代码；如果设计缺失、过期或验收标准不完整，
请列出需要我确认的文档和问题。
```

Agent 会自动读取项目文档并执行对应检查。这一步只负责判断模块准备度，真正开始编码仍然需要通过本次任务的交付合同。

## 主要能力

### 项目记忆

初始化项目级 SSOT，集中保存公司、产品、客户和系统信息：

```text
docs/company.md
docs/product.md
docs/customers.md
docs/system.md
docs/playbooks/
docs/case-log/
```

### 风险感知

根据任务描述和文件范围识别 low、medium、high 风险。登录、支付、生产数据、迁移、部署和安全边界会自动进入更严格的验证路径。

### 渐进式使用模式

风险会自动映射到不同的流程重量：

| 模式 | 适合 | 默认行为 |
| --- | --- | --- |
| `explore` | 原型、一次性脚本、局部实验 | 只保留紧凑 state，不生成完整合同文件，不允许把结果当成生产交付 |
| `delivery` | 正式功能和用户可见改动 | 完整交付合同、验收证据和回滚边界 |
| `high-assurance` | 支付、认证、迁移、生产数据和公开发布 | 更严格的决策门、证据等级和恢复要求 |

也可以手动指定模式，但不能用低级模式绕过高风险任务的最低要求：

```text
请使用 solo-company-harness，以 explore 模式在当前项目中验证一个 parser 原型。
保持改动局部且可逆，不要把原型描述成生产就绪；完成后告诉我实际验证了什么、
哪些问题仍未解决。
```

### 交付合同

在正式修改生产代码之前，要求任务明确写出：

- 为什么做，以及真实用户或业务结果；
- 选择的实现方案和明确边界；
- 可观察的验收标准和对应证据；
- 不可行路径、替代方案和发散思路；
- 回滚或恢复方式。

### Anti-gaming 反作弊验收

每条验收标准都要说明什么不算通过，防止 Agent 只完成指标、不完成真实目标。

例如，真实上传链路不能用下面这些方式冒充完成：

- 手动修改数据库制造成功状态；
- 用 fixture 冒充真实用户数据；
- 用 mock Provider 结果冒充真实外部服务；
- 关闭鉴权让流程暂时跑通；
- 只验证页面能打开，不验证真实用户路径；
- 隐藏错误，只展示成功提示。

### 验证与证据

自动识别项目中的测试、类型检查、Lint 和构建命令，运行后把结果写入 run 记录。涉及外部服务、上传、回调、认证或同步时，优先验证一条真实端到端路径，而不是只看局部测试或构建是否成功。

验证证据分为五级：

```text
L0 static      静态检查
L1 local       本地测试、类型检查、构建或手动 smoke
L2 integration 集成测试或模拟外部服务
L3 real-path   真实第三方服务和真实用户链路
L4 dogfood     自己或种子用户实际使用
```

`delivery` 和 `high-assurance` run 会声明最低证据等级。补充真实路径或 dogfood 证据：

```text
请使用 solo-company-harness 验证真实上传链路，不要只运行单元测试或 mock。
请用非 fixture 文件走真实 Provider、持久化和页面展示路径，保存可追溯的验证产物，
并在最终报告中标明实际达到的证据等级和仍然缺失的证据。
```

Agent 会记录证据收据，但不会假装替你验证外部系统。真实支付、回调、异步任务和远端数据仍然需要项目自己的验证 recipe、沙箱账号和可追溯产物。

### 经验沉淀

```text
单次事件 -> case log
重复问题 -> project playbook
跨项目且经用户批准的经验 -> approved experience
稳定的工作方法 -> Skill 或自动化
```

Skill 不会因为一次任务的反馈而被静默修改，所有跨项目规则都要经过审核。

## 快速开始

### 1. 在 Agent 中安装

在 Codex、Claude Code、OpenCode 或其他支持 Agent Skills 的智能体中新开一个对话，直接发送：

```text
请安装并启用这个 Agent Skill：
https://github.com/ZIFeIYUuuuuuu/solo-company-harness

我当前使用的智能体是：<Codex / Claude Code / OpenCode / 其他宿主>
请按照该宿主当前的 Skill 发现规则安装，不要把 Skill 文件复制进项目源码目录。
安装完成后告诉我实际安装位置，并确认 SKILL.md 可以被加载；不要修改当前项目代码。
```

如果你的 Agent 不支持自动发现 Skill，可以把下面这句话发给它：

```text
请读取这个仓库中的 SKILL.md，把它作为当前项目的 Agent 规则加载：
https://github.com/ZIFeIYUuuuuuu/solo-company-harness/blob/main/SKILL.md
```

不要让用户先查找 `~/.codex`、`~/.claude` 或其他目录。宿主负责选择目录，Agent 负责完成安装并报告结果。

### 2. 在当前项目中启用

进入要开发的项目后，对 Agent 说：

```text
请使用 solo-company-harness 初始化当前项目的项目记忆和宿主规则。
先检查已有的 CLAUDE.md、AGENTS.md、README、docs 和项目配置，保留用户内容，
只补充缺失的 SSOT 文件和 Harness 管理区块。完成后告诉我你读取和创建了哪些文件。
```

Claude Code 通常使用 `CLAUDE.md`；Codex、OpenCode 和通用宿主通常使用 `AGENTS.md`。如果宿主有自己的项目规则文件，Agent 应遵循宿主当前优先级。

### 3. 直接开始一次任务

不需要手动运行 Harness 脚本。直接描述目标，并明确要求 Agent 使用这个 Skill：

```text
请使用 solo-company-harness 完成这个任务：为当前产品增加真实文件上传。

开始前先读取相关项目 SSOT 和现有实现，判断风险与 operating mode。
如果是 delivery 或 high-assurance，请先给我交付合同、验收标准、反作弊规则、
验证计划和回滚方案，等我确认后再修改生产代码。
```

### 4. 让 Agent 管理交付过程

让 Agent 自己执行脚本、记录状态和选择模式，用户只需要在关键决策点确认：

```text
请继续按 solo-company-harness 的 Intent -> Context -> Contract -> Execute ->
Verify -> Release -> Observe -> Distill 流程推进。

每次改变范围、方案或风险等级时先停下来告诉我；不要把局部测试、fixture、mock、
写死返回值或“页面能打开”当成真实交付证据。
```

任务完成后：

```text
请使用 solo-company-harness 做收尾：运行相关测试和真实路径验证，记录实际证据等级，
生成必要的 case log，说明发布模式、残余风险、阻塞路径和可复用经验。
不要为了让任务显示 completed 而跳过证据门禁。
```

Agent 会在项目中维护 `.harness/runs/`、交付合同、验证日志和必要的 case log。用户不需要手动创建这些文件。

### 脚本接口（维护者和自动化集成）

Harness 自带的 Python 脚本是 Agent 的执行接口，不是普通用户必须学习的 CLI。需要在 CI、批处理或没有 Agent 的环境中集成时，再查看 `scripts/` 和 [PLATFORM.md](./PLATFORM.md)。

## 目录结构

```text
SKILL.md                         Agent 核心工作规则
agents/openai.yaml               Codex 可选 UI 元信息
references/approved-experience.md 跨项目批准经验
references/                         按模式按需加载的详细规则
  operating-modes.md
  delivery-contract.md
  evidence-levels.md
  platform-adapters.md
scripts/                         可执行的 Harness 工具
  init_ssot.py                   初始化项目事实源
  init_agents.py                 生成项目级 AGENTS.md
  start_run.py                   创建一次可追踪任务
  contract.py                    创建、验证和批准交付合同
  resolve_mode.py                判断模块是否准备好进入实现
  record_evidence.py             记录 L0-L4 验证证据
  update_run.py                  记录决策、变更和观察
  detect_risk.py                 识别任务风险
  detect_tests.py                识别验证命令
  run_checks.py                  执行并记录验证
  finish_run.py                  收尾并生成 case log
  update_playbook.py             沉淀重复经验
  propose_skill_update.py        提出 Skill 改进
  promote_experience.py          晋升批准的跨项目经验
  host_adapters.py               宿主目录和项目指令适配
  install_host.py                安装到宿主默认或自定义目录
```

## 设计原则

- 项目事实放在项目 SSOT，不放在 Skill 全局规则里。
- 每次任务都保留决策、变更和验证证据。
- 低风险任务保持轻量，中高风险任务必须明确合同、证据和回滚边界。
- 真实用户路径优先于局部测试、模拟 Provider 和漂亮截图。
- 不用一次运行的偶然经验静默改变跨项目规则。
- 用户始终是最终负责人，Agent 是可替换的临时团队。

## 适用范围和限制

这个 Skill 适合软件项目的规划、开发、调试、测试、发布和复盘。它不会自动替你决定产品方向，也不会保证 Agent 不犯错。它做的是把目标、边界、证据和失败状态显式化，让错误更早暴露、更容易回滚。

生产环境仍然需要你自己的密钥管理、权限控制、备份、监控和发布审批。不要把 Skill 的流程记录当成安全控制本身。

核心状态、合同、证据格式和执行脚本保持平台中立。仓库提供 Codex、Claude Code、OpenCode 和通用 Agent Skills 目录适配；`agents/openai.yaml` 只是 Codex 可选 UI 元信息。第三方宿主仍需按自己的发现规则做一次 smoke 测试。

项目仍处于早期维护阶段，长期兼容性和第三方集成覆盖范围尚未承诺。请查看 [`PLATFORM.md`](./PLATFORM.md) 和 [`CHANGELOG.md`](./CHANGELOG.md)，并在关键发布前自行运行测试和真实链路验证。

## 来源与致谢

本项目独立实现，遵循 [Agent Skills 开放标准](https://agentskills.io)，并提供 Codex、Claude Code、OpenCode 等宿主的目录适配。README 的公开项目组织方式参考了 OpenAI Skills、Anthropic Skills 和其他开源 Agent Skill 项目的通用做法，但本仓库不捆绑第三方 Skill 的代码或指令文本。

如果未来引入或修改第三方内容，应保留原作者、原始仓库、原许可证和修改说明，并记录在 [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md) 中。

## 贡献

欢迎提交 Issue、Pull Request 和可复用的交付经验。

适合贡献的内容包括：

- 不依赖特定项目的 Harness 工作流；
- 针对真实失败模式的验证脚本；
- 可复用的项目 playbook；
- 对合同、风险门禁、反作弊验收和经验沉淀的改进。

提交前请确认：

- 不包含 API Key、Secret、个人路径或项目私有数据；
- 修改有清晰的使用场景、边界和验证方式；
- README、SKILL.md 和脚本行为保持一致；
- 如果修改了第三方内容，已补充来源和许可证信息。

## 许可证

本项目以 [MIT License](./LICENSE) 开源。你可以自由使用、修改、复制和再分发，但请保留许可证和版权声明。

由 [ZIFeIYUuuuuuu](https://github.com/ZIFeIYUuuuuuu) 维护。

---

## English

Solo Company Harness is an Agent Skill for solo founders and small teams using AI Coding. It is a lightweight delivery control layer with project memory, progressive operating modes, delivery contracts, anti-gaming acceptance criteria, verification evidence, release modes, and reusable learning.

Quick install:

```text
Install and enable this Agent Skill:
https://github.com/ZIFeIYUuuuuuu/solo-company-harness

I am using <Codex / Claude Code / OpenCode / another Agent Skills host>.
Use the host's current Skill discovery rules and confirm that SKILL.md can be loaded.
```

Then use it in the Agent conversation:

```text
Use the solo-company-harness skill for this project.
```

Read [SKILL.md](./SKILL.md) for the full operating rules. See [PLATFORM.md](./PLATFORM.md) for host limitations and [CHANGELOG.md](./CHANGELOG.md) for version history. This project is released under the [MIT License](./LICENSE).
