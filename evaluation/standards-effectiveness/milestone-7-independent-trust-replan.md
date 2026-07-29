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

The rolling disposition gate reports 594 frozen identifiers across 29 legacy
sources and 28 proposed canonical owners, with 13 owners still missing.

[milestone-7-independent-trust-groups.tsv](milestone-7-independent-trust-groups.tsv)
freezes the active trust-boundary subset:

| Order | Owner | Remaining IDs | State | Dependency |
| ---: | --- | ---: | --- | --- |
| 1 | `topics/security.md` | 7 | Exists | None |
| 2 | `topics/cross-platform.md` | 6 | Exists | None |
| 3 | `profiles/boundaries/interop.md` | 10 | Exists | Accepted Contracts; conditional Concurrency selection |
| 4 | `profiles/languages/rust/interop.md` | 1 | Exists | Interop |
| 5 | `profiles/languages/rust/security.md` | 3 | Exists | Security and Rust Async |
| 6 | `profiles/languages/rust/language-bindings.md` | 34 | Exists | Language Bindings and Rust Async |

These six groups total 61 undisposed identifiers. Their owner-map
destinations remain proposals until an accepted pre-slice review proves the
section role and correctness.

## Selection Decision

The generic Interop group is not one implementation unit. `STD-0474` through
`STD-0482` mix contract evolution, runtime decoding, wire representation, and
routing roles that require separate owner corrections. `STD-0473` alone
describes a foreign event-registration resource and fits the accepted Interop
boundary owner's initialization, callback, release, and shutdown contract.

The legacy rule universally ties unsubscription to subscriber destruction and
uses framework-specific C# and TypeScript examples. Destruction, finalization,
or garbage collection does not prove that callback delivery has stopped, that
in-flight delivery is resolved, or that release occurs on an allowed thread.
This incomplete lifecycle and unsafe cleanup default is recorded as `F049`.

Select only `STD-0473` as the next implementation slice. The Interop profile
must identify the foreign registration owner, callback lifetime and thread,
re-entrancy, provider delivery guarantees, in-flight provider behavior,
unregistration semantics, release authority, and provider shutdown ordering.
When callback-created work can outlive its invocation, it must consume the
generic Concurrency owner for work ownership, failure observation,
cancellation propagation, and work shutdown. Provider delivery scheduling
alone does not select Concurrency. The lifecycle must return typed `invalid`,
`unsupported`, `unavailable`, or incomplete-cleanup diagnostics when the
selected provider/subscriber contract cannot be completed.

The slice refines one existing boundary owner and does not move event-domain
behavior, contract evolution, IPC decoding, wire schemas, language-specific
framework recipes, or routing policy into Interop.

## Remainder Ownership Audit

The re-measurement found that several proposed owner-map destinations are not
implementation-ready. This is recorded as `F048`; each affected group requires
an owner-correction or decomposition re-plan before activation:

- generic Security validation sections mix authority, runtime proof,
  filesystem use, domain constraints, and implementation structure;
- generic Cross-Platform native-library and CI sections mix Interop resource
  lifecycle, Release artifact identity, Documentation, and Verification
  scheduling;
- generic Interop contract and wire sections mix Contracts, IPC, Language
  Bindings, event-resource lifecycle, and routing;
- `STD-0757` is serialized wire representation, not Rust foreign-memory
  authority;
- the Rust Security remainder mixes index closure, bounded admission, and
  panic/API policy; and
- the 34-ID Rust Language Binding remainder requires separate packaging,
  support-surface, error, callback, generation, build, selection, and
  compatibility slices.

The exact role and exclusions for `STD-0473` are now corrected. The remaining
60 identifiers stay under `F048`; no other group or generic Interop section is
activated by this decision.

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

## Accepted Slice 7.4b7a: Generic Network Transport Contract

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
- the historical trust/lifecycle checker only to remove mutable live
  independent-trust count and owner-state ownership while preserving its
  frozen baseline and lifecycle-bridge evidence;
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

