# Module Metadata Schema

## Required Fields

| Field | Constraint |
| --- | --- |
| `ID` | Unique lowercase dot-separated identifier. |
| `Role` | `core`, `router`, `workflow`, `profile`, `topic`, or `reference`. |
| `Level` | `MUST`, `SHOULD`, `PROFILE`, or `REFERENCE`. |
| `Applies when` | Observable inclusion conditions. |
| `Does not apply when` | Common observable exclusions or `none`. |
| `Requires` | Inclusion edges to canonical module IDs or `none`. |
| `Specializes` | Profile-precedence edges to canonical module IDs or `none`. |
| `Verification` | Evidence that demonstrates module compliance. |
| `Canonical owner` | Repository-relative path of the declaring module. |

## Field Grammar

- Symbolic fields (`ID`, `Role`, `Level`, and `Canonical owner`) contain
  exactly one backticked token.
- Relation fields (`Requires` and `Specializes`) contain individually
  backticked module IDs separated by commas and optional surrounding ASCII
  spaces, or exactly one backticked `none` token.
- Empty, duplicate, unquoted, malformed, or mixed-`none` relation items are
  invalid.
- Prose fields (`Applies when`, `Does not apply when`, and `Verification`)
  preserve their complete non-empty Markdown values, including inline code.
- Parsers do not strip backticks globally, infer omitted values, or accept an
  unquoted symbolic compatibility form.

## Invariants

- All fields occur exactly once.
- `core` uses `MUST`; `reference` uses `REFERENCE`; profiles use `PROFILE`.
- A module cannot require or specialize itself.
- Every relation target resolves to exactly one selected canonical module.
- `Requires`, `Specializes`, and their combined relation graph are acyclic.
- Only profiles may use `Specializes`.
- A profile specializes mechanisms owned by the named module; generic
  obligations remain authoritative and are not blanket-overridden.
- The canonical owner equals the declaring file path.
- Inclusion and exclusion conditions cannot both be `none`.
- Metadata does not contain implementation recipes or project-local policy.

## Validation Boundary

Automated validation checks exact field grammar, enum values, ID uniqueness,
owner/path equality, exact relation resolution, profile-only specialization,
self-edges, and relation-specific plus combined cycles. Malformed evidence is
`invalid`; missing required input is `unavailable`. Human review owns whether
applicability, exclusions, specialization mechanisms, and verification are
semantically sufficient.

Rule-level specialization is unsupported by this schema version. It requires a
separately versioned contract with namespaced stable rule IDs, canonical rule
ownership, routing, and graph semantics; legacy migration IDs are not current
rule authority.
