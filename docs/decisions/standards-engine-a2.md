# Standards Engine A2 Controlled Logical Authoring

**Status:** Accepted

A2 extends the accepted A1c facade additively. Its authoring boundary begins
with `create_proposal` plus `find_proposals`: an agent supplies one retained
snapshot and one evidence-backed atomic `StandardsChangeSet` expressed in
canonical standards IDs, authored content, explicit semantics, relationships,
and lifecycle intent. The Engine returns opaque proposal and immutable revision
handles and can rediscover the proposal after process replacement. Repository
paths, complete serialized files, SQLite, Git refs, and object IDs remain
private. The original eight A1c operation roots and behavior remain unchanged;
the coordinated logical-authoring cutover advances the Interface to v20 and the
Authoring revision contract to v2.

`revise_proposal` accepts one expected immutable revision and appends one
normalized change set to its logical program. Authoring derives proposal
identity, base snapshot, retained base-repository path observation, and next
ordinal from the validated expected revision. It publishes the new immutable
record and advances the existing proposal head through one Snapshot-owned
SQLite compare-and-swap transaction. A stale expected head is an `invalid`
result and publishes no candidate record. Historical revision reconstruction is
an internal Authoring seam, not another public operation.

`query_proposal(revision, request)` reconstructs that exact immutable revision
and privately compiles its cumulative logical program into the current
Markdown, TOML, JSON, corpus, relationship, and generated authorities. The
result passes through the same A1c metadata, policy-impact, graph, Router,
coverage, and repository-coverage owners. Route, read, and related use one
shared navigation implementation with authority-specific result projection.
Proposal results and continuations are anchored to the revision, identify
projected content as `projection`, and expose no snapshot child or inspect
handle. Historical revision queries remain stable after proposal-head movement.
There is no second parser, graph, Router, content store, cache, or
proposal-as-snapshot conversion.

`analyze_proposal(revision)` resolves the exact immutable revision and base
snapshot, compiles both through
the current A1c semantic owners, and mechanically derives whole-artifact
modification, move, addition, removal, split, and merge descriptors from their
policy-unit corpora. The caller supplies no changes, content, repository facts,
or material resolver. One evolved `AnalysisState` owns a closed snapshot or
projected-revision material reference; the exact reference participates in
state bytes, Analysis identity, dependency closure, inspection, and cold
replay. Stored normalized changes and semantic proposals are revalidated
against the exact revision during every evaluation. Existing pending/complete
results and `resolve` continue through the same Analysis kernel.

`review_proposal(analysis, decisions, prior_readiness?)` accepts
only a complete revision-backed Analysis with no `requires-change`
disposition, then derives the immutable revision, current proposal head, and
configured `refs/heads/main` target internally. Consumer, impact, and audit
acceptances each carry explicit rationale and evidence and receive an
independent authorization through their existing review capability. Before
readiness publication, Authoring derives one imperative proposal-specific
conventional subject by applying the standards change named by the latest
explicit purpose summary and one material body from the cumulative explicit
rationales. A
content-bound readiness identity binds those decisions and authorization
records to the exact Analysis, revision, base snapshot, current target object,
target ref, and the Standards Verifier semantic-revision-1 `complete`
checkpoint. The Snapshot owner checks the exact proposal head and publishes
the immutable readiness aggregate in one transaction. A prior identical proof
is idempotent; stale or mismatched authority cannot publish readiness.

`apply_proposal(readiness)` reconstructs the exact current readiness and
proposal revision, requires current application authorization, and compiles the
logical program to its exact Engine-owned repository topology. Repository Git
materializes additions, modifications, explicit relocation as removal plus
addition, removals, and executable decisions in a private local clone at the
readiness target. It creates one deterministic proposal-specific conventional
commit and proves that its parent, tree, message, checkout, index, bytes, and
executable modes agree with its object identity. Mechanically authored
standards authorities have canonical regular non-executable mode; the Adapter
still represents and verifies exact executable decisions for its
repository-neutral contract. Candidate blobs and commits must fit the same
bound as subsequent exact reads. The
Standards Verifier owns the programmatic `complete` checkpoint and evaluates
that exact candidate before any candidate object or application fact enters the
configured repository. The Engine asks Repository Git to revalidate the active
candidate after the external checkpoint and before durable admission; invalid
or unsupported drift therefore remains a typed pre-admission rejection. Public
verification failure details retain only bounded identifiers and never expose
the private candidate path or raw diagnostic message. Authoring then persists one immutable verified intent
under the exact proposal-head guard. Repository Git imports the candidate
without a destination ref, advances only `refs/heads/main` through an
expected-old-object compare-and-swap, and observes the target before Authoring
persists the immutable applied outcome. Public success means all of those facts
are established. Every non-applied result after durable application admission
returns the application handle as `recovery-required`; known target divergence
remains distinct from an unavailable publication outcome, and a public recovery
operation remains a separate boundary from application.

