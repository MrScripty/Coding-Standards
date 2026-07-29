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

The rolling disposition gate reports 591 residual identifiers across 28 legacy
sources and 27 proposed canonical owners, with 13 owners still missing.

[milestone-7-independent-trust-groups.tsv](milestone-7-independent-trust-groups.tsv)
records 61 frozen baseline identifiers and 58 current identifiers:

| Order | Proposed owner | Frozen | Current | State | Dependency or blocker |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | `topics/security.md` | 7 | 7 | Decompose | Contracts |
| 2 | `topics/cross-platform.md` | 6 | 6 | Decompose | Missing Tooling owner for affected rows |
| 3 | `profiles/boundaries/interop.md` | 10 | 9 | Decompose | Contracts; `STD-0473` accepted |
| 4 | `profiles/languages/rust/interop.md` | 1 | 0 | Accepted | `STD-0757` accepted |
| 5 | `profiles/languages/rust/security.md` | 3 | 2 | One accepted | `STD-0824` accepted; `STD-0826` remains blocked on missing Rust API |
| 6 | `profiles/languages/rust/language-bindings.md` | 34 | 34 | Decompose | Language Bindings, Rust Async, and missing Tooling owner for affected rows |

The baseline includes accepted `STD-0473`, `STD-0757`, and `STD-0824`. Owner-map
destinations remain audit proposals until an accepted pre-slice review proves
each section's role and correctness.

## Selection Decision

Select only `STD-0583` and `STD-0601`. Together they define when validation
proof remains authoritative and when a new applicable boundary or lost proof
requires decoding again. That is a Contracts concern, not generic Security
implementation structure. Security retains authority over which untrusted
values require proof and the consequences of invalid input.

The implementation must represent validation as a construction result whose
complete contract remains established. It must require new proof after loss of
the validated representation, unchecked mutation, contract change, or a new
applicable boundary, while avoiding redundant decoding inside one preserved
contract. It must not trust the original unknown input, a stale proof, a mutable
alias, or an unproved value merely because validation happened earlier.

## Remainder Ownership Audit

The re-measurement found that several proposed owner-map destinations are not
implementation-ready. This is recorded as `F048`; each affected group requires
an owner-correction or decomposition re-plan before activation:

- generic Security validation sections mix authority, runtime proof,
  filesystem use, domain constraints, and implementation structure;
  `STD-0583` and `STD-0601` form one corrected Contracts proof-lifetime slice;
- generic Cross-Platform native-library and CI sections mix Interop resource
  lifecycle, Release artifact identity, Documentation, and Verification
  scheduling;
- generic Interop contract and wire sections mix Contracts, IPC, Language
  Bindings, and routing;
- `STD-0757` is accepted as a Rust Language Binding representation;
- the Rust Security remainder contains one bounded external-input queue
  contract plus index closure and panic/API policy, with `STD-0826` blocked on
  the missing Rust API owner; and
- the 34-ID Rust Language Binding remainder requires separate packaging,
  support-surface, error, callback, generation, build, selection, and
  compatibility slices, including affected rows blocked on the missing Tooling
  owner.

All 58 current identifiers remain under `F048` in this planning slice. Only
`STD-0583` and `STD-0601` are activated for the next implementation; no other
group or generic section is pre-approved.

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

## Accepted Slice 7.4b7h: Independent Trust Remainder Re-plan

**Outcome:** re-measure the 593-ID global remainder and 60-ID independent trust
subset, correct the next residual owner boundary, and activate exactly one
dependency-ready implementation slice without normative movement.

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

**Remeasurement:** the rolling remainder remains 593 identifiers across 29
legacy sources and 28 proposed owners, with 13 proposed owners still missing.
The independent trust subset remains 60 identifiers across six proposed-owner
groups. Accepted `STD-0473` is excluded from both current counts while its
frozen Interop group remains visible as historical decomposition evidence.

**Independent review:** the first isolated draft selected six generic Security
validation identifiers for Contracts. Review rejected that selection before
transfer because the group still mixes Core trust-boundary rules, Contracts
validated-value reuse, Security authority consequences, implementation
structure, and the decomposable validation table in `STD-0590`. The rejected
draft created no live change, disposition, or fallback plan.

The six proposed-owner groups are baseline decomposition groups, not current
owner authority. Their 61 frozen identifiers include accepted `STD-0473`; the
current remainder is 60. The group fixture now names its count `frozen_ids`
rather than inaccurately calling all 61 identifiers remaining.

