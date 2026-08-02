# Milestone 7 Row 20 Rust API Decomposition

## Owner Contract

`profiles/languages/rust/api.md` is a narrow language specialization. It
applies when a Rust change selects or changes public or boundary-facing type,
conversion, visibility, result, panic, trait, parameter, Cargo-feature, or
Rustdoc mechanisms. It does not own domain invariants, architectural
responsibility, recovery policy, dependency selection, compatibility,
documentation triggers, or consumer publication promises.

The owner requires `core`, `topic.contracts`, `topic.architecture`,
`topic.resilience`, `topic.dependencies`, `workflow.documentation`,
`profile.application.library`, and `profile.language.rust`. Generic owners
select the contract first; this profile selects a supported Rust expression of
that accepted contract. It cannot weaken, replace, or silently complete missing
generic decisions.

Contradictory contract and mechanism facts are `invalid`; an accepted contract
with no supported Rust expression is `unsupported`; missing contract,
ownership, consumer, toolchain, or evidence facts are `unavailable`.

## Exact Dispositions

`STD-0706` is an index. `STD-0713` and `STD-0714` are direct Rust API
refinements. `STD-0707` through `STD-0712`, `STD-0715`, and `STD-0716`
are splits: generic authority remains with its canonical owner while only Rust
mechanisms enter the API profile.

No migrated section may preserve severity heuristics, type-level complexity
thresholds, parse-once slogans, crate-name or tree conventions, universal
`Result`/`Option`/panic tables, `thiserror`/`anyhow` defaults, blanket
`unwrap` exceptions, derive lists, parameter-wrapper defaults, feature
baselines, Cargo command lists, or documentation checklists.

## Ordered Children

1. `20.1`: create the useful owner with `STD-0706`, `STD-0713`, and
   `STD-0714`; establish routing, typed outcomes, public trait, and parameter
   mechanism decisions.
2. `20.2`: split `STD-0707` and `STD-0708` into generic invariant and
   boundary authority plus Rust type and conversion mechanisms.
3. `20.3`: split `STD-0709` and `STD-0710` into Architecture authority
   plus Rust crate, module, visibility, and conditional-compilation mechanisms.
4. `20.4`: split `STD-0711` and `STD-0712` into generic failure authority
   plus Rust `Result`, `Option`, panic, `unwrap`, and `expect` mechanisms.
5. `20.5`: split `STD-0715` into dependency and public-contract authority
   plus Cargo feature expression.
6. `20.6`: split `STD-0716` into Documentation authority plus Rustdoc
   expression, then close the legacy source as an index.

Every child has an exact bounded write set, focused positive and negative
fixtures, canonical-owner checks, no legacy fallback, plan and ledger updates,
and one atomic commit. Shared routing, metadata, dispositions, legacy source,
and plan files remain serial integration-owner work.

## Re-plan Triggers

Stop if the profile must select a generic contract, creates a dependency cycle,
duplicates another Rust profile, requires a compatibility shim, cannot provide
a useful first child, or an identifier cannot receive exactly one disposition
without competing normative authority.
