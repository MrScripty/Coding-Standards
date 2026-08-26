# A1b Authority Object Contracts

**Status:** Proposed planning authority

## Rules

Every stored value is:

```text
AuthorityObjectEnvelope v1
  object_kind
  payload_contract
  payload
```

The envelope is encoded and addressed by identity encoding v2. Every stored
payload field is identity-bearing; no second stored payload may resolve under
the same handle. A payload never contains its own handle. Resolution recomputes
the handle and injects it only into the generated public projection.

Non-authoritative presentation fields are deterministic projections from an
enclosing root and its exact result/presentation contract version. Display
summaries, next operations, fact prompts, dependent-program displays,
generation timestamps, storage paths, parent analysis lineage, transition
order, requirements, obligations, reading plans, and completion state are not
stored unless an exact field below says otherwise.

All maps use closed typed keys. All sets are sorted and deduplicated by the
owning typed key before storage. Every referenced handle must resolve and match
its required object kind before an aggregate object is published.

`standards_authority.get` proves only canonical bytes, handle identity, closed
record shape, object-local invariants, and dependency existence/kind. It does
not import Metadata, Analysis, Graph, Applicability, authorization, or provider
semantics. The bound analysis kernel validates root-relative semantic coherence
when it resolves or projects an aggregate root. Policy and relationship
inspection adapters validate snapshot-relative semantics before returning a
public inspection result.

Every field shown in an exact record below is required. `T?` is the only
optional-field notation. `tuple<T>` is an immutable JSON array whose order is
semantic. `set<T> by K` is encoded as an array, contains no duplicate canonical
K, and is sorted by the owning domain's total order for K. `map<K,V>` is a JSON
object whose keys are K. Records reject unlisted fields. Identity encoding is
never an ordering oracle.

Capitalized public types such as `CanonicalId`, `ChangeDescriptor`,
`EvidenceReference`, and `ReviewScope` mean the exact reachable v11 schema
definition named in the schema/domain audit. A complete handle value includes
its kind, schema version, and ID. Digest is `sha256:` followed by 64 lowercase
hexadecimal digits.

The orders used below are exact: string-like IDs, paths, digests, and handle
IDs compare Unicode scalar sequences; integers compare numerically; Boolean
compares `false` before `true`; enum values compare in their v11 declaration
order; and tuples compare lexicographically by those component orders. Evidence
uses `evidence.id`; handles use `(kind, schema_version, id)`; relationship fingerprints use
`edge`; horizon members use `member.id`; policy subjects and proposals use
their canonical policy ID; dispositions use `(obligation, decision kind)`.
Each owning constructor rejects two distinct values with the same ordering key.

## Dependency DAG

`A -> B` means B stores a handle to A or a payload mechanically derived from A
that must be revalidated before B is published.

```text
nested snapshot ---------> snapshot root
snapshot roots ----------> analysis root
analysis semantic inputs -> analysis context
coverage semantic inputs -> coverage view
snapshot root -----------> policy / relationship inspection
snapshot root -----------> navigation result
analysis context --------> fact requirement
fact requirement --------> fact observation
coverage view -----------> coverage requirement
coverage requirement ----> coverage attestation
coverage view +
requirement +
attestation -------------> coverage certificate
context + observations +
attestations +
requirements + coverage
children + dispositions -> analysis root
```

No payload contains a descendant handle, a handle to itself, or a reference
back from a child to an analysis root. Cycles are invalid.

## Payloads

### `snapshot-root.v1`

- snapshot kind: `git-tree` or `manifest`;
- capture contract version;
- sorted scope and typed exclusions;
- source semantic identity: Git tree/commit for an immutable Git source, or
  `dirty-git`/`non-git` for a validated manifest source;
- sorted entries containing path, entry kind, mode, tracking state, inclusion
  reason, and kind-specific symlink, gitlink, or nested-repository fields;
- included file content as padded standard Base64, decoded byte length, and
  SHA-256 digest;
