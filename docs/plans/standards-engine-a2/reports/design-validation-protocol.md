# A2 Milestone 0 Design-Validation Protocol

**Status:** `admitted for prototype execution`

## Purpose

This protocol decides whether an A2 design idea is sufficiently validated to
enter production planning. It does not establish production correctness,
platform support, objective acceptance, or authority to change canonical
Engine code. A failed, unavailable, or inadequately measured material claim
blocks or rejects the design; review cannot waive it.

## Claim Registration

Before execution, each prototype or minimum viable test records:

1. one design question and the competing outcomes;
2. the representative workflow, state transition, workload, or failure;
3. an effectiveness criterion observable by the caller;
4. an efficiency metric with an owned baseline, comparison, or product budget
   and variability policy;
5. correctness invariants and negative cases;
6. the deciding oracle and its authority boundary;
7. the executable Router facts and selected current standards;
8. environment, inputs, reproduction command, and unsupported boundaries;
9. the exact A1c preservation rows touched; and
10. a predeclared `pass`, `revise`, `reject`, or typed `unavailable` threshold.

Changing the question, oracle, workload, material state model, or threshold
after seeing results creates a new claim registration and requires a re-run.

## Four Independent Dimensions

| Dimension | Admission rule | Insufficient substitute |
| --- | --- | --- |
| Effectiveness | The representative caller completes the named job using only allowed knowledge and every advertised next action is derivable from returned state. | The harness executes without showing that the caller workflow works. |
| Efficiency | Record public call count, caller-supplied field count, durable bytes, scratch bytes, and wall time where applicable. A candidate passes only if it is not strictly dominated by a correctness-equivalent candidate and does not violate A1c's no-full-corpus-per-edit decision. A product latency or resource promise requires an owner-supplied budget; none is guessed. | A faster microbenchmark that omits persistence, validation, or equivalent work. |
| Correctness | Every registered invariant and negative case reaches its predeclared typed state; the highest-fidelity available independent authority decides representation, SQLite, Git, contract, or semantic behavior. | Successful execution, local implementation agreement, generated freshness, or a mocked boundary alone. |
| Standards compliance | The current executable route is recorded; each selected normative owner is reviewed against the design and evidence. Claim-matched verification and Commit review remain separate from prototype behavior. | A checklist, stale route, or passing unrelated repository suite. |

Pairwise efficiency comparison uses representative repeated observations after
one warm-up where timing is material. The record reports every observation and
environment; it does not hide variability behind a single best run. If no
correctness-equivalent baseline or owner-supplied budget exists, the efficiency
claim is `unavailable` and the material design is not admitted.

## Current Executable Standards Route

The public A1c `create_snapshot` plus `query(route)` path was run with planning,
implementation, verification, documentation, commit, build, and tooling
activities; library application; generated-contract and persistence
boundaries; and architecture, contracts, concurrency, resilience,
cross-platform, dependencies, security, diagnostics, and performance topics.
It returned 22 selected standards and zero unresolved fact categories:

- `core` and `router`;
- `workflow.planning`, `workflow.implementation`, `workflow.verification`,
  `workflow.documentation`, `workflow.commit`, `workflow.build`,
  `workflow.tooling`, and dependency-selected `workflow.release`;
- `profile.application.library`, `profile.boundary.generated-contract`, and
  `profile.boundary.persistence`; and
- `topic.architecture`, `topic.contracts`, `topic.concurrency`,
  `topic.resilience`, `topic.cross-platform`, `topic.dependencies`,
  `topic.security`, `topic.diagnostics`, and `topic.performance`.

Concurrent Plan Integration is explicitly excluded because Milestone 0 has one
serial integration owner and no independently integrated development proposals.
No language or framework profile is selected; Python is the experiment
mechanism, not a new public language contract. Interop and IPC are excluded
until a candidate actually crosses those boundaries.

## Prototype Registrations

