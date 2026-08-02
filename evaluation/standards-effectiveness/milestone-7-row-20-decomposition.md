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
4. `20.4`: split `STD-0711` and `STD-0712` across Contracts authority for
   expected absence, invariant violation, and impossible-state semantics;
   Resilience authority for operational failure, recovery, retry, degradation,
   and availability; and Rust `Result`, `Option`, panic, assertion,
   `unreachable!`, `unwrap`, and `expect` mechanisms. Neither generic owner may
   infer the other's contract, and the Rust profile may not select either.
5. `20.5`: split `STD-0715` across Dependencies authority for feature
   selection, optional dependencies, defaults, target variants, and footprint;
   Contracts authority for consumer-visible behavior and compatibility;
   Library authority for real consumer configurations; Documentation authority
   for durable feature-contract documentation; Verification authority for
   claim-matched feature-combination evidence; and Rust API authority only for
   supported Cargo feature and compile-time enforcement mechanisms.
6. `20.6`: split `STD-0716` across Documentation authority for triggers,
   artifacts, placement, and quality; Contracts authority for invariant,
   compatibility, and consumer-contract facts; Resilience authority for
   failure and panic behavior; Dependencies authority for feature-contract
   facts; Rust Unsafe authority for public unsafe contracts and `# Safety`
   obligations; Library authority for external-consumer applicability; and
   Rust API authority only for supported Rustdoc expression. Then close the
   legacy source as an index.

Every child has an exact bounded write set, focused positive and negative
fixtures, canonical-owner checks, no legacy fallback, plan and ledger updates,
and one atomic commit. Shared routing, metadata, dispositions, legacy source,
and plan files remain serial integration-owner work.

## Re-plan Triggers

Stop if the profile must select a generic contract, creates a dependency cycle,
duplicates another Rust profile, requires a compatibility shim, cannot provide
a useful first child, or an identifier cannot receive exactly one disposition
without competing normative authority.

## Child 20.4 Ownership Replan

Lookahead found that “generic failure authority” collapsed two independent
contracts. Contracts owns expected absence, invariant violation, validation,
and impossible-state semantics. Resilience owns operational failure, recovery,
retry, degradation, and availability. Rust API owns only the supported language
expression after every applicable generic contract is accepted.

The child retains its two IDs and one atomic implementation slice because both
legacy sections jointly prescribe the same Rust failure-expression family.
Focused decisions must distinguish expected absence, recoverable operational
failure, invariant violation, and impossible state. Missing or contradictory
generic ownership returns typed diagnostics; no situation table, error crate,
context rule, path exception, or `expect` preference survives as a fallback.

## Child 20.5 Ownership Replan

Lookahead found that “dependency and public-contract authority” omitted three
independent owners. Dependencies selects features, optional dependencies,
default behavior, target variants, and footprint. Contracts owns
consumer-visible behavior and compatibility. Library owns supported real
consumer configurations. Documentation owns documentation triggers and
artifacts. Verification owns claim-matched feature-combination evidence. Rust
API owns only Cargo feature syntax and compile-time enforcement mechanisms.

The child retains `STD-0715` and its ordering because the legacy section is one
mixed feature-contract policy. Focused decisions must reject minimal defaults,
`dep:` syntax, optionality categories, mutual-exclusion rules,
`compile_error!`, README or crate-doc placement, and fixed Cargo command
matrices when their canonical owner has not selected them. Missing or
contradictory facts return typed diagnostics rather than a conventional Cargo
configuration.

## Child 20.6 Ownership Replan

Lookahead found that “Documentation authority plus Rustdoc expression” did not
name the owners of the documented facts. Documentation selects triggers,
artifact type, placement, and quality. Contracts owns invariant, compatibility,
and consumer-contract facts. Resilience owns failure and panic behavior.
Dependencies owns feature-contract facts. Rust Unsafe owns public unsafe
contracts and `# Safety` obligations. Library owns external-consumer
applicability. Rust API owns only Rustdoc syntax and placement within the
already selected Rust artifact.

The child retains `STD-0716`, legacy closure, and ordering. Focused decisions
must reject fixed crate-doc, `# Errors`, `# Panics`, `# Safety`, feature-doc,
README, crate-doc, and example requirements when their canonical owner has not
selected them. Missing or contradictory applicability or content authority
returns typed diagnostics. Closure must leave only canonical routes and no
residual normative checklist.
