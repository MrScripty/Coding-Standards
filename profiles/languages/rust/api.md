# Rust API Profile

**Standards metadata**

- ID: `profile.language.rust.api`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A Rust change selects or changes public or boundary-facing type, conversion, visibility, result, panic, trait, parameter, Cargo-feature, or Rustdoc mechanisms.
- Does not apply when: No Rust API mechanism changes, or the task only selects the generic invariant, architecture, failure, dependency, documentation, compatibility, or consumer contract.
- Requires: `core`, `topic.contracts`, `topic.architecture`, `topic.resilience`, `topic.dependencies`, `workflow.documentation`, `profile.application.library`, `profile.language.rust`
- Specializes: `profile.language.rust`
- Verification: Rust API decision fixtures plus affected public API, consumer, compile, and documentation evidence selected by the generic owners.
- Canonical owner: `profiles/languages/rust/api.md`

## API Mechanism Authority

Generic owners select invariants, architecture, failure behavior, dependency
and feature contracts, documentation obligations, compatibility, and consumer
promises. This profile selects a Rust mechanism only after those contracts are
accepted. A Rust type, trait, derive, visibility modifier, parameter wrapper,
conversion trait, feature, attribute, or documentation form cannot create,
weaken, or silently complete a missing generic contract.

Select the smallest supported Rust surface that preserves the accepted
contract, consumer capabilities, ownership and lifetime semantics, evolution
policy, performance constraints, and evidence claim. Existing syntax,
ecosystem convention, brevity, or compiler acceptance alone does not select the
mechanism.

## Public Contract Trait Mechanisms

Implement or derive a trait only when its semantics are part of the accepted
consumer contract and every represented value can satisfy those semantics.
Select static or dynamic dispatch, associated or generic parameters, sealed or
downstream-implementable traits, extension markers, and result-use attributes
from actual consumer, evolution, object-safety, ownership, performance, and
compatibility facts.

`Debug`, `Display`, `Clone`, `Copy`, equality, ordering, hashing,
`Default`, `#[must_use]`, `#[non_exhaustive]`, sealed traits, associated
types, generics, and trait objects are mechanisms, not baseline requirements.
Do not derive a trait because neighboring types do, expose implementation state
to satisfy formatting, make an expensive or identity-bearing value copyable,
invent a default state, seal an intended extension point, or make a contract
non-exhaustive without an evolution need.

## Validated Type And Conversion Mechanisms

After Contracts selects an invariant owner, enforcement point, proof lifetime,
and failure outcome, select a Rust representation that preserves those facts.
Applicable mechanisms include a private-field newtype, enum, state-specific
type, smart constructor, `TryFrom`, `FromStr`, or another fallible conversion
whose success yields the accepted proof-bearing representation.

Choose the mechanism from the source representation, trust boundary, invariant
complexity, mutation paths, consumer needs, error contract, and toolchain
capability. A type cannot preserve proof after mutation or external state
invalidates its invariant; re-establish proof at the canonical enforcement
point rather than trusting stale construction.

Newtypes, enums, private constructors, `TryFrom`, `FromStr`, typestate, and
named two-variant enums are mechanisms, not defaults. Do not select type-level
complexity from subjective bug cost, a fixed state count, public visibility,
security labels, primitive type names, a parse-once slogan, or preference over
tests and assertions. Do not wrap every primitive, replace every boolean,
mandate one conversion trait by input category, or treat successful parsing as
complete operation-specific validation.

## Parameter And Ownership Mechanisms

Select borrowed or owned parameters from what the operation reads, stores,
transfers, mutates, and returns, including the accepted lifetime and allocation
contract. Select `&str`, `&Path`, slices, owned values, `AsRef`, `Into`,
`Cow`, or a domain type only when that mechanism preserves those facts for
the supported consumers.

Do not accept an owned value when borrowing satisfies the contract, clone only
to satisfy an incidental signature, add a generic conversion wrapper solely
for convenience, or use `Cow` without a real borrow-or-own behavior. Do not
replace a validated domain type with a primitive parameter or introduce a
wrapper whose conversion, error, allocation, ambiguity, or compatibility
effects are unowned.

## Crate And Module Boundary Mechanisms

After Architecture selects responsibility, dependency direction, public
surface, and composition boundaries, express those decisions with supported
Rust crate membership, modules, visibility, re-exports, and conditional
compilation. Keep business policy independent of adapters and bindings when the
accepted architecture requires that separation; do not infer the separation
from crate names or an incumbent workspace layout.

Choose `pub`, `pub(crate)`, private modules, curated re-exports, nested modules,
workspace crates, target modules, or item-level `cfg` from the accepted owner
and consumer contract, compilation boundary, platform variation, test surface,
and toolchain capability. Conditional compilation must preserve one coherent
public contract or expose typed unsupported capability; it cannot silently
select a different authority or behavior.

