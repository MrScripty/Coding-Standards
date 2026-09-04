# Standards Engine A1b Contract And Authority Foundations

**Status:** Accepted historically; runtime architecture superseded by A1c

[A1c](standards-engine-a1c.md) replaces this runtime architecture. This
decision and its acceptance evidence preserve the A1b design history;
consult the [decision index](README.md) for current architecture.

This decision supersedes the A1 contract-compilation, identity, snapshot,
storage, execution-closure, and public-projection architecture. It also
supersedes the C1 through C6 A1b planning designs. Its completed implementation
is recorded in the
[A1b plan](../archive/plans/standards-engine-a1b/plan.md). The implementation is
accepted at commit `84412f22fa9fe082f089eaa347c30c23f185ffee`, tree
`8e0f96a61fcea2398418b17d16a061c20f7463f5`, by the
[final content-bound acceptance](../archive/plans/standards-engine-a1b/reports/a1b-final-acceptance.md).

## Context

A1 proved the four-operation read-only Engine and immutable analysis state, but
its repair history exposed recurring boundary failures:

1. schema validation and generated Python models duplicated semantics;
2. identity canonicalization acquired JSON Schema equality behavior;
3. snapshots mixed source observations with immutable content;
4. inspectable values were split across stores and hidden process state;
5. copied version bags and complete authority views invalidated unrelated work;
6. provider and authorization authority was either ambient or over-aggregated;
7. cold reconstruction depended on loaders not identified by the handle; and
8. planning protocols acquired Git topology and lifecycle authority.

The accepted standards now require coherent ownership, lifecycle, deletion and
interface tests, exact authority scope, material version invalidation, and
commit boundaries owned by the Commit workflow. A1b must correct the system,
not preserve the repair machinery.

The historical analysis is recorded in:

- [A1b redesign brief](../archive/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md);
- [C6/C7 design history](../archive/plans/standards-engine-a1b/reports/c6-c7-design-history-research.md);
- [C7 design proposal](../archive/plans/standards-engine-a1b/reports/c7-design-proposal.md); and
- [C7 SQLite audit](../archive/plans/standards-engine-a1b/reports/c7-sqlite-storage-audit.md).

## Decision

### Public lifecycle

A1b preserves:

```text
query(request) -> NavigationResult | RejectedResult
prepare(request) -> PendingResult | CompleteResult | RejectedResult
resolve(analysis_handle, submission) -> PendingResult | CompleteResult | RejectedResult
inspect(handle) -> InspectionResult | RejectedResult
```

Analysis remains one immutable state machine. Pending and complete results are
projections of an AnalysisState and use its AnalysisHandle. A1b has no mutable
analysis head, packet/report store, global supersession, or temporal
`PACKET.STALE`. A2 separately owns mutable authoring coordination.

Public replacement is atomic at interface schema version 11, request contract
version 3, result projection version 3, public handle version 4, authority
envelope version 1, and identity encoding version 2. Analysis compatibility is
scoped independently by `analysis-root.v1`, identity domain
`coding-standards:analysis:v4`, handle schema 4, result projection 3, and
operation compatibility key `(analysis, 2)`. The shared
`operation-authority-contract.v2` payload contract owns only the stored record
shape; the former umbrella analysis contract/schema pair has no A1b successor.
These proposed versions may change only by re-planning before cutover. No
compatibility reader, writer, or converter is admitted.

### Module graph

```text
standards_identity
    standard library only

standards_contracts
    jsonschema
    referencing

standards_authority
    standards_identity
    sqlite3 from the standard library

domain Modules
    their existing dependencies
    standards_identity where identity is owned
    standards_authority where inspectable values are persisted

standards_engine
    composes all accepted lower Modules

standards_verifier
    validates package, export, entrypoint, contract, and repository closure
```

`standards_contracts` and `standards_authority` do not depend on each other.
The public JSON Schema owns serialized request/result shapes. Domain Modules
own semantic records and behavior. Authority owns storage integrity, not public
schema or domain meaning.

