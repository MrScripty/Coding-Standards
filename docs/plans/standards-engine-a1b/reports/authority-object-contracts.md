# A1b Authority Object Contracts

**Status:** Proposed planning authority

This report owns the immutable object envelope, owner codec inventory,
stored-record algebra, dependency DAG, publication protocol, and
cold-resolution contract. Authority roles and operation dependency derivation
are owned by
[authority composition and execution closure](authority-composition-and-execution-closure.md).
The public JSON Schema owns only serialized request, result, inspection, and
handle shapes.

## Repository Rules

Every stored value uses:

```text
AuthorityObjectEnvelope v1
  object_kind: CanonicalId
  semantic_id: AuthorityObjectId
  storage_format: "authority-envelope.v1"
  direct_dependencies: set<AuthorityObjectReference>
  payload_contract: CanonicalId
  payload: owner-defined closed record
```

The owning domain Module exports one immutable `AuthorityObjectCodecSet`.
Each codec constructs and validates one closed `payload`, declares its allowed
and extracted direct dependencies, and computes `semantic_id` from one typed
material identity record through `standards_identity`. The repository:

- verifies the envelope and canonical storage bytes;
- dispatches `object_kind` through the explicitly injected codec sets;
- asks that owner to decode, validate, and recompute semantic identity;
- verifies direct dependency existence and kind;
- rejects cycles, self-reference, and descendant-to-ancestor references; and
- publishes create-only or returns a typed failure.

`storage_format`, public handle schema, public result projection, storage path,
timestamps, and implementation release are not semantic-ID inputs. A payload
never contains its own public handle. Resolution verifies the object and injects
the handle into its public projection.

There is no generic semantic payload, ambient registration, object enumeration,
owner map, scan, mutable index, compatibility reader, or fallback. Missing content is
`unavailable`, contradictory content is `invalid`, and a well-formed
unsupported contract is `unsupported`.

All set-like records are normalized by their owning typed key before
construction. Two unequal values with one key are `invalid`. Identity bytes
never decide semantic equality, grouping, deduplication, or order.

## Exact Codec Inventory

Every owner exports exactly one `AuthorityObjectCodecSet(owner_id, codecs)`
through its public root. Owner identity occurs only on that set. A codec owns
one object kind, one payload contract, one identity domain, complete payload
construction, and exact dependency extraction. Engine injects the following
closed sets into Authority; no filesystem discovery, entry-point loading,
schema enum, or mutable registry contributes membership.

