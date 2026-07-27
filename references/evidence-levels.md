# Evidence Levels

Load this reference for delivery verification or when an external system is involved.

```text
L0 static      static inspection or configuration review
L1 local       local tests, build, lint, typecheck, or smoke
L2 integration integration tests or simulated external services
L3 real-path   real third-party service and real user path
L4 dogfood     owner or seed user uses the feature realistically
```

`run_checks.py` records successful local commands as L1. Use `record_evidence.py` for
evidence that cannot be inferred from a local command:

```bash
python <skill-dir>/scripts/record_evidence.py <project-root> \
  --level 3 \
  --source real-path \
  --summary "<what actually happened>" \
  --artifact "<log, URL, screenshot, or case log>"
```

The receipt is an auditable claim, not an automatic verifier. A real integration
requires a project-owned recipe that knows the sandbox, credentials, inputs, cleanup,
expected result, and artifacts. Keep those recipes in the project, not in this global
Skill.

Do not call L1 evidence proof of a real callback, payment, production configuration,
or user-visible result. If the required level is unavailable, finish the run as
`blocked` or record the missing level as residual risk rather than lowering the claim.
