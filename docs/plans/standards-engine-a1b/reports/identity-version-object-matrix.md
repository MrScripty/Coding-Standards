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

Authority objects use domain
`coding-standards:authority-object:v1` and their exact `object_kind` as the
ID prefix. Domain-specific identities use the domain and prefix declared in the
migration table. Exact framing, control characters, non-ASCII scalars,
codepoint-equivalent strings, very large integers, Boolean/integer separation,
invalid surrogates, key ordering, and length boundaries require fixtures.

## Direct Authority Objects

Every public inspectable handle directly identifies one immutable stored
object. There is no child-owner lookup table, store scan, or cache index.

```text
AuthorityObjectEnvelope v1
  object_kind
  payload_contract
  payload

object id = identity(
  domain="coding-standards:authority-object:v1",
  id_prefix=envelope.object_kind,
  value=envelope,
)
```

Every public handle has `schema_version = 4`, one exact handle kind, and an ID
whose prefix matches the stored object kind. `standards_authority.resolve`
loads by ID, verifies bytes, envelope, object kind, payload contract, and direct
dependency kinds, then returns the typed object. Root-relative policy,
authorization, provider, and analysis coherence is validated by the bound
kernel when resolving or projecting an aggregate root, not by the repository.
Missing storage is `unavailable`, contradictory content is `invalid`, and a
well-formed unsupported version is `unsupported`.

Snapshot, analysis, and navigation remain aggregate semantic roots. Other
inspectables are stored materialized projections with explicit dependency
handles. They are generated, not authored, and can be reproduced from their
dependencies; direct storage makes cold inspection use the same resolution
rule as every root.

## Public Object Matrix

| Public handle | Stored object kind | Payload contract | Required dependencies |
| --- | --- | --- | --- |
| `SnapshotHandle` | `snapshot-root` | `snapshot-root.v1` | Padded standard-Base64 entry bytes with exact digest/length and nested snapshot object handles |
| `NavigationHandle` | `navigation-result` | `navigation-result.v1` | Snapshot object handle |
| `AnalysisHandle` | `analysis-root` | `analysis-root.v1` | Context, base/proposed snapshots, exact materialized requirement/observation/coverage child handles, handle-free dispositions, and attestation handles |
| `PolicyHandle` | `policy-inspection` | `policy-inspection.v1` | Snapshot object handle and canonical policy identity |
| `RelationshipHandle` | `relationship-inspection` | `relationship-inspection.v1` | Snapshot object handle and compiled edge identity |
| `CertificateHandle` | `coverage-certificate` | `coverage-certificate.v1` | Coverage view, requirement, and attestation object handles |
| `CoverageAuthorityViewHandle` | `coverage-view` | `coverage-view.v1` | Exact coverage-relevant semantic payload; derivation snapshot is excluded provenance |
| `CoverageRequirementHandle` | `coverage-requirement` | `coverage-requirement.v1` | Coverage-view object handle |
| `CoverageAttestationHandle` | `coverage-attestation` | `coverage-attestation.v1` | Requirement object handle, evidence, and authorization |
| `AnalysisContextHandle` | `analysis-context` | `analysis-context.v1` | Narrow changed-policy semantic payload and normalized proposals; full snapshot handles and relationship topology excluded |
| `FactRequirementHandle` | `fact-requirement` | `fact-requirement.v1` | Analysis-context object handle and fact/answer/evidence contracts |
| `FactObservationHandle` | `fact-observation` | `fact-observation.v1` | Requirement object handle, value, evidence, and authorization |

The object-kind vocabulary is closed in A1b. Adding a kind changes the authority
repository contract and public inspectable union. The repository does not
expose arbitrary blobs, object enumeration, graph traversal, collection,
remote storage, or mutable indexes.

Stored payloads never include their own handle. After resolution verifies the
envelope and recomputes its handle, the public projection injects that handle.
Dependencies always point upstream: snapshots; then contexts and coverage
views; then requirements; then observations or attestations; then
certificates; and finally analysis/navigation roots. No child object references
an analysis root. The exact payload fields and dependency DAG are defined in
[authority-object contracts](authority-object-contracts.md).

## Semantic Identity Migration

The following semantic identities were computed through the former recursive
NFC serializer and advance atomically:

