# Rust Language Binding Profile

**Standards metadata**

- ID: `profile.language.rust.language-bindings`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust values or operations are exposed to another language through a binding framework, serialized wire contract, opaque handle, generated wrapper, or stable C ABI.
- Does not apply when: Values remain ordinary Rust values and no host-language representation or operation changes.
- Requires: `core`, `workflow.verification`, `profile.language.rust`, `profile.boundary.language-bindings`
- Specializes: `profile.language.rust`, `profile.boundary.language-bindings`
- Verification: Rust binding-conversion decisions plus affected native conversion and real host-boundary tests.
- Canonical owner: `profiles/languages/rust/language-bindings.md`

## Representation Categories

Classify each exposed Rust value as exactly the representation selected for the
concrete boundary:

- native Rust representation;
- value lifted by a named binding framework;
- serialized value governed by a named wire schema;
- opaque handle with declared ownership and operations;
- stable C-ABI representation with explicit layout and validity; or
- generated host wrapper derived from one of those representations.

Framework lifting is not C-ABI safety. `String`, `Vec<T>`, `Option<T>`, Rust
enums, and framework object types may be supported by a named framework, but
their native Rust layouts are not universally stable C-ABI values.

## Adapter Ownership

Keep domain types independent of binding frameworks. Rust binding adapters own
host representation conversion, error mapping, handle lifecycle, runtime
adaptation, and generated-contract input.

Annotate a domain type only when the selected framework contract permits it
without coupling domain behavior to the framework. Otherwise define an adapter
type. Serialization is selected only when a wire schema is part of the
contract; JSON is not a universal ABI or universal wrapper representation.

## Fallible Conversion

Use checked or fallible conversion whenever the target can reject:

- narrowing or sign-changing integers;
- platform-width sizes and offsets;
- `u128` duration or count values narrowed to fixed-width fields;
- non-UTF-8 paths converted to text;
- enum variants not represented by the host contract;
- serialization and deserialization; and
- any framework conversion with a rejection outcome.

Reserve `From` and `Into` for conversions that are genuinely infallible for the
complete supported domain. Use `TryFrom`, `TryInto`, or an explicit fallible
constructor when rejection is possible, and preserve typed `invalid`,
`unsupported`, or `unavailable` outcomes across the host boundary.

## Stable C ABI

A stable C-ABI value uses ABI-defined fixed-width scalars, explicitly declared
layout, and an ownership contract. Dynamic Rust containers cross a C ABI only
through an explicit pointer/length or opaque-handle contract governed by the
Rust Interop and Unsafe profiles; they are not passed by native layout.

## Verification

Test every conversion through:

- successful native conversion;
- every narrowing, sign, range, path, enum, and schema rejection class;
- opaque-handle ownership and release when selected;
- round trips where the representation contract supports them; and
- the concrete native/host boundary for every supported framework or ABI.

Native-only conversion tests do not prove host lifting, generated wrappers,
wire compatibility, or ABI behavior.

## No Fallback

Failed Rust binding conversion cannot fall back to:

- truncation, wrapping, saturation, or unchecked casts;
- lossy path text;
- default values or unknown enum sentinels;
- JSON treated as a schema-free universal ABI;
- another binding framework or representation; or
- native-only tests presented as host-boundary evidence.

Return the typed diagnostic for the selected representation.