- nested snapshot handles; and
- interpretation-affecting metadata, parser, graph, policy-impact,
  applicability, and snapshot contract versions.

Repository root paths, staging paths, capture time, and worktree location are
excluded.

### `navigation-result.v1`

- snapshot handle;
- normalized query call;
- identity-bearing route, read, or related semantic selection; and
- routing, graph, metadata, interface, and result-projection contract versions.

Its own handle, next operations, summaries, rendered text, and cache state are
excluded and projected deterministically.

### `analysis-context.v1`

- changed policy-unit canonical IDs and owning modules;
- accepted and proposed semantic revisions, content digests, and structural
  digests for those units;
- normalized change descriptors;
- normalized semantic proposals; and
- context, metadata, parser, and proposal contract versions.

Full snapshot handles, unrelated authority bytes, relationship topology,
attestations, observations, dispositions, and any analysis handle are
excluded. Derivation snapshots remain analysis-root authority and provenance,
not context identity. This identity remains narrow enough for fact-observation
reuse.

### `fact-requirement.v1`

- analysis-context handle;
- canonical fact ID;
- exact fact-contract identity and semantic revision;
- value type, domain, nullability, and context kind;
- answer, evidence, provider, and authorization contract versions; and
- dependency digest over the exact fact definition.

Prompt wording, dependent-program lists, and presentation order are excluded.
`PendingResult` exposes a derived `FactRequirementWork` containing the
semantic requirement, current prompt, and current dependent programs.
`inspect(FactRequirementHandle)` returns only the semantic requirement.

### `fact-observation.v1`

- fact-requirement handle;
- exact typed fact value and state;
- complete evidence records;
- authorization reference and authority decision;
- provider claim and provider contract when provider-backed; and
- observation contract version.

Timestamps and display summaries are provenance-only and excluded.

### `coverage-view.v1`

- policy-unit canonical ID and owning module;
- target semantic revision, content digest, and structural digest;
- exact originating relationship set and relationship-kind contract;
- applicability language and referenced program/fact-definition digests;
- audit-horizon provider and contract versions;
- sorted horizon members with relevant content/structural fingerprints;
- identity-resolution contract; and
- coverage, attestation, authorization, and evidence-provider contract
  versions.

Accepted/proposed labels, attestation instances, certificates, reports,
packets, timestamps, storage paths, and dispositions are excluded.
The complete analysis snapshot handle is also excluded because it contains
attestation-source bytes. The view embeds the exact coverage-relevant semantic
payload and fingerprints listed above; its derivation snapshot is
non-identity provenance. This preserves requirement identity when a matching
attestation is committed.

### `coverage-requirement.v1`

- coverage-view handle;
- canonical covered policy-unit subject;
- covered scope;
- relationship kinds and audit horizon identity; and
- exact required evidence contract.

Derivation snapshot may be provenance but is excluded from identity.

### `coverage-attestation.v1`

- coverage-requirement handle;
- complete conclusion;
- evidence records;
- explicit exclusions;
- rationale;
- auditor provenance and authorization decision; and
- attestation contract version.

It does not repeat relationships, horizon members, obligations, dispositions,
or reports.

### `coverage-certificate.v1`

- coverage-view, coverage-requirement, and coverage-attestation handles;
- evidence digests;
- applicability, fact-schema, horizon, relationship, coverage, authorization,
  and tool contract versions.

It contains no change-specific disposition or report reference.
Deterministic certificate provenance is projected from the three dependencies;
generation timestamps are absent.

### `policy-inspection.v1`

- snapshot handle;
- canonical module or policy-unit identity;
- exact metadata, locator, lifecycle, content, and structural facts selected
  for public inspection; and
- metadata/parser/inspection contract versions.

### `relationship-inspection.v1`

- snapshot handle;
- edge ID;
- generic endpoints, kind, groups, traversal, and compiler provenance;
- compiled policy-impact semantics when applicable, including applicability
  program identity, scopes, propagation, evidence owner, and rationale; and
- graph, policy-impact, applicability, and inspection contract versions.

### `analysis-root.v1`

