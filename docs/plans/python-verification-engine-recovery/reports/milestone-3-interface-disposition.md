# Milestone 3 Interface Disposition

## Source-Index Closure

| Current responsibility | Replacement owner |
| --- | --- |
| Exact ordered headings and inclusive line ceiling | `markdown_structure` |
| Manifest and corpus membership/state | `table` |
| Canonical owner paths exist | `repository_paths` |
| Owner-map and disposition identifier equality | `relation` |
| Markdown targets exist and remain contained | `markdown_links` |
| Every declared destination, including anchors, is linked | `markdown_link_coverage` exact-destination mode |
| Source-specific prohibited prose | `table_text_absence` |
| Shared non-authority and no-fallback prose | `text` |
| Former sources are absent from Router | `table_text_absence` |

The contract and heading fixture files duplicate policy that belongs directly
in the suite. Route and prohibited fixtures are consolidated by concern rather
than retained under a fixed per-source directory topology.

## Acceptance Claims

The custom `kind@environment@mode` serialization is not a canonical workflow
artifact and has no non-test consumer. The accepted invariant is expressed as
a normal decision table:

- claim kind and environment identity must match;
- evidence mode must equal the required mode unless the requirement is
  `either`;
- every required claim must have matching evidence; and
- an unmatched identity, mode, or required-set member is unsatisfied.

Canonical claim kinds, environments, and modes remain owned by
`workflows/verification.md`. The fixture records policy decisions without
creating a second serialized claim language.

## Neutral Capability Decision

Resolved repository paths cannot preserve whether a declared Markdown anchor
was selected. The existing `markdown_link_coverage` check therefore gains one
explicit identity selector: resolved repository path or exact Markdown
destination. Both use the same parser, containment behavior, and table source;
the selector changes only the compared identity. No source-index vocabulary or
policy enters the generic check.

## Accepted Evidence

- Both specialized check kinds, implementations, parser branches, private
  tests, and superseded fixtures are absent.
- The source-index suite passes 43 generic checks and retains mutation coverage
  for ordering, membership, routes, line budgets, prohibited content,
  containment, availability, and no-fallback policy.
- The acceptance suite passes as a generic decision table and distinguishes
  exact identity, execution-mode, and required-set failures without parsing a
  serialized claim language.
- All 348 verifier tests, 35 neutral graph tests, 207 declarative suites, and
  the complete checkpoint with 65 retained Bash checkers pass.
