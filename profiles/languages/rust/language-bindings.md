# Rust Language Binding Profile

**Standards metadata**

- ID: `profile.language.rust.language-bindings`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust values or operations are exposed to another language through a binding framework, serialized wire contract, opaque handle, generated wrapper, or stable C ABI.
- Does not apply when: Values remain ordinary Rust values and no host-language representation or operation changes.
- Requires: `core`, `workflow.verification`, `profile.language.rust`, `profile.boundary.language-bindings`
- Specializes: `profile.language.rust`, `profile.boundary.language-bindings`
- Verification: Rust binding architecture, runtime adaptation, executor-delegation, conversion, and wire-representation decisions plus framework-free core checks and affected native/host boundary tests.
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

## Enum Representation

After selecting the boundary mechanism, define the complete enum
representation for that mechanism:

- a named binding framework contract defines supported variants, host names or
  values, payload support, and unknown-variant behavior;
- a serialized enum follows
  [Serialized Wire Representation](#serialized-wire-representation);
- a stable C ABI defines discriminant width, signedness, values, payload
  layout, validity, and ownership explicitly;
- an opaque handle exposes only its declared operations and does not reveal
  native enum layout; and
- a generated wrapper remains derived from one of those selected contracts.

Rust source order, implicit discriminants, variant names, `repr` attributes,
framework defaults, and generated static types do not independently establish
the host representation. A fieldless Rust enum is not automatically an ABI
integer, and a data-carrying enum is not automatically a stable tagged union.

Use checked conversion in both directions. Return `invalid` for a host value,
discriminant, tag, or payload that contradicts the selected representation,
`unsupported` for a well-formed variant outside the supported contract, and
`unavailable` when required framework, schema, ABI, generation, or conversion
capability cannot be obtained.

Do not substitute an unknown sentinel, omit a variant, infer names or numeric
values, reinterpret native layout, retry through another representation, or
report default success.

## Serialized Wire Representation

Select the wire schema, serializer contract, and supported schema or protocol
version before exposing a Rust value as serialized data.
The effective wire representation is derived from:

- the selected Rust adapter type and supported variants;
- the serializer format and version;
- container, variant, and field attributes that affect tagging, content,
  names, casing, defaults, omission, flattening, aliases, and custom
  conversion; and
- the consumer contract for optionality, unknown fields, and unsupported
  variants.

Account for every applicable attribute. An absent attribute may select behavior
defined by the chosen serializer contract, but that behavior is not a
cross-language default and must be represented in the consumer contract.
Rust-native layout, source names, enum shape, and derived static types do not
independently establish serialized shape.

Receiving consumers must agree with the complete effective representation.
Apply [Contracts](../../../topics/contracts.md) to wire-version and
independent-consumer evolution. Schema generation is valid only when the
selected contract names the canonical generation input, generator capability,
and derived artifacts. Generated types do not replace runtime decoding.

Return typed `invalid` when data or consumer shape contradicts the selected
representation, `unsupported` when a well-formed version or variant is outside
the supported contract, and `unavailable` when required schema, serializer,
generation, consumer, or decoding capability cannot be obtained.

## Core And Adapter Boundary

Keep domain behavior and validated domain types usable without a binding
framework, generated host code, or foreign runtime. The core owns domain
invariants, operations, and native types. Rust binding adapters own host
representation conversion, error mapping, handle lifecycle, host entrypoint
adaptation, and generated-contract input.

Adapters depend on core contracts; the core does not depend on adapter modules,
binding packages, generated wrappers, or framework behavior. Preserve that
direction even when core and adapter modules share a package.

A source annotation may remain on a core type only when it adds no binding-
framework dependency, host-specific behavior, or change to the domain
contract. A framework-owned annotation, derive, conversion, callback, or
registration belongs on an adapter type.

Binding-specific dependencies, procedural macros, build scripts, and optional
features belong to an adapter or binding package. A disabled-by-default
framework dependency in the core still couples the core when enabled and does
not satisfy this boundary.

Serialization is selected only when a wire schema is part of the contract;
JSON is not a universal ABI or universal wrapper representation. Generated
host code remains derived from adapter-owned input and contains no domain
behavior.

## Host Error Representation

Select the host error contract and binding mechanism before mapping Rust
failures. The contract defines the stable categories or codes, required
fields, cancellation representation, retry or recovery semantics when
applicable, and which bounded context is safe to expose.

The adapter maps each supported Rust failure exhaustively into that selected
representation. Preserve distinctions that affect host behavior, including
`invalid`, `unsupported`, `unavailable`, cancellation, and operation-specific
failure categories. Multiple Rust sources may map to one host category only
when the host contract intentionally gives them identical observable
semantics.

Human-readable messages are context, not the error contract. Keep them
bounded and non-sensitive. Do not expose native error objects, source chains,
debug output, filesystem paths, credentials, payloads, or third-party error
types unless the selected public contract explicitly defines a safe field and
redaction policy.

Use checked conversion when the host representation can reject a category,
field, code, or value. Return `unsupported` when a well-formed Rust outcome has
no representation in the selected host contract, `unavailable` when required
mapping or binding capability cannot be obtained, and `invalid` when mapping
contradicts the selected contract or would expose prohibited context.

Do not flatten every failure to a string, convert every mapping through
infallible `From`, replace cancellation with generic failure, catch all
unmapped variants as one internal error, substitute a framework-specific error
term, or report default success. Preserve the selected typed outcome.

## Host Event Delivery

Select the host event-delivery contract before implementing the Rust adapter.
The contract defines:

- the event representation and supported variants;
- provider or registration authority under the Interop callback contract;
- push, pull, stream, or another declared delivery mode;
- ordering, capacity, backpressure, and overflow or retention behavior;
- delivery-failure, cancellation, and shutdown outcomes; and
- callback thread, re-entrancy, and input-lifetime requirements.

The adapter bridges that selected contract without moving host behavior into
the core. Push and pull are peer contract choices; neither is a preference or
fallback for the other. A retained provider, registration, buffer, runtime, or
host handle does not authorize carrying an earlier event, cancellation,
result, or failure state into a later delivery.

When buffering is selected, capacity and overflow or retention behavior are
governed by the operation contract. Overflow is observable through the
selected typed outcome or declared event semantics. Do not retain events
without a bound or discard them silently. When direct callback or message
delivery is selected, invoke host-controlled behavior only on an authorized
thread and outside synchronization guards.

Inline delivery remains scoped to the current invocation. Work that may
outlive delivery uses
[Concurrency work ownership](../../../topics/concurrency.md#own-work-failure-and-cancellation)
for failure observation, cancellation, and shutdown. Foreign registration,
in-flight callback, unregistration, and release obligations remain governed by
the [Interop event-registration contract](../../boundaries/interop.md#event-registration-lifecycle).

Preserve provider and host delivery failures. Return `invalid` when adapter
facts contradict the selected contract, `unsupported` when a well-formed event
or delivery mode is outside it, `unavailable` when required registration,
thread, delivery, buffering, or host capability cannot be established before
delivery, and the selected typed incomplete outcome when an active delivery or
shutdown obligation cannot be resolved.

Do not substitute push for pull or pull for push, create an alternate runtime,
detach callback-created work, retry on an arbitrary thread, carry prior event
state forward, drop events silently, or report default success.

## Host Callback Task Adaptation

Select the host callback-task contract before a Rust adapter asks host code to
perform work. The contract defines:

- supported task identities and checked input and output representations;
- callback authority, thread, re-entrancy, and input lifetime;
- synchronous or asynchronous completion and correlation identity;
- admission, capacity, cancellation, deadline, and shutdown obligations; and
- host failure, incomplete completion, duplicate response, and late response
  outcomes.

The core may define a binding-neutral port when host execution is a domain
capability, but the adapter owns host representation and invocation mechanics.
Neither generated host code nor the adapter owns domain behavior. Capture the
current validated task snapshot, release synchronization guards, and then
invoke host-controlled behavior.

Each invocation has fresh task identity, input, cancellation, result, and
failure state. A retained callback, host process, runtime, model, or adapter
does not authorize carrying state from an earlier invocation. Match each
response to the selected correlation contract and resolve terminal completion
once. Preserve the contract-selected outcome for late or duplicate completion
after cancellation or another terminal result.

Inline completion remains scoped to the invocation. Asynchronous work that may
outlive it consumes the composition-owned runtime capability and is registered
with the selected Rust Async and Concurrency lifecycle owner before submission.
That owner observes success, failure, panic, cancellation, and shutdown. The
adapter does not synchronously drive async work, create an alternate runtime,
or detach work to satisfy the callback.

Convert task input, output, and host failures through checked binding
representations. Preserve host task failure and cancellation. Return `invalid`
for malformed input, output, correlation, or contradictory callback facts,
`unsupported` when a well-formed task is outside the selected host contract,
`unavailable` when required callback, runtime, admission, conversion, or result
delivery capability cannot be obtained, and the selected typed incomplete
outcome when accepted work cannot reach an observed terminal state.

Do not install a no-op executor, replace callbacks with snapshot polling or
result injection, use generic/default task output, reinterpret failure as
unsupported delegation, carry prior invocation state forward, or report
default success.

## Handle And Runtime Adaptation

Distinguish a host-visible handle from runtime and task lifecycle. A foreign
handle owns only its declared adapter or domain-object reference. Releasing the
last host handle releases that reference; it does not grant runtime shutdown
authority unless the composition owner separately assigns that authority.

When host adaptation needs asynchronous execution, also select the
[Rust Async profile](async.md). Consume the runtime capability supplied by the
application's composition owner. The capability may remain loaded and shared
across calls or workflow runs without making a binding object, request, task,
or requesting workflow its owner.

Each call creates fresh input, cancellation, result, and failure state. Runtime
reuse never carries any of that request-scoped state into later calls. A
persistence or keep-alive request is lifecycle/scheduling input, not ownership
transfer and not authority to retain the requesting workflow's state.

Expose a host-compatible asynchronous result when work remains scoped to the
call. Work that may outlive the call is registered with the selected lifecycle
owner before submission, and its terminal outcome remains observable through
that owner. The adapter does not synchronously drive an asynchronous runtime,
create an embedded or alternate runtime, or detach work to satisfy a host call.

Return typed `unsupported` or `unavailable` when the selected runtime,
host-async, task-registration, or result-delivery capability cannot be
provided.

## Explicit Executor Delegation

A composite executor defines the exact typed `unsupported` outcome that makes
an operation eligible for one selected next executor. Pass only the current
call's already validated input. Successful local completion is terminal.

Validation, execution, cancellation, resource, lifecycle, and unavailable
capability outcomes remain their original terminal outcomes. Do not
reinterpret them as unsupported. If the selected next executor or its required
capability cannot be obtained, return typed `unavailable`.

Delegated work remains scoped to the current call or is registered with the
selected lifecycle owner before it can outlive that call. Runtime persistence
does not authorize another delegation attempt or retention of the call's
input.

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

## Contract Discovery Adaptation

Implement discovery or negotiation only when the selected Contracts-owned
boundary requires it. That contract defines the discoverable identity,
version or capability representation, supported values, consumer behavior,
and whether discovery is an exported operation, handshake field, package
metadata, schema identifier, or another selected mechanism.

The Rust adapter converts the canonical contract value through the selected
binding representation and verifies the real native/host consumer path. A
package version, build identifier, or exported function is not a universal
compatibility contract and cannot be substituted for the selected mechanism.

Return `invalid` when the adapter value contradicts the selected contract,
`unsupported` when a well-formed discovered value is outside the supported
set, and `unavailable` when required identity, version, capability, conversion,
or consumer evidence cannot be obtained. Do not add a universal `version()`
export, guess compatibility, try alternate discovery, reuse stale discovery
state, or report default success.

## Verification

Verify the core/adapter boundary through:

- core build and tests without binding features, framework packages, generated
  host code, or a foreign runtime;
- dependency and feature inspection proving no adapter or binding-framework
  edge points into the core; and
- adapter and generated-boundary checks for every supported binding mechanism.

Verify contract discovery through the selected real native/host mechanism,
including supported, unsupported, contradictory, and unavailable values.

Core and adapter evidence are independent obligations. Core evidence exercises
domain behavior and validated native types through the framework-free core
contract. Adapter evidence exercises conversion, error mapping, lifecycle, and
entrypoint behavior through the selected real native/host boundary. A
native-only adapter test does not prove host behavior, and a host integration
test does not prove that the core remains framework-independent.

When the selected adapter requires a foreign runtime, its integration evidence
may run in a separately provisioned verification environment. That separation
does not permit excluding the adapter evidence, treating a framework-specific
wrapper as the core contract, or replacing unavailable host capability with
native-only tests. Record typed `invalid` when the implementation contradicts
the selected core/adapter boundary and typed `unavailable` when required core
or adapter evidence or its execution capability cannot be obtained.

Verify runtime and handle adaptation through:

- reuse of one composition-owned runtime with fresh state for every call;
- host-handle release without implicit runtime shutdown;
- scoped asynchronous completion or lifecycle-owned tracked submission;
- observed cancellation, failure, and result delivery for the current call;
  and
- typed failure when any required adaptation capability is unavailable.

Verify host event delivery through:

- real native-to-host delivery for every selected event variant and mode;
- declared ordering, capacity, backpressure, and overflow behavior;
- callback thread, re-entrancy, and current-input lifetime;
- delivery failure, cancellation, and shutdown observation;
- callback invocation outside synchronization guards;
- lifecycle ownership for work that outlives delivery; and
- typed invalid, unsupported, unavailable, and incomplete outcomes.

Verify host callback-task adaptation through:

- every supported task through the real native-to-host callback path;
- checked task-input, result, and failure conversion;
- callback thread, re-entrancy, input lifetime, and invocation outside guards;
- exact response correlation and single terminal completion;
- fresh state across repeated and concurrent invocations;
- observed success, host failure, cancellation, panic, and shutdown;
- lifecycle registration before work can outlive invocation; and
- typed invalid, unsupported, unavailable, and incomplete outcomes.

Verify composite executor delegation through:

- successful local completion without invoking another executor;
- delegation only for the contract's exact unsupported variant;
- the current call's validated input reaching the selected next executor once;
- original typed outcomes for invalid input, execution failure, cancellation,
  resource failure, lifecycle failure, and unavailable capability;
- scoped or lifecycle-owned completion of delegated work; and
- typed unavailable when the selected delegate cannot be obtained.

Test every conversion through:

- successful native conversion;
- every narrowing, sign, range, path, enum, and schema rejection class;
- opaque-handle ownership and release when selected;
- round trips where the representation contract supports them; and
- the concrete native/host boundary for every supported framework or ABI.

Native-only conversion tests do not prove host lifting, generated wrappers,
wire compatibility, or ABI behavior.

For enum representations, verify every supported variant through the real
native/host boundary and cover applicable payloads, names, numeric values,
unknown values, malformed discriminants or tags, unsupported variants, checked
round trips, and unavailable representation capability. For a selected stable
C ABI, verify the declared discriminant and payload layout rather than Rust
native layout.

For serialized representations, verify Rust-to-host and host-to-Rust behavior
for each supported shape. Cover tags, content, renamed variants and fields,
optionality, defaults, omitted fields, unknown-field policy, supported and
unsupported variants, malformed input, and unavailable schema or decoding
capability. Producer-only snapshots or Rust-only round trips do not prove
consumer agreement.

## No Fallback

Missing adapter, framework, generation, or packaging capability cannot add a
binding dependency to the core, move domain behavior into an adapter, merge
the layers, skip framework-free core verification, hand-edit generated output,
or select another binding framework. Return the typed planning, build, or
operation diagnostic for the selected boundary.

Missing runtime or host-async capability cannot embed, create, replace, or
synchronously drive a runtime; block a host scheduler thread; detach work;
discard terminal outcomes; retain prior request state; or select another
binding mechanism.

Composite execution cannot catch every error, reinterpret a failure as
unsupported, retry with rebuilt, default, or prior input, continue after
cancellation, select an alternate executor, runtime, or binding mechanism,
detach delegated work, or discard the original typed outcome.

Failed Rust binding conversion cannot fall back to:

- truncation, wrapping, saturation, or unchecked casts;
- lossy path text;
- default values or unknown enum sentinels;
- JSON treated as a schema-free universal ABI;
- another binding framework or representation; or
- native-only tests presented as host-boundary evidence.

Serialized representations also cannot fall back to schema-free JSON,
Rust-native layout, assumed casing or tagging, unknown-value sentinels,
omitted unsupported variants, another serializer or binding mechanism,
generated-schema claims without the selected capability, producer-only tests,
or weaker evidence.

Return the typed diagnostic for the selected representation.
