# Milestone 7 Independent Trust-Boundary Re-plan

## Purpose

This planning-only report resumes the trust-boundary wave after the generic
Concurrency, Rust Async, and dependent Rust binding/security bridge completed.
It measures the current independent remainder and fully specifies only the
next owner-bounded implementation slice.

This report is planning evidence. It does not own normative security,
cross-platform, interop, language-binding, async, runtime, listener, or
downstream policy.

## Current Audit

The rolling disposition gate reports 613 frozen identifiers across 30 legacy
sources and 29 proposed canonical owners, with 14 owners still missing.

[milestone-7-independent-trust-groups.tsv](milestone-7-independent-trust-groups.tsv)
freezes the active trust-boundary subset:

| Order | Owner | Remaining IDs | State | Dependency |
| ---: | --- | ---: | --- | --- |
| 1 | `topics/security.md` | 12 | Exists | None |
| 2 | `topics/cross-platform.md` | 15 | Exists | None |
| 3 | `profiles/boundaries/interop.md` | 10 | Exists | Accepted Contracts |
| 4 | `profiles/languages/rust/cross-platform.md` | 5 | Missing | Cross-Platform |
| 5 | `profiles/languages/rust/interop.md` | 1 | Exists | Interop |
| 6 | `profiles/languages/rust/security.md` | 3 | Exists | Security and Rust Async |
| 7 | `profiles/languages/rust/language-bindings.md` | 34 | Exists | Language Bindings and Rust Async |

These seven groups total 80 undisposed identifiers. Their owner-map
destinations remain proposals until an accepted pre-slice review proves the
section role and correctness.

## Selection Decision

The highest-priority unresolved correctness defect in the active wave is
`F016`: the generic Security listener-shutdown section links to a nonexistent
Concurrency heading. The same five-section network transport group also
contains universal bind-address recipes, accepts fixed mechanism examples as
policy, requires force-close after a timeout without interruption-safety
authority, and mandates one half-open detection mechanism with a fixed timeout
example.

Select `STD-0596` through `STD-0600` as one atomic generic Security slice.
Splitting the broken shutdown reference from exposure, admission, and liveness
would leave competing transport policy active. The canonical Security topic
already exists, and accepted generic Concurrency owns task lifecycle and
shutdown mechanics.

Cross-platform target policy, native loading, CI matrices, cross-language
contract maintenance, event subscriptions, Rust specializations, binding
packaging/generation, bounded queues, and panic policy remain outside this
slice.

## Accepted Slice 7.4b6: Planning-Only Re-plan

**Allowed write set:**

- this report;
- `milestone-7-independent-trust-groups.tsv`;
- `milestone-7-independent-trust-next-slice.tsv`;
- `verify-milestone-7-independent-trust-replan.sh`;
- the parent Milestone 7 decomposition report;
- evaluation README, findings, active plan, and execution ledger.

No normative standard, legacy standard, final disposition, generated
inventory, owner map, router, metadata contract, template, source, test,
configuration, dependency, lockfile, build output, runtime, listener,
workflow fixture, or downstream repository belongs to this planning slice.

**Acceptance gate:** the checker proves the exact 80-ID/seven-owner remainder,
current owner existence and accepted dependencies, exact five-ID next-slice
proposal, zero premature dispositions, active-plan handoff, parent linkage,
plan lifecycle, shell syntax, whitespace, and all standards-effectiveness
regressions.

**Discovered issue (`Resolved`):** the initial focused checker used Bash's
special `GROUPS` variable for the group-fixture path. It now uses the explicit
`GROUP_FILE` name so the path cannot resolve to a process group identifier.

## Planned Slice 7.4b7a: Generic Network Transport Contract

[milestone-7-independent-trust-next-slice.tsv](milestone-7-independent-trust-next-slice.tsv)
freezes `STD-0596` through `STD-0600`.

**Outcome:** make `topics/security.md` the generic owner for listener exposure,
admission resource protection, lifecycle linkage, and transport liveness
selection without universal addresses, capacities, timeouts, or force-close
behavior.

**Allowed write set:**

- `topics/security.md`;
- `SECURITY-STANDARDS.md`;
- `evaluation/standards-effectiveness/fixtures/security/network-transport-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-network-transport-policy.sh`;
- this report and checker for accepted disposition and handoff state;
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No generic Concurrency or Contracts topic, IPC or language profile, Rust
standard/profile, network implementation, runtime-specific task type,
platform-address recipe, fixed capacity/timeout, router, generated artifact,
template, package/configuration/lockfile, workflow fixture, or downstream
repository belongs to this slice.

**Required semantics:**

- derive listener interface/address exposure from the declared service and
  deployment contract rather than a universal address table;
- define admission capacity and overload behavior at the listener owner before
  accepting work that would exceed the owned limit;
- register accepted work with the selected lifecycle owner and consume generic
  Concurrency for failure observation, cancellation, drain, and shutdown;
- close admission before cancellation and drain;
- permit forced termination only with explicit authority and proven
  interruption safety;
- select keepalive, heartbeat, idle deadline, protocol closure, or another
  supported liveness mechanism from protocol semantics and resource risk;
- preserve typed `invalid`, `unsupported`, `unavailable`, overload, and
  incomplete-shutdown outcomes; and
- keep message schema/dispatch validation with Contracts and the selected
  boundary profile.

**No fallback:** missing exposure, capacity, lifecycle, shutdown, or liveness
facts/capability cannot broaden network exposure, choose a default address,
capacity, timeout, keepalive, heartbeat, or force-close policy, accept before
capacity, detach work, discard outcomes, rely on leaf logging, leave admission
open during shutdown, or select another runtime, thread, listener, or transport
mechanism.

**Focused evidence:** decisions cover local and declared remote exposure,
capacity before acceptance, overload, tracked success/failure/cancellation,
ordered complete and incomplete shutdown, authorized interruption-safe
termination, protocol-selected liveness, missing/unsupported capability, and
rejection of broad-bind, fixed-default, accept-first, detached, discarded,
leaf-logging, open-admission, unsafe-force-close, fixed-timeout, and
alternate-mechanism fallback.

**Acceptance gate:** `F016` is resolved; all five identifiers have one exact
final disposition; Security metadata remains valid; the legacy network section
is a bounded canonical link without broken anchors or fixed mechanisms;
generic Concurrency remains unchanged and passes; unrelated Security sections
remain untouched; and focused plus affected regressions pass.

**Pre-slice review:** accepted. One generic Security owner can represent the
five-section group without a split disposition. The slice consumes accepted
Concurrency lifecycle policy and does not require a new role, taxonomy,
runtime-specific universal mechanism, or compatibility fallback.

## Re-Plan Triggers

- A network section cannot be represented by one Security disposition without
  splitting lifecycle, protocol, or boundary ownership.
- Generic network policy requires changing accepted Concurrency or IPC
  contracts rather than linking to them.
- A safe outcome requires a universal address, capacity, timeout, forced
  termination, or liveness mechanism.
- Focused evidence cannot distinguish service exposure from listener admission
  or protocol liveness from task lifecycle.
- Implementation needs an undisposed identifier, owner, source, generated
  artifact, configuration, lockfile, workflow fixture, or downstream file
  outside the activated write set.
