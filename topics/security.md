# Security

**Standards metadata**

- ID: `topic.security`
- Role: `topic`
- Level: `MUST`
- Applies when: Untrusted input can authorize an operation, resource access, side effect, or security-relevant decision.
- Does not apply when: No untrusted value influences authority or security-relevant behavior.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Untrusted-input and filesystem-containment decision fixtures plus affected trust-boundary tests.
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