| Owner codec set | Object kind | Payload contract | Identity domain | Allowed direct dependency kinds |
| --- | --- | --- | --- | --- |
| `standards-authority` | `content-snapshot` | `content-snapshot.v1` | `coding-standards:content-snapshot:v1` | `content-snapshot` |
| same | `execution-closure` | `execution-closure.v1` | `coding-standards:execution-closure:v1` | `content-snapshot`, `canonical-standards-corpus`, `compiled-policy-impact`, `standards-graph`, `routing-projection`, `coverage-horizon`, `analysis-context`, `fact-requirement`, `fact-observation`, `coverage-view`, `coverage-requirement`, `coverage-attestation`, `coverage-certificate`, `operation-authority-contract`, `provider-authority-view`, `authorization-authority-view` |
| `standards-metadata` | `canonical-standards-corpus` | `canonical-standards-corpus.v1` | `coding-standards:canonical-standards-corpus:v1` | `content-snapshot` |
| `standards-policy-impact` | `compiled-policy-impact` | `compiled-policy-impact.v1` | `coding-standards:compiled-policy-impact:v1` | `content-snapshot`, `canonical-standards-corpus` |
| `standards-graph` | `standards-graph` | `standards-graph.v1` | `coding-standards:standards-graph:v1` | `canonical-standards-corpus`, `compiled-policy-impact` |
| `standards-analysis` | `routing-projection` | `routing-projection.v1` | `coding-standards:routing-projection:v1` | `content-snapshot`, `canonical-standards-corpus` |
| same | `coverage-horizon` | `coverage-horizon.v1` | `coding-standards:coverage-horizon:v1` | `content-snapshot`, `canonical-standards-corpus`, `compiled-policy-impact`, `standards-graph` |
| same | `analysis-context` | `analysis-context.v1` | `coding-standards:analysis-context:v2` | `canonical-standards-corpus`, `routing-projection`, `standards-graph`, `compiled-policy-impact`, `coverage-horizon` |
| same | `fact-requirement` | `fact-requirement.v1` | `coding-standards:fact-requirement:v2` | `analysis-context`, `routing-projection`, `compiled-policy-impact` |
| same | `fact-observation` | `fact-observation.v1` | `coding-standards:fact-observation:v2` | `fact-requirement`, `provider-authority-view`, `authorization-authority-view` |
| same | `coverage-view` | `coverage-view.v1` | `coding-standards:coverage-authority-view:v3` | `canonical-standards-corpus`, `compiled-policy-impact`, `standards-graph`, `coverage-horizon` |
| same | `coverage-requirement` | `coverage-requirement.v1` | `coding-standards:coverage-audit-requirement:v3` | `coverage-view` |
| same | `coverage-attestation` | `coverage-attestation.v1` | `coding-standards:coverage-attestation:v3` | `coverage-requirement`, `authorization-authority-view` |
| same | `coverage-certificate` | `coverage-certificate.v1` | `coding-standards:consumer-coverage-certificate:v3` | `coverage-view`, `coverage-requirement`, `coverage-attestation` |
| same | `analysis-root` | `analysis-root.v1` | `coding-standards:analysis:v4` | `execution-closure`, `analysis-context`, `fact-observation`, `coverage-attestation` |
| `standards-engine` | `operation-authority-contract` | `operation-authority-contract.v1` | `coding-standards:operation-authority-contract:v1` | none |
| same | `standards-authority-view` | `standards-authority-view.v1` | `coding-standards:standards-authority-view:v1` | `content-snapshot`, `operation-authority-contract`, `canonical-standards-corpus`, `routing-projection`, `standards-graph`, `compiled-policy-impact`, `coverage-horizon` |
| same | `navigation-result` | `navigation-result.v1` | `coding-standards:navigation-result:v1` | `execution-closure` |
| same | `policy-inspection` | `policy-inspection.v1` | `coding-standards:policy-inspection:v2` | `execution-closure`, `canonical-standards-corpus` |
| same | `relationship-inspection` | `relationship-inspection.v1` | `coding-standards:relationship-inspection:v2` | `execution-closure`, `standards-graph`, `compiled-policy-impact` |
| same | `provider-authority-view` | `provider-authority-view.v1` | `coding-standards:provider-authority-view:v1` | `content-snapshot` |
| same | `authorization-authority-view` | `authorization-authority-view.v1` | `coding-standards:authorization-authority-view:v1` | none |

`standards_identity`, `standards_contracts`, `standards_applicability`, and the
repository-neutral Graph Engine own no stored object kind. Identity supplies
encoding, Contracts validates public wire values, Applicability supplies pure
program semantics, and standards-specific callers bind those semantics into
their own compiled objects. Adding, removing, renaming, or transferring a kind,
payload contract, identity domain, or allowed dependency is a re-plan trigger.

The public JSON Schema deliberately retains `CanonicalId` representation for
`object_kind`; it does not own this domain catalog. Runtime registry
construction requires exact equality with the codec inventory above.

## Dependency DAG

`A -> B` means B stores a direct reference to upstream A.

```text
nested ContentSnapshot ----------> ContentSnapshot
ContentSnapshot + semantic refs --> owner-local compiled views
ContentSnapshot + selected refs --> StandardsAuthorityView
compiled views + operation refs --> ExecutionClosure
ExecutionClosure + query value --> NavigationResult
ExecutionClosure ------------+---> policy / relationship inspection
                              |
analysis semantic inputs ----> AnalysisContext
AnalysisContext -------------> FactRequirement
FactRequirement -------------> FactObservation
coverage semantic inputs ----> CoverageAuthorityView
CoverageAuthorityView -------> CoverageRequirement
CoverageRequirement ---------> CoverageAttestation
view + requirement +
attestation -----------------> CoverageCertificate
ExecutionClosure + context +
decisions + child refs -----> AnalysisRoot
```

No object references itself or a descendant. Child analysis and coverage
objects never reference AnalysisRoot. Equal semantic values reached through
different construction order produce equal IDs.

## Exact Record Algebra

Every listed field is required unless marked `?`. `tuple<T>` preserves
semantic order. `set<T> by K` is stored in owner-normalized K order and rejects
duplicate K. `AuthorityObjectReference` is exactly `(object_kind,
semantic_id)`.

