# Application exposure review packet

This proposal qualifies unchanged accepted material for application agents.
It does not adopt the CodeRabbit normative drafts or revise principles.

- Proposal: `proposal:v1:800744d7-33d1-4b31-9a8e-bd66d2c9d3db`.
- Revision: `proposal-revision:sha256:15c67a010c50cb271e16abe4dabe2889df266ec9c201d949043af24ff06f4a45`.
- Current state: `needs-action`, with 32 exposure impact reviews pending.
- Accepted snapshot: `snapshot:v1:5fbd6b92-a9f2-4d5e-bbcb-894f843a6a85`.
- Existing source revision: `dcc56f26e884ade260770beceba2501d3746200d`.

Of the 33 previously unreviewed modules, 32 are proposed for application
exposure. `workflow.standards-authoring` remains authoring-only because its
applicability explicitly excludes projects merely applying the library.
Optional reference authority stays optional; no reference becomes a normative
prerequisite merely by approving its exposure.

## Review scope

Review each entire module, including applicability, exceptions, metadata,
links, headings and required dependencies. Assess generality, operational
sufficiency, authority, consumer coherence and whether application exposure is
appropriate. Report concrete blocking defects rather than approving from the
module title or the earlier principle-audit conclusion. The exact candidate
must also pass application read and graph checks before publication.

The source corpus and existing required dependencies have been retained in
[accepted-material.json](accepted-material.json). Engine results are in
[proposal-result.json](proposal-result.json). An independent material review
has not yet been completed for this qualification proposal.

An existing unpublished exposure-manifest change must be preserved. Candidate
and accepted-source content must not be confused with the live dirty worktree.

## Requested modules

| Module | Authority role | Required modules |
| --- | --- | --- |
| `workflow.verification.oracles` | workflow | `workflow.verification` |
| `topic.contracts` | topic | `core`, `workflow.verification` |
| `topic.cross-platform` | topic | `core`, `workflow.verification` |
| `reference.recipes.tooling` | reference | `workflow.tooling`, `topic.dependencies` |
| `profile.boundary.generated-contract` | profile | `core`, `workflow.verification`, `workflow.build`, `topic.contracts`, `topic.dependencies`, `topic.contracts.schemas` |
| `workflow.verification.platforms` | workflow | `workflow.verification` |
| `topic.resilience` | topic | `core`, `workflow.verification`, `topic.contracts` |
| `topic.diagnostics` | topic | `core`, `workflow.verification`, `topic.contracts` |
| `workflow.documentation` | workflow | `core` |
| `workflow.build` | workflow | `core`, `workflow.implementation`, `workflow.verification` |
| `workflow.commit` | workflow | `core`, `workflow.implementation` |
| `workflow.release` | workflow | `core`, `workflow.verification`, `topic.contracts` |
| `workflow.release.operations` | workflow | `workflow.release` |
| `topic.performance` | topic | `core`, `workflow.verification` |
| `topic.contracts.schemas` | topic | `topic.contracts` |
| `topic.contracts.protocols` | topic | `topic.contracts` |
| `topic.contracts.evolution` | topic | `topic.contracts` |
| `topic.architecture` | topic | `core`, `topic.contracts` |
| `topic.architecture.replay` | topic | `topic.architecture` |
| `topic.code-design` | topic | `core` |
| `topic.dependencies` | topic | `core`, `workflow.verification` |
| `topic.licensing` | topic | `core`, `workflow.verification` |
| `topic.accessibility` | topic | `core`, `workflow.verification` |
| `profile.boundary.persistence` | profile | `core`, `workflow.verification`, `topic.contracts`, `topic.contracts.evolution` |
| `profile.application.frontend` | profile | `core`, `workflow.verification`, `topic.accessibility` |
| `profile.language.rust` | profile | `core` |
| `profile.language.rust.async` | profile | `core`, `workflow.verification`, `topic.concurrency`, `profile.language.rust` |
| `profile.language.rust.api` | profile | `core`, `topic.contracts`, `workflow.documentation`, `profile.language.rust` |
| `profile.language.rust.security` | profile | `core`, `workflow.verification`, `topic.security`, `profile.language.rust` |
| `profile.language.typescript` | profile | `core`, `workflow.verification` |
| `profile.language.typescript.async` | profile | `core`, `workflow.verification`, `topic.concurrency`, `profile.language.typescript` |
| `workflow.verification.gui` | workflow | `workflow.verification` |

## Exact accepted module text

The fenced content below preserves the MCP-returned bytes of each module.
Relative links inside those code blocks refer to the canonical module location,
not this packet's location.

### workflow.verification.oracles

````markdown
# Independent Test Oracles

**Standards metadata**

- ID: `workflow.verification.oracles`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change creates a validator, negative fixture, property test, differential test, or other independent oracle.
- Does not apply when: Ordinary existing assertions suffice and no validation oracle, negative fixture, property, or differential mechanism changes.
- Requires: `workflow.verification`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `workflows/verification/oracles.md`

## Evidence Oracle Boundaries

For each acceptance claim, identify the observation mechanism and the exact
property it can decide. The expected property must come from authority
independent of the subject under test. Two projections that share one semantic
implementation can prove agreement with each other, but not conformance to an
external contract.

Keep these evidence boundaries explicit:

- deterministic generation proves freshness from the selected source, not
  semantic completeness;
- an exact literal proves literal identity only when literal identity is the
  contract;
- coordinated edits to a subject and a copied expectation do not provide an
  independent oracle; and
- mutation evidence proves detection of the sampled mutations, not complete
  detection outside the sampled domain.

When the required claim has no independent or otherwise authoritative oracle,
return `unavailable`. When the mechanism cannot decide the claimed property,
the evidence is `invalid`. Do not upgrade local agreement, freshness, parsing,
snapshot equality, or a passing harness into a stronger conformance claim.
## Negative Fixture Isolation

A negative fixture proves its intended failure only when every unrelated
precondition is valid and the observed result identifies the expected
diagnostic or failure point. Record the expected typed diagnostic and the
relevant complete message or structured fields when those details distinguish
the target failure from earlier validation failures.

Construct the fixture from a valid case by changing only the condition under
test where practical. A nonzero exit, thrown exception, generic rejection, or
substring match is insufficient when several validators can reject the same
input. If the fixture cannot reach the intended boundary, classify the
evidence as `invalid`; do not count incidental failure as acceptance.
## Property And Differential Evidence

Property, generative, mutation, and differential evidence must name:

- the property being tested;
- the generated or sampled input domain;
- the independent or authoritative oracle;
- the compared implementations or projections;
- reproducibility and shrinking behavior where applicable; and
- the unsupported or unexamined domain.

Comparison between local implementations proves consistency only unless an
independent authority establishes expected semantics. External conformance
claims require the selected specification, reference implementation, official
corpus, or another authority that is independent of the implementations being
compared. A sampled counterexample can disprove a universal claim; absence of
one does not prove completeness beyond the declared domain.

Return `unsupported` when the selected oracle or corpus does not cover a
well-formed required domain and `unavailable` when required authority or
reproducibility inputs cannot be obtained. Do not silently narrow the claim to
the cases a generator or local comparator happens to support.
````

### topic.contracts

````markdown
# Contract Evolution And Degraded Outcomes

**Standards metadata**

- ID: `topic.contracts`
- Role: `topic`
- Level: `MUST`
- Applies when: A change affects data or behavior consumed across a module, process, persistence, package, deployment, or generated boundary.
- Does not apply when: A private implementation detail has no independent consumer, stored representation, or externally observable promise.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Contract and runtime-decoding decision fixtures plus affected producer/consumer claims.
- Canonical owner: `topics/contracts.md`

## Invariant Contracts

State each material invariant as an observable contract owned by the value,
operation, state transition, or boundary that must preserve it. Record the
applicable domain, required state, and the transitions that may establish,
preserve, or invalidate it.

Preconditions describe facts a caller or upstream owner must establish before
an operation. Postconditions describe facts the operation guarantees on each
declared outcome. Internal assumptions are not preconditions unless a real
caller can establish and verify them. Do not transfer an implementation
obligation to a caller merely to simplify the implementation.

Select enforcement points from the invariant's authority, corruption impact,
trust boundary, mutation paths, and proof lifetime. Construction, transition,
boundary, persistence, and read-time checks are different decisions. Build
mode alone does not decide which invariants remain enforced, and successful
earlier validation does not authorize stale proof.

Document an invariant when its owner, meaning, enforcement point, invalidation,
or failure outcome is not evident from the type and implementation. Keep the
contract with its canonical owner; do not require a copied comment template or
repeat the same authority at every call site.

Verification selects evidence that can prove the invariant and its relevant
failure mode. Evidence may be a focused example, property check, model,
contract fixture, integration path, static proof, or other objective-aligned
method. Do not require one test per sentence or infer adequate evidence from a
test name.

Before selecting a violation outcome, classify its source and reachable
consequence. Distinguish arbitrary or adversarial input, operational failure,
a contained programming defect, invalid state that can escape through a public
or trust boundary, and corruption of authoritative state. Select rejection,
immediate failure, a typed public outcome, recovery, or another mechanism from
that classification and the owned operation contract; no mechanism is
universally correct for every invariant.

Immediate failure with trace-led diagnosis is valid for a contained
programming defect when it prevents invalid state from escaping or corrupting
authority and no public, availability, or recovery contract requires another
outcome. Arbitrary or adversarial input must follow its boundary and Security
contract. Operational failure, escaping invalid state, and authoritative-state
corruption preserve their selected typed outcome or recovery obligation; a
diagnostic alone cannot satisfy those contracts.

An invariant violation is `invalid`. Missing authority, classification,
enforcement capability, selected outcome, or required evidence is
`unavailable`; a well-formed contract variant outside the supported set is
`unsupported`. Do not substitute debug-only enforcement, logging without the
selected outcome, silent corruption, an unchecked state, or a weaker
invariant. Panic, recovery, rejection, or graceful termination is valid only
when it is the selected outcome rather than a fallback.

## Runtime Decoding At Boundaries

When a value enters through a trust, process, persistence, plugin, queue, or
independently deployed boundary, treat its representation as unknown until an
executable decoder or smart constructor proves the applicable contract.

A validated value is a construction result, not a type annotation. Successful
parsing or deserialization proves only that a representation was readable. A
type assertion, generic object check, producer-side static type, or partial
field check cannot establish runtime validity.

Before constructing a validated value, check every invariant required by that
value, including those that apply:

- aggregate shape, required fields, optionality, and extra-field policy;
- discriminants and the complete selected variant;
- field domains, bounds, identifiers, and cross-field relationships;
- supported contract or schema versions; and
- explicit normalization and defaulting rules.

The decoder must return either the validated representation or a typed
diagnostic:

- `invalid` for malformed data, failed constraints, or incomplete proof;
- `unsupported` for a well-formed version or variant outside the supported
  contract; or
- `unavailable` when required decoding capability or contract material cannot
  be obtained.

The validated representation must not expose an unchecked mutable alias that
can invalidate the proof after construction. Passing the validated value
inward does not authorize reuse of the original unknown representation.

Values created and kept inside one trusted in-process boundary do not require a
redundant runtime decode when their constructor already enforces the same
invariants. Crossing a new applicable boundary, changing contract version, or
losing the validated representation requires decoding again.

Do not fall back to a cast, the original input, an alternate unchecked shape, a
permissive default, or a weaker decoder when proof is missing. No particular
schema or validation library is mandatory; the observable proof and typed
outcomes are.

## Inbound And Outbound Boundary Proof

Apply the complete applicable contract in both directions. Inbound validation
proves that unknown input may enter the owning boundary. Outbound validation
proves that a produced value may cross its destination boundary. Validation in
one direction does not prove the other direction, and successful transport,
serialization, parsing, or operation completion does not prove the value's
contract.

For inbound values, establish the runtime-decoding proof above before business
logic consumes the value. For outbound values, first classify the operation or
protocol outcome, then prove the complete destination representation before
emitting it or treating it as a successful result. Error, rejection, and
degraded representations have contracts too; do not parse or reinterpret one
as a successful payload merely because its representation is readable.

Code inside one trusted boundary consumes an intact proof-bearing
representation without redundant validation. A new destination, contract
version, representation, or trust boundary requires the proof applicable to
that crossing.

Return a typed boundary outcome that preserves the failed obligation:

- `invalid` when the representation or required invariants fail;
- `unsupported` when a well-formed outcome, version, or variant is outside the
  selected contract; or
- `unavailable` when required contract, decoding, encoding, or outcome
  classification capability is absent.

The owning protocol or adapter may specialize these outcomes into its declared
mechanisms. Contracts does not mandate HTTP status checks, exception throwing,
response wrappers, middleware, or a particular decoder. Do not treat a default
body, empty object, alternate parser, guessed status, successful transport, or
the original unchecked value as a valid fallback.

## Validation Proof Lifetime

Validation authority belongs to the proof-bearing representation produced by
the applicable decoder or smart constructor, not to the fact that validation
happened earlier. Record the complete contract and version whose invariants the
representation establishes.

The proof remains authoritative only while the validated representation is
retained, its invariants cannot be changed through an unchecked alias, the
applicable contract is unchanged, and the value remains inside the boundary
for which that proof applies. Code inside that boundary consumes the validated
representation directly; it does not decode the same unchanged value again.

Establish new proof after the validated representation is lost, after unchecked
mutation, when the applicable contract or required invariants change, or when
the value crosses a new trust, process, persistence, plugin, queue, or
independently deployed boundary. The new boundary applies its complete current
contract to the current input; validation of a prior value or representation
does not carry forward.

A boolean validation flag, validation-history record, type annotation, or
equality with a previously validated value is not a validated representation.
Missing capability returns typed `unavailable`; a well-formed unsupported
contract returns `unsupported`; failed proof returns `invalid`.

Do not fall back to the original unknown input, stale proof, unchecked mutable
alias, implicit trust across a new boundary, permissive defaults, or a weaker
decoder. Do not discard an intact proof-bearing representation merely to
mandate redundant validation.

## Record Contract Facts First

Before selecting compatibility or migration behavior, record:

- canonical producer and policy owner;
- actual consumers and their owners;
- whether producer and consumers deploy atomically or independently;
- whether values persist beyond one coordinated deployment;
- supported prior versions or data states;
- source of truth and whether substitutes preserve the same semantics; and
- public, regulatory, protocol, or platform promises outside repository control.

Unknown facts produce an unresolved-contract diagnostic. Do not select the most
compatible-looking default.

## Producer-Consumer Semantic Preservation

A structured contract governs every meaning selected by its canonical
authority, not only field names or readable representation. Record which shape,
optionality, discriminants, defaults, constraints, identifiers, ordering,
labels, descriptions, and compatibility behavior affect producer output,
consumer decisions, persisted identity, or operator action. A category is not
contractual merely because it appears in this list; authority and observable
use select the applicable semantics.

Each producer proves that its emitted value satisfies the selected contract.
Each consumer proves that it accepts and preserves the selected semantics it
uses. A projection, form, menu, runtime object, generated configuration, or
stored artifact is a new destination representation when it transforms those
semantics and must satisfy its own explicit destination contract.

A consumer may intentionally omit, transform, or reinterpret a source semantic
only when the destination contract authorizes that behavior and the affected
compatibility and persistence outcomes are explicit. Successful parsing,
matching field names, a producer test, documentation of the transformation, or
visual similarity does not prove destination conformance.

Missing authority, consumer facts, or destination contract is `unavailable`;
contradictory output, silently dropped selected meaning, or incomplete proof is
`invalid`; a well-formed source variant outside the destination support set is
`unsupported`. Do not fall back to inferred defaults, nearby labels, source
ordering, guessed enum meaning, omitted constraints, or the original source
representation when destination proof is absent.

## Contract Artifact Necessity And Authority Placement

Create a contract artifact only when it has a distinct purpose that the
existing authoritative representation does not already satisfy. Valid purposes
include establishing independently consumed authority, enforcing a boundary
invariant, making invalid states unrepresentable, defining a distinct wire or
persistence representation, governing evolution, enabling deterministic
generation, or removing duplicated interpretation.

A DTO, projection, wrapper, schema, interface, or generated artifact that only
mirrors another shape is not justified without a distinct ownership,
validation, representation, evolution, or transport obligation. Convenience,
framework convention, symmetry, and possible future reuse are not sufficient
contract purposes.

Place canonical authority where every selected producer, consumer, validator,
and generator can depend on it without depending on an unrelated
implementation. This may be a dedicated package, an owned schema or generator
input, or a producer-owned module with an appropriate dependency boundary. A
dedicated package is not required when one owner and its consumers can access
the authority without cycles, duplicated definitions, or implementation
coupling.

Record the authority, purpose, consumers, derivation, invalidation, and
evolution class before introducing the artifact. Missing required facts or
authority is `unavailable`; an artifact that contradicts its authority or lacks
a distinct purpose is `invalid`; an unavailable required artifact mechanism is
`unsupported`. Do not fall back to an inferred mirror, duplicated schema,
unrelated implementation dependency, or speculative compatibility artifact.

## Declaration And Semantic Authority

