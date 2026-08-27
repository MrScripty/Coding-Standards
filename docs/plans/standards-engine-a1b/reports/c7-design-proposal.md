# Standards Engine A1b Candidate C7 Design Proposal

**Status:** Proposed C7 planning authority; pending content-bound review

**Reviewed planning boundary:** commit
`9794b92708aad42c4838f9ad5c6b78e3984d73b3`, tree
`0f7bc73dcaf6c7cacf348c6f8de50ff5f41928c5`

**Lifecycle effect:** Candidate C6 is rejected and superseded by this blocked
C7 replacement. Implementation remains unavailable until the revised plan,
ADR, and cited evidence receive one content-bound review with no blocking
finding.

## Purpose

C7 retains A1b's durable corrections while simplifying the authority model
that accumulated through candidates C through C6. It is informed by the
[C6/C7 history research](c6-c7-design-history-research.md) and the accepted
authority-scope standards.

The design keeps:

- the maintained Draft 2020-12 validator;
- separate schema, domain, and identity semantics;
- generated public request and result types;
- one immutable A1 analysis state and handle;
- direct storage for every inspectable object;
- exact owner codec and import membership;
- explicit policy-impact and coverage authority;
- transition-only provider and authorization authority;
- atomic public cutover; and
- cold-process reconstruction without ambient state.

C7 changes C6 in four material ways:

1. an ExecutionClosure stores only qualified roots while its identity binds the
   canonical derived transitive set;
2. `NextOperation` remains structural guidance rather than authority for a
   future transition;
3. ContentSnapshot becomes a leaf mapping of logical repository paths to exact
   bytes, with capture facts separated from semantic identity; and
4. one gitignored SQLite database replaces the Linux-ext4 object-file
   publication protocol.

## Design Principles

1. Authored repository text remains Git authority. SQLite is not committed.
2. Semantic identity is independent of storage bytes, source locators, host
   operating system, caches, and implementation releases.
3. Every public handle resolves one directly stored immutable object.
4. Every stored object declares exact owner-extracted direct dependencies.
5. Roots select authority; one traversal derives closure; optional caches own
   no meaning.
6. Result projection reads stored objects and executes no live provider,
   authorization, source-capture, owner-discovery, or current-code replay.
7. Platform-specific capture and persistence mechanics remain behind internal
   Interfaces and do not enter domain Modules.
8. Typed `invalid`, `unsupported`, and `unavailable` outcomes retain their
   accepted meanings.

## Module Graph

```text
standards_identity
  `-- standard library

standards_contracts
  |-- jsonschema
  |-- referencing
  `-- standard library

standards_authority
  |-- standards_identity
  |-- sqlite3 from the Python standard library
  `-- standard library

standards_metadata
standards_policy_impact
standards_graph
standards_analysis
  `-- construct owner-local authority values through their existing graph

standards_engine
  |-- composes all lower Modules
  |-- selects operation-qualified roots
  `-- adapts only generated public contracts
