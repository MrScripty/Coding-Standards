# Plan: Standards Engine Standards Recovery

**Plan status:** `Blocked`

**Current phase:** standards-recovery resume admission

**Next slice:** admit the compacted recovery-resume boundary

**Acceptance status:** `partial`

**Planning comparison baseline:** commit
`3439aae9540786d9734431e633ea5b62afb50592`, tree
`0ff4af77ebe5056c9478f04bf65dd87141f573d8`

**Historical A1 reproduction boundary:** commit
`2359a98740b6035a0414bfaf5427ceaa1301a1c8`, tree
`97c850ab718287007c1e1daac538f40869f71a1d`

**Accepted policy-impact prerequisite:** candidate commit
`7bc8bd070f882eb9779dc678139777d05a6ce7c7`, tree
`35a22f824f7ed5f50347032b956b2108fc073f77`; acceptance-report
commit `bf9f3d86c8109532f7846ce2f6e547ab155bb200`, tree
`5a877289fbc388e9bacfc77746a42ef85d0fb363`; acceptance-transition
commit `dd571976068916f2f95d89c55c8824a20b92acb2`, tree
`15e482de3334137f14a55bf2c22e2560188dd647`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

**Semantic-impact inventory:**
[semantic-impact-inventory.md](reports/semantic-impact-inventory.md)

**Consumer dispositions:**
[standards-recovery-consumer-dispositions.md](reports/standards-recovery-consumer-dispositions.md)

**Authoring brief:**
[Standards Recovery And Standards Engine A1b Redesign](../standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md)

**Accepted recovery-enabling prerequisite:**
[Policy-Impact Authority V2](../standards-engine-policy-impact-authority-v2/plan.md)

## Objective

Recover the standards authority needed to govern a later Standards Engine A1b
redesign. The accepted result makes evidence-oracle boundaries,
generated-contract semantic conformance, immutable authority closure,
implementation-versus-dependency decisions, systemic-finding re-planning, and
Generated Contract routing explicit and mutually consistent across normative
policy, semantic metadata, agent entry points, fixtures, and executable
verification.

