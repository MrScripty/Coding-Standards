# A2-P4R Facade-Composition Execution Admission

**Status:** `executed; pass; typed-continuation design admitted for later
contract planning`

## Question And Scope

Can one additive typed-continuation Interface let the representative agent
create, rediscover, revise, query, analyze, review, apply, and recover a
proposal using only authored material, judgments, and returned opaque handles,
while preserving all eight A1c operation roots and hiding projected material,
mutable evidence selection, authority, persistence, verification, and Git
coordination inside one deep Authoring Module?

P4R selects no production root, request, result, version, schema, Adapter, or
source. It compares prototype-local Interface candidates after P2R2 accepted
the private projected-material composition and after the user selected direct
canonical publication as the one application success meaning.

## Fixed Constraints And Dependencies

Every candidate must preserve the exact A1c roots `create_snapshot`,
`find_snapshots`, `delete_snapshot`, `undelete_snapshot`, `query`, `prepare`,
`resolve`, and `inspect`, including their capabilities and meanings. It must
not use tagged dispatch, overload an A1c root, create a proposal snapshot,
select mutable current analysis or readiness, accept caller Git/ref/OID/store
facts, expose a material resolver, or create another Analysis authority.

Revision normalization, readiness derivation, result projection, and current
compiler/Analysis composition are in-process dependencies. Snapshot/SQLite and
local Git are local-substitutable dependencies whose accepted P2R2 and P3
evidence remains authoritative for identity, lifecycle, publication, and
recovery. Their seams remain private. The generated Python Interface is the
only external seam; P4R adds no public storage, repository, authority, or
verification port.

The illustrative shape is deliberately non-authorizing:

```python
result = facade.explicit_intent(
    prior_opaque_handle,
    caller_authored_input,
)
```

## Design-It-Twice Candidates

### Minimal Three-Root Goal Interface

`find_proposals`, `author_revision`, and `conclude_revision` maximize apparent
leverage. A snapshot-or-revision anchor folds create and revise together;
authoring always compiles and analyzes a fixed dossier; conclusion combines
review, application, and recovery.

This candidate is retained as a control. It is not correctness-equivalent if
the anchor variant changes authorization or state transition, if callers lose
arbitrary projected query, if cheap drafting always incurs analysis, or if
review/application/recovery failure contracts become one hidden tagged
language. Lower call or field counts cannot dominate a candidate that preserves
those distinct caller goals.

### Flexible Revision-Addressed Portfolio

`create_proposal`, `find_proposals`, `revise_proposal`, `query_proposal`,
`analyze_proposal`, `review_proposal`, `apply_proposal`, and
`recover_application` keep distinct authorization, ordering, and terminal
contracts explicit. The flexible form supplies proposal plus expected revision
for review and may accept optional prior analysis/readiness handles.

This is the correctness-equivalent breadth baseline. It has strong Locality,
but callers may duplicate relationships already derivable from exact immutable
handles.

### Typed-Continuation Portfolio

The selected candidate under test retains those eight explicit intents but
requires only the immediately relevant authored facts and opaque continuation:

| Candidate operation | Caller fields | Hidden knowledge |
| --- | --- | --- |
| `create_proposal` | `base_snapshot`, `mutations`, `semantic_proposals` | proposal identity, first revision, dependency publication |
| `find_proposals` | optional `after`, `limit` | durable catalog, lifecycle filtering, head projection |
| `revise_proposal` | `expected_revision`, `mutations`, `semantic_proposals` | proposal lookup, base, head CAS, invalidation |
| `query_proposal` | `revision`, `request` | projected material and current query composition |
| `analyze_proposal` | `revision` | material reference, normalized inputs, Analysis identity |
| `review_proposal` | `analysis`, `decisions`, optional `prior_readiness` | proposal/revision binding, head check, authority, readiness derivation |
| `apply_proposal` | `readiness` | target authority, expected object, staging, verification, publication |
| `recover_application` | `application` | durable attempt, Git observation, truthful terminal state |

The representative workflow supplies both mutation and semantic-proposal
material on creation and revision, so optional-field packaging cannot game the
caller-knowledge metric. Results carry the exact proposal, revision, analysis,
readiness, and application handles needed by the next intent. Pending analysis
continues only through unchanged A1c `resolve`.

This candidate is preferred for execution because it combines the flexible
portfolio's explicit semantics with the common caller's smallest truthful
continuations. It is not admitted until the executable oracle passes.

## Effectiveness And Efficiency Oracle

The representative workflow must complete create, cold-handoff-style
rediscovery through canonical handle round trips, stale-safe revise, arbitrary
projected query, projected analysis plus unchanged `resolve`, immutable review,
direct configured-main publication, and recovery. Every returned next action
must be derivable from the result and allowed caller knowledge.

For each candidate, the prototype records:

- additive operation roots and public calls;
- required and supplied atomic caller facts, including nested facts;
- total defined input fields and result-carried handles;
- ambiguous next actions and distinct authorization/ordering contracts;
- existing A1c definitions or capabilities changed;
- coordinated contract-owner changes; and
- the deletion-test disposition and hidden behaviors per operation.

