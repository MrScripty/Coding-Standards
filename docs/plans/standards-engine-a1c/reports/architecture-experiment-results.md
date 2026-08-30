# A1c Architecture Experiment Results

**Status:** `Implemented` for the bounded architecture experiments

**Prototype:** [snapshot-aggregate-prototype.py](snapshot-aggregate-prototype.py)

## Executed Boundary

Run from the repository root:

```bash
python3 docs/plans/standards-engine-a1c/reports/snapshot-aggregate-prototype.py
```

The self-checking prototype uses one disposable temporary SQLite file and
prints the complete relevant state after every transition. It imports no A1b
production package and creates no retained database.

## Results

| Experiment | Result | Disposition |
| --- | --- | --- |
| A1C-E1 snapshot Interface | Tagged and explicit Interfaces can drive equal behavior over one internal Snapshot Module. Explicit methods keep create, find, delete, and undelete schemas, authorization, and typed outcomes distinct; the tagged operation adds request-kind dispatch without hiding any domain concept. | Select explicit methods over one internal Snapshot Module. Four caller commands do not create four internal authority owners. |
| A1C-E2 identity separation | Two roots created over the same current canonical bytes received distinct snapshot handles and one shared content identity. Quarantining or purging one did not affect the other. | Accept content identity plus independent snapshot-root lifecycle identity as the candidate model. |
| A1C-E3 aggregate persistence | Two analysis aggregates retained children inside aggregate payloads. A derived child index supported cold inspection without independently storing each child as semantic authority. Closed-file copying preserved the aggregate, and an injected interruption rolled back a partial purge. | Select one SQLite-backed snapshot aggregate with derived child indexes. Keep SQLite behind the Snapshot Module rather than exposing a generic object repository or public persistence Seam. |
| A1C-E4 discovery summary | Two equal-content roots created at one logical time had equal provenance but distinct store-assigned handles. The agent uses those handles, not the shared content hash, to address snapshots and attach dependent work. | Select handle, lifecycle, source-commit provenance, creation time, and conditional purge deadline. Do not expose the content hash as snapshot identity or add project labels the engine cannot authoritatively interpret. |
| A1C-E5 operation/version authority | Both public Interface candidates reused one Snapshot Module and one state model. A1b's operation contracts duplicate role/cardinality declarations already selected by operation implementation and exact stored dependencies. | Retain one compiled public facade contract plus domain-owned material identity and compatibility constants. Do not persist independently identified per-operation authority objects when no independent consumer or overlap promise exists. |
| A1C-E6 evidence substitution | External-schema, identity-separation, transaction, cold-reopen, failure-outcome, lifecycle, platform, and false-empty coverage evidence remain necessary. Backup/restore, independently durable child authority, per-operation authority-object closure, and repository-global runtime invalidation were not needed by the exercised workflows. | Replace mechanism-shaped evidence with the claim-matched portfolio below. Keep historical evidence until the replacement implementation proves the same reachable failures. |

## Observed Cases

The executable probe passed these named cases:

- `same-content-isolation`;
- `active-discovery`;
- `unique-id-addressing`;
- `child-inspection`;
- `quarantined-discovery`;
- `undelete`;
- `cold-reopen` without reading the canonical source;
- `closed-store-copy`;
- `interrupted-purge-rollback`;
- `expiry-and-shared-content`;
- `transactional-purge`;
- `interface-parity`;
- `coverage-local-invalidation`; and
- `invalid-config-rejected`.

The final first-root purge retained one canonical-content row because the
second root still owned it. Purging the second root removed the content,
aggregate records, and derived child index. Minimal tombstones retained only
the purged snapshot IDs and purge times so later use could return
`SNAPSHOT.EXPIRED` and prevent identity reuse without retaining deleted
standards, decisions, or evidence.

## Snapshot Identity Clarification

The earlier experiment interpretation incorrectly treated rediscovery as a
request for the engine to infer which project a snapshot belongs to. The
product requires no such inference.

