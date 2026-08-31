# Plan: Standards Engine A1c Corrective Revalidation

**Plan status:** `Accepted`

**Current phase:** Milestone 2 accepted

**Next slice:** `none`

**Acceptance status:** `satisfied`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Repair the accepted A1c implementation where the current Coding Standards audit
found false public-path, immutable-authority, dependency-local invalidation, and
evidence-lifecycle claims. Preserve A1c's single aggregate, opaque handles,
SQLite snapshot ownership, generated contract algebra, and external JSON Schema
semantics while reopening only the affected acceptance claims.

The accepted A1c reports remain historical evidence for commit `59934010`.
This plan owns corrective implementation and current revalidation; it does not
rewrite those reports as though the defects were absent at their original
boundary.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1CR-A1 | All eight agent operations execute through `AgentToolFacade`; valid `prepare` reaches Analysis and every malformed or unsupported request produces its owned typed result. | `user-workflow` | `representative` | `automated` | `satisfied` | [Milestone 0 ledger evidence](execution-ledger.md#2026-08-30---milestone-0-boundary-correction) |
| A1CR-A2 | Persisted analysis distinguishes malformed state from a well-formed unsupported version, checks current domain compatibility, and cold-projects every advertised child without ambient authority. | `integration` | `representative` | `automated` | `satisfied` | [Committed-candidate Engine evidence](execution-ledger.md#2026-08-30---milestone-1-dependency-local-coverage-acceptance) |
| A1CR-A3 | Snapshot creation requires identical first-pass and frozen-replay path closure as well as identical semantic output. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 0 ledger evidence](execution-ledger.md#2026-08-30---milestone-0-boundary-correction) |
| A1CR-A4 | A subject's coverage identity changes for its policy, relationships, consumers, evidence-suite closure, or shared interpretation protocol and remains stable for an unrelated suite input; completeness review still blocks missing or undispositioned consumers. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 1 ledger evidence](execution-ledger.md#2026-08-30---milestone-1-dependency-local-coverage-acceptance) |
| A1CR-A5 | Historical A1c migration evidence is content-bound and no permanent check compares that accepted boundary with unrelated future graph evolution. | `focused` | `not-applicable` | `automated` | `satisfied` | [Milestone 2 acceptance](reports/milestone-2-corrective-acceptance.md) |
| A1CR-A6 | Linux required-real evidence is limited to behavior that crosses the real platform boundary; deterministic transaction and lifecycle semantics retain focused evidence without being misrepresented as repeated platform proof. | `system` | `required-real` | `automated` | `satisfied` | [Milestone 2 acceptance](reports/milestone-2-corrective-acceptance.md) |
| A1CR-A7 | Version roles, local Git interpretation ownership, permanent byte-integrity evidence, and contract proof lifetime have explicit current decisions consistent with Architecture, Contracts, Dependencies, and Verification. | `contract` | `not-applicable` | `automated` | `satisfied` | [Milestone 2 acceptance](reports/milestone-2-corrective-acceptance.md) |
| A1CR-A8 | Focused package suites, generated freshness, complete declarative suites, retained checkers, formatting/linting, and diff hygiene pass on one coherent implementation. | `integration` | repository-supported verification environments | `automated` | `satisfied` | [Milestone 2 acceptance](reports/milestone-2-corrective-acceptance.md) |

## Scope

### In Scope

- Public A1c facade delegation and real-facade workflow evidence.
- Persisted AnalysisState shape, version, identity, and current-contract
  compatibility outcomes.
- Snapshot path-closure replay equality.
- One proof-bearing contract decode per public input boundary.
- Dependency-local coverage identity and the neutral suite-input manifest value
  needed by both Analysis and Verifier.
- Current coverage-attestation migration from the stronger global review to the
  narrower dependency-local identity without changing authored conclusions.
- Retirement of the permanent whole-graph A1b-to-A1c migration comparison.
- Proportional Linux platform claims and retained exact-byte integrity evidence.
- Version-role and Repository Git dependency decisions.

### Out Of Scope

- New A1c product operations, A2 authoring, or compatibility with an unreleased
  prior engine version.
- Windows or macOS support claims.
- Replacing SQLite, Git, `jsonschema`, the generated public algebra, opaque
  handles, or the single AnalysisState aggregate.
- A semantic consumer-discovery algorithm. Agents and authored attestations
  retain semantic completeness authority.
- Rewriting shared A1c history or altering historical acceptance reports.
- Normative standards changes; the current standards already select the needed
  corrections.

## Constraints And Assumptions

### Constraints

- Work is serial. Concurrent Plan Integration is not applicable.
- The user explicitly admitted corrective implementation after reviewing the
  current-tree audit. Review evidence and lifecycle updates do not prescribe
  commit topology.
- Existing authored complete attestations were made against a global superset
  of the new local dependency closure. Migration may preserve their conclusion,
  evidence, exclusions, rationale, and provenance, but must record the identity
  transformation and may not invent a new semantic review.
- Missing-consumer detection remains an independent authored completeness
  obligation. A local digest is never proof that an undeclared semantic
  consumer does not exist.
- The suite-input manifest is neutral immutable metadata. Verifier owns
  discovering inputs from checker implementations; Metadata owns the manifest
  value, validation, and per-suite closure projection; Analysis consumes that
  projection without depending on Verifier.
- No permanent evidence mechanism is added unless it has a distinct deciding
  claim. Existing checks are removed or narrowed when the repaired proof
  subsumes them.

### Assumptions

- Current `jsonschema` remains the Draft 2020-12 semantics owner.
- Current A1c stores are development artifacts without a published cross-engine
  migration promise. Correctly formed obsolete state returns `unsupported`;
  malformed or identity-contradictory state returns `invalid`.
- The accepted global coverage review is sufficient migration evidence for its
  dependency-local subset when the graph, consumer, and evidence dependencies
  are mechanically derived from that same reviewed authority.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Keep one A1c AnalysisState and generated result algebra; repair false boundary behavior in place. | Architecture and Engine | Current audit and accepted A1c ADR | None |
| Use one authoritative contract decode and proof-bearing generated value at the facade boundary. | Contracts | `topics/contracts.md` validation proof lifetime | Facade prevalidation followed by decoder revalidation |
| Separate malformed persisted state from well-formed unsupported contract versions and verify stored domain compatibility before projection. | Analysis and Contracts | Current audit | Combined unsupported outcome |
| Compare both semantic signatures and recorded requested-path sets during snapshot replay. | Snapshot and Engine | A1c ADR roots-only closure promise | Semantic-signature-only replay check |
| Place the neutral suite-input manifest value and per-suite dependency projection in `standards_metadata`; keep checker-specific discovery in Verifier. | Metadata and Verification | Deletion test: without the neutral value, Analysis and Verifier require parallel parsers and identity rules | Verifier-only manifest model and Analysis global horizon hashing |
| Keep completeness review independent from subject identity. Subject identity binds declared local dependencies; missing or undispositioned consumers still block through coverage review. | Analysis and Verification | Accepted dependency-local prototype and A1C-A5 | One complete-horizon digest in every subject |
| Retire the permanent whole-graph migration comparison after preserving its accepted fixture as historical evidence. | Verification | New evidence proportionality and bounded-population rules | Mutable-current-registry A1c migration check |
| Split platform evidence by claim: real Linux proves platform crossings; focused deterministic tests prove transaction and lifecycle semantics. | Verification | Current audit and evidence proportionality | One oversized A1C-A7 platform claim |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| Public facade | User workflow | Invoke each raw mapping through `AgentToolFacade` | Generated v12 schema and result algebra | v11 inputs | Exact typed interface rejection |
| Persisted state | Persistence/contract | Cold reopen exact aggregate and mutate shape/version independently | Stored identity plus current domain contract table | Unknown well-formed version | `invalid` for malformed; `unsupported` for unknown version |
| Snapshot closure | Immutable authority | Two recording sources over Git and frozen content | Exact requested-path sets and semantic signatures | Missing frozen input | `SNAPSHOT.CLOSURE_MISMATCH` |
| Local coverage | Identity/invalidation | Mutate one dependency class at a time | Compiled policy relationships, registered consumer content, neutral suite-input manifest | Never-declared semantic consumer | Missing disposition blocks; unrelated input preserves subject identity |
| Migration evidence | Evidence lifecycle | Historical fixture remains byte-bound and is absent from current mutable comparison | Accepted A1c report | Unknown external consumer | Retired path/current public-root checks still fail precisely |
| Platform | Runtime boundary | Real Linux facade/store harness plus focused deterministic Snapshot tests | OS, CPython, SQLite, and store contracts | Windows/macOS | Exact typed unavailable/invalid outcomes |

## Systemic Finding Audit

- Invariant family and canonical owner: public/internal boundary proof,
  immutable reconstruction, dependency-local identity, and permanent evidence
  lifecycle remain with their declared Engine, Snapshot, Analysis, and
  Verification owners.
- Bounded authority, representation, and reachable consumer population: all
  eight facade methods, AnalysisState decoding and cold loading, both snapshot
  compilation passes, every coverage subject, suite-input producer/consumer,
  A1c migration checker, and platform harness.
- Expansion facts: the population expands only for a newly discovered semantic
  owner, reachable consumer, material risk, or public or persistence promise.
- Consumer dispositions: exact findings are tracked in [issues.md](issues.md);
  each is fix-now or evidence-retirement in Milestones 0 through 2.
- Deletion, consolidation, smaller-Interface, stronger-proof, and
  evidence-replacement alternatives: subject-local invalidation replaces
  global per-subject hashing; one exact requirement reference replaces repeated
  attestation coordinates; neither replaces authored semantic completeness.
- Evidence-backed stopping condition: every selected consumer has a disposition,
  every current subject has one exact attestation and certificate, and focused
  mutation tests prove selected-change invalidation and unrelated stability.
- Repaired-composition comparison: the repair removes global and duplicated
  authority while preserving the original completeness and audit objective.

## Simplicity And Ownership Review

**Applicability:** `applicable`

- Independent concepts and dimensions: immutable suite-input observation,
  checker-specific discovery, subject-local dependency identity, and global
  semantic completeness are separate concerns.
- State, identity, value, time, policy, and mechanism: immutable values and
  semantic completeness remain separate from storage, version, and verifier
  mechanisms.
  - Canonical authority scope and referenced authorities: snapshot bytes own
    persisted inputs; Analysis owns coverage identity; authored attestations
    own semantic completeness; Verifier owns checker execution.
  - Version roles and owned promises: suite-manifest and repository-attestation
    current-format versions remain independent from AnalysisState and public
    Interface versions.
  - Supported compatibility overlaps and consumer matrix: no compatibility
    overlap is promised for the uncommitted repository-attestation format;
    Analysis and the eleven authored source files move atomically to v5.
  - Material identity-invalidation effects: selected relationship, consumer,
    or evidence-suite changes alter only dependent requirement identities;
    unrelated inputs do not.
- Caller and composition-root knowledge: callers pass opaque handles and raw
  operation values; Engine composes Metadata, Analysis, Snapshot, and Contracts.
- Representative change paths and forced owners: a suite input changes only
  subjects selecting its suite; a shared interpretation contract changes all;
  an unrelated graph addition does not rewrite historical A1c evidence.
- Stable Interfaces versus hidden knowledge: Metadata exposes one immutable
  manifest and per-suite fingerprint; it does not expose Verifier check classes.
- Independent evolution, testing, failure, and replacement: checker discovery
  and manifest interpretation can evolve independently through one serialized
  contract; malformed and unsupported states remain distinct.
- Necessary complexity and containment: no new package, operation, store,
  registry, certificate kind, or compatibility layer is introduced.
- Deletion and cumulative machinery result: delete the one-use migration
  checker; consolidate duplicate manifest interpretation and boundary
  validation; retain only claim-matched platform evidence.

## Milestones

### Milestone 0: Boundary Correctness

**Goal:** Make the existing public and persisted A1c boundaries satisfy their
already accepted contracts.

**Allowed write set:**

- `docs/decisions/standards-engine-a1c.md`
- `docs/plans/standards-engine-a1c-repair/plan.md`
- `docs/plans/standards-engine-a1c-repair/issues.md`
- `docs/plans/standards-engine-a1c-repair/execution-ledger.md`
- `docs/plans/standards-engine-a1c-repair/reports/dependency-and-version-decisions.md`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- `tools/standards_analysis/standards_analysis/state.py`
- `tools/standards_analysis/tests/test_state.py`
- `tools/standards_contracts/standards_contracts/runtime.py`
- `tools/standards_contracts/tests/test_semantics.py`
- `tools/standards_engine/standards_engine/engine.py`
- `tools/standards_engine/standards_engine/tools.py`
- `tools/standards_engine/tests/platform_harness.py`
- `tools/standards_engine/tests/test_analysis.py`
- `tools/standards_engine/tests/test_generated_contract.py`
- `tools/standards_engine/tests/test_platform_harness.py`
- `tools/repository_git/README.md`

**Tasks:**

- [x] Correct facade delegation and exercise every operation through it.
- [x] Split malformed and unsupported persisted-state outcomes and enforce
  current domain-contract compatibility.
- [x] Compare first and replay path closures.
- [x] Remove repeated validation of one unchanged public input.
- [x] Classify version roles and record the Repository Git dependency decision.

**Acceptance gate:** focused Analysis, Contracts, Engine, Snapshot, and
Repository Git tests pass; each repaired negative case reaches its exact
outcome; no public contract or handle version changes.

**Status:** `Accepted`

### Milestone 1: Dependency-Local Coverage

**Goal:** Preserve semantic completeness while making subject identity depend
only on its typed deciding closure.

**Allowed write set:**

- Plan, issue, ledger, ADR, and Milestone 1 evidence under this plan directory.
- `tools/standards_metadata/standards_metadata/suite_inputs.py`
- `tools/standards_metadata/standards_metadata/__init__.py`
- `tools/standards_metadata/tests/test_suite_inputs.py`
- `tools/standards_verifier/standards_verifier/suite_inputs.py`
- `tools/standards_verifier/tests/test_suite_inputs.py`
- `tools/standards_analysis/standards_analysis/coverage.py`
- `tools/standards_analysis/tests/test_coverage.py`
- `tools/standards_engine/standards_engine/engine.py`
- `tools/standards_engine/tests/test_analysis.py`
- `evaluation/standards-effectiveness/policy-coverage/horizons.toml`
- The eleven registered files under `evaluation/standards-effectiveness/policy-coverage/attestations/`.
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- `evaluation/standards-effectiveness/policy-impact-node-catalog.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/a1c/relationship-migration.tsv`
- `prompts/planning.md`
- `prompts/implement-plan.md`
- `templates/PLAN-TEMPLATE.md`
- `evaluation/standards-effectiveness/suites/contract-authority-scope.toml`
- `evaluation/standards-effectiveness/suites/systemic-finding-replanning.toml`
- Exact policy-impact declaration files selected for the new Metadata source and changed consumers after compiling the current graph.

**Tasks:**

- [x] Move the immutable suite-input manifest value and decoder upstream without
  moving checker discovery or execution.
- [x] Derive sorted per-suite transitive dependency fingerprints.
- [x] Replace global horizon bytes in each subject view with shared protocol,
  subject, relationship, consumer, and evidence-suite dependencies.
- [x] Preserve a separate completeness projection and exact missing-disposition
  failure.
- [x] Migrate current complete attestations from the reviewed global superset,
  recording the exact identity transformation without claiming a new audit.
- [x] Apply the admitted current-standards corrections from the seven-subject
  audit before renewing its stale semantic revisions.
- [x] Review all 53 incident semantic relationships, execute the 14 selected
  suites and declared requirements, derive the exact 44-subject invalidation
  set, and require 51/51 final attestation and certificate equality.
- [x] Replace duplicated repository-attestation dependency coordinates with one
  exact requirement identity under source schema v5; stale requirement
  identities must not authorize current coverage.
- [x] Project the new Metadata suite-input implementation into the existing
  policy graph and record each added relationship in the still-active A1c
  migration evidence.

**Acceptance gate:** every dependency-class mutation has the exact invalidation
set; unrelated suite changes preserve all unrelated subjects; false-empty and
missing-disposition fixtures still block; all current subjects have one valid
attestation and generated certificate.

**Status:** `Accepted`

### Milestone 2: Evidence Portfolio And Revalidation

**Goal:** Remove stale historical coupling, align platform claims with their
actual proof boundaries, and accept the repaired A1c result.

**Allowed write set:**

- Plan, issue, ledger, and Milestone 2/final evidence under this plan directory.
- `docs/decisions/standards-engine-a1c.md`
- `evaluation/standards-effectiveness/suites/a1c-public-cutover.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/a1c/relationship-migration.tsv`
- `evaluation/standards-effectiveness/fixtures/policy-impact/a1c/missing-admitted-source.toml`
- `evaluation/standards-effectiveness/policy-impact-node-catalog.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.dependencies.toml`
- The eleven registered files under `evaluation/standards-effectiveness/policy-coverage/attestations/`.
- `tools/standards_verifier/standards_verifier/checks/__init__.py`
- `tools/standards_verifier/standards_verifier/checks/policy_impact_migration.py`
- `tools/standards_verifier/tests/test_policy_impact.py`
- `tools/standards_engine/tests/platform_harness.py`
- `tools/standards_engine/tests/test_platform_harness.py`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- Generated checker inventory artifacts only when mechanically changed by
  removing the retired checker source or references.

**Tasks:**

- [x] Remove the permanent whole-graph migration check and preserve the accepted
  fixture only as historical report evidence.
- [x] Retain smaller current package/removal invariants.
- [x] Remove the retired check's implementation and fixture graph nodes,
  source-owned relationships, parser registration, and shared focused tests;
  rederive the exact 51-subject coverage closure after those inputs are final.
- [x] Run real-facade Linux transfer/concurrency evidence and focused
  transaction/lifecycle tests under their correct claim kinds.
- [x] Decide whether exact closed-store byte hashing has distinct transport
  value; retain it with a lifecycle statement or remove it.
- [x] Run complete verification and publish corrective acceptance evidence.

**Acceptance gate:** A1CR-A1 through A1CR-A8 are satisfied, every issue is
resolved or explicitly deferred outside the product claim, and the complete
repository checkpoint and diff hygiene pass.

**Status:** `Accepted`

## Blockers

- `none`

## Re-Plan Triggers

- Dependency-local coverage cannot preserve false-empty or missing-consumer
  blocking without reintroducing global per-subject invalidation.
- The neutral suite-input value requires Verifier check semantics or reverses
  the existing Analysis-to-Verifier dependency direction.
- Persisted A1c state has a real external compatibility consumer requiring a
  migration reader rather than typed unsupported behavior.
- A public contract or handle representation must change.
- A required repair changes a file outside the milestone write set in a way
  that changes ownership, contract, risk, or acceptance scope.
- Removing the migration checker leaves another current claim without deciding
  evidence.
- Real Linux behavior contradicts the proposed platform-claim split.
- Cumulative machinery increases beyond the accepted A1c composition instead
  of consolidating or deleting it.

## Concurrent Work

Not applicable. Work is serial and shared authority changes remain with one
integration owner.

## Repository Isolation

No additional branch or worktree is required. The current `main` worktree is
clean, work is serial, and no outstanding proposal can become stale. Commit
boundaries follow coherent outcomes rather than plan lifecycle transitions.

## Final Acceptance

- Acceptance status: `satisfied`
- Deferred follow-ups: Windows and macOS remain unsupported until real evidence;
  cross-engine migration remains deferred until a published compatibility
  promise exists.
- Final status: `Accepted`