### ContentSnapshotV1

```text
ContentSnapshotV1 {
  scope: set<path> by path,
  exclusions: set<path> by path,
  entries: set<ContentEntryV1> by path
}

ContentEntryV1 {
  path,
  entry_type: "file" | "directory" | "symlink" | "nested-content",
  mode,
  content_base64?,
  content_digest?,
  byte_length?,
  symlink_target?,
  nested_content: AuthorityObjectReference?  # kind = content-snapshot
}
```

Included file bytes use padded standard Base64 plus exact SHA-256 and decoded
length. Reads verify all three. Entry-type rules require exactly the fields
needed for a file, directory, symlink, or nested-content entry. Repository root,
worktree path, capture Adapter kind, tracking state, inclusion explanation,
capture time, staging path, Git commit, source Git tree OID, recorded gitlink,
checked-out revision, worktree state, parser versions, and semantic
interpretations are excluded after capture validation. Git and manifest
Adapters resolve their locators, validate source consistency, construct this
same canonical content record, and discard adapter observations. Equal selected
content under equal scope and exclusions produces one snapshot across capture
Adapters, Git hash formats, or source trees differing only outside the selected
scope. No capture-provenance object is admitted.

### SemanticAuthorityObject

Each admitted owner codec defines one closed payload contract and material
identity record. Its envelope direct dependencies must equal the dependencies
extracted by that codec's constructor. An object cannot contain a free-form
version map.
Compatibility identity is either:

- a content-addressed semantic payload whose meaning is fully represented by
  the owner-defined identity record; or
- a stable contract ID plus semantic revision and exact structural/content
  digest when the domain already owns reviewed revision lifecycle.

The repository never interprets either form generically.

### StandardsAuthorityViewV1

Each Engine-owned operation contract is one exact record:

```text
OperationAuthorityContractV1 {
  id: "operation-contract.route.v1" |
      "operation-contract.read.v1" |
      "operation-contract.related.v1" |
      "operation-contract.analysis.v1",
  operation: "route" | "read" | "related" | "analysis",
  required_roles: set<RoleKindRequirementV1> by role,
  coherence_rules: set<CanonicalId> by ID
}

RoleKindRequirementV1 {
  role: CanonicalId,
  object_kind: CanonicalId
}
```

The exact four records, role-kind requirements, and coherence-rule IDs are
owned by
[authority composition and execution closure](authority-composition-and-execution-closure.md).
Their union is derived review evidence, not another runtime profile.

```text
StandardsAuthorityViewV1 {
  content: AuthorityObjectReference,  # kind = content-snapshot
  operation_contracts: set<OperationAuthoritySelectionV1> by operation,
  authorities: set<SemanticAuthoritySelectionV1> by role
}

OperationAuthoritySelectionV1 {
  operation: "route" | "read" | "related" | "analysis",
  authority: AuthorityObjectReference
}

SemanticAuthoritySelectionV1 {
  role: CanonicalId,
  authority: AuthorityObjectReference
}
```

The Engine constructor resolves each selected operation contract and validates
only that contract's required role-to-kind membership and coherence rules.
Unknown authorities not selected by any operation contract are invalid. The
view record contains no copied semantic payload, ambient role profile, provider,
authorization decision, or operation result.

### ExecutionClosureV1

```text
ExecutionClosureV1 {
  operation: "route" | "read" | "related" | "analysis",
  roots: set<ExecutionAuthorityRootV1> by
    (side, role, object_kind, semantic_id),
  dependencies: set<AuthorityObjectReference> by (object_kind, semantic_id)
}

ExecutionAuthorityRootV1 {
  side: "current" | "accepted" | "proposed" | "transition",
  role: CanonicalId,
  authority: AuthorityObjectReference
}
```

`dependencies` is the exact transitive closure obtained by walking `roots`.
It includes each root once. The constructor rejects an omitted, extra,
unpublished, contradictory, cyclic, or differently typed dependency.
ExecutionClosure owns no executable semantics; it is generated evidence.
Analysis closure is transition-closed: it includes role- and side-qualified
authority needed by the current projection and every advertised valid next
transition, including dormant conditional applicability. An authority is
unused only when it cannot affect either the current projection or any such
transition. Fresh provider claims and authorization decisions remain trusted
transition inputs; their accepted immutable views enter the successor closure.

### NavigationResultV1