**Resolved re-plan trigger:** the historical trust/lifecycle checker compared
its frozen independent-trust rows to live owner counts. That duplicated the
new independent checker and would reject every valid later disposition. The
approved narrow expansion keeps the historical 90-ID baseline, exact group
rows, and lifecycle-bridge progression while making this report's checker the
sole owner of current independent-trust counts and owner state.

**Acceptance result:** accepted. The Security topic now owns contract-selected
listener exposure, admission before acceptance, lifecycle registration,
ordered shutdown, typed incomplete drain, interruption-safe termination, and
protocol-selected liveness. The legacy five-section network group is one
bounded canonical link. Thirty-two focused decisions reject universal
addresses, capacities, timeouts, liveness mechanisms, unsafe termination,
accept-first ordering, detached work, discarded outcomes, leaf-only logging,
open admission, and alternate-mechanism fallback.

All five identifiers have exact `refine` dispositions to
`topics/security.md`, and `F016` is resolved. The rolling Milestone 7 remainder
is 608 identifiers across 30 sources and 29 owners, with 14 owners still
missing. The active independent trust-boundary subset contains 75 identifiers
across the same seven baseline owner groups.

## Accepted Slice 7.4b7b: Planning-Only Remainder Re-plan

**Allowed write set:**

- this report;
- `milestone-7-independent-trust-groups.tsv`;
- `milestone-7-independent-trust-next-slice.tsv`;
- `verify-milestone-7-independent-trust-replan.sh`;
- the parent Milestone 7 decomposition report;
- evaluation README, findings, active plan, and execution ledger.

No normative or legacy standard, final disposition, generated inventory,
owner map, router, metadata contract, template, source, test, configuration,
dependency, lockfile, build output, runtime, workflow fixture, or downstream
repository belongs to this planning slice.

**Acceptance result:** accepted. The audit proves the 608-ID global remainder,
75-ID/seven-owner trust subset, current owner state, and accepted dependencies.
It freezes exactly nine zero-disposition Cross-Platform identifiers for the
next slice and records `F046`.

**No fallback:** the selection does not infer a next slice from stale baseline
order, preserve conflicting legacy guidance, combine owners to avoid a missing
contract, invent owner files, or activate implementation before exact
measurement and pre-slice review pass.

## Accepted Slice 7.4b7c: Generic Platform Target And Isolation Contract

[milestone-7-independent-trust-next-slice.tsv](milestone-7-independent-trust-next-slice.tsv)
freezes `STD-0280` through `STD-0288`.

**Outcome:** make `topics/cross-platform.md` the generic owner for declared
platform support, platform-dependent behavior isolation, mechanism selection,
semantic fidelity, and typed unresolved outcomes.

**Allowed write set:**

- `topics/cross-platform.md`;
- the opening target/core-rules group in `CROSS-PLATFORM-STANDARDS.md`;
- a focused platform-target decision fixture and checker;
- this report and checker for accepted disposition and handoff state;
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No native-library or CI section, Security/Contracts/Concurrency topic, generic
Interop or language profile, Rust standard/profile, router, generated artifact,
template, package/configuration/dependency/lockfile, workflow fixture, source,
runtime, build output, or downstream repository belongs to this slice.

**Required semantics:**

- derive supported targets, support levels, and evidence obligations from an
  explicit project, product, or release contract;
- define required behavior and unavailable/unsupported outcomes per target;
- keep platform selection and platform-specific mechanics outside domain
  behavior while permitting the smallest cohesive boundary supported by the
  language and architecture;
- select compile-time, runtime, composition, dispatch, file, and module
  mechanisms from language, toolchain, artifact, and deployment facts;
- preserve declared semantics instead of treating a stub, log, false result,
  omitted feature, or alternate implementation as graceful degradation;
