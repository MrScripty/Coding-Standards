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
