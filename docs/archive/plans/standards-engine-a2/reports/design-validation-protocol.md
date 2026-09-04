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
| Efficiency | Record public call count, caller-supplied field count, durable bytes, scratch bytes, and wall time where applicable. A design passes only against its registered correctness-equivalent comparison or an exact Product/Architecture-owned structural or resource budget; it must also preserve A1c's no-full-corpus-per-edit decision. A product latency or resource promise requires an owner-supplied budget; none is guessed. | A faster microbenchmark that omits persistence, validation, equivalent work, or the registered budget. |
| Correctness | Every registered invariant and negative case reaches its predeclared typed state; the highest-fidelity available independent authority decides representation, SQLite, Git, contract, or semantic behavior. | Successful execution, local implementation agreement, generated freshness, or a mocked boundary alone. |
| Standards compliance | The current executable route is recorded; each selected normative owner is reviewed against the design and evidence. Claim-matched verification and Commit review remain separate from prototype behavior. | A checklist, stale route, or passing unrelated repository suite. |

Pairwise efficiency comparison uses representative repeated observations after
one warm-up where timing is material. A registered structural budget uses
actual Interface signatures and traces once per supported runtime; it does not
create timing repetitions when time has no deciding claim. The record reports
every applicable observation and environment and does not hide variability
behind a single best run. If no correctness-equivalent baseline or exact
owner-supplied budget exists, the efficiency claim is `unavailable` and the
material design is not admitted.

## Current Executable Standards Route

The public A1c `create_snapshot` plus `query(route)` path was refreshed for P5
on exact base `b503dcb76fd27aca41df154f37e20f6635de44bf` with planning,
implementation, verification, documentation, commit, build, and tooling
activities; library application; generated-contract and persistence
boundaries; and architecture, contracts, concurrency, resilience,
cross-platform, dependencies, security, diagnostics, and performance topics.
P5 also selects the IPC boundary because it crosses and measures the Git
subprocess contract. The route returned 23 selected standards and zero
unresolved fact categories:

- `core` and `router`;
- `workflow.planning`, `workflow.implementation`, `workflow.verification`,
  `workflow.documentation`, `workflow.commit`, `workflow.build`,
  `workflow.tooling`, and dependency-selected `workflow.release`;
- `profile.application.library`, `profile.boundary.generated-contract`,
  `profile.boundary.ipc`, and `profile.boundary.persistence`; and
- `topic.architecture`, `topic.contracts`, `topic.concurrency`,
  `topic.resilience`, `topic.cross-platform`, `topic.dependencies`,
  `topic.security`, `topic.diagnostics`, and `topic.performance`.

Concurrent Plan Integration is explicitly excluded because Milestone 0 has one
serial integration owner and no independently integrated development proposals.
No language or framework profile is selected; Python is the experiment
mechanism, not a new public language contract. Interop remains excluded.

The combined P5 executable and its P5L replacement later failed independent
lifecycle and composition audits before measurement or behavior. P5C is a new,
narrower, resource-free executable claim. Its selected owners are Core,
Planning, Implementation, Verification, Documentation, Commit, Build, Tooling,
Release, Library, Generated Contract, Architecture, Contracts, Dependencies,
Security, and Resilience. Resilience owns preservation of the callback or
target failure and terminal revocation when that dependency fails. IPC,
Persistence, Concurrency, Cross-Platform, Diagnostics, and Performance are not
selected for P5C because it makes no resource, asynchronous, platform,
diagnostic, or measurement claim. A future P5R or P5M admission must refresh
its own executable route rather than inherit the historical 23-standard P5
route or P5C's narrower route.

## Prototype Registrations