- return typed `invalid`, `unsupported`, or `unavailable` diagnostics when the
  selected target contract cannot be established; and
- route language-specific target syntax and verification to the selected
  language profile.

**No fallback:** missing target, support, capability, build, or deployment
facts cannot choose a default platform list, support tier, Strategy/Factory,
runtime detection, compile-time condition, file layout, stub implementation,
silent feature omission, alternate mechanism, or weaker evidence.

**Focused evidence:** decisions cover single and multiple declared targets,
compile-time and runtime selection, cohesive isolation, semantic optionality,
typed unsupported/unavailable outcomes, and rejection of hard-coded target
lists, default support tiers, mandatory Strategy/Factory or one-file-per-
platform layout, runtime-only selection, best-effort stubs, silent omission,
alternate-mechanism fallback, and simulated evidence for required-real target
claims.

**Acceptance gate:** `F046` is resolved; all nine identifiers have one exact
final disposition; Cross-Platform metadata remains valid; the legacy opening
group is a bounded canonical link without fixed targets or universal
mechanisms; the accepted filesystem-identity section remains unchanged and
passes; unrelated native-library and CI sections remain untouched; and focused
plus affected regressions pass.

**Pre-slice review:** accepted. One generic Cross-Platform owner can represent
the target and isolation group without absorbing language-specific mechanisms,
native loading, CI scheduling, or Rust specialization. The section is a
dependency for the missing Rust profile, but that profile remains a later
owner-bounded slice.

**Acceptance result:** accepted. The Cross-Platform topic now owns declared
target support, cohesive platform isolation, contract-selected compile-time,
runtime, composition, and dispatch mechanisms, semantic fidelity, and typed
unresolved outcomes. The legacy opening group is one bounded canonical link.
Twenty-five focused decisions reject fixed targets and tiers, universal
architecture/layout mechanisms, runtime-only or compile-only selection, stubs,
false results, silent omission, alternate implementations, and weaker
evidence.

All nine identifiers have exact final dispositions and `F046` is resolved. The
rolling Milestone 7 remainder is 599 identifiers across 30 sources and 29
owners, with 14 owners still missing. The active independent trust-boundary
subset contains 66 identifiers across the same seven baseline owner groups.

## Accepted Slice 7.4b7d: Planning-Only Remainder Re-plan

**Allowed write set:**

- this report;
- `milestone-7-independent-trust-groups.tsv`;
- `milestone-7-independent-trust-next-slice.tsv`;
- `verify-milestone-7-independent-trust-replan.sh`;
- the parent Milestone 7 decomposition report;
- evaluation README, findings, active plan, and execution ledger.

No normative or legacy standard, final disposition, generated inventory,
owner map, router, metadata contract, template, source, test, configuration,
dependency, lockfile, build output, runtime, workflow fixture, or downstream
repository belongs to this planning slice.

**Acceptance result:** accepted. The audit proves the 599-ID global remainder,
66-ID/seven-owner trust subset, current owner state, and accepted dependencies.
It freezes exactly five zero-disposition Rust Cross-Platform identifiers for
the next slice, records `F047`, and records the residual owner corrections and
decomposition requirement as `F048`.

**No fallback:** the selection does not infer a next slice from stale order,
preserve conflicting legacy guidance, combine owners to avoid a missing
contract, invent an undeclared owner, or activate implementation before exact
measurement and pre-slice review pass.

## Accepted Slice 7.4b7e: Rust Target And Configuration Contract

[milestone-7-independent-trust-next-slice.tsv](milestone-7-independent-trust-next-slice.tsv)
freezes `STD-0726` through `STD-0730`.

**Outcome:** establish `profiles/languages/rust/cross-platform.md` as the Rust
specialization for declared target triples, contract-selected build and
configuration mechanisms, cohesive platform-code placement, and target-
matched evidence.

**Allowed write set:**