- analysis-context handle;
- base and proposed snapshot handles;
- authorization-authority view;
- evidence-provider contract/input view;
- sorted dependency-valid fact-observation handles;
- sorted materialized fact-requirement, coverage-view, coverage-requirement,
  and coverage-certificate handles needed to reproduce the current projection;
- sorted handle-free consumer and impact disposition records, each containing
  its exact obligation/dependency fingerprint, decision, evidence, and
  authorization;
- sorted coverage-attestation handles;
- normalized dormant-valid decisions as well as material decisions; and
- analysis, applicability, metadata, graph, parser, evidence-provider,
  authorization, interface, and result-projection contract versions.

Obligation and impact-trace values, reading plans, certificate content,
completion proofs, pending/complete results, and next operations are derived.
The root stores the direct handles of materialized inspectable dependencies but
not duplicate child payloads. Invalid decisions are removed before
construction.

## Exact Record Algebra

The prose above explains purpose; the following closed records govern
construction.

```text
ParserVersionsV1 = map<CanonicalId, NonEmptyString>
ProviderVersionsV1 = map<CanonicalId, NonEmptyString>

SnapshotVersionsV1 {
  snapshot_contract_version: "snapshot-root.v1",
  metadata_api_version: NonEmptyString,
  parser_versions: ParserVersionsV1,
  graph_engine_contract_version: NonEmptyString,
  policy_impact_contract_version: NonEmptyString,
  applicability_language_version: 1,
  coverage_contract_version: NonEmptyString,
  identity_resolution_contract_version: NonEmptyString
}
NavigationVersionsV1 {
  navigation_contract_version: "navigation-result.v1",
  interface_schema_version: 11,
  result_projection_version: 3,
  routing_contract_version: NonEmptyString,
  metadata_api_version: NonEmptyString,
  graph_engine_contract_version: NonEmptyString,
  parser_versions: ParserVersionsV1
}
AnalysisContextVersionsV1 {
  context_contract_version: "analysis-context.v1",
  metadata_api_version: NonEmptyString,
  parser_versions: ParserVersionsV1,
  proposal_contract_version: NonEmptyString
}
PolicyInspectionVersionsV1 {
  inspection_contract_version: "policy-inspection.v1",
  metadata_api_version: NonEmptyString,
  parser_versions: ParserVersionsV1
}
RelationshipInspectionVersionsV1 {
  inspection_contract_version: "relationship-inspection.v1",
  graph_engine_contract_version: NonEmptyString,
  policy_impact_contract_version: NonEmptyString,
  applicability_language_version: 1
}
AnalysisRootVersionsV1 {
  analysis_contract_version: 7,
  analysis_schema_version: 4,
  applicability_language_version: 1,
  metadata_api_version: NonEmptyString,
  graph_engine_contract_version: NonEmptyString,
  parser_versions: ParserVersionsV1,
  evidence_provider_contract_versions: ProviderVersionsV1,
  authorization_contract_version: NonEmptyString,
  interface_schema_version: 11,
  result_projection_version: 3,
  authority_object_contract_version: 1,
  identity_encoding_version: 2
}

StoredBytesV1 {
  base64: string,
  byte_length: integer >= 0,
  digest: Digest
}

SnapshotCommonV1 {
  path: NonEmptyString,
  mode: integer >= 0,
  tracking: "tracked" | "untracked" | "not-applicable",
  inclusion: "included" | "excluded",
  reason: NonEmptyString
}

StoredFileEntryV1 = SnapshotCommonV1 + {
  entry_type: "file", content: StoredBytesV1?
}
StoredDirectoryEntryV1 = SnapshotCommonV1 + {
  entry_type: "directory"
}
StoredSymlinkEntryV1 = SnapshotCommonV1 + {
  entry_type: "symlink",
  symlink_target: string,
  symlink_resolution: "not-followed" | "followed-contained" | "inert-escape",
  content: StoredBytesV1?
}
StoredGitlinkEntryV1 = SnapshotCommonV1 + {
  entry_type: "gitlink",
  recorded_gitlink: GitObjectId,
  checked_out_revision: GitObjectId,
  worktree_state: "clean" | "dirty" | "diverged" | "dirty-and-diverged",
  nested_snapshot: SnapshotHandle?
}
StoredNestedRepositoryEntryV1 = SnapshotCommonV1 + {
  entry_type: "nested-repository",
  nested_identity: NonEmptyString,
  checked_out_revision: GitObjectId,
  worktree_state: "clean" | "dirty" | "diverged" | "dirty-and-diverged",
  nested_snapshot: SnapshotHandle
}
StoredSnapshotEntryV1 = StoredFileEntryV1 | StoredDirectoryEntryV1 |
  StoredSymlinkEntryV1 | StoredGitlinkEntryV1 |
  StoredNestedRepositoryEntryV1

GitSnapshotSourceV1 {
  kind: "git-tree", commit: GitObjectId, tree: GitObjectId
}
ManifestSnapshotSourceV1 {
  kind: "manifest", source_state: "dirty-git" | "non-git"
}

SnapshotRootV1 {
  capture_contract: "snapshot-capture.v1",
  source: GitSnapshotSourceV1 | ManifestSnapshotSourceV1,
  scope: set<NonEmptyString> by path,
  exclusions: set<SnapshotExclusion> by exclusion.path,
  entries: set<StoredSnapshotEntryV1> by entry.path,
  versions: SnapshotVersionsV1
}

NavigationResultObjectV1 {
  snapshot: SnapshotHandle,
  request: QueryRequest,
  selection: RouteResultSemanticV1 | ReadResultSemanticV1 |
    RelatedResultSemanticV1,
  versions: NavigationVersionsV1
}

AnalysisContextObjectV1 {
  context_kind: "standards-change",
  subjects: set<ChangedPolicyUnit> by subject.policy,
  changes: set<ChangeDescriptor> by typed-change-key,
  semantic_proposals: set<SemanticProposal> by proposal.policy,
  versions: AnalysisContextVersionsV1
}

FactRequirementObjectV1 {
  context: AnalysisContextHandle,
  fact: CanonicalId,
  fact_semantic_revision: integer >= 1,
  fact_contract_digest: Digest,
  value_contract: FactValueContract,
  answer_contract: CanonicalId,
  evidence_contract: CanonicalId,
  authorization_capability: CanonicalId,
  provider_contract_versions: ProviderVersionsV1,
  contract_version: "fact-requirement.v1"
}

ProviderClaimV1 {
  provider: CanonicalId,
  provider_contract_version: NonEmptyString,
  immutable_input_view: Digest,
  claim_digest: Digest
}

FactObservationObjectV1 {
  requirement: FactRequirementHandle,
  value: FactValue,
  evidence: set<EvidenceReference> by evidence.id,
  authorization: AuthorizationReference,
  provider_claim: ProviderClaimV1?,
  contract_version: "fact-observation.v1"
}

RelationshipFingerprintV1 { edge: EdgeId, fingerprint: Digest }
CoverageHorizonV1 {
  id: CanonicalId,
  provider: CanonicalId,
  version: integer >= 1,
  digest: Digest,
  members: set<CoverageHorizonMember> by member.id
}

CoverageViewObjectV1 {
  subject: CanonicalId,
  owner: CanonicalId,
  semantic_revision: integer >= 1,
  representation_digest: Digest,
  structural_digest: Digest,
  relationship_kinds: set<CanonicalId> by value,
  relationship_fingerprints: set<RelationshipFingerprintV1> by edge,
  relationship_kind_contract_version: integer >= 1,
  relationship_provider_contract_digest: Digest,
  applicability_language_version: 1,
  applicability_program_digests: set<Digest> by value,
  fact_schema_digest: Digest,
  horizon: CoverageHorizonV1,
  identity_resolution_contract_version: NonEmptyString,
  coverage_contract_version: NonEmptyString,
  attestation_contract_version: NonEmptyString,
  authorization_contract_version: NonEmptyString,
  evidence_provider_contract_version: NonEmptyString
}

CoverageRequirementObjectV1 {
  coverage_view: CoverageAuthorityViewHandle,
  subject: CanonicalId,
  owner: CanonicalId,
  semantic_revision: integer >= 1,
  relationship_kinds: set<CanonicalId> by value,
  horizon: CanonicalId,
  required_evidence_contract: CanonicalId,
  contract_version: "coverage-requirement.v1"
}

CoverageAttestationClaimV1 {
  requirement: CoverageRequirementHandle,
  conclusion: "complete",
  evidence: set<EvidenceReference> by evidence.id,
  explicit_exclusions: set<EvidenceReference> by evidence.id,
  rationale: NonEmptyString,
  auditor_provenance: NonEmptyString
}

CoverageAttestationObjectV1 {
  requirement: CoverageRequirementHandle,
  conclusion: "complete",
  evidence: set<EvidenceReference> by evidence.id,
  explicit_exclusions: set<EvidenceReference> by evidence.id,
  rationale: NonEmptyString,
  auditor_provenance: NonEmptyString,
  authorization: AuthorizationReference,
  contract_version: "coverage-attestation.v1"
}

CoverageCertificateObjectV1 {
  coverage_view: CoverageAuthorityViewHandle,
  requirement: CoverageRequirementHandle,
  attestation: CoverageAttestationHandle,
  subject: CanonicalId,
  owner: CanonicalId,
  semantic_revision: integer >= 1,
  horizon_digest: Digest,
  relationship_digest: Digest,
  evidence_digests: set<Digest> by value,
  applicability_contract_version: NonEmptyString,
  fact_schema_digest: Digest,
  coverage_contract_version: NonEmptyString,
  attestation_contract_version: NonEmptyString,
  authorization_contract_version: NonEmptyString,
  evidence_provider_contract_version: NonEmptyString
}

PolicyInspectionObjectV1 {
  snapshot: SnapshotHandle,
  policy: CanonicalId,
  declaration: CanonicalModuleDeclaration | PolicyUnitDeclaration,
  representation_digest: Digest,
  structural_digest: Digest,
  provenance: ProvenanceRecord,
  versions: PolicyInspectionVersionsV1
}

RelationshipInspectionObjectV1 {
  snapshot: SnapshotHandle,
  relationship: RelationshipSummary,
  policy_semantics: PolicyRelationshipInspection | null,
  compiler_provenance: ProvenanceRecord,
  versions: RelationshipInspectionVersionsV1
}

ConsumerDispositionV1 {
  obligation: ObligationId,
  obligation_fingerprint: DecisionFingerprint,
  result: NonEmptyString,
  rationale: NonEmptyString,
  evidence: set<EvidenceReference> by evidence.id,
  authorization: AuthorizationReference
}
ImpactDispositionV1 {
  obligation: ObligationId,
  obligation_fingerprint: DecisionFingerprint,
  result: NonEmptyString,
  rationale: NonEmptyString,
  evidence: set<EvidenceReference> by evidence.id,
  authorization: AuthorizationReference
}

AnalysisRootObjectV1 {
  base_snapshot: SnapshotHandle,
  proposed_snapshot: SnapshotHandle,
  context: AnalysisContextHandle,
  authorization_view: AuthorizationAuthorityView,
  provider_view: ProviderAuthorityView,
  fact_requirements: set<FactRequirementHandle> by (kind, schema_version, id),
  fact_observations: set<FactObservationHandle> by (kind, schema_version, id),
  coverage_views: set<CoverageAuthorityViewHandle> by (kind, schema_version, id),
  coverage_requirements: set<CoverageRequirementHandle> by (kind, schema_version, id),
  consumer_dispositions: set<ConsumerDispositionV1> by obligation,
  impact_dispositions: set<ImpactDispositionV1> by obligation,
  coverage_attestations: set<CoverageAttestationHandle> by (kind, schema_version, id),
  coverage_certificates: set<CertificateHandle> by (kind, schema_version, id),
  versions: AnalysisRootVersionsV1
}
```

