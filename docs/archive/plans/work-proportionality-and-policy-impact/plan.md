# Plan: Work Proportionality And Policy Impact Recovery

**Plan status:** `Accepted`

**Current phase:** Recovery accepted

**Next slice:** `none`

**Acceptance status:** `satisfied`

**Accepted base:** `5222c1d7cd6d623854114af26f612b4606a8369c`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Make implementation slicing proportional to coherent risk and acceptance, and
give normative policy changes an explicit reviewed impact relation so affected
consumers and projections are updated without inference from links or text.

## Objective Acceptance

| ID | Observable criterion | Status | Evidence |
| --- | --- | --- | --- |
| A1 | A permanent typed relation answers which semantic consumers and projections require review when an audited policy owner changes. | `satisfied` | [Planning impact foundation](reports/planning-impact-foundation.md) |
| A2 | Reverse impact for `workflow.planning` returns every required consumer, and each returned consumer has one exact recovery disposition. | `satisfied` | [Exact consumer dispositions](reports/planning-consumer-dispositions.tsv) |
| A3 | Bounded coherent changes may proceed as one slice without a written plan, while materially sequenced or independently acceptable work still selects planning. | `satisfied` | [Proportionality evidence](reports/work-slice-proportionality.md) |
| A4 | Ordinary written-plan implementation consumes no concurrent-only revision or reconciliation records. | `satisfied` | `planning-admission` and `plan-implementation-entrypoint` suites |
| A5 | Concurrent stale-proposal protections remain conditionally routed and accepted verification passes without weakening ownership or no-fallback contracts. | `satisfied` | Final mixed checkpoint recorded in the ledger |

## Scope

### In Scope

- A permanent repository-owned semantic consumer/impact manifest, bounded
  coverage authority, validation, and deterministic reverse-impact query.
- Planning-owned impact coverage and exact change-specific consumer review.
- Work-slice, written-plan, plan-operation, plan/ledger update, prompt,
  template, Router, fixture, and suite corrections returned by the impact
  query.
- Focused, declarative, Python-unit, generated-evidence, mixed-checkpoint, and
  staged-scope acceptance.

### Out Of Scope

- M6-I17 or any other verifier-package migration.
- Changes to the temporary Bash checker graph or its frozen schema.
- Semantic-edge inference from hyperlinks, lexical similarity, or standards
  `Requires`.
- A generalized graph database, scheduler, change database, or append-only
  impact ledger.
- Global impact-coverage claims before every normative owner is audited.

## Constraints And Assumptions

### Constraints

- One serial integration owner controls active plans, Router, canonical
  workflows, shared verifier code, suite registry, manifests, generated
  artifacts, and acceptance state.
- The Milestone 2 accepted base is fixed at
  `5222c1d7cd6d623854114af26f612b4606a8369c`; an intervening shared-authority
  change makes the proposal stale and requires fresh admission.
- The impact manifest stores reviewed current policy structure. Recovery-only
  dispositions and execution evidence belong in this directory's reports and
  ledger.
- Initial coverage is explicitly bounded to owners audited by this recovery.
  A previously uncovered owner must be audited before its next normative
  change.
- Relation types are limited to normative consumer, Router projection, prompt
  projection, template projection, fixture projection, and enforcement-suite
  projection.
- Existing declarative mechanics are preferred. New Python is permitted only
  for strict semantic-edge validation or deterministic querying that existing
  checks cannot express clearly.
- Replaced policy is removed in the accepting slice; no compatibility
  representation, dual authority, or fallback remains.
- Use the fewest coherent commits that preserve Milestone 1 as an accepted
  dependency of Milestone 2. Commit cadence does not create plan or ledger
  edits by itself.

### Assumptions

- Canonical metadata and the suite registry can resolve reviewed owner and
  evidence-owner identities without duplicating ownership in the manifest.
- Existing declarative checks can own most schema and projection evidence; a
  bounded Python query/validator may own only the semantic relation behavior
  they cannot express clearly.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Accept semantic-impact authority before changing proportionality policy. | This recovery | The second milestone must consume the accepted query. | Direct consumer discovery by links or lexical search |
| Keep initial impact coverage explicitly bounded to audited owners. | Planning policy projection | Global owner audit is outside this recovery. | Implied global completeness |
| Keep concurrent revision and reconciliation decisions conditional on profile applicability. | Concurrent Plan Integration profile | Existing accepted applicability contract | Unconditional implementation consumption |
| Treat coherent behavior, risk, dependency, and acceptance as slice boundaries. | `workflow.planning` | Recovery objective | File-count and commit-cadence slicing |

