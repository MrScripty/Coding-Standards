# Milestone 0 Architecture And Contract Review

## Review Boundary

This review covers only the Standards Engine A1 architecture decision and
canonical interface contracts. It does not accept runtime behavior, metadata
cutover, repository mutation, controlled authoring, evidence-oracle policy, or
external-project baselines.

Reviewed artifacts:

- [Architecture decision](../../../../decisions/standards-engine-navigation-analysis.md)
- [Contract README](../../../../../tools/standards_engine/contracts/README.md)
- [Canonical schema](../../../../../tools/standards_engine/contracts/a1-contract.schema.json)
- [Examples](../../../../../tools/standards_engine/contracts/examples/a1-examples.json)
- [Identity fixtures](../../../../../tools/standards_engine/contracts/identity-fixtures.json)
- Contract validator (historical path: `tools/standards_engine/contracts/validate_contracts.py`)

The integration owner performed the architecture and contract review against
the routed Architecture, Contracts, Diagnostics, Security, Cross-Platform,
Documentation, Tooling, Verification, Planning, and Implementation standards.

## Architecture Review

| Concern | Accepted result |
| --- | --- |
| Module depth | `standards_engine` is a small facade; neutral metadata, graph mechanics, and standards-specific analysis remain independent lower modules. |
| Dependency direction | Analysis depends on neutral metadata and graph contracts. The verifier is a consumer, not an upstream owner. No lower module depends on the facade. |
| Authority | Documents own meaning, canonical metadata owns module identity, sidecars own policy-unit identity, relationship declarations own semantic edges, and generated artifacts remain projections. |
| Product boundary | A1 is read-only navigation and analysis. Controlled authoring and apply-eligible acceptance remain excluded. |
| Caller interface | Typed Python and structured tool calls are authoritative. Text labels and CLI syntax are optional projections. |
| Snapshot bootstrap | A trusted source provider issues the initial opaque snapshot handle. Callers do not provide repository paths, and adapters cannot substitute ambient current state. |
| Authorization | Trusted adapters inject capability context outside caller-authored payloads. Analysis, consumer review, impact review, and audit review remain independent capabilities. |
| Graph composition | Impact uses `policy-impact` and conditionally `standards-requires` and `standards-specializes`. It does not broaden through `semantic` or hide provenance through `standards-dependencies`. |
| Compatibility | Contract version 1 has one representation. Unknown versions are `unsupported`; no compatibility parser or fallback is accepted. |

No architecture applicability finding requires changing the selected module or
authority boundary. The decision is accepted.

## Contract Review

The canonical JSON Schema defines:

- every public operation envelope and request/result union;
- snapshot, navigation, policy, relationship, packet, report, certificate, and
  inspection handles;
- route, read, related, prepare, resolve, and inspect variants;
- expected typed rejection outcomes and trusted capability context;
- policy-unit declarations, tombstones, semantic overlays, and changed-policy
  dimensions;
- policy-impact, applicability-fact, audit-horizon, audit-declaration,
  certificate, decision-contract, and dependency-fingerprint representations;
- six change seed variants and their exact named graph groups;
- packet obligations, questions, submissions, reading plans, dispositions, and
  completion proof;
- clean-Git and dirty/non-Git snapshot evidence, including tracked/untracked
  state, exclusions, modes, symlink handling, gitlinks, nested state, and
  relevant contract and implementation provenance; and
- canonical identity domains and included/excluded field paths.

The review made these corrections before acceptance:

- separated graph seed descriptors from changed policy-unit semantic state;
- removed a redundant numeric reading-plan index because array order owns
  deterministic order;
- excluded self-identities, timestamps, summaries, derived next operations,
  and implementation-only versions from content identities;
- distinguished graph and analyzer implementation provenance from contract
  versions that can affect analysis identity;
- added explicit tool-call envelopes and trusted snapshot bootstrap;
- made handle ID domains type-specific;
- encoded all six accepted/proposed change cardinalities; and
- added corpus membership, audit renewal, decision-contract, and registered
  horizon fields needed for bounded coverage.

The schema remains the sole machine-shape authority. The validator implements a
declared strict subset of JSON Schema Draft 2020-12 and rejects unknown schema
keywords rather than silently ignoring a contract it cannot check. A future
need for unsupported schema behavior is a re-plan trigger.

## Verification

The following evidence passed from the current Milestone 0 tree:

```text
python3 tools/standards_engine/contracts/validate_contracts.py
PASS: 22 examples, 7 identity fixtures, 4 operation envelopes, 94 definitions
```

The validator also runs negative self-checks for:

- unsupported schema keywords;
- duplicate JSON keys;
- missing request discriminators;
- type-incompatible applicability facts;
- wrong content-addressed ID domains;
- Boolean/integer constant confusion; and
- invalid change identity cardinality.

Identity fixtures mutate every included field and require the identity to
change. They mutate every represented excluded field and require the identity
to remain stable. The accepted graph selections were also checked against the
current repository graph providers; all selected groups exist and neither
`semantic` nor `standards-dependencies` is selected.

Python syntax compilation passed with bytecode output redirected outside the
repository. Twelve affected declarative suites passed. The complete declarative
registry passed 218 selected, 218 passed, zero failed, and zero blocked. Plan
structure passed, 57 local links across all eight changed Markdown artifacts
resolved through the existing Markdown-link engine, and `git diff --check`
passed.

## Acceptance

Milestone 0 is accepted as architecture and contract authority. No runtime
module, metadata loader, generated Python projection, agent tool, compatibility
path, or controlled-authoring behavior was introduced.

Runtime implementation remains unavailable until this accepted planning slice
is committed, its exact commit and tree are recorded as the implementation
base, and the plan is explicitly started.
