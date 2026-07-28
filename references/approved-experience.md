# Approved Experience

User-approved cross-project lessons live here.

Load this file when a task resembles a previously approved pattern, failure mode, verification rule, release rule, or operating convention.

Do not add project-specific facts here. Keep project facts in that project's SSOT.

## Entries

### 2026-07-02 - Approved Lesson

Approved by: user
Scope: Cross-project delivery for auth, sync, multi-runtime apps, and external integrations
Source run: 20260702-004014-distill-project-development-lessons

Lessons:
- Validate the real user path separately from developer diagnostics; do not treat a working script, visible browser, fixture, or operator workflow as proof that the product flow works.
- For high-risk flows such as auth, sync, payments, migrations, and data publishing, require a repeatable E2E path plus explicit failure-state handling before claiming completion.
- After adding or changing client app pages, verify generated runtime assets and platform constraints, not only TypeScript or framework build success.
- Keep environment configuration aligned across .env examples, Docker/compose files, launcher scripts, documentation, and test commands; configuration drift is a product bug.
- Classify errors into actionable states for the UI, such as auth required, retry later, service unavailable, invalid credentials, and data not publishable, instead of surfacing raw backend errors.
- For data sync products, save raw evidence first, write normalized data transactionally, publish only complete successful batches, and never let failed syncs overwrite previously visible good data.
- Repeated portal-flow regressions should become a delivery checklist: verify user-owned mini-program auth, fixture E2E publication, mobile runtime safety, generated page assets, and aligned local environment config before claiming completion.

Evidence:
- docs/playbooks/mini-program-portal-sync-delivery.md
- docs/case-log/2026-07-02-distill-project-development-lessons.md
- C:\Users\Administrator\Desktop\信息门户\docs\case-log\2026-07-02-distill-project-development-lessons.md

- SKILL.md update requested: no. Keep this as reference experience.
### 2026-07-23 - Approved Lesson

Approved by: user
Scope: Cross-project delivery, external integrations, user constraint enforcement
Source run: manual

Lessons:
- 先验证真实用户路径，再扩展审计、重试和高级质量能力；局部测试、构建成功或模拟 Provider 不能替代真实端到端 smoke。
- 外部服务配置是系统代码的一部分，必须版本化并在本地、测试、Docker、远端进程、反向代理和文档之间保持一致；配置漂移应被当作产品缺陷。
- 一个生产能力只保留一个 canonical path；重复网关、重复存储和重复 secret 会造成配置漂移与责任不清。
- 先冻结可验证的 MVP 闭环，再增加多窗口、replay、审计、策略和质量优化；传输可用性必须先于模型语义质量。
- 当用户请求违反已批准的安全、数据完整性、验收或部署约束时，系统必须先提醒并分类为硬约束、可协商约束或建议约束；硬约束阻断，可协商约束提出修正并记录，建议约束只提示。
- 对可逆且仍在已批准合同范围内的请求，告知用户后可自动采用修正；任何改变合同、权限、安全边界或数据保留策略的修改必须取得用户明确批准，不能静默改变。
- 用户坚持不能覆盖安全、隐私、密钥保护、数据不可变性、真实验收和禁止伪造结果等硬约束；可接受的例外必须记录为显式项目决策，不得变成默认规则。

Evidence:
- docs/case-log/2026-07-23-phase-2b-real-visual-inventory-live-acceptance.md
- docs/playbooks/real-path-media-delivery-gates.md
- docs/case-log/2026-07-22-distill-cross-project-delivery-lesson.md

- SKILL.md update requested: yes. Review and patch the core workflow if this changes operating behavior.
