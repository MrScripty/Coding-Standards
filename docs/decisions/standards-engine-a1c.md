# Standards Engine A1c Snapshot And Analysis Architecture

**Status:** Accepted

This decision supersedes the A1b runtime architecture for A1c. The accepted
A1b implementation and [A1b ADR](standards-engine-a1b.md) remain historical
evidence rather than current runtime authority. This decision does not
authorize A2 authoring or cross-engine state migration.

## Context

A1b corrected real defects in schema semantics, identity framing, immutable
replay, typed uncertainty, and hidden process state. Its complete design also
gave fourteen independently stored semantic kinds, operation-authority
objects, authority views, generic envelopes and codecs, roots-only execution
closures, backup and restore operations, and broad coverage invalidation to a
product whose primary caller uses a small Python facade.

The accepted A1/A1b audit found no external deployed Engine consumer, retained
A1 state, or non-test caller of A1b persistence. Later product discovery
established the actual A1c contract:

- software-development agents are the first caller;
- a harness-managed tool call is the primary deployment;
- handles must survive process and agent-instance replacement;
- Coding Standards owns durable snapshots and dependent analysis state;
- callers may create only from the configured repository's current canonical
  commit and cannot select Git history or provide raw authority bytes;
- equal-content snapshots require independent lifecycle identities;
- deletion quarantines a complete dependent aggregate for seven days by
  default and permits complete undelete before expiry;
- closed stores avoid platform-specific identity and path assumptions;
- Linux is the verified A1c runtime platform, while Windows and macOS support
  remain deferred until real execution environments are available;
- cross-engine compatibility remains deferred until feature completeness; and
- semantic understanding remains with the agent.

The bounded A1c prototype and composed-design review are recorded in
[architecture experiment results](../plans/standards-engine-a1c/reports/architecture-experiment-results.md).
The remaining capture, aggregate-lifecycle, and complete-Interface assumptions
are exercised in the
[binding assumptions validation](../plans/standards-engine-a1c/reports/a1c-binding-assumptions-validation.md).
That evidence confirms the selected mechanisms while retaining production
parity, generated-contract, authorization, and verified-platform gates.

## Decision

### Public Interface

A1c exposes eight explicit operations through one generated Python facade:

```text
create_snapshot() -> CreateSnapshotResult | RejectedResult
find_snapshots(request) -> FindSnapshotsResult | RejectedResult
delete_snapshot(snapshot) -> DeleteSnapshotResult | RejectedResult
undelete_snapshot(snapshot) -> UndeleteSnapshotResult | RejectedResult

query(snapshot, request) -> NavigationResult | RejectedResult
prepare(request) -> PendingResult | CompleteResult | RejectedResult
resolve(analysis, submission) -> PendingResult | CompleteResult | RejectedResult
inspect(handle) -> InspectionResult | RejectedResult
```

The four snapshot methods have distinct request, authorization, effect, and
result contracts but share one internal Snapshot Module. They are not four
internal authorities and are not collapsed behind a tagged dispatch method.

`find_snapshots` uses deterministic keyset pagination over creation time and
snapshot ID. The continuation is the last returned snapshot ID, not stored
cursor state. Each page is a current lifecycle view; the operation does not
promise a transactionally frozen multi-page catalog.

The public facade contains no repository path, caller-selected commit, raw
snapshot bytes, content hash, project label, SQLite location, backup operation,
immediate purge operation, or child-level deletion operation.

### Snapshot And Content Identity

`SnapshotId` is a unique opaque lifecycle identifier with the representation
`snapshot:v1:<uuid4>`. UUID bits have no semantic meaning and grant no
authorization. The Snapshot Module generates the ID and the SQLite primary key
enforces uniqueness. A generated collision rejects the transaction as
`SNAPSHOT.ID_COLLISION`; it is never interpreted as an existing snapshot or
silently replaced with content identity.

Every creation produces a new `SnapshotId`, including creation over canonical
bytes already present in the store. Agents use this ID to address the snapshot
and allocate all dependent work. Equal content may be deduplicated internally,
but deleting one root cannot affect another.

`ContentId` is an internal content-addressed integrity and deduplication key
over the sorted logical path and exact-byte set. It is not public identity,
lifecycle authority, caller context, or a substitute for `SnapshotId`. Source
commit and creation time are provenance only.

