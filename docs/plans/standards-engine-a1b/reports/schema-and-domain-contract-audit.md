# A1b Schema And Domain Contract Audit

**Status:** Proposed planning authority

**Audit base:** accepted comparison commit
`c4408363752b10060f631247f3e2f1fa26eae003`, tree
`84477150bd368a168dd04da3770de55c23bbb817`

The audited v10 schema, generator, and validator are byte-identical between
that accepted base and the superseded `f41037bf71deddba36056b27d418fe767a7cfb62`
candidate. Their SHA-256 digests are respectively
`0413a07fde2021b75d1c9de97b164773c6f60a94c365bab5b92f0c709b2e0a9f`,
`d77732477c14e2fff1ea5d3b27427991f0a5b38e1f3d9fe37a7490a7378401ba`, and
`669dcec8b80b1be63be402e9852b5e54824eae52f348d08ae0b7b9bdab3a319f`.

## Decision

The public JSON Schema owns serialized request, result, submission, inspection,
and public handle shapes. It does not own identity construction,
authorization, state transitions, persistence, policy-impact meaning, or
projection lifecycle.

`jsonschema.Draft202012Validator` is the sole executable owner of Draft 2020-12
validation. A1b does not implement, override, or independently certify JSON
Schema semantics. Generated Python models call the same compiled validator
before construction and contain no keyword interpreter.

## Public Schema Profile

The v11 schema declares the exact meta-schema URI
`https://json-schema.org/draft/2020-12/schema`. That dialect's meta-schema
declares these required vocabularies:

| Vocabulary URI | Required | A1b use |
| --- | --- | --- |
| `https://json-schema.org/draft/2020-12/vocab/core` | true | Schema identity, references, definitions, and annotations |
| `https://json-schema.org/draft/2020-12/vocab/applicator` | true | Object/array application and `oneOf` |
| `https://json-schema.org/draft/2020-12/vocab/unevaluated` | true | Selected by the dialect; no reachable unevaluated keyword is authored |
| `https://json-schema.org/draft/2020-12/vocab/validation` | true | Type, const, enum, required, cardinality, pattern, and numeric constraints |
| `https://json-schema.org/draft/2020-12/vocab/meta-data` | true | `title`, `description`, and `default`; no reachable `deprecated`, `readOnly`, `writeOnly`, or `examples` keyword is authored |
| `https://json-schema.org/draft/2020-12/vocab/format-annotation` | true | Selected by the dialect; no reachable `format` keyword is authored or asserted |
| `https://json-schema.org/draft/2020-12/vocab/content` | true | Selected by the dialect; no reachable content keyword is authored |

No custom vocabulary or extension keyword is accepted. A1b does not enable the
optional format-assertion vocabulary
`https://json-schema.org/draft/2020-12/vocab/format-assertion`.

Within that exact dialect, v11 uses this projection surface:

```text
$schema, $id, $ref, $defs,
title, description, default,
type, const, enum, oneOf,
required, properties, additionalProperties,
items, minItems, uniqueItems,
minLength, pattern, minimum
```

This is a projection-compiler profile, not a locally implemented validator
subset. `jsonschema` validates every schema and instance. The projection
compiler rejects a reachable construct outside this list because it cannot
promise a complete Python or agent-tool representation.

References are same-resource `#/$defs/...` references only. Runtime retrieval,
remote resources, custom vocabularies, format assertion, keyword overrides,
and dynamic references are not admitted.

All current patterns are anchored ASCII identifier or digest expressions. The
v11 projection profile admits only literals, ASCII character classes and
ranges, grouping-free repetition, anchors, and escaped punctuation. Backrefs,
lookaround, Unicode properties, inline flags, alternation, and engine-specific
extensions are unsupported. This keeps Python and agent-tool consumers within
one demonstrably common pattern surface. The validator remains the validation
owner.

The canonical root and `$defs` contain only definitions reachable from the
four public operations declared by the interface contract. Internal authoring
declarations move to their existing domain loaders and contracts. A public
definition outside the operation closure is invalid rather than silently
retained.

## Extension Disposition

Version 10 contains five `x-standards-engine-*` families. Version 11 removes all
of them from the JSON Schema.

