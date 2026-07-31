# Language Binding Boundary Profile

**Standards metadata**

- ID: `profile.boundary.language-bindings`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A native library exposes values or operations to another language through generated wrappers, a binding framework, serialization, opaque handles, or a stable ABI.
- Does not apply when: No host-language API or cross-language representation is created or changed.
- Requires: `core`, `workflow.verification`, `topic.contracts`, `profile.boundary.interop`
- Specializes: `topic.contracts`, `profile.boundary.interop`
- Verification: Binding-representation decisions and affected native/host boundary tests.
- Canonical owner: `profiles/boundaries/language-bindings.md`

## Select The Boundary Mechanism

Select the mechanism from the complete boundary contract before defining
adapter types or generated host APIs. The contract identifies:

- host consumers, supported runtimes, and process topology;
- deployment, isolation, failure-containment, and trust boundaries;
- value, call, callback, threading, ownership, and lifecycle requirements;
- required latency, throughput, transfer, and startup characteristics;
- supported targets, packaging, toolchain, and generation constraints; and
- available framework, ABI, serialization, runtime, and verification
  capabilities.

Use binding-framework lifting only when one named framework supports the
selected hosts and every required value, operation, callback, thread, and
lifecycle behavior. Select a stable ABI only when layout, calling convention,
ownership, validity, and supported consumers are explicit. Select opaque
handles when identity and exported operations are the contract while native
representation remains hidden. Select serialization when a named wire schema
and serializer govern the representation.

When the selected contract crosses a process boundary, select and route to the
[IPC boundary profile](ipc.md); process transport is not a substitute for a
failed in-process binding. Generated wrappers derive from one selected
mechanism and are not an independent transport.

Target-language count, host-language label, UI technology, framework
popularity, and example repository layout do not select a mechanism. Multiple
mechanisms may expose the same domain contract only as separately declared
adapters with their own representation, lifecycle, capability, packaging, and
native/host evidence.

Return `invalid` when the selected mechanism contradicts known boundary facts,
`unsupported` when a well-formed requirement is outside its declared contract,
and `unavailable` when a required mechanism, runtime, generator, target, or
verification capability cannot be obtained. Do not retry through another
framework, ABI, serialization format, or process transport.

## Declare The Boundary Mechanism

Every binding declares the concrete mechanism used for each exposed value or
operation:

- binding-framework lifting or transport;
- serialized wire representation;
- stable ABI value representation;
- opaque handle plus exported operations; or
- generated host wrapper over one of those mechanisms.

Do not label a native-language type universally binding-safe or ABI-safe.
Support by one framework proves only that framework's declared conversion and
runtime contract.

## Representation Categories

Keep these categories distinct:

| Category | Meaning |
| --- | --- |
| Native value | In-process value governed by the implementation language |
| Framework-lifted value | Converted or transported by one named binding framework |
| Serialized value | Bytes or text governed by an explicit wire schema |
| Stable ABI value | Layout, calling convention, ownership, and validity are defined for the ABI |
| Opaque handle | Foreign callers hold identity while the native owner retains representation |
| Generated host wrapper | Derived API surface; not an independent native representation |

A value may have more than one representation, but each conversion is explicit
and tested. Framework support does not imply stable memory layout, and
serialization does not create a C ABI.

## Serialized Wire Representation

Select the canonical wire contract and the concrete serializer mechanism
before defining producer or consumer types. Derive the effective serialized
shape from both authorities, including every applicable:

- tagged-enum form, tag key, content key, and payload structure;
- variant spelling, numeric value, casing, and explicit rename;
- field name, casing, explicit rename, flattening, omission, and default rule;
  and
- version marker, unknown-field policy, and unsupported-variant behavior.

Native type names, default serializer conventions, generated static types, and
successful producer-side serialization do not independently establish the
wire representation. Consumers must agree with the complete selected shape and
must runtime-decode it under the applicable Contracts and IPC rules.

Evidence covers producer-to-consumer and consumer-to-producer behavior whenever
the contract is bidirectional, plus malformed, unsupported, missing-field,
renamed, omitted, extra-field, and unavailable-capability cases applicable to
the selected shape. One-way contracts require evidence only in the declared
direction, but producer-only snapshots are not consumer evidence.

Return `invalid` for a representation that contradicts the selected schema or
serializer rules, `unsupported` for a well-formed variant or version outside
the declared contract, and `unavailable` when required schema, serializer,
generated support, consumer capability, or evidence cannot be obtained. Do not
infer casing or tagging, use schema-free serialization, omit an unsupported
variant, substitute a sentinel/default shape, or retry with another serializer
or binding mechanism.

## Layer Ownership

Domain logic and validated domain types remain independent of binding
frameworks. Binding adapters own representation conversion, error mapping,
host-runtime adaptation, callbacks, and lifecycle bridging. Generated host
code remains derived and contains no business rules.

