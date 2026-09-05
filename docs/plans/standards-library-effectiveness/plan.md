# Plan: Standards Library Effectiveness Restructure

**Plan status:** `Active`

**Current phase:** Milestone 8 admission and planning

**Next slice:** select two bounded independent downstream pilots and admit the
scenario comparison, migration guidance, and final concision review. Milestone 7
is accepted in the [source closure report](reports/milestone-7-source-closure.md).

**Acceptance status:** `partial`

**Composed-design review:** `applicable`; the
[navigation authoring admission](reports/milestone-7-navigation-authoring-admission.md#composed-design-review)
records the eight artifact probes for the Engine extension. Implementation,
source application, and Milestone 7 verification are complete.

**Execution ledger:** [Milestone execution ledger](execution-ledger.md)

**Issues:** [Standards effectiveness findings](issues.md)

This file owns current objective, decisions, milestone state, blockers, and the
next authorized slice. Detailed execution history belongs in the linked ledger
and reports. Migration lifecycle belongs in canonical package, disposition,
owner, and generated-evidence records.

## Objective

Make the Coding Standards repository objectively more effective as reusable
guidance for unrelated downstream repositories. The revised library must:

- produce higher-quality plans and implementation procedures;
- route tasks to the smallest sufficient standards set;
- distinguish mandatory rules, recommendations, profiles, and reference;
- give each normative rule one canonical owner;
- preserve objective-level acceptance through planning and implementation;
- separate active plan state from execution history;
- make compatibility, fallback, documentation, and process obligations
  proportional to real contracts and risks; and
- remain stack-agnostic at the root, with explicit profiles for specialized
  guidance.

Pantograph remains one regression case, not the design target or a source of
universal architecture policy.

## Objective Acceptance

| ID | Observable criterion | Status | Evidence |
| --- | --- | --- | --- |
| A1 | Fixed scenarios improve or preserve every critical rubric dimension. | `satisfied` | [Baseline scores](../../../evaluation/standards-effectiveness/baseline-scores.md) and [current rescore](../../archive/plans/planning-proportionality-recovery/reports/scenario-rescore.md) |
| A2 | Routing, ownership, duplication, disposition, and link targets pass from canonical evidence. | `satisfied` | [Accepted source closure](reports/milestone-7-source-closure.md), with separate current-source and historical reconciliation evidence |
| A3 | Two independent downstream pilots complete without loading the full library. | `pending` | Milestone 8 |
| A4 | Migration and standards-version guidance is published. | `pending` | Milestone 8 |
| A5 | Final manual review confirms the library is stack-agnostic, routed, concise, and free of competing normative owners. | `pending` | Milestone 8 |

## Scope And Constraints

### In Scope

- Library information architecture and task routing.
- Normative level, applicability, ownership, and precedence metadata.
- Planning, implementation, verification, re-planning, and release workflows.
- Active-plan, ledger, issue, report, and ADR ownership.
- Typed acceptance for focused through user-visible and release checks.
- Contract evolution, compatibility, fallback, and degraded-mode policy.
- Proportional documentation and commit obligations.
- Normative deduplication, reference extraction, versioning, and adoption.
- Repeatable before-and-after evaluation.

### Out Of Scope

- Retrofitting downstream repositories.
- Encoding one product's architecture as generic policy.
- Removing safety, security, accessibility, interop, or concurrency semantics
  solely to reduce document size.
- Building a documentation site unless repository navigation proves
  insufficient.

### Constraints

- Root guidance owns cross-language principles; profiles own specializations.
- Each retained mandatory rule has one canonical owner and observable reason.
- Every removed or moved rule has a recorded
  `keep/refine/merge/move/remove` disposition.
- Old entrypoints may route readers only when they do not compete as normative
  owners.
- Automation enforces deterministic structure and evidence, not subjective
  architecture.
- Shared contracts and authority files integrate serially.
- Work proceeds in verified atomic slices without compatibility or fallback
  preservation of replaced standards and verification methods.

## Binding Decisions

| Decision | Binding direction |
| --- | --- |
| Progressive disclosure | Route from Core through one workflow and only applicable profiles and topics. |
| Normative ownership | Every retained rule has one canonical owner; indexes link without restating rules. |
| Planning artifacts | Active plans own current state; ledgers and reports own history; ADRs own durable architectural decisions. |
| Specialization | Root guidance stays stack-agnostic; language and application details belong in profiles. |
| Reference material | Examples, recipes, and tool versions are non-normative unless explicitly promoted. |
| Acceptance model | Required evidence is a set of typed claims; proof kind, environment, and execution mode are independent dimensions. |
| Migration lifecycle | Canonical package, disposition, owner, and generated records own status; active-plan narration does not. |
| Verification migration | Bash checkers and helpers are removed with accepted Python-engine replacements; no wrappers, dual authority, compatibility parsers, or fallback remain. |
| Accelerated execution | Select proportional `serial-coherent`, `pre-admitted`, `owner-wave`, or `shared-contract` migration modes from current risk and concurrency facts. Owner-coherent packages may prepare concurrently with disjoint write sets; shared registry, evidence, Router, and plan integration remain serial. |
| Recovery dependency | The historical Git reachability recovery and the reopened cleanup plan are accepted. Obtain fresh graph evidence before selecting another verifier package rather than reusing post-M6-I52 selection facts. |
| Current efficiency recovery | The accepted efficiency recovery stabilizes temporary component identities and applies proportional serial/wave migration modes. Historical cleanup is accepted only after explicit reachability reconciliation; normal remote backup is accepted and pilots remain separately owned. |

## Current Architecture

```text
CORE-STANDARDS.md
  + one workflow
  + applicable application, boundary, and language profiles
  + affected topic modules
```

Canonical modules declare purpose, level, applicability and exclusions,
prerequisites, specialization, verification, and owner. Readers do not infer
precedence from scattered prose.

The active artifact boundary is:

```text
plan.md              current objective, decisions, milestones, blockers, next slice
execution-ledger.md  accepted execution and verification history
issues.md            findings and dispositions
reports/             detailed investigations and evidence
ADRs                 durable architecture decisions
```

Lifecycle states are `Planned`, `Active`, `Blocked`, `Implemented`,
`Verifying`, `Accepted`, `Deferred`, and `Superseded`. `Implemented` is not
complete; `Accepted` requires the named evidence.

## Milestones

| Milestone | Outcome | Status | Current evidence or next work |
| --- | --- | --- | --- |
| 0 | Baseline and fixed scenarios | `Accepted` | [Baseline report](../../../evaluation/standards-effectiveness/baseline-report.md), [scenario fixtures](../../../evaluation/standards-effectiveness/fixtures/scenarios.md) |
| 1 | Architecture, metadata, routing, and ownership | `Accepted` | [Owner map](../../../evaluation/standards-effectiveness/owner-map.tsv), [generated owner map](../../../evaluation/standards-effectiveness/generated/rule-owner-map.tsv) |
| 2 | Core and Router vertical slice | `Accepted` | [Core](../../../CORE-STANDARDS.md), [Router](../../../STANDARDS-ROUTER.md) |
| 3 | Planning and implementation lifecycle | `Accepted` | [Planning](../../../workflows/planning.md), [Implementation](../../../workflows/implementation.md) |
| 4 | Typed verification and release acceptance | `Accepted` | [Verification](../../../workflows/verification.md), [Release](../../../workflows/release.md) |
| 5 | Contracts, compatibility, and fallbacks | `Accepted` | [Contracts](../../../topics/contracts.md) |
| 6 | Proportional documentation and commit process | `Accepted` | [Documentation](../../../workflows/documentation.md), [Commit](../../../workflows/commit.md) |
| 7 | Role-based consolidation and verification migration | `Accepted` | [Source closure](reports/milestone-7-source-closure.md): 27 entrypoints reviewed, ten corrected through the Engine |
| 8 | Scenario rescore, pilots, migration publication, and final review | `Planned` | Ready for bounded admission; pilots and final review remain unexecuted |

### Milestone 7 Current State

**Status:** `Accepted`. The [source closure report](reports/milestone-7-source-closure.md)
binds acceptance to Engine publications `67d3e205` and `ff6f3b21` and the
D001–D010 [semantic ownership review](reports/milestone-7-semantic-ownership-review.md).
Ten legacy indexes were corrected; seventeen retain their reviewed bytes.
All 70 canonical modules remain unchanged. The final population audit resolves
197 local inline links and 21 heading fragments across all 27 entrypoints.

**Authority and verification:** M7-OWN-01 through M7-OWN-05 and M7-OWN-07 are
resolved. All 916 historical identifiers are reconciled separately from current
canonical membership and 54 canonical Router rules. Frozen evidence is preserved.
The Engine checkpoint passes 73 suites and 121 structural checks; it does not
certify prose conformance or downstream effectiveness. M7-OWN-06 remains in
Milestone 8's A5 concision review.

**Accepted migration boundary:** verification migration remains accepted through
M6-Z1: the complete command is Python-only, with no Bash verifier, helper,
launcher, or temporary migration model. Earlier `7.4c3` source-closure claims
are historical evidence superseded by the current review and final closure.

**Accepted recovery boundary:** M6-I16 is accepted after one-owner final-state
proof. The [work proportionality and policy impact recovery](../../archive/plans/work-proportionality-and-policy-impact/plan.md)
and [generic edge-system recovery](../../archive/plans/generic-edge-system/plan.md)
are accepted. Fresh post-recovery evidence selected M6-I17 and fresh
post-M6-I17 evidence selected M6-I18; no stale package evidence was reused.

**Remaining work:** Milestone 8 scenario comparison, two independent downstream
pilots, migration and standards-version guidance, and final manual review.
A2 is satisfied at the reviewed source boundary; A3, A4, and A5 remain pending.
Incomplete declared relationship mappings are explicit and are not interpreted
as proof of complete semantic consumer coverage.

## Simplicity And Ownership Review

**Applicability:** `applicable`

- Independent concepts and dimensions: routing, normative ownership,
  verification migration, downstream pilots, and publication remain separate
  milestones with distinct acceptance evidence.
- State, identity, value, time, policy, and mechanism: canonical rule identity
  and policy values stay in standards-owned records; package timing and
  mechanism migration stay in lifecycle manifests and the engine plan.
- Caller and composition-root knowledge: the Router composes the smallest
  applicable standards set, while the verification engine composes registered
  suites without moving policy into orchestration.
- Representative change paths and forced owners: a checker migration changes
  its owner-coherent suite, exact lifecycle records, and generated evidence
  without forcing unrelated normative modules to change.
- Stable Interfaces versus hidden knowledge: metadata, routing, dispositions,
  and suite contracts expose typed authority rather than relying on headings,
  filenames, or scattered plan narration.
- Independent evolution, testing, failure, and replacement: standards owners,
  reference material, migration packages, declarative checks, and pilots carry
  separate evidence and can fail without inheriting each other's authority.
- Necessary complexity and containment: temporary Bash graph evidence and
  mixed execution were contained to the verification migration and removed at
  the accepted zero-Bash boundary.
- Deletion and cumulative machinery result: each accepted slice deleted its
  replaced Bash authority, and the remaining migration machinery disappeared
  at zero-Bash closure rather than becoming permanent infrastructure.

## Evidence Index

| Authority | Canonical artifact |
| --- | --- |
| Detailed accepted execution history | [Execution ledger](execution-ledger.md) |
| Findings and resolutions | [Findings](issues.md) |
| Rule ownership | [Owner map](../../../evaluation/standards-effectiveness/owner-map.tsv) and [generated owner map](../../../evaluation/standards-effectiveness/generated/rule-owner-map.tsv) |
| Rule dispositions | [Consolidation dispositions](../../../evaluation/standards-effectiveness/consolidation-dispositions.tsv) |
| Milestone 7 decomposition | [Execution decomposition](../../../evaluation/standards-effectiveness/milestone-7-execution-decomposition.tsv) |
| Verification migration lifecycle | [Verification-engine plan](../../archive/plans/standards-verification-engine/plan.md), [ledger](../../archive/plans/standards-verification-engine/execution-ledger.md), and [M6-Z1 closure](../../archive/plans/standards-verification-engine/reports/m6-z1-zero-bash-closure.md) |
| Migration-Python terminal lifecycle | [Recovery plan](../../archive/plans/python-verification-engine-recovery/plan.md) and [ledger](../../archive/plans/python-verification-engine-recovery/execution-ledger.md) |
| Current recovery state | [Generic edge-system recovery](../../archive/plans/generic-edge-system/plan.md) and [ledger](../../archive/plans/generic-edge-system/execution-ledger.md) |
| Accepted engine recovery | [Python verification engine design recovery](../../archive/plans/python-verification-engine-recovery/plan.md) |

## Blockers

- `none`

## Slice Procedure

1. Confirm a clean repository and name one behavior plus exact write set.
2. Identify affected owners, identifiers, dispositions, and no-fallback impact.
3. Implement one coherent unit with focused evidence; split only when
   separation materially improves acceptance, risk, dependency, conflict,
   rollback, or feedback.
4. Run risk-proportionate checks and any required shared checkpoint.
5. Update current plan state and put execution detail in the ledger.
6. Review the staged write set and create one atomic conventional commit.

If history obscures current authority, move it to its canonical ledger or
report before continuing.

## Re-Plan Triggers

| Trigger | Required response |
| --- | --- |
| Safety or correctness semantics would be dropped | Stop, restore traceability, and revise the disposition. |
| Ordinary routing needs most of the library | Rework roles or routing before migration. |
| A rule cannot map to one owner | Resolve ownership before moving it. |
| Stable links require duplicate normative owners | Use a routing index or versioned migration, not duplication. |
| A shared taxonomy or authority contract must change outside the slice | Stop and admit a serial contract slice. |
| A checker migration needs a wrapper, retained Bash execution, compatibility parser, inferred owner, false dependency, or fallback | Stop and re-plan a canonical Python-engine replacement. |
| Active-plan compaction would remove evidence without canonical ledger, report, package, disposition, or lifecycle ownership | Stop and migrate that authority before deleting prose. |
| Pilot evidence invalidates sequence or targets | Record the evidence and revise milestones before continuing. |

## Final Acceptance

- **Objective evidence:** Pending Milestone 8 scenario
  comparison, two downstream pilots, migration publication, and manual review.
- **Deferred follow-ups:** None beyond milestones explicitly marked `Planned`.
- **Final status:** `Active`