The seventh production boundary adds `recover_application(readiness)`. During
application admission, Authoring atomically stores the verified immutable
intent and one immutable readiness-to-application selection. Recovery requires
current `standards.proposal.recover` authority bound to the exact readiness,
revision, expected target, fixed ref, and verification contract. It follows
the derived selection directly and never enumerates applications. A durable
applied outcome is historical authority even if `main` later moves. Without an
outcome, only observing the exact candidate permits Authoring to record the
already-established result. The expected target remains uncertain, another
target is diverged, and an unavailable observation remains unavailable.
Recovery performs no materialization, verification, object import, Git write,
retry, rollback, mutable phase transition, or schema migration.

Proposal IDs are unique lifecycle identities (`proposal:v1:<uuid4>`). Revision
IDs are content-bound identities over proposal ID, ordinal, base snapshot, base
repository path observation, the normalized cumulative logical change sets,
and the Authoring contract version. A proposal is a snapshot-dependent aggregate root
whose only mutable field is its head revision. The existing Snapshot Module
remains the single SQLite owner: store v2 adds aggregate heads and atomically
migrates an exact, integrity-valid v1 store before use. Migration publishes the
exact v2 schema or rolls back without changing any A1c row. Snapshot quarantine
hides proposals and purge removes their roots and immutable revisions through
the same dependency lifecycle. Discovery reads one transactionally consistent
page in durable insertion order and revalidates each head's canonical material,
kind, dependencies, proposal binding, and content identity before returning its
handle.
Minimal root tombstones prevent an expired proposal handle from aliasing a
later proposal if an ID factory repeats a UUID.

Existing-store identity, version, schema, and integrity are proved before any
persistent SQLite profile change. Failed opens close their connection, and a
failed first initialization removes only the exact staging file it created.
The facade keeps store selection at the deployment boundary and exposes an
owned close/context-manager lifecycle, not a caller-selected store path.

The public interface declares proposal author, read, composite review,
application, and application-recovery capabilities at the same deployment
boundary that owns the existing A1c capabilities; the domain does not add a
second ambient authorization mechanism or a generic capability-set contract.
Interface v20 and Authoring contract v2 replace the repository-shaped v19/v1
authoring representation in one coordinated cutover. Analysis request v5 and
result/state v6 add the truthful module-change variant required by logical
standards and relationship edits. Snapshot handle v5, Analysis handle v6,
proposal revision handle v1, readiness contract/handle v1, application
contract/handle v1, and store schema v2 remain because the cutover changes none
of those owned promises. The store already owns opaque aggregate
bytes, exact snapshot dependencies, and transactional aggregate publication,
so verified intent, selection, and outcome records require no schema migration
or mutable index. This decision does not add automatic retry/rollback, a
mutable application root or phase ledger, generic process or resource
ownership, measurement mechanism, or standards-graph node. The tested
P5C forwarding capability is intentionally not productionized because no real
caller needs a second eight-method A1c surface.

## Repository Git Dependency Re-evaluation

The write-capable A2 boundary triggers the A1c decision's required
re-evaluation because the Repository Git Adapter coordinates exact candidate
tree construction and one ref mutation. The required capability is
local-clone isolation, safe add/modify/remove index materialization, explicit
executable modes, deterministic proposal-specific commit creation,
complete-checkpoint execution against the exact checkout, object import without
a destination ref, expected-old-object ref update, exact observation, bounded
output, sanitized execution, and typed failure on Linux with the already
required Git executable.

The selected Git CLI Adapter delegates clone, checkout, index, object, and ref
semantics to Git and adds only product-specific sequencing, containment,
identity checks, and typed projection. Dulwich would add a second Git
implementation and its runtime/security lifecycle while the deployment still
requires Git for repository verification. pygit2/libgit2 would additionally
add native ABI, provisioning, and target obligations. Raw filesystem or ref
file mutation would locally implement repository semantics and is rejected.
For this contract, extending the existing bounded Adapter has the smallest
semantic and dependency surface. Re-evaluate again if a consumer requires
remote transport, credentials, signatures, arbitrary refs, non-local
repositories, merge/rebase semantics, or a platform without the selected Git
executable.

Standards graphs remain exclusively standards-domain authority. A2 consumes
them through the accepted A1c analysis semantics when evaluating proposed
standards content; it does not use them as an Engine implementation registry.
Engine feature sources, tests, proposal roots, and revision roots do not become
standards-graph or policy-impact-graph nodes merely because they implement or
verify A2.
