# Findings and dispositions

- S1 — Locally fixed and tested, contracts/projection: generic JSON walking treats property maps and
  literal $ref-shaped data as schemas. Cover compiler, selector, MCP and CLI consumers.
- S2 — Locally fixed and tested, contracts/Python projection: a $ref-named field is admitted but its
  generated Python is syntactically invalid. Preserve the wire name and escape only
  names that cannot be represented safely; retain collision rejection.
- S3 — Qualification, integration owner: this runtime is Python 3.13.5 rather than
  locked Python 3.11/3.12. A Python 3.12 download failed due to unavailable network
  DNS. Keep the lock unchanged and require supported CI evidence for acceptance.
  Integration follow-up (2026-09-26): local Python 3.12.3 with locked dependency
  versions passes the contracts supported-environment check without a skip; see
  verification.md for local qualification. CI acceptance remains separate.
- S4 — Retirement, host operator: compatibility remains required pending actual
  client/version qualification. Record each supported client/version and deployment
  result (or explicit support retirement), including model-visible nested fields.
  Then update launch configurations and remove the workaround, flag and obsolete
  tests atomically. No store migration is involved. Native reference-only output can
  be chosen at that cutover; do not add a third mode or infer support from client names.
- S5 — Acceptance, integration owner: independent review and actual configured-client
  qualification are separate from local implementation tests. Retain these open
  until evidence is recorded; protocol tests alone do not prove model behavior.
