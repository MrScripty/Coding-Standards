# Milestone 7 Row 21 Rust Dependency Decomposition

## Owner Contract

`profiles/languages/rust/dependencies.md` is a narrow Rust and Cargo mechanism
specialization. It applies when an accepted dependency contract must be
expressed or inspected through Cargo manifests, workspace inheritance,
features, resolution metadata, dependency graphs, audit adapters, or build-cost
measurement. It does not own dependency selection, security or licensing
findings, performance claims, verification evidence, tooling schedules, public
feature contracts, or command recipes.

The owner requires `core`, `workflow.verification`, `profile.language.rust`, and
`topic.dependencies`. Other generic owners route conditionally. Contradictory
contract and mechanism facts are `invalid`; a valid contract with no supported
Cargo expression is `unsupported`; missing owner, resolver, toolchain,
consumer, or evidence facts are `unavailable`. No Cargo convention, installed
tool, incumbent manifest, successful command, or smallest diff is a fallback.

## Exact Dispositions

`STD-0731` is an index. Six section owners are splits into generic authority
and narrow Rust mechanisms. Fourteen command, manifest, and shell examples move
to `reference/recipes/rust-dependencies.md`, which is non-normative and cannot
select tools, schedules, thresholds, or policy.

## Ordered Children

1. `21.1`: create the useful owner and parent route with `STD-0731`.
2. `21.2`: split `STD-0732`; move `STD-0733` and `STD-0734` to reference.
3. `21.3`: split `STD-0735`; move `STD-0736` and `STD-0737` to reference.
4. `21.4`: split `STD-0738`; move `STD-0739` and `STD-0740` to reference.
5. `21.5`: split `STD-0741`; move `STD-0742` through `STD-0746` to reference.
6. `21.6`: split `STD-0747`; move `STD-0748` to reference.
7. `21.7`: split `STD-0749`; move `STD-0750` and `STD-0751` to reference,
   then close the legacy source.

Each child has exact dispositions, focused positive and negative fixtures, no
legacy fallback, plan and ledger updates, and one atomic commit. The profile,
reference recipe, dispositions, legacy source, plan, and routing remain serial
integration-owner files.

## Re-plan Triggers

Stop if the Rust profile must select generic policy, an example must remain
normative, the reference recipe becomes a tool-selection authority, a section
cannot receive one exact disposition, dependencies create a cycle, or legacy
closure would retain policy.
