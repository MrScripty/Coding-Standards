# Security

**Standards metadata**

- ID: `topic.security`
- Role: `topic`
- Level: `MUST`
- Applies when: Untrusted input can authorize an operation, resource access, side effect, or security-relevant decision, or a network listener exposes and retains resources.
- Does not apply when: No untrusted value influences authority or security-relevant behavior and no network listener accepts externally initiated work.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Untrusted-input, filesystem-containment, and network-transport decision fixtures plus affected trust-boundary tests.
- Canonical owner: `topics/security.md`

## Untrusted Structured Input

Decode untrusted structured input through the complete contract required by the
operation before it can authorize work, resource access, or side effects.
Parsing, deserialization, static typing, type assertions, generic shape checks,
and envelope-only validation are not proof of operation-specific fields.

The [Contracts topic](contracts.md#runtime-decoding-at-boundaries) owns generic
runtime proof. Select the [IPC boundary profile](../profiles/boundaries/ipc.md)
when structured messages cross a process or independently evolving component
boundary. Security does not duplicate their schemas or dispatch logic.

Malformed or incomplete input returns typed `invalid`; a well-formed but
unsupported contract or operation returns typed `unsupported`; unavailable
required decoding capability returns typed `unavailable`. Do not continue with
the original input, a cast, a default operation, or a weaker decoder.

## Network Transport Boundary

A listener's exposure comes from the declared service and deployment contract.
Local, remote, and multi-interface exposure are deployment facts, not defaults
inferred from development mode, transport type, or address family. If the
required exposure cannot be established, return typed `unavailable`; reject
contradictory or unauthorized exposure as `invalid`.

The listener owner defines a finite admission capacity and the corresponding
overload outcome. Acquire admission before accepting work that would exceed the
owned limit. Capacity exhaustion returns the declared typed overload result;
it does not accept first, queue without an owned bound, or choose a default
capacity.

After acceptance, register the connection work with the selected lifecycle
owner. That owner observes success, failure, and cancellation. Use
[Concurrency](concurrency.md#own-work-failure-and-cancellation) for work
ownership, failure observation, cancellation, drain, and shutdown behavior.
Logging at a connection leaf does not transfer lifecycle ownership.

Close admission before signalling cancellation, then drain registered work.
Report incomplete drain as a typed incomplete-shutdown outcome. Forced
termination is permitted only when there is explicit authority and the work is
proven interruption-safe; otherwise preserve the incomplete result.

Select connection-liveness behavior from protocol semantics and resource risk.
Protocol closure, transport keepalive, application heartbeat, idle deadline,
or another supported mechanism is valid only when the selected contract
defines its behavior and capability. Missing facts or capability return typed
`invalid`, `unsupported`, `unavailable`, overload, or incomplete-shutdown
outcomes as applicable.

Message validation remains with
[Contracts](contracts.md#runtime-decoding-at-boundaries) and the selected
[IPC boundary profile](../profiles/boundaries/ipc.md). Transport acceptance
does not prove a message schema, action payload, or dispatch variant.

### No Fallback

Do not broaden exposure, select a default address, capacity, timeout, or
liveness mechanism, accept before capacity, detach work, discard outcomes,
substitute leaf logging for ownership, leave admission open during shutdown,
force termination without authority and interruption safety, or select another
runtime, thread, listener, or transport when the required contract or
capability is missing.

## Filesystem Containment

Treat a path as authority to a filesystem object, not as an ordinary string.
Before an operation, establish:

- the trusted root and the operation it authorizes;
- whether the candidate must already exist or may be created;
- the platform and filesystem identity semantics;
- whether an attacker can modify path components concurrently; and
- the typed result when safe resolution cannot be established.

Unknown facts produce a typed diagnostic. Do not accept a path by guessing a
platform default, falling back to lexical comparison, or ignoring failed
canonicalization.

## Existing Candidates

Resolve the trusted root and existing candidate using filesystem-aware
canonical identity. Accept the candidate only when its resolved path is the
root or a component descendant permitted by the operation.

A string-prefix test is not containment. It confuses sibling names such as
`/srv/data` and `/srv/data-backup`, ignores component boundaries, and does not
resolve symlink aliases. Case folding and Unicode normalization follow the
actual filesystem contract; operating-system labels alone are insufficient
when mounted filesystems can differ.

Reject traversal or a resolved symlink escape as `invalid`. Return
`unavailable` when required identity facts cannot be resolved safely.

## Non-Existing Candidates

For creation, resolve and validate the nearest existing ancestor, then validate
each remaining component under the intended operation. Reject parent
traversal, absolute replacement, invalid components, and any target whose
validated ancestor is outside the trusted root.

Use a platform capability that anchors creation to the validated directory
when the threat model permits concurrent mutation. Lexically appending a
non-existing suffix to a previously checked string does not establish
containment.

## Validation And Use

Validation followed by a path-based operation can race with symlink or
directory replacement. When untrusted actors can mutate the path concurrently,
use handle-relative, capability-based, or equivalent platform operations that
preserve the validated authority through use.

Revalidation is sufficient only when the recorded threat model excludes
concurrent mutation for the complete validation/use interval. If the required
atomic or anchored operation is unavailable, return a typed `unsupported` or
`unavailable` result rather than silently using a weaker path.

## Verification

Affected checks cover:

- declared local, remote, and multi-interface listener exposure;
- admission before acceptance, overload, and tracked connection outcomes;
- ordered listener shutdown, incomplete drain, and termination authority;
- protocol-selected liveness and unavailable capability;
- `..` traversal and absolute-path replacement;
- sibling-prefix confusion;
- symlinks that remain inside or escape the trusted root;
- the root itself when the operation permits it;
- creation beneath validated and unvalidated ancestors;
- platform-specific case, normalization, and alias behavior;
- concurrent component replacement where it is in scope; and
- typed failure when safe containment cannot be established.

Use the [Cross-Platform topic](cross-platform.md) for path construction,
filesystem identity, and supported-platform evidence.
