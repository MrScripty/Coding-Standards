# Milestone 7 Row 5 Decomposition

## Purpose

This report records the bounded owner review of immutable execution row 5,
`STD-0804` through `STD-0809`. It is planning evidence, not normative policy.

The baseline row proposes one Rust Language Binding owner, but the frozen text
contains four independently changeable outcomes. Implementing it as one rule
would duplicate accepted generic owners and preserve fixed framework,
compatibility, and version-discovery defaults.

## Scope

This slice changes only:

- this report and its focused checker;
- the execution decomposition overlay;
- the acceleration package outcome; and
- the active plan, acceleration report, evaluation index, findings, and
  execution ledger.

It changes no normative or legacy standard, disposition, generated artifact,
owner map, immutable baseline train row, router, metadata, dependency
declaration, decision fixture, configuration, lockfile, or downstream
repository.

## Frozen Evidence

| IDs | Frozen concern | Ownership finding |
| --- | --- | --- |
| `STD-0804` | Rustler/NIF pure-logic separation and a framework-specific example | Rust binding architecture specializes the accepted framework-independent core/adapter boundary. |
| `STD-0805`, `STD-0806` | Binding approach catalog and universal framework-selection rules | Generic Language Binding owns boundary-mechanism selection; selected IPC/process boundaries route to their own profiles. |
| `STD-0807`, `STD-0808` | Additive/breaking claims, regeneration, and lockstep versions | Contracts owns compatibility classes, deployment facts, generated consistency, and supported-version evidence. |
| `STD-0809` | Mandatory runtime `version()` export | Rust binding adaptation implements a discovery mechanism only when the selected contract requires one. |

## Binding Decomposition

Row 5 receives four ordered children in
[the execution decomposition overlay](milestone-7-execution-decomposition.tsv):

### Child 5.1: Rust Core And Adapter Testability

- IDs: `STD-0804`
- Owner: `profiles/languages/rust/language-bindings.md`
- Outcome: consolidate NIF-specific separation into the accepted Rust
  core/adapter boundary and framework-free core evidence.

Domain logic and validated types remain usable without the binding framework
or foreign runtime. Adapter tests and real host evidence remain distinct from
core tests. A named Rustler layout or unknown-sentinel example cannot become a
universal architecture.

### Child 5.2: Boundary Mechanism Selection

- IDs: `STD-0805`, `STD-0806`
- Owner: `profiles/boundaries/language-bindings.md`
- Outcome: select the boundary mechanism from host, process, deployment,
  representation, lifecycle, performance, isolation, and support facts.

The owner distinguishes binding-framework lifting, generated wrappers, stable
ABI, opaque handles, serialized transport, and a separately selected process
or IPC boundary. It does not choose UniFFI from target count, prescribe
Rustler, PyO3, Tauri, RPC, or handwritten FFI from one host label, or switch to
another mechanism after the selected mechanism is unsupported or unavailable.

### Child 5.3: Binding Contract Evolution

- IDs: `STD-0807`, `STD-0808`
- Owner: `topics/contracts.md`
- Outcome: consume accepted contract classes and deployment facts for
  generated, public, persisted, ABI, wire, package, and coordinated evolution.

Additive syntax is not universally compatible. Producer and consumer
deployment, exhaustive enums, defaults, generated artifacts, persisted state,
and published promises select replacement, migration, negotiation, or typed
rejection. Native and wrapper versions are not forced into lockstep.

### Child 5.4: Rust Contract Discovery Adaptation

- IDs: `STD-0809`
- Owner: `profiles/languages/rust/language-bindings.md`
- Outcome: implement a checked Rust/host discovery or negotiation mechanism
  only when required by the selected Contracts-owned boundary contract.

The selected contract defines identity, version or capability representation,
consumer behavior, unsupported states, and evidence. A universal `version()`
function, package-version string, alternate discovery path, guessed
compatibility, or default success is prohibited.

## Order

The children remain serial:

1. preserve the core/adapter boundary;
2. select the applicable boundary mechanism;
3. establish evolution semantics from contract facts; and
4. adapt any required discovery mechanism in Rust.

All children must receive exact dispositions in order before immutable row 6
can activate. Partial or out-of-order completion remains invalid.

## No Fallback

This decomposition does not retain:

- framework-specific examples as generic architecture;
- target-count or host-label mechanism defaults;
- Tauri, RPC, or another boundary as a substitute for a failed binding;
- blanket additive compatibility;
- mandatory major-version or lockstep wrapper/core rules;
- regeneration without canonical-source and consumer evidence;
- a universal runtime version export; or
- alternate discovery, guessed compatibility, or default success.

Missing contract facts or capability return the applicable typed diagnostic.

## Progress

Milestone `7.4b8o` accepted child `5.1`, `STD-0804`, as one Rust Language
Binding core/adapter testability contract with focused decision-table evidence
and one exact disposition.

Milestone `7.4b8p` accepted child `5.2`, `STD-0805` and `STD-0806`, as generic
Language Binding boundary-mechanism selection with focused decision-table
evidence and two exact dispositions.

Milestone `7.4b8q` accepted child `5.3`, `STD-0807` and `STD-0808`, as
Contracts-owned binding evolution with focused decision-table evidence and two
exact dispositions.

Milestone `7.4b8r` accepted child `5.4`, `STD-0809`, as Rust adaptation of a
Contracts-selected discovery mechanism with focused decision-table evidence
and one exact disposition.

Row 5 is complete. Milestone `7.4b8s` begins bounded owner review of immutable
row 6, `STD-0294` through `STD-0299`.
