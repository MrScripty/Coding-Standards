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