### Contract compiler

`jsonschema.Draft202012Validator` is the sole Draft 2020-12 validator. A1b
does not implement JSON Schema keywords or claim independent Draft
certification. The Contracts Module:

- loads and self-checks the canonical schema;
- resolves the closed local-reference graph through `referencing`;
- validates instances through the selected validator;
- compiles the admitted public projection profile;
- generates native request/result models and agent tools; and
- rejects unsupported reachable constructs before generation.

Generated freshness and semantic correctness are independent checks. Direct
validator and Adapter behavior are different entrypoints to the same external
validator, not independent conformance oracles.

Schema validation equality, applicability equality, identity encoding, and
domain ordering are separate contracts. JSON Schema strings compare according
to the selected Draft implementation. Identity encoding preserves codepoints.
Only a domain owner may normalize its semantic identity record.

### Identity

`standards_identity` owns domain-separated identity encoding v2. It encodes a
typed closed record without recursive Unicode normalization and hashes:

```text
domain separator
contract version
canonical typed record
```

Object keys, ordering, deduplication, aliases, and semantic equivalence remain
owned by the domain that defines them. The identity Module supplies encoding
and hashing, not cross-domain meaning.

### Immutable object envelope

Every persisted inspectable value uses:

```text
AuthorityObjectEnvelopeV1
  envelope_kind = authority-envelope
  envelope_version = 1
  object_kind: nonempty opaque Unicode-scalar string
  semantic_id: nonempty opaque Unicode-scalar string
  direct_dependencies: sorted unique AuthorityObjectReferenceV1[]
  payload_contract: nonempty opaque Unicode-scalar string
  payload: identity-v2 JSON-compatible typed value
```

Envelope bytes are exactly identity-v2 canonical typed encoding of this closed
seven-field object without the identity hash frame. References contain exactly
`object_kind` and `semantic_id`. Unknown fields, floats, noncanonical bytes,
duplicate or unsorted dependencies, and encoded envelopes larger than
67,108,864 bytes reject. Raw content is represented through owner-validated
padded Base64 inside the payload.

Envelope kind and version provide structural dispatch only. A well-typed
unknown kind or positive version is `unsupported`; malformed structure is
`invalid`. Object-kind and payload-contract values remain codepoint-exact
opaque identifiers owned by the injected codec sets. Authority compares and
dispatches them without normalizing them or inferring domain meaning.
`semantic_id` is likewise opaque to Authority: the repository requires exact
handle/envelope/reference equality, while the owning codec validates its
grammar and recomputes it from the owner-defined material identity record.

The envelope's `object_kind` must agree with the typed handle. The repository
validates envelope shape, dependency references, acyclicity, stored bytes, and
handle agreement. It does not interpret domain payloads.

Each owning Module exports one closed `AuthorityObjectCodecSet`. Its codecs
construct and validate payloads, compute semantic IDs, extract allowed direct
dependencies, and decode owner-typed values. Codec membership remains local to
the owner. Standards Engine composition injects an explicit closed tuple of
codec sets. Verification derives the aggregate kind/facade/dependency evidence
from those executable owners; there is no handwritten central codec manifest.

### SQLite repository

The durable adapter uses SQLite and stores only:

```sql
CREATE TABLE authority_objects (
    handle TEXT COLLATE BINARY PRIMARY KEY,
    envelope BLOB NOT NULL
) WITHOUT ROWID;
```

The envelope already owns kind, so SQL does not duplicate `object_kind`.
`put_if_absent(handle, envelope)` executes in one transaction:

1. verify typed handle, canonical envelope, codec identity, and dependencies;
2. insert when absent;
3. treat identical existing bytes as idempotent success; and
4. reject different bytes for the same handle as a contradiction.

