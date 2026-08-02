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
