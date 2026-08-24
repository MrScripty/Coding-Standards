# Milestone 4 Single-State Acceptance

## Status

Milestone 4 and Plan A1 are accepted.

The accepted implementation boundary is commit
`94b295b40bc1cef9a6281355d68115f3a98ed112`, tree
`ff032da51fcaff45533c07daa8de464065b8e55c`.

## Accepted Outcome

A1 now has one lifecycle identity:

```text
immutable authority + dependency-valid decisions
                      |
                      v
                AnalysisState
                      |
                      v
                AnalysisHandle
                      |
                 project(state)
                  /          \
                 v            v
          PendingResult  CompleteResult
```

The implementation removes packet and report identities, hidden mutable
sessions, global supersession, temporal packet staleness, raw standards-change
facts, and caller-coordinated observation lists. Pending and complete results,
requirements, obligations, reading plans, certificates, and completion proofs
are deterministic non-authoritative projections.

Authorized submissions advance one immutable state to another. Repeating the
same transition is idempotent; different valid submissions create independent
children. Mutable proposal-head coordination remains outside A1 and belongs to
future controlled authoring.

## Authority And Reuse

State identity binds exact accepted and proposed snapshots, normalized changes
and semantic proposals, semantic contract versions, authorization-authority
and provider-contract/input views, evidence, coverage attestations, and every
dependency-valid accepted decision. It excludes lineage, transition order,
timestamps, summaries, store location, and derived work.

Applicability uses semantic fact contracts, topology-independent analysis
contexts, content-addressed requirements, and evidence- and
authorization-bound observations. Only current material requirements block
completion. Dependency-valid observations remain available when dormant, and
prior analysis contributes decisions only after exact dependency
revalidation.

Providers return typed claims over declared immutable inputs. The analysis
module alone validates claims and constructs canonical observations. Provider
unavailability is distinct from deterministic absence.

## Coverage And Lifecycle

The provider-v2 coverage projection, 856-member independent horizon, 28
coverage subjects, compiled policy-impact relationships, and accepted
attestations remained valid at the implementation boundary. The complete
verifier accepted every current certificate. Because the single-state cutover
changed analysis lifecycle authority but no coverage-authority input, no
additional attestation renewal was required.

Existing behavioral fixtures cover same-module and cross-module moves, splits,
and merges, including predecessor/successor impact union and lifecycle
reciprocity.

## Contract Cutover

The replacement is coordinated across:

- The typed Python request/result interface.
- Agent tool schemas and adapters.
- Canonical JSON Schema interface version 8.
- Analysis-state schema and identity version 2.
- Analysis contract version 5.
- Applicability language version 3.
- Examples, identity fixtures, deterministic text rendering, and inspection.
- In-memory and cold-process filesystem state stores.

No packet/report compatibility loader or alternate analysis runtime remains.

## Verification

The exact implementation tree passed:

- 80 `standards_analysis` tests.
- 30 `standards_engine` tests.
- 12 `standards_applicability` tests.
- 7 `standards_policy_impact` tests.
- 17 `standards_metadata` tests.
- 35 `graph_engine` tests.
- 2 `standards_graph` tests.
- 380 `standards_verifier` tests.
- Contract validation for 33 examples, 8 identity fixtures, 4 operation
  envelopes, and 134 definitions.
- All 218 declarative suites.
- The complete standards checkpoint with 53 retained Bash checkers.
- Ruff formatting and lint checks.
- Git diff checks.

Focused evidence includes same-work/different-evidence identity, repeated
preparation, idempotent transitions, independent branches, decision-order
normalization, dormant observations, provider unavailability, authorization
validation, exact completion, typed modification/addition/removal workflows,
and genuine cold-process reconstruction with no shared in-memory store.

## Deferred Scope

Plan A2 controlled authoring, Plan B evidence-oracle policy, and Plan C
external project baselines remain inactive and require independent admission.