Readers resolve exact handles and verify the returned envelope. The adapter
supports integrity checking, deterministic SQLite backup, offline restore to a
distinct absent store, crash recovery, and cold-process reopen. The default
store is `<repository-root>/.standards-engine/authority.sqlite3`; an explicitly
restored store is selected only through trusted Engine composition. Backup and
restore never overwrite or mutate the configured live store. The former store
remains rollback authority, and retention/deletion remains operator-owned. The
adapter does not expose scans or mutable indexes as semantic authority.

Required-real interruption evidence uses a capability-checked Linux `strace`
syscall-injection harness to deliver `SIGKILL` at the real SQLite `fsync` or
`fdatasync` reached during commit. It is test-only; production retains the
standard-library `sqlite3` Adapter and no custom VFS.

A1b admits SQLite schema v1 only. It has no schema migration framework,
semantic export/import, dual reader, checked-in database, or legacy-state
converter. Database files are local generated runtime state and are ignored by
Git. Backup preserves the database; it is not a domain transfer format.

### Content snapshots

The public content contracts are:

```text
RepositoryPathV1
  components: nonempty tuple<Unicode scalar string>

CaptureRequestV1
  files: nonempty set<RepositoryPathV1>

ContentSnapshotV2
  files: nonempty set<(RepositoryPathV1, exact bytes)>
```

A component's UTF-8 encoding must contain 1 through 255 bytes. Empty, `.`,
`..`, slash, NUL, lone surrogates, and repository-control `.git` paths
reject. Duplicate logical paths reject. Codepoints and case are preserved.
Ordering uses Unicode scalar sequence with a prefix before its extension.
Backslash is an ordinary scalar on the admitted Linux platform.

Snapshot identity binds only sorted logical paths and exact bytes. Base64,
digest, and byte length are verified serialized projections. Scope,
exclusions, directories, modes, symlinks, source roots, Git identities,
tracking state, inclusion decisions, worktree observations, and capture
receipts are not snapshot authority.

Bootstrap derives an exact file set and requires equality with the capture
request. Capture does not recursively discover files or interpret exclusions.

### Capture adapters

The Git adapter resolves one commit object ID, validates every traversed Git
object against its object ID, accepts regular file modes `100644` and
`100755`, and returns only requested bytes. A gitlink is traversed only
through an explicit prefix-to-object-database mapping; nested requested files
are flattened into their logical repository paths. The adapter reads no
worktree, index, or status.

The native adapter is admitted only for Linux x86-64 on a case-sensitive,
non-casefold ext4 mount. It:

1. starts from a retained descriptor for `/`;
2. uses descriptor-relative no-follow opens;
3. retains directory and file descriptors on one mount;
4. rejects symlinks, casefold mounts, cross-mount traversal, and nonregular
   files;
5. reads each file twice;
6. independently rewalks the complete request; and
7. requires endpoint metadata, descriptor identity, and bytes to agree.

Endpoint agreement prevents returned mixed endpoints but does not claim to
detect every transient same-user mutation that leaves identical final state.
Such a stronger guarantee is a re-plan trigger.

Both adapters produce identical ContentSnapshotV2 identity for identical path
and byte sets. Adapter identity and source locator do not enter the result.

### Authority views and operation contracts

A `StandardsAuthorityView` references owner-produced semantic authorities. It
contains no copied payload, version bag, provider decision, authorization
decision, or executable domain logic.

Standards Engine owns four executable `OperationAuthorityContractV2` values:

| Operation | Compatibility revision | Required role-to-kind pairs | Allowed dynamic role-to-kind pairs |
| --- | --- | --- | --- |
| route | 2 | metadata -> canonical-standards-corpus; routing -> routing-projection; graph -> standards-graph | none |
| read | 2 | metadata -> canonical-standards-corpus; graph -> standards-graph | none |
| related | 2 | metadata -> canonical-standards-corpus; graph -> standards-graph | none |
| analysis | 2 | metadata -> canonical-standards-corpus; graph -> standards-graph; policy-impact -> compiled-policy-impact; coverage -> coverage-horizon | context -> analysis-context; requirement -> fact-requirement; observation -> fact-observation; coverage-view -> coverage-view; coverage-requirement -> coverage-requirement; coverage-attestation -> coverage-attestation; coverage-certificate -> coverage-certificate; provider-authority -> provider-authority; authorization-grant -> authorization-grant |