Analysis remains an immutable value transition. Its content identity binds its
normalized inputs and accepted decisions, including every referenced snapshot
root ID. Equal analysis material under different snapshot roots therefore
cannot alias lifecycle ownership. Derived child handles contain their parent
analysis handle and typed child identity; they do not identify independently
stored authority objects.

### Canonical Capture

Snapshot creation binds one Git commit internally by resolving the configured
canonical repository's current `HEAD`. The caller cannot supply the revision.
All subsequent reads use exact Git object IDs and validate returned object type,
length, and hash. Worktree, index, status, and ambient `GIT_*` variables do not
participate.

Capture uses a traced roots-only authority compilation:

1. bind a Git content source to the resolved commit;
2. invoke the canonical metadata, policy-unit, routing, policy-impact, graph,
   coverage, and contract loaders from their declared root inputs;
3. record every logical path and exact byte sequence requested by those typed
   loaders;
4. reject missing, escaped, contradictory, duplicate, or unsupported inputs;
5. construct the immutable content set from the recorded closure;
6. rerun the same compilers through a second recording source over the in-memory
   content set and require the same requested-path closure and semantic outputs;
   an uncaptured replay request is a closure mismatch; and
7. publish the content and new snapshot root in one SQLite transaction.

The traversal is linear in the requested files and declared references. It
does not recursively scan the filesystem, infer consumers from prose, or bind
mutable corpus counts and hashes in code. A new declared authority reference is
discovered because its owning loader requests it.

### Module Graph

```text
standards_identity
    standard library only

standards_contracts
    jsonschema
    referencing

repository_git
    standard library and the Git executable

standards_snapshots
    standards_identity
    sqlite3 from the standard library

metadata, applicability, policy-impact, graph
    retain their semantic dependencies
    no snapshot or SQLite dependency

standards_analysis
    metadata
    applicability
    policy-impact
    graph_engine
    standards_identity

standards_engine
    composes contracts, repository_git, snapshots, and domain Modules

standards_verifier
    repository_git
    consumes public and package contracts
```

`repository_git` is a small neutral Adapter Module. Snapshot capture and the
Verifier are independent real consumers of sanitized Git execution and exact
repository observations. Without it, the same hostile-environment, output,
and object-integrity rules would be duplicated or the Verifier would depend on
snapshot lifecycle. It owns no standards meaning, snapshot state, analysis, or
verification policy.

`standards_snapshots` replaces `standards_authority`. It accepts already
captured immutable content from the Engine composition root and owns content
sets, unique roots, SQLite publication, discovery, quarantine, undelete,
expiry, dependent-record storage, and derived lookup indexes. It does not
depend on Repository Git and does not own domain semantics, JSON Schema, Git
policy, analysis evaluation, authorization decisions, or backup and restore.

### SQLite Store

The Snapshot Module owns one current-version SQLite store. Its logical schema
contains:

- store contract metadata;
- deduplicated canonical content sets and exact file rows;
- independently identified snapshot roots with provenance and lifecycle;
- immutable analysis-state aggregate payloads and their snapshot dependencies;
- derived analysis-child lookup rows; and
- minimal purged-root tombstones containing only snapshot ID and purge time.

Foreign keys and transactions enforce aggregate ownership. Publishing a root
or analysis state is all-or-nothing. Analysis rows reference every snapshot
they require; purging any required root cascades to those rows and indexes.
Quarantine makes the root and every dependent operation unavailable without
physically deleting bytes. Undelete restores the whole aggregate before its
fixed deadline. Repeat deletion returns the existing deadline and never
extends it.

Expiry is evaluated on ordinary later invocations; no background service is
required. Purge transactionally removes expired roots, dependent analyses and
indexes, and content no remaining root references. A tombstone preserves
`SNAPSHOT.EXPIRED` and prevents ID reuse without retaining deleted authority.

The default quarantine duration is seven days. Deployment configuration may
select another positive duration, but the Python Interface and individual
delete requests cannot. The effective deadline is stored at deletion time and
does not change when configuration changes.