The store assigns every snapshot root a unique opaque ID. Agents use that ID to
address the root and every linked change set, analysis, and artifact. A content
hash answers only whether immutable canonical bytes can be shared internally.
It is not a snapshot handle, ownership key, display label, or caller context.

One store may therefore contain:

```text
snapshot:01 -> content:abc -> change sets and analyses owned by root 01
snapshot:02 -> content:abc -> change sets and analyses owned by root 02
```

Deleting root 01 cannot affect root 02. The content row remains while any root
references it. `find_snapshots` lists unique root IDs and contextual lifecycle
and provenance fields. If a caller discards the ID that identified its own
workflow, Coding Standards may list and inspect retained roots, but it does not
guess project meaning. Empty equal-content roots contain equivalent standards
content and no dependent work, but remain distinct lifecycle roots.

Project IDs, mutable labels, paths, and hidden caller catalogs are therefore
unnecessary. A harness may retain its own association with a snapshot handle,
but that association does not become Coding Standards authority.

## Selected Snapshot Interface

The public candidate adds four explicit methods beside the inherited analysis
and navigation behavior:

- `create_snapshot()`;
- `find_snapshots(lifecycle="active")`;
- `delete_snapshot(snapshot_id)`; and
- `undelete_snapshot(snapshot_id)`.

The methods share one internal Snapshot Module and one lifecycle state model.
They remain separate because their inputs, authorization, effects, and result
variants differ. A tagged `snapshots({kind: ...})` method makes the caller learn
the same concepts plus a dispatch discriminant and therefore has less Depth.

`SnapshotSummary` contains the unique handle, lifecycle, source commit,
creation time, and purge deadline when quarantined. Source commit and time are
provenance and display context only. They do not participate in lifecycle
identity and cannot replace the handle.

## Persistence And Coverage Results

The SQLite candidate passed current-version close/reopen, closed-file copying,
foreign-key cascade, equal-content reference retention, and injected
interruption rollback. The experiment supports one SQLite-backed Snapshot
Module. It does not justify a public repository Protocol, a second memory
Adapter, an Engine backup/restore Interface, or a finalized physical schema.
Temporary SQLite files are sufficient for focused tests.

The coverage probe projected only authored coverage-relevant inputs: policy
subject state, relationships, fact contract, and independently declared audit
horizon members. An unrelated repository member changed without invalidating
the coverage identity. A selected horizon member or relationship change did
invalidate it. Snapshot-root IDs did not enter the semantic projection; roots
own lifecycle, while exact content and relationship state own coverage
meaning.

This resolves A1C-007 as follows:

- preserve exact current-engine replay from immutable snapshot content and
  retained decisions;
- bind coverage to its typed dependency projection;
- keep the repository-global suite-input digest as verification freshness
  evidence, not product analysis identity; and
- preserve independent coverage audits so an empty graph result never proves
  complete consumer discovery by itself.

### Operation Dependency Closure

Removing persisted `OperationAuthorityContract` objects does not make
dependency closure descriptive or optional. Each domain-owned immutable state
or result type contains exact typed references to every authority that can
affect its reproduction. Its constructor enforces required references and
cardinality. The generic closure walker follows those references and rejects a
missing, contradictory, cyclic, or unsupported dependency.

The removed object is the second role/cardinality declaration for an operation,
not the closure invariant. Adding a dependency changes the owning domain type,
constructor, identity, and focused replay evidence. It does not require a
separately persisted operation record, role registry, view selection, codec,
handle kind, or public inspection variant.

## Composed Design Admission

### Concerns And Owners