Timing is not material to this Interface-selection question and no latency
budget is inferred. The selected candidate passes efficiency only if no
correctness-equivalent candidate strictly dominates it on calls, caller facts,
defined fields, ambiguity, and coordinated change locality. A smaller but
semantically incomplete Interface is not an efficiency winner.

## Correctness Oracle

The current A1c manifest is the independent preservation authority. The
prototype-local Interface model and method introspection decide only the P4R
candidate shape. The current contract compiler must continue rejecting
additive roots until a later contract/version slice explicitly changes it;
P4R does not claim generated-contract acceptance.

The prototype must verdict-gate:

1. exact unchanged A1c roots and capability maps;
2. exact selected method names and caller fields, with no generic `invoke`;
3. canonical opaque-handle round trips and one result-carried continuation at
   every transition;
4. exact immutable revision, analysis, readiness, and application bindings;
5. arbitrary revision query and exact historical revision addressability after
   head movement;
6. unchanged A1c `resolve` continuation for pending projected analysis;
7. no projected snapshot, mutable current-evidence selector, caller target,
   Git/ref/OID/store/resolver/capability field, or authored completion flag;
8. one Authoring Module, one Analysis authority, and private dependency seams;
9. exact non-mutation on wrong-handle, stale-revision, analysis mismatch or
   incomplete analysis, stale readiness, unauthorized review/application,
   unsupported contract, stale target, and unavailable recovery cases;
10. the selected direct-publication postcondition represented without exposing
    its internal target facts; and
11. current compiler rejection of the unadmitted additive Interface.

Every negative must return its predeclared code, outcome category, and bounded
non-sensitive message. Any invariant or preservation failure is `reject`.
An unavailable deciding oracle is `revise`. `pass` requires effectiveness,
efficiency, correctness, Linux CPython 3.11 and 3.12 execution, independent
specification and standards review, and every repository gate.

## Limits

P4R may use prototype-local in-memory Authoring records and deterministic
private publication/authority Adapters because P2R2 and P3 already own the real
SQLite/Git claims. It must surface complete relevant state and Adapter traces
and make no durability, platform-Git, generated-contract, schema, migration, or
production-performance claim. Exact request/result schemas, public versions,
store representation, mutation variants beyond exact replacement, and
implementation write sets remain later decisions.

## Isolation And Execution Contract

- Exact base: `fc7dbeabb5828b5b6f3840a1ff004209ae291385`.
- Private branch: `prototype/a2-m0-facade-composition`.
- Task-owned worktree:
  `/tmp/coding-standards-a2-p4r-facade-composition`.
- Sole authored source:
  `tools/standards_engine/tests/prototypes/a2/facade-composition.prototype.py`.
- Branch-local generated artifact:
  `evaluation/standards-effectiveness/generated/suite-inputs.json`, which may
  change only its repository-index digest after the source is staged.
- Required runtimes:
  `/tmp/coding-standards-a1c-py311/bin/python` and
  `/tmp/coding-standards-a1c-py312/bin/python`, both with `PYTHONPATH=.`,
  `PYTHONDONTWRITEBYTECODE=1`, and safe-path `-P`.
- Archive ref:
  `refs/archive/a2-prototypes/p4r-facade-composition`.
- Expected terminal disposition: `removed-archived`.

The prototype source and branch-local generated projection never merge to
`main`. P5, ADR, public/persisted contract selection, migration, and production
source remain blocked until a passing P4R verdict is recorded canonically.

## Terminal Result

P4R passed on frozen source
`sha256:d3e9d80f3561eb83d818969cdf586d423baba594a8a435a547e2c5dc034c036f`
and evidence commit `9a0c34325e2849c437072b12b3188bede7f08d4e`.
All 34 executable gates passed on dependency-complete Linux CPython 3.11.14
and 3.12.3, including the real current A1c platform-harness continuation. The
representative workload supplied exactly its 49 independently named required
facts across 11 A2 calls plus unchanged A1c `resolve`; 28 negative cases
covered all 17 registered failure contracts.

The admitted design is the eight-intent typed-continuation portfolio recorded
above. The run exercised only exact replacement mutations. Current generated
`QueryCall` validation covered route, read, and related request variants, while
prototype-local projected answers deliberately made no claim to be canonical
A1c `QueryResult` semantics. Exact schemas, public versions, handle wire
formats, persistence, migration, ADR, production write sets, and Engine code
remain deferred.

Independent specification and standards reviews passed on the exact frozen
hash after their findings were corrected. The complete repository checkpoint
passed 269 of 269 declarative checks and all seven retained Bash verifiers.
The evidence commit is protected at
`refs/archive/a2-prototypes/p4r-facade-composition`; the clean worktree and
temporary branch were removed, and no prototype source entered `main`.

The next slice is a fresh P5 admission against the accepted P2R2 material model
and this accepted P4R facade. The former P5 base predates both and is not valid
execution authority.