| Concern | Current domain | A1b domain/result |
| --- | --- | --- |
| Snapshot lifecycle identity | `snapshot:v3` | Replaced by `snapshot-root.v1` authority object and handle v4 |
| Navigation lifecycle identity | `navigation:v3` | Replaced by `navigation-result.v1` authority object and handle v4 |
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
| Authorization authority view | `authorization-authority-view:v1` | `authorization-authority-view:v2` |
| Provider authority view | `provider-authority-view:v1` | `provider-authority-view:v2` |
| Policy-unit structural digest | implicit normalized structural encoding | `policy-unit-structure.v2` identity encoding |
| Analysis ordering and dedup keys | generic canonical bytes | Typed domain keys; not identities |

The policy-impact edge algorithm, graph edge identities, raw representation
digests, and applicability digest domains remain unchanged only after focused
tests prove they do not consume the retired encoder and their semantic inputs
are unchanged.

Directly stored inspectables have no second semantic ID. Their authority-object
handle is their sole identity, and the versioned payload contract supplies the
domain semantics. Domain-specific IDs remain only for semantic records that are
not directly stored objects, including obligations and impact traces.

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
| Provider immutable snapshot inputs | Complete snapshot-handle key `(kind, schema_version, id)`. The base and proposed role positions remain authored fields; additional provider inputs are key-sorted. |
| Consumer review group | `(canonical consumer ID, review_scope_key, review-contract ID)`. Overlapping scopes do not merge. |
| Policy-impact selection reason | `(source policy-unit ID, edge ID, relation, evidence owner, trace_keys)`, with trace key `(graph_side_rank, trace ID, applicability_rank)`, graph-side rank `accepted`, `proposed`, and applicability rank `true`, `false`, `unknown`. |
| Consumer evidence-owner set | Canonical evidence-owner ID. |
| Reading reason | Variant rank and fields: `(0, obligation)` for `consumer-review-obligation`; `(1, projection)` for `routing-base`; `(2, rule, scalar-sorted fact IDs)` for `routing-rule`; `(3, edge, source)` for `requires`; `(4, edge, source)` for `specializes`. |
| Reading entry grouping | `(target, review_scope_key)`. Reasons are unioned by reading-reason key; authority is derived from target and conflicting authority is invalid. State rank is `selected`, `unresolved`, `conditional`. |
| Reading entry presentation order | `(minimum order_class, minimum order_rank within that class, target, review_scope_key)`. The first two values are routing/analysis presentation inputs and must be nonnegative integers. |
| Fact requirement work | Requirement handle `(kind, schema_version, id)`; dependent program IDs are scalar-sorted. |
| Obligation work | Obligation ID. Different records under one ID are invalid. |
| Accepted fact observations | Requirement handle key; different observations for one requirement form separate successor branches and cannot coexist in one state. Stored observation handles are ordered by `(kind, schema_version, id)`. |
| Accepted dispositions | `(obligation ID, decision_kind_rank)`, with decision rank `consumer`, `impact`. Different records under one key form separate successor branches and cannot coexist in one state. |
| Coverage decisions | Coverage-requirement handle key; stored attestation and certificate handles use `(kind, schema_version, id)`. |
| `NextOperation` | `(operation_rank, request_kind_rank, optional target, optional obligation_id, optional requirement_id, optional snapshot_handle, optional analysis_handle)`. Operation rank is `query`, `resolve`, `inspect`; query request rank is `route`, `read`, `related`; resolve request rank is `provide-fact`, `consumer-disposition`, `impact-disposition`, `coverage-attestation`; inspect has one request rank. |
| Result changes | The underlying `ChangeDescriptor` key. Requirements and obligations use the work keys above; reading entries use their presentation key; next operations use `NextOperation` key. |
| Snapshot scopes, exclusions, and entries | Scope path, exclusion path, and entry path respectively. Nested handles use `(kind, schema_version, id)`. |
| Policy-unit structure | Aliases, predecessors, and successors are scalar-sorted canonical IDs; heading-path component order is authored; corpus records use canonical policy-unit ID. |
| Authority-object sets | The exact member keys declared in `authority-object-contracts.md`; handle sets always use `(kind, schema_version, id)`. |

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
| Analysis contract/schema | 6/3 | 7/4 |
| Public handle schema | mixed/current 3 | universal 4 |
| Identity encoding | implicit NFC v1 | codepoint-preserving v2 |
| Authority object envelope | absent | 1 |
| Snapshot/analysis/navigation payload | split implementations | root payload 1 each |

Version 10, every former handle representation, and every former persisted
state are `unsupported`. No compatibility parser, converter, alias, or fallback
is admitted.