The store uses one schema version and no migration framework in A1c. Unknown
schema versions are `unsupported`; malformed or contradictory stores are
`invalid`; unavailable files, locks, or required capabilities are
`unavailable`. Lock contention is not silently retried as another operation.

The administrative movement unit is the complete closed SQLite store. All
connections must be closed and transient journal files absent before copying.
Coding Standards does not expose backup, restore, import, export, or merge
operations. Divergent copies are independent stores and are never merged by
snapshot ID.

### Analysis Persistence And Replay

The analysis Module owns one immutable `AnalysisState` containing only exact
inputs and dependency-valid accepted decisions:

- base and proposed snapshot IDs;
- normalized changes and semantic proposals;
- fact observations;
- consumer and impact dispositions;
- authored coverage attestations;
- evidence and authorization records; and
- material domain compatibility constants.

Requirements, obligations, impact traces, reading plans, certificates,
completion proofs, pending results, and complete results are deterministic
projections and are not independently stored authority. A domain-owned codec
validates and serializes the complete aggregate. The Snapshot Module stores its
opaque canonical bytes and a derived child index; it does not interpret them.

`prepare` optionally accepts one prior analysis handle. The Analysis kernel
imports only decisions whose narrow dependencies remain valid. Dormant-valid
decisions remain in state; dependency-invalid decisions are removed. Current
material requirements alone block completion. Providers produce typed claims
over declared immutable inputs; Analysis alone validates claims and constructs
observations. Router facts remain ephemeral navigation input and never become
standards-change observations.

Cold replay resolves exact snapshot and analysis records from the store,
recompiles domain material from snapshot bytes, revalidates retained decisions,
and projects the result. It never substitutes the current repository,
authorization, provider input, or another snapshot for missing material.

### Dependency Closure

A1c removes persisted operation-authority contracts, standards-authority views,
generic authority envelopes, owner codec registries, and execution-closure
objects.

Exact closure remains mechanical. Each domain-owned persistent aggregate has a
closed constructor and codec that declares and validates its typed direct
dependencies. Analysis state records exact snapshot roots and accepted decision
dependencies. A small composition-root traversal verifies that every declared
dependency resolves, agrees with its expected type and owner, is acyclic where
cycles are forbidden, and is compatible with the current domain contract.

There is no second role/cardinality registry. Adding a dependency changes the
owning domain type, identity material, codec, and focused replay evidence.
Navigation values are recomputable projections and require no persisted
execution closure.

### Contracts And Versions

The canonical JSON Schema continues to own serialized public request and result
shapes. `jsonschema.Draft202012Validator` remains the sole Draft semantics
implementation. A1c does not implement JSON Schema keywords.

One operation declaration identifies every public operation, its stable opaque
operation ID, capability, input definition, and result definitions. The
contract compiler traverses every reachable definition, rejects unsupported
constructs, generates native Python models and agent tools, and uses the same
compiled validator at the public boundary.

Schema-instance equality, domain equality, identity encoding, ordering, and
content deduplication remain separate contracts. Generated freshness, schema
conformance, public producer behavior, and domain identity evidence remain
separate claims.

The public decoder validates one incoming value and retains that proof in the
frozen generated representation. Nested construction during that decode does
not repeat validation. Direct generated-model construction remains a complete
smart-constructor boundary. Engine-produced generated results retain their
proof through the facade, which checks exact membership in the schema-derived
operation result algebra before serialization rather than validating the same
unchanged value again.

The A1c public replacement advances the facade schema to version 12 and the
public handle representation to version 5. These numbers identify incompatible
serialized contracts, not implementation releases. Domain owners retain only
material identity or compatibility constants. Operation compatibility changes
advance the affected operation declaration rather than a stored operation
object or copied version bag.

No v11 reader, converter, dual writer, fallback decoder, alias, or SQLite
schema migration is provided. The repository has no retained A1b store or
external client requiring overlap. Cross-engine snapshot compatibility remains
deferred; a later stable-release plan must define it before making such a
promise.

The current role and bump rules are recorded in the
[A1c corrective version matrix](../plans/standards-engine-a1c-repair/reports/dependency-and-version-decisions.md).
Interface, request, result, handle, AnalysisState format, Analysis identity, and
SQLite store values advance only for their named promise; none is an umbrella
implementation or release version.

