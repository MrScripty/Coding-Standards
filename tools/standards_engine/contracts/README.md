# Standards Engine A1b Contracts

This directory owns the serialized public shape of the read-only Standards
Engine interface. Runtime policy meaning, identity construction, persistence,
repository loading, and controlled authoring belong to their domain Modules.

## Authority

[`a1-contract.schema.json`](a1-contract.schema.json) is the sole public JSON
shape authority. It uses JSON Schema Draft 2020-12. The selected
`standards_contracts` dependency validates instances and compiles the reachable
public definition closure; this package does not implement JSON Schema
keywords.

[`a1-interface.toml`](a1-interface.toml) owns operation roots, accepted result
families, capabilities, and independent request/result compatibility versions.
It contains no domain identity fields or runtime state machine.

The compiler produces these disposable projections:

- [`../standards_engine/_generated_contract.py`](../standards_engine/_generated_contract.py)
- [`generated/agent-tools.json`](generated/agent-tools.json)

Files under [`examples/`](examples/) are reviewed authored fixtures. Each
example names one reachable schema definition and supplies one value. They do
not define fields, defaults, variants, identity, or runtime semantics.

## Public Operations

| Operation | Input | Success result | Expected rejection |
| --- | --- | --- | --- |
| `query` | `QueryCall` | `NavigationResult` | `RejectedResult` |
| `prepare` | `PrepareCall` | `PendingResult` or `CompleteResult` | `RejectedResult` |
| `resolve` | `ResolveCall` | `PendingResult` or `CompleteResult` | `RejectedResult` |
| `inspect` | `InspectCall` | `InspectionResult` | `RejectedResult` |

Interface schema version 11 uses request contract version 3 and result
projection version 3. Public authority handles use schema version 4. Unsupported
well-formed compatibility keys return `unsupported`; there is no old-version
parser or fallback.

Trusted provider and authorization context is injected by the Engine
composition root. Caller-authored requests cannot grant capabilities or supply
trusted standards-change facts.

## Identity And Authority

The schema governs representation only. `standards_identity` owns exact
identity-v2 framing and codepoint-preserving encoding. Each domain Module owns
its material record, ordering, deduplication, semantic identity, and direct
authority references. Schema annotations, generated classes, builds, and
release versions do not acquire domain authority.

`standards_authority` stores immutable owner-encoded objects and resolves exact
handles. Queries bind an explicit `StandardsAuthorityViewHandle`; analyses bind
base and proposed views. Reads, inspections, and cold reconstruction resolve
captured immutable content and never substitute the live worktree.

An `AnalysisHandle` is the sole A1 analysis identity. Pending and complete
results are deterministic projections of immutable state. Resolution creates
an independent child state; A1 has no mutable head, global supersession, or
temporal packet staleness.

## Verification

From the repository root, run:

```text
PYTHONPATH=. python3 -P tools/standards_engine/contracts/generate_contract.py --check
```

The check compiles the canonical schema and interface through
`standards_contracts`, compares both generated projections byte-for-byte, and
validates every authored example through the same production contract runtime.
Generated freshness is not semantic conformance evidence by itself; the
registered contract suite separately exercises the selected Draft validator,
public behavior, identity equality, and unsupported-profile outcomes.