```

`standards_contracts` and `standards_authority` remain independent. Contracts
owns public wire representation. Authority owns immutable envelopes, direct
resolution, storage, and closure traversal. Domain Modules own semantic
construction, identity records, dependency extraction, and validation.

Authority exposes no public arbitrary-object, SQL, graph traversal, mutable
head, enumeration, or query Interface. Owner codec sets and operation
contracts remain closed machine-verified membership.

## Public Interface

C7 preserves the four-operation facade:

```python
query(view, request) -> NavigationResult | RejectedResult
prepare(request) -> AnalysisResult | RejectedResult
resolve(analysis_handle, submission) -> AnalysisResult | RejectedResult
inspect(handle) -> InspectionResult | RejectedResult
```

Requests and results use generated native types compiled from the canonical
JSON Schema and closed interface declaration. Internal domain values,
dependency exceptions, SQLite exceptions, and platform exceptions cannot
cross the facade.

Every result contains handles needed for exact continuation and inspection.
Pending and complete results are projections of one immutable AnalysisState;
they do not introduce packet or report identities.

## Contract Compiler

`standards_contracts` retains the C6 direction:

```python
contract = compile_contract(schema_source, interface_source)
value = contract.decode(definition_id, unknown_value)
json_value = contract.to_json_value(value)
artifacts = compile_projections(contract, targets)
```

`jsonschema.Draft202012Validator` remains the sole Draft validator. Generated
types call the same compiled validator and contain no keyword interpreter.
The JSON Schema owns serialized shapes only. The interface declaration owns
operation roots and capabilities. Domain Modules own semantic invariants,
identity, transitions, authorization, and policy meaning.

Generation freshness and semantic correctness remain separate evidence.
Repository tests exercise the selected schema profile and known regressions;
they do not reimplement or recertify Draft 2020-12.

## Equality And Identity

The domains remain separate:

| Domain | Owner | Rule |
| --- | --- | --- |
| JSON Schema instance equality | selected validator | Draft 2020-12 behavior |
| Applicability equality | `standards_applicability` | explicit typed domain rules |
| Semantic object identity | domain owner plus `standards_identity` | owner-selected material record with codepoint-preserving encoding |
| Domain ordering and deduplication | domain owner | typed keys |
| Content bytes | content producer | exact bytes and SHA-256 |
| SQLite row equality | `standards_authority` Adapter | exact handle and envelope BLOB equality |

SQLite collation, row order, page format, transaction IDs, schema version,
database path, and SQLite release never decide domain equality or identity.

## Immutable Authority Objects

Every object retains one closed envelope:

```text
AuthorityObjectEnvelopeV1 {
  object_kind,
  semantic_id,
  storage_format,
  direct_dependencies,
  payload_contract,
  payload
}
```

The owning codec:

- validates one closed payload;
- constructs its material semantic identity record;
- extracts exact direct dependencies;
- declares allowed dependency kinds; and
- decodes the typed value.

Authority verifies canonical envelope bytes, exact owner membership, owner
recomputed semantic identity, extracted dependency equality, dependency
existence and kind, and acyclicity. It then stores the canonical envelope BLOB
under its handle. Every child object remains directly stored; aggregate-root
scans and owner maps remain prohibited.

Each public owner root exports exactly one closed codec set. This table is
planning evidence, not a second runtime registry; Verification derives and
compares it with the executable owner exports.

| Owner | Object kind | Payload contract | Identity domain | Allowed direct dependency kinds |
| --- | --- | --- | --- | --- |
| Authority | `content-snapshot` | `content-snapshot.v2` | `coding-standards:content-snapshot:v2` | none |
| Authority | `execution-closure` | `execution-closure.v2` | `coding-standards:execution-closure:v2` | every other kind in this closed table |
| Metadata | `canonical-standards-corpus` | `canonical-standards-corpus.v1` | `coding-standards:canonical-standards-corpus:v1` | `content-snapshot` |
| Policy Impact | `compiled-policy-impact` | `compiled-policy-impact.v1` | `coding-standards:compiled-policy-impact:v1` | `content-snapshot`, `canonical-standards-corpus` |
| Standards Graph | `standards-graph` | `standards-graph.v1` | `coding-standards:standards-graph:v1` | `canonical-standards-corpus`, `compiled-policy-impact` |
| Analysis | `routing-projection` | `routing-projection.v1` | `coding-standards:routing-projection:v1` | `content-snapshot`, `canonical-standards-corpus` |
| Analysis | `coverage-horizon` | `coverage-horizon.v1` | `coding-standards:coverage-horizon:v1` | `content-snapshot`, `canonical-standards-corpus`, `compiled-policy-impact`, `standards-graph` |
| Analysis | `analysis-context` | `analysis-context.v1` | `coding-standards:analysis-context:v2` | `canonical-standards-corpus`, `routing-projection`, `standards-graph`, `compiled-policy-impact`, `coverage-horizon` |
| Analysis | `fact-requirement` | `fact-requirement.v1` | `coding-standards:fact-requirement:v2` | `analysis-context`, `routing-projection`, `compiled-policy-impact` |
| Analysis | `provider-authority` | `provider-authority.v1` | `coding-standards:provider-authority:v1` | `content-snapshot`, `canonical-standards-corpus`, `routing-projection`, `compiled-policy-impact`, `standards-graph`, `coverage-horizon`, `analysis-context`, `fact-requirement` |
| Analysis | `authorization-grant` | `authorization-grant.v1` | `coding-standards:authorization-grant:v1` | none |
| Analysis | `fact-observation` | `fact-observation.v1` | `coding-standards:fact-observation:v2` | `fact-requirement`, `provider-authority`, `authorization-grant` |
| Analysis | `coverage-view` | `coverage-view.v1` | `coding-standards:coverage-authority-view:v3` | `canonical-standards-corpus`, `compiled-policy-impact`, `standards-graph`, `coverage-horizon` |
| Analysis | `coverage-requirement` | `coverage-requirement.v1` | `coding-standards:coverage-audit-requirement:v3` | `coverage-view` |
| Analysis | `coverage-attestation` | `coverage-attestation.v1` | `coding-standards:coverage-attestation:v3` | `coverage-requirement`, `authorization-grant` |
| Analysis | `coverage-certificate` | `coverage-certificate.v1` | `coding-standards:consumer-coverage-certificate:v3` | `coverage-view`, `coverage-requirement`, `coverage-attestation` |
| Analysis | `analysis-root` | `analysis-root.v1` | `coding-standards:analysis:v4` | `execution-closure`, `analysis-context`, `fact-observation`, `coverage-attestation` |
| Engine | `operation-authority-contract` | `operation-authority-contract.v2` | `coding-standards:operation-authority-contract:v2` | none |
| Engine | `standards-authority-view` | `standards-authority-view.v1` | `coding-standards:standards-authority-view:v1` | `content-snapshot`, `operation-authority-contract`, `canonical-standards-corpus`, `routing-projection`, `standards-graph`, `compiled-policy-impact`, `coverage-horizon` |
| Engine | `navigation-result` | `navigation-result.v1` | `coding-standards:navigation-result:v1` | `execution-closure` |
| Engine | `policy-inspection` | `policy-inspection.v1` | `coding-standards:policy-inspection:v2` | `execution-closure`, `canonical-standards-corpus` |
| Engine | `relationship-inspection` | `relationship-inspection.v1` | `coding-standards:relationship-inspection:v2` | `execution-closure`, `standards-graph`, `compiled-policy-impact` |

Identity, Contracts, Applicability, and repository-neutral Graph Engine own no
persisted kind. Adding, removing, renaming, or transferring a kind, payload
contract, identity domain, or allowed dependency is a re-plan trigger.

## SQLite Durable Object Store

Git continues to store human-authored Markdown, TOML, JSON Schema, fixtures,
attestations, plans, and ADRs. SQLite stores machine-managed
immutable objects and generated state. The database and its journal files are
gitignored.

The internal storage Interface remains small:

```python
stored = store.get(handle)
result = store.put_if_absent(handle, envelope_bytes)
```

The initial logical schema is intentionally not a domain model. SQLite's
`application_id` and `user_version` header fields are the sole database-kind
and schema-version authorities; no metadata row repeats them:

```sql
PRAGMA application_id = 1397047601; -- 0x53454131, "SEA1"
PRAGMA user_version = 1;

