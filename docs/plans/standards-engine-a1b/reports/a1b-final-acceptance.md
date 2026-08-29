# Standards Engine A1b Final Acceptance

**Status:** `Accepted`

**Implementation commit:** `84412f22fa9fe082f089eaa347c30c23f185ffee`

**Implementation tree:** `8e0f96a61fcea2398418b17d16a061c20f7463f5`

**Implementation predecessor:** `e955c39e46397babf74f4fc7407606fe17a223ef`

**Reviewed:** `2026-08-29`

## Review Boundary

Independent content-bound Standards and Specification review accepted the
identified implementation commit and tree with zero findings on both axes. The
review covered the material A1b implementation content; this report records
that result and does not alter the reviewed implementation semantics.

The review independently reproduced the corrected governed-source behavior for:

- one- and two-armed conditional deletion;
- `while`, `for`, and `try` branch-exit deletion;
- conditional `sys` provenance used from a nested scope;
- benign augmented assignment;
- dynamic `eval` and import capability on an augmented-assignment right-hand
  side; and
- class, function, and comprehension sibling-scope behavior.

The correction remains one bounded lexical abstraction: supported branch
visitors join definite binding and possible capability provenance. It does not
evaluate conditions, construct a general control-flow graph, or interpret
Python.

## Objective Closure

The accepted boundary satisfies A1B-A1 through A1B-A11. In particular:

- the selected Draft 2020-12 dependency remains the sole schema validator;
- generated request and result models cover the complete admitted public
  closure;
- JSON Schema, applicability, identity, ordering, and deduplication semantics
  remain separately owned;
- immutable authority values reconstruct through exact persisted references in
  a cold process;
- operation closures contain qualified roots and derive transitive
  dependencies through owner-declared references;
- all four public operations use generated v11 values;
- the exact dependency, license, notice, and required-real oracle evidence
  remains unchanged and accepted;
- governed production imports and entrypoints satisfy the closed package
  contract;
- superseded A1 implementations and fallbacks are unreachable;
- selected impact consumers, dispositions, coverage subjects, and valid
  certificates reconcile exactly; and
- all focused and broad verification gates pass without mutable catalog-count
  or hardcoded content-hash assertions.

## Verification

| Evidence | Accepted result |
| --- | --- |
| Corrected governed-source and Git-reachability matrix | 45 of 45 tests passed on each exact locked CPython 3.11 and 3.12 environment |
| Broad Python package verification | 679 tests passed, with required-real evidence executed separately |
| Standards Analysis | 66 tests passed |
| Standards Engine | 36 tests passed |
| Standards Verifier | 433 tests passed |
| Declarative verification | 226 of 226 registered suites passed |
| Retained migration verification | All 53 retained Bash migration checkers passed without extension |
| Generated and repository hygiene | Generated freshness, Ruff, plan validation, and diff hygiene passed |

The independent review also reran the A1b public cutover evidence, including
the required-real dependency and interruption boundaries. No blocked consumer,
fallback, parallel authority, external consumer, retained A1 state, mutable
count oracle, or hardcoded generated identity remains.

## Disposition

The implementation commit and tree above are accepted as the completed A1b
boundary. Milestones 0 through 4 and the A1b ADR are accepted. A2 remains
inactive and requires its own review and admission; this acceptance grants no
A2 implementation authority.
