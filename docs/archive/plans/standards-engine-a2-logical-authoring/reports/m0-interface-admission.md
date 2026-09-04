# Milestone 0 Logical Authoring Interface Admission

**Status:** `Accepted`

**Development Decision:** `implement`

## Decision

Keep every accepted A1c/A2 operation and trust boundary. Replace only the
repository-shaped payload of `create_proposal` and `revise_proposal` with one
atomic `StandardsChangeSet`. Each accepted revision appends one normalized
change set to an immutable logical program rooted at the proposal's exact base
Snapshot. The Engine privately compiles that program to the current standards
authorities and reuses the existing A1c compiler, graph, Router, navigation,
and Analysis path.

This is a deepening of the existing Authoring Module, not a second authoring
Interface, graph, parser, store, or lifecycle.

## Compared Interfaces

| Candidate | Interface and Depth | Caller knowledge and Locality | Machinery/deletion result | Decision |
| --- | --- | --- | --- | --- |
| Operation-specific single edit | One closed `StandardEdit` per revision; high Depth for the common one-unit revision. | Minimal common payload, but an atomic split, removal, or coupled relationship repair requires multiple intermediate revisions and can expose states that are invalid only temporarily. | Small public algebra, but coupled-operation variants grow and orchestration leaks into callers. Deleting batch support would continue to force sequencing outward. | Useful common-path evidence; reject the one-edit restriction. |
| Three-root effect facade plus atomic changes | Collapse reads, authoring, and transitions behind three tagged roots. | Atomic domain work is local, but capabilities and effects become less local because unrelated A1c/A2 operations share broad dispatch Interfaces. | Conflicts with A1c's explicit operation roots and adds no product capability. | Reject the facade collapse; retain its atomic change-set idea. |
| Sealed flexible intent program and document block algebra | Complete desired state with a public Markdown-like block AST, placement vocabulary, coverage edits, and sealed byte projection. | Hides formats but makes callers learn a second document model and several authority families. | A large renderer/AST/sealed-cache surface becomes permanent; deletion would not remove the necessary core compiler, only speculative generality. | Reject the AST, writer registry, sealed-byte cache, and authored coverage language. |
| **Selected: bounded atomic change set** | Existing create/revise operations carry closed standards-domain edits and plain authored policy text/fragments. One private logical-authoring compiler coordinates current owners. | Callers know canonical standards/policy IDs, opaque non-standard consumer handles, authored policy, explicit semantics, rationale, and evidence—never repository representation. Changes remain local to the Engine and the semantic owner they affect. | The unavoidable writer and topology planner pass the deletion test: removing them would redistribute Markdown/TOML/JSON/path coordination to every caller. No general AST or extension registry is admitted. | **Implement.** |

The selected Module has high Leverage: one stable Seam hides seven physical
changes in the representative add without changing the Snapshot, Analysis,
review, readiness, application, or recovery Interfaces.

## Admitted Public Shape

The two changed calls become:

```text
create_proposal(base_snapshot, change_set)
revise_proposal(expected_revision, change_set)
```

`StandardsChangeSet` contains one purpose record (`summary`, `rationale`, and
explicit evidence) and an unordered, non-empty set of closed edits. Input order
does not affect revision identity or candidate bytes. Each logical facet may be
written at most once in a change set.

The admitted edit families are:

- create or revise a standard using canonical ID, title, authored body text
  without a metadata envelope, and explicit logical metadata;
- revise a registered policy unit using its canonical ID, authored section
  content, semantic revision, and intent without resubmitting its surrounding
  document;
- move a registered policy unit between canonical standards using canonical
  unit/standard IDs and an optional canonical sibling anchor;
- retire a policy unit or standard with successors and explicit dispositions
  for every affected relationship;
- replace the exact desired `Requires` and `Specializes` sets for one standard;
  and
- put or remove a fully specified policy-impact/broader semantic relationship.