CREATE TABLE authority_objects (
    handle TEXT COLLATE BINARY PRIMARY KEY,
    envelope BLOB NOT NULL,
    CHECK (typeof(handle) = 'text'),
    CHECK (typeof(envelope) = 'blob')
) WITHOUT ROWID;
```

No semantic payload field is projected into SQL columns. No dependency table,
closure table, latest-state pointer, mutable status, timestamp, source path, or
owner table is admitted initially.

Rows are immutable. Authority validates the envelope kind against the typed
handle before SQL and after every read; SQLite does not repeat that projection.
`put_if_absent` starts one explicit write transaction, inserts an absent
handle, and verifies exact existing bytes on conflict.
Identical bytes are idempotent success; different bytes are
`IDENTITY.COLLISION` and `invalid`. The Adapter exposes no update or delete
operation. Database triggers reject accidental updates or deletes to the
object table.

The database is a mutable container of immutable values, not a mutable
semantic head. Dependencies publish before dependents. A failed root
transaction may leave unreachable immutable objects but cannot publish a root
whose dependencies are absent.

The selected initial SQLite profile and remaining platform evidence are
defined by the [SQLite storage audit](c7-sqlite-storage-audit.md).

## Roots-Only Execution Closure

Every semantic object still stores exact direct dependencies. An
ExecutionClosure stores only operation-qualified roots:

```text
ExecutionClosureV2 {
  operation: route | read | related | analysis,
  roots: set<ExecutionAuthorityRoot> by
    (side, role, object_kind, semantic_id)
}
```

The Authority implementation owns one internal iterative traversal:

```text
D = canonical_transitive_closure(roots, immutable_store)

