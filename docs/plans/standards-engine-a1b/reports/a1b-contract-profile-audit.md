# A1b Contract Profile Audit

**Recorded:** 2026-08-28

## Scope

This audit covers the canonical A1b v11 public schema, operation interface,
generated Python algebra, generated agent-tool projection, and the runtime
validator Adapter. It does not claim independent certification of the complete
JSON Schema Draft 2020-12 language.

## Authority And Projection

| Artifact | Role | SHA-256 |
| --- | --- | --- |
| `tools/standards_engine/contracts/a1-contract.schema.json` | Authored public shape authority | `bd618af35fc7280805cabe8adaeebfba5e1def0cbf6b3e334e91563f2435bca8` |
| `tools/standards_engine/contracts/a1-interface.toml` | Authored operation/interface authority | `8d4adb47f90f0c8168873d89578b292c728badad7334d5f15c15125279ec6b00` |
| `tools/standards_engine/standards_engine/_generated_contract.py` | Generated Python projection | `073b905463aa41435291d8caec1f1a8e45d5ba8b51936fd82bd58a56360b0e21` |
| `tools/standards_engine/contracts/generated/agent-tools.json` | Generated agent-tool projection | `4f39681a1ae1d47aceebcedcc5d1972aefee5cedced1d07b0ffee342862d3b81` |

The agent-tool digest in the table is not acceptance authority; generated
freshness compares exact bytes. The canonical schema and interface are
byte-identical to the independently admitted planning artifacts:

- `docs/plans/standards-engine-a1b/reports/a1-contract-v11.schema.json`
- `docs/plans/standards-engine-a1b/reports/a1-interface-v11.toml`

## Semantic Boundary

- `standards_contracts` compiles the reachable local-reference closure and
  rejects unsupported projection semantics.
- Runtime instance validation delegates to the selected
  `jsonschema.Draft202012Validator`; the repository has no JSON Schema keyword
  interpreter.
- Generated models enforce the complete reachable request and result algebra
  and then delegate instance semantics to the same compiled contract.
- JSON Schema instance equality, applicability equality, identity encoding,
  and domain ordering remain separate owner contracts.
- The public Engine facade accepts and returns generated v11 values only.
- Unsupported compatibility keys and payload formats return typed unsupported
  outcomes; no prior-version fallback is reachable.

## Evidence

The registered `generated-contract-semantic-conformance` suite proves compiler
closure, generated freshness, validator-backed models, equality-domain
separation, the known historical A1 nonconformance, and positive and negative
projection behavior. The `a1b-public-cutover` suite proves the generated facade
is part of the closed public package boundary.

Focused Contracts tests and generated-contract Engine tests passed at this
boundary. Final complete-checkpoint evidence is recorded separately in
`a1b-cutover-evidence.md`.

## Disposition

The v11 schema and interface remain the authored public authorities. Generated
Python and agent-tool files are disposable exact projections. There is no
second schema-semantic implementation or handwritten public result algebra.