The typed `(operation, compatibility_revision)` pair is the compatibility key;
there is no encoded selector string. Revisions are immutable, monotonically
allocated per operation, may contain gaps, and never imply compatibility by
numeric range. The Engine supports an explicit set of keys and never reuses a
retired key for different semantics or accepts unequal normalized promises
under one key. Each complete record independently receives an envelope
`semantic_id` under
`coding-standards:operation-authority-contract-identity:v1`. A view references
that exact stored object. A material compatibility change advances only the
affected operation's revision; any material record-content change changes its
content-addressed semantic ID. The payload contract
`operation-authority-contract.v2`, envelope version, SQLite representation, and
storage bytes do not enter that semantic identity.

Every required role has cardinality `1..1`. Analysis context has cardinality
`1..1`; every other allowed dynamic role has cardinality `0..*`. No `decision`
object kind exists: dispositions are fields of `analysis-root.v1`. Analysis has
no routing role or routing dependency.

The following structural role dependencies are derived review evidence from
the exact owner codec dependency contracts and owner-extracted references; they
are not fields of an operation-contract payload or a second runtime catalog:

```text
metadata -> content
routing -> content, metadata
policy-impact -> content, metadata
graph -> metadata, policy-impact
coverage -> content, metadata, policy-impact, graph
context -> metadata
requirement -> context, policy-impact
observation -> requirement, optional provider-authority, authorization-grant
coverage-view -> metadata, policy-impact, graph, coverage
coverage-requirement -> coverage-view
coverage-attestation -> coverage-requirement, authorization-grant
coverage-certificate -> coverage-view, coverage-requirement, coverage-attestation
provider-authority -> exact declared subset of content, metadata,
                      policy-impact, graph, coverage, context, requirement
authorization-grant -> none
```

The Engine validates operation, supported compatibility key, role, kind, and
cardinality through one generic coherence algorithm. Owner codecs own allowed
direct dependency kinds and extract each exact reference. Authority provides
generic reference traversal and does not own operation or dependency policy.
`inspect` directly resolves the identified object and therefore has no
operation-authority contract.

Navigation uses side `current`. Analysis roots use `accepted` and
`proposed`; contract-transition authority common to both sides remains
explicitly qualified.

### Roots-only execution closure

`ExecutionClosureV2` persists only a sorted unique set of qualified roots:

```text
(side, role, object_kind, semantic_id)
```

The selected operation contract is a root. Domain operations return
`AuthorityBoundValue` with their direct semantic dependencies. The kernel
derives transitive dependency set `D` by deterministic traversal through
owner-declared envelope references and validates all role, kind, side, cycle,
and coherence invariants.

Closure identity binds the root set and derived `D` under the closure contract
version. `D` need not be redundantly persisted as caller-authored authority;
it is reproducible from immutable objects. Missing objects, kind mismatch,
cycles, or a changed derived set reject.

The closure covers the current result or analysis state. It does not speculate
about every possible future submission. A successor transition identifies and
stores any newly consumed authority in the child state.

### Consumed trust authority

Providers return claims over declared immutable inputs. Analysis alone
validates a claim and constructs canonical observations.

