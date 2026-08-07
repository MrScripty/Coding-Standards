# Checker Structure Inventory

## Authority And Limits

`evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`
is generated structural evidence. It records every current `verify-*.sh`
entrypoint, line count, exact inbound references by executable, contract, and
documentation class, named verifier/helper dependencies, and use of `sed`,
AWK, `rg`, and the legacy decision-table helper.

The generator does not infer canonical owner, semantic risk, migration
disposition, or package cohesion. Those are review decisions owned by this
plan. A documentation reference does not create an execution dependency, while
an executable or frozen contract reference must be migrated or updated before
the named checker can be deleted.

## Baseline Results

- 274 current Bash verifier entrypoints;
- 77 with no named verifier or helper dependency;
- 47 using `sed`;
- 249 using AWK;
- 264 using `rg`; and
- 13 using the legacy decision-table helper.

The exact per-checker values are kept in the generated TSV rather than copied
into this report. `generate_inventory.py --check` is blocking in the generic
launcher, so checker additions, removals, reference changes, dependency changes,
or measured mechanism changes require explicit regeneration and review.

## First Reviewed Package

Package `M2-P1` contains these eight Rust Tooling leaf checkers:

| Suite | Replaced checker | Decision fixture | Exact ID |
| --- | --- | --- | --- |
| `rust-tooling-adapter-inventory` | `verify-rust-tooling-adapter-inventory.sh` | `tooling-adapter-inventory-decisions.tsv` | `STD-0840` |
| `rust-tooling-baseline-commands` | `verify-rust-tooling-baseline-commands.sh` | `tooling-baseline-command-decisions.tsv` | `STD-0832` |
| `rust-tooling-build-script` | `verify-rust-tooling-build-script.sh` | `tooling-build-script-decisions.tsv` | `STD-0841` |
| `rust-tooling-compile-fail` | `verify-rust-tooling-compile-fail.sh` | `tooling-compile-fail-decisions.tsv` | `STD-0837` |
| `rust-tooling-feature-matrix` | `verify-rust-tooling-feature-matrix.sh` | `tooling-feature-matrix-decisions.tsv` | `STD-0836` |
| `rust-tooling-property-test` | `verify-rust-tooling-property-test.sh` | `tooling-property-test-decisions.tsv` | `STD-0838` |
| `rust-tooling-test-runner` | `verify-rust-tooling-test-runner.sh` | `tooling-test-runner-decisions.tsv` | `STD-0835` |
| `rust-tooling-workspace-lints` | `verify-rust-tooling-workspace-lints.sh` | `tooling-workspace-lint-decisions.tsv` | `STD-0833` |

### Cohesion Decision

- Canonical owner: `profile.language.rust.tooling`, with selected generic owner
  prerequisites preserved in each suite's fixture and required text.
- Observable package outcome: selected Rust tooling mechanisms remain adapters
  to accepted owner decisions and cannot create generic policy or named-tool,
  layout, command, harness, feature, lint, or build defaults.
- Risk: `consolidation`; accepted semantics and fixtures do not change.
- Dependencies: none of the eight scripts invokes a verifier/helper, and no
  executable or frozen contract references its path before this report.
- Assertion family: ordered decision outcomes, required canonical profile and
  non-normative reference text, prohibited former-source default, and one exact
  disposition row per suite.
- Write owner: one package author may edit only the eight suite TOMLs, registry
  rows, eight deleted scripts, regenerated structural inventory, and child plan
  records. Engine source and shared historical manifests remain read-only.
- Gate: direct execution of all eight suite IDs, generic launcher, removed-path
  and stale-inventory checks, plan/diff integrity, and one complete mixed suite.

The similarly short `verify-rust-release-automation-adapter.sh` is excluded: it
belongs to the Rust Release owner and has a two-disposition Release/reference
contract. Similar shell shape does not authorize cross-owner batching.

## Next Classification Work

After `M2-P1`, classification proceeds by canonical owner and dependency shape.
No script is scheduled for deletion solely because it is short, unreferenced,
or mechanically similar. Executable and frozen-contract references are resolved
in the accepting package; historical checker-identity contracts remain deferred
to Milestone 3's shared migration-contract replacement.