```text
NavigationResultV1 {
  operation: "route" | "read" | "related",
  request: normalized operation request,
  authority: AuthorityObjectReference,  # kind = execution-closure
  semantic_result: exact owner-normalized route/read/related value
}
```

The complete StandardsAuthorityView, summaries, rendered text, next operations,
and result wire version are excluded.

### AnalysisContextV1

- changed policy-unit IDs and owning modules;
- accepted/proposed semantic revisions plus content and structural digests;
- normalized change descriptors and semantic proposals; and
- exact authority references material to interpreting those records.

Full standards views, unrelated relationship topology, attestations,
observations, dispositions, and AnalysisRoot are excluded.

### FactRequirementV1

- AnalysisContext object reference;
- canonical fact ID, semantic revision, fact-contract digest, value contract,
  answer contract, evidence contract, and authorization capability; and
- exact authority dependencies for those contracts.

Prompt wording, dependent programs, selecting relationships, and presentation
order are excluded. Pending projection joins the requirement with current
display work.

### FactObservationV1

- FactRequirement object reference;
- exact typed fact value and state;
- complete evidence;
- authorization reference and decision;
- provider claim when provider-backed; and
- exact provider/authorization authority references that validated it.

Timestamps and summaries are excluded.

### CoverageAuthorityViewV1

- policy-unit ID, owner, target semantic revision, representation digest, and
  structural digest;
- exact relationship kinds and relationship fingerprints;
- applicability program and fact-schema digests;
- independent horizon identity, members, and member fingerprints; and
- exact owner-local authority dependencies used to derive the view.

Accepted/proposed labels, complete StandardsAuthorityView, attestation source
records, attestations, certificates, analysis reports, timestamps, storage
paths, and dispositions are excluded.

### CoverageRequirementV1

- CoverageAuthorityView object reference;
- covered subject, owner, semantic revision, relationship kinds, and horizon;
  and
- required evidence contract.

The derivation StandardsAuthorityView may appear as non-identity provenance but
does not enter requirement semantic identity.

### CoverageAttestationV1

- CoverageRequirement object reference;
- complete conclusion, evidence, exclusions, rationale, and auditor provenance;
- authorization reference and exact validating authority dependency; and
- attestation semantic contract.

It does not repeat relationships, horizon members, obligations, dispositions,
reports, or complete views.

### CoverageCertificateV1

- CoverageAuthorityView, CoverageRequirement, and CoverageAttestation object
  references;
- evidence, fact-schema, horizon, and relationship digests needed for public
  inspection; and
- exact authority dependencies of deterministic certificate construction.

The three upstream references are the certificate authority. It contains no
change-specific disposition, report reference, repeated version bag, or
generation timestamp.

### PolicyInspectionV1 And RelationshipInspectionV1

Each stores the exact inspected semantic projection, its canonical target, and
the material Read or Related ExecutionClosure. They do not bind the complete
StandardsAuthorityView.

Policy inspection contains canonical module or policy-unit metadata, locator,
lifecycle, representation, and structural facts. Relationship inspection
contains generic topology and compiler provenance plus compiled policy-impact
semantics when applicable.

### AnalysisRootV1

```text
AnalysisRootV1 {
  authority: AuthorityObjectReference,  # kind = execution-closure
  context: AuthorityObjectReference,  # kind = analysis-context
  fact_observations: set<AuthorityObjectReference>,  # kind = fact-observation
  dispositions: set<DispositionRecord>,
  coverage_attestations: set<AuthorityObjectReference>
    # kind = coverage-attestation
}
```

The state retains every dependency-valid accepted decision, including
dormant-valid decisions. Normalization removes dependency-invalid decisions and
rejects conflicting decisions under one decision key. Current requirements,
obligations, coverage views and requirements, certificates, reading plans,
completion, results, and next operations are derived. Generated children remain
directly storable and inspectable but are not repeated as state authority.
Complete base/proposed StandardsAuthorityViews are
prepare inputs only and never state fields or result projections. The narrow
context plus transition-closed closure retains the accepted/proposed material
authority needed for deterministic projection and valid successors. Prior
analysis reuse validates each decision's narrow dependencies against the new
request rather than recovering the former complete views.

Stored payloads use only `AuthorityObjectReference`. Public projection resolves
those references and injects the appropriate schema-v4 handle. Public handle
kind or schema-version fields never enter a stored payload or semantic identity.