| ID | Exact prototype-only path | Predeclared question and comparison | Effectiveness and efficiency criteria | Correctness oracle and required negative cases | Pass threshold |
| --- | --- | --- | --- | --- | --- |
| A2-P1 | `tools/standards_engine/prototypes/a2/authoring-state-model.prototype.html` | Can one visible immutable-revision/mutable-head model distinguish draft, analyzed, ready, staged, published, interrupted, stale, unauthorized, and recovery-required outcomes without changing A1c state? Compare exact revision-bound evidence with mutable completion flags. | Guided create/revise/analyze/approve/apply/recover workflows complete with opaque IDs and explicit next actions; fewer caller-owned facts and no dominated state representation. | Pure transition reducer plus A1c-U03/U06/U07/U19; stale head, stale analysis, mutation after approval, revoked authority, target conflict, interruption before/after publication, and contradictory observation. | `pass` only if every guided scenario reaches its exact state and mutable authored completion is unnecessary; otherwise `revise` or `reject`. |
| A2-P2 | `tools/standards_engine/tests/prototypes/a2/projected-view.prototype.py` | Can exact non-Git mutations overlay frozen A1c content and execute the current compiler/analyzer path without proposal-as-snapshot or a second analyzer? Compare overlay composition with a scratch Git commit containing the same bytes. | Both paths expose the same requested corpus and semantic signature; caller supplies only base handle plus mutations. Record changed bytes, materialization bytes, call count, and repeated compile time; reject full-corpus durable copies. | Current A1c compiler and a separately captured scratch Git revision; invalid path, missing target, duplicate mutation, traversal, and semantic-invalid cases. | `pass` only on semantic equivalence, containment, exact failure, and a non-dominated no-full-copy representation. |
| A2-P2R | `tools/standards_engine/tests/prototypes/a2/projected-analysis-replay.prototype.py` | Can any private seam feed projected revision material to the existing analyzer and still produce an injective, immutable, cold-replayable identity using the unchanged A1c AnalysisState, without a proposal snapshot, mutable current-head lookup, new public A1c field, or second analyzer? Compare external current-head lookup, ephemeral material injection, synthetic proposed snapshot, changed AnalysisState identity, and separate authoring-analysis state. | Two byte-distinct revisions over one base and identical declared analysis changes must remain distinguishable after head movement and process reopen. Record state bytes, retained identity bytes, resolver inputs, replay observations, and duplicated authorities; no full-corpus or latency claim is inferred. | Current A1c AnalysisState codec and generated prepare contract, exact A1c preservation matrix, P1 immutable evidence result, and P2 overlay result; same-state/different-revision collision, head advance, missing ephemeral input, synthetic-snapshot detection, state-format change, and second-authority detection. | `pass` only if one candidate is injective and cold-replayable while every protected A1c/P1/P2 constraint remains true; `reject-requires-product-reauthorization` if every bounded candidate either loses exact replay identity or violates a protected decision; `revise` only if the current codec or oracle is unavailable. |
| A2-P2R2 | `tools/standards_engine/tests/prototypes/a2/projected-material-identity.prototype.py` | Does the explicitly reauthorized closed `ProjectedRevisionMaterialRef` give one evolved `AnalysisState` injective immutable identity and exact cold replay through the existing compiler and Analysis kernel while snapshot-backed A1c behavior, one SQLite aggregate owner, and one Analysis authority remain intact? Compare the selected exact reference with the current omitted-reference collision and a correctness-equivalent full-material embedding control; retain current-head, synthetic-snapshot, identity-salt, and second-state cases as prohibited controls. | The representative caller analyzes either of two byte-distinct immutable revisions over one base without supplying changes, material bytes, repository facts, resolver choice, or current head. Record canonical state/reference/full-material bytes, fixed resolver calls, dependency rows, close/reopen observations, and both runtime environments. The selected state must retain only bounded reference and normalized analysis inputs, never a full projected corpus per analysis. | Candidate domain codec plus current canonical identity encoding, current compiler and Analysis kernel, real scratch SQLite, current snapshot path, and exact preservation matrix. Required outcomes are `A2P2R2.REVISION_BASE_MISMATCH`, `A2P2R2.REVISION_UNAVAILABLE`, `A2P2R2.REVISION_IDENTITY_MISMATCH`, current `SNAPSHOT.QUARANTINED`, `SNAPSHOT.EXPIRED`, and `SNAPSHOT.UNAVAILABLE`, plus exact rejection of ambient lookup and duplicate authority. Equal descriptors with distinct revision bytes, head movement, process reopen, and snapshot behavior are positive controls. | `pass` only if both revisions have distinct canonical states and handles, each cold replay resolves exact original bytes after head movement, every negative case reaches its exact typed outcome, snapshot behavior is unchanged, one aggregate and Analysis authority remain, reference storage is bounded rather than corpus-sized, and dependency-complete Linux CPython 3.11 and 3.12 plus current standards checks pass; otherwise `revise` only for an unavailable deciding oracle and `reject` for an invariant or preservation failure. |
| A2-P3 | `tools/standards_engine/tests/prototypes/a2/publication-recovery.prototype.py` | Can scratch SQLite attempt state and Git expected-ref publication prove stage-before-publish and cold recovery? Compare expected-target atomic update with unchecked ref update and publish-before-verify. | Verified candidate is invisible until one publication transition; caller never coordinates Git. Record Git/process calls, durable attempt bytes, scratch bytes, and repeated phase time. | Real scratch SQLite and Git; stale target, verification failure, unauthorized attempt, interruption at every material phase, applied-before-response, unchanged target, contradictory target, and cold reopen. | `pass` only if unchecked/publish-first alternatives are rejected and recovery distinguishes unchanged, applied, stale, and recovery-required without guessing or rollback. |
| A2-P4 | `tools/standards_engine/tests/prototypes/a2/facade-workflow.prototype.py` | Which additive explicit operation set forms the smallest deep Authoring Interface while preserving all eight A1c roots? Compare explicit authoring operations, a tagged dispatch, and A1c query/inspect overload. | Representative workflow completes with no caller-owned internal facts; compare operation roots, calls, request fields, coordinated schema changes, and next-operation ambiguity. | Current operation manifest and generated-facade model; invalid kind, wrong handle, stale expected head, unauthorized apply, and unsupported contract. | `pass` only for an explicit additive Interface that preserves all eight roots, rejects dispatch/overload alternatives, and is not dominated in caller knowledge and change locality. |
| A2-P4R | `tools/standards_engine/tests/prototypes/a2/facade-composition.prototype.py` | Can a typed-continuation portfolio remove P4's projected snapshot, mutable evidence, and caller Git stand-ins while retaining explicit caller goals? Compare it with a minimal three-root goal Interface, a flexible revision-addressed portfolio, P4's invalid surface, tagged dispatch, and A1c overload. | Complete the representative handle-carried workflow with arbitrary projected query, unchanged Analysis continuation, direct configured-main application, and recovery. Record calls, atomic caller facts, defined fields, result handles, ambiguity, coordinated owners, and deletion-test leverage; timing is immaterial. | Exact current A1c manifest/capabilities, prototype-local method introspection and state/trace, accepted P2R2/P3 decisions, and current compiler rejection of unadmitted roots. Wrong handle, stale revision, analysis mismatch/incomplete, stale readiness, unauthorized review/apply, unsupported contract, stale internal target, and unavailable recovery must not mutate state. | `pass` only if every exact invariant and negative passes on dependency-complete CPython 3.11 and 3.12, no forbidden caller fact or second authority appears, next handles are complete, existing A1c behavior is unchanged, and no correctness-equivalent candidate strictly dominates the selected Interface. |
| A2-P5 | `tools/standards_engine/tests/prototypes/a2/efficiency-measurement.prototype.py` | Historical combined-design comparison superseded before measurement. Exact terminal authority is the [P5 decomposition](p5-lifecycle-decomposition.md). | No result: supporting gates could not establish actual lifecycle ownership. | Independent audits found stale reopen ownership, pre-owner acquisition, an unproved process-registration gap, and excessive change propagation. | `reject-evidence-implementation`; no combined-design verdict and no correction authority. |
| A2-P5L | `tools/standards_engine/tests/prototypes/a2/p5_lifecycle_owner_prototype.py` and `tools/standards_engine/tests/prototypes/a2/p5_lifecycle_ownership_mvt.py` | Historical P5 lifecycle-owner question superseded at frozen-source audit. | No behavior or runtime observation ran. | Independent audits rejected stale linear authority, an uncontained handoff, post-registration async evidence, literal structural claims, raw Engine exposure, lifecycle/measurement coupling, and incomplete process-group terminal ownership. | `reject-evidence-implementation`; removed-archived at exact commit `4c1c5359a8314fc9106de4a92dd7b3a7cb0e44e6`; no correction or successor execution authority. |
| A2-P5C | `tools/standards_engine/tests/prototypes/a2/p5_phase_capability_prototype.py` and `tools/standards_engine/tests/prototypes/a2/p5_phase_capability_mvt.py` | Can one synchronous callback-scoped capability mirror all eight current explicit A1c roots, delegate identical generated requests to the same-named target methods, and permanently revoke after return or failure while omitting Engine and resource lifecycle from its supported callback Interface? Use one selected design and an owned structural budget, not candidate comparison. | One phase entry, one callback parameter, eight exact typed roots, one request per delegation, one private lease/capability per phase, one exact `PhaseRevokedError`, and zero generic tags, returned resource/cleanup identities, lifecycle ordering, cleanup branches, I/O, persisted bytes, timing, or report artifacts. | Current `StandardsEngine` signatures and generated call/result types plus one resource-free recording target. Require exact request/result/target-failure/body-failure identity, retained and returned capability revocation, successive-phase isolation, and exact `PhaseRevokedError("phase capability is revoked")` with no cause before stale target access. Also require the exact public surface, forbidden imports, and unchanged A1c sources. | `pass` only if one frozen bundle passes independent source audits and the unchanged resource-free MVT on dependency-complete CPython 3.11 and 3.12 within the exact budget. Any nonpass terminates and archives the source; P5R and P5M remain unavailable. |