| Former family | Former concern | V11 owner and representation |
| --- | --- | --- |
| `contract` | Versions, operations, capabilities, bootstrap, projection targets, state machine, impact groups | Closed `a1-interface.toml` owns operation names, input/result roots, interface versions, and capability selection. `standards_engine` owns bootstrap. `standards_analysis` owns state transitions and impact-group selection. Build invocation owns selected projection targets. |
| `identity` | Domain, included fields, excluded fields | Each domain Module constructs one typed identity record and invokes `standards_identity`. Identity rules are executable code plus domain fixtures, not schema annotations. |
| `invariants` | Cross-field and semantic rules | Applicability, Metadata, Analysis, Policy Impact, Graph, and Authority own typed constructors and failures. The public schema owns only representable shape constraints. |
| `projection` | Pending/complete result derivation | `standards_analysis.project` owns deterministic domain projection; `standards_engine` exhaustively adapts it to generated public results. |
| `authority` | Trusted capability injection | `standards_engine` capability adapter and authorization contract own trusted execution context; callers cannot supply it through the public schema. |

### Machine-readable v11 authority

The complete proposed serialized algebra is owned by
[`a1-contract-v11.schema.json`](a1-contract-v11.schema.json), SHA-256
`349c06fce684accce477675a9048690100b999058fa25463b2f656028d666d50`.
The complete proposed operation/capability Interface is owned by
[`a1-interface-v11.toml`](a1-interface-v11.toml), SHA-256
`8d4adb47f90f0c8168873d89578b292c728badad7334d5f15c15125279ec6b00`.
These exact admitted bytes are planning authority. Milestone 1 compiles them
as isolated inputs; Milestone 3 promotes them byte-for-byte to the canonical
production paths. Discovering that either artifact needs a shape or version
change requires re-planning before implementation continues.

The interface artifact has one closed schema:

```text
schema_version
interface_schema_version
request_contract_version
result_projection_version

operations[]:
  id
  input_definition
  result_definitions[]
  capability | capability_by_submission{}
```

It contains exactly `query`, `prepare`, `resolve`, and `inspect`. The contract
compiler verifies that every named definition exists, every operation closure
is complete, every submission discriminant has one capability, and no extra
operation or field exists. Agent-tool generation and facade dispatch consume
this one operation contract.

The schema artifact owns the exact reachable definition closure. The compiler
derives that closure from the four operation roots and requires exact set
equality with `$defs`; this report deliberately does not duplicate mutable
definition names or counts. Internal authoring definitions outside the
operation closure are absent. Added, removed, or renamed definitions require a
new admitted schema artifact.

Every public handle is the exact closed record `kind`, `id`, and
`schema_version = 4`; the schema owns each kind and content-addressed ID prefix.
There is no generic immutable-authority handle. `ProviderInputReference` is the
exact closed reference allowed in provider authority. Stored authority-object
records and their local/aggregate semantic invariants are defined separately
in [authority-object contracts](authority-object-contracts.md).

V11 changes `FactRequirement` to the semantic object: it excludes `prompt`
and `dependent_programs`. New `FactRequirementWork` contains
`requirement`, `prompt`, and `dependent_programs`, and
`PendingResult.fact_requirements` uses that projection.
`FactRequirementInspectionResult` continues to expose the semantic
`FactRequirement`. Certificate provenance has no generation timestamp.

Snapshot bootstrap is composition configuration, not a public operation.
Projection target selection is a build command input, not contract semantics.
Analysis state transitions and graph-group selection remain typed constants and
behavior in `standards_analysis`.

## Validation And Construction Flow

```text
strict JSON value
      |
      v
compiled Draft202012Validator
      |
      +-- invalid -> stable ContractFailure adapter
      |
      v
generated immutable model construction
      |
      v
domain adapter and domain-owned invariants
```

The stable failure adapter records outcome, code, definition, instance pointer,
schema pointer, keyword, and nested causes. It never exposes dependency
exception types or message text as contract authority.

Defaults remain schema annotations. A1b never injects a schema default.
Generated constructors represent an omitted non-required property with one
private `MISSING` sentinel that cannot appear in JSON; explicit `null`
remains distinct. Serialization omits `MISSING` and preserves every explicit
value. Required properties have no constructor default.

## Evidence Boundary

A1b relies on `jsonschema`'s maintained upstream Draft implementation and its
upstream conformance process. The repository does not copy or execute the full
official JSON Schema corpus and does not claim to re-certify Draft 2020-12.

Repository evidence covers only:

- the exact dependency identity and validator class;
- schema self-validation through `check_schema`;
- same-resource reference configuration with no retrieval;
- known A1 Boolean/integer, Unicode, `pattern`, and `uniqueItems` regressions
  through the production adapter;
- stable error adaptation;
- complete public-operation reachability;
- generated model and agent-tool projection; and
- rejection of unsupported projection constructs.

Generated freshness, adapter correctness, projection completeness, domain
invariants, and public facade behavior remain separate claims.

## Re-Plan Triggers

Re-plan if a reachable contract requires an excluded projection construct,
remote reference, custom vocabulary, format assertion, unsupported pattern,
validator extension, runtime schema discovery, or default injection semantics.