closure_id = H(
  execution-closure-domain-v2,
  operation,
  canonical-qualified-roots,
  D
)
```

The closure payload does not repeat `D`, but its identity binds `D`. Resolution
re-traverses stored direct dependencies and recomputes the handle. A missing
object is `unavailable`; a cycle, kind mismatch, identity contradiction, or
different derived set is `invalid`.

The closure envelope's direct dependencies equal the unique unqualified root
references. The qualified payload roots retain operation side and role; the
envelope references establish stored dependency existence and kind.

Authority owns traversal mechanics only. Engine and Analysis own root
selection. No generic graph-traversal Interface becomes public.

The flattened set may later be cached by closure handle. Such a cache is
discardable, cannot complete missing authority, and must reproduce the closure
handle before use. C7 implements no closure cache until measured performance
evidence demonstrates a need.

The C6 repeated dependency list was generated by the same traversal and was
not an independent omission oracle. C7 proves completeness through independent
fixture graphs, execution-consumption instrumentation, missing/extra edge
mutations, dormant-transition scenarios, and cold-process reconstruction.

## Operation Authority

Engine owns one executable `operation-authority-contract.v2` implementation
and four immutable records:

```text
OperationAuthorityContractV2 {
  contract_id,
  operation: route | read | related | analysis,
  required_view_roles: set<RoleKindRequirement> by role,
  allowed_dynamic_roles: set<RoleKindRequirement> by role
}
```

| Contract | Exact required view roles |
| --- | --- |
| `operation-contract.route.v2` | metadata -> canonical-standards-corpus; routing -> routing-projection; graph -> standards-graph |
| `operation-contract.read.v2` | metadata -> canonical-standards-corpus; graph -> standards-graph |
| `operation-contract.related.v2` | metadata -> canonical-standards-corpus; graph -> standards-graph |
| `operation-contract.analysis.v2` | metadata -> canonical-standards-corpus; graph -> standards-graph; policy-impact -> compiled-policy-impact; coverage -> coverage-horizon |

The analysis contract alone permits dynamic roles for analysis context, fact
requirements, observations, coverage objects, decisions, and actually
consumed provider or authorization objects. Its exact role-kind set is part of
the record. No ambient catalog can add a role.

The Engine-owned coherence algorithm requires each view to select exactly one
contract for each family and exactly the union of their required semantic
roles. Contract operation, role, kind, and cardinality must match exactly.
Owner-extracted edges must be:

```text
metadata      -> content
routing       -> content, metadata
policy-impact -> content, metadata
graph         -> metadata, policy-impact
coverage      -> content, metadata, policy-impact, graph
```

Analysis views select the same analysis-contract semantic ID. Static roots
come from the selected contract. Dynamic roots exactly equal qualified
dependencies returned by Analysis `AuthorityBoundValue`s. Missing referenced
content is `unavailable`; absent or extra roles, wrong kinds, conflicting
selections, cycles, or edge contradictions are `invalid`; an unknown
well-formed contract is `unsupported`.

Owner-local codec sets remain executable authority exported by each owner.
The composition root injects their exact closed tuple explicitly. Verification
derives the codec inventory, four operation records, facade mapping, and
structural-edge matrix from those executable owners; no central handwritten
codec manifest or runtime discovery becomes a second authority.

Facade mapping is fixed: query variants use route, read, or related;
`prepare` and `resolve` use analysis; `inspect` directly resolves the addressed
object and has no operation contract. Navigation roots use side `current`.
Analysis roots use sides `accepted` and `proposed`, with the common contract
rooted once on side `transition`.

## Standards Authority View

StandardsAuthorityView remains a reference-only composition value selecting:

- one ContentSnapshot;
- owner-local compiled semantic objects; and
- one operation contract for each of the four authority families.

It owns stable role selection and composition coherence. It contains no copied
semantic payload, provider, authorization decision, version bag, executable
behavior, or complete-operation identity. Results bind only their material
operation closure.

## Leaf-Only Content Snapshot

C7 separates immutable selected content from the recipe and provenance used to
capture it:

```text
RepositoryPathV1 {
  components: nonempty tuple<UnicodeScalarString>
}

