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

## No Fallback

An unsupported or failed representation cannot fall back to:

- reinterpreting native memory as a stable ABI;
- lossy or schema-free serialization;
- an implicit default or truncating conversion;
- a different binding framework;
- an opaque handle with undeclared lifetime; or
- hand-edited generated code.

Return the typed diagnostic for the selected mechanism.

## Verification

Affected tests cover:

- every declared representation and successful conversion;
- invalid, unsupported, and unavailable outcomes;
- framework-lifted values versus stable ABI values;
- serialized schema round trips;
- opaque-handle ownership and release;
- generated-wrapper regeneration and a real host smoke path; and
- proof that generated code and adapters contain no domain behavior.