**Owner correction:** `STD-0757` is a serialized Rust/host representation, not
foreign-memory authority. Its canonical owner is
`profiles/languages/rust/language-bindings.md`, consuming Contracts and the
generic Language Binding boundary. That owner and every declared prerequisite
already exist. The other groups remain blocked on decomposition or a missing
owner; row order does not make either no-prerequisite generic group ready.
In particular, `STD-0826` cannot move until a Rust API profile owns panic/API
policy, and tooling-oriented Cross-Platform and Rust Language Binding rows
cannot move until their Tooling workflow owner exists. Those later exact
subsets remain unresolved under `F048`; this slice does not invent either
owner or pre-approve their dispositions.

The legacy Serde section treats attributes as a complete wire contract and
prescribes explicit casing plus shared generation without first selecting the
schema, serializer, consumer contract, and available generation capability.
The canonical Rust specialization must derive the effective serialized shape
from the selected schema and all applicable Serde attributes, require consumer
agreement and native/host evidence, and preserve typed outcomes when a schema,
variant, or capability is invalid, unsupported, or unavailable. This conflict
is recorded as `F051`.

**Selection decision:** freeze the one corrected identifier in
[milestone-7-independent-trust-next-slice.tsv](milestone-7-independent-trust-next-slice.tsv)
for `7.4b7i`. The Rust Language Binding profile already applies to serialized
wire contracts, distinguishes serialized values from native, ABI, framework,
handle, and generated representations, and consumes the accepted generic
owners. The slice may refine only that Rust profile, replace only the legacy
Serde section, update the Rust profile index, add focused evidence, and record
one exact disposition.

**Pre-slice review:** accepted. One Rust Language Binding specialization can
own Serde-specific schema and attribute mechanisms without changing generic
Contracts, Interop, Language Binding, Security, Rust Interop, or Rust Async
authority. The legacy section is one bounded source group, and real
native/host round-trip evidence can distinguish schema agreement from
producer-only serialization.

**Acceptance gate:** the checker proves the exact 593-ID global and 60-ID
independent-trust remainders, the exact 61-ID frozen baseline across six
proposed-owner groups, exact one-ID corrected Rust Language Binding proposal,
zero premature dispositions, accepted
dependencies, active-plan handoff, parent linkage, plan lifecycle, shell
syntax, whitespace, and all standards-effectiveness regressions.

**Final review findings (`Resolved`):** the corrected checker now requires
exactly zero `STD-0757` dispositions during the planning slice; the report has
one current 61-baseline/60-current audit instead of stale 61-remaining
language; the group fixture records and verifies missing Rust API and Tooling
owners; and the active-plan report label names the current Rust wire-
representation handoff.

**No fallback:** do not infer the next owner from the historical group order,
combine a mixed generic group, treat Serde attributes or Rust-native layout as
a schema substitute, assume default casing, tagging, enum, or field behavior,
reuse the completed `STD-0473` disposition, invent a missing owner, or start
another implementation before exact measurement and pre-slice review pass.

## Planned Slice 7.4b7i: Rust Serialized Binding Representation

**Outcome:** make the Rust Language Binding profile canonical for deriving and
proving a selected Serde wire representation across a real Rust/host boundary.

**Allowed write set:**

- `profiles/languages/rust/language-bindings.md`;
- only the legacy “Serde Wire-Format Alignment” section in
  `languages/rust/RUST-INTEROP-STANDARDS.md`;
- `profiles/languages/rust/README.md`;
- `fixtures/rust/wire-representation-decisions.tsv`;
- `verify-rust-wire-representation.sh`;
- `consolidation-dispositions.tsv`;
- this report and checker;
- evaluation README, findings, active plan, and execution ledger.

No generic Contracts, Interop, Language Binding, Security, Rust Interop
profile, Rust Async, Router, metadata, template, generated, dependency,
configuration, lockfile, workflow fixture, runtime, or downstream file belongs
to the implementation slice.

**Required semantics:**

- select the wire schema and serializer contract before deriving shape;
- derive effective tags, content fields, casing, names, optionality, variants,
  and field representation from the selected schema and applicable Serde
  attributes;
- require receiving consumers to agree with that effective representation;
- preserve typed `invalid`, `unsupported`, and `unavailable` outcomes; and
- verify supported representations through native/host round trips and
  rejection cases, not producer-only serialization.

**No fallback:** reject schema-free JSON, Rust-native layout, default casing or
tagging, unknown-value sentinels, omitted unsupported variants, another
serializer or binding mechanism, generated-schema claims without selected
capability, producer-only tests, and weaker evidence.

## Re-Plan Triggers

- `STD-0757` requires a generic schema-policy change outside the Rust
  specialization.
- One exact disposition cannot replace the complete legacy Serde section
  without splitting generic Contracts and Rust mechanism ownership.
- Focused evidence cannot distinguish schema invalidity, unsupported
  representations, unavailable schema/generation capability, and native/host
  disagreement.
- Implementation needs an undisposed identifier, owner, source, generated
  artifact, configuration, lockfile, workflow fixture, or downstream file
  outside the activated write set.

