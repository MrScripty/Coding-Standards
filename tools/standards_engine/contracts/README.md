# Standards Engine A1 Contracts

This directory owns the machine-readable A1 navigation and read-only analysis
contract. It contains no engine runtime, repository loader, policy decision, or
controlled-authoring behavior.

## Authority

[`a1-contract.schema.json`](a1-contract.schema.json) is the sole machine shape
authority. It uses JSON Schema Draft 2020-12 and these extension annotations:

- `x-standards-engine-contract` declares operation, projection, version, and
  state-machine metadata.
- `x-standards-engine-identity` declares identity domains and included fields.
- `x-standards-engine-authority` distinguishes trusted adapter inputs from
  caller-authored payloads.

The extensions are contract data. They must not be copied into an independent
state machine or identity table. Python models, JSON validators, agent-tool
definitions, documentation, and renderers must be generated from or checked
against the schema.

Files under [`examples/`](examples/) are projections. Each envelope names one
schema definition and supplies one value. Examples do not add fields, defaults,
variants, or semantics.

## Public Operations

| Operation | Input | Success result | Expected rejection |
| --- | --- | --- | --- |
| `query` | `QueryCall` | `NavigationResult` | `RejectedResult` |
| `prepare` | `PrepareCall` | `PendingPacket` or `CompletedAnalysisReport` | `RejectedResult` |
| `resolve` | `ResolveCall` | `PendingPacket` or `CompletedAnalysisReport` | `RejectedResult` |
| `inspect` | `InspectCall` | `InspectionResult` | `RejectedResult` |

Trusted capability context is injected by the Python composition root or tool
adapter. It is not accepted from a caller-authored request body. Tool exposure
does not grant a capability.

A trusted source provider issues the initial snapshot handle when an engine or
tool session is established. Callers receive that opaque handle rather than a
repository path. Calls always carry it explicitly, and an adapter cannot
substitute the ambient current tree for a missing or stale handle.

Contract version `1` has one accepted representation. Incompatible contract
changes require a new version and migration decision; unknown versions are
`unsupported` and do not select a compatibility parser.

## Identity Serialization

Identity-bearing values use canonical JSON:

- UTF-8 encoding;
- NFC-normalized model strings;
- lexical object-key order;
- array order preserved when semantically meaningful;
- canonical strings for enums;
- JSON booleans and base-10 integers;
- no floating point values;
- missing and `null` remain distinct; and
- no insignificant whitespace.

The identity is:

```text
sha256(domain-prefix + NUL + canonical-identity-bytes)
```

The schema's identity annotation lists the domain and included fields for each
identity-bearing definition. Human summaries, text rendering, timestamps,
logging values, display-only ordering, and `next_operations` are excluded.
Raw representation digests hash exact source bytes and do not use model-string
normalization.

## State Contract

`query` does not create mutable navigation state. Its handles bind the same
snapshot and can be used only with that snapshot.

`prepare` reaches either:

- `pending`, when at least one required obligation or question remains; or
- `complete`, when all completion invariants already hold.

`resolve` accepts one typed submission against an exact packet. It returns a new
packet when work remains or a completed report at the fixed point. Packets bound
to changed inputs are stale. Unchanged decisions may be imported into a new
packet only through exact dependency-fingerprint equality.

`CompletedAnalysisReport` is not an approval of policy meaning and cannot
authorize mutation or application.

`next_operations` is a schema-governed, derived projection of valid state
transitions. It is optional guidance and excluded from identity.

## Graph Selection

The accepted graph group mapping is owned by the
[architecture decision](../../../docs/decisions/standards-engine-navigation-analysis.md#graph-composition).
The schema carries the same group IDs as a mechanically checkable projection.
The `semantic` and `standards-dependencies` groups are intentionally not A1
impact-selection groups.

## Validation

Run:

```text
python3 tools/standards_engine/contracts/validate_contracts.py
```

The validator uses only the Python standard library. It:

- rejects unsupported keywords in the maintained JSON Schema subset;
- resolves local `$ref` values;
- validates every example against its named definition;
- verifies discriminated unions select exactly one variant;
- checks that identity annotations name real fields and exclude derived fields;
- verifies canonical identity fixtures; and
- checks that public operation and state-machine references resolve.

The validator is contract conformance tooling, not an engine runtime or a
parallel schema authority.
