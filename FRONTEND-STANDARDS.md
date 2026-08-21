# Frontend Standards Migration Index

This former standards entrypoint is non-normative navigation. It owns no
frontend, accessibility, tooling, lifecycle, or verification policy,
applicability decision, default, example, or fallback authority.

If a route is missing, conflicting, or inapplicable, return the Router's typed
diagnostic instead of using prior wording from this file.

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