| Concern | Owner and lifecycle | Interface knowledge retained | Reason and deletion result |
| --- | --- | --- | --- |
| Draft contract semantics and generated public algebra | Contracts; changes with the public representation or selected Draft behavior | Canonical schema, operation declaration, compiled validator, generated request/result projection | Retain. Deletion recreates schema interpretation and projection in the facade and tests. |
| Identity framing and hashing | Identity; changes only with an owned identity domain | Representation-preserving encoding and domain-labelled hashing | Retain. Deletion redistributes byte framing and collision rules across every identity owner. |
| Snapshot content and lifecycle aggregate | Snapshot Module; root lifetime begins at creation and ends after quarantine expiry | Current-source capture, unique root IDs, internal content deduplication, discovery, resolution, aggregate persistence, quarantine, undelete, purge | Retain and deepen around SQLite. Deletion forces callers to store bytes, coordinate children, and implement lifecycle transitions. |
| Metadata, applicability, graph, and policy-impact semantics | Existing domain owners; immutable per captured content or projection | Typed compile and evaluation Interfaces over exact snapshot content | Retain domain ownership. Snapshot storage references their values without acquiring their semantics. |
| Analysis state and coverage decisions | Analysis; immutable state transitions under one snapshot root | Inputs and dependency-valid decisions are stored as aggregate records; requirements, obligations, reading plans, certificates, and results are derived | Retain one analysis kernel. Delete independent storage authority for each derived child while preserving inspectability through a derived index. |
| Agent-facing composition | Standards Engine facade; one deployed current contract | Eight explicit operations, generated values, typed failures, current authorization and provider execution context | Retain as the composition root. It must not own domain semantics or expose SQLite, codecs, content hashes, or dependency-role registries. |
| Verification | Verification owner; retained per reachable claim | External Draft conformance, generated freshness, identity fixtures, domain behavior, aggregate lifecycle, cold reopen, platform, and false-empty coverage | Retain claim-matched evidence. Delete mechanism tests when their mechanism is removed and a deeper Interface proves the same failure. |

### Knowledge And Dependency Direction

Agents know only typed requests/results, unique handles, lifecycle outcomes,
and evidence/authorization requirements. They do not know paths, SQL tables,
content hashes, codecs, authority-role cardinalities, child cleanup order, or
Git object mechanics.

Peer domain Modules receive immutable content or typed owner values. They do
not depend on SQLite or the facade. The Snapshot Module stores opaque
domain-owned aggregate payloads and derived lookup indexes without interpreting
their semantics. The Engine composition root knows the configured canonical
source, Snapshot Module, compiled contracts, domain compilers, analysis kernel,
and current execution-context Adapters. This composition knowledge is
necessary; it is not persisted as a second semantic authority.

The dependency direction is:

```text
Contracts -> maintained Draft validator and Identity
Snapshot Module -> Identity and SQLite
Analysis kernel -> Identity, Metadata, Applicability, Graph, and Policy Impact
Standards Engine facade -> Contracts, Snapshot Module, and Analysis kernel
```

The Snapshot Module does not depend on Contracts, Metadata, Graph, Analysis,
or the Standards Engine. Domain codecs, when required for aggregate payloads,
remain owned and supplied by their domains rather than becoming storage
semantics.

### Representative Change Locality

| Change | Semantically required owners | Owners not invalidated |
| --- | --- | --- |
| Add one public result field | Owning domain projection, canonical schema/interface declaration, contract compiler output, facade mapping, focused consumer evidence | Snapshot storage and unrelated domain identities unless the field changes their persisted meaning |
| Add one private stored field | Snapshot Module and SQLite schema/current-version tests | Public schema, agent tools, navigation, and analysis semantics |
| Add one inspectable derived analysis concept | Analysis aggregate projection, derived child index, inspect result variant if publicly required | Generic storage-kind registry, independent child codec/envelope, snapshot identity, unrelated operations |
| Change one identity rule | Identity plus the exact domain identity owner and its consumers | JSON Schema equality, lifecycle root IDs, unrelated domain identities |
| Change snapshot lifecycle result semantics | Snapshot Module, public snapshot operation contract, facade projection, lifecycle evidence | Navigation and analysis identities, metadata, graph, policy impact, coverage |
| Change one analysis decision dependency | Analysis state identity/transition and focused coverage or obligation evidence | Snapshot content identity, snapshot lifecycle, query/read operation contracts |