```text
ProviderAuthorityV1
  provider_id
  semantic_revision
  input_contract
  evidence_contract
  inputs: sorted qualified authority references

AuthorizationGrantV1
  issuer_id: CanonicalId
  issuer_semantic_revision: integer >= 1
  grant_id: CanonicalId
  principal_id: CanonicalId
  capability: CanonicalId
  action: provide-fact | consumer-disposition | impact-disposition |
          coverage-attestation
  subject: AuthorizationSubjectV1
  authorization_contract = authorization-grant.v1
  authorization_evidence: nonempty sorted EvidenceReferenceV1[]
  revocation_authority_id: CanonicalId
  revocation_authority_semantic_revision: integer >= 1
  revocation_contract = authorization-revocation.v1
  revocation_evidence: nonempty sorted EvidenceReferenceV1[]
  revocation_state = not-revoked
  decision = allow

AuthorizationSubjectV1 =
  { kind: fact-requirement, id: FactRequirementId } |
  { kind: consumer-obligation, id: ObligationId } |
  { kind: impact-obligation, id: ObligationId } |
  { kind: coverage-requirement, id: CoverageRequirementId }

EvidenceReferenceV1
  id: CanonicalId
  digest: Digest
  provider_contract: CanonicalId
  provider_contract_version: NonEmptyString
```

Every grant, subject, and evidence value is a closed object. Subject kind must
match action exactly. Evidence is ordered and made unique by
`(provider_contract, provider_contract_version, id)`; digest is deliberately
excluded from that logical key, so repeated keys reject whether their records
agree or conflict. Values compare codepoint-for-codepoint without Unicode
normalization. The injected issuer Adapter, principal, capability, contracts,
evidence, exact evidence-byte digest, and immutable revocation proof must all
match. Denial or revocation is `unauthorized`; missing trust is `unavailable`;
contradiction is `invalid`; and an unknown well-formed contract is
`unsupported`. A1b admits no temporal or expiring grant.

A successful child state includes the exact provider and authorization objects
it consumed. A deterministic provider result of no observation stores no trust
object. Provider unavailability, unresolved immutable input, and undeclared
ambient input are distinct failures and never silently mean no observation.
Existing states and results replay without a live provider or authorization
service.

Analysis state retains all dependency-valid observations, dispositions, and
coverage attestations, including dormant-valid decisions. Materiality is
derived during projection. Invalid decisions are removed when constructing a
successor; unresolved material requirements alone block completion.

### Cold reconstruction and inspection

Every advertised handle directly resolves one persisted owner-typed object.
Cold reconstruction requires:

- the SQLite database path;
- the requested handle;
- the exact owner codec sets exported by public Module roots; and
- implementation supporting the identity and envelope contracts.

It requires no worktree, Git repository, source manifest, owner map, scan,
process cache, live provider, or fresh authorization call. Inspection returns
generated public result types and never leaks a domain model or dependency
exception across the facade.

### Package and import closure

Every Engine Module manifest owns its exact production direct requirements,
Python range, one public import root, and repository entrypoints. The root owns
one statically resolvable `__all__`. An AST-backed verifier derives governed
source ownership and imports and requires exact manifest equality.

Cross-Module production imports use public roots and exported names. Private
child imports, alternate roots, star imports, dynamic imports, unowned files,
and ambient script-directory imports reject. Every root, export, and entrypoint
executes from outside the checkout in safe-path mode with only the admitted
lock and checkout root.

### Platform scope

A1b implementation and required-real evidence cover Linux x86-64, CPython 3.11
and 3.12, glibc 2.17 or newer, case-sensitive ext4, and the selected SQLite
runtime. macOS, Windows, another architecture or filesystem, casefolding,
non-UTF-8 names, and platform-specific durability semantics require separate
design and evidence. This limitation is explicit; POSIX behavior is not
presented as portable behavior.

### Planning and acceptance

Work is serial. The Concurrent Plan Integration profile is not applicable.
Review binds identified semantic content. Adding review evidence or recording
lifecycle state does not invalidate unchanged reviewed semantics.

Plans do not prescribe commit count, parentage, direct-child chains,
exact-HEAD-only review, or standalone admit/start/verify/accept commits.
Lifecycle changes travel with substantive implementation, material replanning,
an accepted implementation boundary, or final acceptance evidence.

The v11 public cutover replaces schema, generator, runtime, persistence,
facade, tests, examples, policy-impact registrations, relationships, and
coverage atomically. Empty impact is not evidence of no impact without valid
independent coverage. A2 remains inactive until independent A1b acceptance.

