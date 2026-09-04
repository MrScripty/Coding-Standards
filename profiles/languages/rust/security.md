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

Apply the [Rust API error policy](../../../languages/rust/RUST-API-STANDARDS.md#result-option-panic)
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