An endpoint that is a canonical standard or policy unit uses its canonical ID.
An existing non-standard consumer uses an opaque, Snapshot-bound authoring
target handle returned by Engine query/inspection. The handle, not a path, is
submitted back to the Engine.

Standard creation may include registered policy-unit declarations referencing
headings in its authored body. A whole-body revision remains supported for
unmapped content, but a focused policy-unit revision is the common operation.
The public Interface does not contain repository paths, complete files,
metadata envelopes, TOML/JSON, SQL/table identities, Git refs/OIDs, commit
objects, or remote controls.

## Semantic And Mechanical Boundary

The caller or reviewer owns:

- standard and policy-unit identity and lifecycle intent;
- authored policy text and explicit semantic-revision intent;
- `Requires`, `Specializes`, policy-impact, and broader semantic meaning;
- relationship endpoints, applicability, scopes, evidence owner, rationale,
  successor/disposition decisions, and evidence; and
- coverage attestations and review decisions through the existing authorized
  Analysis/resolve/review workflow.

The Engine may only derive:

- canonical owner placement and file topology;
- Markdown metadata envelopes and fixed-schema TOML/JSON serialization;
- corpus, policy-unit, relationship-source, and generated-input registry
  membership and deterministic ordering;
- structural/representation digests, exact affected IDs, change descriptors,
  and semantic-proposal records from explicit intent;
- Router/graph/coverage requirements by invoking their current compilers; and
- candidate commit material from the validated change-set purpose.

The Engine never invents a relationship, lifecycle successor, applicability,
semantic revision, evidence conclusion, attestation, authorization, or review
disposition. Missing meaning is a typed rejection.

## Ordering And Invariants

1. Decode the generated contract and reject unknown members.
2. Authorize the existing operation before durable state disclosure.
3. Resolve the exact base/head and enforce proposal-head compare-and-swap.
4. Normalize the change set and reject duplicate/conflicting facet writes.
5. Compose it with the immutable prior logical program over the exact base
   Snapshot.
6. Resolve canonical IDs and opaque target handles; discover affected
   relationships without deciding their disposition.
7. Require explicit semantics, lifecycle decisions, rationale, and evidence.
8. Project only the current fixed authority families into an immutable virtual
   content source.
9. Compile through the existing metadata, policy-unit, policy-impact, graph,
   Router, coverage, and repository-coverage owners.
10. Mechanically derive current Analysis inputs, build the v2 revision
    identity, store the immutable aggregate, and advance the head atomically.

Every exact revision remains queryable and analyzable after a later head
advance or process replacement. A stale or invalid change set stores nothing
and does not advance the proposal head. No configured repository, index, Git
object, or ref is written before apply. The private compiler may create
task-owned ephemeral Git state solely to evaluate current index-dependent
canonical verification authorities; that state is deleted with the projection
and is never a proposal, persistence, or publication authority.

## Typed Failure Contract

The existing `RejectedResult` outcomes remain. The implementation provides
stable Authoring codes for at least:

- invalid/duplicate edits and invalid canonical IDs;
- unknown or already-existing standards/policy units;
- stale proposal head;
- missing semantic or lifecycle disposition;
- missing rationale/evidence or invalid semantic revision;
- dangling relationship, invalid placement, and `Requires`/`Specializes`
  closure failures;
- projection disagreement with a canonical compiler;
- unsupported edit, topology, relationship kind, retained authoring contract,
  or platform; and
- unavailable Snapshot, authority, store, or compiler input.

Canonical owner diagnostics, such as `METADATA.REQUIRES_CYCLE`, are preserved
when they already state the exact failure more precisely.

## Reorganization Boundary

“Reorganize” in this plan means changing explicit graph relationships and
moving registered policy units whose canonical IDs give them stable logical
identity. Arbitrary movement of unregistered paragraphs or sections is
unsupported. Supporting it would require headings-as-public-locators, path
knowledge, inference, or a generic document AST, all outside the admitted
product contract. This limit still satisfies LA-A2, which requires explicit
relationship **or** placement change.