- new `profiles/languages/rust/cross-platform.md`;
- `languages/rust/RUST-CROSS-PLATFORM-STANDARDS.md`;
- `profiles/languages/rust/README.md`;
- `STANDARDS-ROUTER.md`;
- `README.md`;
- `evaluation/standards-effectiveness/fixtures/rust/target-configuration-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-rust-target-configuration.sh`;
- this report and checker for accepted disposition and handoff state;
- `evaluation/standards-effectiveness/consolidation-dispositions.tsv`;
- `evaluation/standards-effectiveness/README.md`;
- `evaluation/standards-effectiveness/findings.md`;
- `plans/standards-library-effectiveness-restructure-plan.md`; and
- `evaluation/standards-effectiveness/execution-ledger.md`.

No generic Cross-Platform normative change, native-library/CI standard,
Security/Contracts/Concurrency/Interop topic or profile, other Rust standard
or profile, generated artifact, metadata schema, template, package,
configuration/dependency/lockfile, workflow fixture, source, runtime, build
output, or downstream repository belongs to this slice.

**Required semantics:**

- derive Rust target triples, support claims, artifact requirements, and
  evidence from the selected project/product/release target contract;
- select `cfg`, build-script, feature, composition, dispatch, file, and module
  mechanisms from Rust, toolchain, artifact, and deployment facts;
- keep target mechanics outside domain behavior at the smallest cohesive Rust
  boundary without requiring a shared trait or platform module;
- permit inline `cfg` when cohesion and reviewability support it, without
  numeric line, parameter, block-count, or comment thresholds;
- require evidence matching every declared target claim and distinguish
  compile, link, package, integration, and real-target runtime evidence; and
- return typed `invalid`, `unsupported`, or `unavailable` outcomes when the
  selected target or evidence contract cannot be established.

**No fallback:** missing target, toolchain, artifact, capability, deployment,
or evidence facts cannot choose default triples, support tiers, best-effort
status, a module/trait layout, inline-`cfg` thresholds, `cross`, containers,
hosted runners, simulated evidence, another target, or weaker checks.

**Focused evidence:** decisions cover declared single and multiple Rust
targets, compile-time and runtime selection, build-script and composition
selection with explicit basis/ownership/precedence, cohesive module and inline
placement, target-matched compile/link/runtime evidence, typed unresolved
outcomes, and rejection of fixed triples, best-effort support, feature-as-
target substitution, unjustified build scripts, ambiguous combined mechanisms,
universal trait/module layout, numeric extraction rules, fixed commands/tools,
substitute environments, alternate targets, and weaker evidence.

**Acceptance gate:** `F047` is resolved; all five identifiers have one exact
final disposition; the new profile metadata and routing are valid; the legacy
Rust document is a bounded canonical link without fixed targets, layout,
thresholds, commands, or substitute tools; the generic Cross-Platform topic
remains unchanged and passes; unrelated Rust profiles and standards remain
untouched; and focused plus affected regressions pass.

**Pre-slice review:** accepted. The owner is already declared by the frozen
owner map and information architecture, its generic dependency is accepted,
and all five sections form one Rust specialization without absorbing generic
platform, CI scheduling, native loading, or release policy.

**Acceptance result:** accepted. The Rust Cross-Platform profile now owns
declared target triples, contract-selected `cfg`/build/feature/composition/
dispatch mechanisms, cohesive placement, and evidence matched to compile,
link, package, integration, and runtime claims. The Rust index, router, and
top-level README route to the profile. The legacy Rust document is a bounded
canonical link.

All five identifiers have exact final dispositions and `F047` is resolved.
The rolling Milestone 7 remainder is 594 identifiers across 29 sources and 28
owners, with 13 canonical owners still missing. The active independent
trust-boundary subset contains 61 identifiers across six remaining owner
groups; the 61 IDs under `F048` remain blocked on owner correction or
decomposition.

## Accepted Slice 7.4b7f: Planning-Only Remainder Re-plan

