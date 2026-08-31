# M6-I75 Decision Traceability Admission

## Decision

Admit one `shared-contract` package at train order 190 to replace both
`evaluation/standards-effectiveness/verify-decision-traceability.sh` and
`templates/check-decision-traceability.sh` with one standard-library Python
package, a standalone-copyable Python checker, and a package-owned Python
contract verifier.

Fresh post-M6-I74 evidence reports one caller-free verifier: the 140-line
decision-traceability fixture checker. Its sole executable dependency is the
349-line distributed Bash template. Migrating only the verifier would retain
the final external Bash helper; retiring the helper without an executable
replacement would remove adopted-repository functionality. The two paths are
therefore one semantic and executable closure.

## Preserved Contract

The package preserves:

- explicit `staged` and `range` modes with no mode, branch, adjacent-revision,
  or map fallback;
- index-only changed paths and map/artifact content for staged mode;
- explicit three-dot base/head changes and commit-owned map/artifact content
  for range mode;
- prior/current map union so removing a row cannot hide its trigger;
- exact paths or slash-terminated prefix triggers;
- strict map header, row width, repository-relative paths, boundary IDs, and
  `boundary-readme`, `contract-readme`, `adr`, or `runbook` profiles;
- exact required headings and ADR affected-boundary identity;
- artifact-to-trigger identity, excluding unrelated ADRs and unstaged
  artifacts; and
- every isolated-Git positive and negative scenario in the current verifier.

## Python Ownership Boundary

One new `tools/decision_traceability` package owns:

- a standalone standard-library checker entrypoint that can be copied into an
  adopting repository without this repository on `PYTHONPATH`;
- a public import contract for focused tests;
- a fixed Python verification entrypoint that recreates the reviewed isolated
  Git scenarios; and
- a strict package manifest registering both safe-path smoke operations.

The existing registered `python_package_contract` assertion executes both
entrypoints through reviewed fixed contracts. The existing
`documentation-traceability-policy` suite continues to own policy decisions,
workflow text, exact dispositions, recipe projection, and former-source
exclusion, with its executable examples changed atomically from `.sh` to
`.py`. The template hook and non-normative recipe point to the Python checker.

No general command check, suite-configured action, subprocess callback,
embedded shell, Bash wrapper, duplicated implementation, compatibility alias,
implicit mode, inferred map, alternate artifact, waiver, or fallback is
admitted.

## Acceptance Evidence

Acceptance requires public-API and CLI tests; exact isolated-Git parity for
missing mode, index isolation, mapped artifact, prior/current map union,
explicit range revisions, unrelated ADR rejection, path/profile/header
validation, and successful staged/range cases; package-contract safe-path
execution; documentation-suite mutation parity; exact edge transfer; generated
freshness; numeric lifecycle; final dependency-local coverage compilation; all
Verifier, repository-Git, and graph-engine tests; all registered suites; the
complete mixed checkpoint; plan validation; removal of both Bash paths; and
staged write-set review.

The final exact write set and coverage renewal are frozen after the Python
package and governed documentation projections compile together.

## Acceptance

Accepted at train order 190. The package exposes one public standard-library
implementation and two fixed repository entrypoints: CLI help and the complete
isolated-Git contract. The former fixture verifier and distributed Bash helper
are deleted; the template hook and recipe invoke the standalone Python copy.

The contract verifier preserves missing-mode rejection, staged map and artifact
isolation, successful staged enforcement, explicit range revisions independent
of unstaged state, unrelated ADR rejection, removed-row coverage, and invalid
header/profile outcomes. The seven-check documentation suite additionally
owns the hook, recipe, former-source, and legacy-default projections. Three
disposable mutations prove those new projections reject regression.

Two exact native-engine edge dispositions transfer helper execution to the
existing package-contract assertion. Fresh generated evidence reports 50 Bash
checkers, 53 nodes, 373 edges, and 53 components. Package smoke, focused tests,
numeric lifecycle, exact 24/24 coverage renewal, 51/51 final coverage, all
verifier and graph tests, all 228 suites, plan validation, and the complete
50-entrypoint mixed checkpoint pass. No Bash bridge, compatibility alias,
copied implementation, inferred input, waiver, or fallback remains.