## Minimum Viable Test

A disposable Python probe under one task-owned `/tmp` directory exercised the
selected shape against `StandardsEngine._compile`, which invokes the real
canonical metadata, policy-unit, policy-impact, graph, Router, coverage, and
repository-coverage compilers. The prototype was run on Linux CPython 3.11 and
3.12 and was deleted after this evidence was recorded.

Positive results on both runtimes:

- baseline compile;
- logical creation of one topic and one policy unit;
- explicit policy-impact relationship creation;
- focused policy-unit content/semantic-revision update;
- explicit `Requires` reorganization;
- removal with complete relationship dispositions;
- deterministic output and identity under shuffled edit order;
- SQLite close/reopen with identical revision IDs and candidate replay; and
- proposal-head CAS with exactly one current winner.

The representative create used two public logical edits and caused seven
hidden representation updates: module Markdown, canonical corpus, policy-unit
registry and sidecar, policy-impact registry and declaration, and generated
suite inputs. The public payload contained none of the corresponding paths or
format tokens. The resulting coverage requirement existed without any
inferred attestation. After explicit removal, the real compiled semantic
signature matched the baseline.

Negative results on both runtimes:

| Case | Deciding diagnostic |
| --- | --- |
| Repository-shaped public member | `AUTHORING.INVALID_ARGUMENTS` |
| Missing retirement relationship dispositions | `AUTHORING.MISSING_SEMANTIC_DECISION` |
| Incomplete semantic relationship authority | `AUTHORING.SEMANTICS_REQUIRED` |
| Real dependency cycle | `METADATA.REQUIRES_CYCLE` |

## Effectiveness, Efficiency, Correctness, And Standards Verdict

- **Effectiveness:** the selected Interface covers add, focused revision,
  relationship reorganization, removal, replay, and concurrent head behavior.
- **Efficiency:** the common focused revision is one edit containing only the
  changed policy facts; the add hid seven physical updates behind two edits.
  No runtime measurement framework is warranted because there is no admitted
  latency/throughput budget.
- **Correctness:** real compilers decided every positive candidate and the
  cycle negative; exact replay, ordering, removal closure, and CAS were
  observed on both supported runtimes.
- **Standards compliance:** the design preserves the A1c deep Module and
  operation-specific trust seams, keeps semantic owners singular, hides
  persistence/repository mechanism, uses typed failures, adds no speculative
  dependency or remote seam, and has a bounded verification plan.

No new production dependency is admitted. Fixed-schema writers use current
models, `tomllib`, deterministic serializers, and exact captured content. A
generic TOML writer, Markdown AST, extension registry, sealed-byte cache,
second compiler, or second store is prohibited.

## Version And Identity Decision

- Public Interface: `19` to `20` (breaking coordinated authoring replacement).
- Authoring aggregate/identity contract: `1` to `2`.
- Analysis request `4`, Analysis result/state `5`, public handle schema `5`,
  and Snapshot store schema `2`: unchanged.
- Revision identity binds proposal, ordinal, base Snapshot, authoring contract,
  and the complete normalized accumulated logical program. Renderer-only
  changes cannot reinterpret a retained revision; an unsupported retained
  writer/intent version is rejected.
- No compatibility overlap or general migration is admitted by the current
  consumer/state inventory.

## Production Admission And Stopping Rule

Milestone 1 may use exactly its predeclared write set. The MVT found no missing
production file or dependency. Implementation is reversible and no named
unresolved issue threatens an irreversible or high-consequence result.

The Milestone 0 stopping condition is met. Development therefore returns
`implement`; an adjacent uncertainty must not start another design cycle
unless it invalidates this contract, demonstrates a standards violation, or
materially changes reversibility or consequence.