CaptureRequestV1 {
  files: nonempty set<RepositoryPathV1> by path
}

ContentSnapshotV2 {
  files: nonempty set<(RepositoryPathV1, exact_bytes)> by path
}
```

`/` is the canonical serialized separator; it is not a native path operation.
Components are valid UTF-8 Unicode scalar sequences whose encoding is 1 to 255
bytes. Empty components, `.`, `..`, NUL, `/`, lone surrogates, `.git` control
paths, and duplicate paths reject. Backslash is an ordinary scalar on the
admitted Linux profile. The contract performs no Unicode normalization or
case folding. Components sort by Unicode scalar value and a prefix sorts
before its descendants. Native names that cannot round-trip exactly are
`unsupported`; two native names mapping to one logical path are `invalid`.

Paths and decoded exact bytes are the complete identity record. Per-file
digest, byte length, and padded Base64 are verified storage and inspection
projections. Request order, directories, modes, capture Adapter, Git locator,
source root, capture time, and capture observations are not snapshot identity.

The request names exact regular-file leaves; capture performs no directory
recursion and has no exclusion language. Engine bootstrap derives the exact
file set from its captured discovery roots and requires snapshot keys to equal
that source closure. Symlinks, device files, sockets, cross-mount paths,
casefolded ext4 directories, and other non-regular entries are `unsupported`.
Nested Git content is flattened under its gitlink prefix after exact object
resolution. A missing nested database or object is `unavailable`; no nested
snapshot or boundary marker enters identity.

Equal logical path-to-byte maps produce one snapshot across Git and native
Linux/ext4 capture, source locations, and file modes.
Changing any selected path or byte changes snapshot identity.

This intentionally replaces A1 snapshot behavior. `scope`, exclusions,
inclusion reasons, directories, entry types, modes, symlink fields, Git versus
manifest inspection variants, source/tracking/commit/tree facts, gitlink and
worktree state, nested-snapshot fields, and snapshot version bags are deleted.
Exact file keys replace scope-membership evidence. Old handles and persisted
states are typed `unsupported`; no converter or compatibility path is admitted.

## Capture Sources And Provenance

One internal `CaptureSource` Interface produces bounded observations from:

- exact Git objects; or
- a supported native worktree.

Git capture resolves one revision to one commit OID and then reads and
hash-verifies only that commit's tree and blob objects. Modes `100644` and
`100755` are accepted as regular files. Worktree, index, status, and moved refs
are immaterial. Gitlinks use an explicit prefix-to-object-database map, follow
the parent tree's exact commit, and flatten selected descendants. Missing
objects are `unavailable`; malformed or hash-contradictory objects are
`invalid`; selected unsupported object types are `unsupported`.

Native Linux/ext4 capture opens the canonical absolute root component by
component from `/` with directory-relative `O_NOFOLLOW|O_CLOEXEC` operations.
It retains every traversed directory and selected file descriptor, requires
one local case-sensitive ext4 mount, and records mount ID, device, inode, type,
size, mtime, and ctime. It reads every file twice from the held descriptor,
then independently rewalks the root and every logical path and compares all
bindings. Publication requires equal manifests, bytes, bindings, and exact
request keys. A mismatch returns source-changed `unavailable` and publishes
nothing. The guarantee is endpoint-consistent capture, not proof that no
transient same-user mutation ever occurred.

`CaptureReceipt` is rejected because no semantic or audit consumer requires
durable source-to-snapshot lineage. Successful capture returns only the
snapshot handle. Bounded source observations remain failure diagnostics;
domain provenance from a snapshot path to a compiled semantic object remains.

## Platform Model

Semantic paths, object envelopes, closure identities, analysis identities, and
SQLite row values are platform neutral. Platform differences belong to:

- native `CaptureSource` Adapters;
- SQLite runtime and local-filesystem capability evidence;
- secure private store-root selection;
- dependency artifact locks; and
- required-real verification.

The admitted A1b target is Linux x86-64 on one local, case-sensitive ext4
filesystem with the exact CPython, SQLite, and dependency artifacts frozen by
Milestone 0. macOS, Windows, another architecture, another filesystem, or a
casefolded/cross-mount ext4 capture is a future re-plan trigger rather than an
initial implementation target.

Network and remotely synchronized filesystems are outside the initial SQLite
store contract. Unsupported aliases, links, reparse points, path mappings, or
filesystem capabilities produce typed outcomes rather than weaker fallback.

## Immutable Analysis State

A1 remains one pure immutable state transition:

```text
project(state, immutable_authority_resolver) -> AnalysisResult

