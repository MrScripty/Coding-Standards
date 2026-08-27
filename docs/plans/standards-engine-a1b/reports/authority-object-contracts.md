# A1b Authority Object Contracts

**Status:** Proposed planning authority

This report owns the immutable object envelope, stored-record algebra,
dependency DAG, publication protocol, and cold-resolution contract. Authority
scope and execution dependency derivation are owned by
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

The owning domain Module constructs and validates `payload`, declares its
direct dependencies, and computes `semantic_id` from one typed material
identity record through `standards_identity`. The repository:

- verifies the envelope and canonical storage bytes;
- dispatches `object_kind` to exactly one registered owner;
- asks that owner to decode, validate, and recompute semantic identity;
- verifies direct dependency existence and kind;
- rejects cycles, self-reference, and descendant-to-ancestor references; and
- publishes create-only or returns a typed failure.

`storage_format`, public handle schema, public result projection, storage path,
timestamps, and implementation release are not semantic-ID inputs. A payload
never contains its own public handle. Resolution verifies the object and injects
the handle into its public projection.

There is no generic semantic payload, object enumeration, owner map, scan,
mutable index, compatibility reader, or fallback. Missing content is
`unavailable`, contradictory content is `invalid`, and a well-formed
unsupported contract is `unsupported`.

All set-like records are normalized by their owning typed key before
construction. Two unequal values with one key are `invalid`. Identity bytes
never decide semantic equality, grouping, deduplication, or order.

## Object Ownership

| Object family | Owner | Semantic identity input | Excluded from semantic identity |
| --- | --- | --- | --- |
| `content-snapshot` | `standards_authority` capture | Exact capture payload plus capture-contract authority | Metadata, parser, routing, graph, policy, coverage, wire and storage versions |
| Owner-local semantic authority | Registered domain Module | One coherent compatibility promise and exact authored/compiled semantic payload | Other Module promises and shared release facts |
| Owner-local compiled view | Registered domain Module | Exact content/authority dependencies and compiled semantic result | Callers, caches, rendering and unrelated views |
| `standards-authority-view` | `standards_engine` | ContentSnapshot plus sorted role-to-authority selections | Copied payloads, providers, authorization and operation results |
| `execution-closure` | Engine or Analysis composing kernel | Operation family plus exact root and transitive dependency references | Semantic result, complete standards view and presentation contract |
| `navigation-result` | `standards_engine` | Normalized query, semantic result and exact ExecutionClosure | Summary, rendering, next operations and wire version |
| `analysis-root` | `standards_analysis` | Requested change, views, exact ExecutionClosure and dependency-valid accepted decisions | Derived current work, rendering, lineage and transition order |
| Analysis and coverage child objects | `standards_analysis` | Exact narrow semantic payload and upstream handles listed below | Analysis root and unrelated repository authority |
| Policy and relationship inspection objects | Metadata, Graph, and Policy Impact adapters | Exact inspected semantic value and material ExecutionClosure | Complete standards view and presentation-only fields |

Semantic authority and compiled-view object kinds are registered by their
manifest-owning domain Module. The generated object-kind dispatch is the sole
repository membership projection. A file, import, schema definition, or
StandardsAuthorityView selection does not register an object kind.

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
base/proposed views +
ExecutionClosure + context +
decisions + child handles ---> AnalysisRoot
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
  capture_kind: "git-tree" | "manifest",
  capture_authority: AuthorityObjectReference,
  scope: set<path> by path,
  exclusions: set<ContentExclusionV1> by path,
  source_identity:
    GitSourceV1 { tree, commit }
    | ManifestSourceV1 { source_kind: "dirty-git" | "non-git" },
  entries: set<ContentEntryV1> by path
}

ContentEntryV1 {
  path,
  entry_type,
  mode,
  tracking,
  inclusion,
  reason,
  content_base64?,
  content_digest?,
  byte_length?,
  symlink_target?,
  symlink_resolution?,
  recorded_gitlink?,
  checked_out_revision?,
  nested_identity?,
  nested_content: ContentSnapshotHandle?,
  worktree_state?
}
```

Included file bytes use padded standard Base64 plus exact SHA-256 and decoded
length. Reads verify all three. Repository root, worktree path, capture time,
staging path, parser versions, and semantic interpretations are excluded.

### SemanticAuthorityObject

Each registered owner defines one closed payload contract and material identity
record. Its envelope direct dependencies must equal the dependencies accepted by
that owner's constructor. An object cannot contain a free-form version map.
Compatibility identity is either:

- a content-addressed semantic payload whose meaning is fully represented by
  the owner-defined identity record; or
- a stable contract ID plus semantic revision and exact structural/content
  digest when the domain already owns reviewed revision lifecycle.

The repository never interprets either form generically.

### StandardsAuthorityViewV1

```text
StandardsAuthorityViewV1 {
  content: ContentSnapshotHandle,
  authorities: set<SemanticAuthoritySelectionV1> by role
}

