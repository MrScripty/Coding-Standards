# Milestone 3 Unmapped Normative Obligations

## Result

The accepted and proposed canonical corpora can no longer omit changed
normative authority merely because it lacks a policy-impact edge or a declared
policy-unit change descriptor.

`standards_metadata.project_unmapped_module` uses the canonical Markdown
heading parser to remove every exact active policy-unit scope from a module and
digest the remaining bytes. Nested or otherwise overlapping active policy-unit
locators are rejected. `standards_analysis` compares the accepted and proposed
projections and separately compares policy-unit authority not claimed by the
classified change set.

One `unmapped-normative-change` obligation is generated per affected canonical
module. It has whole-artifact review scope, remains required, permits only an
impact disposition, and carries a content-addressed fingerprint over the exact
accepted and proposed unmapped representations, module locators, unclaimed
policy-unit state, and analysis decision contract.

## Boundaries

- A correctly declared change wholly inside one policy-unit scope does not
  create unmapped work.
- A changed normative scope outside policy units creates the obligation.
- A changed policy unit omitted from change descriptors creates the
  obligation even when the module's unmapped representation is unchanged.
- Added or removed normative modules create the obligation.
- Canonical `reference` modules are explicitly non-normative and are excluded.
- The detector does not judge prose meaning, infer graph edges, search copied
  policy strings, or use line numbers as authority.

## Verification

- Standards metadata: 17 tests passed.
- Standards analysis: 42 tests passed.
- Standards Engine: 15 tests passed.
- Standards verifier: 380 tests passed.
- Public contract validator: 29 examples, 7 identity fixtures, 4 operation
  envelopes, and 109 definitions passed.
- Exact obligation projection, mapped-change exclusion, omitted-descriptor,
  added-module, reference-only, locator-overlap, and deterministic scope tests
  passed.
- Declarative verification: 218 of 218 suites passed.
- Complete mixed checkpoint: generated evidence, 218 declarative suites, and
  all 53 retained Bash checkers passed.
- Plan structure and `git diff --check` passed.