Crates, modules, visibility modifiers, re-exports, and `cfg` are mechanisms,
not architecture defaults. Do not prescribe `core`, `contracts`, `adapter`,
`infra`, `bindings`, `app`, `server`, `cli`, or `xtask` roles; a fixed source
tree; `lib.rs`, `error.rs`, `types.rs`, `platform`, test, benchmark, or example
placement; public re-exports; `pub(crate)` implementation modules; or thin
platform modules without the accepted architecture and consumer facts.

## Failure Expression Mechanisms

After Contracts selects expected absence, invariant, validation, and
impossible-state semantics, and after Resilience selects every applicable
operational failure, recovery, retry, degradation, and availability outcome,
express those decisions with supported Rust mechanisms. The Rust profile does
not infer whether a condition is absent, failed, invalid, impossible,
recoverable, degradable, or terminal.

Select `Result`, `Option`, an error type, propagation with `?`, matching,
assertion, panic, `unreachable!`, `unwrap`, or `expect` only when the accepted
contract gives that mechanism the required value, error, termination,
diagnostic, and consumer semantics. An `Option` must not erase failure or
unavailability. Panic, assertion, `unreachable!`, `unwrap`, and `expect` must
not replace a missing proof, recovery decision, or typed outcome.

These are language mechanisms, not situation defaults. Do not select them from
an external-input label, public visibility, request or lifecycle path, test or
example location, prototype status, compile-time construction, or a claim that
an operation is "truly infallible." Do not mandate `thiserror`, `anyhow`, a
specific error-enum shape, prohibition of `Result<T, String>`, added context,
or preference for `expect` over `unwrap` without the accepted contract and
consumer facts.

## Cargo Feature Expression Mechanisms

After Dependencies selects feature, optional-dependency, default, target, and
footprint behavior; Contracts selects consumer-visible compatibility; Library
selects supported real consumer configurations; Documentation selects durable
artifacts; and Verification selects claim-matched evidence, express the
accepted result with supported Cargo and Rust mechanisms.

Applicable mechanisms include named Cargo features, a `default` feature set,
optional dependency declarations, explicit dependency forwarding, `dep:`
references, feature grouping, target-specific dependency declarations,
item-level or module-level `cfg`, and compile-time conflict diagnostics. Select
only mechanisms supported by the declared Cargo resolver and toolchain, and
preserve each accepted consumer configuration without exposing an unintended
public feature or silently changing behavior.

Cargo mechanisms are not feature-policy defaults. Do not require minimal or
empty defaults, `dep:` syntax, optionality for expensive/platform/unsafe/binding
dependencies, avoidance or acceptance of mutually exclusive features,
`compile_error!`, README or crate-doc placement, default/all/no-default command
matrices, `cargo hack`, or an all-features configuration without the applicable
generic owner decisions and capability evidence.

## Rustdoc Expression Mechanisms

After Documentation selects the documentation trigger, artifact, placement,
audience, and quality contract, and after each content owner supplies its
authoritative facts, select a supported Rustdoc expression. Content owners may
include Contracts for invariant and compatibility facts, Resilience for failure
behavior, Dependencies for feature facts, Rust Unsafe for safety contracts, and
Library for external-consumer applicability.

Applicable mechanisms include crate-level `//!` documentation, item-level
`///` documentation, headings, code blocks, doctests, examples, intra-doc links,
and attributes that control rendered documentation. Select the form from the
accepted artifact and audience, public surface, content contract, supported
toolchain, and evidence claim. Rustdoc form cannot create or weaken the fact it
describes, and generated output cannot replace its canonical source.

Rustdoc forms are not documentation defaults. Do not require crate-level docs,
`# Errors`, `# Panics`, `# Safety`, feature sections, README or crate-doc
placement, examples, or explanations of implementation mechanics without the
applicable owner decision. The Rust Unsafe profile remains authoritative for
public unsafe contracts and `# Safety` obligations; this profile only expresses
an accepted obligation in Rustdoc.

## Typed Outcomes

Return typed `invalid` when the selected Rust mechanism contradicts the
accepted contract, ownership, lifetime, consumer, or semantic facts. Return
typed `unsupported` when a valid contract has no supported Rust expression
for the selected toolchain or consumers. Return typed `unavailable` when a
required contract, owner, consumer capability, toolchain fact, or evidence
claim cannot be established.

Do not fall back to an incumbent signature, universal derive set, conventional
trait shape, trait object, generic wrapper, owned parameter, clone, primitive
type, successful compile, or smallest diff.

## Verification

Evidence covers applicable public consumers, trait semantics, downstream
implementation or sealing, dispatch behavior, invariant representation and
proof lifetime, fallible conversion and rejected inputs, ownership and
borrowing, allocation and conversion, compatibility, ignored-result behavior,
and the actual supported toolchain. Compile success proves only that the
selected program is accepted by that compiler invocation; it does not prove
semantic, validation, consumer, compatibility, performance, or documentation
claims.