## Consequences

- One external validator owns Draft semantics.
- One identity Module owns representation-preserving encoding, not domain
  equality.
- One immutable repository resolves every inspectable handle.
- SQLite replaces Git-hostile checked-in binary state with local generated
  storage while authored authority remains text in Git.
- Exact file-list snapshots remove recursive scope and filesystem metadata from
  identity.
- Roots-only closure removes copied dependency bags and hypothetical future
  authority.
- Owner-local codecs avoid both generic domain ownership and a central manifest.
- Direct consumed-trust objects make replay self-contained without broad trust
  views.
- The admitted platform is narrow and testable; portability is deferred rather
  than inferred.

## Rejected Alternatives

### Continue the local Draft subset

Rejected because it duplicates a mature validator and already diverged from
the declared Draft.

### Make generated classes or annotations semantic authority

Rejected because serialized shape and domain behavior have different owners.

### Preserve recursive NFC identity encoding

Rejected because representation identity and domain semantic equality are
different contracts.

### Retain C6 directory and hard-link storage

Rejected because it creates substantial publication, cleanup, locking, alias,
and filesystem machinery that SQLite already owns.

### Store object kind in both SQL and envelope

Rejected because two authorities can disagree. The typed handle and envelope
are validated on every operation.

### Store aggregate roots or complete authority views

Rejected because aggregate identity invalidates unrelated operations and
conceals exact material dependencies.

### Store transitive closure as caller-authored authority

Rejected because it duplicates direct references. Roots and immutable objects
derive the closure deterministically.

### Make closure transition-future-complete

Rejected because the set of future submissions is not current state authority.
A child stores authority actually consumed by its transition.

### Aggregate provider or authorization views

Rejected because they invalidate decisions for unrelated trust changes and
recreate ambient authority. Store exact consumed objects.

### Centralize codec membership

Rejected because a central manifest duplicates owner-local executable
authority. Composition injects owner exports and verification derives closure.

### Put SQLite databases or semantic exports in Git

Rejected because authored authority remains reviewable text and Git is not an
effective mutable binary database manager. SQLite is local generated storage.

### Implement migrations before a migration consumer exists

Rejected because A1b has no retained state. Schema migration or semantic
transfer requires a new consumer and re-plan.

### Claim macOS or Windows portability

Rejected because capture and durability contracts are not yet proven there.
Platform support requires explicit adapters and required-real evidence.

## Re-Plan Conditions

Re-plan if:

- the admitted v11 schema or interface shape changes;
- a reachable public construct exceeds the projection profile;
- an inspectable object cannot use direct immutable lookup;
- owner-local codecs cannot close without a central semantic authority;
- SQLite schema migration, semantic export/import, another database, or
  checked-in database authority becomes necessary;
- in-place destructive restore, Engine-owned backup retention, or automatic
  backup deletion becomes necessary;
- exact file-list capture needs recursion, exclusions, nonregular files,
  non-UTF-8 names, streaming, or identity beyond logical paths and raw bytes;
- macOS, Windows, another architecture/filesystem, casefolding, or stronger
  transient-mutation detection becomes required;
- operation roles, role dependencies, dynamic roles, codec kinds, or trust
  objects differ from the admitted executable contracts;
- replay requires ambient or live provider/authorization authority;
- a relationship, semantic consumer, horizon input, source path, or package
  import falls outside the admitted inventory or write set;
- old and new public authorities must coexist; or
- implementation would change normative policy, generic graph semantics, or A2.

## Acceptance

This ADR is `Accepted` for the exact implementation boundary identified by the
[final content-bound acceptance](../archive/plans/standards-engine-a1b/reports/a1b-final-acceptance.md).
That review proves the contract, identity, storage, capture, operation,
consumed-trust, package, migration-deletion, consumer-disposition, and coverage
claims with no blocked consumer. A2 remains outside this decision.
