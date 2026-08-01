# Testing Standards Migration Index

This file is a non-normative compatibility index. It defines no testing policy,
acceptance checklist, tool default, or completion criterion.

Use the canonical owner for the concern being decided:

| Concern | Canonical owner |
| --- | --- |
| Acceptance claims, evidence kinds, environments, test design, placement, coverage, test data, async evidence, supporting gates, and diagnosis | [Verification](workflows/verification.md) |
| Concurrent test resources and asynchronous lifecycle obligations | [Concurrency](topics/concurrency.md) |
| Native and host binding evidence | [Language Bindings](profiles/boundaries/language-bindings.md) |
| Replay, recovery, resumption, and idempotency evidence | [Resilience](topics/resilience.md) |
| Persisted contract artifact validation | [Contracts](topics/contracts.md) |
| Frontend interaction and browser evidence | [Frontend](profiles/applications/frontend.md) |
| Performance workloads, budgets, and benchmark evidence | [Performance](topics/performance.md) |
| Language-specific syntax and commands | [Profiles](profiles/README.md) |

Repository plans select the required claims and evidence from those owners.
Completion follows the accepted plan and observed results, never this index.