**Allowed write set:**

- this report;
- `milestone-7-independent-trust-groups.tsv`;
- `milestone-7-independent-trust-next-slice.tsv`;
- `verify-milestone-7-independent-trust-replan.sh`;
- the parent Milestone 7 decomposition report;
- evaluation README, findings, active plan, and execution ledger.

No normative or legacy standard, final disposition, generated inventory,
owner map, router, metadata contract, template, source, test, configuration,
dependency, lockfile, build output, runtime, workflow fixture, or downstream
repository belongs to this planning slice.

**Acceptance result:** accepted. The audit proves the 594-ID global remainder,
61-ID/six-owner trust subset, current owner state, and accepted dependencies.
It corrects the generic Interop group into one exact event-registration
lifecycle unit and nine still-blocked mixed-role sections, freezes one
zero-disposition identifier for the next slice, and records `F049`.

**No fallback:** the selection does not preserve destruction-linked cleanup,
infer registration release from finalization or garbage collection, combine
the remaining Interop roles, select an alternate event mechanism, or activate
implementation before exact measurement and pre-slice review pass.

## Accepted Slice 7.4b7f1: Event Registration Pre-slice Correction

The first `7.4b7g` implementation attempt was rejected before transfer. Adding
an unconditional `topic.concurrency` metadata requirement exceeded the
accepted write set because four dependent binding/Interop checkers each own an
explicit metadata closure. Independent review also found that the draft
conflated asynchronous provider delivery with locally outliving callback work,
mandated one shutdown sequence, lacked lifecycle-phase evidence, treated
repeated unregistration as universally successful, and did not prove the
bounded legacy edit strongly enough.

**Decision:** use conditional Concurrency selection. Interop owns provider-
granted registration, delivery guarantees, in-flight provider behavior,
unregistration, foreign release, and provider shutdown facts. Select
Concurrency only when callback-created work can outlive the callback
invocation. Do not add `topic.concurrency` to the profile's unconditional
metadata requirements and do not edit dependent metadata-closure checkers.

**Allowed write set:**

- this report;
- `milestone-7-independent-trust-groups.tsv`;
- `milestone-7-independent-trust-next-slice.tsv`;
- `verify-milestone-7-independent-trust-replan.sh`;
- evaluation README, findings, active plan, and execution ledger.

No normative or legacy standard, final disposition, generated inventory,
owner map, parent decomposition report, implementation checker, metadata
contract, router, template, source, test, configuration, dependency, lockfile,
build output, runtime, workflow fixture, or downstream repository belongs to
this corrective planning slice.

**Acceptance result:** the corrective decision is accepted. The corrected
implementation contract preserves the existing Interop metadata closure, makes
Concurrency conditional, requires provider-selected ordering and
repeated/concurrent behavior, requires phase-aware typed outcomes, and requires
staged-diff proof that unrelated legacy Interop sections remain byte-for-byte
unchanged. Normative implementation remains blocked until `7.4b7f2` repairs
the pre-existing complete-suite verification defect.

**Verification procedure:** invoke the complete checker suite with fail-fast
shell behavior. A loop whose final command succeeds does not prove earlier
checkers passed.

**Verification result:** the focused independent-trust checker, plan lifecycle,
shell syntax, and whitespace checks pass. The fail-fast complete suite stops at
`verify-rust-binding-executor-delegation.sh` because that checker still
requires the historical partial `F026` status from `7.4b4e`; the accepted
`7.4b5f` slice resolved `F026`. The live `f497517` baseline fails the same
assertion, proving this is a pre-existing checker defect rather than a result of
the corrective planning diff. This defect is recorded as `F050`.

**No fallback:** do not broaden the implementation write set to repair an
unnecessary unconditional dependency, treat asynchronous provider delivery as
proof of outliving local work, impose a universal shutdown order, assume
repeated unregistration is idempotent, or accept a suite command that masks an
intermediate failure.

