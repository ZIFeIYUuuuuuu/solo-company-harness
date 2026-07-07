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
