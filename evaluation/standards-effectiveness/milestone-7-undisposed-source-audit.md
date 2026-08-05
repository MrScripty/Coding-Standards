# Milestone 7 Undisposed Source Audit

## Scope

This audit compares Markdown heading deletions from frozen baseline
`6b4df85f042898374e9d23d265f4ecd25b0a7ba7` with the stable section inventory
and exact consolidation dispositions. It identifies frozen headings deleted
from their source while their identifier remains undisposed.

The audit covers heading deletion, not semantic content removal beneath a
retained heading. Exact current-heading review distinguishes deleted-and-added
formatting from a genuinely absent frozen section.

## Result

The baseline diff contains 812 deleted heading lines. Nineteen correspond to
currently undisposed identifiers. Two are retained headings rewritten by a
larger file diff and are not source gaps:

| ID | Source | Classification |
| --- | --- | --- |
| `STD-0349` | `DOCUMENTATION-STANDARDS.md` | Retained `Documentation Standards` index heading. |
| `STD-0900` | `templates/README-TEMPLATE.md` | Retained `Purpose` heading. |

Seventeen identifiers are genuinely absent:

| IDs | Source | Removal origin | Scheduled row |
| --- | --- | --- | --- |
| `STD-0088` | `ARCHITECTURE-PATTERNS.md` | Child 37.4 removed the nested Directory README Requirement with the parent tree. | 38 |
| `STD-0899`, `STD-0901`-`STD-0905`, `STD-0907`-`STD-0916` | `templates/README-TEMPLATE.md` | Milestone 6.1 replaced the universal directory template with the conditional boundary template. | 47 |

The row-47 identifiers cover the renamed boundary title; removed contents,
problem, constraints, decision, alternatives, revisit, dependency, example,
testing, and notes sections; and the renamed decision-link, consumer-contract,
and producer-contract sections. `STD-0906` Invariants and `STD-0900` Purpose
remain present.

## Constraints

- Every absent identifier still requires exactly one disposition.
- Frozen identities and immutable baseline evidence cannot be rewritten.
- Removed universal template text cannot be restored as a compatibility path.
- Row 47 cannot be completed before rows 38 through 46 without an approved
  immutable-train replan.
- A temporary audit exception must remain explicit and fail when an
  unrecorded orphan appears; it cannot become a silent fallback.

## Replan Trigger

The approved sequence can close `STD-0088` in row 38, but the audit also proves
sixteen later-row provenance gaps. Continuing requires an explicit decision to
retain row order with bounded row-47 debt, or to replan the immutable train.
Restoring the legacy template is not an admissible option.
