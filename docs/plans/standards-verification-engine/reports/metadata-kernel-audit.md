# M6-K1 Metadata Kernel Audit

## Question

Can the typed metadata primitive preserve the canonical metadata contract
without copying the Bash helper's incomplete specialization behavior or
inventing rule-level authority?

## Evidence

- The repository has 19 live non-empty `Specializes` declarations. Every target
  is a canonical module ID.
- `check-metadata.sh` resolves `Requires` and `Specializes` only against
  module IDs selected for the invocation.
- The helper checks cycles only through `Requires`.
- `metadata-schema.md` previously described `Specializes` as module IDs or
  rule IDs, while `information-architecture.md` referred to rules named by the
  field.
- Current canonical rules have no stable individual IDs.
- `generated/rule-owner-map.tsv` maps frozen legacy `STD-*` sections to
  proposed migration owners. It cannot own current rule identity or precedence.
- The fixture corpus covers field presence, level, owner, self-dependency,
  unresolved requirement, requirement cycle, and duplicate module ID. It lacks
  specialization-role, specialization-resolution, list-grammar, specialization
  cycle, and combined-cycle cases.
- `verify-metadata-fixtures.sh` is the fixture checker. After it, 52 semantic
  checkers still execute `check-metadata.sh`.

## Decision

Use module-level specialization for the current schema. A profile may refine
mechanisms owned by named modules, but generic obligations remain authoritative.
Rule-level targets require a future version with namespaced IDs, canonical rule
ownership, routing, and graph semantics.

Treat `Requires` and `Specializes` as distinct typed relations and reject
cycles in either relation or their combined graph. Resolve every target exactly;
return typed diagnostics for malformed, unavailable, or unsupported inputs.

Use field-specific syntax. IDs, enums, owner paths, and relation items are
backticked symbolic tokens. Applicability, exclusion, and verification are
non-empty Markdown prose whose exact content is preserved, including embedded
inline code. The parser does not strip backticks globally or accept unquoted
symbolic values as a compatibility form.

## Proposed First Vertical Slice

After package admission, implement one typed metadata-graph check, focused
tests, missing negative fixtures, and one registered suite. Delete
`verify-metadata-fixtures.sh` in the same accepted package. Keep
`check-metadata.sh` and all 52 semantic consumers unchanged until later
owner-coherent waves.

## Exclusions

No rule registry, namespaced rule syntax, legacy-map lookup, compatibility
parser, helper wrapper, command action, consumer migration, canonical-module
rewrite, lockfile change, or fallback path is admitted.