When a change affects schema dialects, generated contracts, or contract version invalidation, follow [Declaration And Semantic Authority](contracts/schemas.md#declaration-and-semantic-authority).

## Version Scope And Invalidation

When a change affects schema dialects, generated contracts, or contract version invalidation, follow [Version Scope And Invalidation](contracts/schemas.md#version-scope-and-invalidation).

## Generated Contract Semantic Conformance

When a change affects schema dialects, generated contracts, or contract version invalidation, follow [Generated Contract Semantic Conformance](contracts/schemas.md#generated-contract-semantic-conformance).

## Schema Dialect And Vocabulary

When a change affects schema dialects, generated contracts, or contract version invalidation, follow [Schema Dialect And Vocabulary](contracts/schemas.md#schema-dialect-and-vocabulary).

## Identity And Instance Equality

Keep schema-instance equality, domain-value equality, and content-identity
canonicalization as separate contracts. Each equality relation declares its
owner, applicable types, normalization behavior, duplicate semantics, and
consumer purpose. A normalization selected for stable identifiers does not
change instance equality unless the schema or domain contract explicitly says
so.

Validators, generated decoders, identity serializers, applicability
evaluators, and persisted-handle implementations use the equality relation
owned by their selected contract. Agreement between two local implementations
does not establish that either matches an external schema dialect. Test
cross-type numeric and Boolean values, Unicode representations, collection
uniqueness, constants, and enumerations only where those cases belong to the
declared domain.

Contradictory equality authorities are `invalid`; a required relation outside
the supported dialect or domain is `unsupported`; and a missing equality
authority is `unavailable`. Do not reuse canonical identity bytes as a general
validation comparator or silently normalize values at a boundary whose
contract requires codepoint-preserving comparison.

## Protocol Outcome Projection

When a change projects domain outcomes into a protocol or adapts a protocol boundary, follow [Protocol Outcome Projection](contracts/protocols.md#protocol-outcome-projection).

## Protocol Adapter Proof

When a change projects domain outcomes into a protocol or adapts a protocol boundary, follow [Protocol Adapter Proof](contracts/protocols.md#protocol-adapter-proof).

## Contract Classes

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Contract Classes](contracts/evolution.md#contract-classes).

## Cross-Language Contract Selection

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Cross-Language Contract Selection](contracts/evolution.md#cross-language-contract-selection).

## Coordinated Breaking Replacement

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Coordinated Breaking Replacement](contracts/evolution.md#coordinated-breaking-replacement).

## Persisted Evolution

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Persisted Evolution](contracts/evolution.md#persisted-evolution).

## Persisted Contract Artifacts

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Persisted Contract Artifacts](contracts/evolution.md#persisted-contract-artifacts).

## Public And Independently Deployed Evolution

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Public And Independently Deployed Evolution](contracts/evolution.md#public-and-independently-deployed-evolution).

## Degraded Outcomes

Degraded behavior is valid only when its source is authoritative enough for the
operation and its semantics remain true. Record:

- provenance and freshness;
- operations allowed while degraded;
- differences visible to callers or users;
- recovery and invalidation behavior; and
- acceptance claims for the degraded path.

If no semantically valid result exists, return a typed outcome such as:

- `unavailable` when a required capability or resource is absent;
- `invalid` when input or stored state violates the contract;
- `unsupported` when a version or capability is outside the supported set; or
- `deferred` when valid work is durably queued for later execution.

Do not return defaults, partial values, empty collections, stale cache entries,
or alternate execution paths unless the contract explicitly defines them as
valid results.

## No Implicit Fallback

Fallback is a contract decision, not an exception-handling convenience. It
requires:

- an owner with authority to define the substitute;
- semantic fidelity for the requested operation;
- an observable degraded state;
- bounded staleness or validity rules; and
- focused and objective-level evidence.

When any requirement is missing, preserve the typed diagnostic rather than
guessing, silently retrying another backend, or carrying forward old behavior.
````

### topic.cross-platform

````markdown
# Cross-Platform

**Standards metadata**

- ID: `topic.cross-platform`
- Role: `topic`
- Level: `MUST`
- Applies when: Supported targets differ in capability, build or deployment selection, platform behavior, filesystem identity, or required evidence.
- Does not apply when: The affected behavior has one declared target contract and no platform-dependent behavior or portable boundary.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Platform-target, native-artifact-loading, and filesystem-identity decision fixtures plus evidence on each target required by the selected claim.
- Canonical owner: `topics/cross-platform.md`

## Platform Support Contract

Declare supported targets in the project, product, or release contract. For
each target, define the support claim, required behavior, unavailable or
unsupported capabilities, artifact/build requirements, and evidence needed to
accept the claim. Product target names and support tiers are project facts, not
generic defaults.

A required behavior must retain its declared semantics on every target covered
by the claim. An intentionally optional capability is distinct from an
unimplemented required capability. Return typed `invalid` for contradictory
target facts, `unsupported` when the declared target or capability is outside
the supported contract, and `unavailable` when required target, build,
deployment, capability, or evidence facts cannot be established.

## Platform Behavior Isolation

Keep platform selection and platform-specific mechanics outside domain
behavior. Choose the smallest cohesive boundary that preserves the domain
contract and follows the language and architecture: a function, module,
adapter, injected capability, build-selected implementation, or another
explicit boundary may be correct.

Select compile-time, runtime, composition, and dispatch mechanisms from the
language, toolchain, artifact, and deployment contract. File and module
boundaries follow cohesion and language conventions. No Strategy/Factory,
runtime detection, compile-time condition, or one-file-per-platform layout is
universally required.

Platform-specific code may return a typed unsupported or unavailable outcome
when the selected contract permits it. A stub, log message, false result,
silent omission, or alternate implementation is not graceful degradation
unless an explicit product contract defines that result as semantically valid.

Language-specific target syntax, build mechanisms, and target verification
belong to the selected language profile. Use the
[Standards Router](../STANDARDS-ROUTER.md) to select it.

### No Fallback

Missing target, support, capability, build, deployment, or evidence facts
cannot choose a default platform list, support tier, Strategy/Factory, runtime
detection, compile-time condition, file layout, stub, silent omission,
alternate mechanism, or weaker evidence.

## Native Artifact Loading

Before selecting how a native artifact is linked, located, loaded, or supplied,
declare:

- the artifact identity or immutable revision and its canonical authority;
- target, architecture, ABI, and compatibility requirements;
- delivery authority and location contract;
- integrity or authenticity requirements when applicable;
- the mechanism and lifecycle authority that make it available to the
  consumer; and
- the consumer and target evidence required by the support claim.

Select static linking, dynamic loading, package-managed resolution, an
operating-system loader, a process-provided handle, an embedded resource, or
another mechanism only when the declared artifact and deployment contracts
support it. A package resolver or operating-system search path is valid only
when that authority is part of the deployment contract and resolves the
declared artifact; ambient discovery is not artifact identity.

The selected consumer must verify the resolved artifact and preserve its
declared lifecycle and failure semantics. Shipped artifact identity,
installation information, and publication presentation belong to
[Release](../workflows/release.md). Language-specific linking and loader
mechanics belong to the selected language profile.

Return `invalid` for contradictory or ambiguous artifact facts, `unsupported`
for a well-formed target, ABI, or artifact outside the declared support
contract, and `unavailable` when required artifact, delivery, loader,
capability, or evidence facts cannot be established.

### No Fallback

Do not mandate Strategy/Factory, guess a filename or extension, use an ambient
search result as identity, try another loader or artifact, embed a copy, or
report success when the selected artifact contract is unsupported or
unavailable.

## Filesystem Paths

Use path APIs that preserve platform components. Do not construct paths with
hard-coded separators or recover components by splitting display strings.
Spaces and other valid platform path characters remain ordinary path data, not
shell or parsing syntax.

## Display, Lexical, And Canonical Forms

Keep these concepts distinct:

- display form is presentation for a user or log;
- lexical normalization resolves syntax such as redundant separators and
  `.` components without proving filesystem identity; and
- canonical identity resolves the filesystem object and aliases according to
  the platform contract.

Tests compare the form used by the behavior under test. Code that canonicalizes
or resolves real paths needs canonical expectations; display-only behavior
must not force canonical presentation.

## Comparison

Compare path components using the selected platform and filesystem contract.
Do not use raw string prefix as equality, ancestry, or containment. Do not
apply one universal case-folding or Unicode-normalization rule merely from an
operating-system name; mounted filesystems and platform-managed aliases can
have different identity behavior.

Account for temp directories, symlinked workspaces, mounted volumes, and
platform aliases such as two display paths resolving to one object. When an
untrusted path authorizes an operation, apply
[Filesystem Containment](security.md#filesystem-containment) in addition to
these identity rules.

## Verification

Platform-target checks cover single and multiple declared targets, mechanism
selection, cohesive isolation, semantic optionality, typed outcomes, and the
evidence environment required by each support claim.

Record the supported platform and filesystem families for the affected claim.
Exercise path construction and identity on each required family where behavior
differs. A simulated or single-filesystem check cannot satisfy a claim that
requires real behavior from another filesystem family.

Include spaces, alias paths, differing case behavior, canonical root equality,
and component-aware ancestry where applicable. Unknown filesystem semantics
produce an unresolved platform diagnostic rather than a guessed comparison.
````

### reference.recipes.tooling

````markdown
# Tooling Recipes

**Standards metadata**

- ID: `reference.recipes.tooling`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A project has selected a development-tool workflow and needs illustrative hook or editor configuration.
- Does not apply when: Tool, dependency, editor-configuration, file-setting, acceptance, scheduling, or bypass decisions are being made.
- Requires: `workflow.tooling`, `topic.dependencies`
- Specializes: `none`
- Verification: Tooling-reference dispositions, metadata, link, and authority checks.
- Canonical owner: `reference/recipes/tooling.md`

This material is non-normative. [Tooling](../../workflows/tooling.md) owns tool
selection, configuration, automation, and scheduling. [Dependencies](../../topics/dependencies.md)
owns dependency selection and installation. Projects must make those decisions
before adapting an example below.

## Maintained Editor Configuration Recipe

For ordinary UTF-8 source files shared across editors, an `.editorconfig` can
express the Tooling defaults without selecting a language formatter:

```ini
root = true

[*]
charset = utf-8
insert_final_newline = true
```

Scope this to owned source files when the repository also contains formats
whose consumers require a different encoding or ending. Leave indentation and
language layout to the existing formatter. Verify an affected editor or tool
actually consumes the settings, then check the resulting file with its real
consumer. The following retained migration examples illustrate additional
mechanisms and historical configurations, not a current universal preset.

## Legacy Tool Setup And Package Script Example

The legacy setup example listed EditorConfig, a formatter such as Prettier, a
linter such as ESLint, and a hook runner such as Lefthook or Husky. This list is
historical illustration only. It does not establish a minimum setup, required
tool category, product choice, installation checklist, or provisioning
authority.

One legacy `package.json` example used:

```json
{
  "scripts": {
    "lint": "npm run lint:critical && npm run lint:no-new",
    "lint:critical": "node scripts/lint-critical.mjs",
    "lint:no-new": "node scripts/lint-no-new.mjs",
    "lint:full": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "format": "prettier --write \"src/**/*.{ts,js,json,css}\"",
    "format:check": "prettier --check \"src/**/*.{ts,js,json,css}\"",
    "typecheck": "tsc --noEmit",
    "test": "jest",
    "prepare": "lefthook install"
  }
}
```

For ESLint versions using flat configuration, the legacy note omitted `--ext`
and relied on configuration `files` patterns. Product version, package manager,
script names, command composition, paths, globs, flags, check allocation, hook
installation, and result interpretation must come from canonical decisions;
none of this example is a default.

## Hook Feedback

A local hook can shorten feedback time for formatting, linting, type, or test
failures. That possible benefit does not make a hook stage, product, command,
or check an acceptance requirement. Required evidence remains defined by the
selected verification contract regardless of where the check runs.

## Lefthook Example

Lefthook is one possible language-agnostic hook runner. A project that has
selected it through its canonical tooling and dependency decisions might use
commands such as:

```bash
npm install lefthook --save-dev
curl -sSfL https://get.lh.run | sh
lefthook install
```

These are alternatives from the legacy example, not installation defaults.
Verify the selected installation source, current syntax, trust requirements,
and version policy before use.

An illustrative configuration is:

```yaml
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{ts,js}"
      run: npm run lint {staged_files}
    format-check:
      glob: "*.{ts,js,json,css}"
      run: npm run format:check {staged_files}
    typecheck:
      run: npm run typecheck

pre-push:
  commands:
    test:
      run: npm test
```

The product, stages, parallel mode, globs, commands, and check allocation are
examples only. They do not define a fallback configuration.

## EditorConfig Example

EditorConfig can express selected formatting settings across supporting editors
and IDEs. It is only one possible transport. The canonical
[Tooling workflow](../../workflows/tooling.md#editor-and-file-configuration)
must select the mechanism, settings, scope, and precedence before this sample is
adapted.

```ini
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{js,ts,jsx,tsx,json,css,scss,html,svelte,vue}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

The mechanism, root scope, patterns, indentation, line ending, encoding,
whitespace, final-newline, and file-family values are examples only. They are
not recommended defaults and may conflict with repository or consumer
contracts.

## Linter Category Examples

Teams sometimes group lint checks as style, quality, security, or type checks.
Example products include Prettier or ESLint for style, Pylint or Clippy for
quality, Semgrep or Bandit for security, and TypeScript or mypy for type
analysis. These categories overlap and the products can serve several purposes.

The taxonomy and products are illustrative only. The canonical
[lint policy](../../workflows/tooling.md#lint-policy-and-orchestration) selects
purpose, rules, scope, severity, and tooling from owned facts; it does not infer
them from a category label or this product list.

## TypeScript Tooling Examples

After the canonical [TypeScript profile](../../profiles/languages/typescript.md#static-analysis-and-compiler-configuration)
selects project boundaries and checks, an ESLint flat configuration might scope
type-aware analysis through a `files` block and an owned project configuration:

```javascript
export default tseslint.config({
  files: ['src/**/*.{ts,tsx}'],
  languageOptions: { parserOptions: { project: './tsconfig.json' } },
  extends: [...tseslint.configs.strictTypeChecked],
});
```

Product-specific failure modes can include applying type-aware presets to
non-TypeScript files, mixing ignore declarations into incompatible blocks, or
using command flags unsupported by the selected configuration format.

A formatter configuration used by the same legacy example was:

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

A compiler example might enable `strict`, `noImplicitReturns`,
`exactOptionalPropertyTypes`, or `noUncheckedIndexedAccess`. An architecture
example might implement an owned prohibition through ESLint's
`no-restricted-syntax`. These products, versions, presets, globs, project paths,
flags, severities, and selectors are examples only, not defaults.

### Illustrative React Automatic JSX Lint Adapter

When the selected React runtime, TypeScript contract, lint purpose, and plugin
semantics prove that legacy JSX-scope and runtime prop-validation rules do not
apply, an ESLint adapter might contain:

```javascript
rules: {
  'react/react-in-jsx-scope': 'off',
  'react/prop-types': 'off',
}
```

This snippet does not select React, a React version, the automatic JSX runtime,
TypeScript, ESLint, these plugins, rule disablement, severity, parser, preset, or
validation strategy. A project name or version label cannot replace evidence
that each rule is inapplicable to every selected source and consumer.

## Formatting Automation Examples

After canonical [formatting policy](../../workflows/tooling.md#formatting-policy-and-orchestration)
selects authority and behavior, a VS Code configuration might enable
`editor.formatOnSave` and select a formatter extension. A project using
Prettier and ESLint might install `eslint-config-prettier` to disable overlapping
style rules.

Those editor settings, products, extension identifiers, package commands, and
format-on-save behavior are examples only. They do not select formatting
authority, grant mutation authority, or establish when evidence must run.

A selected Prettier check might use:

```bash
prettier --check "src/**/*.ts"
```

The command, check mode, source glob, and nonzero result interpretation depend
on the selected product version and formatting claim. They are not defaults.

## CI Orchestration Examples

After canonical [CI orchestration](../../workflows/tooling.md#ci-orchestration-and-scheduling)
selects dependencies, continuation, cancellation, and reporting behavior, a
GitHub Actions matrix can express selected continuation with
`strategy.fail-fast: false`. A final reporting job can use `if: always()`, and
an explicitly advisory step can use `continue-on-error: true`.

One possible three-group graph places setup validation before independent
quality checks and runs expensive checks only after their required claims pass.
GitHub Actions can express those edges with `needs` and conditions such as
`success()`. Selected commands might include `./launcher.sh --ci-preflight` or
`npm run ci:preflight`.

The provider, matrix behavior, summary job, error continuation, dependency
syntax, group names, group count, execution order, and commands are examples
only. They do not define a fallback topology or evidence contract.

## Automation Cost Examples

After canonical [automation-cost policy](../../workflows/tooling.md#automation-cost-and-operational-evidence)
selects caching, cancellation, and diagnostics, GitHub Actions can express
read-only contents permission and per-run cancellation:

```yaml
permissions:
  contents: read
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Selected Node and Rust dependency caches might use `actions/setup-node@v4` with
`cache: npm`, or `actions/cache@v4` for Cargo registry and Git data. Commands
such as `npm ci` and `cargo test --workspace`, lockfile-derived keys, exact
compiled-output keys, and broad dependency-download restore keys are
product-specific examples, not defaults.

GitHub failure diagnostics might append a redacted summary to
`$GITHUB_STEP_SUMMARY` and conditionally use `actions/upload-artifact@v4` for
selected log or test-result paths. Artifact names, missing-file behavior, and
retention periods must come from the canonical decision; the legacy example's
14-day retention is illustrative only.

These provider actions, versions, permissions, concurrency expressions, cache
paths, key fields, commands, summary variables, artifact paths, and retention
values cannot select automation behavior or satisfy evidence by themselves.


## Complete CI Workflow Example

This is the complete legacy GitHub Actions example. It is non-normative and may
be adapted only after canonical Tooling and Verification decisions select every
behavior represented by it.

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:
  preflight:
    runs-on: ubuntu-latest
    timeout-minutes: 8
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Preflight
        run: npm run ci:preflight

  lint_critical:
    needs: preflight
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Lint (critical anti-patterns)
        run: npm run lint:critical

  lint_no_new:
    needs: preflight
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm run lint:no-new

  lint_full_audit:
    needs: preflight
    runs-on: ubuntu-latest
    timeout-minutes: 10
    continue-on-error: true
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm run lint:full

  typecheck:
    needs: preflight
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm run typecheck

  format_check:
    needs: preflight
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm run format:check

  test:
    needs: preflight
    timeout-minutes: 20
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm test

  integration:
    needs: [lint_critical, lint_no_new, typecheck, format_check, test]
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm run test:integration

  ci_summary:
    if: always()
    needs: [preflight, lint_critical, lint_no_new, lint_full_audit, typecheck, format_check, test, integration]
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Summarize blocking results
        env:
          PREFLIGHT: ${{ needs.preflight.result }}
          LINT_CRITICAL: ${{ needs.lint_critical.result }}
          LINT_NO_NEW: ${{ needs.lint_no_new.result }}
          TYPECHECK: ${{ needs.typecheck.result }}
          FORMAT_CHECK: ${{ needs.format_check.result }}
          TEST: ${{ needs.test.result }}
          INTEGRATION: ${{ needs.integration.result }}
        run: |
          failures=0

          for gate in PREFLIGHT LINT_CRITICAL LINT_NO_NEW TYPECHECK FORMAT_CHECK TEST INTEGRATION; do
            result="${!gate}"
            echo "- ${gate}: ${result}" >> "$GITHUB_STEP_SUMMARY"
            if [ "$result" = "skipped" ]; then
              echo "  - Skipped because an upstream tier did not pass." >> "$GITHUB_STEP_SUMMARY"
            fi
            if [ "$result" != "success" ]; then
              failures=1
            fi
          done

          exit "$failures"
```

The workflow path, provider, triggers, permissions, jobs, gates, action versions,
caches, commands, timeouts, matrices, dependencies, summaries, and shell logic
are examples only and define no fallback.
````

### profile.boundary.generated-contract

````markdown
# Generated Contract Boundary Profile

**Standards metadata**

- ID: `profile.boundary.generated-contract`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A schema or generator produces program-facing models, validators, tool definitions, bindings, configuration, or another consumed representation.
- Does not apply when: Generation produces no representation interpreted by a program consumer, or the change preserves the generated contract and all of its consumers unchanged.
- Requires: `core`, `workflow.verification`, `workflow.build`, `topic.contracts`, `topic.dependencies`, `topic.contracts.schemas`
- Specializes: `topic.contracts`
- Verification: Generated-contract routing, semantic-conformance, freshness, public-consumer, unsupported-domain, and reconstruction evidence.
- Canonical owner: `profiles/boundaries/generated-contract.md`

## Applicability

Select this profile when a canonical declaration and generator or compiler
produce a representation that a program consumes as models, validation,
dispatch, tool definitions, bindings, configuration, or another executable
contract. Generated documentation, reports, or copied data do not select it
unless a program consumer relies on their generated representation.

Select the Language Binding profile only for a genuine native/host or
cross-language representation. Select IPC only for a process, message,
plugin-host, or independently deployed boundary. Select Persistence only for
durable generated or consumed state. The presence of serialization, another
language in the repository, or a checked-in output does not establish those
additional boundaries.

Missing consumer or boundary facts leave routing `unavailable`; contradictory
facts are `invalid`. Do not route to a smaller contract profile when required
applicability facts are unresolved.

## Semantic Closure

Apply the complete generated-contract semantics owned by Contracts. Record the
canonical declaration, exact dialect and vocabulary, supported semantic
surface, generator and executable semantics owners, reachable public
operations, generated outputs, and actual producer and consumer entry points.
Also record the declaration's authority scope, independently changing semantic
owners it references, and each version's compatibility and material
invalidation scope. A declaration may project or invoke independently owned
semantics; generation does not transfer those authorities to the declaration
or justify one umbrella version.

Build owns deterministic derivation and stale-output rejection. Verification
owns claim and oracle sufficiency. Dependencies owns the decision to adopt an
established implementation or maintain difficult standardized semantics
locally. This profile specializes their application to the generated boundary;
it does not duplicate their policy.

Acceptance distinguishes source freshness, shape agreement, semantic
conformance, and public consumer behavior. It includes explicit rejection of
unsupported source behavior and uses an independent reference or official
corpus when several local implementations interpret an external contract.
Generated output, copied expectations, or agreement among local projections
cannot be the sole semantic oracle.

Return `invalid` for incomplete reachable closure, stale output, contradictory
semantics, or incomplete producer/consumer proof; `unsupported` for a
well-formed source construct outside the declared support set; and
`unavailable` when required declaration, generator, consumer, oracle, or
dependency-decision authority cannot be obtained. Do not partially generate,
silently omit semantics, or fall back to inferred consumer shape.

## Composed-Design Projection

Generation may make authoring easy without making the produced artifact simple.
For this profile, the produced artifact includes the generated Interface, its
consumers, the generator, runtime interpretation, and compatibility and
invalidation promises. Automating their coordinated propagation does not prove
that they can change independently.
````

### workflow.verification.platforms

````markdown
# Platform Verification

**Standards metadata**

- ID: `workflow.verification.platforms`
- Role: `workflow`
- Level: `MUST`
- Applies when: A claim spans supported targets or requires platform-specific evidence.
- Does not apply when: The claim has no target-specific behavior or supported-platform evidence obligation.
- Requires: `workflow.verification`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `workflows/verification/platforms.md`

## Platform Evidence Coverage

For each declared platform-support claim, record every required target or
environment and map it to the evidence kind, environment qualification,
execution mode, and observed result that prove that claim. Required behavior
must be evidenced on every target whose real behavior is part of the support
contract. A build, simulation, or result from one target does not prove
different target behavior.

Best-effort and unsupported targets remain explicit and cannot satisfy a
required target entry. A best-effort failure may leave the required claim
accepted only when the support contract makes that target genuinely optional
and the result is still recorded.

Select local hooks, push or review checks, hosted or self-managed runners,
provider matrices, dedicated hardware, release gates, and manual procedures
from risk, cost, target availability, credentials, and release facts.
Failure fan-out and early termination are orchestration decisions; neither
`fail-fast` setting is universal. Different environments may use different
commands when they prove the same declared claim.

If any required target result is missing, failed, or blocked, acceptance
remains blocked. Contradictory support/evidence mappings are invalid, an
explicitly unsupported target is unsupported, and missing support, target,
environment, scheduling, or orchestration facts are unavailable.

Do not infer Linux and Windows, substitute current-platform compilation,
weaken a required target to best-effort, copy a provider matrix, or impose a
fixed pre-commit, pre-push, push, or pull-request schedule as fallback.
````

### topic.resilience

````markdown
# Resilience

**Standards metadata**

- ID: `topic.resilience`
- Role: `topic`
- Level: `MUST`
- Applies when: A dependency, service, resource, or startup condition can fail and the product must choose whether to fail, retry, degrade, or remain unavailable.
- Does not apply when: No failure condition affects an operation, lifecycle, resource, or user-visible outcome.
- Requires: `core`, `workflow.verification`, `topic.contracts`
- Specializes: `none`
- Verification: Resilience decision fixtures plus affected startup, dependency, retry, degradation, and recovery tests.
- Canonical owner: `topics/resilience.md`

## Failure And Recovery Authority

Select one owner for the complete failure and recovery contract at each
applicable boundary. The contract names the dependency or resource, the
operation and lifecycle phase, criticality, retry or degradation semantics,
observable outcome, recovery authority, and evidence required to accept the
behavior. A failure category, retry count, timeout, or best-effort label is not
an independent policy authority.

Return typed `invalid` for contradictory criticality, recovery, or outcome
facts; return typed `unsupported` when a declared resilience mode is outside
the selected contract; and return typed `unavailable` when required
dependency, recovery, or evidence capability cannot be established. Do not
continue with an unowned failure, silently ignore it, or claim recovery from
logging alone.

## Failure Classification And Decision

Classify a failure from authoritative facts about the dependency, operation,
lifecycle phase, state ownership, selected degraded outcome, and available
recovery capability. Labels such as corrupt, unavailable, stale, external,
required, or optional describe evidence; they do not select a recovery action
by themselves.

Apply this decision order:

1. Establish whether the dependency is required or best-effort for the current
   operation and lifecycle phase.
2. Establish whether affected state is authoritative, disposable derived state,
   or unknown.
3. Select the declared terminal, degraded, retry, or reconstruction outcome.
4. Prove retry safety, reconstruction authority, and required evidence before
   executing that outcome.
5. Return the selected result or typed diagnostic without changing mechanisms.

## Criticality And Degradation

Classify a dependency as required or best-effort from the operation and
product contract. Required failures preserve the declared failure outcome;
best-effort behavior is valid only when the contract defines the degraded
semantics, user-visible impact, observability, and recovery obligations.
Startup checks and steady-state handling may differ only when the lifecycle
contract declares that distinction.

Do not turn an unavailable required dependency into success, substitute an
empty or stale value, skip a required startup check, or apply best-effort
handling because a default is convenient. A degraded result is not a generic
fallback; it is a selected contract outcome with evidence.

## Startup Resilience

Make startup decisions from the startup lifecycle contract rather than from a
universal dependency category. A required startup capability that cannot be
established prevents readiness with a typed diagnostic. A best-effort
capability permits startup only when the accepted contract defines the
degraded service surface, health state, user-visible impact, observability, and
later recovery authority.

Do not infer that databases and configuration are always required or that
caches, indexes, analytics, telemetry, and logging sinks are always optional.
Do not report readiness while a required capability is unavailable.

## Best-Effort Dependency Boundaries

A best-effort adapter returns the explicitly selected degraded result. It
preserves the distinction between absence, unavailable capability, invalid
state, unsupported behavior, and a successful value. Catching an arbitrary
failure and returning no value, an empty value, stale data, cached data,
partial output, or success is not a best-effort contract.

The adapter records health and recovery evidence without becoming the owner of
the dependency's authoritative state or the caller's operation semantics.

## Retry And Recovery

Retry only when the operation is eligible, the retry authority is selected,
the attempt and time budgets are bounded, and repeated execution is safe under
the operation's idempotency contract. Recovery may retry, reinitialize,
degrade, or fail according to the selected contract; it must not switch to an
alternate dependency or unbounded loop when the selected mechanism is missing.

Record attempts, terminal outcome, cancellation, and recovery evidence at the
owner that controls the operation. Typed diagnostics preserve the distinction
between failed, unavailable, unsupported, and successfully degraded outcomes.

### Remote Retry Budgets And Unknown Outcomes

For a remote operation, give one layer responsibility for retries. Bound the
whole operation with an end-to-end deadline, including queueing, attempts, and
backoff; a per-attempt timeout alone does not bound user latency. Propagate the
remaining budget and cancellation to downstream work. Avoid multiplying
retries at several layers. Use capped backoff with jitter for transient shared
failures, honoring valid service retry hints within the remaining budget.

A timeout after sending a mutation can mean the effect committed but its reply
was lost. Treat that as an unknown outcome, not proof of failure. Reconcile
through an operation identifier or retry under an idempotency contract before
attempting the effect again. Test lost replies and exhausted deadlines as well
as ordinary transient failures.

### Idempotency Records

When duplicate delivery can repeat an effect, define the key's scope (such as
caller, operation, and resource), bind it to the request's meaning, and reject
reuse with conflicting input. Record the deduplication result and effect in one
atomic boundary where possible. If they cross systems, use an explicit durable
coordination protocol and reconciliation; a local cache does not make the
remote effect atomic. Define how long records are retained relative to the
supported retry window and what happens after expiry. Test concurrent duplicate
requests, conflicting input, interrupted writes, and expiry.

### Time Semantics

Distinguish an elapsed duration, a deadline, an instant, and a civil date/time.
Use a monotonic clock for in-process elapsed budgets; a wall clock can jump.
Do not persist or transmit a process-local monotonic timestamp as a portable
instant. For cross-process deadlines, define clock-skew assumptions and bound
the local remaining budget. Calendar schedules need a timezone and a policy
for ambiguous or missing civil times. Use controllable clocks in tests when
timing affects correctness rather than relying on sleeps.

## State Reconstruction

Delete, replace, seed, or rebuild state only when the Contracts owner proves
that the affected state is disposable derived state and identifies a complete
authoritative reconstruction source. Corrupt or unavailable authoritative
state remains intact for diagnosis or explicit recovery; it is not converted
to defaults or silently replaced.

Cold-start and lazy-rebuild behavior is valid only as a selected reconstruction
contract. A missing cache does not authorize stale reads, alternate stores, or
weaker evidence.

## Replay And Resumption Evidence

When durable commands, events, projections, workers, retries, or reconnects can
repeat or resume work, declare the authoritative history or checkpoint, replay
boundary, duplicate identity, idempotency contract, projection convergence
rule, partial-failure state, and condition permitting new work to resume.

Evidence exercises the real persistence and execution boundaries applicable to
the claim. It proves bootstrap or replay from authoritative state, duplicate
request handling, projection convergence after recovery, worker or connection
resumption from the selected position, and repair or rejection of partial work
before later work proceeds. A pure helper, successful restart, empty-state
bootstrap, log message, or final snapshot without the transition path does not
prove recovery.

Return `invalid` when replay, duplicate, convergence, or resume facts
contradict the operation contract; `unsupported` when the requested recovery
mode is outside the declared contract; and `unavailable` when authoritative
history, checkpoint, persistence, execution boundary, or required evidence
cannot be obtained. Do not restart from an inferred position, discard or
reapply unknown work, reset authoritative state, continue after unproven
partial failure, or substitute a helper-only or weaker recovery path.

## Acceptance Evidence

Verification covers required and best-effort behavior at startup and runtime,
bounded retry and cancellation, degraded result shape, health transitions,
terminal diagnostics, reconstruction authority, replay, duplicate handling,
projection convergence, resumption, partial-failure repair, and recovery. Availability
claims must match the service surface that remains valid during degradation.

## No Fallback

Missing facts or capability cannot select a default retry policy, timeout,
dependency, empty result, stale result, ignored error, alternate mechanism,
or silent degradation. Unknown recovery behavior remains a typed diagnostic.

## Failure Boundaries And Diagnostics

Select exception, result, status, event, or terminal mechanisms from the
language and operation contract. Handle or translate failure at the narrowest
boundary owning recovery, a public outcome, or diagnostics. Preserve original
causes and typed classification; do not catch, log, wrap, or rethrow at every
layer.

Diagnostics carry bounded, non-sensitive context required by the selected
operator or consumer claim. Channel, correlation, detail, sampling, and
retention belong to the application's diagnostic owner. Do not mandate logging,
tracing, exceptions, correlation IDs, or one boundary list.

Contradictory classification or authority is typed `invalid`; missing required
cause, owner, context, or diagnostic capability is typed `unavailable`. Do not
replace failure with a default, guessed class, duplicate log, context-free
wrapper, swallowed outcome, or successful fallback.
````

### topic.diagnostics

````markdown
# Diagnostics

**Standards metadata**

- ID: `topic.diagnostics`
- Role: `topic`
- Level: `MUST`
- Applies when: A change creates or changes diagnostic context, causal identity, reporting, propagation, retention, sampling, redaction projection, or a diagnostic claim.
- Does not apply when: The change affects no diagnostic behavior or claim and preserves every selected diagnostic contract unchanged.
- Requires: `core`, `workflow.verification`, `topic.contracts`
- Specializes: `none`
- Verification: Diagnostics owner and activity-context decision fixtures plus claim-matched producer, consumer, disclosure, lifecycle, and failure evidence.
- Canonical owner: `topics/diagnostics.md`

## Diagnostic Authority

Diagnostics projects information about an operation or outcome for a selected
consumer or operator. Record the diagnostic purpose, audience, owning operation
or event, required context, disclosure authority, lifecycle, destination, and
evidence before selecting a mechanism.

A typed business or protocol outcome remains owned by its contract. Emitting a
diagnostic does not classify, handle, recover, retry, suppress, or convert that
outcome and cannot replace returning it to the responsible caller.

## Diagnostic Selection

Select a diagnostic only when an accepted operator, consumer, verification, or
support claim requires observable information beyond the owned result. Select
its channel, detail, timing, sampling, and retention from that claim and the
available application and operational capabilities.

Logging, tracing, metrics, events, status surfaces, exceptions, and persisted
records are possible projections, not universal requirements or substitutes.
Success through one channel does not prove another channel or the underlying
operation.

## Causal Identity And Context

Use operation, event, parent, or correlation identity only when the selected
workflow requires observations to be associated across applicable boundaries.
Define creation, propagation, uniqueness, scope, invalidation, and terminal
behavior from that workflow. Do not generate or forward correlation identifiers
merely because multiple layers exist.

An activity context contains only the selected identity and bounded fields
needed to connect those observations. Create child identity only for a selected
causal child operation, preserve the declared parent relationship across each
applicable boundary, and reject absent, malformed, reused, or contradictory
identity according to the owning contract. A single-boundary operation does not
need correlation merely to satisfy a tracing shape.

Carry only bounded context required by the selected audience and claim. Field
availability does not authorize disclosure. Apply Security authority before
including sensitive data and preserve the selected redaction at every
projection and transport boundary.

## Lifecycle And Failure

Define which start, progress, completion, failure, cancellation, retry, and
recovery observations are required. Emit each selected terminal observation
once at the boundary that owns the diagnostic projection; do not report the
same failure independently at every layer.

Propagation follows the operation lifecycle, including asynchronous completion,
cancellation, retries, and handoff when those states apply. A synchronous
wrapper, lexical scope, thread-local value, or request lifetime does not prove
that context remains valid through another lifecycle.

Specify diagnostic channel failure, buffering, backpressure, recursion,
shutdown, and retention behavior where applicable. A failed diagnostic channel
does not change the operation outcome or authorize a successful diagnostic
claim.

## Responsibility Boundaries

Contracts owns outcome meaning. Resilience owns failure handling and recovery.
Security owns sensitive-data authority. Performance owns performance claims.
Verification owns evidence sufficiency. Tooling owns collection, storage, and
orchestration mechanisms. Application, boundary, language, and framework
profiles own their accepted adapters.

Diagnostics owns only the generic projection contract and does not mandate a
telemetry product, fixed application layers, correlation model, transport,
storage system, or language mechanism.

## Typed Outcomes

Return `unavailable` when required purpose, audience, authority, context,
propagation, redaction, destination, or capability cannot be established;
`invalid` for contradictory context, unsafe disclosure, broken causal identity,
duplicate terminal reporting, or a false diagnostic claim; and `unsupported`
when the selected mechanism cannot represent a supported diagnostic contract.

Do not fall back to raw context, guessed identity, duplicate logs, swallowed
outcomes, a nearby channel, silent discard, or reported success without the
selected diagnostic evidence.
````

### workflow.documentation

````markdown
# Documentation Workflow

**Standards metadata**

- ID: `workflow.documentation`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change creates or alters a durable responsibility, decision, contract, or operational boundary.
- Does not apply when: A change preserves documented responsibilities, decisions, contracts, and operational procedures.
- Requires: `core`
- Specializes: `none`
- Verification: Documentation decision, policy consolidation, and traceability checks.
- Canonical owner: `workflows/documentation.md`

## Select Documentation From Impact

Durable documentation is required when a reader must understand information
that source code and tests do not own clearly enough:

- why a meaningful module or operational boundary exists;
- which responsibility and invariants that boundary owns;
- what consumers rely on across a public, process, language, persistence, or
  generated-artifact boundary;
- why a consequential decision was selected; or
- how an operator must perform or recover a non-obvious procedure.

Directory count, file count, and the presence of a `src/` path are not
documentation requirements. A local implementation change that preserves all
documented decisions and contracts requires tests and code review, not an
unrelated README or ADR edit.

## Documentation Profiles

Select the smallest profile that preserves the affected knowledge:

| Profile | Select when | Required content |
| --- | --- | --- |
| `none` | The change preserves durable responsibilities, invariants, decisions, contracts, and procedures. | No documentation artifact. |
| `boundary-readme` | A meaningful module or operational boundary is created or its responsibility/invariants change. | Purpose, owned responsibility, invariants, entry points, and applicable links to accepted decisions or contracts. |
| `contract-readme` | Consumers need stable behavior at a public, process, language, persistence, or generated-artifact boundary. | Boundary README plus inputs/outputs, lifecycle, failures, compatibility or migration, and producer/consumer ownership. |
| `adr` | A durable decision crosses boundaries, has material alternatives, or must outlive the implementation plan. | Context, decision, alternatives, consequences, status, affected boundaries, and supersession links. |
| `runbook` | Operators need a repeatable deployment, recovery, migration, or incident procedure. | Preconditions, steps, validation, failure handling, rollback or repair, and owner. |

More than one profile may apply. When an ADR or contract document owns the
rationale, a README links to that owner and summarizes only the local
responsibility. Do not copy the full decision into every artifact.

If the impact cannot be classified, record an unresolved documentation
diagnostic. Do not create a speculative README or ADR as a fallback.

## Artifact Placement

Follow the adopting repository's documented placement and naming convention.
When no convention exists:

- keep boundary-owned documentation with the boundary;
- place project-level decisions, plans, and reports under a root `docs/`
  directory with concern-specific subdirectories; and
- group multi-file work under one descriptive, lowercase, hyphenated slug.

The artifact's owner and links must remain unambiguous. Do not scatter one work
item across unrelated roots, reorganize unaffected documentation to satisfy
this default, or retain an obsolete layout as a compatibility fallback. A
layout replacement updates affected links and automation in the same accepted
change.

## Boundary README

A boundary README is concise and specific. It contains:

- `Purpose`: why the boundary exists;
- `Responsibility`: behavior and state owned here, plus explicit exclusions;
- `Invariants`: conditions that must remain true;
- `Entry Points`: the interfaces or commands a reader should start from.

Add `Consumer Contract` or `Produced Contract` only when that contract exists.
Add `Decision Links` only when accepted rationale or a canonical contract
exists. Add operational instructions only when the boundary owns them. Omit
non-applicable sections instead of filling them with `None`, generic prose, or
invented alternatives.

## Repository Entry Point

When a repository is independently adopted, operated, or contributed to, its
root README is the discovery boundary. It states:

- the repository's purpose and intended audience;
- stable commands or interfaces needed to start;
- the minimum verified setup and use path for that audience; and
- links to owned contribution, operation, contract, decision, and license
  documents when those concerns apply.

Select sections from actual audience needs. Do not require a fixed heading
list, duplicate detailed owner documents, or maintain a file-by-file project
tree. Update the entry point when these facts change; unrelated implementation
changes require no root README churn.

## Contract Documentation

Contract documentation states the facts a consumer needs:

- input and output semantics;
- validation and typed failure outcomes;
- lifecycle, ordering, cancellation, idempotency, and retry behavior;
- compatibility, versioning, migration, or coordinated replacement policy;
- producer and consumer ownership; and
- verification evidence or executable contract location.

Follow [Contract Evolution](../topics/contracts.md). Unknown contract facts
remain diagnostics; documentation must not invent defaults or compatibility.

## Decision Traceability

Update durable documentation only when its owned knowledge changes:

- update the affected boundary README when responsibility or invariants change;
- update the canonical contract when consumer-visible semantics change;
- add or supersede an ADR when a durable cross-boundary decision changes; and
- update a runbook when its procedure or recovery semantics change.

Every ADR identifies affected boundary paths or stable contract identifiers.
An unrelated ADR cannot satisfy traceability for a changed boundary.

Plans and pull requests link to accepted rationale. They may summarize the
current change, but they do not become duplicate long-term owners.

When automation enforces traceability, select its impact mapping from
project-owned trigger paths or stable contract identifiers, the exact durable
knowledge each trigger can change, the canonical artifact that owns that
knowledge, and the accepted documentation profile. A broad directory may be a
trigger only when every relevant change beneath it affects the same owned
knowledge. Routine implementation paths do not acquire documentation
obligations from location alone.

Each invocation must identify the exact change input it evaluates. Staged mode
evaluates only index state. Range mode requires explicit base and head revisions and
evaluates both prior and current mapping state so deleting a trigger or map row
cannot hide an obligation. A changed artifact satisfies only its mapped boundary
or stable contract; an unrelated README, ADR, plan, or pull request is not a
substitute.

Do not default to a `src/` directory, README per directory, fixed headings,
placeholder content, one map location, staged or range mode, a branch name,
adjacent revisions, or a documentation artifact. Contradictory trigger,
boundary, profile, or artifact authority is `invalid`. Missing maps, modes,
revisions, paths, or canonical artifacts are `unavailable`. An enforcement
mechanism unable to evaluate the selected repository state or prior mapping is
`unsupported`; do not infer a diff, broaden the map, accept unrelated artifacts,
or silently skip unresolved inputs.

## Quality Rules

- Write project-specific information that cannot be inferred from names alone.
- Keep contents lists limited to stable entry points, not every file.
- Keep examples aligned with real public entry points.
- Remove or supersede stale decisions; do not append competing authority.
- Treat generated documentation as derived output and update its source in the
  same change.
- Verify links and any executable examples affected by the change.
````

### workflow.build

````markdown
# Build Workflow

**Standards metadata**

- ID: `workflow.build`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change selects or changes a build-time action, authoritative build input, produced or generated output, invalidation rule, build environment access, native build integration, or deterministic-build requirement.
- Does not apply when: The task only consumes an unchanged build artifact or runs an unchanged build procedure without changing its contract.
- Requires: `core`, `workflow.implementation`, `workflow.verification`
- Specializes: `none`
- Verification: Build-action contract decisions plus affected input, output, invalidation, side-effect, environment, determinism, and consumer evidence.
- Canonical owner: `workflows/build.md`

## Build Authority

Authorize a build-time action from an owned artifact, consumer, target,
generation, dependency, or release contract. Identify the owner that may add,
change, or remove the action and the lifecycle phase in which it executes. A
build-system feature, existing script, ecosystem convention, successful build,
or convenience does not create authority.

Build owns the action contract, not the content contracts it consumes.
Contracts owns generated representation authority, Dependencies owns external
requirements, Cross-Platform owns target and capability facts, Security owns
untrusted authority and supply-chain risks, Release owns released artifacts and
reproducibility claims, and Tooling owns automation orchestration. Language and
build-system profiles express accepted decisions through supported mechanisms.

## Inputs, Outputs, And Side Effects

Name every authoritative input, produced output, consumer, permitted side
effect, and write boundary. Distinguish source inputs, generated intermediates,
final artifacts, diagnostics, caches, and metadata. An output path, environment
variable, compiler convention, or prior generated file cannot become authority.

Write only within the selected build output boundary unless another owner
explicitly authorizes a source change. Generated output follows the canonical
producer and consumer contract; do not hand-edit it, infer its source from the
output, or write into source merely because a tool supports that location.

## Invalidation And Incrementality

Derive rerun and invalidation inputs from every fact that can change the
observable output or required side effect. Include source, configuration,
environment, toolchain, dependency, target, and generator facts only when they
are material to the selected action.

Do not default to always rerun, never rerun, timestamps, directory-wide watches,
the current manifest, or a conventional directive list. A cache or incremental
result is valid only when its key and invalidation boundary cover all
authoritative inputs and exclude undeclared mutable state.

## Environment And External Effects

Declare required filesystem, process, environment, network, credential,
toolchain, compiler, and system-library access. Select build-time discovery only
when the accepted contract requires facts before artifact construction and the
result can be reproduced or intentionally qualified for the target claim.

Do not move runtime capability detection into the build, invoke a raw compiler,
access the network, inherit ambient environment state, or execute downloaded
content by convention. Missing required access or capability retains a typed
outcome; it does not authorize another command, dependency, detection phase, or
cached result.

## Determinism And Reproducibility

Derive determinism from the affected artifact and release claims. Control every
material nondeterministic input required by those claims, including time, paths,
ordering, locale, randomness, environment, network results, and tool versions.
Determinism of one generated file does not prove a reproducible released
artifact, and a pinned tool does not prove deterministic output.

Do not default to a timestamp variable, source-date convention, clean build,
lockfile, or byte-for-byte claim. When the required determinism cannot be
established, return the applicable typed outcome rather than relabeling the
artifact or accepting an unverified build.

## Typed Outcomes

Contradictory authority, input, output, consumer, side-effect, invalidation,
environment, target, or determinism facts are `invalid`. A well-formed action
outside supported build, platform, or toolchain capability is `unsupported`.
Missing authority, material input, output owner, consumer, invalidation fact,
access, capability, or evidence is `unavailable`.

Do not fall back to an existing script, conventional purpose, source-tree
output, broad rerun, raw compiler, runtime or build-time detection swap,
ambient environment, timestamp convention, minimal dependency set, successful
no-op, or default success.

## Verification

Evidence covers the accepted action and phase, authoritative inputs, produced
outputs and consumers, write boundary and side effects, invalidation behavior,
qualified environment and target, deterministic properties, typed failures,
and every changed producer-consumer path. Build success proves only that the
selected invocation exited successfully.
````

### workflow.commit

````markdown
# Commit Workflow

**Standards metadata**

- ID: `workflow.commit`
- Role: `workflow`
- Level: `MUST`
- Applies when: A repository change will be committed, local history maintenance is requested, or branch/worktree isolation, integration, lifecycle assessment, or cleanup is being decided or performed.
- Does not apply when: Work is read-only and requires no commit, history, branch, or worktree lifecycle decision.
- Requires: `core`, `workflow.implementation`
- Specializes: `none`
- Verification: Commit authority fixtures and staged-scope review.
- Canonical owner: `workflows/commit.md`

## Per-Commit Boundary

Before every commit:

1. inspect repository status;
2. confirm only the declared slice write set is staged;
3. review the staged diff, generated-file effects, and sensitive-file risk;
4. confirm credentials, secrets, personal configuration, and unintended binary
   artifacts are absent;
5. run the focused and affected verification selected for the slice;
6. update active plan, issue, or ledger state only when current authority,
   lifecycle, blockers, acceptance, next-slice state, an accepted-slice
   boundary, a material deviation, or a material verification result changes;
   do not mirror commit cadence into planning artifacts; and
7. create one atomic conventional commit that describes the coherent outcome.

Per-commit review concerns the index and the current slice. Do not require a
full unpushed-history audit before every atomic commit.

## Branch And Worktree Applicability

Do not require a branch or worktree for every change. Use one when it provides
material isolation for review, concurrent proposals, experimentation, release
maintenance, risk containment, or repository-required checks. The current
integration owner may work directly on the integration branch for a small
serial change when repository controls allow it and no outstanding proposal can
become stale.

Select isolation from those facts, not from file count, commit count, elapsed
time, branch count, worktree count, or a preferred Git ceremony. Preparing work
in another worktree does not make cherry-pick the default integration method.

## Governed Branch Context

For governed branch work, retain enough context to resolve:

- purpose and responsible owner;
- target or integration branch;
- admitted base or revision when concurrency makes it relevant;
- whether the branch is private, shared, or long-lived;
- integration owner; and
- expected terminal disposition.

Use the task, branch name, repository history, plan, pull request, or another
owned artifact that already contains these facts. Do not require a heavyweight
record for a trivial private branch when its name, task, and history make the
contract unambiguous. Missing facts that affect safe integration or cleanup are
`unavailable`; contradictory ownership or target facts are `invalid`.

## Integration Mechanism Selection

Use the least history-transforming mechanism compatible with the accepted
outcome:

- Fast-forward a complete accepted branch when it descends from current target
  authority.
- For a complete private proposal based on stale target authority, an
  authorized owner may rebase it onto fresh authority, resolve conflicts,
  reverify the result, and then fast-forward it.
- Create a merge commit when preserving branch topology has durable review,
  release, or repository value.
- Cherry-pick for selective acceptance, backports, recovery, or another case
  where integrating the complete branch is inappropriate.

Do not cherry-pick merely because work was prepared in another worktree. Do
not rewrite shared or published history without separate explicit authority.
When facts do not support one mechanism, return a history-integration
diagnostic instead of trying another mechanism as fallback.

## Cherry-Pick And Replacement Lineage

When cherry-pick or reconstruction creates a replacement commit, record the
source branch, source commit, accepted replacement commit, integration mode,
verification result, and terminal branch disposition in durable acceptance
evidence. Git ancestry reporting a source commit as unmerged does not prove
that a patch-equivalent accepted replacement remains semantically unintegrated.

Patch equivalence may trigger review, but automated retirement requires an
explicit source-to-accepted mapping. Do not infer acceptance from matching
diffs alone.

## Terminal Branch Lifecycle

Classify every short-lived governed branch or proposal as `integrated`,
`rejected`, `abandoned`, `superseded`, or retained under an explicit long-lived
contract. A retained long-lived branch states its continuing purpose, owner,
synchronization policy, supported consumers, and retirement condition.

Branch refs and worktrees are operational resources, not permanent evidence
databases. Preserve durable rationale and acceptance evidence in commits, pull
requests, issues, plans, ledgers, manifests, or reports. Do not retain a
redundant branch solely to preserve history that durable evidence already owns.

## Worktree Lifecycle And Cleanup Authority

Remove a completed clean worktree when its purpose ends, and prune stale
administrative registrations only after confirming that no live worktree owns
them and resolving the registered head's commit disposition. A detached
worktree registration can be the only local reachability root for its head;
missing paths and unlocked registrations do not prove that pruning is safe.
Never force-remove a dirty, unknown, user-owned, locked, or uniquely committed
worktree through generic automation. Removing a redundant branch ref is not
the same operation or authority as rewriting history reachable by shared refs.

Before worktree removal or registration pruning, record the exact head OID and
classify its reachability as `retained-ref`, `registration-only`, or `unknown`.
Select exactly one commit disposition:

- `retained`: the resource remains or the OID is reachable from a named retained
  ref;
- `archived`: an exact recovery or archive ref has been created and verified
  before the registration is removed; or
- `discard-authorized`: separate destructive authority names every commit that
  may become unreachable and records permanent retirement.

Unknown reachability, a registration-only head without verified archive
protection, or a missing commit disposition refuses cleanup. Do not select a
different disposition as fallback.

The integration owner may perform predeclared safe cleanup for branches and
worktrees created by the governed task after terminal evidence is recorded.
Delegated workers must not delete resources outside their declared ownership.
Automation may retire a branch only when ownership, integration, and terminal
evidence are unambiguous. Patch-equivalent or cherry-picked branches require
the source-to-accepted mapping before automated retirement. Age and quantity
may trigger review but never independently authorize deletion.

When a governed task creates a worktree, terminal acceptance records its exact
path, head reachability, commit disposition, and one explicit outcome:
`removed-reachable`, `removed-archived`, `retained-protected`, or
`discard-authorized`. It then confirms either that the path and stale
registration are absent from `git worktree list` after safe removal or that an
explicit retained-resource contract names its purpose, owner, and next
disposition. A task-created registration that remains without that contract,
or was removed without accepted commit protection, is `unavailable` for
terminal acceptance. Check only paths created by the task; this postcondition
does not authorize a repository-wide prune or cleanup of historical, unknown,
or other-owner registrations.

For any cleanup batch that can remove a commit reachability root, capture the
exact protected-OID set before mutation and compare it with retained or archive
refs after mutation. Every protected OID must still exist and satisfy its
recorded disposition. Repository object-integrity checks, including
`git fsck --no-dangling`, do not prove continued reachability and cannot replace
this comparison.

Discarding unique commits from a rejected or abandoned branch requires
separate explicit destructive authority naming the branch and unique commits,
confirming they are not accepted, shared, or otherwise required, and recording
the selected recovery or permanent-retirement outcome. Generic cleanup
automation must refuse that operation; rejection alone is not discard
authority.

## Branch-History Review

Review the complete branch range at boundaries where its sequence matters:

- milestone or implementation-wave closure;
- pre-push;
- pull-request preparation or update;
- release preparation; or
- an explicit history-maintenance request.

Use an explicit intended base and inspect the commit graph, staged/unstaged
state, and cumulative diff. Identify accidental regressions followed by fixes,
misleading boundaries, fixup commits, and unintended merge topology.

History review produces findings. It does not itself authorize rewriting.

Automation may remind an operator to perform a selected history review and may
report the explicit range, graph, or cumulative diff. It must not infer the
intended base, decide that cleanup is required, or run amend, rebase, reset,
squash, commit-dropping, or topology-changing commands. Missing range or base
facts produce a typed process diagnostic.

## Hook Bypass Authority

Bypassing a repository hook skips an automation mechanism; it does not waive
the underlying implementation, verification, security, or commit obligation.
Permit bypass only when an explicitly authorized procedure identifies the
affected hook, change scope, reason, unmet checks, risk owner, compensating
evidence or containment, and required follow-up.

Record the bypass in the durable location selected by that procedure. A commit
message, emergency label, production incident, tool failure, or operator
urgency does not grant authority by itself. Do not default to a bypass command,
`no-verify` flag, emergency exception, successful no-op, or later repair.

When bypass authority, scope, or required evidence is missing or contradictory,
return a typed process diagnostic and leave the hook enabled. When the selected
procedure cannot be executed in the repository or toolchain, report the
unsupported mechanism rather than silently committing through another path.

## Rewrite Authority

Rebase, amend, reset, squash, commit dropping, and merge-topology rewriting
change existing history. Perform them only when all conditions hold:

- the maintainer or user explicitly authorized the rewrite and its scope;
- the exact commit range and intended base are known;
- every affected commit is confirmed unshared and unpushed;
- no collaborator, worktree, automation, or dependent branch relies on the
  existing commit IDs;
- the original tip is preserved in a named recoverable Git reference;
- the worktree and index state are understood and preserved; and
- affected verification will be rerun after the rewrite.

If any fact is unknown, return a history-maintenance diagnostic and leave the
existing commits intact. Never infer rewrite authority from a request to
implement, commit, clean up, or prepare a pull request.

Shared or pushed history is immutable under this workflow. Correct it with a
new atomic commit unless the repository owner invokes a separate,
explicitly-governed emergency procedure.

## Topology

Linear-history cleanup and merge-topology rewriting are different operations.
When an authorized range contains merges:

- preserve or intentionally replace integration semantics;
- use merge-aware tooling;
- inspect the graph before and after;
- verify every retained parent relationship; and
- stop if the intended topology is ambiguous.

Do not flatten merges as a default cleanup strategy.

## Commit Message

Use the repository's conventional commit format. The subject states the
observable change concisely in imperative mood. The body explains material
rationale, scope, and contract effects when the subject is insufficient.

Keep command logs and verification output in the plan ledger, pull request, or
completion record rather than the commit message.

See the non-normative [Commit Recipe](../reference/recipes/commits.md) for
syntax, staging commands, footer forms, and examples.

## Invalid Outcomes

Stop with a typed process diagnostic when:

- unrelated dirty files overlap or make staged scope ambiguous;
- required verification did not pass;
- the intended base or commit range is unresolved;
- rewrite authority or unshared status is missing;
- recovery of the original history is not established; or
- the requested rewrite would alter shared history;
- branch purpose, target, ownership, or terminal evidence needed for the
  selected operation is unavailable;
- a task-created worktree remains registered without an explicit retained-
  resource contract;
- worktree removal or registration pruning lacks an exact head OID,
  reachability classification, commit disposition, or protected-OID
  postcondition;
- a replacement commit lacks source-to-accepted lineage; or
- cleanup would affect an unknown, dirty, locked, user-owned, or uniquely
  committed resource.

Do not use reset, stash, amend, rebase, or an unrelated cleanup commit as an
implicit fallback for an unresolved repository state.
````

### workflow.release

````markdown
# Release Workflow

**Standards metadata**

- ID: `workflow.release`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change ships or publishes an artifact, changes a published version promise, or prepares consumer-visible release information.
- Does not apply when: A coordinated internal change is neither shipped independently nor part of a published contract.
- Requires: `core`, `workflow.verification`, `topic.contracts`
- Specializes: `none`
- Verification: Release decision fixtures, ownership checks, and affected release acceptance claims.
- Canonical owner: `workflows/release.md`

## Release Boundary

Select this workflow when at least one release fact is present:

- an artifact or package will be shipped or published;
- independently deployed consumers rely on a published version promise;
- a public contract, supported persisted state, or distribution channel changes;
  or
- consumer-visible release information must be prepared.

An internal coordinated replacement does not require release compatibility,
versioning, or changelog work merely because the repository has versions. If
the release facts are unknown, report an unresolved release diagnostic instead
of assuming a public or internal boundary.

## Contract And Version Decision

Classify affected contracts through
[Contract Evolution](../topics/contracts.md) before choosing a version,
compatibility window, deprecation, or migration.

- `internal-coordinated` changes replace all owned consumers atomically and do
  not create a compatibility version by default.
- `public-versioned` changes follow the published version promise.
- `distributed-independent` changes define negotiation, overlap, migration, or
  typed rejection for unsupported versions.
- `persisted` changes name supported source states and migration evidence.

When a project adopts Semantic Versioning, choose the bump from observable
published-contract effects: incompatible change, compatible capability, or
compatible correction. Do not infer compatibility from source syntax, commit
type, or additive shape alone.

Major version zero denotes initial development under SemVer; it is not a
prerelease identifier and does not erase explicit consumer or migration
promises. Prerelease identifiers such as `-alpha.1` separately describe release
precedence.

Define the release unit from actual publication and consumer ownership.
Packages may version independently or in lockstep. Do not force workspace-wide
version alignment without an adopted release-unit contract.

## Deprecation And Migration

A deprecation policy exists only for a published promise that requires overlap.
It states:

- the deprecated behavior and supported replacement;
- the versions or time window in which both remain supported;
- how consumers discover the deprecation;
- the removal version or decision trigger; and
- evidence for the replacement and removal path.

Breaking public or persisted changes provide migration instructions
proportional to consumer needs. Internal coordinated replacement removes the
old path in the same change and must not add a speculative deprecation shim.

## Changelog

Record consumer-visible changes for a release boundary. A project may collect
entries directly under an unreleased section or use independently mergeable
fragments. The chosen mechanism must avoid silent loss and merge-conflict-prone
shared edits.

An entry states the observable change, affected consumers, and migration or
security implications when applicable. Typical categories include added,
changed, deprecated, removed, fixed, and security, but project-owned formats
may differ.

Do not derive changelog inclusion solely from commit types. Internal refactors,
tests, formatting, and tooling changes are omitted unless they alter the
published artifact or consumer contract.

At release preparation:

1. assemble all applicable entries for the selected release unit;
2. resolve the version and date from the accepted version decision;
3. link required migration instructions and public diagnostics;
4. exclude sensitive security details until disclosure is authorized; and
5. verify that the released entries match the artifact and published contract.

## Artifact Plan

Define the shipped artifact set from the selected release unit, distribution
channels, supported targets, and consumer contract. For each artifact, record:

- identity, version or immutable revision, target, format, and architecture;
- how consumers install, load, or execute it;
- its relationship to other artifacts in the same release;
- required integrity, authenticity, provenance, and dependency metadata; and
- the acceptance claim that proves the published artifact is usable.

Ship only artifacts that the project promises to distribute. Source archives
generated by a hosting service, native packages, installers, binaries, shared
libraries, debug symbols, checksums, signatures, provenance, and bills of
materials are separate decisions. Do not make one artifact type universal
because it was useful for another product.

Artifact names must be unique within their distribution channel and identify
the facts consumers need to select the correct download. Prefer the ecosystem's
native target and package conventions. Do not impose one cross-ecosystem
filename template when a registry or installer owns identity and selection.

For a native artifact, derive its package coordinate or filename, prefix,
extension, target and architecture labels, and relationship to companion
artifacts from the release unit, ecosystem, and distribution-channel contract.
An operating-system name alone does not select these facts.

Give affected consumers the authoritative acquisition location and the
information required to verify, install or provision, and load the artifact,
including required native dependencies and its relationship to the canonical
[loading contract](../topics/cross-platform.md#native-artifact-loading).
Place this information on the publication or package surface selected by the
consumer contract; do not attach installation prose to every
platform-specific implementation.

Return an unresolved artifact-plan diagnostic for missing or contradictory
identity, target, acquisition, installation, loading, or evidence facts. Do not
guess a conventional filename, use an ambient package as identity, substitute
another artifact, or publish with incomplete consumer information.

### Binding Artifact Roles And Composition

When a release exposes language bindings, classify each applicable item before
building the artifact plan:

- the product's native implementation artifact, when it is shipped separately;
- internal adapter, wrapper, generator, schema, or build input that produces a
  boundary but is not automatically a published product;
- generated host source or a host-language package consumed by applications;
  and
- a selected bundle that intentionally contains more than one of these items.

Record which items are release artifacts and which remain internal inputs. For
each shipped item, apply the complete artifact plan and its own applicable
[contract classes](../topics/contracts.md#contract-classes). Derive artifact
count, target coverage, separate or bundled composition, identity, naming,
relationships, acquisition, installation/loading information, and evidence
from the release unit, channels, supported targets, package ecosystems, and
consumer contracts.

An adapter or generator framework is not the product identity unless the
product contract says the framework itself is the product. Shared build
provenance may establish consistency between related artifacts, but
compatibility and version relationships remain Contracts-owned decisions.

Return an unresolved artifact-plan diagnostic when required roles,
composition, identities, relationships, consumer information, or evidence are
missing or contradictory. Do not assume one native library per target,
separate host packages, a convenience bundle, framework-derived names, example
archive names, or default success. Do not publish an internal build input
merely because it participates in binding generation.

### Binding Generation Procedures

When the accepted release artifact plan includes generated bindings, derive a
procedure from that plan rather than from a language profile example. The
procedure must identify the Contracts-selected generation authority, generator capability and version, build and dependency inputs, target and consumer
claims, output artifacts, reproducibility controls, and evidence connecting
each output to its accepted input. Commands are selected only after those
facts and their owner are accepted.

Do not infer a procedure from a compiled native library, source annotation,
framework default, target-language list, package name, output directory, or
globally installed tool. Do not switch generators, hand-edit generated output,
silently regenerate missing inputs, or claim success when a required toolchain,
authority, target, output, or evidence fact is unavailable. Return a typed `release-procedure` diagnostic for missing capability and a typed `invalid`
outcome for contradictory ownership or derivation.

Select integrity and supply-chain metadata from actual requirements:

- provide cryptographic checksums when consumers or the distribution channel
  use them to verify downloaded bytes;
- provide signatures or provenance when authenticity or build-origin claims
  are part of the release contract; and
- provide an SBOM when shipped content bundles dependencies or when consumer,
  security, regulatory, or organizational policy requires one.

Use a documented machine-readable format accepted by the intended consumer or
channel. Generate metadata from the final artifact set and verify that it
describes the published bytes. If required artifact or metadata facts are
unknown, report an unresolved artifact-plan diagnostic instead of assuming a
default package set.

## Reproducibility

State the reproducibility claim precisely. A pinned toolchain or lockfile
improves input control but does not by itself prove byte-for-byte reproducible
artifacts. A reproducible-build claim names the controlled inputs, build
environment, comparison method, and observed evidence.

Pin toolchains, build images, generators, and dependency inputs to the extent
required by the release claim. Control timestamps, host paths, locale, ordering,
randomness, network access, and other nondeterministic inputs that affect the
artifact.

Lockfile ownership follows the released dependency-resolution contract:

- commit a lockfile when it is source input for the resolved dependency closure
  used to build, test, package, or operate a released artifact;
- omit a lockfile from a published package only when the ecosystem contract
  intentionally delegates resolution to each consumer and the repository does
  not need that lockfile for its own released artifacts or tooling; and
- evaluate mixed workspaces as release units rather than applying one
  application-versus-library label to every member.

Do not silently regenerate missing pinned inputs during release. If the
required resolution or toolchain cannot be reproduced, block the corresponding
artifact claim with a typed diagnostic.

## Pipeline Mechanics

A release pipeline turns one authenticated release decision into the artifact
plan and evidence required for publication. It does not infer a release from an
ordinary branch push, path match, version-like string, or provider default.

Define an unambiguous dispatch contract:

- the accepted release unit and version or immutable source revision;
- who or what may authorize dispatch;
- how the pipeline distinguishes normal validation from release work;
- required claims and artifact-plan inputs; and
- the publication environment and permissions that may be reached.

The dispatch may use a protected tag, signed reference, manually approved
candidate, or registry-native mechanism. The mechanism is project-owned, but an
unauthenticated or ambiguous reference must produce a typed release-dispatch
diagnostic and must not enter packaging, signing, or publication stages.

### Build Procedure Selection

Derive each build procedure from the accepted artifact plan, including the
artifact identity, purpose, target, mode or optimization claim, source and
dependency inputs, toolchain capability, output location, and required
evidence. Execute only procedures selected for required artifacts. A project
with no build artifact has no build procedure; it does not gain a successful
no-op build action.

Development, optimized, debug, release, native, generated, and packaged
outputs are distinct only when the artifact and consumer contracts require
those distinctions. Do not invent universal build action names, paired modes,
commands, target binaries, or optimization meanings. When a toolchain can
produce multiple outputs, select the exact planned artifact rather than
guessing its default target.

Return typed `invalid` for contradictory artifact or mode facts and typed
`release-procedure` or `unavailable` when a required artifact, toolchain
capability, target, input, procedure, or evidence cannot be resolved. Do not
compile implicitly through another action, substitute a development artifact,
choose an alternate target or mode, or report success for an inapplicable or
unresolved build.

Build and package every target required by the accepted artifact plan. The
matrix follows supported target and environment claims rather than a universal
platform list. Unsupported or best-effort targets remain explicit and cannot
silently satisfy required matrix entries.

Collect artifacts by planned identity. Missing, duplicate, stale, or
unexpected required artifacts fail collection with diagnostics; automation
must not ignore a missing required output. Generate selected integrity,
provenance, signature, and dependency metadata from the final collected set,
then verify it against those bytes.

The publication handoff runs only after:

1. every required build, behavior, and release-artifact claim is satisfied;
2. the collected set matches the artifact plan;
3. version, changelog, migration, and disclosure decisions are accepted; and
4. the destination and authorization are explicit.

Use least-privilege credentials scoped to the publication stage and target.
Untrusted change validation must not receive release credentials. Prefer a
staging or draft state when the channel supports review, but do not treat a
provider-specific draft feature as universal policy.

Pipeline completion proves only the claims it records. A successful automation
job cannot replace missing behavior or user-workflow evidence.

## Maintenance And Channels

When a change selects maintenance channels, publication presentation, or release recovery procedures, follow [Maintenance And Channels](release/operations.md#maintenance-and-channels).

## Publication Presentation

When a change selects maintenance channels, publication presentation, or release recovery procedures, follow [Publication Presentation](release/operations.md#publication-presentation).

## Profile Routing And Release Procedure

Use [Standards Router](../STANDARDS-ROUTER.md) to select every applicable
language, application, boundary, and topic profile in addition to this
workflow. Profiles add ecosystem mechanisms and verification but cannot
override the cross-language release contracts owned here. For example, a
Rust-owned release change selects the Rust profile, which routes current
specialized Cargo release guidance during migration; the generic workflow does
not link directly to one language's tools.

Derive the release procedure from the accepted release decisions:

1. Confirm the release unit, affected contracts, consumers, and responsible
   authorities.
2. Select applicable profiles and topics through the router.
3. Accept version, changelog, migration, maintenance, channel, artifact, and
   publication decisions.
4. Satisfy every required behavior, environment, and release-artifact claim.
5. Authorize pipeline dispatch from the accepted immutable source.
6. Collect and verify the exact artifact set and selected metadata.
7. Project accepted notes, disclosures, artifacts, and channel state to the
   publication destination.
8. Verify representative published artifacts when required by the acceptance
   plan, then record the publication result and any remaining obligations.

Commit messages, branch names, tags, registry commands, audit tools, review
states, and publication commands are project- and profile-owned mechanisms.
They are required only when selected by the accepted procedure. If a required
step has no resolved owner or mechanism, return a typed release-procedure
diagnostic rather than substituting a conventional command.

## Recovery And Withdrawal

When a change selects maintenance channels, publication presentation, or release recovery procedures, follow [Recovery And Withdrawal](release/operations.md#recovery-and-withdrawal).

## Acceptance Boundary

Before publishing, identify every claim required by the release:

- `release-artifact` claims for packaging, installation, loading, checksums,
  signatures, or publication properties;
- behavior claims for changed contracts, systems, or user workflows; and
- environment qualifications for supported targets or required infrastructure.

The [Verification Workflow](verification.md) owns claim meaning and evidence
sufficiency. An artifact startup smoke proves only its named artifact
assertions; it does not prove changed feature behavior, other target artifacts,
or a user workflow.

Unsatisfied required claims remain visible release blockers. Release procedure
and publication gates consume accepted claims but cannot downgrade or replace
them.

## Optional Reference

The non-normative [Release Recipe](../reference/recipes/releases.md) illustrates
one changelog automation configuration. It does not select tools, commit
categories, release mechanisms, or policy.
````

### workflow.release.operations

````markdown
# Release Maintenance And Recovery

**Standards metadata**

- ID: `workflow.release.operations`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change selects maintenance channels, publication presentation, or release recovery procedures.
- Does not apply when: No maintenance channel, publication presentation, or release recovery procedure changes.
- Requires: `workflow.release`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `workflows/release/operations.md`

## Maintenance And Channels

For each release unit that promises post-publication support, define a
maintenance contract before making that promise:

- the supported release lines and their immutable source lineage;
- the fixes, compatibility obligations, and response classes in scope;
- who may start, extend, or end support;
- the support window or explicit end condition;
- how a fix reaches every affected supported line and relevant successor line;
  and
- the release channel through which consumers receive the result.

A standard release has no intrinsic branch, tag, maintenance duration, or
support class. Trunk-only maintenance, release branches, signed references,
registry revisions, and other source-selection mechanisms are project-owned
implementations of the maintenance contract.

When correcting a supported release, identify every affected release line,
select an accepted immutable source for each line, apply and verify the change
under that line's contract, and publish a new artifact identity. Reconcile the
fix into relevant successor lines or record an explicit reason why it does not
apply. Do not mutate published bytes or silently omit an affected supported
line.

Long-term support is an explicit support class, not a property inferred from a
branch name or release age. Its contract names scope, duration or end
condition, compatibility and security commitments, source lineage, delivery
channels, and responsible authority. If those facts are absent, return a typed
release-maintenance diagnostic rather than claiming maintenance or long-term
support.

A release channel is a consumer contract, not a branch, tag, version-like
string, or deployment environment. Define its audience, stability and
compatibility expectations, admission and promotion criteria, update and
discovery behavior, retention and support policy, withdrawal or rollback
behavior, and artifact identity rules.

Prerelease identifiers and channels are independent decisions. Promotion may
reuse accepted bytes only when the destination channel accepts the same
artifact identity and evidence; otherwise produce and verify a new planned
artifact. If the channel or promotion decision is unresolved, return a typed
release-channel diagnostic and do not silently publish to a default channel.

Feature flags and runtime activation controls do not define release channels.
When a product can deploy code separately from activating behavior, govern
that mechanism through an explicit project-owned configuration and lifecycle
policy rather than inferring it from the release process.
## Publication Presentation

A publication surface presents an accepted release to consumers. It does not
own versioning, channels, artifact identity, compatibility, or acceptance
decisions. Before publication, define:

- the destination and release channel;
- the responsible publication authority;
- any private, staged, review, public, or withdrawn visibility states;
- the accepted release notes and required disclosures;
- how planned artifacts and their relationships are presented; and
- how consumers discover, select, verify, and report problems with the release.

Enter a draft or review state only when the destination supports it and the
accepted publication procedure requires it. A provider feature or manual
review is not a universal release gate. Publication may proceed only from the
canonical pipeline handoff with the authority required for the selected
destination and visibility transition.

Derive prerelease presentation from the accepted version and channel
contracts. Major version zero does not by itself make a publication a
prerelease. Provider labels are projections of the canonical decision and
cannot redefine it.

Release notes derive from the accepted changelog, migration obligations,
support policy, and required security or operational disclosures. Generated
summaries may supplement that material when they are accurate, but cannot
replace required curated content or invent unaccepted claims.

Present the exact artifact identities and relationships from the artifact
plan. Give consumers enough target, format, and compatibility context to select
the correct artifact, and place each selected integrity, signature,
provenance, or dependency document where its relationship to the final bytes
is unambiguous. Provider layout and grouping may improve discovery but must not
create a second artifact identity scheme.

If destination, authority, visibility, notes, channel projection, or artifact
presentation is unresolved, return a typed release-publication diagnostic and
do not publish using a provider default.
## Recovery And Withdrawal

Plan recovery for each publication destination and channel before relying on a
generic rollback claim. Published artifacts may be immutable, cached,
installed, mirrored, or consumed offline, so reversal can require one or more
distinct actions:

- stop further distribution or promotion;
- mark, yank, withdraw, or deprecate an affected artifact when supported;
- notify affected consumers and operators;
- contain active harm through an authorized operational control;
- publish a corrected or superseding release; and
- restore or migrate affected state under its persistence contract.

Start recovery when accepted evidence or observed impact invalidates a required
release claim, creates unacceptable security or safety exposure, corrupts
artifacts or state, or violates the release's support and channel contracts.
Classify affected release units, versions, channels, consumers, artifacts, and
persisted state before selecting actions.

Use only transitions supported by the destination and contract. Do not describe
withdrawal as erasure when consumers may retain bytes, mutate a published
artifact in place, reuse an immutable version or artifact identity for
different bytes, or assume every registry supports unpublishing. When reversal
is unavailable, contain distribution where possible, communicate the status,
and publish a newly identified correction or superseding decision.

The recovery contract names normal and emergency authorities, required
approvals, credential scope, notification owners, and any actions permitted
before broader review. Urgency does not grant implicit authority. If immediate
action is necessary, record the acting authority, evidence, scope, and
follow-up obligations.

Verify each recovery action against its intended effect. A replacement release
must satisfy its own version, contract, artifact, behavior, and publication
claims; recovery status cannot waive normal acceptance. Reconcile corrections
across every affected supported release line.

Record the incident, consumer impact, actions, residual exposure, and prevention
decision in the durable artifact selected by documentation policy. A changelog
or release note is appropriate only when it communicates a consumer-relevant
change; it is not a universal post-incident record.

If affected scope, channel capability, authority, safe action, or replacement
evidence is unresolved, return a typed release-recovery diagnostic and preserve
the known incident state rather than claiming rollback success.
````

### topic.performance

````markdown
# Performance

**Standards metadata**

- ID: `topic.performance`
- Role: `topic`
- Level: `MUST`
- Applies when: A task changes a performance claim, budget, measurement, optimization, benchmark, resource-use behavior, or performance-sensitive implementation.
- Does not apply when: The task makes no performance or resource-use claim and does not change a measured performance-sensitive path.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Performance claim, measurement, optimization, benchmark, and regression decision fixtures plus claim-matched measurements in the required environment.
- Canonical owner: `topics/performance.md`

## Performance Claim Authority

Name the owned performance claim before selecting an optimization. The claim
identifies the operation or workflow, metric, workload, budget or comparison,
environment, variability policy, and consumer impact. Latency, throughput,
memory, energy, startup, frame time, and capacity are distinct claims.

A hot-path label, call frequency, allocation, algorithm class, profiler sample,
or benchmark result is evidence about a claim; it does not independently
authorize an implementation change.

## Measurement Contract

Measure the relevant workload in an environment representative of the claim.
Record inputs, data scale and distribution, warm-up or steady-state conditions,
runtime and build configuration, hardware or resource constraints, sample
method, variability, and baseline. Control only factors material to the claim.

Use profiling to locate contributing work when the claim and available tooling
make profiling informative. Profiling before every change is not universal,
and a profile does not prove an end-to-end budget or regression by itself.

Do not substitute a debug build, synthetic microbenchmark, single sample,
different device, stale baseline, or unrelated workload when the required
measurement is unavailable.

## Optimization Decision

Optimize when evidence shows the owned claim is unsatisfied or materially at
risk and the proposed change addresses a measured contributor. Evaluate the
effect on correctness, maintainability, resource use, other performance
claims, and operational complexity.

Allocation avoidance, pooling, caching, batching, precomputation, parallelism,
specialization, and lower-level representations are mechanisms, not defaults.
Code that runs at startup may still own a startup claim; code in a loop may be
irrelevant to the limiting claim. Readability does not automatically block or
authorize an optimization.

Retain the simplest implementation that satisfies the accepted claim and its
other contracts. Remove or revise an optimization when representative evidence
shows it no longer provides the intended value or its tradeoffs are no longer
accepted.

## Benchmarks And Regression Evidence

Use a microbenchmark for an isolated mechanism claim and an integration or
user-workflow measurement for an end-to-end claim. Choose the narrowest
measurement that covers the property; neither form substitutes for the other.

[Performance Test Evidence](#performance-test-evidence) defines the shared
workload, baseline, environment, threshold, and reporting requirements.
Documentation records durable claim, tradeoff, and reproduction facts that cannot be recovered
from the code and evidence. Documentation does not replace measurement.

## Performance Test Evidence

Select the benchmark or test harness from the owned claim, workload, required
environment, and measurement capability. An ecosystem harness may improve
repeatability, but its use does not establish that the workload, metric,
baseline, budget, or environment is authoritative. A unit-test clock around one
invocation does not prove an end-to-end latency, throughput, capacity, memory,
energy, startup, or frame-time claim unless its measurement contract covers
that claim.

A performance budget names its authority, consumer impact, workload, metric,
environment, and variability policy. Derive a threshold from that contract; do
not copy a duration, percentage, sample count, machine, CI cadence, or benchmark
tool from an example. Compare the candidate with the applicable baseline or
budget and preserve correctness and resource-tradeoff evidence.

When a representative environment, reliable measurement capability,
authoritative budget, or applicable baseline is unavailable, return
`unavailable`. Do not pass a weaker microbenchmark, nearby device, debug build,
single timing sample, or successful harness execution as the required result.

## Typed Outcomes

Contradictory metric, budget, workload, environment, or authority facts are
`invalid`. A declared claim or mechanism outside supported product or platform
capability is `unsupported`. Missing baseline, representative environment,
measurement capability, budget authority, or required evidence is
`unavailable`.

Do not continue with a guessed budget, conventional threshold, alternate
workload, stale benchmark, nearby device, allocation ban, hot-loop assumption,
weaker evidence, undocumented comparison, or default success.

## Verification

Evidence covers the accepted workload and environment, baseline and candidate,
variability policy, claimed improvement or budget, correctness and resource
tradeoffs, and negative or unsupported cases. Re-run the narrowest complete
claim after implementation and retain evidence according to its decision and
regression value.
````

### topic.contracts.schemas

````markdown
# Schemas And Generated Contracts

**Standards metadata**

- ID: `topic.contracts.schemas`
- Role: `topic`
- Level: `MUST`
- Applies when: A change affects schema dialects, generated contracts, or contract version invalidation.
- Does not apply when: No schema dialect, generated contract, or contract-version invalidation changes.
- Requires: `topic.contracts`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `topics/contracts/schemas.md`

## Declaration And Semantic Authority

A contract declaration owns only the representation and meanings selected by
its declared responsibility. Before treating one declaration as canonical for
several semantic families, identify the owner of each applicable family, such
as representation, validation, identity, authorization, state transition,
persistence, projection, and compatibility. The list is illustrative;
observable meaning and actual ownership select the families.

An annotation, extension, reference, generated model, or validator may project
or invoke semantics owned elsewhere without transferring that ownership to the
declaration. Record how each referenced owner is resolved and which executable
enforces its semantics. Do not create a second interpreter, redefine domain
policy as declaration metadata, or infer that declaration authority includes
every concern the artifact can describe.

One owner may legitimately hold declaration and executable or domain semantics
when they form one coherent responsibility. Distinct owners are also valid
when the dependency and projection are explicit. Missing semantic authority is
`unavailable`; contradictory authorities or an attempted ownership transfer by
annotation are `invalid`; a well-formed semantic family outside the supported
contract is `unsupported`.
## Version Scope And Invalidation

A version identifies one coherent compatibility or evolution promise. Record
the promise, authority, consumers, supported overlap, invalidation effect, and
the representations or behaviors it governs. Several concerns may share a
version only when they intentionally share that promise; independently
changing promises require independently scoped versions or an explicit version
record that preserves their separate identities.

Classify the role before adding or reusing a version-like value:

- a current-format discriminator rejects representations the current decoder
  does not support, without promising overlap with an older reader;
- an identity-domain revision changes the semantic identity or invalidation
  domain selected by its authority;
- a compatibility version governs producer-consumer combinations supported at
  the same time;
- a migration version identifies an admitted source-to-destination transition;
  and
- an allocation ordinal supplies uniqueness or ordering inside one authority
  and is not a compatibility promise.

One value may serve more than one role only when those roles have the same
authority, consumers, change reasons, and consequences. Similar names,
monotonic integers, shared storage, or simultaneous updates do not establish
that equivalence.

A common file, schema, model, package, generator, build, release, deployment,
or cutover may coordinate changes without creating one version scope. Do not
use an umbrella version to force unrelated consumers to migrate together or to
make an independently compatible concern appear changed.

Include a contract version in content identity, cache invalidation, persisted
handles, replay closure, or regeneration inputs only when a change to that
version can materially change the reproduced meaning. Representation-only
change does not invalidate semantic identity unless the selected contract
proves that effect. Record that proof rather than coupling every available
version defensively.

Require a compatibility matrix only for producer, consumer, and persisted-state
combinations the selected contract actually promises concurrently. An atomic
coordinated replacement needs a fail-closed current-format decision, not a
historical compatibility matrix by default. Do not infer retained readers,
cross-engine migration, or every pairwise version combination from hypothetical
consumers or from the presence of several version-like fields. Each admitted
overlap names its owner, evidence, retirement condition, and cumulative support
cost.

Missing promise, consumer, or invalidation facts are `unavailable`;
contradictory scopes or identity coupling to an unrelated version are
`invalid`; and a well-formed version outside the supported promise is
`unsupported`. Do not fall back to lockstep increments, broad cache busting, or
the version already present on a containing artifact.
## Generated Contract Semantic Conformance

A generated contract has one canonical declaration authority and one
identified executable semantics owner for every supported keyword, extension,
or construct. Inventory every public operation and traverse every definition
reachable from those operations. A generator that copies visible field names
but omits reachable variants or selected semantics is incomplete.

The destination representation preserves every meaning selected by its
contract, including applicable types, fields, requiredness, optionality,
defaults, constraints, discriminants, variants, ordering, normalization,
equality, and typed failures. Unsupported source behavior is rejected
explicitly; it is not partially generated or interpreted through a convenient
local subset.

Generate deterministically from the canonical declaration and reject stale
outputs. Prove generated freshness separately from shape agreement, semantic
agreement, and behavior through the actual public producer and consumer entry
points. A fresh artifact is not evidence that the generator implemented the
complete selected semantics.

When multiple executables interpret the same declaration, prove the supported
dialect against an independent reference or official conformance corpus.
Comparing the local executables remains useful consistency evidence but cannot
be the only external-conformance oracle.
## Schema Dialect And Vocabulary

Before implementing or generating from a schema, declare the exact dialect,
vocabularies, extensions, and supported keyword and annotation inventory.
Identify the authority and executable semantics owner for each supported
element, including traversal and reference behavior. A filename, media type,
schema-like shape, or parser success does not identify a dialect or support
set.

Reject an unknown required dialect, vocabulary, keyword, extension, or
reachable construct as `unsupported`. Return `unavailable` when the selected
authority or required conformance evidence cannot be obtained, and `invalid`
when an implementation claims support while omitting or contradicting selected
semantics. Do not infer support from nearby keywords, local examples, another
implementation, or the subset exercised by current fixtures.
````

### topic.contracts.protocols

````markdown
# Protocol Adapters

**Standards metadata**

- ID: `topic.contracts.protocols`
- Role: `topic`
- Level: `MUST`
- Applies when: A change projects domain outcomes into a protocol or adapts a protocol boundary.
- Does not apply when: No domain outcome or boundary representation is projected into a protocol.
- Requires: `topic.contracts`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `topics/contracts/protocols.md`

## Protocol Outcome Projection

Classify the authoritative operation outcome before projecting it through a
protocol. Record the outcome authority, applicable protocol and version,
supported outcome variants, status or control metadata, response
representation, disclosure decision, consumers, and evidence that each
projection preserves the selected meaning.

The selected protocol contract decides how an outcome is represented. A
transport-level success may carry a rejected application outcome only when that
is an explicit supported representation; a transport-level failure does not by
itself classify the operation. Status, headers or equivalent control metadata,
and body must describe one consistent selected outcome. Serialization,
readability, a status class, or a familiar envelope does not establish that
consistency.

Do not infer a universal mapping from outcome names to HTTP status codes or
other protocol controls. A protocol may define different mappings for
different operations, versions, consumers, or externally governed promises.
Likewise, no JSON envelope, human-readable message field, error code, empty
body, or response wrapper is a default. Security selects what may be disclosed;
Diagnostics selects reporting projections without changing the operation
outcome.

Return:

- `unavailable` when the authoritative outcome, protocol contract,
  representation, disclosure decision, adapter capability, or required
  evidence cannot be obtained;
- `invalid` when status, control metadata, body, or disclosure contradicts the
  selected outcome or representation; or
- `unsupported` when a well-formed outcome or representation has no supported
  projection in the selected protocol contract.

Do not guess a status or envelope, map an unknown failure to a default internal
error, treat transport success as operation success, expose raw diagnostic text,
switch representations or decoders, retry, recover, or emit a partial response
as a fallback. Illustrative HTTP mechanisms are isolated in the
[HTTP projection recipes](../../reference/recipes/http.md).
## Protocol Adapter Proof

A producer adapter accepts an already authoritative operation outcome, selects
the exact operation and protocol-version projection, constructs its complete
response representation, proves status or control metadata, body, and
disclosure consistency, and only then emits the response. A shared error type,
middleware layer, exception mapping, or response wrapper is optional mechanism,
not outcome authority.

A consumer adapter treats the received response as unknown. It selects the
applicable operation and protocol-version contract, validates all required
status or control metadata, headers, content type, and body variant, constructs
the validated outcome representation, and only then exposes that outcome to its
caller. Checking status before body, body before status, or both in one decoder
is a mechanism decision; neither status nor body alone proves the outcome when
the selected contract requires both.

Producer and consumer proof must agree on every selected variant, including
success, rejection, failure, empty, and degraded responses. A protocol may
explicitly represent an application error through successful HTTP transport;
that is valid only when producer and consumer contracts select and prove the
same representation. Conversely, a status convention cannot hide a body that
contradicts it.

Adapters do not select disclosure, diagnostic reporting, retry, recovery, or
degradation policy. Security owns disclosure, Diagnostics owns reporting
projection, Resilience owns retry and recovery, and Verification owns claims
that clients, intermediaries, or monitoring systems interpret the projection.

Return `unavailable` when the adapter, mapping, decoder, disclosure decision,
consumer facts, or evidence is absent; `invalid` for incomplete proof,
contradictory response parts, unsafe disclosure, duplicate or partial emission,
or a false interpretation claim; and `unsupported` for a well-formed response
variant outside the selected contract.

Do not substitute a generic error, raw message, default internal-error mapping,
status-only or body-only interpretation, alternate decoder, successful
transport, retry, recovery, or duplicate response. Preserve the typed outcome
when complete adapter proof cannot be established.
````

### topic.contracts.evolution

````markdown
# Contract Evolution

**Standards metadata**

- ID: `topic.contracts.evolution`
- Role: `topic`
- Level: `MUST`
- Applies when: A change affects contract compatibility, persisted representations, or independently changing consumers.
- Does not apply when: No compatibility promise, persisted representation, or independently changing consumer is affected.
- Requires: `topic.contracts`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `topics/contracts/evolution.md`

## Contract Classes

| Class | Required evolution policy |
| --- | --- |
| `internal-coordinated` | Replace producer and all consumers atomically. Remove the old shape in the same change; do not add a compatibility shim. |
| `persisted` | Define supported source states, migration or rejection behavior, rollback/data-retention needs, and round-trip evidence. |
| `public-versioned` | Follow the published compatibility and versioning promise; deprecate or version when independent consumers need overlap. |
| `distributed-independent` | Negotiate or explicitly reject versions because producer and consumer deployments may overlap. |
| `generated` | Change the canonical source and generator, regenerate deterministically, and verify producer/consumer consistency. |

A boundary may have more than one class. For example, a generated public binding
requires both generated-source consistency and the public versioning promise.
## Cross-Language Contract Selection

Using more than one implementation language does not select a compatibility
policy or make either implementation authoritative. Apply every applicable
contract class, then record one canonical authority for the effective wire or
schema contract. The authority may be a schema, protocol specification,
generator input, or explicitly owned producer contract; serializer defaults
and a consumer's inferred shape are not authorities.

For an `internal-coordinated` contract, update the authority, producer, and
every consumer atomically and remove the rejected representation in the same
change. For a `generated` contract, update the canonical source and generator
before regenerating every affected producer and consumer. For a `persisted`,
`public-versioned`, or `distributed-independent` contract, follow its declared
migration, compatibility-window, or negotiation policy and reject unsupported
versions explicitly. Cross-language use does not justify dual reads, dual
writes, guessed schemas, or an indefinite old-shape path.

For language bindings, classify each affected artifact independently: native
adapter API, canonical generator input, generated source, host package, native
package, stable ABI, wire representation, and persisted representation. One
release may coordinate several artifacts, but a shared release input or
version identifier does not give them one compatibility promise.
Common build or release provenance may establish source-to-artifact
consistency evidence; it does not select a compatibility class, compatibility
window, or lockstep version relationship.

Select canonical generation authority from the applicable contract: an owned
schema or protocol, declared generator input, or explicitly owned producer
contract. A compiled implementation artifact, source annotation, generated
consumer output, or whichever input a framework accepts is not canonical by
default. When generation applies, record the authority, generator capability,
affected outputs, deterministic derivation, and producer/consumer consistency
evidence before producing or publishing an output.

Regenerate only affected outputs when their canonical generation input or
generator changes. An unrelated private implementation change does not require
regeneration. When regeneration applies, update the canonical input and
generator first, derive every affected output deterministically, and verify
each supported producer/consumer path. Do not hand-edit generated output or
regenerate from inferred consumer shape.

Select shared or independent artifact versions from actual publication,
deployment, package-resolution, and consumer compatibility contracts. Do not
force native libraries and host packages into lockstep or independent versions
without those facts. A syntactically additive change is compatible only when
every applicable consumer contract permits it; exhaustive variants, required
behavior, defaults, fields, generated APIs, persisted state, and ABI or wire
representations may make it breaking.

Evidence must match the selected contract and deployment facts. Prove the
canonical authority, the producer's emitted representation, and each affected
consumer's accepted and rejected representations. Coordinated contracts
require complete producer/consumer evidence from the atomic change.
Independently deployed contracts require supported-version and
unsupported-version evidence across the promised overlap. Generated contracts
also require deterministic regeneration and source-to-output consistency.

Return `unavailable` when the canonical authority or required contract
capability cannot be obtained, `unsupported` when a well-formed version lies
outside the declared support policy, and `invalid` when the representation or
required producer/consumer proof does not satisfy the selected contract. Do
not guess from serializer defaults, preserve an old representation as a
compatibility shim, try a second shape, or report success with incomplete
consumer evidence.
## Coordinated Breaking Replacement

Breaking replacement is preferred when all consumers and persisted states are
owned and updated in one atomic deployment. The change must:

1. update the canonical producer and every consumer;
2. remove the rejected shape and execution path;
3. update fixtures and generated artifacts;
4. return typed diagnostics for stale or invalid input; and
5. verify the complete affected path.

Do not keep dead fields, adapters, aliases, dual reads/writes, or old runtime
paths merely because they existed.
## Persisted Evolution

Persistence requires compatibility only for data states the project actually
commits to retain. Define:

- supported source versions;
- ordered and transactional migration where applicable;
- idempotency or explicit one-shot preconditions;
- backup, rollback, and failure behavior;
- typed rejection for unsupported or corrupt states; and
- evidence using representative existing data.

Never delete or overwrite authoritative data as a recovery fallback. Rebuild is
valid only for explicitly disposable derived state whose authoritative source
and reconstruction procedure are known.
## Persisted Contract Artifacts

For a checked-in example, fixture, template, manifest, saved workflow, request,
response, or other persisted artifact derived from a schema, generator, or
producer contract, record the canonical authority, applicable contract version,
derivation method, intended consumers, and whether the artifact is authored
input, authoritative state, or disposable derived output.

Validation proves that the current artifact satisfies its applicable producer
and consumer contracts. Regeneration proves deterministic derivation from the
selected authority; it does not by itself prove that consumers accept the
result or that overwriting the prior artifact is authorized. When regeneration
is selected, preserve authored or authoritative inputs and verify every
affected consumer path before accepting the new output.

Return `invalid` when the artifact contradicts its selected authority or
consumer contract, `unsupported` when its well-formed version or variant is
outside the declared support set, and `unavailable` when the authority,
generator, decoder, consumer, provenance, or required evidence cannot be
obtained. Do not accept a stale artifact, infer authority from the checked-in
shape, regenerate from a consumer guess, overwrite authoritative input, copy a
producer snapshot as consumer proof, or report success because generation or
parsing completed.
## Public And Independently Deployed Evolution

For public or independently deployed consumers:

- state the compatibility window and version negotiation mechanism;
- preserve old behavior only for the promised window;
- keep version-specific handling explicit and testable;
- reject unsupported versions with typed diagnostics; and
- remove expired compatibility paths through a planned breaking release.

Speculative consumers do not justify indefinite compatibility.
````

### topic.architecture

````markdown
# Architecture

**Standards metadata**

- ID: `topic.architecture`
- Role: `topic`
- Level: `MUST`
- Applies when: A change creates or changes module, layer, service, process, data-authority, composition, dependency-direction, or state-ownership boundaries.
- Does not apply when: No architectural ownership, dependency, lifecycle, or deployment boundary changes.
- Requires: `core`, `topic.contracts`
- Specializes: `none`
- Verification: Architecture decision fixtures plus affected dependency, contract, lifecycle, and cross-boundary evidence.
- Canonical owner: `topics/architecture.md`

## Architecture Authority

Architecture owns placement and direction of responsibilities, authority,
state, dependencies, and runtime composition. Contracts owns boundary
representation and compatibility; Concurrency owns ordering and concurrent
access; Resilience owns failure and degradation; deployment and application
profiles own concrete mechanisms.

## Design Vocabulary

A **module** owns a coherent responsibility behind an **interface**, the
behavior and obligations visible to callers. A **seam** is a boundary where an
implementation can vary without changing the caller's contract. **Depth** is
how much useful responsibility an interface hides; **leverage** is the useful
work enabled by that interface; **locality** means a change stays with its
owning concern. These terms describe design effects, not counts of files or
classes. Capitalization elsewhere in this library does not introduce a new
kind of object.

## Concern Boundaries

Separate concerns when they change for different reasons, require different
owners or lifecycles, or let callers ignore unrelated policy safely. Keep a
coherent concern together when its invariants, inputs, outputs, lifecycle, and
failure behavior form one decision. Directory and file placement follow those
boundaries; repository shape does not create them.

Select layers, modules, packages, services, or processes from actual ownership,
deployment, trust, scaling, lifecycle, and change facts. Do not require a
universal layer count, layer name, directory tree, source-root README threshold,
or inward-dependency diagram.

## Composed Design Admission

Apply this admission when a material design introduces or changes Modules,
Interfaces, Seams, Adapters, composition roots, or several permanent mechanisms
that together create a new operational or maintenance obligation. Re-run it
when a replacement design changes that composition or observed change
propagation is materially broader than predicted.

Record the produced artifact, not only its proposed parts:

1. independent concerns and their what, who, how, when, where, and why
   dimensions;
2. required and accidental interleavings of state, identity, value, time,
   policy, and mechanism;
3. everything callers, peer Modules, and the composition root must know;
4. representative changes and every owner each change is semantically forced
   to touch;
5. which dependencies carry stable values or Interfaces and which expose
   hidden representation, ordering, lifecycle, policy, or version knowledge;
6. whether the parts can evolve, be verified, fail, and be replaced
   independently;
7. the deletion result for each new permanent Module, Seam, Adapter, registry,
   validator, generator, version, or other mechanism; and
8. necessary inherent complexity, where it is contained, and the cumulative
   machinery retained by the complete design.

A useful Module has Depth: its Interface gives callers Leverage while hiding
more knowledge than it requires them to learn. Evaluate Locality through the
representative changes; a nominal split is still complected when the same
knowledge and verification must propagate through its callers or peer Modules.
Use the deletion test: if deleting a Module makes its complexity disappear, it
was incidental; if the necessary complexity reappears across callers, the
Module was containing it.

A hypothetical Adapter may probe the shape of a possible Seam, but does not
justify permanent generality. Generality requires a current independent reason.
Materially distinct real implementations are evidence; a separately owned
public contract, trust, deployment or lifecycle boundary, or enforceable
invariant may also justify a Seam without multiple current implementations.
Keep test-only or internal Seams inside the Module unless callers need the
variation as part of its Interface.

The admission must be able to keep one deep coherent Module, introduce a Seam,
aggregate adjacent machinery, or delete or decline a guarantee. File, type,
Module, dependency, or test counts are diagnostic inputs, never the verdict.
Missing material artifact or change-path facts are `unavailable`; contradictory
ownership, Interface, or coupling claims are `invalid`.

## Authority Scope Admission

Before a module, schema, manifest, registry, model, interface, or other artifact
becomes canonical for more than one concern, record the responsibility it
owns, the concerns it only references, the owner and lifecycle of each concern,
and the reasons those concerns change. Canonical placement is an ownership
decision; the ability to contain, serialize, validate, generate, or distribute
information does not transfer authority for that information.

Admit one authority scope only when its concerns form one coherent
responsibility with aligned owners, lifecycle, invariants, and change reasons.
When concerns can change independently, keep their authorities independently
replaceable even if one artifact references or packages them together. A
shared file, data format, generator, deployment, release, or repository
location is not evidence of a shared responsibility.

The selected boundary should hide more implementation detail than it exposes
through its interface and localize the complexity required to uphold its
responsibility. If removing one concern would leave unrelated fields,
versions, invalidation, consumers, or policy in place, treat that as evidence
of separate authority unless an explicit shared invariant proves otherwise.

Missing owner, lifecycle, or change facts are `unavailable`; contradictory
authority is `invalid`. Do not fall back to an umbrella artifact, the current
file boundary, or a single version merely because separation requires an
adapter or explicit composition.

## Dependency Direction And Services

Dependencies point toward the owner of the stable contract, not toward a
framework, transport, UI, storage mechanism, or current file location.
Business policy remains usable independently of delivery and infrastructure
mechanisms unless its domain contract requires them. A service boundary
requires an independently meaningful owner or deployment/lifecycle boundary;
test convenience alone does not create one.

## Data And State Authority

Assign every authoritative datum and state transition one owner. Projections,
caches, views, and pending input identify their source and synchronization
contract and cannot become a second authority. Backend, frontend, worker,
process, or database location does not determine ownership by itself.
Optimistic projection is allowed only when its reconciliation and failure
semantics satisfy the selected contract.

## Runtime Composition

Construct concrete infrastructure and long-lived resources at the narrowest
composition boundary that owns their configuration and lifecycle. Consumers
depend on selected contracts and receive dependencies explicitly. Do not create
ambient global infrastructure, duplicate a long-lived owner, or hide runtime
selection inside business policy.

## Immutable Authority Closure

When a handle promises immutable results or replay, follow [Immutable Authority Closure](architecture/replay.md#immutable-authority-closure).

## Typed Outcomes

Return typed `invalid` for contradictory ownership, dependency, lifecycle, or
authority decisions; typed `unsupported` when a valid required architecture is
not supported by the selected environment; and typed `unavailable` when a
required owner, contract, deployment, lifecycle, or capability fact cannot be
established. Do not fall back to the incumbent structure, a fixed layer model,
backend ownership, framework placement, global state, or the smallest diff.

## Verification

Evidence covers applicable dependency direction, owner uniqueness, independent
business-policy tests, contract boundaries, state transitions, projection
reconciliation, composition lifecycle, and real cross-boundary behavior.

After these decisions are complete, the non-normative
[Architecture Pattern Reference](../reference/patterns/architecture.md) may
help communicate an illustrative structural shape. Reference presence does not
select a pattern or establish applicability.
````

### topic.architecture.replay

````markdown
# Immutable Results And Replay

**Standards metadata**

- ID: `topic.architecture.replay`
- Role: `topic`
- Level: `MUST`
- Applies when: A handle promises immutable results or replay.
- Does not apply when: A handle exposes only live state and promises neither immutable results nor replay.
- Requires: `topic.architecture`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `topics/architecture/replay.md`

## Immutable Authority Closure

A handle that promises an immutable result or replay binds the complete
transitive authority closure needed to reproduce that promised result. A live
inspection handle may observe current state when its contract says so;
inspectability alone does not promise replay. The closure includes each
authority, contract, provider input, and historical authorization input whose
value determines the captured result, referenced through an exact immutable
identity.

Derive that closure from the handle's advertised operations, result semantics,
supported lifetime, and reconstruction promise. An in-process handle need not
be independently persisted when its contract ends with the owning process. A
handle promising cold replay or use after its producer ends must bind a durable
reconstruction source. Do not strengthen an in-process inspection promise into
cold replay merely because persistence machinery is available.

Closure completeness does not require one separately persisted identity,
codec, version, handle, allocation ordinal, registry, or lifecycle object for
each concern. One immutable aggregate may carry the complete admitted closure.
Require independently replaceable records only when an independently owned
authority, consumer promise, lifetime, or reconstruction path needs them. The
ability to name a field or serialize a record is not evidence that another
authority object is required.

Reconstruction of the promised result cannot depend on ambient mutable state,
an instance-local cache, the originating process, undeclared providers, or a
live filesystem or service read that is not itself bound into the closure.
Derived results may be cached, but cache availability and process history cannot change
their meaning.

Current permission to access or disclose a captured result remains a separate
security decision. Check it when the access contract requires it, and deny
revoked access without changing the captured content or substituting a newer
result. Historical permission is an input to replay, not a continuing grant.

Persistence owns reopening through real store adapters, and Contracts owns
handle representation and version behavior. If any required authority cannot
be resolved exactly, return `unavailable`; if resolved content contradicts its
identity or closure, return `invalid`; and if the representation or contract
version is well formed but unsupported, return `unsupported`. Do not replace a
missing immutable input with current ambient state.
````

### topic.code-design

````markdown
# Code Design And Ownership

**Standards metadata**

- ID: `topic.code-design`
- Role: `topic`
- Level: `MUST`
- Applies when: A change makes structural, abstraction, or terminology decisions.
- Does not apply when: No structural, abstraction, or terminology decision changes.
- Requires: `core`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `topics/code-design.md`

## Simplicity And Ownership

- Separate concerns that change for different reasons. Do not split coherent
  behavior merely to reduce file or line counts.
- Give each policy, state, lifecycle, contract, and generated artifact one
  canonical owner.
- Keep business policy independent of transport, UI projection, persistence,
  runtime wiring, and diagnostics unless the domain itself requires coupling.
- Make dependencies point toward stable contracts and owned abstractions.
- Do not create a second source of truth to avoid changing the real owner.

Simplicity is the reduction of entanglement and reasoning load, not the
minimization of files, types, dependencies, abstractions, or lines. A boundary
is useful when it lets a maintainer understand or change one concern without
also understanding unrelated transport, lifecycle, persistence, runtime, UI,
timing, or diagnostics policy.

Keep one coherent concern together when its invariants, lifecycle, inputs,
outputs, and failure behavior form one decision. Introduce a named boundary
when it separates independently changing decisions, establishes one owner, or
makes an invariant enforceable. More named components can be simpler when each
removes unrelated context from the others.

Do not select a design from a file-length threshold, type count, dependency
count, call-site count, repository layout, incumbent abstraction, or smallest
diff. If material ownership, invariants, lifecycle, failure, or change facts
are unresolved, return the applicable typed diagnostic or record the decision
before implementation rather than choosing the fewest visible constructs.

### Code And Terminology Discipline

Use the least code and structure that make the owned behavior, invariants,
lifecycle, failures, and side effects clear. Additional structure is justified
when it separates independently changing decisions, enforces an invariant,
removes repeated reasoning, or supports demonstrated variants. It is not
justified by speculative reuse, a preferred construct count, an incumbent
pattern, or the smallest visible diff.

Create an abstraction only when callers can safely ignore a concern that the
abstraction owns. Keep its material lifecycle, ordering, state authority,
failure behavior, and side effects visible in the contract. One call site may
justify a boundary and many call sites may not; call count does not decide.

Consolidate repeated implementations when they express the same owned
contract and independent copies create divergence risk. Keep superficially
similar implementations separate when their owners, invariants, lifecycle, or
change axes differ. Do not apply blanket extraction, reuse, or duplication
rules.

Delete code, aliases, adapters, flags, comments, and conditional code branches
that have no current owner or supported contract. Preserve a path only for a
real active consumer, retained state, deployment overlap, or other declared
lifecycle obligation. Unverified future use and incumbent presence are not
retention authority.

Choose names from domain meaning, role, unit, ownership, lifecycle, and
observable effect at the narrowest useful scope. Use one term for one concept
within a contract and distinguish different concepts even when their
implementations look alike. Rename when current terminology misstates the
owned concept; do not keep or copy a name solely for consistency with an
incumbent, framework convention, or generic naming recipe.

Missing or contradictory ownership, invariant, consumer, lifecycle, or domain
meaning requires a typed diagnostic or a recorded decision before structural
change. Do not fall back to fixed call counts, blanket DRY, universal brevity,
speculative extension points, existing terminology, or copied examples.

### Simple, Easy, And Complection

For these standards, **simple** describes an artifact whose distinct concerns
are not interleaved. **Easy** describes an approach that is familiar, nearby,
available, or convenient to a particular person or environment. Easy and simple
may coincide, but neither proves the other.

An artifact is **complex** or **complected** when otherwise independent concerns
must be understood or changed together because their knowledge, state,
identity, value, time, location, representation, mechanism, or policy is
interleaved. To **compose** is only to place concerns together; composition,
decomposition, and naming do not decide simplicity.

Judge the produced artifact and its evolution, not the ease of authoring,
generation, installation, familiarity, or conformance to an incumbent pattern.
Simplicity evidence asks whether independent concerns can be understood and
changed independently and whether each change exposes only the knowledge it
owns. Counts may locate accumulated cost but cannot decide simplicity.
````

### topic.dependencies

````markdown
# Dependencies

**Standards metadata**

- ID: `topic.dependencies`
- Role: `topic`
- Level: `MUST`
- Applies when: A change adds, selects, resolves, installs, updates, removes, audits, or changes ownership of a software, toolchain, service, build, test, runtime, or system dependency, or decides to implement difficult standardized semantics instead of adopting an established implementation.
- Does not apply when: No dependency requirement, implementation-versus-adoption decision, declaration, resolution, provisioning, or lifecycle behavior changes.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Dependency requirement, ownership, selection, resolution, authorization, satisfaction, and lifecycle decision fixtures plus affected real resolver and consumer evidence.
- Canonical owner: `topics/dependencies.md`

## Dependency Authority

Select a dependency only from an explicit requirement and consumer contract.
The contract identifies the capability, owning execution boundary, lifecycle
phase, supported targets and environments, release or deployment constraints,
and evidence required to prove satisfaction.

Dependencies owns requirement, candidate comparison, selection, declaration
ownership, resolution, provisioning authorization, satisfaction, update, and
removal policy. Release owns published artifact and consumer acquisition
information. Security owns trust and untrusted-input authorization. Resilience
owns failure, retry, and degradation. Language and framework profiles own
mechanisms. Launcher only projects an accepted dependency procedure.

## Requirement And Ownership

Declare each dependency at the narrowest boundary that owns and executes it.
Shared declarations require evidence that multiple owned consumers use the
same requirement; centralized version coordination does not erase consumer
ownership. Incidental transitive availability, workspace hoisting, global
installation, ambient search paths, and another package's declaration are not
satisfaction evidence.

Classify runtime, build, test, development, generated, optional, and system
requirements from actual consumer and lifecycle facts. Do not infer ownership
or criticality from repository layout, dependency category, package-manager
convention, or current installation state.

## Candidate Selection

Compare supported candidates against the complete requirement. Applicable
facts may include capability and API fit, target support, maintenance and
support commitments, license, security evidence, provenance, transitive and
operational cost, performance, size, interoperability, release model,
migration cost, and independent-consumer constraints.

Use only facts material to the selected contract and record the decision
proportionally to its risk. Popularity, recency, download count, line count,
transitive count, standard-library status, ecosystem ranking, or one maintainer
signal cannot select or reject a candidate by itself. Do not choose an
in-house implementation, incumbent package, largest framework, smallest
package, or first available alternative as fallback.

Inspection output is candidate evidence, not selection authority. A dependency
graph, reverse-dependency path, transitive count, or standard-library
alternative can inform applicable contract facts but cannot independently
accept or reject a candidate.

## Implementation Versus Dependency

Treat a decision to implement difficult standardized semantics locally instead
of adopting an established implementation as a dependency-selection decision.
This applies to schemas, protocols, parsers, serializers, cryptography,
scheduling, and comparable domains where correctness depends on a substantial
external or standardized semantic surface.

Compare the local implementation and candidate dependencies against the same
complete requirement, including:

- required semantic surface and extension behavior;
- conformance, compatibility, and official or independent test support;
- supported targets, provenance, and licenses;
- update, vulnerability, and security-response ownership;
- failure and unsupported-domain behavior;
- implementation and long-term maintenance cost; and
- the continuing cost of keeping a local subset correct.

Record why the selected option satisfies the requirement and how its semantic
claims will be maintained. A preference against dependencies, a small current
input set, sunk implementation cost, or absence of an immediate failing test
does not justify local implementation. If required candidate or maintenance
facts are missing, return `unavailable`; if no supported option meets the
requirement, return `unsupported`; and if the decision contradicts known
contract facts, return `invalid`.

Apply this comparison when creating a local standardized implementation,
materially extending its semantic surface, or renewing its dependency and
maintenance decision. The later existence of a candidate dependency does not
by itself require automatic deletion of an unchanged accepted local
implementation; re-evaluate it at one of those lifecycle triggers against the
current requirement and ownership facts.

A thin Adapter that delegates the standardized semantics to an established
dependency is not a second implementation of those semantics. A
domain-specific product may own distinct local semantics even when it uses an
established dependency internally. Judge both by their real Interface,
delegation, added behavior, failure contract, and maintenance ownership. Do not
describe a pass-through reimplementation as an Adapter or invent nominally
distinct domain behavior merely to avoid the dependency comparison.

## Resolution And Reproducibility

Select manifest constraints, lock or snapshot material, feature sets, target
variants, source identity, integrity data, and resolver mode from the artifact,
consumer, release, and deployment contracts. Applications, published
libraries, tools, system packages, and independently resolved consumers may
require different strategies.

The selected resolution must be reproducible to the degree required by its
claim and must preserve enough identity to audit the dependency actually
consumed. Do not impose one lockfile, exact pin, version range, workspace
override, update cadence, registry, or resolver command universally. Do not
silently use an unlocked, cached, ambient, transitive, global, or alternate
resolution when required material is missing.

## Compatibility And Lifecycle

Define update, replacement, and removal obligations from every owned consumer,
published contract, persisted or wire representation, generated artifact,
supported target, and deployment unit affected by the dependency. Candidate
version labels and changelogs are inputs; they do not prove compatibility.

Before mutation, identify the current consumed identity, proposed identity,
contract changes, migration requirements, rollback or recovery authority, and
claim-matched evidence. Resolve the candidate in an isolated or reviewable
state when the selected tool supports it. Do not update an unrelated
dependency, broaden constraints, accept a resolver-selected version, or retain
an incumbent solely because compatibility evidence is unavailable.

Removal proves that declarations, lock or snapshot material, feature
selection, generated output, code paths, tooling, release artifacts, and owned
consumer references no longer require the dependency. Search results and
unused-dependency tools are supporting evidence, not complete removal proof.

## Features And Footprint

Select features, optional capabilities, default-feature behavior, target
variants, and dependency placement from actual consumer requirements. Measure
transitive graph, build, binary, bundle, startup, memory, operational, and
support effects only when material to the contract.

Feature gating, dependency splitting, standard-library use, in-house
implementation, and framework avoidance are mechanisms, not defaults. A
library's reusable consumer surface may impose different footprint and target
constraints from an application, but repository layer or artifact label alone
does not select a threshold.

Do not use fixed line counts, transitive counts, package sizes, download
trends, release ages, maintainer counts, or "one purpose" labels as automatic
selection or rejection rules.

## Audit And Review

Derive audit scope and cadence from provenance, security, licensing,
maintenance, compatibility, support, release, and operational risk. Record
which identities and consumers were examined, the authoritative evidence,
findings, disposition owner, deadline or acceptance condition, and required
follow-up.

Automated vulnerability, license, provenance, unused, duplicate, outdated, and
footprint tools prove only their declared detection contracts. Manual review
may cover context unavailable to tools. Neither tool output nor absence of a
finding proves that every dependency obligation is satisfied.

Classify findings through their canonical owner. Security owns vulnerability
and trust response, Licensing owns legal obligations, Release owns publication
effects, and Dependencies owns selection and lifecycle consequences. Do not
silently ignore findings, upgrade everything, remove a dependency, or accept a
warning because a conventional severity or schedule says so.

## Automation And Bootstrap

Automation implements selected dependency checks and procedures; it does not
create policy. Each check declares its owner, inputs, required capability,
environment, evidence, and blocking or advisory outcome. Select local, commit,
pull-request, scheduled, release, or manual execution from the claim and cost.

Tools required to execute dependency checks are dependencies themselves. Give
them explicit ownership, resolution, provisioning authority, and satisfaction
evidence. Do not install audit tools implicitly in a check, depend on ambient
global tools, copy a universal CI workflow, or treat tool startup as proof of
the dependency claim.

## Satisfaction And Provisioning

Define satisfaction evidence for each requirement before provisioning. A
binary presence check, import, version string, manifest entry, lockfile entry,
service response, or package-manager status is sufficient only when the
requirement contract says it proves the required capability and identity.

Install, update, repair, or remove a dependency only with explicit operator or
automation authority and a selected procedure. Re-check the complete
satisfaction contract after mutation and preserve the procedure's diagnostics
and terminal outcome. An already satisfied requirement may be reported without
mutation; an unsupported or inapplicable requirement is not a successful
no-op.

Do not install implicitly during build or run, auto-escalate privileges,
replace a selected dependency, change registries, broaden versions, mutate
unrelated dependencies, or treat attempted installation as proof of success.

### Provisioning Procedure

Represent each requirement as an independently identifiable unit with its own
satisfaction contract and, when provisioning is authorized, its own selected
mutation procedure. Evaluate every declared requirement independently so an
already satisfied requirement is not mutated merely because another
requirement is missing. Grouped resolution or installation is permitted only
when the selected tool owns that transaction and preserves per-requirement
identity, evidence, diagnostics, and terminal outcomes.

The procedure order is:

1. evaluate the declared satisfaction contract;
2. report the accepted already-satisfied outcome without mutation, or identify
   the missing or invalid evidence;
3. obtain explicit mutation authority and execute the selected procedure only
   for requirements that need it;
4. re-evaluate the same satisfaction contract after mutation; and
5. preserve any resolver, provisioning, or verification failure as the
   requirement's terminal outcome.

Function names, process exit codes, command names, status labels, and output
format are projections selected by the owning language, tool, application, or
operator contract. They are not universal dependency policy. A Launcher action
may expose the accepted procedure, but it cannot create missing authority,
replace the satisfaction contract, combine unrelated requirements into one
opaque result, or reinterpret failure as success.

## Typed Outcomes

Return typed `invalid` for contradictory requirements, ownership, constraints,
or authorization; typed `unsupported` when no supported candidate or procedure
meets a valid declared requirement; and typed `unavailable` when required
candidate, resolver, identity, provisioning capability, or evidence cannot be
established. Preserve resolver, verification, and consumer failures when they
are more specific.

Do not continue with an incumbent, transitive, cached, global, standard-library,
in-house, alternate-registry, alternate-version, successful-no-op, skipped
verification, or default-success fallback.

## Verification

Evidence covers applicable:

- requirement and narrow execution-boundary ownership;
- candidate comparison against all material constraints;
- selected source, identity, constraints, features, and target variants;
- reproducible resolution and consumed-artifact identity;
- already-satisfied, missing, unsupported, invalid, and unavailable outcomes;
- explicit mutation authority and post-mutation satisfaction;
- update and removal effects on every owned consumer; and
- compatibility and migration effects across independently changing contracts;
- selected feature and footprint behavior where material;
- audit findings, ownership, disposition, and follow-up;
- automation environment, bootstrap dependencies, and blocking semantics; and
- rejection of ambient, transitive, global, alternate, privilege, and
  default-success fallbacks.
````

### topic.licensing

````markdown
# Licensing

**Standards metadata**

- ID: `topic.licensing`
- Role: `topic`
- Level: `MUST`
- Applies when: A change selects, incorporates, adapts, modifies, generates from, redistributes, or publishes third-party code, data, media, documentation, models, or other licensed material.
- Does not apply when: The change uses only material owned by the project and creates no third-party license or notice obligation.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Provenance, license-authority, compatibility, obligation, attribution, and distribution decision fixtures plus affected artifact evidence.
- Canonical owner: `topics/licensing.md`

## Authority And Ownership

Identify the material, source, version or revision, copyright and notice
material, and authoritative license terms before incorporation or
distribution. A repository label, package metadata field, catalog entry,
license name, source comment, or remembered convention is evidence only when
the applicable authority makes it so.

Licensing owns provenance, authoritative terms, intended-use and distribution
compatibility, resulting obligations, and attribution requirements.
Dependencies may use licensing facts when selecting a dependency.
Documentation and Release project accepted notices and obligations into their
owned artifacts; they do not decide compatibility or invent terms.

## Compatibility And Obligations

Evaluate the authoritative terms against the actual activity and artifact:
use, modification, combination, linking, generation, embedding, redistribution,
publication, target recipients, source availability, and other material
conditions. Select only facts applicable to that contract.

Do not infer compatibility from a fixed license-name matrix, labels such as
permissive or viral, a dynamic-versus-static linking slogan, project
popularity, or a prior use in another artifact. When interpretation requires
legal authority beyond the project's accepted policy, record the unresolved
decision and route it to the designated legal or licensing owner.

Record every accepted obligation at the narrowest artifact or distribution
boundary that must satisfy it, including required notices, attribution,
license-text inclusion, source or modification information, offer or
availability duties, and propagation conditions when the authoritative terms
actually require them.

## Attribution And Provenance

Preserve enough provenance to identify the incorporated material and verify
the applicable terms. Place attribution and notices where the authoritative
terms and selected distribution contract require them. Keep adapted scope and
material modifications traceable when needed to distinguish project work from
third-party work or satisfy an obligation.

Do not require one copied file-level or function-level template. Do not omit,
relocate, summarize, or rewrite required legal text merely to fit a preferred
documentation layout. Non-normative examples may illustrate an already
selected obligation but cannot establish one.

## Typed Outcomes

Contradictory source, identity, provenance, or obligation facts are `invalid`.
A well-formed proposed use or distribution that the authoritative terms do not
permit is `unsupported`. Missing source identity, authoritative terms,
required interpretation authority, or obligation evidence is `unavailable`.

Do not continue with guessed terms, a similar license, a package-manager label,
an incumbent attribution, a copied matrix, omitted notices, or default
compatibility.

## Verification

Evidence covers the exact material and revision, authoritative terms, declared
activity and distribution, compatibility decision, applicable obligations,
required notice contents and placement, and the produced artifact or
distribution surface. Negative evidence covers unknown or conflicting
provenance, missing terms, unsupported activity, missing obligations, stale
notices, and attribution attached to the wrong material or artifact.
````

### topic.accessibility

````markdown
# Accessibility

**Standards metadata**

- ID: `topic.accessibility`
- Role: `topic`
- Level: `MUST`
- Applies when: A change creates or changes a user-facing task, interaction, content, control, status, notification, or accessibility claim.
- Does not apply when: The change has no user-facing behavior or accessibility claim and cannot affect access to a supported user task.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Accessibility contract decision fixtures plus claim-matched evidence for the selected users, tasks, platforms, modalities, capabilities, and conformance obligations.
- Canonical owner: `topics/accessibility.md`

## Accessibility Authority

Accessibility owns the outcomes required for supported users to perceive,
understand, navigate, operate, and receive the results of user-facing behavior.
Define those outcomes from the product contract and affected user tasks before
selecting an interface mechanism.

An accessibility contract identifies the supported users and tasks, relevant
content and controls, supported platforms, required interaction and perception
modalities, available assistive capabilities, selected conformance obligations,
and evidence needed to establish the claim. Do not infer that contract from the
current interface technology, one input method, one assistive technology, or a
general statement that the interface is accessible.

## Outcome And Modality Selection

Select required outcomes and modalities from actual user, product, platform,
and regulatory or organizational obligations. Visual, auditory, tactile,
pointer, keyboard, switch, voice, and programmatic access are possible contract
dimensions, not a universal checklist. Support for one modality does not prove
equivalent access through another.

An external accessibility standard or conformance level applies only when the
project contract selects its authority, scope, version, target platform, and
evidence obligations. Do not silently select, upgrade, weaken, or substitute an
external standard when those facts are absent.

## Semantic Meaning And Role

Expose each user-facing element's purpose, role, relationships, value, state,
availability, and change through every modality required by the accepted
contract. Derive that meaning from the user task and observable behavior, not
from appearance, event-handler name, current widget, or implementation type.

Use a platform-native mechanism when it satisfies the complete selected
meaning, modality, state, feedback, and lifecycle contract. A native mechanism
is preferred only on that evidence; semantic markup, an accessibility API role,
or a conventional control is not a universal mechanism and does not prove the
outcome by itself.

## Action And Navigation Outcomes

Classify an interaction by its user-visible result. An action changes
application state or performs an operation. Navigation changes the user's
location or active destination. A control that can do both declares the
conditions, resulting state, destination, feedback, and required modalities
for each outcome.

Do not select action or navigation semantics from visual styling, click
handling, a URL-shaped value, or an incumbent element. Do not substitute one
outcome for the other when the required platform mechanism is unavailable.

## Custom Interaction Outcomes

A custom interaction is permitted only when supported mechanisms cannot satisfy
the accepted task and its implementation covers the complete selected role,
state, value, relationships, activation, modalities, feedback, focus or
position lifecycle, cancellation, and failure outcomes.

Support through one event, input method, visual state, role declaration, or
assistive mechanism does not prove another modality or the complete custom
interaction. Missing required capability or evidence is a typed outcome, not
authority to omit behavior or emulate a nearby control incompletely.

## Input Modality Equivalence

For every required modality, define how a user reaches, identifies, activates,
adjusts, cancels, and receives feedback from the interaction. Preserve task
order, state effects, and failure outcomes across modalities where the contract
requires equivalent access. Support through pointer activation, a click event,
or one native control does not establish another input modality.

Keyboard, switch, voice, touch, pointer, and programmatic interaction are
selected capabilities, not mutual substitutes or universal requirements. When
a required modality cannot be supported or established, return its typed
outcome instead of omitting it or treating another modality as sufficient.

## Focus Visibility And Authority

When the selected interaction model has an active position or focus concept,
assign authority for its current target and make that target perceivable through
the required modalities and states. Visibility must remain distinguishable in
the supported environment and must not depend only on color, pointer hover, or
an implementation-specific default unless the accepted contract proves it.

Removing, hiding, or moving focus is valid only as part of an owned transition
that preserves task continuity and feedback. Styling, browser defaults, or a
successful focus API call alone do not prove visibility or correct authority.

## Focus Lifecycle

For composite, transient, modal, or dynamically replaced interactions, define
the initial target, movement boundaries, active-order behavior, dismissal and
cancellation, restoration destination, target removal, nested interaction, and
failure outcomes from the user task and supported platform.

A fixed trap, first-control target, Escape binding, return-to-trigger rule, or
DOM-presence check is a possible mechanism, not a generic lifecycle contract.
If the authoritative target no longer exists, resolve the next target through
the selected task lifecycle or return a typed diagnostic; do not silently lose
or guess focus.

## Names And Descriptions

Provide each user-facing control, region, status, and task-relevant item a name
or description sufficient to distinguish its purpose, scope, current target,
and effect through every required modality. Names remain stable enough for task
continuity and update when the represented purpose or state changes.

Visible text, hidden text, platform naming APIs, associated content, and
generated descriptions are mechanisms. A role, icon, position, implementation
identifier, or generated default does not independently establish a meaningful
name. Do not expose internal detail as a substitute for user-task meaning.

## Input Relationships And Instructions

For user input, expose the relationship among the input, its purpose, name,
instructions, units or format, constraints, current value, validation state,
errors, and recovery action through the required modalities. Preserve those
relationships when layout, state, content, or validation changes.

Visual proximity, placeholder content, color, field order, or one assistive
projection does not prove the relationship. If required naming, instruction,
state, or error capability is missing, return a typed outcome rather than
accepting an unlabeled or ambiguously associated input.

## Media Meaning And Classification

Classify media, imagery, icons, animation, audio, and visual or auditory effects
from the meaning and function they contribute to the user task in context.
Informative media contributes content, status, identity, instruction, or
function. Decorative media contributes no task-relevant meaning after the
surrounding context and supported modalities are considered.

Classification is an owned content decision, not a property of file type,
component name, placement, repetition, visual subtlety, or library convention.
Re-evaluate it when content, context, state, or function changes.

## Equivalent Media Outcomes

For informative or functional media, provide the selected users an equivalent
task outcome through every required modality, preserving relevant meaning,
state, timing, controls, and change notification. For decorative media, prevent
the mechanism from introducing misleading or redundant meaning where the
selected platform supports that projection.

Alternate text, captions, transcripts, descriptions, hidden semantics, visible
labels, and adjacent content are mechanisms selected from the media and task
contract. An empty string, filename, icon-library default, nearby visual text,
or successful API attribute does not independently prove classification or
equivalence.

## Accessibility Evidence Claims

Define evidence from each accepted accessibility outcome, affected users and
tasks, supported platforms and modalities, relevant states, failure paths, and
conformance obligations. Select automated, manual, assistive-technology, user,
inspection, or combined evidence only for the claims each method can establish.

Tooling selects and orchestrates lint products, rules, severity, scope, commands,
and schedules. Verification owns evidence kind, environment, execution, and
acceptance meaning. Accessibility owns the user-access claim those systems
consume. A configured plugin, named rule set, zero lint findings, CI execution,
or successful command does not prove a broader accessibility outcome.

## Responsibility Boundaries

Accessibility owns required user-access outcomes and conformance obligations.
Application, frontend, language, and framework profiles own concrete semantic,
interaction, rendering, platform, and assistive-technology mechanisms. Tooling
owns selected lint and automation execution. Verification owns the evidence
plan and acceptance claim. Documentation records durable accessibility
contracts and decisions when they cannot be recovered from implementation and
evidence.

A mechanism such as semantic markup, an accessibility API, keyboard handling,
focus management, captions, alternate text, automated linting, or a manual
assistive-technology check is evidence or implementation only for the outcomes
its selected contract covers. No mechanism, tool, browser, framework, input
method, assistive technology, or passing check independently defines or proves
the complete accessibility contract.

## Typed Outcomes

Return typed `invalid` for contradictory users, tasks, modalities, conformance,
or authority requirements. Return typed `unsupported` when a valid required
outcome cannot be provided by the selected product or supported platform.
Return typed `unavailable` when required users, tasks, platform facts,
capabilities, conformance authority, or claim-matched evidence cannot be
established.

Do not continue by assuming a web interface, a particular external standard,
one input modality, one assistive technology, a conventional lint configuration,
weaker evidence, omitted behavior, or default success.

## Verification

Evidence covers the selected users and tasks, supported platforms, required
modalities and capabilities, applicable conformance obligations, successful and
unsuccessful outcomes, and any mechanism-specific claims. Automated checks,
manual review, assistive-technology exercises, and user evaluation prove only
their declared scope; select and combine them from the accepted claim.
````

### profile.boundary.persistence

````markdown
# Persistence Boundary Profile

**Standards metadata**

- ID: `profile.boundary.persistence`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A change creates or changes a durable read, write, publication, transaction, migration-application, version-ledger, or store-mutation boundary.
- Does not apply when: State is proven process-local and ephemeral, or the change preserves every selected durable-state mechanism and contract unchanged.
- Requires: `core`, `workflow.verification`, `topic.contracts`, `topic.contracts.evolution`
- Specializes: `topic.contracts`
- Verification: Persistence owner decisions plus claim-matched durable source, destination, publication, interruption, and reopening evidence.
- Canonical owner: `profiles/boundaries/persistence.md`

## Concurrent Durable Updates

When two writers can update the same invariant, a read followed by an
unconditional write can lose an update. For example, both writers reading
revision 7 and saving a new balance must not silently overwrite one another.
Use a conditional revision update and check that it succeeded, or a transaction
whose isolation and locking protect the entire invariant. A uniqueness check
followed by a separate insert is subject to the same race; enforce uniqueness
at the durable boundary.

On a retryable conflict, re-read and re-evaluate the whole transaction within
a bounded budget. Do not retry only the final statement using stale decisions,
and do not repeat nontransactional external effects without their own
idempotency or coordination contract. Test concurrent writers and aborted
transactions against the actual store guarantees.

## Durable Boundary Authority

Treat state as durable when a supported consumer can observe it after the
operation, process, deployment, or runtime that produced it has ended. Before
selecting a persistence mechanism, establish the authoritative source and
destination states, supported versions, required durable invariants, mutation
and publication authority, available store capabilities, and acceptance
evidence.

A configured store, existing table, file path, transaction API, migration
directory, or prior implementation does not select the mechanism. Use the
[Contracts topic](../../topics/contracts.md) to select supported states,
evolution, and compatibility before applying this profile.

## Select The Durable Mechanism

Select the mechanism from the owned invariant and proven capabilities. Record:

- which state is authoritative before and after the operation;
- which component may read, stage, publish, replace, or remove each durable
  representation;
- the atomicity, integrity, ordering, interruption, and reopening guarantees
  the operation requires;
- the versions and persisted states the current contract supports;
- the store guarantees actually available in the required environment; and
- the evidence that proves the selected postcondition to its consumers.

The selected contract may use a transaction, atomic replacement, append-only
record, journal, object publication, explicit version ledger, or another proven
mechanism. None is a universal default. If no durable state crosses the
boundary, do not introduce persistence work merely because a store is present.

## Durable Mutation Contract

For each durable mutation, define the authoritative precondition, accepted
postcondition, integrity constraints, publication boundary, interruption
behavior, and proof required by actual consumers. Select operation structure
from those facts and the available store guarantees. Gathering, validation,
isolated staging, publication, and postcondition proof are distinct
responsibilities when the selected contract requires them; they are not a
mandatory five-phase implementation sequence.

Complete every precondition and input proof that must hold before publication.
Staging may use incomplete representations only when they are non-authoritative,
unobservable to consumers, bounded by an owned lifecycle, and either completed
or removed according to the selected failure contract. Never publish a
placeholder or temporarily invalid representation as authoritative state.

Publish through a mechanism that makes the selected postcondition observable
without exposing a prohibited partial state. A transaction, atomic replacement,
journal, or append-only operation satisfies this requirement only when its
proven guarantees match the complete invariant. Successful API return, an
allocated identifier, or completion of one write does not prove related
indexes, references, records, or metadata are consistent.

Run every proof required for authoritative correctness in each supported
production path. Optional debug audits may add evidence, but they cannot replace
required runtime validation or postcondition proof. If publication may have
partly occurred or its outcome cannot be established, do not report success or
continue from guessed state; preserve the typed outcome for the owning recovery
contract.

## Migration Execution Contract

Execute a migration only for source and destination states selected by
Contracts. Before mutation, prove the authoritative current state, applicable
migration identity and integrity, deterministic dependency and ordering facts,
required store capabilities, ledger consistency, and coordination authority.
A migration directory, filename sort, pending row, startup hook, or newer
application version does not prove those facts.

Give each selected migration stable identity under the applicable contract and
verify that the artifact to execute is the accepted artifact. Define how changed,
missing, duplicate, or conflicting identities are classified. Discover and
order migrations from explicit accepted metadata or another deterministic
contract; do not infer authority from filesystem enumeration or an incidental
lexical order.

Keep durable state and its migration ledger consistent at every authoritative
publication boundary. Record completion only after the destination postcondition
is proven. Re-entry behavior is selected per migration: proven idempotent
application, one-shot rejection, continuation from an owned checkpoint, or
another explicit mechanism. Prior attempt, process restart, or an apparently
pending ledger entry does not authorize repeated application.

Define interruption and unknown-outcome handling before execution. Preserve the
observed source, destination, and ledger facts for Resilience to select recovery;
do not delete, rebuild, roll back, roll forward, or mark completion by default.
The caller that owns an accepted lifecycle trigger invokes migration execution.
Application startup is one possible trigger, not migration authority or a
universal execution phase.

Contracts determines whether different application versions or retained states
must coexist. Derive overlap handling from actual deployment and consumer facts.
Additive shape, a default value, ignored data, a two-phase shim, or coordinated
replacement is safe only when the selected producer-consumer contract proves
it; none is a compatibility default owned by Persistence.

## Responsibility Boundaries

Persistence owns durable read, write, staging, publication, transaction,
migration-application, ledger, and store-adapter mechanisms. Contracts owns
supported state and evolution semantics. Resilience owns failure handling and
recovery. Concurrency owns overlapping access and coordination. Security owns
authorization. Build owns generated artifacts. Diagnostics owns reporting.
Verification owns evidence sufficiency.

This profile does not own every in-memory mutation and does not mandate a
database, transaction, migration framework or format, startup execution,
version table, rollback mechanism, compatibility window, or implementation
phase sequence.

## Typed Outcomes And No Fallback

Return `unavailable` when required authority, source or destination state,
durable invariant, store capability, ledger, coordination, or evidence cannot
be established. Return `invalid` for partial authoritative publication,
contradictory durable state or ledger facts, corrupt state, or incomplete proof.
Return `unsupported` when a well-formed persisted version or required mechanism
is outside the selected contract.

Do not fall back to partial writes, temporary invalid authoritative state,
debug-only validation, deletion or rebuild, guessed migration order, repeated
application, startup execution, default rollback, assumed additive
compatibility, a nearby weaker store, or speculative coexistence. Return the
typed diagnostic selected by the failed durable contract.

## Verification

Verify the claims selected for the changed boundary. Applicable evidence covers
authoritative source and destination state, precondition and postcondition
proof, isolated staging, interruption before and during publication, reopening
through real store adapters, supported and unsupported versions, overlapping
access, corrupt or contradictory state, and rejection of every prohibited
fallback.

Illustrative mechanism adaptation belongs in the non-normative
[Persistence Mechanism Recipes](../../reference/recipes/persistence.md).
````

### profile.application.frontend

````markdown
# Frontend Application Profile

**Standards metadata**

- ID: `profile.application.frontend`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A web or web-technology user interface, component, rendering path, interaction, frontend state projection, or frontend test changes.
- Does not apply when: No user-interface projection, interaction, frontend state, or frontend-owned evidence changes.
- Requires: `core`, `workflow.verification`, `topic.accessibility`
- Specializes: `topic.contracts`, `topic.accessibility`
- Verification: Frontend authority, projection, synchronization, interaction, accessibility, and evidence decision fixtures plus affected component and real-browser evidence.
- Canonical owner: `profiles/applications/frontend.md`

Select [Contracts](../../topics/contracts.md) when this change affects a runtime
boundary, domain invariant, public representation, or compatibility promise.
A local presentation or implementation change does not select that topic by
itself. The specialization applies when the corresponding concern is affected.

## Applicability Decision

Apply this profile when a change creates or alters a web or web-technology UI
projection, presentation-state owner, rendering lifecycle, user interaction,
frontend synchronization path, or frontend-specific evidence claim. Determine
applicability from the changed responsibility and observable behavior, not from
a product label, executable type, repository directory, or named container
technology.

A browser, embedded web view, desktop shell, or hybrid application is not
automatically in scope when the change has no frontend responsibility. A
frontend remains in scope when its UI mechanism is hosted outside a conventional
browser. Domain, persistence, transport, and native-host changes retain their
own owners even when a frontend consumes their results.

Missing responsibility or boundary facts are `unavailable`; contradictory
ownership is `invalid`; and a selected UI requirement that the supported
platform cannot represent is `unsupported`. Do not assume browser behavior,
copy a neighboring product profile, infer scope from Electron, Tauri, WebView,
or another framework name, or silently treat a cross-boundary change as
frontend-owned.

## Projection Authority

A frontend projects canonical application and domain state into a user
interface and translates user interaction into declared actions. It owns
presentation state, rendering lifecycle, interaction adaptation, and
frontend-specific evidence. It does not own domain behavior, persistence,
transport, runtime decoding, or accessibility policy.

Select the authoritative state and action contract before selecting a
framework mechanism. Independently produced input requires Contracts-owned
runtime proof before it becomes frontend state. Do not infer domain authority
from the rendered tree, duplicate backend rules in components, or treat a
TypeScript type as runtime proof.

## Rendering And Synchronization

Prefer declarative projection when the selected framework can express the
required output and lifecycle. Direct DOM, canvas, WebGL, native-widget, or
other imperative access is valid when the interaction or rendering contract
requires it and ownership, cleanup, and synchronization are explicit.

Select rendering from the authoritative state, required output, interaction,
lifecycle, platform capability, and evidence. Declarative bindings do not
become state authority, and imperative access does not authorize reconstruction
from the rendered tree. Isolate mechanism-owned mutation from declarative
ownership only when the selected renderer requires it, and prove cleanup and
reconciliation at that boundary.

Synchronize from authoritative state through the selected event, subscription,
query, or boundary mechanism. Polling is valid only when the source contract is
pull-based or no supported event mechanism satisfies the requirement. Its
owner, cadence, cancellation, stale-result handling, and terminal outcomes
must be explicit.

Event delivery, subscriptions, direct queries, and polling are alternatives
selected by the source and consumer contracts; none is a universal preference.
A pull-style FFI or message drain remains a boundary adapter and does not
authorize a second UI polling loop. The synchronization mechanism must preserve
ordering, duplicate, stale-result, cancellation, and unavailable-source
outcomes required by its owners.

Do not use a second UI store, DOM reads, global timer, copied response, or
periodic reconciliation as fallback for missing authority or synchronization.
Do not switch between declarative and imperative rendering, event and polling,
or push and pull sources when the selected mechanism is unavailable. Return
`invalid` for contradictory authority, unsafe mutation, stale application, or
incomplete lifecycle; `unsupported` for a valid requirement outside platform
capability; and `unavailable` for missing authority, source contract,
mechanism, lifecycle, or evidence.

Illustrative mechanisms are isolated in the
[Frontend mechanism recipes](../../reference/recipes/frontend.md).

## Lifecycle-Owned Frontend Work

For timers, polling, subscriptions, observers, animation callbacks, and other
work that can outlive one immediate call, identify the frontend owner, protected
state, invocation authority, start condition, completion, cancellation,
supersession, dependency change, teardown boundary, and terminal outcomes.
Concurrency owns generic work lifecycle; TypeScript Async owns TypeScript
invocation and result-application mechanisms.

Select a resource holder and cleanup trigger from the framework and lifecycle
contract. A ref, component state, field, closure, abort signal, generation
token, or owner object is a mechanism, not a default. Completion, dependency
change, unmount, shutdown, retry, and replacement require cleanup only when they
end or supersede the selected ownership interval.

Prevent duplicate active work and stale result application through proven
identity and lifecycle authority. Clearing a timer, returning from a callback,
or observing one successful update does not prove cancellation, terminal
classification, cleanup, or exclusion of a superseded result.

Missing owner, identity, lifecycle, cleanup capability, or evidence is
`unavailable`; contradictory ownership, duplicate work, stale application,
unobserved completion, or incomplete cleanup is `invalid`; and a valid
lifecycle unsupported by the selected mechanism is `unsupported`. Do not
fall back to a global timer, fixed cadence, ref holder, state holder, silent
stale-result discard, retry, detached work, or default success.

## Interaction And Accessibility

Project every supported interaction through declared action and state
transitions. Select pointer, keyboard, focus, gesture, and assistive-technology
mechanisms from the component and Accessibility contracts. Visual behavior
alone is not interaction proof.

An unsupported interaction or platform capability returns the declared
`unsupported` outcome. Contradictory ownership, inaccessible required
interaction, or ambiguous action mapping is `invalid`. Missing authoritative
state, decoder, lifecycle, capability evidence, or required browser evidence
is `unavailable`.

Do not silently omit an applicable interaction, install an inert control,
substitute a pointer-only path, or report success from a visual snapshot.

## Evidence

Use the narrowest evidence that proves the changed claim:

- pure projection and state transitions may use deterministic component tests;
- user-visible semantics require role, name, state, and interaction evidence;
- geometry, focus, pointer capture, browser APIs, rendering engines, and
  embedded controls require evidence in an environment that implements them;
- backend-to-frontend flows require evidence through the real contract and
  projection boundaries.

Selectors and simulation tools are mechanisms. Choose them from the behavior
under test and do not treat a preferred query API, synthetic event, DOM shim,
snapshot, or component mount as universal evidence.

Select interaction evidence from the user-observable contract. Semantic
controls require accessible role, name, state, focus, keyboard, and activation
evidence for every applicable interaction path. Embedded controls inside
draggable, pannable, zoomable, or canvas-style containers also require pointer
capture and release, focus and escape, and parent-gesture conflict evidence.
A selector or event-dispatch API is not evidence unless its semantics match the
claim.

Browser geometry, layout, pointer capture, focus transfer, rendering-engine,
and browser-API claims require a representative browser environment. Pure
geometry functions may be proved deterministically, but mocked rectangles or a
DOM shim do not prove browser integration. If the required environment is not
available, report `unavailable` instead of substituting component success.

Polling, timers, subscriptions, observers, and other lifecycle-owned work
require evidence that completion, dependency change, retry, cancellation, and
unmount release the resource, prevent duplicate work, and exclude stale
results. A successful update does not prove cleanup.

## Typed Outcomes

Preserve typed `invalid`, `unsupported`, and `unavailable` outcomes through the
UI contract. A presentation layer may map them to declared user-facing states,
but must not convert them to stale content, empty success, guessed defaults,
silent omission, or an alternate interaction.

Evidence covers successful projection, invalid input, unsupported
capabilities, unavailable dependencies, lifecycle cleanup, repeated
invocations without state carry-forward, and the real environment for claims
that component-level simulation cannot prove.
````

### profile.language.rust

````markdown
# Rust Language Profile

**Standards metadata**

- ID: `profile.language.rust`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust source, Cargo metadata, or Rust-generated artifacts change.
- Does not apply when: No Rust-owned artifact changes.
- Requires: `core`
- Specializes: `none`
- Verification: Affected Cargo formatting, lint, build, and test commands pass.
- Canonical owner: `profiles/languages/rust/README.md`

This profile owns Rust mechanisms. Cross-language policy remains in Core,
workflows, application profiles, boundary profiles, and topics.

## Baseline Rust Change

For a local library bug fix:

1. Use the existing crate and workspace ownership boundaries.
2. Add a focused Rust regression test.
3. Run formatting for affected Rust files or the workspace.
4. Run Clippy for the affected package/targets with repository-configured
   warnings.
5. Run the focused test and affected package tests.
6. Run broader workspace checks only when shared contracts or workspace wiring
   changed.

Do not require `--all-features` when declared features are mutually exclusive.
Test default, no-default, individual, and explicitly supported combinations
according to the crate's feature contract.

## Rust Invariants

- Prefer validated types and checked conversions at boundaries.
- Route public or boundary-facing Rust type, trait, parameter, conversion,
  visibility, result, panic, feature, and Rustdoc mechanisms through the
  [Rust API profile](api.md).
- Route Cargo declaration, workspace, resolver, dependency-graph, audit-adapter,
  and build-cost measurement mechanisms through the
  [Rust Dependency profile](dependencies.md).
- Route Rust toolchain, Cargo release metadata, publication-control,
  release-adapter, and release-evidence mechanisms through the
  [Rust Release profile](release.md).
- Route Rust and Cargo formatting, lint, test-runner, feature-matrix,
  benchmark, coverage, diagnostic, and build-script adapter mechanisms through
  the [Rust Tooling profile](tooling.md).
- Route async API and suspension-boundary selection through the
  [Rust Async profile](async.md).
- Route Rust target selection, configuration placement, and target evidence
  through the [Rust Cross-Platform profile](cross-platform.md).
- Give async runtimes and spawned tasks explicit lifecycle owners.
- Do not hold synchronous guards across `.await`.
- Deny unsafe by default and route legitimate unsafe work through the
  [Rust Unsafe profile](unsafe.md).
- Route raw foreign memory, checked dimensions, and callback borrows through
  the [Rust Interop profile](interop.md).
- Route untrusted dimensions, counts, offsets, strides, and lengths through
  the [Rust Security profile](security.md) before arithmetic or resource use.
- Route Rust host representations and cross-language conversions through the
  [Rust Language Binding profile](language-bindings.md).
- Keep generated bindings derived and test both native and host sides when that
  boundary changes.

## Canonical Routing And No Legacy Authority

This profile and the specialized profiles linked above are the canonical Rust
mechanism owners. Files under the legacy Rust standards directory are
non-normative migration indexes; they do not own Rust policy or supply a route
when canonical facts are missing.

Return typed `unavailable` when the required owner, applicability, or capability
facts cannot be established, typed `invalid` when routing facts contradict, and
typed `unsupported` through the selected owner when a required mechanism is not
supported.

Do not fall back to a legacy Rust file, a nearby profile, every Rust profile, or
a default runtime, tool, target, feature matrix, benchmark adapter, unsafe
policy, or verification command.
````

### profile.language.rust.async

````markdown
# Rust Async Profile

**Standards metadata**

- ID: `profile.language.rust.async`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust code changes an asynchronous API, suspension boundary, concurrent I/O contract, stream, backpressure, cancellation-aware operation, or async resource lifetime.
- Does not apply when: The affected Rust behavior is synchronous and does not select or change an asynchronous contract or mechanism.
- Requires: `core`, `workflow.verification`, `topic.concurrency`, `profile.language.rust`
- Specializes: `topic.concurrency`, `profile.language.rust`
- Verification: Rust async-boundary, lifecycle, blocking-isolation, and synchronization decisions plus affected API, cancellation, integration, and shutdown tests.
- Canonical owner: `profiles/languages/rust/async.md`

## Select The Execution Contract

Select synchronous or asynchronous behavior from:

- whether the operation suspends for I/O or scheduling;
- whether concurrent I/O, streaming, or backpressure is part of the contract;
- caller and consumer deployment/API constraints;
- cancellation and lifecycle obligations; and
- supported execution capabilities.

Do not add `async` merely because a caller is asynchronous. Do not remove
`async` merely to satisfy a blanket synchronous-core preference.

## Keep Non-Suspending Logic Synchronous

Parsing, validation, transformation, policy, and other pure logic remain
synchronous when they have no suspension, concurrency, cancellation, or async
resource-lifetime contract. An async shell may call that synchronous logic
without making the inner operation asynchronous.

A function with no suspension point requires an explicit contract reason to be
async. Caller convenience alone is not sufficient.

## Preserve Genuine Async Contracts

An async core or library API is valid when concurrent I/O, streaming,
backpressure, cancellation, or an async resource lifetime is part of its
observable contract. Record that contract and verify it through the real
supported execution path.

Library ownership does not imply synchronous or asynchronous behavior by
default. Public API shape follows the library's consumer and lifecycle
contract.

## Runtime Composition

The adopting application's composition root owns runtime construction,
configuration, sharing, and shutdown. A library consumes an injected runtime
capability or exposes an async contract to its caller; it does not create a
process-global or alternate runtime to make an operation execute.

The composition owner records supported runtime capabilities and makes them
available to all operations that share that runtime. A request, task, binding,
or library call may use the selected capability without becoming the runtime
owner.

## Own Spawned Work

Every spawned task is registered with one lifecycle owner before it can outlive
its spawning scope. That owner:

- retains the task's completion capability;
- observes success, failure, panic, and cancellation;
- defines whether and when restart is valid;
- includes the task in shutdown; and
- releases tracking only after a terminal outcome is observed.

The concrete task set or handle type follows the selected runtime. Returning
from a spawn call, logging inside the task, or discarding a handle does not
establish ownership.

## Coordinate Shutdown

An owned shutdown sequence:

1. makes repeated shutdown requests idempotent or returns the same typed
   terminal outcome;
2. closes admission for new owned work;
3. signals cancellation through the selected mechanism;
4. drains and observes tracked work; and
5. reports complete, incomplete, or failed shutdown through typed outcomes.

A time limit does not itself authorize abort. Force-abort is permitted only
when the lifecycle owner has abort authority and the operation contract proves
that interruption cannot violate required consistency, durability, or release
obligations. Otherwise an incomplete drain remains a typed incomplete or
unavailable outcome for the owning operation.

## Isolate Blocking Work

Classify whether an operation can block its executing thread or consume
sustained CPU before placing it on an async execution path. Use a supported
async capability only when it preserves the operation's I/O, cancellation,
resource-lifetime, ordering, and failure contract.

The runtime composition and lifecycle boundary owns the isolation capability
for unavoidable blocking or CPU-heavy work. That capability defines admission,
capacity, completion observation, cancellation/shutdown behavior, and resource
accounting. Isolation without a bounded or otherwise governed capacity contract
is not sufficient.

Do not execute blocking work inline on an async request or lifecycle path. Do
not invoke or await blocking work while holding a synchronization guard.
Preserve related invariants through an appropriate ownership, coordination, or
transaction design rather than splitting the protected operation for
convenience.

## Select Synchronization From Contract

Select synchronization from:

- whether the protected critical section can suspend;
- the complete invariant and ownership boundary;
- contention and read/write behavior;
- fairness, poisoning, recovery, and cancellation obligations; and
- capabilities supported by the selected runtime and deployment.

A non-suspending critical section uses a mechanism that does not require
suspension support. A guard crosses suspension only when the selected mechanism
supports that behavior and the invariant requires the protected scope. If no
supported mechanism can preserve the invariant, redesign ownership or
coordination, or return the operation's typed unavailable outcome.

Do not call external, plugin, callback, or user-controlled behavior while a
guard is held. Do not select one synchronization implementation as a universal
default for all Rust state.

## Prove Cancellation State

Stopping or dropping future polling proves only that the future will not be
polled by that owner. It does not prove that external I/O, a remote request, a
blocking operation, or another independently owned side effect stopped or
rolled back.

Derive external cancellation and terminal-state claims from the affected
capability's contract and evidence. If external work may continue, preserve its
identity and ownership so completion, cancellation, reconciliation, or retry
can be handled explicitly.

## Preserve Durable Work

Before a durable multi-step operation crosses a cancellation point, select a
transactional, idempotent, resumable, or compensating design that preserves its
required invariant. A cancellation boundary cannot leave authoritative state
in an unclassified partial outcome.

## Own Asynchronous Cleanup

Cleanup that can suspend has an explicit lifecycle-owned completion path.
Synchronous destruction may release synchronous resources or enforce a local
safety invariant, but it does not stand in for required asynchronous cleanup.
Do not detach cleanup merely to let destruction or shutdown return.

## Own Lifecycle Evidence

The lifecycle owner observes health, success, failure, panic, cancellation, and
shutdown outcomes for its owned work. Leaf operations may emit diagnostic
context, but leaf logging does not establish terminal-state ownership or prove
that a failed task remains supervised.

Select health, telemetry, and inspection mechanisms from the operational
contract and supported environment. Tool availability is not evidence unless
the lifecycle owner consumes the relevant signal and connects it to an owned
operation and terminal outcome.

## Typed Outcomes

Return the operation's typed `unsupported` or `unavailable` outcome when its
required execution contract cannot be provided. Preserve operation-specific
failures when they are more precise. Runtime, task, and shutdown failures retain
their operation-specific terminal outcome. Missing blocking-isolation,
capacity, synchronization, cancellation, cleanup, or observation capability
remains explicit.

## No Fallback

Unresolved execution requirements cannot select sync, async, a thread, a
runtime, blocking, or detached work by convenience. Do not silently change the
API contract, block an async path, create a runtime, or discard owned work to
make the operation execute.

Missing lifecycle proof cannot create a library-global or alternate runtime,
detach work, treat leaf logging as ownership, discard failure or panic, keep
admission open while draining, or force-abort work without authority and
interruption safety.

Missing execution or synchronization proof cannot block inline, create an
alternate executor or thread, run unbounded isolated work, hold an unsupported
guard across suspension, split a related invariant, or select a universal
mutex.

Runtime construction, task ownership, shutdown sequencing, blocking isolation,
synchronization selection, cancellation safety, cleanup, and lifecycle
evidence are defined above without selecting a project-specific mechanism.

Missing cancellation or observation proof cannot assume external cancellation
from a dropped future, leave durable work unprotected, delegate async cleanup
only to synchronous destruction, detach cleanup, treat leaf logging as
ownership, permit silent task death, or present tool availability as lifecycle
evidence.

## Verification

Evidence covers the affected contract:

- pure non-suspending logic remains callable synchronously;
- real I/O or streaming paths suspend through the supported mechanism;
- cancellation and resource lifetimes remain observable where contracted;
- sync and async public consumers receive the declared API;
- unsupported or unavailable execution capability returns a typed outcome;
- runtime construction occurs only at the selected composition owner;
- spawned work reaches one observed terminal outcome;
- shutdown closes admission, signals cancellation, and drains tracked work;
- abort paths prove authority and interruption safety; and
- blocking work uses an equivalent async capability or governed isolation;
- isolated work participates in admission, completion, and shutdown ownership;
- synchronization preserves the complete invariant across any suspension;
- unsupported isolation, capacity, or synchronization returns a typed outcome;
- dropped future polling is distinguished from external operation state;
- durable work remains transactional, idempotent, resumable, or compensating;
- asynchronous cleanup reaches an owned observed completion;
- lifecycle health and terminal outcomes are observed by their owner;
- unavailable cancellation, cleanup, or observation returns a typed outcome;
  and
- no convenience fallback changes execution mode or ownership.
````

### profile.language.rust.api

````markdown
# Rust API Profile

**Standards metadata**

- ID: `profile.language.rust.api`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A Rust change selects or changes public or boundary-facing type, conversion, visibility, result, panic, trait, parameter, Cargo-feature, or Rustdoc mechanisms.
- Does not apply when: No Rust API mechanism changes, or the task only selects the generic invariant, architecture, failure, dependency, documentation, compatibility, or consumer contract.
- Requires: `core`, `topic.contracts`, `workflow.documentation`, `profile.language.rust`
- Specializes: `profile.language.rust`
- Verification: Rust API decision fixtures plus affected public API, consumer, compile, and documentation evidence selected by the generic owners.
- Canonical owner: `profiles/languages/rust/api.md`

## Conditional Generic Guidance

Select [Architecture](../../../topics/architecture.md) when responsibility or
state ownership changes, [Resilience](../../../topics/resilience.md) when
failure or retry semantics change, and [Dependencies](../../../topics/dependencies.md)
when dependency or feature selection changes. Select the
[Library profile](../../applications/library.md) for a reusable package; an API
inside an application does not by itself make that application a library.

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

## Rust Source Feature Expression Mechanisms

After Dependencies selects feature, optional-dependency, default, target, and
footprint behavior; Contracts selects consumer-visible compatibility; Library
selects supported real consumer configurations; Documentation selects durable
artifacts; and Verification selects claim-matched evidence, express the
accepted public API result with supported Rust source mechanisms.

Applicable mechanisms include item-level or module-level `cfg`, public item and
module exposure under an accepted feature contract, and compile-time conflict
diagnostics. Select only mechanisms supported by the declared Rust toolchain,
and preserve each accepted consumer configuration without exposing an
unintended public API or silently changing behavior.

Rust source mechanisms are not feature-policy defaults. Do not require `cfg`,
public feature exposure, mutually exclusive feature handling, `compile_error!`,
README or crate-doc placement, command matrices, or an all-features
configuration without the applicable generic owner decisions and capability
evidence. Cargo manifest dependency mechanisms belong only to the Rust
Dependency profile.

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
````

### profile.language.rust.security

````markdown
# Rust Security Profile

**Standards metadata**

- ID: `profile.language.rust.security`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust consumes an untrusted filesystem path, converts untrusted dimensions, counts, offsets, strides, or lengths before bounded use, owns an external-input queue, or owns a listener boundary whose exposure, admission, connection work, or shutdown affects resource or security guarantees.
- Does not apply when: Filesystem authority and concurrent-mutation safety are already proven for the complete operation, values are represented by a validated type whose invariant proves the complete arithmetic and resource contract, no external-input queue is affected, and no Rust listener boundary is affected.
- Requires: `core`, `workflow.verification`, `topic.security`, `profile.language.rust`
- Specializes: `topic.security`, `profile.language.rust`
- Verification: Rust filesystem-authority, checked-boundary-arithmetic, external-input-queue, and listener-lifecycle decisions plus affected filesystem, parser, allocation, indexing, queue, admission, connection, and shutdown tests.
- Canonical owner: `profiles/languages/rust/security.md`

## Panic And Recoverable Error Boundary

Apply the [Rust API error policy](api.md#failure-expression-mechanisms)
to public and internal fallible Rust operations. This profile specializes that
policy for production request paths, lifecycle code, background services, and
network handlers: recoverable errors must remain typed results and must not be
converted to `unwrap()` or `expect()` panics. A panic, `debug_assert!`, or
`unreachable!` is valid only for a proven internal invariant or compile-time
impossibility outside a recoverable input or shutdown outcome, with the
required panic documentation and evidence.

Tests and explicitly non-production examples may use panic assertions when
their scope is declared. Missing proof that a condition is an internal
invariant returns typed `unavailable`; a recoverable error represented by a
panic returns typed `invalid`. Do not replace a failed result with a default,
sentinel, ignored error, alternate operation, or broad catch-all recovery.

## Filesystem Authority Through Use

Apply the generic [Security filesystem contract](../../../topics/security.md#filesystem-containment)
before a Rust filesystem operation. A canonicalized `PathBuf` records identity
and containment at validation time; it does not preserve authority when a
component can be replaced before use.

Record whether concurrent component mutation is excluded for the complete
validation/use interval. When mutation is possible, keep a held file or
directory capability and use a handle-relative operation or an equivalent
supported mechanism. Anchor creation to that authority rather than
reconstructing a pathname.

Immediate revalidation is sufficient only when the recorded threat model
excludes concurrent mutation through the operation. If containment is invalid,
the required mechanism is unsupported, or necessary filesystem facts are
unknown, return typed `invalid`, `unsupported`, or `unavailable` respectively.

## Listener Admission And Lifecycle

Derive the listener's interface and address exposure from the selected service
contract; the service exposure contract is the authority. Local-only and
remotely accessible services have different boundaries; neither one supplies a
universal address for another service.
Unknown exposure facts return typed `unavailable`, and an exposure forbidden by
the selected service contract returns typed `invalid`.

The listener owner defines admission capacity and overload behavior. Acquire
capacity before accepting work that would exceed the owned limit. When no
capacity is available, apply the declared backpressure behavior or return the
typed overload outcome without accepting unowned work. Missing capacity facts
or capability return typed `unavailable` or `unsupported` as applicable.

Apply the [Rust Async profile](async.md) to every accepted connection that may
outlive the accept scope. The listener must register connection work with the
selected lifecycle owner before it can outlive that scope. The lifecycle owner
retains the operation needed to observe success, failure, panic, and
cancellation; logging inside detached work is not ownership.

Shutdown must close admission, signal cancellation, drain tracked work, and
then report the typed result. A complete drain succeeds. An incomplete drain
returns the typed incomplete-shutdown outcome; excess admission returns the
declared typed overload outcome before acceptance. Force-abort is permitted
only when the selected lifecycle owner has authority and the work is proven
interruption-safe.

## Checked Boundary Sizing

Treat dimensions, counts, offsets, strides, and lengths from FFI, IPC, network,
file, command-line, or other untrusted input as source-domain values until
conversion succeeds.

Convert each value into the target integer domain with `TryFrom` or an
equivalent checked conversion before multiplication, addition, indexing,
allocation, or slice construction. A later checked multiplication does not
repair an earlier lossy cast.

Use checked arithmetic for every operation in the size expression. Return typed
`invalid` for negative values, values that do not fit the target domain, and
arithmetic overflow.

## Resource Limits

Check the operation's supported resource limit after representability and
arithmetic succeed. Integer fit does not prove that an allocation, collection,
message, image, or other resource size is permitted.

Return typed `invalid` when the computed value exceeds the declared operation
limit. A zero value is accepted only when the operation contract explicitly
permits it; otherwise return typed `invalid`.

## External-Input Queues

Before accepting external input into a queue, select the queue owner's
operation and resource contract. It defines capacity, what the queue owns,
supported overload behavior, retention or eviction semantics, telemetry, and
the typed outcome for each result. Capacity is not a universal numeric constant
and no overload behavior is a default.

When the selected contract supports rejection, retention, or eviction, return
its declared typed outcome and emit the selected owner telemetry. A queue must
not silently discard work or retain work beyond its declared ownership. Each
accepted item has current input and its declared lifecycle only; queue reuse
does not carry prior input, cancellation, result, or failure state forward.

Return typed `invalid` for contradictory queue or resource facts,
`unsupported` for a well-formed queue behavior outside the selected contract,
and `unavailable` when required capacity, overload, telemetry, or ownership
capability cannot be established.

## Interop Relationship

This profile owns checked Rust sizing for untrusted inputs. When the computed
size authorizes access to raw foreign memory, also apply the
[Rust Interop profile](interop.md); numeric validity does not prove pointer,
allocation, provenance, initialization, alignment, aliasing, or lifetime
authority.

## No Fallback

Failed filesystem authority proof cannot fall back to a plain or stale
`PathBuf`, lexical prefix, ignored canonicalization failure, revalidation while
concurrent mutation remains possible, unanchored creation, an alternate root,
or another filesystem mechanism selected only because the required one is
unavailable.

Missing listener or lifecycle capability cannot fall back to a broader
interface, fixed default capacity, accept-before-capacity ordering, detached
connection work, a discarded outcome, leaf logging as ownership, admission
left open during shutdown, unauthorized or unsafe force-abort, or another
runtime, thread, or listener mechanism.

Failed conversion, arithmetic, or limit proof cannot fall back to:

- `as` or another lossy or unchecked conversion;
- zero, an empty value, or a sentinel size;
- clamping, saturation, wrapping, or truncation;
- a smaller default allocation or operation; or
- continuing with a partially checked expression.

External-input queues cannot fall back to a fixed capacity, default reject-new
or drop-oldest behavior, unbounded accumulation, silent discard, leaf-only
telemetry, another queue, runtime, or thread mechanism, prior-input carry-
forward, or weaker evidence. Return the selected typed outcome.

Return the typed diagnostic before allocation, indexing, slice construction, or
resource use.

## Verification

Affected tests cover:

- existing-object use through held or handle-relative authority;
- creation anchored to validated directory authority;
- immediate revalidation only under an excluded-mutation threat model;
- symlink or component replacement between validation and use;
- invalid, unsupported, and unavailable authority outcomes;
- rejection of plain-path, lexical, revalidation, alternate-root, and
  unanchored-creation fallback;
- local and explicitly declared remote listener exposure;
- admission before accept and declared overload behavior;
- tracked connection success, failure, panic, and cancellation;
- ordered shutdown with complete and incomplete drain;
- unavailable exposure, capacity, registration, cancellation, and drain
  capability;
- unsupported lifecycle capability; and
- rejection of broad-bind, default-capacity, accept-first, detached,
  discarded-outcome, leaf-logging, open-admission, force-abort, and
  alternate-runtime fallback;
- negative and target-domain-too-wide values;
- multiplication and addition overflow;
- values that fit the integer domain but exceed the resource limit;
- permitted and forbidden zero values;
- valid bounded values; and
- rejection of cast, zero, clamp, saturation, wrap, truncation, and
  smaller-default recovery.
- contract-selected capacity, overload, retention, rejection, eviction, and
  telemetry behavior for external-input queues;
- invalid, unsupported, unavailable, and declared overload queue outcomes; and
- rejection of fixed capacity, default overflow, unbounded, silent-discard,
  leaf-telemetry, alternate-mechanism, prior-input, and weaker-evidence
  fallback.
````

### profile.language.typescript

````markdown
# TypeScript Profile

**Standards metadata**

- ID: `profile.language.typescript`
- Role: `profile`
- Level: `PROFILE`
- Applies when: TypeScript source, compiler configuration, declarations, generated TypeScript, or TypeScript-visible contract surfaces change.
- Does not apply when: No TypeScript-owned source, configuration, generated artifact, or consumer surface changes.
- Requires: `core`, `workflow.verification`
- Specializes: `topic.contracts`
- Verification: TypeScript public-surface, inference, runtime-decoding, contract-projection, and generated-type decision fixtures plus affected compiler and consumer evidence.
- Canonical owner: `profiles/languages/typescript.md`

Select [Contracts](../../topics/contracts.md) when this change affects a runtime
boundary, domain invariant, public representation, or compatibility promise.
A local presentation or implementation change does not select that topic by
itself. The specialization applies when the corresponding concern is affected.

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
generated-source authority, and required lint claims. For new owned TypeScript
code, SHOULD enable `strict` as the starting point: it catches common nullability
and implicit-type mistakes before runtime. Existing projects may adopt it in
stages with explicit debt boundaries. Individual overrides need a concrete
compatibility or migration reason. Review newly enabled diagnostics on compiler
upgrades, since the strict family can grow. Runtime decoding remains necessary
for untrusted values even when strict compilation succeeds.

Architecture analysis must derive prohibited and required relationships from
the canonical architecture contract. A linter selector or custom rule is an
implementation mechanism, not architecture authority. Do not default to an
ESLint version, parser, preset, formatter integration, file glob, ignore list,
additional compiler-flag list, severity, or custom-rule implementation.
The strict default above is conditional guidance, not a fixed version or universal
lint preset.

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
````

### profile.language.typescript.async

````markdown
# TypeScript Async Profile

**Standards metadata**

- ID: `profile.language.typescript.async`
- Role: `profile`
- Level: `PROFILE`
- Applies when: TypeScript asynchronous operations can overlap, be superseded, mutate shared or visible state, or require cancellation and terminal-result ownership.
- Does not apply when: No TypeScript async mechanism changes or execution is proven sequential with no operation outliving its immediate caller.
- Requires: `core`, `workflow.verification`, `topic.concurrency`, `profile.language.typescript`
- Specializes: `topic.concurrency`
- Verification: TypeScript invocation-authority, cancellation, completion, and state-application decisions plus focused tests for the selected mechanism.
- Canonical owner: `profiles/languages/typescript/async.md`

## Inherit The Generic Lifecycle Contract

[Concurrency And Async Lifecycle](../../../topics/concurrency.md) owns work,
failure, cancellation, nonblocking execution, and shutdown. This profile owns
only TypeScript mechanisms for identifying the current invocation, classifying
superseded completion, and controlling result application.

A `Promise`, generation token, request identifier, or `AbortSignal` does not
permit detached work, discarded failure, ignored cancellation, or state from
one invocation to become input or output authority for another.

## Establish Current-Invocation Authority

When operations can overlap, select an explicit owner and mechanism that can
prove which invocation may mutate current state. Valid mechanisms can include
a scope-owned generation token, cancellation signal, serialized owner, or
another mechanism whose lifetime and comparison contract are verified.

Do not select a process-global counter, one example request identifier, or
silent stale-result discard as universal policy. The mechanism must be scoped
to the state it protects and must not wrap, collide, leak across owners, or
carry inputs from an earlier invocation.

## Classify Every Completion

Observe every started operation's success, failure, cancellation, or
superseded result. A superseded completion must not mutate current state, but
it still has an explicit terminal classification owned by the operation's
lifecycle owner.

Propagate cancellation when it remains part of the operation contract. When
the underlying operation cannot be cancelled, continue to observe its
completion and classify it without applying a superseded result. Do not treat
an early `return`, ignored promise, or omitted callback as completion evidence.

## Typed Outcomes

Return the operation's typed `invalid`, `unsupported`, or `unavailable`
diagnostic when invocation authority contradicts result application, the
selected mechanism cannot provide required cancellation or identity, or
required ownership and evidence are unknown. Preserve a more specific
operation failure when one exists.

Do not continue with a process-global counter, stale state mutation, ignored
completion, ignored cancellation, alternate mechanism, or default success.

## Verification

Evidence must cover the selected mechanism, including applicable:

- overlapping invocations with only the current result applied;
- explicit success, failure, cancellation, and superseded classifications;
- scoped authority across multiple independent owners;
- repeated operations with distinct inputs and cancellation;
- rejection of stale mutation and process-global authority; and
- typed failure when identity, cancellation, ownership, or evidence is absent.
````

### workflow.verification.gui

````markdown
# GUI Verification

**Standards metadata**

- ID: `workflow.verification.gui`
- Role: `workflow`
- Level: `MUST`
- Applies when: A graphical user workflow requires smoke evidence.
- Does not apply when: No graphical workflow claim is affected.
- Requires: `workflow.verification`
- Specializes: `none`
- Verification: GUI smoke decisions and the real affected interaction path.
- Canonical owner: `workflows/verification/gui.md`

## GUI Smoke Evidence

When a smoke procedure launches a GUI or desktop runtime, qualify the claim
against the environment and execution mode that materially affect startup.
Record applicable display or session capability, sandbox policy, graphics
capability, shared-memory or equivalent resource constraints, state isolation,
and bounded process-lifecycle behavior. Select mechanisms only after these
facts and the supported target contract are known.

CI-specific display servers, software rendering, sandbox flags, resource
limits, or process wrappers are valid only when the selected smoke environment
requires them and the procedure records their effect on the claim. Keep a
verification-only procedure separate from normal interactive startup when
their runtime contracts differ. Do not silently weaken the user runtime,
inherit an operator desktop session, or choose a conventional virtual display,
graphics mode, sandbox setting, shared-memory workaround, or timeout.

The application launcher may expose and transport the selected procedure, but
Verification owns its evidence kind, environment qualification, execution
mode, assertions, and acceptance result. A local reproduction is supporting
evidence unless its environment satisfies the same material facts. Undeclared
runner behavior, missing required capability, premature exit, failed
assertions, or an environment mismatch blocks the claim with the applicable
typed diagnostic; it does not fall back to startup-only evidence, another
environment, or default success.
````