## Accepted Slice 7.4b7f2: Executor Delegation Verification Repair

**Outcome:** restore truthful complete-suite verification before normative
Interop work by replacing the stale temporary `F026` assertion with the
accepted resolved state.

**Allowed write set:**

- `verify-rust-binding-executor-delegation.sh`;
- this report and checker for prerequisite and accepted-state handoff;
- evaluation README, findings, active plan, and execution ledger.

No normative or legacy standard, disposition, fixture, generated artifact,
owner map, router, metadata contract, parent decomposition report, source,
configuration, dependency, lockfile, build output, workflow fixture, runtime,
or downstream repository belongs to this verification-only slice.

**Required correction:** replace only the stale temporary `F026` status
assertion. Preserve the executor-delegation decisions, exact `STD-0781`
disposition, metadata closure, canonical profile requirements, bounded legacy
proof, and dependent decomposition checks.

**Acceptance gate:** the repaired checker passes directly; the focused
independent-trust checker still passes; the staged diff contains only the
authorized verification and planning artifacts; shell syntax and whitespace
pass; and every `evaluation/standards-effectiveness/verify-*.sh` checker passes
under fail-fast execution.

**Acceptance result:** accepted. The executor-delegation checker now requires
the stable resolved `F026` state established by `7.4b5f`. Its decision fixture,
exact `STD-0781` disposition, metadata closure, profile requirements, bounded
legacy proof, and dependent decomposition checks remain unchanged. Focused,
affected, and fail-fast complete-suite verification pass.

**No fallback:** do not weaken or skip the checker, accept multiple `F026`
states, rewrite historical evidence, change normative behavior, or continue to
`7.4b7g` while the complete suite is red.

## Accepted Slice 7.4b7g: Event Registration Lifecycle Contract

[milestone-7-independent-trust-next-slice.tsv](milestone-7-independent-trust-next-slice.tsv)
freezes `STD-0473`.

**Outcome:** extend `profiles/boundaries/interop.md` so foreign event
registration, callback delivery guarantees, unregistration, release, and
provider shutdown follow one explicit provider/subscriber lifecycle contract,
while callback-created work that can outlive its invocation is conditionally
routed to Concurrency.

**Allowed write set:**

- `profiles/boundaries/interop.md`;
- only the event-subscription section in `INTEROP-STANDARDS.md`;
- `evaluation/standards-effectiveness/fixtures/interop/event-registration-decisions.tsv`;
- new `evaluation/standards-effectiveness/verify-interop-event-registration.sh`;
- this report and checker for accepted disposition and handoff state;
- `evaluation/standards-effectiveness/consolidation-dispositions.tsv`;
- evaluation README, findings, active plan, and execution ledger.

No contract-evolution, runtime-decoding, serialization, enum/struct alignment,
routing, IPC, Language Binding, generic Concurrency normative change,
language-specific, dependent metadata-closure checker, parent decomposition
report, generated, template, package/configuration/dependency/lockfile,
workflow fixture, source, runtime, build-output, or downstream file belongs to
this slice.

**Required semantics:**

- name registration, callback, unregistration, and foreign release authority;
- define callback thread, re-entrancy, input lifetime, and in-flight delivery
  behavior;
- keep provider delivery scheduling separate from callback-created work
  lifetime, selecting Concurrency only when local work can outlive invocation;
- make the provider contract select repeated and concurrent unregistration
  outcomes instead of assuming idempotent success;
- make the provider contract select and prove valid delivery stop,
  quiescence/cancellation, unregistration, release, and shutdown ordering
  instead of imposing one sequence;
- distinguish pre-registration, active, unregistering, and released lifecycle
  phases;
- distinguish complete cleanup from typed incomplete cleanup; and
- return `invalid`, `unsupported`, or `unavailable` when required lifecycle
  facts or capabilities cannot be established.

