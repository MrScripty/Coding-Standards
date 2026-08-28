# A1b Identity, Version, And Authority-Object Matrix

**Status:** Proposed planning authority

## Identity Encoding Version 2

`standards_identity` owns one deterministic encoding:

- a JSON-compatible UTF-8 encoding defined byte-for-byte below;
- `null`, Boolean, integer, string, array, and string-keyed object values only;
- no floating-point values;
- object keys sorted by Unicode codepoint;
- array order preserved unless the owning typed identity record declares and
  constructs a semantic order;
- strings and keys preserved codepoint-for-codepoint; and
- compact separators with no representation-dependent whitespace.

The encoder performs no Unicode normalization, equality, sorting of semantic
sets, deduplication, defaulting, coercion, or field selection. Domain Modules
construct typed identity records and normalize only fields whose documented
meaning requires it. `standards_applicability` retains its explicit NFC domain
contract and its existing v1 digests after byte-level proof that it does not use
the replaced generic serializer.

Raw content digests remain SHA-256 over exact bytes and do not use identity
encoding.

### Exact byte grammar

- `null`, `true`, and `false` use those exact ASCII bytes. Boolean is
  tested before integer and is never accepted as integer.
- Integer zero is `0`. Other integers are optional ASCII `-` followed by
  base-10 digits with no leading zero, plus sign, exponent, decimal point, or
  implementation-size limit.
- Strings contain only Unicode scalar values. Lone UTF-16 surrogate code points
  are invalid.
- U+0022 and U+005C escape as `\"` and `\\`. U+0000 through U+001F
  escape as lowercase `\u00xx`. Every other scalar is emitted as its
  unescaped UTF-8 sequence; no optional short escape or ASCII-only escaping is
  used.
- Arrays use `[`, `,`, and `]` with no whitespace and preserve authored
  order.
- Objects require string keys, sort them by Unicode scalar sequence, and use
  `{`, `,`, `:`, and `}` with no whitespace. Codepoint-distinct keys
  remain distinct.

The hash frame is:

```text
ASCII "coding-standards:identity:v2\0"
u32be byte length of domain
UTF-8 domain
u32be byte length of ID prefix
ASCII ID prefix
u64be byte length of encoded value
encoded value
```

Domain is nonempty ASCII `[a-z0-9][a-z0-9.:-]*`. ID prefix is nonempty ASCII
`[a-z][a-z0-9.-]*`. The digest is SHA-256 over the complete frame and output
is exactly `<prefix>:sha256:<64 lowercase hexadecimal digits>`.

Each domain owner declares one identity domain, prefix, and typed material
record. Storage-envelope, public-handle, result-projection, generator, build,
and release fields are excluded unless the domain owner proves they materially
change the represented semantic value. Exact framing, control characters,
non-ASCII scalars, codepoint-equivalent strings, very large integers,
Boolean/integer separation, invalid surrogates, key ordering, and length
boundaries require fixtures.

## Direct Authority Objects

Every public inspectable handle directly identifies one immutable stored
semantic object. There is no child-owner lookup table, store scan, cache index,
or separately supplied version record.

```text
AuthorityObjectEnvelope v1
  envelope_kind: "authority-envelope"
  envelope_version: 1
  object_kind: nonempty opaque Unicode-scalar string
  semantic_id: nonempty opaque Unicode-scalar string
  direct_dependencies: sorted unique AuthorityObjectReferenceV1[]
  payload_contract: nonempty opaque Unicode-scalar string
  payload: identity-v2 JSON-compatible typed value
```

Envelope bytes are exactly the identity-v2 canonical typed encoding of that
seven-field object, without the identity hash frame. References contain exactly
`object_kind` and `semantic_id`; unknown fields, floats, noncanonical bytes,
duplicate or unsorted references, and envelopes larger than 67,108,864 bytes
reject. The size limit is an A1b storage-support bound, not semantic identity.
Envelope kind and version provide structural dispatch only. Object kinds and
payload contracts remain exact opaque values owned by injected domain codecs;
Authority neither normalizes them nor infers domain meaning.

Every public handle has `schema_version = 4`, one exact handle kind, and its
schema-owned wire ID representation. `standards_authority.resolve` treats the
supplied semantic ID as an opaque exact storage key, requires
handle/envelope equality, verifies bytes and envelope, dispatches by the
structural object kind to the injected owner codec, requires the codec to
validate and recompute the same semantic identity, and verifies direct
dependency kinds before returning the typed object. Authority does not infer a
generic relationship between ID spelling and object kind. Owner-local
codec sets are injected explicitly and their aggregate closure is derived from
the executable owners specified by the [C7 design](c7-design-proposal.md).
Envelope
format is a storage-decoding promise and does not define domain identity.
Missing storage is `unavailable`, contradictory content is `invalid`, and a
well-formed unsupported contract is `unsupported`.