P5C supports only `--all`. After both frozen-source audits pass, execute the
unchanged source once per supported runtime:

```text
PYTHONDONTWRITEBYTECODE=1 python3.11 -P tools/standards_engine/tests/prototypes/a2/p5_phase_capability_mvt.py --all
PYTHONDONTWRITEBYTECODE=1 python3.12 -P tools/standards_engine/tests/prototypes/a2/p5_phase_capability_mvt.py --all
```

Success prints exactly `P5C PASS` and exits zero. P5C creates no report or
result file. A failed assertion or unavailable dependency exits nonzero and
cannot be converted into a pass label.

P5C is an accidental-authority and lifetime-safety experiment for trusted,
synchronous Python composition. Its supported boundary is the capability's
public methods, callback arguments, and ordinary phase-owned return values. It
does not claim confidentiality, sandboxing, or containment against hostile
inspection of private attributes, bound methods, closures, frames, garbage-
collector state, monkeypatching, or other reflective Python mechanisms. A
caller requiring an adversarial boundary rejects this composition and must
return to Security-owned isolation design; P5C evidence cannot admit that use.

### P5C A1c Preservation Dispositions

| Accepted decision | P5C disposition | Deciding oracle |
| --- | --- | --- |
| A1C-U02 harness-managed calls and custom integration | `unchanged`: P5C is a private prototype-only composition seam, not a deployment mode, public tool call, or alternate behavior contract. | Both sources remain below the test/prototype boundary and excluded from package/public entrypoints; the generated agent-tool projection and current public Engine contract remain byte-identical. |
| A1C-U03 distinct invocation/handoff lifetimes | `composed-without-change`: the private phase lifetime is shorter than an Engine invocation and grants no durable authority; generated handles/results remain ordinary immutable values. | A retained or returned phase capability is revoked on normal return and exact body/target failure, while the identical generated request/result objects cross the callback unchanged. No capability is serialized or persisted. |
| A1C-U12 explicit Snapshot operations | `unchanged`: P5C mirrors `create_snapshot`, `find_snapshots`, `delete_snapshot`, and `undelete_snapshot` as separate same-name typed methods and adds no tag, overload, catalog, or Engine constructor state. | Signature/type-hint comparison proves the four exact roots; the recording target receives each identical call once; forbidden-surface review rejects generic dispatch and lifecycle methods. |
| A1C-U15 one generated facade contract | `unchanged`: P5C consumes current generated request/result types and defines no schema, codec, version, projection, or public operation. | Generated-contract, agent-tool, operation-manifest, and package-input identities are unchanged; the capability Module imports generated types and typing support only. |
| A1C-U18 supported runtimes | `composed-without-change`: P5C claims only resource-free synchronous behavior on dependency-complete Linux CPython 3.11 and 3.12. | The identical frozen bundle passes once on each accepted runtime; no Windows, macOS, process, filesystem, SQLite, or concurrent behavior is claimed. |
| A1C-U20 eight accepted typed operations | `unchanged`: P5C has exactly the same eight operation names, generated call parameters, and result unions; it neither replaces nor adds a public Engine root. | Resolved signature/type comparison against current `StandardsEngine`, exact same-object request/result/failure delegation for every root, and byte-identical Engine/generated sources all pass. |