SemanticAuthoritySelectionV1 {
  role: CanonicalId,
  authority: AuthorityObjectReference
}
```

The Engine constructor owns the closed required-role rules and verifies that
each selected authority belongs to its role and content. The record contains no
copied semantic payload, contract version, provider, authorization decision, or
operation result.

### ExecutionClosureV1

```text
ExecutionClosureV1 {
  operation: "route" | "read" | "related" | "analysis",
  roots: set<AuthorityObjectReference> by (object_kind, semantic_id),
  dependencies: set<AuthorityObjectReference> by (object_kind, semantic_id)
}
```

`dependencies` is the exact transitive closure obtained by walking `roots`.
It includes each root once. The constructor rejects an omitted, extra,
unpublished, contradictory, cyclic, or differently typed dependency.
ExecutionClosure owns no executable semantics; it is generated evidence.

### NavigationResultV1

```text
NavigationResultV1 {
  operation: "route" | "read" | "related",
  request: normalized operation request,
  authority: ExecutionClosureHandle,
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

- AnalysisContext handle;
- canonical fact ID, semantic revision, fact-contract digest, value contract,
  answer contract, evidence contract, and authorization capability; and
- exact authority dependencies for those contracts.

Prompt wording, dependent programs, selecting relationships, and presentation
order are excluded. Pending projection joins the requirement with current
display work.

### FactObservationV1

- FactRequirement handle;
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

- CoverageAuthorityView handle;
- covered subject, owner, semantic revision, relationship kinds, and horizon;
  and
- required evidence contract.

The derivation StandardsAuthorityView may appear as non-identity provenance but
does not enter requirement semantic identity.

### CoverageAttestationV1

- CoverageRequirement handle;
- complete conclusion, evidence, exclusions, rationale, and auditor provenance;
- authorization reference and exact validating authority dependency; and
- attestation semantic contract.

It does not repeat relationships, horizon members, obligations, dispositions,
reports, or complete views.

### CoverageCertificateV1

- CoverageAuthorityView, CoverageRequirement, and CoverageAttestation handles;
- evidence, fact-schema, horizon, and relationship digests needed for public
  inspection; and
- exact authority dependencies of deterministic certificate construction.

The three upstream handles are the certificate authority. It contains no
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
  base_view: StandardsAuthorityViewHandle,
  proposed_view: StandardsAuthorityViewHandle,
  authority: ExecutionClosureHandle,
  context: AnalysisContextHandle,
  fact_requirements: set<FactRequirementHandle>,
  fact_observations: set<FactObservationHandle>,
  dispositions: set<DispositionRecord>,
  coverage_views: set<CoverageAuthorityViewHandle>,
  coverage_requirements: set<CoverageRequirementHandle>,
  coverage_attestations: set<CoverageAttestationHandle>,
  coverage_certificates: set<CoverageCertificateHandle>
}
```

The state retains every dependency-valid accepted decision, including
dormant-valid decisions. Normalization removes dependency-invalid decisions and
rejects conflicting decisions under one decision key. Current requirements,
obligations, reading plans, certificate projections, completion, results, and
next operations are derived.

## Semantic And Repository Validation

Repository validation:

1. decode canonical envelope bytes;
2. verify storage format and closed registered object kind;
3. dispatch to exactly one owner;
4. verify the owner-decoded closed payload;
5. recompute owner-defined semantic identity;
6. resolve every direct dependency and verify kind;
7. reject self-reference and cycles; and
8. return the typed object.

Domain validation:

1. ContentSnapshot entries satisfy kind-specific field rules and exact
   byte/digest/length agreement.
2. StandardsAuthorityView has exactly one authority per required role and every
   authority is coherent with its selected content.
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
8. AnalysisRoot contains exactly the dependency-valid decisions and materialized
   child handles needed for deterministic projection. Extra or missing current
   children reject.
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