| ID | Exact prototype-only path | Predeclared question and comparison | Effectiveness and efficiency criteria | Correctness oracle and required negative cases | Pass threshold |
| --- | --- | --- | --- | --- | --- |
| A2-P1 | `tools/standards_engine/prototypes/a2/authoring-state-model.prototype.html` | Can one visible immutable-revision/mutable-head model distinguish draft, analyzed, ready, staged, published, interrupted, stale, unauthorized, and recovery-required outcomes without changing A1c state? Compare exact revision-bound evidence with mutable completion flags. | Guided create/revise/analyze/approve/apply/recover workflows complete with opaque IDs and explicit next actions; fewer caller-owned facts and no dominated state representation. | Pure transition reducer plus A1c-U03/U06/U07/U19; stale head, stale analysis, mutation after approval, revoked authority, target conflict, interruption before/after publication, and contradictory observation. | `pass` only if every guided scenario reaches its exact state and mutable authored completion is unnecessary; otherwise `revise` or `reject`. |
| A2-P2 | `tools/standards_engine/prototypes/a2/projected-view.prototype.py` | Can exact non-Git mutations overlay frozen A1c content and execute the current compiler/analyzer path without proposal-as-snapshot or a second analyzer? Compare overlay composition with a scratch Git commit containing the same bytes. | Both paths expose the same requested corpus and semantic signature; caller supplies only base handle plus mutations. Record changed bytes, materialization bytes, call count, and repeated compile time; reject full-corpus durable copies. | Current A1c compiler and a separately captured scratch Git revision; invalid path, missing target, duplicate mutation, traversal, and semantic-invalid cases. | `pass` only on semantic equivalence, containment, exact failure, and a non-dominated no-full-copy representation. |
| A2-P3 | `tools/standards_engine/prototypes/a2/publication-recovery.prototype.py` | Can scratch SQLite attempt state and Git expected-ref publication prove stage-before-publish and cold recovery? Compare expected-target atomic update with unchecked ref update and publish-before-verify. | Verified candidate is invisible until one publication transition; caller never coordinates Git. Record Git/process calls, durable attempt bytes, scratch bytes, and repeated phase time. | Real scratch SQLite and Git; stale target, verification failure, unauthorized attempt, interruption at every material phase, applied-before-response, unchanged target, contradictory target, and cold reopen. | `pass` only if unchecked/publish-first alternatives are rejected and recovery distinguishes unchanged, applied, stale, and recovery-required without guessing or rollback. |
| A2-P4 | `tools/standards_engine/prototypes/a2/facade-workflow.prototype.py` | Which additive explicit operation set forms the smallest deep Authoring Interface while preserving all eight A1c roots? Compare explicit authoring operations, a tagged dispatch, and A1c query/inspect overload. | Representative workflow completes with no caller-owned internal facts; compare operation roots, calls, request fields, coordinated schema changes, and next-operation ambiguity. | Current operation manifest and generated-facade model; invalid kind, wrong handle, stale expected head, unauthorized apply, and unsupported contract. | `pass` only for an explicit additive Interface that preserves all eight roots, rejects dispatch/overload alternatives, and is not dominated in caller knowledge and change locality. |
| A2-P5 | `tools/standards_engine/prototypes/a2/efficiency-measurement.prototype.py` | Is the selected combined design non-dominated on the current corpus and representative workflow? Compare overlay/delta state with full-copy-per-revision and selected facade with alternatives. | Report public calls, caller fields, base/changed/durable/scratch bytes, Git/process calls, and repeated wall-time observations after warm-up. No unowned latency promise is inferred. | Measured filesystem/store sizes and monotonic clock over equivalent validated work; include no-op, small edit, multi-file edit, invalid edit, and repeated revision. | `pass` only if selected candidates are correctness-equivalent, no candidate strictly dominates them, and durable revision state is proportional to change material rather than full corpus bytes. |

## Isolation And Commit Contract

Each prototype receives its own private task branch and `/tmp` worktree from
the exact canonical commit containing this protocol. A separately committed
execution-admission record must name that base, branch, worktree, and write set
on canonical `main` before creation. The prototype owner is the A2 prototype
owner; the integration target and owner are canonical `main` and the A2
integration owner.
The authored prototype write set is exactly the path in the registration
table. Its branch-local commit also owns the mechanically regenerated
`evaluation/standards-effectiveness/generated/suite-inputs.json` after the
prototype path is staged. Exact review must show that this generated file
changes only its repository-index digest. The worktree uses disposable
repositories and stores only, has no canonical runtime consumer, and is never
merged; neither the prototype nor its branch-local generated projection enters
canonical `main`.

Each prototype is committed with focused reproduction evidence. The canonical
[prototype evidence index](prototype-evidence-index.md) later records the exact
base, branch, commit, command, observations, limitations, verdict, and A1c
preservation result. After the question is settled, its commit is protected by
a named recovery ref before the worktree becomes `removed-archived`, or the
worktree receives an explicit `retained-protected` contract. No branch or
worktree cleanup is inferred.

## Evidence Boundary

Prototype pass admits only the stated design decision for a later exact
production slice. Production still requires generated contract conformance,
real public behavior, durable migration or rejection, Linux CPython 3.11 and
3.12 evidence, complete policy-impact and coverage closure, independent
Standards and specification review, and a separately admitted write set.