Any nonpassing preservation row rejects the frozen P5C source. It does not
authorize an A1c change.

## Isolation And Commit Contract

Each prototype receives its own private task branch and `/tmp` worktree from
the exact base named by a durable execution-admission record on canonical
`main`. That record must exist before creation and must bind the current
registration meaning even when the prototype base intentionally excludes later
planning-only commits. Commit selects the coherent boundary; the plan does not
prescribe standalone or exact-parent topology. The prototype owner is the A2
prototype owner; the integration target and owner are canonical `main` and the
A2 integration owner.
The authored prototype write set is exactly the path or paths in the
registration table. Its branch-local commit also owns the mechanically regenerated
`evaluation/standards-effectiveness/generated/suite-inputs.json` after the
prototype path is staged. Exact review must show that this generated file
changes only its repository-index digest. Executable Python prototypes are test
artifacts below `tools/standards_engine/tests/prototypes/a2`; the existing
package contract must continue to exclude them from production source
ownership and package-input selection. A package-input entry or unowned-source
diagnostic is a stop-and-replan result. Existing file entries, registry and
suite-definition digests, graph, inventory, and retirement evidence must
remain unchanged. The worktree uses disposable repositories and stores only,
has no canonical runtime consumer, and is never merged; neither the prototype
nor its branch-local generated projection enters canonical `main`.

Each prototype is committed with focused reproduction evidence. The canonical
[prototype evidence index](prototype-evidence-index.md) later records the exact
base, branch, commit, command, observations, limitations, verdict, and A1c
preservation result. After the question is settled, its commit is protected by
a named recovery ref before the worktree becomes `removed-archived`, or the
worktree receives an explicit `retained-protected` contract. No branch or
worktree cleanup is inferred.

When a pre-authored prototype is mechanically relocated to its registered test
path, exact review may correct only an embedded reproduction path and the
minimum `__file__` parent depth needed to retain the same repository or package
root. The prototype owner must review the exact source diff and rerun the full
registered oracle. Any other logic, question, comparison, criterion, or
threshold change remains a stop-and-replan result.

## Evidence Boundary

Prototype pass admits only the stated design decision for a later exact
production slice. Production still requires generated contract conformance,
real public behavior, durable migration or rejection, Linux CPython 3.11 and
3.12 evidence, complete policy-impact and coverage closure, independent
Standards and specification review, and a separately admitted write set.