The navigation semantic variants are the corresponding v11 result records with
`kind`, `handle`, `next`, summaries, rendered text, and cache state removed.
Their discriminant, targets, scopes, authority classifications, reasons,
states, and exact read bytes remain. Change, scope, reason, operation, work,
decision, and handle-set keys use the exact typed contracts in the
[identity/version matrix](identity-version-object-matrix.md); identity bytes are
never substituted as an ordering key.

An included file requires `content`; an excluded file forbids it. A symlink
with `followed-contained` and `inclusion = "included"` requires `content`; all
other symlinks forbid it. A clean gitlink may omit `nested_snapshot`; every
dirty or diverged gitlink requires it. Provider-backed observations require
`provider_claim`; human-authorized observations forbid it.

## Coherence Predicates

Object construction and aggregate resolution enforce these predicates at the
named boundary:

1. Every `get` verifies canonical bytes and handle identity. Object construction
   verifies that every dependency resolves under the same repository contract
   and has the required object kind and payload contract.
2. Snapshot construction verifies entries are closed, unique by path, and
   byte/digest/length exact;
   every nested handle resolves before its parent is published.
3. Analysis-root validation proves its context equals fresh classification of
   the exact base and proposed snapshots under the context's recorded changes,
   proposals, and versions.
4. Analysis-root validation proves every observation's requirement is in the
   root dependency set, names the root context, matches current
   fact/answer/evidence/provider contracts, and is accepted by the root
   authorization and provider views. At most one observation exists per
   requirement.
