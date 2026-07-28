# Module Metadata Schema

## Required Fields

| Field | Constraint |
| --- | --- |
| `ID` | Unique lowercase dot-separated identifier. |
| `Role` | `core`, `router`, `workflow`, `profile`, `topic`, or `reference`. |
| `Level` | `MUST`, `SHOULD`, `PROFILE`, or `REFERENCE`. |
| `Applies when` | Observable inclusion conditions. |
| `Does not apply when` | Common observable exclusions or `none`. |
| `Requires` | Comma-separated module IDs or `none`. |
| `Specializes` | Comma-separated module IDs/rule IDs or `none`. |
| `Verification` | Evidence that demonstrates module compliance. |
| `Canonical owner` | Repository-relative path of the declaring module. |

## Invariants

- All fields occur exactly once.
- `core` uses `MUST`; `reference` uses `REFERENCE`; profiles use `PROFILE`.
- A module cannot require or specialize itself.
- Every dependency ID resolves to one canonical module.
- Dependency relationships are acyclic.
- Only profiles may use `Specializes`.
- The canonical owner equals the declaring file path.
- Inclusion and exclusion conditions cannot both be `none`.
- Metadata does not contain implementation recipes or project-local policy.

## Validation Boundary

Automated validation checks field presence, enum values, ID uniqueness,
owner/path equality, resolvable dependencies, self-dependencies, and cycles.
Human review owns whether applicability, exclusions, and verification are
semantically sufficient.
