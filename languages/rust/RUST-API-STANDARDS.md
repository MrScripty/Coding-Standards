# Rust API Standards

Canonical Rust API mechanisms are migrating to the
[Rust API profile](../../profiles/languages/rust/api.md). Generic contracts
remain with their routed owners. This legacy file retains authority only for
sections not yet moved.

## Correct-By-Construction Policy

Canonical invariant authority belongs to
[Contracts](../../topics/contracts.md#invariant-contracts). Select a Rust
proof-bearing representation through the
[Rust API profile](../../profiles/languages/rust/api.md#validated-type-and-conversion-mechanisms).
This legacy route defines no bug-cost, visibility, state-count, security-label,
type-level-complexity, test, or assertion default.

## Parse, Do Not Re-Validate

Canonical runtime proof and proof lifetime belong to
[Contracts](../../topics/contracts.md#validation-proof-lifetime); untrusted
input authorization belongs to [Security](../../topics/security.md#input-validation-authority).
Select Rust validated types, constructors, and fallible conversions through the
[Rust API profile](../../profiles/languages/rust/api.md#validated-type-and-conversion-mechanisms).
This legacy route defines no parse-once, no-revalidation, `TryFrom`, `FromStr`,
newtype, enum, boolean replacement, private-constructor, primitive-wrapper, or
error-crate default.

## Crate Roles

Canonical responsibility, dependency-direction, and composition authority
belongs to [Architecture](../../topics/architecture.md). Select Rust crate and
module expression through the
[Rust API profile](../../profiles/languages/rust/api.md#crate-and-module-boundary-mechanisms).
This legacy route defines no crate-role name, workspace-member, core, contract,
adapter, infrastructure, binding, application, server, CLI, `xtask`, utility,
or dependency-direction default.

## Module Layout

Canonical module, public-surface, and placement authority belongs to
[Architecture](../../topics/architecture.md). Select Rust visibility,
re-export, module, crate, and conditional-compilation expression through the
[Rust API profile](../../profiles/languages/rust/api.md#crate-and-module-boundary-mechanisms).
This legacy route defines no source tree, file name, crate-root re-export,
`pub(crate)`, error-module, feature-module, platform-module, integration-test,
benchmark, example, thin-module, or inline-`cfg` default.

## Result, Option, Panic

Canonical expected-absence, invariant, validation, and impossible-state
semantics belong to [Contracts](../../topics/contracts.md); operational failure,
recovery, retry, degradation, and availability belong to
[Resilience](../../topics/resilience.md). Select Rust failure expression through
the [Rust API profile](../../profiles/languages/rust/api.md#failure-expression-mechanisms).
This legacy route defines no situation table, `Result`, `Option`, panic,
assertion, `unreachable!`, error-enum, `thiserror`, `anyhow`, string-error, or
context default.

## `unwrap` And `expect`

Canonical proof, invariant, impossible-state, and operational-failure authority
belongs to [Contracts](../../topics/contracts.md) and
[Resilience](../../topics/resilience.md). Select Rust assertion, panic,
`unreachable!`, `unwrap`, and `expect` expression through the
[Rust API profile](../../profiles/languages/rust/api.md#failure-expression-mechanisms).
This legacy route defines no production-path prohibition, test, example,
prototype, guarded-invariant, compile-time, infallibility, message, or `expect`
preference exception.

## Public Contract Traits

Select public contract trait mechanisms through the canonical
[Rust API profile](../../profiles/languages/rust/api.md#public-contract-trait-mechanisms).
This legacy route defines no derive, display, result-use, extension, dispatch,
associated-type, generic, sealing, or trait-object default.

## Parameter Ergonomics

Select Rust parameter and ownership mechanisms through the canonical
[Rust API profile](../../profiles/languages/rust/api.md#parameter-and-ownership-mechanisms).
This legacy route defines no borrowing, ownership, conversion-wrapper, `Cow`,
allocation, cloning, primitive, or signature default.

## Feature Contracts

Canonical feature selection and footprint belong to
[Dependencies](../../topics/dependencies.md#features-and-footprint);
consumer-visible compatibility belongs to
[Contracts](../../topics/contracts.md#public-and-independently-deployed-evolution);
real consumer configurations belong to the
[Library profile](../../profiles/applications/library.md#dependencies);
durable feature artifacts belong to
[Documentation](../../workflows/documentation.md#contract-documentation); and
evidence selection belongs to
[Verification](../../workflows/verification.md#selecting-claims). Select Cargo
expression through the
[Rust API profile](../../profiles/languages/rust/api.md#cargo-feature-expression-mechanisms).
This legacy route defines no minimal-default, `dep:`, optionality-category,
mutual-exclusion, `compile_error!`, README, crate-doc, Cargo-command,
all-features, or `cargo hack` default.

## Documentation

Rust crates should document contracts where the compiler cannot fully enforce
intent.

Required documentation:

- crate-level `//!` docs for public library crates
- `# Errors` sections on public fallible functions where behavior is not obvious
- `# Panics` sections on public functions that can panic
- `# Safety` sections on every `unsafe fn` and unsafe-owning module
- feature-flag documentation in README or crate docs
- examples for public APIs that are intended for external users

Do not document obvious implementation mechanics. Document invariants,
contracts, safety obligations, compatibility expectations, and why a design
exists.