The six policy families and their projections exist in the current tree. The
remaining work is to reconcile that implemented authority against the accepted
policy-impact v2 prerequisite, freeze the final recovery authority, prove exact
coverage and consumer dispositions, and obtain independent exact-tree
acceptance. Broader A1b implementation and all A2 work remain excluded.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| SR-A1 | Each defect family has normative policy with stable policy-unit identity, exact locator, and non-overlapping ownership. | `contract` | `not-applicable` | `automated` | `pending` | Pending final locator and ownership verification |
| SR-A2 | Router prose and executable projection select the Generated Contract profile and required owners, preserve conditional IPC and Language Binding selection, and expose unresolved facts. | `user-workflow` | `not-applicable` | `automated` | `pending` | Pending final Router fixture verification |
| SR-A3 | Prior and current semantic graphs are compared, every changed policy unit has valid coverage, and no empty impact result is accepted without a certificate. | `integration` | `not-applicable` | `automated` | `pending` | Pending final graph and coverage reconciliation |
| SR-A4 | Every selected consumer has exactly one current non-blocked disposition supported by reviewed evidence. | `integration` | `not-applicable` | `manual` | `pending` | Pending final independent disposition review |
| SR-A5 | Normative policy, policy units, relationships, prompts, templates, fixtures, suites, and verifier support agree at one exact tree. | `integration` | `not-applicable` | `automated` | `pending` | Pending coordinated projection verification |
| SR-A6 | Generated freshness and generated semantic correctness are proved separately. | `contract` | `not-applicable` | `automated` | `pending` | Pending final evidence-lane verification |
| SR-A7 | Recovery distinguishes local agreement from external conformance, records the accepted A1 nonconformance, and assigns runtime correction to A1b. | `contract` | `not-applicable` | `automated` | `pending` | Pending final known-nonconformance classification evidence |
| SR-A8 | Schema instance equality and content-identity canonicalization are exercised as separate contracts. | `contract` | `not-applicable` | `automated` | `pending` | Pending final equality-domain fixture verification |
| SR-A9 | Immutable authority reconstruction uses a fresh public process and remains unaffected by post-capture source mutation. | `system` | `not-applicable` | `automated` | `pending` | Pending final cold-process evidence |
| SR-A10 | Every negative fixture satisfies unrelated preconditions and proves its exact intended diagnostic. | `focused` | `not-applicable` | `automated` | `pending` | Pending final isolated-negative evidence |
| SR-A11 | Generated closure, public result, semantic-version identity, and JSON Schema equality repair families are reproduced without changing A1 runtime behavior. | `contract` | `not-applicable` | `automated` | `satisfied` | [Historical reproductions](reports/historical-a1-repair-reproductions.md) and [equality reproduction](reports/json-schema-instance-equality-reproduction.md) |
| SR-A12 | Immutable reads and cold reconstruction are reproduced through their public process boundaries without changing A1 runtime behavior. | `system` | `not-applicable` | `automated` | `satisfied` | [Historical reproductions](reports/historical-a1-repair-reproductions.md) |
| SR-A13 | Historical acceptance-oracle failures are reproduced at their intended failure points without changing A1 runtime behavior. | `focused` | `not-applicable` | `automated` | `satisfied` | [Exact negative diagnostics](reports/historical-a1-repair-reproductions.md#exact-negative-diagnostics) |
| SR-A14 | One clean candidate commit and tree pass focused recovery checks and all registered repository verification. | `integration` | `not-applicable` | `automated` | `pending` | Pending exact-tree candidate report |
| SR-A15 | An independent reviewer accepts the exact candidate, final coverage, dispositions, and objective claims with no blocked consumer. | `integration` | `not-applicable` | `manual` | `pending` | Pending independent recovery acceptance |

## Scope

### In Scope

- Final reconciliation of the six implemented policy families and their
  Router, profile, policy-unit, relationship, prompt, template, fixture,
  suite, and verifier projections.
- Re-resolution of the admitted mapped-consumer closure at the exact resume
  tree.
- Prior/current graph comparison, final consumer dispositions, post-freeze
  coverage validation, and exact-tree acceptance.
- Durable evidence separating freshness, semantics, external conformance,
  identity equality, cold reconstruction, and intended negative diagnostics.
- The recorded Draft 2020-12 reference-only Licensing decision.

### Out Of Scope

- A1b runtime redesign, equality correction, validator selection, contract
  compiler, immutable authority repository, or result-algebra changes.
- A2 controlled authoring and Plan C external baselines.
- Production changes under `tools/standards_engine/`,
  `tools/standards_analysis/`, `tools/standards_applicability/`,
  `tools/standards_policy_impact/`, `tools/standards_metadata/`,
  `tools/standards_graph/`, or `tools/graph_engine/`.
- Further edits to package tests already corrected and accepted by the
  policy-impact prerequisite.
- New dependencies, copied external corpora, JSON-specific recovery machinery,
  or correction of the recorded A1 JSON Schema nonconformance.
- New or extended Bash verification. The retained plan-structure and
  plan-fixture checkers remain migration-owned and unchanged.

## Constraints And Assumptions

- No implementation invocation is available while this plan is `Blocked`.
- The accepted prerequisite is imported as evidence and current authority; it
  is not reimplemented by this plan.
- Policy authority and every required projection remain one coordinated
  outcome. Prose-only or executable-only acceptance is invalid.
- Every authoritative metadata change requires a new prior/current impact
  comparison. Empty impact remains unresolved without valid independent
  coverage.
- Attestation decisions occur only after policy, relationships, suites,
  registrations, and other horizon-affecting inputs are frozen.
- Existing attestations may be reused only when their exact requirement,
  evidence, provider, and authorization identities remain valid. Otherwise
  the owning attestation is renewed through the same coverage Interface.
- Suite registrations are resolved through the canonical suite registry;
  expanded suite paths are evidence, not copied planning authority.
- A2 remains inactive through recovery and through subsequent A1b planning,
  implementation, migration, and independent acceptance.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Standards recovery precedes A1b planning; independently accepted A1b precedes any A2 review. | This plan | [A1b authoring brief](../standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md) | Direct A1-to-A2 progression |
| The existing recovery plan remains the sole plan authority and exposes only current work; the ledger and reports own historical admissions and rejected protocols. | Planning | `workflows/planning.md` current-state rule | The accumulated multi-protocol active plan |
| Policy-impact v2 is the accepted shared relationship authority and public v10 prerequisite. | Accepted prerequisite | [Prerequisite acceptance](../standards-engine-policy-impact-authority-v2/reports/prerequisite-acceptance.md) | Router-only dispatch and split compatibility authority |
| The six policy families remain one coordinated standards outcome. | This plan | [Semantic-impact inventory](reports/semantic-impact-inventory.md) | Local defect-by-defect acceptance |
| Stable heading-scoped policy units own changed normative meaning; declarations are source-owned. | Normative owners and metadata | Current policy-unit and relationship registries | Module-level or inferred semantic authority |
| Schema instance equality, domain equality, and content identity remain separate domains. | Contracts | [Equality reproduction](reports/json-schema-instance-equality-reproduction.md) | Identity canonicalization as schema equality |
| Freshness, local agreement, semantic conformance, mutation detection, and cold replay are separate evidence claims. | Verification | Historical reproductions and registered suites | One undifferentiated green oracle |
| Recovery enforcement uses registered Python declarative suites and no new Bash behavior. | Verification-engine migration | Suite registry and current migration constraints | Temporary Bash enforcement |
| Current impact is an evidence input, not completeness proof; coverage and per-consumer dispositions remain mandatory. | Planning and analysis | Accepted coverage model | Empty graph result as no-impact proof |
| Draft 2020-12 is reference authority only; no third-party content is incorporated. | Licensing | [Licensing decision](reports/draft-2020-12-reference-licensing-decision.md) | Treating reference selection as unreviewed |

## Semantic Impact And Consumer Closure

The pre-policy inventory and scope audit remain membership authority:

- [semantic-impact-inventory.md](reports/semantic-impact-inventory.md) owns the
  policy-family mapping and proposed consumer classes.
- [pre-policy-scope-audit.md](reports/pre-policy-scope-audit.md) owns the 36
  selected suite IDs and exact non-registry consumer list.
- [standards-recovery-consumer-dispositions.md](reports/standards-recovery-consumer-dispositions.md)
  owns current consumer dispositions.

At the resume candidate tree:

- `W` is the exact remaining milestone write set.
- `S` is every suite definition and registered input mechanically resolved
  from the 36 audit-selected suite IDs through the canonical suite registry.
- `E` is the audit's exact non-registry consumer list and contains no wildcard.
- `R = (S union E) - W` is the protected mapped-consumer closure.

Admission must prove every selected suite resolves, every path in `E` resolves,
`W intersect R` is empty, and mapped consumers equal `W union R`. `R` protects
mutation and requires disposition review; it does not restrict incidental
reading. A semantic change required outside `W` is a re-plan trigger.

For every policy unit, final verification must resolve the exact locator,
compare prior and current relationships, retain every selected consumer, audit
the independent horizon, assign one non-blocked disposition, and recompile
coverage after any authority change.

## Required Projection Matrix

| Projection | Required agreement |
| --- | --- |
| Router | `STANDARDS-ROUTER.md` and the typed Router projection agree on Generated Contract applicability, owner closure, conditional IPC/Language Binding selection, and unresolved facts. |
| Normative policy and profile | Six policy families have one owner each; the Generated Contract profile specializes application mechanics without replacing Contracts, Verification, Build, or Dependencies. |
| Policy units and graph | Every changed heading has one stable unit and exact locator; every relationship is source-owned and compiled through policy-impact v2. |
| Prompts and template | Planning and implementation consume routed authority, systemic-finding replanning, independent evidence, and complete dispositions without copying a standards list. |
| Fixtures and suites | Registered Python suites cover applicability, non-applicability, unknowns, semantic mutations, cold reconstruction, and exact negative diagnostics. |
| Verification | Freshness, semantics, coverage, consumer disposition, and complete repository checks remain distinct oracles. |

## Recovery Resume Admission

The accepted prerequisite does not itself resume this blocked plan. Resume uses
one current protocol:

1. Commit one blocked governance candidate derived from prerequisite transition
   `dd571976068916f2f95d89c55c8824a20b92acb2`. The candidate may change only:
   - this `plan.md`;
   - `execution-ledger.md`;
   - `issues.md`; and
   - the accepted prerequisite `plan.md` to reconcile completed tasks and its
     stale blocker narration.
2. An independent reviewer authors only
   `reports/standards-recovery-resume-admission.md`, binding the exact candidate
   commit/tree and confirming the compact current authority, exact remaining
   write sets, resolved prerequisite, protected consumer closure, evidence
   lanes, and A1b/A2 exclusions. The report references retained migration
   verification through this plan rather than adding new checker-name inputs.
3. If accepted, a direct-child mechanical transition changes only this plan,
   the ledger, and SESR-009/SESR-030 lifecycle fields in `issues.md`. It records
   candidate and report commit/tree identities, moves the plan and Milestone 1
   from `Blocked` to `Planned`, and names recovery-resume `start` as the sole
   next operation.
4. `start` is valid only while that transition is current `HEAD` with a clean
   worktree. It records the transition commit/tree, moves the plan and
   Milestone 1 to `Active`, and authorizes only the Milestone 1 `W` below.

Any other candidate, report, transition, parent, or generated-artifact delta
invalidates admission.

## Milestones

### Milestone 0: Historical Reproduction And Scope Audit

**Goal:** Preserve the exact accepted-A1 reproductions and the independently
admitted pre-policy consumer map.

**Evidence:** [Historical reproductions](reports/historical-a1-repair-reproductions.md),
[equality reproduction](reports/json-schema-instance-equality-reproduction.md),
and [pre-policy scope audit](reports/pre-policy-scope-audit.md).

**Acceptance gate:** SR-A11 through SR-A13 are satisfied; the audit is planning
evidence rather than final coverage; checker and generated-evidence closure is
fresh.

**Status:** `Accepted`

### Milestone 1: Reconcile And Freeze Implemented Standards Authority

**Goal:** Revalidate the implemented six-policy authority and its complete
consumer closure against the accepted policy-impact v2 tree, then freeze the
authority for final coverage.

**Allowed write set (`W`):**

- `docs/plans/standards-engine-standards-recovery/plan.md`
- `docs/plans/standards-engine-standards-recovery/execution-ledger.md`
- `docs/plans/standards-engine-standards-recovery/issues.md`
- `docs/plans/standards-engine-standards-recovery/reports/semantic-impact-inventory.md`
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-consumer-dispositions.md`

All normative policy, Router/profile metadata, policy-unit and relationship
declarations, prompts, templates, fixtures, suite registrations, generated
artifacts, package code, and package tests are frozen outside `W`. The accepted
prerequisite is evidence, not additional recovery write authority.

**Completed implementation:**

- [x] Add the six normative policy families and the Generated Contract profile.
- [x] Register canonical profile membership, Router fact/rule semantics,
  stable policy units, and source-owned relationships.
- [x] Project the policy into planning/implementation prompts and the plan
  template.
- [x] Add positive, negative, non-applicable, unresolved, mutation, and
  cold-process fixtures and register six Python declarative suites.
- [x] Replace live-authority fact, rule, edge, consumer, navigation, and
  analysis cardinality oracles with semantic identity and cause-set assertions.
- [x] Regenerate admitted migration evidence without modifying checker or
  generator behavior.
- [x] Replace split policy-impact validity/projection authority and obtain
  independent acceptance of policy-impact v2 and public A1 v10.

**Remaining tasks:**

- [ ] Re-resolve `S` and verify `E` at the exact resume candidate; derive
  `R = (S union E) - W` and prove exact path resolution and disjointness.
- [ ] Compare the planning baseline, pre-prerequisite recovery authority, and
  current compiled graph. Explain every retained, added, removed, or corrected
  relationship without using mutable totals.
- [ ] Revalidate every policy-unit locator, Router/profile projection, suite
  registration, generated artifact, and current consumer disposition.
- [ ] Prove no consumer is blocked and no protected consumer requires mutation.
- [ ] Run focused recovery verification and the complete repository checkpoint,
  then record the exact frozen M1 tree.

**Acceptance gate:** The six policy families and projections agree; `W/S/E/R`
is exact; graph changes are fully dispositioned; generated evidence is fresh;
all selected consumers have non-blocked dispositions; no frozen authority path
requires modification; and the complete checkpoint passes.

**Status:** `Blocked` pending recovery-resume admission

### Milestone 2: Final Coverage And Exact-Tree Acceptance

**Goal:** Compile final coverage from the frozen authority and obtain
independent acceptance of one clean standards-recovery tree.

**Allowed write set:**

- `evaluation/standards-effectiveness/policy-coverage/attestations/router.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.verification.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.contracts.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.architecture.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.dependencies.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.planning.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/profile.boundary.generated-contract.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.commit.toml`
- `docs/plans/standards-engine-standards-recovery/plan.md`
- `docs/plans/standards-engine-standards-recovery/execution-ledger.md`
- `docs/plans/standards-engine-standards-recovery/issues.md`
- `docs/plans/standards-engine-standards-recovery/reports/semantic-impact-inventory.md`
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-consumer-dispositions.md`
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-coverage.md` (new)
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-candidate.md` (new)
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-acceptance.md` (new, independent reviewer owned)

The eight attestation files are the current policy-impact v2 owner-local
authority closure. They may change only when exact final requirements cannot
reuse a dependency-valid current attestation. No attestation source, horizon,
policy, relationship, suite, runtime, generated contract, or package test is
writable in this milestone.

**Tasks:**

- [ ] Freeze every horizon-affecting input before compiling final requirements.
- [ ] Derive current subjects and requirements mechanically. Revalidate exact
  reusable attestations and renew only requirements whose identity or accepted
  evidence/authorization contract changed.
- [ ] Generate certificates and prove exact active-policy-unit, requirement,
  attestation, and certificate subject equality with no stale, duplicate,
  extra, missing, or blocked subject.
- [ ] Prove every selected consumer has exactly one current non-blocked
  disposition and no independent-horizon member is missing.
- [ ] Run all focused package tests, contract generation/validation, registered
  declarative suites, complete Python checkpoint, retained migration checks,
  plan/link/generated checks, Ruff, and `git diff --check` from one clean tree.
- [ ] Record one candidate commit/tree without claiming acceptance.
- [ ] Obtain independent Standards and specification review of that exact tree.
- [ ] Mark this recovery `Accepted` only after SR-A1 through SR-A15 are
  satisfied. Only then may a separate A1b plan and superseding ADR be authored.

**Acceptance gate:** Exact coverage subject equality, complete non-blocked
consumer dispositions, a green complete checkpoint, and one independent report
accepting the exact clean candidate tree.

**Status:** `Blocked` by Milestone 1

## Verification Strategy

| Claim | Required oracle | Explicit non-proof |
| --- | --- | --- |
| Generated freshness | Regenerate and compare exact output. | Fresh output does not prove semantics. |
| Generated semantics | Normative authority plus independent behavioral or mutation evidence. | Two local implementations agreeing proves only consistency. |
| Schema instance equality | Selected Draft 2020-12 data-model and codepoint equality. | Identity canonicalization and Python equality are non-proofs. |
| Content identity | Domain-separated canonical serialization fixtures. | Schema equality does not define identity normalization. |
| Immutable authority closure | Persist, destroy process state, reconstruct through public adapters, and compare after source mutation. | In-memory reuse or private cache injection is not cold reconstruction. |
| Negative fixture | Otherwise-valid fixture plus exact intended diagnostic. | Generic failure or substring matching is insufficient. |
| Coverage completeness | Independent horizon plus exact requirement/attestation/certificate subject equality. | Existing graph edges or an empty impact result are insufficient. |
| Mutable corpus behavior | Named semantic identities, set equality, and cause preservation. | Repository-wide relationship, rule, standards, or test totals are insufficient. |

## Blockers

- The accepted prerequisite does not authorize recovery resume. This plan and
  Milestone 1 remain blocked until the exact governance candidate receives an
  independent resume-admission report and its authorized transition is current.
- The recorded A1 JSON Schema equality nonconformance remains intentionally
  unresolved for A1b.
- A1b planning and all A2 work remain blocked by independent acceptance of this
  recovery; A2 remains blocked further by independent A1b acceptance.

## Re-Plan Triggers

- Resume admission rejects or changes scope, closure, evidence lanes, write
  sets, sequence, or exact parent-chain requirements.
- The candidate/report/transition/start identities or parent chain differ from
  the resume protocol, or a governance operation changes another path.
- `S` or `E` cannot be resolved exactly, contains a wildcard, overlaps `W`
  after derivation, or selects an undispositioned consumer.
- A frozen normative, metadata, relationship, fixture, suite, generated,
  runtime, or test path requires modification.
- Graph comparison reveals unexplained topology or semantic drift, or another
  duplicated policy-impact validity/projection authority appears.
- Generated evidence becomes stale or changes checker/generator behavior,
  unrelated records, dependency fields, or component topology.
- A policy locator is missing, duplicated, overlapping, or no longer denotes
  one coherent meaning.
- A changed authority or horizon input invalidates reviewed impact or coverage.
- An empty impact result lacks independent coverage, or the horizon cannot
  discover consumers omitted from graph and catalog authority.
- A negative fixture misses its intended diagnostic or a lower-fidelity oracle
  is proposed for a higher-fidelity claim.
- A finding reveals another member of the same invariant family outside the
  audited closure.
- A new dependency, external corpus, runtime change, broader A1b design, or A2
  requirement becomes necessary.
- Any milestone misses its gate or an independent reviewer cannot accept the
  exact tree.

## Concurrent Work

No concurrent implementation is admitted. Normative authority, Router and
semantic metadata, coverage, active planning, and candidate integration remain
serial owner writes. Independent reviewers inspect immutable trees and author
only the report named by the applicable admission or acceptance protocol.

## Subsequent Broader A1b Planning Gate

Only after Milestone 2 is independently accepted may the broader A1b plan and
superseding ADR be created. That planning must evaluate a mature Draft 2020-12
validator, define equality domains separately, design the contract compiler and
immutable authority repository, inventory public consumers and persisted A1
state, and decide coordinated contract/handle migration. It authorizes no A1b
implementation. A2 remains inactive until A1b implementation and migration are
independently accepted.

## Final Acceptance

- Acceptance status: `partial`
- Deferred follow-ups: A1b planning and ADR remain gated by this recovery; A2
  remains gated by independently accepted A1b; Plan C remains inactive.
- Final status: `Blocked`