### Removed Or Declined Machinery

- Do not persist `OperationAuthorityContract` values. Operation dependencies
  are exact typed references in domain-owned state and are traversed through a
  generic closure walker; current cross-engine compatibility is deliberately
  unsupported.
- Do not store every inspectable child as an independent authority object.
  Store the owning aggregate once and derive indexes and projections.
- Do not expose a generic Authority repository, memory/SQLite Adapter pair, or
  backup/restore Interface merely for test symmetry or possible future reuse.
- Do not put content hashes, project identities, caller labels, or Git object
  IDs into snapshot-root identity.
- Do not bind product coverage to the repository-global suite-input digest.
- Do not retain custom package or governed-source machinery as product runtime
  authority. Repository policy enforcement remains Verification-owned and must
  justify itself by its own reachable claims.

### Failures And Inherent Complexity

Canonical-source unavailability belongs to the source Adapter. Unknown,
quarantined, expired, corrupt, or unsupported-store outcomes belong to the
Snapshot Module. Public shape invalidity belongs to Contracts and the facade.
Unresolved facts and obligations belong to Analysis. Current authorization
belongs to the execution context; a stored handle never grants access.

The inherent complexity is immutable content capture, unique lifecycle roots,
aggregate retention, typed public contracts, external schema conformance,
domain compilation, graph-guided analysis, evidence-backed decisions, and
current authorization. The candidate contains that complexity in deep owners
and removes independent lifecycle, version, and storage machinery that had no
demonstrated caller.

## Evidence Portfolio

| Claim | Retained deciding evidence | Removed or replaced evidence |
| --- | --- | --- |
| Public values follow Draft 2020-12 | Maintained Draft validator through the production Adapter plus external differential cases | Multiple local validators agreeing with each other |
| Generated Interface is fresh and semantically complete | Operation-reachable contract compilation, semantic conformance, and freshness as separate checks | Field-name-only generation checks |
| Identity domains are exact | Representation/framing fixtures and domain-owned equality and ordering cases | One canonical serializer used as schema equality or deduplication authority |
| Snapshot aggregates survive and delete correctly | Unique-ID, equal-content, close/reopen, closed-copy, interruption rollback, quarantine, undelete, expiry, purge, and child-inspection cases | Independent persistence tests for every derived child and Engine backup/restore |
| Analysis is reproducible | Immutable snapshot plus stored input/decision aggregate, cold projection, and decision-branch cases | Direct storage, envelope, and codec tests for every projected requirement or certificate |
| Empty impact is trustworthy | Independent horizon audit, exact relationship/fact dependencies, and false-empty negative fixtures | Existing graph or catalog completeness treated as its own oracle |
| Supported platforms work | Real Linux, Windows, and macOS jobs against the selected SQLite and source behavior | Linux execution extrapolated to other platforms |

## Design Disposition

The bounded experiments select a coherent A1c architecture candidate, not a
production implementation. The next step requires a plan re-scope that admits
the superseding ADR and exact implementation-plan artifacts. Production source,
public schema, canonical policy, and A2 remain unchanged and unauthorized.

## Prototype Limits

- Canonical bytes are a bounded stand-in for complete corpus capture and
  validation.
- Authorization is represented by separate method boundaries, not a real
  authorization Adapter.
- Minimal tombstones preserve `SNAPSHOT.EXPIRED` and prevent ID reuse without
  retaining deleted authority. Their storage growth must be measured during
  implementation but does not require another lifecycle or public operation.
- The derived child index demonstrates lookup mechanics, not production scale
  or the complete analysis projection.
- The temporary SQLite experiment ran on Linux only and proves no Windows or
  macOS storage behavior.
- Change-set authoring remains outside A1c.

## Conclusion

The two-identity aggregate model survives unique-ID addressing, deletion,
cold-reopen, closed-copy, interruption, and locality tests and is materially
simpler than assigning an independent lifecycle to every child. The composed
candidate is ready for an ADR and planning re-scope, not production
implementation.