## Semantic And Repository Validation

Repository validation:

1. decode canonical envelope bytes;
2. verify storage format and closed admitted object kind;
3. dispatch to exactly one injected owner codec;
4. verify the codec-decoded closed payload;
5. recompute owner-defined semantic identity through that codec;
6. resolve every direct dependency and verify kind;
7. reject self-reference and cycles; and
8. return the typed object.

Domain validation:

1. ContentSnapshot entries satisfy kind-specific field rules and exact
   byte/digest/length agreement.
2. StandardsAuthorityView has exactly one contract per operation and at most
   one authority per selected role. Every role resolves to the kind required by
   at least one operation contract, and every selection is coherent with its
   selected content. No ambient role profile completes the view.
3. Owner-local compiled views equal fresh owner compilation from their exact
   content and semantic-authority dependencies.
4. ExecutionClosure equals the transitive closure of roots; no manually supplied
   version or ambient process value completes it.
5. Navigation result equals fresh operation execution from its normalized
   request and material closure.
6. Narrow AnalysisContext, FactRequirement, and CoverageAuthorityView identities
   exclude unrelated authority exactly as declared.
7. Observations, dispositions, and attestations validate evidence and
   authorization through the exact authority references retained by Analysis
   execution.
8. AnalysisRoot contains exactly the dependency-valid observations,
   dispositions, and authored coverage attestations needed for deterministic
   projection and valid next transitions. Derived requirement, coverage-view,
   certificate, complete-view, or lineage fields reject.
9. Existing AnalysisRoot projection never invokes live providers or seeks fresh
   authorization. A new transition may do so before publishing a successor.

## Durable Publication

The durable Adapter is Linux-ext4-only and retains C4's reviewed containment
and durability design:

- one canonical absolute store path walked from a trusted `/` descriptor with
  descriptor-relative no-follow directory opens;
- owner/mode checks, exact device/inode/mount identity, ext4 and writable-mount
  proof, and hard-link/`fsync`/advisory-lock capability probes;
- all later operations relative to retained descriptors;
- lock-free reads and one non-authoritative repository publication lock;
- one same-directory `O_CREAT|O_EXCL|O_NOFOLLOW` staging file;
- file `fsync`, atomic create-only hard-link publication, directory `fsync`,
  final-object verification, and terminal staging cleanup; and
- a complete root rewalk before success to reject path-component replacement.

The final path is
`objects/<object-kind>/<semantic-id-digest>`. Existing byte-identical content
is idempotent success; different content under one semantic ID is
`IDENTITY.COLLISION` and `invalid`. Existing content is never overwritten.
Interruption before publication leaves no resolvable object. Interruption after
publication is reconciled by retrying the same immutable put. Dependencies
publish before dependents.

Storage-format changes may require repository migration but do not alter domain
semantic IDs merely because envelope bytes change.

## Construction Order

1. Capture and publish ContentSnapshots.
2. Construct owner-local SemanticAuthorityObjects and compiled views.
3. Construct and publish StandardsAuthorityViews after role/coherence checks.
4. Execute a query through AuthorityBoundValues, derive and publish its
   ExecutionClosure, then publish NavigationResult.
5. For analysis, resolve base/proposed views, construct narrow context and
   reusable child objects, run eligible providers over declared immutable
   inputs, and derive AnalysisExecutionClosure.
6. Construct normalized AnalysisRoot only after every dependency has published
   and re-resolved.
7. Resolution projects the supplied root, validates one submission and trusted
   execution context, constructs new decision objects, removes invalid
   decisions, retains dormant-valid decisions, derives a successor closure, and
   publishes one independent successor AnalysisRoot.

## Re-Plan Triggers

Re-plan if:

- a semantic identity requires storage-envelope or public-wire fields;
- the repository must interpret a domain payload generically;
- a StandardsAuthorityView contains copied semantics or transition-only trust;
- an ExecutionClosure cannot be derived from the direct dependencies returned
  by execution;
- a public handle requires an owner map, scan, mutable index, ambient
  configuration, or companion handle;
- an existing analysis projection requires live provider or authorization
  execution;
- a dependency would point to a descendant or itself;
- a new public inspectable family, compatibility reader, remote store, garbage
  collector, streaming snapshot, or A2 mutable head is required; or
- the exact Linux ext4 durability/containment capability cannot be proved.