advance(
  state,
  submission,
  trusted_execution_context
) -> successor AnalysisState
```

The public facade may keep `resolve(handle, submission)` because the bound
Engine supplies trusted execution context. A successful successor stores every
new material immutable provider, evidence, and authorization record. Failed or
unavailable transition authority publishes no successor.

AnalysisState stores:

- exact base and proposed material authority references;
- normalized changes and semantic proposals;
- dependency-valid fact observations;
- dependency-valid review dispositions;
- authored coverage attestations; and
- the roots-only AnalysisExecutionClosure handle.

Requirements, obligations, reading plans, certificates, completion proofs,
and next operations remain deterministic projections. Dormant-valid decisions
remain retained; only current material unresolved work blocks completion.

`NextOperation` is structural guidance over current work. It is not
authorization and does not require the current state to pre-bind fresh trust
for a hypothetical successor. A transition binds only the exact immutable
authority it actually consumes into the successful child.

A1 has no global latest head, supersession, temporal stale packet, or mutable
session. Independent valid submissions naturally produce independent child
states. A2 alone owns mutable proposal heads and compare-and-swap semantics.

## Consumed Trust Authority

Aggregate provider and authorization views are removed. A successful analysis
transition stores only the exact trust objects it consumed:

```text
ProviderAuthorityV1 {
  provider_id,
  semantic_revision,
  input_contract,
  evidence_contract,
  inputs: set<QualifiedAuthorityReference> by (side, role, kind, id)
}