**No fallback:** do not retain destruction-, finalizer-, or garbage-collection
cleanup; bypass Concurrency ownership with detached callback work; retain a
stale registration; silently drop callbacks; retry on an arbitrary thread;
select an alternate event mechanism; or claim successful cleanup after
incomplete foreign release.

**Focused evidence:** decisions independently cover lifecycle phase, provider
delivery scheduling, local callback-work lifetime, in-flight delivery,
provider-selected repeated/concurrent unregistration outcomes, provider-
selected subscriber/provider shutdown and release ordering, unavailable
quiescence/release capability before and after activation, conditional
Concurrency routing, and rejection of framework lifecycle assumptions and
detached callback cleanup.

**Acceptance gate:** `F049` is resolved; `STD-0473` has one exact `refine`
disposition; the Interop profile owns the complete registration lifecycle; the
legacy section is a bounded canonical link without C#/TypeScript examples or
destruction-linked cleanup; Contracts, Concurrency, and existing Interop
ownership checks pass; staged diff proves unrelated Interop sections remain
byte-for-byte unchanged; and focused plus affected regressions pass under a
fail-fast complete-suite invocation.

**Pre-slice review:** accepted. Event registration is a foreign resource with
provider-governed callback and release authority already owned by the Interop
boundary profile. The one-ID slice completes that lifecycle without absorbing
event-domain behavior, Contracts, IPC, Language Bindings, language recipes, or
the other nine mixed-role Interop sections. The verification-only `7.4b7f2`
prerequisite is accepted, so this normative slice is now active.

**Acceptance result:** accepted. The Interop profile now owns the explicit
provider-governed registration lifecycle and phase-aware typed outcomes.
Provider delivery mode remains independent from local callback-work lifetime;
only outliving work selects Concurrency. Provider contracts select
repeated/concurrent unregistration outcomes and valid delivery, quiescence,
release, and shutdown order. The legacy event section is one bounded canonical
link, `STD-0473` has one exact `refine` disposition, and `F049` is resolved.

**Independent review findings (`Resolved`):** the initial evidence let fallback
attempts erase the phase-selected diagnostic, represented only pairwise order,
and did not tie repeated/concurrent outcomes tightly enough to selected
provider contracts. The corrected fixture preserves root diagnostics, records
complete selected and observed lifecycle sequences with quiescence before
release, rejects mismatched sequences, and proves selected repeated and
concurrent outcomes.

Forty-three focused decisions cover all lifecycle phases, both delivery modes
with inline and outliving work, four valid provider-selected orders, repeated
and concurrent outcomes, capability loss before and after activation, current
input isolation, incomplete cleanup, and all prohibited fallback paths. The
rolling remainder is 593 identifiers across 29 sources and 28 owners, with 13
owners still missing. The independent trust subset is 60 identifiers across
six owners.

## Planned Slice 7.4b7h: Independent Trust Remainder Re-plan

**Outcome:** re-measure the 593-ID global remainder and 60-ID independent trust
subset, correct the next residual owner boundary, and activate exactly one
dependency-ready implementation slice without normative movement.

**No fallback:** do not infer the next owner from the historical group order,
combine mixed-role identifiers, reuse the completed `STD-0473` disposition,
invent a missing owner, or start another implementation before exact
measurement and pre-slice review pass.

## Re-Plan Triggers

- Event registration cannot be represented as provider-governed foreign
  resource lifecycle without moving event-domain behavior into Interop.
- Correct cleanup requires a generic Concurrency or Contracts change outside
  the activated owner boundary.
- A provider contract cannot distinguish cancellation, in-flight delivery,
  unregistration, release, and shutdown completion.
- Focused evidence cannot distinguish complete cleanup from typed incomplete
  cleanup.
- Implementation needs an undisposed identifier, owner, source, generated
  artifact, configuration, lockfile, workflow fixture, or downstream file
  outside the activated write set.