Operation compatibility keys and stored semantic identities are distinct. The
initial exact keys are `(route, 2)`, `(read, 2)`, `(related, 2)`, and
`(analysis, 2)`. Revisions are scoped and allocated monotonically per
operation, may contain gaps, and have no range-compatibility meaning. Each
stored record independently has a content-addressed semantic ID under
`coding-standards:operation-authority-contract-identity:v1`; its owner codec
owns the rendered grammar. Compatibility keys express supported promises;
semantic IDs identify exact record content. The
`operation-authority-contract.v2` payload contract governs representation only.

## Public Object Matrix

| Public handle | Stored object kind | Payload contract | Required dependencies |
| --- | --- | --- | --- |
| `ContentSnapshotHandle` | `content-snapshot` | `content-snapshot.v2` | Exact sorted logical Unicode-scalar component paths and exact file bytes, with padded standard-Base64/digest/length as verified projections; no scope, exclusion, directory, mode, symlink, nested snapshot, Git, filesystem, or Adapter observation |
| `StandardsAuthorityViewHandle` | `standards-authority-view` | `standards-authority-view.v1` | ContentSnapshot, exactly one selected contract per operation, and exact role-to-semantic-authority references |
| `ExecutionClosureHandle` | `execution-closure` | `execution-closure.v2` | Exact sorted unique side- and role-qualified roots, including the selected operation contract; transitive dependencies are deterministically derived from immutable owner references |
| `NavigationHandle` | `navigation-result` | `navigation-result.v1` | Normalized query, semantic result, and operation-specific ExecutionClosure |
| `AnalysisHandle` | `analysis-root` | `analysis-root.v1` | Roots-only material AnalysisExecutionClosure, narrow context, dependency-valid fact observations and dispositions, authored coverage attestations, and exact consumed provider/authorization references; complete views, hypothetical future authority, and derived requirements/certificates are excluded |
| `PolicyHandle` | `policy-inspection` | `policy-inspection.v1` | Canonical policy identity, semantic projection, and material ExecutionClosure |
| `RelationshipHandle` | `relationship-inspection` | `relationship-inspection.v1` | Compiled edge identity, semantic projection, and material ExecutionClosure |
| `CertificateHandle` | `coverage-certificate` | `coverage-certificate.v1` | Coverage view, requirement, and attestation object handles |
| `CoverageAuthorityViewHandle` | `coverage-view` | `coverage-view.v1` | Exact coverage-relevant semantic payload and owner-local authority references; derivation view is excluded provenance |
| `CoverageRequirementHandle` | `coverage-requirement` | `coverage-requirement.v1` | Coverage-view object handle |
| `CoverageAttestationHandle` | `coverage-attestation` | `coverage-attestation.v1` | Requirement object handle, evidence, and authorization |
| `AnalysisContextHandle` | `analysis-context` | `analysis-context.v1` | Narrow changed-policy semantic payload and normalized proposals; full view handles and relationship topology excluded |
| `FactRequirementHandle` | `fact-requirement` | `fact-requirement.v1` | Analysis-context object handle plus fact/answer/evidence authority |
| `FactObservationHandle` | `fact-observation` | `fact-observation.v1` | Requirement object handle, value, evidence, and authorization |

The object-kind vocabulary is closed in A1b. Adding a kind changes the authority
repository contract and public inspectable union. The repository does not
expose arbitrary blobs, object enumeration, graph traversal, collection,
remote storage, or mutable indexes.

Stored payloads never include their own handle. After resolution verifies the
envelope and owner-recomputed semantic ID, the public projection injects that
handle. Dependencies always point upstream from content and owner-local
semantic authorities through views and execution closures to results. No child
object references an analysis root. The exact payload and dependency contracts
are defined in the [C7 design](c7-design-proposal.md); SQLite owns only envelope
persistence.

## Semantic Identity Migration

The following semantic identities were computed through the former recursive
NFC serializer and advance atomically:

| Concern | Current domain | A1b domain/result |
| --- | --- | --- |
| Snapshot lifecycle identity | `snapshot:v3` | Replaced by exact logical-path/raw-byte `content-snapshot.v2` object and handle v4 |
| Standards authority composition | absent | `standards-authority-view.v1` object and handle v4 |
| Material operation authority | implicit or copied version records | roots-only `execution-closure.v2` object and handle v4 |
| Operation-family role/coherence promise | implicit shared configuration | One exact `(operation, compatibility_revision)` promise and independently content-addressed semantic object for each route, read, related, and analysis family; `operation-authority-contract.v2` owns payload representation only |
| Navigation lifecycle identity | `navigation:v3` | Replaced by `coding-standards:navigation-result:v1`, whose typed record includes the route/read/related discriminant, and handle v4 |
| Analysis lifecycle identity | `analysis:v3` | Replaced by `analysis-root.v1` authority object and handle v4 |
| Obligation | `obligation:v2` | `obligation:v3` |
| Analysis context | `analysis-context:v1` | Replaced by `analysis-context.v1` authority object and handle v4 |
| Fact requirement | `fact-requirement:v1` | Replaced by `fact-requirement.v1` authority object and handle v4 |
| Fact observation | `fact-observation:v1` | Replaced by `fact-observation.v1` authority object and handle v4 |
| Impact trace | `impact-trace:v1` | `impact-trace:v2` |
| Coverage authority view | `coverage-authority-view:v2` | Replaced by `coverage-view.v1` authority object and handle v4 |
| Coverage audit requirement | `coverage-audit-requirement:v2` | Replaced by `coverage-requirement.v1` authority object and handle v4 |
| Coverage attestation | `coverage-attestation:v2` | Replaced by `coverage-attestation.v1` authority object and handle v4 |
| Consumer coverage certificate | `consumer-coverage-certificate:v2` | Replaced by `coverage-certificate.v1` authority object and handle v4 |
| Authorization authority | `authorization-authority-view:v1` | Replaced by exact consumed `authorization-grant.v1` objects; referenced only by successful material decisions |
| Provider authority | `provider-authority-view:v1` | Replaced by exact consumed `provider-authority.v1` objects; deterministic no-observation stores none |
| Policy-unit structural digest | implicit normalized structural encoding | `policy-unit-structure.v2` identity encoding |
| Analysis ordering and dedup keys | generic canonical bytes | Typed domain keys; not identities |

The policy-impact edge algorithm, graph edge identities, raw representation
digests, and applicability digest domains remain unchanged only after focused
tests prove they do not consume the retired encoder and their semantic inputs
are unchanged.

Directly stored inspectables have one owner-defined semantic ID. Their public
handle represents that ID; envelope and handle wire formats are separate
compatibility promises. Domain-specific IDs remain for semantic records that
are not directly stored objects, including obligations and impact traces.

## Domain Ordering And Deduplication

The following table is the closed A1b replacement for every production use of
generic canonical bytes as an ordering, grouping, deduplication, or conflict
oracle. Scalar strings compare by Unicode scalar sequence. Optional values use
`(0)` for absent and `(1, value)` for present. Tuples compare
lexicographically. A set-like field is first normalized by its declared member
key. Two values with the same key collapse only when the owner finds their
normalized typed records equal; two unequal records with the same key are
`invalid`. Typed-record equality compares the declared fields recursively,
keeps Boolean distinct from integer, preserves codepoint-distinct strings, and
uses authored or owner-normalized array order as declared. It never encodes the
records first. None of these keys is an identity hash input until its owner
places the already-normalized value in a typed identity record.

