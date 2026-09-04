# Milestone 7 Routing And Candidate Completeness

## Exact Routing

The `s1-routing` decision fixture now distinguishes material planning scope from
a bounded local migration mechanic. Its reviewed route projection names exact
direct canonical module IDs for every resolved case and `unresolved` for cases
whose authority or workload facts are missing.

The downstream `metadata_route` adapter:

1. reads the exact decision and expectation case sets;
2. maps selected decision outputs to reviewed canonical module IDs;
3. resolves the current canonical module corpus;
4. derives transitive `standards-requires` closure through the neutral graph
   engine; and
5. compares exact direct and closure results with the reviewed fixture.

The adapter owns no graph storage, edge declaration, inferred route, or fallback
selection. The neutral graph remains upstream. The existing six-document S1
metadata check remains bounded S1 evidence; verifier-change routes now use the
complete canonical corpus independently.

## Terminal Candidate Completeness

Migration-only modules declare one structural top-level
`MIGRATION_TERMINAL_TRIGGER`. Migration-only check modules additionally declare
their exposed check kinds. The temporary `migration_python_dispositions` adapter
parses those declarations with Python AST, derives module IDs and paths from the
contained package location, and compares the resulting module/check-kind set
exactly with terminal disposition rows.

This separates authority cleanly:

- module-local declarations own candidate classification;
- source location derives identity and path;
- the disposition table owns terminal decisions and rationale; and
- the adapter owns exact comparison only.

No central candidate list, filename convention, import heuristic, link scan, or
disposition-derived candidate is used. The adapter, registration, tests, and
dispositions are themselves scheduled for deletion at accepted zero-Bash
closure.

## Verification

- 22 focused route, migration-candidate, and package-contract tests passed.
- Deleting a module disposition and deleting a check-kind disposition each
  produced `ASSERT.MIGRATION_PYTHON_DISPOSITION`.
- Direct-module, closure, unresolved-selection, and case-coverage mutations
  produced their exact routing diagnostics.
- `s1-routing` passed 13 checks.
- `checker-migration-packages` passed 3 checks.
- All 383 verifier tests passed.
- All 35 neutral graph tests passed.
- All 215 registered declarative suites passed.
- Generated inventory, graph, and numeric-retirement freshness passed with 56
  retained Bash checkers, 60 nodes, 401 edges, and 60 components.
- `git diff --check` passed.

The complete mixed checkpoint remains the Milestone 9 recovery acceptance gate;
it is not repeated at this intermediate shared-contract milestone.