### Coverage

Coverage identity binds only inputs capable of changing consumer discovery:

- canonical policy-unit identity and semantic payload;
- compiled relationships and applicability dependencies;
- referenced fact contracts;
- independent horizon provider contract; and
- exact selected horizon-member semantic or content fingerprints.

Repository-global suite-input or file-index freshness remains Verification
evidence and does not enter product coverage identity. Attestations are authored
authority stored in analysis state; requirements and certificates are derived.
An empty graph result is never proof of complete coverage without an
independently audited horizon.

### Failures And Authorization

Public failures preserve `invalid`, `unsupported`, and `unavailable` outcomes.
Snapshot absence, quarantine, expiry, store incompatibility, corruption, and
lock unavailability remain distinct codes. Programming defects and impossible
generated results are not converted into caller argument errors.

Capabilities are evaluated through the harness-supplied execution context.
Handles are identifiers, not authorization. Stored decisions retain exact
evidence and authorization records, and reuse revalidates them against the
current declared authority inputs. Live network, ambient filesystem state, and
undeclared provider inputs cannot affect deterministic state creation.

### Platform Contract

Linux is the verified A1c product platform on CPython 3.11 and 3.12. Logical
repository paths use slash-independent component tuples and preserve Unicode
codepoints and case. The real Linux harness proves Git-backed capture, SQLite
open and close behavior, unchanged closed-store copying, concurrent cold
process reads, and the public snapshot and analysis workflow. Focused Snapshot
tests separately prove deterministic transaction rollback, aggregate
quarantine, expiry, and lifecycle rules; those tests are not represented as
additional real-platform observations.

The harness hashes a closed SQLite file only to detect corruption between its
administrative copy and consumer open. That digest is test-local transport
evidence, not snapshot identity, logical database identity, a compatibility
promise, or a public import/export contract. Remove the hash when the tested
transport supplies equivalent integrity verification or when the harness no
longer copies raw closed-store bytes.

The implementation retains platform-neutral identity, path, and closed-store
boundaries, but A1c does not claim Windows or macOS support. Those platforms
remain future targets and require the same real harness evidence before a
later release or plan may advertise them as supported. Linux evidence is not
treated as proof of either deferred target.

The former Linux/ext4-only native filesystem capture Adapter is deleted. Git
object capture is the sole canonical snapshot source for A1c.

## Composed-Design Reconciliation

The accepted experiment composition remains intact except that the previously
unnamed canonical-source Seam is assigned to `repository_git` because it has
two independent consumers.

- Independent concerns: public contract compilation, identity framing, Git
  repository observation, snapshot lifecycle persistence, domain compilation,
  analysis transitions, and verification change for different reasons.
- Interleaving: unique root identity is separate from content equality;
  quarantine time is separate from stored bytes; Git mechanism is separate from
  snapshot policy; derived analysis work is separate from accepted decisions.
- Caller knowledge: agents know generated operations and opaque handles only.
  They do not know Git commands, content hashes, SQL, codecs, closure roles, or
  child cleanup.
- Change locality: Git security changes affect `repository_git`; SQLite schema
  changes affect Snapshot; fact or obligation changes affect Analysis; public
  shapes affect Contracts and the facade; identity framing affects Identity and
  the exact owning domain.
- Stable Interfaces: peer domain Modules consume immutable content sources and
  typed values, not tables, journal modes, operation registries, or envelope
  layouts.
- Independent evolution: repository observation, storage, analysis, contracts,
  and verification have distinct failures and focused tests.
- Necessary complexity: exact capture, durable roots, aggregate deletion,
  immutable decisions, external schema semantics, and typed uncertainty remain
  contained by their owners.
- Deletion result: deleting Identity, Contracts, Git observation, Snapshot, or
  Analysis redistributes required complexity to several consumers. Deleting
  generic Authority, independent child storage, stored operation contracts,
  backup/restore, native capture, or global coverage invalidation removes
  machinery without removing a selected product capability.

The additional Git Module improves the composition: it prevents both duplicated
security behavior and an inverted Verifier-to-Snapshot dependency while adding
no semantic or lifecycle authority.

## A2 Projected-Material Supersession