AuthorizationGrantV1 {
  issuer,
  issuer_semantic_revision,
  grant_id,
  capability,
  decision: "allow",
  authorization_digest,
  revocation_digest
}
```

Provider direct dependencies exactly equal its unqualified inputs; its identity
includes the complete payload and those references. An authorization grant has
no authority-object dependency. Its two digests bind the exact adapter-validated
assertion and validity/revocation state without storing a live credential.

Observations, dispositions, attestations, and evidence bindings reference these
stored objects directly rather than repeating provider or issuer versions. The
trusted execution context contains explicitly injected provider and
authorization Adapters, never a discoverable registry. Denial is
`unauthorized`; unavailable trust publishes no successor; malformed or
conflicting trust is `invalid`. Deterministic no-observation creates no decision
or stored trust object.

`project(state, resolver)` accepts no execution context. `advance` projects the
parent, validates current work, obtains only currently required trust, stores
accepted direct trust objects, builds the child closure, and then publishes the
child. Provider, issuer, capability, or revocation changes cannot alter the
parent identity. No closure pre-authorizes a hypothetical successor.

## Inspection And Backup

`inspect(handle)` directly loads and validates the addressed object from
SQLite. It does not:

- scan analysis states;
- consult an owner map outside the closed codec registry;
- rerun current domain construction;
- read Git or a worktree;
- invoke providers or authorization services; or
- require a cache.

The database is not committed to Git. SQLite's backup operation may support
operator recovery while the database is open, but backup files are operational
copies of the store and are not semantic interchange or Git artifacts. A1b has
no export/import Interface because no external consumer or retained source
state requires one.

## Failure Semantics

| Condition | Outcome |
| --- | --- |
| malformed handle, contradictory object, cycle, wrong kind, hash mismatch, collision, corrupt database structure | `invalid` |
| well-formed unsupported contract, platform, path class, filesystem, SQLite runtime, dependency artifact, or object version | `unsupported` |
| missing object, missing nested content, source changed during capture, store busy past admitted bound, I/O failure, unavailable provider or authorization input | `unavailable` |

No outcome falls back to live source, current code reconstruction, another
store, another platform mechanism, or an old contract.

## Migration And Cutover

C7 remains a coordinated breaking replacement:

1. independently accept the identified material C7 plan and ADR content;
2. build foundations only in admitted staging paths;
3. freeze schema, interface, codec, operation, SQLite schema-v1, path, and
   Linux/ext4 target contracts;
4. inventory every public and persisted A1 consumer;
5. update schema, generated types, facade, domain producers, storage,
   inspection, tests, documentation, catalogs, relationships, and coverage in
   one production cutover;
6. delete the local validator, old identity encoder, split stores, directory
   object Adapter, dependency-list closure payload, old snapshots, owner maps,
   scans, copied version bags, old handle versions, and fallbacks; and
7. obtain independent content-bound implementation acceptance before A2 review.

SQLite database files are never migration artifacts in Git. Opening creates or
verifies exactly schema v1; any other well-formed schema is `unsupported`.
There is no migration framework, dual reader, or conversion path. Existing
retained database state discovered before cutover is a re-plan trigger; the
current inventory reports none.

## Verification Program

### Contract and identity

- selected-validator differential cases for the admitted schema profile;
- complete generated request/result/inspection closure;
- codepoint, Boolean/integer, Unicode, ordering, and owner-domain cases;
- stale generation separate from semantic conformance; and
- exact intended diagnostics for negative fixtures.

### Authority and closure

- closed codec membership and wrong-owner negatives;
- exact four-contract records, facade mapping, role cardinality, and structural
  edge equality derived from executable owners;
- direct-dependency extraction equality;
- independent chain, diamond, cycle, missing, wrong-kind, and conflict graphs;
- execution-consumption traces compared with selected roots;
- reachable and unreachable dependency mutations;
- dormant applicability and successor-only trust cases;
- parent identity stability under provider, issuer, capability, and revocation
  changes; independent children; unavailable trust; deterministic
  no-observation stability;
- deterministic ordering and identity under insertion reordering; and
- cold reconstruction with caches, source, providers, and authorization
  services absent.

### Snapshot and capture

- exact path and byte mutation identity;
- equal Git/native leaf maps produce equal identity;
- request order, mode, source root, Adapter, and locator changes preserve
  identity;
- UTF-8, normalization-distinct, case-distinct, collision, and unsupported
  native-path fixtures;
- Git object verification, moved-ref/worktree independence, and nested gitlink
  flattening;
- native delete, replacement, rename, parent replacement, symlink substitution,
  write/truncate/restore, file/directory ABA, and root-replacement cases; and
- exact captured-key/source-closure equality with no `CaptureReceipt`.

### SQLite persistence

- schema and runtime-profile checks;
- identical and conflicting concurrent inserts;
- application and process interruption before, during, and after commit;
- cold reopen and exact object verification;
- update/delete rejection;
- corrupted row, corrupt database, missing database, and I/O outcomes;
- exact schema-v1 initialization and other-schema rejection;
- no dependency on row order, collation, timestamps, or current process; and
- required-real Linux x86-64, case-sensitive local ext4 evidence.

### Integration

- all public operations return only generated result variants;
- every inspectable handle resolves directly;
- operation dependency mutations affect only actual consumers;
- policy-impact and coverage subjects reconcile exactly;
- old implementations and compatibility paths are unreachable; and
- broad package, declarative, retained migration, and diff checks pass.

## Historical Regression Guard

C7 must not repeat:

- A1 live worktree reads or hidden session state;
- incomplete generated result semantics;
- local JSON Schema keyword or equality ownership;
- aggregate-only child lookup;
- private imports or filesystem-discovered registries;
- C4 copied version bags;
- C5 complete-view invalidation, current-only closure, or ambient role rules;
- C6 pre-authorization of hypothetical successors;
- mutable catalog totals as acceptance oracles; or
- generated evidence treated as independent semantic authority.

## Rejected Alternatives

### Commit SQLite to Git

Rejected because database page churn is not reviewable or mergeable authority.
Git owns authored text and migration source; SQLite owns local machine-managed
state.

### Replace authored declarations with SQL rows

Rejected because standards, relationships, attestations, and plans require
human review, diffs, merge behavior, and explicit authorship.

### Keep the native ext4 object-file store

Rejected as the preferred direction because it retains application-owned
staging, hard-link publication, locking, synchronization, cleanup, and recovery
that SQLite already provides behind one smaller Adapter. Other platform stores
are not part of A1b.

### Recursively redefine every semantic object ID

Rejected because making every owner semantic ID include transitive envelope
dependencies broadens identity coupling. ExecutionClosure alone hashes its
canonical derived dependency set.

### Persist the flattened closure set as authority

Rejected because it duplicates object direct dependencies and traversal.
Optional verified caching is sufficient if measurement later requires it.

### Support arbitrary raw-byte paths immediately

Rejected because Windows and many domain consumers require a Unicode logical
path contract. Unsupported non-round-trippable paths are simpler than making
every consumer byte-aware without a demonstrated requirement.

## Remaining Admission Evidence

The material design decisions are closed. The admission content set now:

1. revises and freezes the proposed v11 schema while retaining the unimplemented
   public version numbers;
2. records every removed snapshot/storage/closure/trust field and its update,
   retirement, or unsupported disposition in the consumer inventory;
3. fixes the SQLite application ID, schema, pragma profile, capability floor,
   5000-millisecond busy bound, private-root contract, ext4 detection, and
   required-real crash evidence;
4. assigns executable codec sets to owner roots and executable operation,
   facade, role, and structural-edge contracts to Engine, with aggregate
   evidence mechanically derived by Verification; and
5. updates the A1b write sets, policy-impact migration, and final coverage
   sequence for SQLite, roots-only closure, consumed trust, and snapshot v2.

## Current Recommendation

Proceed with one blocked C7 planning candidate and one content-bound review of
its complete material semantics. Do not modify A1 runtime, policy metadata,
coverage attestations, or A2 until the remaining evidence is assembled and C7
is admitted with no blocking finding.