5. Analysis-root validation proves each disposition names one freshly derived obligation, carries that
   obligation's exact current fingerprint, satisfies its review contract, and
   is authorized. At most one disposition exists per obligation and kind.
6. Coverage-chain construction proves requirement fields equal the resolved view. An attestation names
   that requirement and satisfies its evidence and authorization contracts. A
   certificate's three dependencies form that exact object-local chain, and
   every repeated digest, subject, and version equals the resolved dependency
   value. Analysis-root validation additionally checks current authorization.
7. Analysis-root validation proves every coverage view equals the coverage projection rederived for its subject
   from the applicable root snapshot semantic payload and independent horizon.
   Full snapshot identity and attestation artifacts do not enter view identity.
8. Policy and relationship inspection adapters prove their objects equal fresh compilation from their
   exact snapshot. Navigation selection equals fresh query execution against
   its exact snapshot and normalized request.
9. Analysis-root validation requires the exact materialized child handles used
   by its current projection and rejects extra, missing, or unrelated children.
   Current material work, derived certificates, reading plan, result status,
   completion proof, and next operations equal a fresh deterministic projection
   of the normalized root. Dormant-valid decisions remain stored but do not
   block completion.
10. No aggregate publishes until every referenced dependency has been
    published and re-resolved. Cycles and self-reference reject.

## Construction Order

Preparation constructs or resolves snapshots, then context, reusable
requirements/observations and coverage objects, and finally the normalized
analysis root. Resolution projects the supplied analysis root, validates one
submission, constructs any new requirement-dependent object, normalizes the
decision set, then constructs a new analysis root. A coverage submission
contains only `CoverageAttestationClaimV1`. The bound analysis kernel verifies
that the claim names the current coverage requirement, validates its evidence
against that requirement, obtains and validates the caller's authorization
from the trusted execution context, and only then constructs and publishes
`CoverageAttestationObjectV1`. A caller never supplies an attestation handle,
stored-object contract version, or authorization record.

Policy and relationship inspection objects materialize from one exact
snapshot. Navigation objects materialize from one exact snapshot and query.
Certificates materialize from their three upstream coverage objects. Equal
payloads reached through different operation order produce the same handle.

## Re-Plan Triggers

Re-plan if a payload needs its own handle, a dependency would point to a
descendant or itself, a new public inspectable kind is required, a stored
derived-work projection becomes authority, or exact evidence/authorization
cannot be represented without ambient state.
