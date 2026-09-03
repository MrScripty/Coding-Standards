# Standards Engine A2 Controlled Authoring

**Status:** Accepted

A2 extends the accepted A1c facade additively. Its first production boundary is
`create_proposal` plus `find_proposals`: an agent supplies one retained snapshot,
exact non-Git replacement mutations, and A1c-shaped semantic proposals; the
Engine returns opaque proposal and immutable revision handles and can rediscover
the proposal after process replacement. The original eight A1c operations,
their request/result versions, and their behavior remain unchanged.

The second production boundary adds `revise_proposal`. Its caller supplies one
expected immutable revision plus the complete replacement and semantic material
for the successor. Authoring derives proposal identity, base snapshot, and next
ordinal from the validated expected revision. It publishes the new immutable
record and advances the existing proposal head through one Snapshot-owned
SQLite compare-and-swap transaction. A stale expected head is an `invalid`
result and publishes no candidate record. Historical revision reconstruction is
an internal Authoring seam, not another public operation.

The third production boundary adds `query_proposal(revision, request)`. The
Engine reconstructs that exact immutable revision, overlays its replacement
bytes on the retained base snapshot, and compiles the projected material
through the same A1c metadata, policy-impact, graph, Router, coverage, and
repository-coverage owners. Route, read, and related use one shared navigation
implementation with authority-specific result projection. Proposal results and
continuations are anchored to the revision, identify projected content as
`projection`, and expose no snapshot child or inspect handle. Historical
revision queries remain stable after proposal-head movement. There is no
second parser, graph, Router, content store, cache, or proposal-as-snapshot
conversion.

Proposal IDs are unique lifecycle identities (`proposal:v1:<uuid4>`). Initial
revision IDs are content-bound identities over proposal ID, ordinal, base
snapshot, normalized replacement material, semantic proposals, and the
Authoring contract version. A proposal is a snapshot-dependent aggregate root
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

The public interface declares `standards.proposal.author` and
`standards.proposal.read` capabilities at the same deployment boundary that
owns the existing A1c capabilities; the domain does not add a second ambient
authorization mechanism. Interface schema v15 adds proposal content query
without changing the A1c request/result promises, existing handle versions,
Authoring material identity, or store schema. This decision does not yet add
projected analysis, review/readiness, Git publication, or recovery. The tested
P5C forwarding capability is intentionally not
productionized because no real caller needs a second eight-method A1c surface.

Standards graphs remain exclusively standards-domain authority. A2 consumes
them through the accepted A1c analysis semantics when evaluating proposed
standards content; it does not use them as an Engine implementation registry.
Engine feature sources, tests, proposal roots, and revision roots do not become
standards-graph or policy-impact-graph nodes merely because they implement or
verify A2.