| Owner and value | Exact key or order |
| --- | --- |
| Analysis `ReviewScope` | `whole-artifact -> (0)`; `structured -> (1, heading_path tuple)`. Scope compatibility is key equality only. |
| Analysis `ChangeDescriptor` | `(change_kind_rank, accepted_ids, proposed_ids, review_scope_key, optional accepted_module, optional proposed_module)`, where IDs are scalar-sorted sets and kind rank is `modification`, `addition`, `removal`, `move`, `split`, `merge`. |
| Analysis changed-policy subjects | Canonical policy ID. One policy cannot have two distinct subject records. |
| Analysis semantic proposals | Canonical policy ID. One policy cannot have two distinct proposals. |
| Provider immutable content/view inputs | Complete handle key `(kind, schema_version, id)`. Base and proposed roles remain authored fields; additional inputs are key-sorted. |
| Consumer review group | `(canonical consumer ID, review_scope_key, review-contract ID)`. Overlapping scopes do not merge. |
| Policy-impact selection reason | `(source policy-unit ID, edge ID, relation, evidence owner, trace_keys)`, with trace key `(graph_side_rank, trace ID, applicability_rank)`, graph-side rank `accepted`, `proposed`, and applicability rank `true`, `false`, `unknown`. |
| Consumer evidence-owner set | Canonical evidence-owner ID. |
| Reading reason | Variant rank and fields: `(0, obligation)` for `consumer-review-obligation`; `(1, projection)` for `routing-base`; `(2, rule, scalar-sorted fact IDs)` for `routing-rule`; `(3, edge, source)` for `requires`; `(4, edge, source)` for `specializes`. |
| Reading entry grouping | `(target, review_scope_key)`. Reasons are unioned by reading-reason key; authority is derived from target and conflicting authority is invalid. State rank is `selected`, `unresolved`, `conditional`. |
| Reading entry presentation order | `(minimum order_class, minimum order_rank within that class, target, review_scope_key)`. The first two values are routing/analysis presentation inputs and must be nonnegative integers. |
| Fact requirement work | Requirement handle `(kind, schema_version, id)`; dependent program IDs are scalar-sorted. |
| Obligation work | Obligation ID. Different records under one ID are invalid. |
| Accepted fact observations | Requirement semantic-reference key `(object_kind, semantic_id)`; different observations for one requirement form separate successor branches and cannot coexist in one state. Stored observation references use the same key. |
| Accepted dispositions | `(obligation ID, decision_kind_rank)`, with decision rank `consumer`, `impact`. Different records under one key form separate successor branches and cannot coexist in one state. |
| Coverage decisions | Coverage-requirement semantic-reference key `(object_kind, semantic_id)`; stored attestation references use the same key. Certificates are derived and not repeated in AnalysisState. |
| `NextOperation` | `(operation_rank, request_kind_rank, optional target, optional obligation_id, optional requirement_id, optional view_handle, optional analysis_handle)`. Operation rank is `query`, `resolve`, `inspect`; query request rank is `route`, `read`, `related`; resolve request rank is `provide-fact`, `consumer-disposition`, `impact-disposition`, `coverage-attestation`; inspect has one request rank. |
| Result changes | The underlying `ChangeDescriptor` key. Requirements and obligations use the work keys above; reading entries use their presentation key; next operations use `NextOperation` key. |
| ContentSnapshot files | RepositoryPath components compare by Unicode scalar sequence with a prefix before its extension; entries compare by that logical path. Identity binds decoded exact bytes, not Base64/digest/length projections. |
| StandardsAuthorityView selections | Operation-contract selections use operation rank `route`, `read`, `related`, `analysis`; semantic-authority selections use canonical role. Unequal authority references under one operation or role are invalid. |
| ExecutionClosure references | Roots use `(side, role, object_kind, semantic_id)`. Transitive dependencies use `(object_kind, semantic_id)` and are derived in deterministic traversal order rather than persisted as caller-authored closure membership. |
| Policy-unit structure | Aliases, predecessors, and successors are scalar-sorted canonical IDs; heading-path component order is authored; corpus records use canonical policy-unit ID. |
| Authority-object sets | The exact member keys exported by owner-local executable codec sets; stored references use `(object_kind, semantic_id)`, while public-only handle sets use `(kind, schema_version, id)`. |

Generic string-keyed map encoding still sorts keys to produce deterministic
identity bytes, but that representation rule never decides domain equality.
Applicability keeps its separate v1 normalization, equality, and digest
contract. The old facade candidate scan/dedup has no A1b key because direct
handle resolution deletes that algorithm rather than translating it.

Required fixtures permute every set-like input, retain identical results under
input reordering, change identity when a semantic member changes, and reject a
same-key/different-value conflict. Reading fixtures additionally cover multiple
reasons, exact scope separation, direct-plus-dependency selection, and state
collapse. Next-operation fixtures cover every variant, optional-field boundary,
deduplication, and deterministic ordering without encoded-byte comparison.

## Public Contract Versions

| Contract | Current | A1b |
| --- | --- | --- |
| Interface/schema | 10 | 11 |
| Request contract | 2 | 3 |
| Result projection | 2 | 3 |
| Public handle schema | mixed/current 3 | universal 4 |
| Identity encoding | implicit NFC v1 | codepoint-preserving v2 |
| Authority object envelope | absent | 1 |
| Content/view/closure/navigation/analysis payloads | split implementations and version bags | owner-scoped payload 1 each |

Version 10, every former handle representation, and every former persisted
state are `unsupported`. No compatibility parser, converter, alias, or fallback
is admitted.

The former analysis contract/schema umbrella versions `6/3` have no A1b
successors. Analysis payload compatibility is owned by `analysis-root.v1`,
analysis semantic identity by `coding-standards:analysis:v4`, public handle
representation by handle schema 4, result representation by result projection
3, and executable analysis-operation compatibility by `(analysis, 2)`. The
shared `operation-authority-contract.v2` payload contract governs only the
stored operation-record shape.
These independently changing promises are not coupled through another analysis
version pair.