## Accepted Slice 7.4b7i: Rust Serialized Binding Representation

**Outcome:** accepted. `STD-0757` now has one exact `refine` disposition from
the legacy Rust Interop source to the Rust Language Binding specialization.
The canonical representation contract requires selected schema and serializer
facts, complete applicable Serde attributes, consumer agreement, typed
`invalid`, `unsupported`, and `unavailable` outcomes, and native/host
round-trip plus rejection evidence. It rejects schema-free JSON, Rust-native
layout, assumed casing or tagging, unknown sentinels, omitted unsupported
variants, alternate serializers or bindings, unsupported generated-schema
claims, producer-only tests, and weaker evidence.

Only the legacy Serde Wire-Format Alignment section changed: its defaults and
examples are replaced with a bounded canonical link. The Rust profile index no
longer directs wire representation to the legacy Interop section. Unrelated
legacy Rust Interop sections remain byte-for-byte preserved.

The rolling remainder is 592 identifiers across 28 legacy sources and 27
proposed owners, with 13 proposed owners still missing. The independent trust
remainder is 59 identifiers across six proposed-owner groups. The frozen
61-ID group baseline remains historical evidence and includes accepted
`STD-0473` and `STD-0757`.

**Verification:** 27 focused wire-representation decisions, one exact
disposition, metadata and index closure, legacy-section preservation, affected
Language Binding and conversion regressions, independent-trust progress, plan
lifecycle, shell syntax, whitespace, exact staged scope, and every
`evaluation/standards-effectiveness/verify-*.sh` checker pass under fail-fast
execution.

## Planned Slice 7.4b7j: Independent Trust Remainder Re-plan

**Outcome:** re-measure the 592-ID global remainder across 28 sources and 27
owners, plus the 59-ID independent-trust remainder; correct exactly one next
owner boundary; and activate one dependency-ready implementation slice without
normative movement.

**Allowed write set:** the independent-trust report, its group and next-slice
fixtures and checker, the parent Milestone 7 decomposition report, evaluation
README and findings, active plan, and execution ledger. No normative or legacy
standard, final disposition, generated inventory, owner map, router, metadata,
template, configuration, dependency, lockfile, workflow fixture, runtime, or
downstream file belongs to this planning slice.

**No fallback:** readiness must follow exact current measurement, canonical
owner correctness, all prerequisites, and pre-slice review. The slice cannot
reuse a historical group order, treat the frozen baseline as a live remainder,
invent a missing owner, combine mixed roles, preserve legacy policy, or approve
an implementation disposition before the planning gate passes.

## Accepted Slice 7.4b7j: Independent Trust Remainder Re-plan

**Outcome:** accepted. The rolling remainder is 592 identifiers across 28
legacy sources and 27 proposed owners, with 13 proposed owners still missing.
The independent trust remainder is 59 identifiers across six proposed-owner
groups. The revised group fixture makes accepted baseline identifiers explicit
instead of encoding owner-specific subtraction in the checker.

**Selection decision:** `STD-0824` is a bounded external-input queue rule,
not a generic queue implementation recipe or Rust Async ownership rule. The
existing Rust Security profile owns operation resource limits and typed
resource outcomes. Its selected contract can state capacity, overload,
retention, rejection, and telemetry behavior without a fixed numeric limit or
default discard policy. This legacy defect is recorded as `F052`. `STD-0821`
remains index closure, and `STD-0826` remains blocked on the missing Rust API
owner.

**Pre-slice review:** accepted. One Rust Security specialization can own the
selected queue resource contract without changing generic Security,
Concurrency, Rust Async, Rust API, or Tooling authority. The legacy Bounded
Queues section is one cohesive source section. The implementation needs only
that profile, the bounded legacy section, focused decisions/checker, exact
disposition, and serial planning records.

**No fallback:** the queue contract cannot choose a fixed capacity, drop-oldest
or default reject behavior, silent discard, leaf-only telemetry, an unbounded
queue, another queue mechanism, or weaker evidence when the selected resource
or overload contract is missing.

## Planned Slice 7.4b7k: Rust External-Input Queue Contract

**Outcome:** make the Rust Security profile canonical for selecting and proving
external-input queue resource limits, overload behavior, retention or rejection
semantics, telemetry, typed outcomes, and Rust operation evidence for
`STD-0824`.

**Allowed write set:** `profiles/languages/rust/security.md`; only the legacy
Bounded Queues section in `languages/rust/RUST-SECURITY-STANDARDS.md`; one
focused Rust queue decision fixture and checker; the exact disposition; this
report, group and next-slice fixtures, and checker; evaluation README and
findings; active plan; and execution ledger. No generic Security, Concurrency,
Rust Async, Rust API, Tooling,
router, metadata, template, generated artifact, configuration, dependency,
lockfile, workflow fixture, runtime, source, build output, or downstream file
belongs to this implementation slice.

