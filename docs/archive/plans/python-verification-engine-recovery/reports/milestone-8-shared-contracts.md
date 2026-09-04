# Milestone 8 Shared Contract Acceptance

## Result

Milestone 8 is accepted. Projection syntax has one parser and one reader,
`EngineError` derives process status only from the diagnostic outcome, and the
source-index suite derives its bounded membership from existing corpus facts.

## Architecture Applicability

Architecture is not selected for the final design. The change consolidates
parsing and status derivation inside existing verifier owners and composes
existing `table` membership and predicate contracts. It does not introduce a
new module boundary, dependency direction, graph capability, or domain owner.

The final design deliberately does not add nested member sources or a new
membership-cardinality mode. Existing `members` retains its exact meaning: each
declared identity resolves to exactly one canonical row.

## Projection And Diagnostic Contracts

- `_parse_projection_contract` is the sole parser for projected table columns,
  order, predicates, split configuration, and expected rows where required.
- `parse_projected_table_source` layers path and header requirements on that
  parsed representation.
- `read_projected_table_rows` owns the repeated strict read-and-project step for
  projected-source consumers.
- `EngineError` accepts one `Diagnostic`; its `exit_code` is derived from the
  diagnostic outcome. No numeric override or contradiction path remains.

## Source Membership

The eight source-index members are not stored in a new fixture or repeated in
suite predicates. They are derived from the existing corpus rows where
`kind=standard` and `normative=derived`.

That provider is consumed by:

- the closure-manifest table member scope;
- the corpus-membership table member scope; and
- the projected Markdown source for source-link validation.

Checks whose complete 27-row or 916-identity domains are valid now evaluate
those complete domains. In particular, identifier membership compares all 916
`(source, id)` pairs between the owner map and disposition table.

During implementation, applying exact-one member selection to a many-row
relation produced duplicate-canonical-row diagnostics. Adding a cardinality
mode was rejected because the complete relation already provides a stronger
and simpler invariant. A standalone eight-row member fixture was also rejected
because it would copy membership already derivable from canonical corpus facts.

## Verification

- Focused projection and Markdown tests: 126 passed.
- Source-index closure suite: 43 checks passed.
- All verifier unit tests: 386 passed.
- Neutral graph tests: 35 passed.
- All declarative suites: 215 passed.
- Generated inventory, graph, and numeric-retirement freshness passed for 56
  Bash verifiers, 60 graph nodes, 401 edges, and 60 components.

The complete mixed checkpoint is reserved for Milestone 9, where it is part of
the required three-sample current performance workload.
