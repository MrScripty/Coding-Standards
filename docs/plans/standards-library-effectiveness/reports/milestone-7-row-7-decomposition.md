# Milestone 7 Row 7 Decomposition

## Purpose

This report records the bounded owner review of immutable execution row 7,
`STD-0761` through `STD-0771`. It is planning evidence, not normative policy.

The baseline row proposes one Rust Language Binding owner, but the frozen text
mixes Rust workspace and verification mechanics, release artifact composition,
artifact compatibility, and generic binding-surface governance. Implementing
it as one rule would duplicate accepted Release, Contracts, Verification, and
generic Language Binding authority while preserving example layouts and broad
defaults as policy.

## Scope

This slice changes only:

- this report and its focused checker;
- the execution decomposition overlay;
- the acceleration package outcome and prerequisites; and
- the active plan, acceleration report, evaluation index, findings, execution
  ledger, and superseded cursor assertions.

It changes no normative or legacy standard, disposition, generated artifact,
owner map, immutable baseline train row, router, metadata, dependency
declaration, decision fixture, configuration, lockfile, or downstream
repository.

## Frozen Evidence

| IDs | Frozen concern | Ownership finding |
| --- | --- | --- |
| `STD-0761`, `STD-0762` | Example crate/binding directory layout and `default-members` exclusion for crates needing foreign runtimes | The Rust Language Binding profile owns binding-specific core/adapter package separation and its native/host evidence obligations. Workspace paths and Cargo membership are project mechanisms; unavailable foreign-runtime capability cannot remove required adapter evidence. |
| `STD-0763`-`STD-0766` | Product-native, wrapper, and host-package identities; mandatory artifact count and packaging; example release layout | Release owns the selected artifact set, artifact relationships, consumer information, and publication shape. Binding mechanism names do not replace product identity, but one native library per target, separate packages, and convenience-bundle status are not universal defaults. |
| `STD-0767` | Naming and compatibility notes for native and generated artifacts | Contracts owns compatibility class, coordinated replacement, independent-consumer windows, generated consistency, and artifact version relationships. A shared build or release does not force one compatibility promise or lockstep version. |
| `STD-0768`-`STD-0771` | Curated exported surface, support tiers, language parity, wrapper ownership, review questions, and evidence | The generic Language Binding boundary owns which client operations and representations are exposed. Contracts owns compatibility promises and Verification owns evidence claims; Rust only specializes representation and adapter mechanics. |

## Rust Binding Row Decomposition

Row 7 receives four ordered children in
[the execution decomposition overlay](../../../../evaluation/standards-effectiveness/milestone-7-execution-decomposition.tsv).

### Child 7.1: Rust Binding Workspace And Evidence Boundary

- IDs: `STD-0761`, `STD-0762`
- Owner: `profiles/languages/rust/language-bindings.md`
- Outcome: preserve core/adapter dependency direction and distinct core,
  adapter, generated, native, and host evidence without prescribing a crate
  tree or excluding required evidence.

Projects may select workspace members, package boundaries, features, scripts,
and separately provisioned host environments from their actual ownership and
toolchain facts. Missing foreign-runtime capability is typed `unavailable`; it
does not make required adapter or host evidence pass.

### Child 7.2: Binding Artifact Roles And Release Composition

- IDs: `STD-0763` through `STD-0766`
- Owner: `workflows/release.md`
- Outcome: identify native implementation artifacts, internal adapter or
  generator inputs, generated host artifacts, and optional bundles in one
  contract-selected release artifact plan.

The release derives artifact count, target coverage, package composition,
naming, relationships, and consumer installation/loading information from the
release unit, distribution channels, targets, and consumer contracts. Example
ZIP names and separate-package or convenience-bundle defaults do not become
generic requirements.

### Child 7.3: Binding Artifact Compatibility

- ID: `STD-0767`
- Owner: `topics/contracts.md`
- Outcome: classify each native adapter, generator input, generated source,
  host package, native package, ABI, wire representation, and persisted
  representation under its applicable contract.

Coordinated artifacts may be replaced atomically. Independently consumed,
persisted, public, or distributed artifacts follow their declared windows or
negotiation rules. Common build provenance may support consistency evidence,
but does not force lockstep versions or one compatibility promise.

### Child 7.4: Binding Surface Contract

- IDs: `STD-0768` through `STD-0771`
- Owner: `profiles/boundaries/language-bindings.md`
- Outcome: select the exported client surface, host-language subsets, support
  promises, representation, lifecycle, failure, documentation, and evidence
  from declared consumer and product contracts.

Domain semantics remain in the canonical backend or core owner. Adapters expose
only selected boundary representations and operations. Support labels,
language parity, packaging, and evidence are explicit contract facts rather
than universal tier names or automatic exports.

## Order

The children remain serial:

1. preserve Rust core/adapter boundaries and evidence obligations;
2. define the release artifact roles and composition;
3. apply compatibility contracts to each artifact independently; and
4. define the generic exported binding surface that consumes those contracts.

All children must receive exact dispositions in order before immutable row 8
can activate. Partial or out-of-order completion remains invalid.

## No Fallback

This decomposition does not retain:

- one prescribed crate, bindings, scripts, or generated-output layout;
- `default-members` exclusion as satisfaction of required foreign-runtime
  evidence;
- one native library per target, separate host packages, or optional bundles
  as universal architecture;
- framework-derived product identity or example ZIP names;
- same-build provenance as forced lockstep versioning or compatibility;
- automatic export of every technically available operation;
- fixed `supported`, `experimental`, and `internal-only` labels as a universal
  taxonomy;
- identical or non-identical language parity as a default; or
- native-only tests, documentation, or packaging as substitutes for required
  real host-boundary evidence.

Missing or contradictory contract facts produce typed diagnostics.

## Next Slice

Milestone `7.4b8x` accepted child `7.1`, `STD-0761` and `STD-0762`, as the
Rust binding package/workspace and evidence boundary with 14 decision cases
and two exact dispositions.

Milestone `7.4b8y` accepted child `7.2`, `STD-0763` through `STD-0766`, as
Release-owned binding artifact roles and composition with 23 decision cases
and four exact dispositions.

Milestone `7.4b8z` accepted child `7.3`, `STD-0767`, as Contracts-owned
per-artifact compatibility with 19 decision cases and one additional exact
disposition.

Milestone `7.4b8aa` accepted child `7.4`, `STD-0768` through `STD-0771`, as
the generic exported binding-surface contract with 19 decision cases and four
exact dispositions. Row 7 is complete.