**Required semantics:** select capacity and overload behavior from the queue
owner's resource and operation contract before accepting external input; define
whether supported overload rejects, retains, or evicts work and its typed
outcome; emit selected owner telemetry for rejection or eviction; preserve
input/lifecycle ownership; and verify supported paths plus invalid,
unsupported, unavailable, overload, and rejected-fallback cases.

**No fallback:** reject a fixed capacity, implicit drop-oldest or reject-new
default, unbounded accumulation, silent discard, substitute queue/runtime,
leaf-only telemetry, prior input carry-forward, or producer-only/weaker
evidence. Return the typed selected outcome.

**Resolved re-plan trigger:** accepting `STD-0824` changes the current group
count and consumes the activated next-slice row. The approved serial write set
therefore includes the group and next-slice fixtures. This preserves explicit
accepted-ID evidence and prevents owner-specific checker subtraction or a
stale implementation handoff.

## Accepted Slice 7.4b7k: Rust External-Input Queue Contract

**Outcome:** accepted. Rust Security now owns selected queue capacity,
overload, retention or eviction semantics, telemetry, current-input ownership,
typed outcomes, and Rust operation evidence for `STD-0824`. The legacy fixed-
capacity and drop-oldest example is one bounded canonical link. Eighteen
focused decisions reject fixed/default/unbounded capacity, silent discard,
alternate runtime, prior-input carry-forward, and weaker evidence.

The rolling remainder is 591 identifiers across 28 legacy sources and 27
proposed owners, with 13 owners still missing. The independent trust remainder
is 58 identifiers across six frozen proposed-owner groups. The group fixture
records `STD-0824` as accepted, and no implementation candidate is activated
before the next planning-only slice.

## Planned Slice 7.4b7l: Independent Trust Remainder Re-plan

**Outcome:** re-measure the 591-ID global and 58-ID independent-trust
remainders, correct exactly one next owner boundary, and activate one
dependency-ready implementation slice without normative movement.

**No fallback:** do not infer readiness from frozen row order, retain the
consumed queue proposal, invent a missing owner, combine mixed roles, or create
a disposition before exact measurement and pre-slice review pass.

## Accepted Slice 7.4b7l: Independent Trust Remainder Re-plan

**Outcome:** accepted. The rolling remainder is 591 identifiers across 28
legacy sources and 27 proposed owners, with 13 proposed owners still missing.
The independent trust remainder is 58 identifiers across six proposed-owner
groups. No normative standard or final disposition changed.

**Selection decision:** `STD-0583` and `STD-0601` are one validation
proof-lifetime contract. Contracts already owns validated representations,
proof invalidation, and repeated decoding at new applicable boundaries.
Security owns untrusted-input consequences, but does not own a universal
central validator or absolute trust for every internal value. The paired move
prevents either legacy absolute from surviving alone. This defect is recorded
as `F053`.

**Pre-slice review:** accepted. The two source sections are semantically
coupled, their corrected Contracts owner exists, and no missing Tooling or Rust
API owner is required. `STD-0821` remains final index closure. `STD-0826`
remains blocked on the missing Rust API owner. The other generic Security rows
still require separate decomposition.

**No fallback:** validation history cannot authorize the original unknown
input, a stale proof, unchecked mutable alias, changed contract, or value that
crossed a new applicable boundary. Conversely, the implementation cannot
mandate redundant decoding while the same validated representation and
complete contract remain intact.

## Planned Slice 7.4b7m: Validation Proof-Lifetime Contract

**Outcome:** make Contracts canonical for the lifetime and invalidation of a
validated representation for `STD-0583` and `STD-0601`.

**Allowed write set:** `topics/contracts.md`; only the legacy Core Principle
and What NOT to Validate sections in `SECURITY-STANDARDS.md`; one focused
validation proof-lifetime decision fixture and checker; two exact
dispositions; this report and checker; group and next-slice fixtures;
evaluation README and findings; active plan; and execution ledger. No generic
Security normative section, Cross-Platform, Interop, Rust profile, Tooling,
Rust API, router, metadata, template, generated artifact, configuration,
dependency, lockfile, workflow fixture, runtime, source, build output, or
downstream file belongs to this implementation slice.

**Required semantics:** define a validated representation as the proof-bearing
construction result; preserve its authority only while the complete contract
and invariants remain established; require new proof after representation
loss, unchecked mutation, contract change, or a new applicable boundary; and
avoid redundant decoding for unchanged values retained inside one trusted
contract.

**No fallback:** reject original-input reuse, validation-history flags, stale
proof, unchecked mutable aliases, implicit trust after a new boundary,
permissive defaults, weaker decoders, and redundant validation mandates that
discard an intact proof-bearing representation.
