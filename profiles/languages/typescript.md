# TypeScript Profile

**Standards metadata**

- ID: `profile.language.typescript`
- Role: `profile`
- Level: `PROFILE`
- Applies when: TypeScript source, compiler configuration, declarations, generated TypeScript, or TypeScript-visible contract surfaces change.
- Does not apply when: No TypeScript-owned source, configuration, generated artifact, or consumer surface changes.
- Requires: `core`, `workflow.verification`, `topic.contracts`
- Specializes: `topic.contracts`
- Verification: TypeScript public-surface, inference, runtime-decoding, contract-projection, and generated-type decision fixtures plus affected compiler and consumer evidence.
- Canonical owner: `profiles/languages/typescript.md`

## Public Type Surfaces

Select explicit annotations where they preserve an owned consumer contract,
published declaration, overload, generated interface, independently compiled
boundary, or reviewable API promise. Inference is valid for local
implementation and may be valid at a public surface when the emitted and
consumed contract is intentionally derived and verified.

Do not require explicit return types for every exported function or permit
inference merely because a function is private. Select the mechanism from the
actual consumer boundary, declaration output, refactoring risk, and evidence.

## Runtime Boundaries

TypeScript types do not validate runtime values. Decode untrusted or
independently produced input through the canonical
[Contracts](../../topics/contracts.md#runtime-decoding-at-boundaries)
authority before treating it as a domain value. Use `unknown` or another
non-authorizing representation until proof is established when the selected
decoder requires it.

Do not use `any`, a type assertion, generic parameter, interface declaration,
or copied response shape as runtime proof. Preserve the decoder's typed
`invalid`, `unsupported`, or `unavailable` outcome.

## Contract Type Projection

Derive TypeScript contract types from the canonical schema, generator input,
producer contract, or owned domain authority selected by Contracts. Generate
types when generation is the selected authority; otherwise keep a separately
implemented projection traceable and prove conformance through the real
producer and consumer path.

Use domain types when they encode real distinctions or invariants. A raw
primitive is valid when it is the selected contract; wrapping every string or
number does not create proof. Do not hand-copy an external response, infer a
schema from one sample, rename variants independently, or substitute a nearby
type when authority or generation is unavailable.

## Typed Outcomes

Contradictory type authority, declaration output, or producer/consumer
representations are `invalid`. A well-formed contract variant outside the
supported set is `unsupported`. Missing schema, decoder, generator, consumer
contract, or required evidence is `unavailable`.

Do not continue with `any`, assertions, stale declarations, copied shapes,
alternate generators, raw primitives that erase required distinctions, or
default success.

## Static Analysis And Compiler Configuration

Select type-aware lint scope from the actual TypeScript project boundaries,
included source and configuration consumers, parser/compiler compatibility,
generated-source authority, and required lint claims. Select compiler checks
individually from owned invariants, emitted declaration contracts, runtime
assumptions, migration constraints, and supported toolchain capability.

Architecture analysis must derive prohibited and required relationships from
the canonical architecture contract. A linter selector or custom rule is an
implementation mechanism, not architecture authority. Do not default to an
ESLint version, parser, preset, formatter integration, file glob, ignore list,
strict-mode bundle, compiler-flag list, severity, or custom-rule implementation.

Contradictory project, compiler, consumer, or architecture facts are `invalid`.
Missing project boundaries, rule authority, or required configuration evidence
is `unavailable`. Required analysis unsupported by the selected compiler or
toolchain is `unsupported`; do not broaden scope, disable the check, copy a
nearby preset, or accept a compiler pass as runtime or architecture proof.

## Verification

Evidence covers applicable compiler configuration, emitted declarations,
generated-source consistency, runtime rejection of invalid input, supported
and unsupported variants, domain distinctions, and the real producer/consumer
path. A compiler pass proves static consistency only; it does not prove runtime
input validity or external contract conformance.
