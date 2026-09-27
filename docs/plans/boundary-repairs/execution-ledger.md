# Execution ledger

## 2026-09-27 — B1 admission

- Verified upstream `af6b829a` and exact source artifact SHA-256
  `55ced93355da26d20d3d5f8d31821916bdcbef1196b46339c2b761652f2e7e4d`.
- Isolated local branch `boundary-repairs`, target main; source initially clean.
- Routed explicit task facts: 28 selected modules, zero unresolved questions.
- Preserved first routing request error (used `set` instead of declared `enum-set`);
  corrected the caller, not the production schema.
- Supported Python 3.12 installation failed on DNS access. Existing dependency lock
  is unchanged; local runtime qualification is recorded separately.

## 2026-09-27 — Shared digest constraint correction

- The F07 conformance corpus found an additional same-family inconsistency: the
  pattern `^sha256:[0-9a-f]{64}$` admits a trailing newline through the selected
  validator, but domain fullmatch rejects it. Preserve the failing baseline log.
- Tighten the canonical Digest with `maxLength: 71`, admit that existing validator
  keyword in the compiler, and test independent character-count semantics plus
  generated preservation. Do not alter regex meaning or create a new validator.
- Advance only the existing interface edition to 44. Native operation shapes and
  persisted formats are unchanged; regenerate declarations through their owner.
- This replaces the initial no-declaration-change assumption inside F07's bounded
  population. The composed design retains the same owners and introduces no new
  mechanism. Add the directly affected compiler/declaration/test/version consumers
  to the exact write set.

## 2026-09-27 — Implementation and verification observations

- Initial counterexamples for F04–F07 failed before the repairs; 20 first focused
  methods passed afterward. Broader numeric tests then included nullable/implicit
  containers, boolean item schemas and simultaneous reference/union clauses.
  These reuse validated structure and the existing validator; no replacement
  constraint evaluator was introduced. The current canonical corpus contains no
  simultaneous ref/oneOf node, but the admitted profile can describe one.
- Real integral semantic revisions reached proposals through inline and shared
  evidence and cold MCP stdio. The first readback expectation included the original
  module's extra separator newline; the fixture was corrected to the exact rendered
  heading/body request. Rendering and domain acceptance were not changed.
- All eleven supporting-package selections passed with two environment-dependent
  skips. The permission case separately passed as an unprivileged user. The six
  new CI selections also passed as the exact CI commands.
- Complete Engine selection: 523 tests, 522 passes, one stale authored example
  interface-edition assertion. Both current discovery examples were updated to
  edition 44 without changing the assertion. Final focused reruns are recorded
  separately rather than relabeling that original failure.
- Actual baseline-produced snapshots, Analysis and readiness reopened under the
  candidate. An early retention checker expected a top-level code rather than
  the focused workflow's nested rejection; its assertion was corrected, not the
  existing failure projection. Altered evidence retained the exact digest-mismatch
  rejection, restored bytes reproduced readiness, and main did not advance.
- Final material self-review checked authority separation, declaration/operation
  scope, no-effects negatives and unchanged store/handle formats. Independent
  external review and the locked environment remain named integration gates.

## 2026-09-27 — Final source and artifact checks

- Final integrated Engine rerun: 94 passed. Contracts: 80 passed and the unchanged
  supported-environment skip. All 523 current Engine IDs have observed passing
  evidence, with the initial stale-example failure and its correction retained.
- Complete structural checkpoint: 73 suites and 121 checks passed. Final generated
  freshness, syntax, whitespace, source preservation and fresh-base reconstruction
  are recorded in the delivery evidence. The integration artifact does not advance
  a remote ref or the production standards.
- B1 remains Verifying with partial acceptance: local source/artifact claims A1–A5
  are complete; supported locked-runtime CI and independent material review (A6)
  remain explicitly pending.