Accepted A2 Milestone 4 supersedes only A1c's snapshot-only proposed-analysis
material assumption. One immutable Analysis-owned reference now identifies
either an exact proposed snapshot or an exact immutable proposal revision over
the Analysis base snapshot. Snapshot-backed `prepare` maps its existing
`proposed_snapshot` request to the snapshot variant. Additive
`analyze_proposal(revision)` resolves the revision's retained base and exact
replacement overlay without accepting caller-supplied changes, material,
repository facts, or resolver choice.

For revision-backed analysis, Analysis derives whole-artifact change
descriptors from the compiled accepted and projected policy-unit corpora and
retains those normalized inputs with the revision's semantic proposals. Every
evaluation, including cold replay and the existing `resolve`, reloads the exact
revision and rejects any retained-input mismatch. The revision reference is
part of Analysis identity, so byte-distinct revisions cannot alias even when
their derived descriptors are equal. The Analysis aggregate depends on the
base snapshot; the snapshot variant also depends on its proposed snapshot.
Proposal revisions remain Authoring-owned, snapshot-dependent records and do
not become snapshot or Analysis authority.

This is a coordinated current-engine contract replacement: Analysis state is
v5, its identity domain and public handles are v6, result projection is v5,
and the generated interface is v16. Obsolete Analysis state is unsupported;
there is no dual reader, handle alias, or silent reinterpretation. A1c request
contract v4 is unchanged. Proposal revision handle v1, Authoring contract v1,
and SQLite store schema v2 are also unchanged because their owned promises do
not change: the Snapshot store already persists opaque aggregate bytes and
exact arbitrary snapshot-dependency sets. A no-op store migration is rejected
as unnecessary machinery.

The existing compiler, Analysis kernel, immutable transition model,
pending/complete projections, inspection, and `resolve` remain the sole
semantic path. Revision-backed fact providers may request a proposed
`revision` immutable input; Analysis never labels a revision as a proposed
`snapshot`. This supersession adds no mutable proposal-head replay, projected
corpus copy, generic public material Interface, second analyzer, review or
readiness state, application, Git publication, or recovery behavior.

## Migration

The migration is an atomic A1b-to-A1c source and public-contract replacement.
Lower semantic Modules remain available while their authority-envelope wrappers
are removed. `standards_authority` is replaced by `repository_git` and
`standards_snapshots`. Analysis storage becomes one aggregate. The Engine
facade switches to snapshot-root inputs and generated v12 results. Historical
A1b suites and graph records are replaced, not retained as parallel runtime
authority.

The exact component and consumer dispositions are owned by the
[migration inventory](../plans/standards-engine-a1c/reports/a1b-to-a1c-migration-inventory.md).
The completed relationship-migration table is retained as historical evidence
only. It is not an active suite input, graph consumer, or permanent comparison
between historical and current policy authority.

## Consequences

Benefits:

- agents receive durable snapshot ownership without coordinating content,
  children, or individual observations;
- one root ID cannot alias another equal-content lifecycle;
- domain semantics no longer require generic persistence envelopes;
- cold replay keeps exact immutable inputs without independently storing every
  derived value;
- coverage changes invalidate only relevant decisions; and
- Git, SQLite, schema, and analysis failures have coherent owners.

Costs:

- snapshot creation recompiles the complete declared authority closure;
- current-engine replay recomputes derived domain projections;
- one SQLite store remains operational state requiring administrative file
  protection; and
- Windows and macOS support remain unavailable until real platform evidence is
  obtained.

## Re-Plan Triggers

Re-plan if:

- a real consumer requires caller-selected history, project labels, immediate
  purge, child-level lifecycle, Engine backup/restore, or cross-store merge;
- traced compilation cannot prove complete canonical authority closure;
- analysis cannot be reproduced from stored aggregate inputs and snapshot
  bytes without independently stored derived authority;
- a selected dependency lacks Linux or supported Python compatibility;
- Windows or macOS support is proposed without real platform evidence;
- a retained external consumer or A1b store requires compatibility overlap;
- a domain dependency cannot be expressed once in its owning state/codec;
- measured replay or catalog behavior requires a new cache or pagination
  contract; or
- implementation changes the composed ownership or makes required reasoning
  propagate beyond the owners identified here.
