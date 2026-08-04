# Frontend Standards Migration Index

This file is a non-normative compatibility index. It defines no frontend,
accessibility, tooling, lifecycle, or verification policy and selects no
framework, platform, mechanism, or fallback.

Use the canonical owner for the concern being decided:

| Concern | Canonical owner |
| --- | --- |
| Frontend applicability, projection, rendering, synchronization, interaction adaptation, lifecycle specialization, and user-observable evidence | [Frontend](profiles/applications/frontend.md) |
| User-access outcomes, modalities, semantics, interaction equivalence, and accessibility claims | [Accessibility](topics/accessibility.md) |
| Generic asynchronous work, cancellation, cleanup, and stale-result exclusion | [Concurrency](topics/concurrency.md) |
| TypeScript project boundaries, compiler compatibility, and static-analysis selection | [TypeScript](profiles/languages/typescript.md) |
| TypeScript asynchronous invocation mechanisms | [TypeScript Async](profiles/languages/typescript/async.md) |
| Lint purpose, rules, severity, scope, and orchestration | [Tooling](workflows/tooling.md) |
| Evidence kind, environment, execution, and acceptance meaning | [Verification](workflows/verification.md) |
| Illustrative frontend mechanisms | [Frontend recipes](reference/recipes/frontend.md) |
| Illustrative lint mechanisms | [Tooling recipes](reference/recipes/tooling.md) |

Repository plans and accepted contracts select the applicable owners and
evidence. Implementation and completion follow those authorities, never this
index.