## Milestones

### Milestone 1: Semantic Consumer/Impact Foundation

**Goal:** accept the smallest permanent reviewed relation that identifies the
semantic consumers and projections requiring review when `workflow.planning`
changes.

**Allowed write set:**

- this plan directory;
- the permanent semantic-impact manifest and bounded coverage authority;
- focused Python verifier/query mechanics and unit tests if required;
- focused semantic-impact fixtures and registered suite;
- suite registry, generated evidence, and verifier documentation affected by
  the accepted mechanics; and
- the two parent active plans for current dependency state only.

**Required result:**

- each edge records canonical owner, consumer artifact, relation type,
  applicability condition, and verification/evidence owner;
- duplicate edges, unknown owners or consumers, missing applicability,
  malformed relations, path escape, and missing files are rejected;
- reverse impact for `workflow.planning` deterministically returns its
  implementation workflow, Router, planning and implementation prompts, plan
  template, planning/concurrent fixtures, and planning-admission,
  concurrent-profile, implementation-entrypoint, and affected template suites;
- bounded coverage is explicit and no global completeness is claimed; and
- the temporary checker graph is unchanged.

**Acceptance gate:** focused mechanics and negative fixtures pass; the reverse
query returns the required set; all Python tests and registered declarative
suites pass; generated evidence is current; affected plan-structure and link
checks pass; the mixed checkpoint passes; and staged scope is exact.

**Status:** `Accepted`

### Milestone 2: Work-Slice Proportionality And Residual Correction

**Goal:** use the accepted impact relation to correct slice proportionality,
written-plan routing, plan-operation language, artifact-update cadence, and the
residual unconditional concurrent-protocol consumer.

**Allowed write set:**

- every Planning consumer returned by the accepted impact query and recorded
  in the exact recovery disposition report;
- focused decision fixtures and their owning suites;
- generated evidence affected by those reviewed files; and
- this recovery plan, the two parent active plans, and their ledgers only when
  current authority or accepted-slice state changes.

**Required result:**

- one coherent implementation unit remains one slice unless separation
  materially improves independent acceptance, risk containment, dependency
  ordering, conflict isolation, rollback, or feedback;
- bounded local work may state an exact write set inline and takes precedence
  over boundary-based written-plan triggers;
- file, layer, line, or commit count does not determine slice count;
- directly discovering another affected file triggers re-planning only when it
  changes objective, ownership, contract, risk, or acceptance scope;
- generic written-plan implementation consumes Planning path, operation,
  lifecycle, current-authority, and acceptance decisions only;
- revision, stale-state, compatibility, and reconciliation records remain
  conditional on the Concurrent Plan Integration profile;
- plan and ledger edits occur for authority, state, accepted boundaries,
  material deviations, or verification evidence, not mechanically per commit;
  and
- all seven required proportionality and concurrency scenarios have behavioral
  decision evidence.

**Acceptance gate:** every queried consumer has exactly one `updated`,
`reviewed-no-change`, or `not-applicable` disposition with evidence; all
required focused suites, plan checks, links, generated freshness, Python tests,
registered suites, mixed checkpoint, diff checks, and staged review pass; the
residual contradiction is absent; both parent plans resume at a fresh
post-recovery graph audit without preselecting M6-I17.

**Status:** `Accepted`

## Blockers

- `none`

## Re-Plan Triggers

- The accepted base or shared authority changes before integration.
- Existing declarative capabilities cannot express the relation without a
  policy-specific engine branch or inferred edge.
- The required Planning consumer set cannot be represented with one canonical
  owner and one explicit evidence owner per edge.
- Milestone 2 requires an unqueried semantic consumer or changes the objective,
  ownership, contract, risk, or acceptance scope.
- Acceptance would require changing the temporary checker graph, weakening a
  concurrent stale-state protection, retaining old policy, or admitting
  M6-I17.

## Concurrent Work

This recovery is serial shared-authority work. Read-only investigation may be
delegated, but all writes and acceptance remain with one integration owner.

## Final Acceptance

- Acceptance status: `satisfied`
- Deferred follow-ups: unaudited normative owners require impact audit before
  their next normative change.
- Final status: `Accepted`
