# Interop Boundary Profile

**Standards metadata**

- ID: `profile.boundary.interop`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Code accesses foreign memory, handles, callbacks, runtimes, or resources whose authority is governed by another language, ABI, library, process, or independently evolving component.
- Does not apply when: Values remain ordinary owned values inside one trusted runtime, or only serialized messages cross a boundary covered by the IPC profile.
- Requires: `core`, `workflow.verification`, `topic.contracts`, `topic.security`
- Specializes: `topic.contracts`, `topic.security`
- Verification: Foreign-memory authority decisions and affected provider/consumer boundary tests.
- Canonical owner: `profiles/boundaries/interop.md`

## Foreign Authority

Treat a foreign pointer, handle, buffer, callback, or resource as authority
granted by its provider contract. Before access, establish every fact required
by the operation:

- representation and allocation identity;
- initialized readable or writable extent;
- access permission, mutability, and aliasing constraints;
- provider-guaranteed lifetime;
- calling and callback thread requirements; and
- release authority and whether release is required, optional, or provider-
  owned.

Static typing, non-nullness, a received length, successful lookup, or prior use
does not prove the remaining facts.

## Validate Before Access

Construct a validated adapter value only after the complete applicable
authority contract is proven. Use [Contracts](../../topics/contracts.md#runtime-decoding-at-boundaries)
for generic runtime proof and [Security](../../topics/security.md#untrusted-structured-input)
when foreign input can authorize work or resource access.

Return `invalid` for malformed or contradictory authority, `unsupported` for a
well-formed foreign representation outside the supported contract, and
`unavailable` when required authority evidence or capability cannot be
obtained.

## Copying Is Not Proof

Copy foreign memory only after the source is valid to read for the complete
copied extent. A copy can transfer ownership after valid access; it cannot
repair an invalid pointer, guessed length, expired lifetime, uninitialized
region, wrong thread, or incompatible representation.

The copied value has independent lifetime only after the copy completes
successfully. Do not retain a foreign pointer or borrowed view beyond the
provider guarantee.

## Initialization And Release

Name the owner of initialization, shutdown, and release. Define:

- valid lifecycle states and transitions;
- repeated initialization and shutdown behavior;
- concurrent call behavior;
- whether outstanding callbacks or borrows block release; and
- recovery after partial initialization or failed shutdown.

Do not infer ownership from whichever caller first initialized a shared
runtime. Do not double-release, silently skip required release, or substitute a
fresh resource when the selected contract cannot be completed.

## Thread And Callback Contract

State which threads may call each boundary operation, which thread invokes
callbacks, whether callbacks may re-enter, and how long callback inputs remain
valid. Marshal explicitly when required. Wrong-thread access or an expired
callback lifetime is `invalid`, not a reason to retry on an arbitrary thread.

## Adapter Isolation

Keep foreign-boundary mechanics in thin adapters that expose validated,
owned, or explicitly borrowed values to business logic. Unsafe operations,
raw handles, release mechanics, and runtime-specific callbacks do not belong
in domain logic.

Language profiles specialize mechanisms without weakening this authority
contract. A safe-looking wrapper is not proof unless it validates or requires
every fact it relies on.

## No Fallback

Missing foreign authority cannot fall back to:

- a guessed or sentinel length;
- copying before validation;
- a default thread or lifetime;
- alternate ownership or release assumptions;
- unchecked access through a weaker adapter; or
- creating a replacement resource and pretending it is the selected one.

Return the typed diagnostic that explains which contract could not be
established.

## Verification

Affected tests cover valid access and:

- invalid, unsupported, and unavailable authority;
- partial initialization and initialized extents;
- expired borrows and callback lifetimes;
- wrong-thread and re-entrant behavior;
- copy-before-proof rejection and copy-after-proof success;
- repeated initialization, shutdown, and release; and
- proof that business logic receives no raw foreign authority.