Adapters depend on core contracts; core does not depend on adapters or
generated wrappers. Multiple binding mechanisms may expose the same domain
contract only through separate adapters with independently declared
representations.

Use the [Interop profile](interop.md) for foreign resource and memory authority
and [Contracts](../../topics/contracts.md) for public, generated, ABI, wire, and
independently deployed compatibility decisions.

Use the [Rust specialization](../languages/rust/language-bindings.md) for Rust
representation categories, fallible conversions, and native/host evidence.

## Exported Surface Contract

Select each exported operation and representation from declared consumer and
product contracts. Record the actual consumers, selected host-language
subsets, owning semantic layer, lifecycle and diagnostic behavior,
compatibility promise, support and publication status, documentation, and
required native and real host evidence.

Expose only selected client operations. Internal helpers, framework-local
controls, debug and recovery paths, and technically exportable types remain
unexposed unless an explicit consumer contract selects them. Domain behavior
and canonical semantics remain in their core or backend owner; adapters own
only boundary representation and host-runtime adaptation.

Different host languages may expose different declared subsets. Neither exact
parity nor divergence is a default. Support categories and publication status
are project contract facts; no fixed support-tier vocabulary is universal.
Every selected surface states which consumers receive it, how it is packaged
and versioned, and which native and host evidence supports the claim.

Return `unavailable` when required consumer, support, host-subset,
documentation, compatibility, or evidence facts cannot be obtained, and
`invalid` when selected facts contradict ownership or another applicable
contract. Do not export all technically available operations, invent fixed
support tiers, force language parity, move domain semantics into adapters,
substitute native-only evidence, or report default success.

## Conversion Outcomes

Validate and convert at the owning adapter. Return:

- `invalid` when input violates the selected representation or conversion
  contract;
- `unsupported` when the value or operation has no representation in the
  selected binding mechanism; or
- `unavailable` when required schema, generated support, runtime capability, or
  converter cannot be obtained.

Preserve conversion rejection across the host boundary. Do not turn it into a
default value, successful empty value, or generic internal error that loses the
boundary cause.

## Generated Artifacts

Generated wrappers are derived from the selected native contract and generation
input. Regenerate them when that input changes, and verify both native adapter
and real host-language paths. Do not hand-maintain business logic in generated
files or treat generated static types as runtime proof.

## Binding Evidence Cohorts

For each supported binding claim, select evidence that independently covers the
native adapter contract and the real host consumer contract. Native evidence
includes applicable contract shaping, representation conversion, diagnostic
mapping, ownership, and lifecycle behavior. Host evidence loads the selected
generated or packaged binding through the declared host runtime and exercises
the native artifact shape that consumers receive.

When host bindings and native artifacts are published, installed, or versioned
as separate units, identify the release cohort or compatibility contract that
authorizes their combination. Evidence must prove that selected units work
together; sharing a build directory, version string, or generation run is not
proof by itself. Release and packaging owners define artifact identity and
provenance while this profile owns boundary compatibility behavior.

Evidence breadth follows declared consumers, support status, representations,
operations, lifecycle, and packaging claims. An experimental label, internal
helper path, wrapper test, native-only test, host-only smoke, generated type,
or producer snapshot does not reduce or satisfy a selected public claim.
Verification scheduling follows the selected claim and available environment;
do not infer per-change, pre-push, CI, or release cadence from the binding type
or support label.

Return `invalid` for contradictory cohort, representation, or ownership facts,
`unsupported` for a well-formed host or operation outside the declared binding
contract, and `unavailable` when required native, host, package, runtime, or
provenance evidence cannot be obtained. Do not substitute another artifact,
host, wrapper, smoke path, schedule, or weaker evidence.

## No Fallback

An unsupported or failed representation cannot fall back to:

- reinterpreting native memory as a stable ABI;
- lossy or schema-free serialization;
- an implicit default or truncating conversion;
- a different binding framework;
- an opaque handle with undeclared lifetime; or
- hand-edited generated code.

An unsupported or unavailable mechanism also cannot fall back to a choice
derived from target count, host label, UI technology, framework popularity, or
the next available mechanism.

Return the typed diagnostic for the selected mechanism.

## Verification

Affected tests cover:

- selection from complete boundary facts and rejection of contradictory facts;
- selected and deliberately unexposed client surfaces across declared hosts;
- support, documentation, compatibility, and native/host evidence claims;
- every declared representation and successful conversion;
- invalid, unsupported, and unavailable outcomes;
- framework-lifted values versus stable ABI values;
- serialized schema round trips;
- opaque-handle ownership and release;
- generated-wrapper regeneration and a real host smoke path; and
- native-adapter and real-host evidence for every selected binding claim;
- package-cohort compatibility when binding and native units vary separately;
- proof that generated code and adapters contain no domain behavior.
