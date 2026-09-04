# Plan: Contract Authority Scope

**Plan status:** `Accepted`

**Current phase:** Milestone 0 accepted

**Next slice:** `none`

**Acceptance status:** `satisfied`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Make the general standards reject accidental concentration of independently
changing responsibilities and versions in one canonical contract artifact,
without prescribing a project-specific schema decomposition.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Architecture requires an explicit authority-scope decision before one artifact or module becomes canonical for several concerns. | `contract` | `not-applicable` | `automated-and-review` | `satisfied` | Architecture policy and authority-scope fixture |
| A2 | Contracts distinguishes declaration authority from executable or domain-semantic authority. | `contract` | `not-applicable` | `automated-and-review` | `satisfied` | Declaration-authority fixture |
| A3 | Contract versions follow coherent compatibility promises and material invalidation, not file, build, or release co-location. | `contract` | `not-applicable` | `automated-and-review` | `satisfied` | Version-scope fixture |
| A4 | Every direct semantic consumer is reviewed and applicable relationships are represented in the policy-impact graph. | `integration` | `not-applicable` | `automated-and-review` | `satisfied` | [Impact review](reports/authority-scope-impact-review.md) and 61-node/251-edge compiled graph |
| A5 | The complete standards checkpoint passes with current exact policy-coverage attestations. | `system` | `local-repository` | `automated` | `satisfied` | 225 declarative suites, 53 retained checkers, and 44 exact coverage certificates passed |

## Scope

### In Scope

- General Architecture and Contracts rules for canonical authority admission,
  semantic ownership, version scope, and invalidation.
- The Generated Contract profile and planning/implementation prompts where they
  project those general decisions.
- Policy units, decision fixtures, an enforcement suite, and policy-impact and
  coverage graph authority required to make the change reviewable.
- An explicit audit of whether an existing rule should be modified or removed.

### Out Of Scope

- A repository-specific replacement for the standards-engine A1 schema.
- Selecting a universal number of schemas, modules, layers, or version fields.
- Requiring separate artifacts for concerns that share one owner, lifecycle,
  invariant set, and compatibility promise.

## Constraints And Assumptions

### Constraints

- Rules remain technology-, language-, framework-, and repository-agnostic.
- Existing concern-boundary and cross-language version guidance remains valid;
  this change must close their admission and generality gaps without creating a
  competing authority.
- Decision fixtures must include coherent aggregation as well as invalid,
  unavailable, and split-authority outcomes.
- Policy-impact declarations contain only direct semantic consumers.

### Assumptions

- Architecture owns responsibility placement; Contracts owns representation,
  semantic selection, compatibility, and version behavior.
- The current policy-impact and exact-coverage systems can represent the new
  units without an engine change.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Add an authority-scope admission rule to Architecture rather than a schema-specific size rule. | `topic.architecture` | Independent change-axis and ownership failure | none |
| Add declaration-versus-semantic authority and version-scope rules to Contracts. | `topic.contracts` | Contract concerns may apply without generation or another language | Cross-language-only placement for part of the version rule |
| Keep coherent multi-concern modules and coordinated versions valid when one responsibility and compatibility promise justify them. | Architecture and Contracts | Deep-module interface and deletion tests | Artifact-count heuristics |
| Extend the Generated Contract profile as a projection, not as the canonical owner of the new rules. | `profile.boundary.generated-contract` | Profile specializes Contracts | none |
| Remove no existing normative rule unless the consumer audit finds a contradiction or obsolete authority. | This plan | Existing concern separation and cross-language guidance are directionally correct | none |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| Authority admission | concern/owner/lifecycle changes | declarative decision fixture | Architecture prose review | unresolved owner or change facts | typed unavailable or split authority |
| Semantic ownership | declaration versus executable/domain meaning | declarative decision fixture | Contracts prose review | missing semantic owner | typed unavailable |
| Version scope | compatibility promise and identity invalidation | declarative decision fixture | Contracts prose review | unknown promise/effect | separate versions or typed unavailable |
| Graph completeness | direct consumer relationships | policy-impact compiler and exact query | reviewed disposition report | undeclared catalog node | graph validation failure |

## Systemic Finding Audit

- Invariant family: canonical artifacts must not acquire unrelated authority or
  version coupling merely because they can serialize it.
- Sibling producers and consumers: architecture decisions, contract authors,
  generated-contract boundaries, planning prompts, generators, validators,
  identities, persistence, and public consumers.
- Authority and projection inventory: Architecture and Contracts own policy;
  the generated-contract profile and prompts project it; suites and fixtures
  enforce it; the policy-impact and coverage graphs record affected consumers.
- Consumer dispositions: recorded in the impact-review report before coverage
  attestation renewal.
- Scope or sequencing replacement: standards and evidence freeze before exact
  coverage is re-attested.

## Simplicity And Ownership Review

- Independent concepts: declaration shape, executable interpretation, domain
  policy, identity, persistence, authorization, projection, and evolution.
- Intentional coupling: concepts sharing one owner, lifecycle, invariant set,
  and compatibility promise may remain behind one interface.
- Accidental coupling risk: an umbrella schema/version invalidating or forcing
  coordinated changes across unrelated concerns.
- Policy/state/lifecycle owners: Architecture places responsibility; Contracts
  owns representation and compatibility; each selected domain retains its
  executable semantics and state lifecycle.
- Future changes that should remain independent: transport representation,
  identity semantics, authorization policy, state transitions, and persistence
  layout unless an explicit shared promise proves otherwise.

## Milestones

### Milestone 0: General Policy And Evidence

**Goal:** Add, connect, and verify the smallest general standards correction.

**Allowed write set:**

- `topics/architecture.md`
- `topics/contracts.md`
- `profiles/boundaries/generated-contract.md`
- `prompts/planning.md`
- `prompts/implement-plan.md`
- `templates/PLAN-TEMPLATE.md`
- `evaluation/standards-effectiveness/policy-units/`
- `evaluation/standards-effectiveness/fixtures/architecture/`
- `evaluation/standards-effectiveness/fixtures/contracts/`
- `evaluation/standards-effectiveness/suites/`
- `evaluation/standards-effectiveness/suite-registry.toml`
- `evaluation/standards-effectiveness/policy-impact/`
- `evaluation/standards-effectiveness/policy-impact-node-catalog.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/`
- This plan directory.

**Tasks:**

- [x] Complete the existing-policy and direct-consumer audit.
- [x] Add general authority-scope, semantic-owner, and version-scope rules.
- [x] Add positive and negative decision fixtures and suite checks.
- [x] Connect every applicable direct consumer in the policy-impact graph.
- [x] Renew exact coverage against the frozen final authority.
- [x] Run focused and complete verification and commit the accepted change.

**Acceptance gate:**

- All five objective claims are satisfied, the policy-impact query matches the
  reviewed disposition inventory, and the complete checkpoint passes.

**Status:** `Accepted`

## Blockers

- `none`

## Re-Plan Triggers

- The audit finds an existing canonical rule that already enforces all three
  decisions with tested projections.
- Policy-impact compilation exposes an unreviewed direct consumer or authority
  cycle.
- A fixture cannot distinguish coherent aggregation from accidental coupling.

## Final Acceptance

- Acceptance status: `satisfied`
- Deferred follow-ups: `none`
- Final status: `Accepted`
