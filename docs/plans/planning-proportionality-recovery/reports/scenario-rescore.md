# Planning Recovery Scenario Rescore

## Scope

This review applies the unchanged rubric in
[the evaluation README](../../../../evaluation/standards-effectiveness/README.md#scoring)
to the unchanged seven
[scenario fixtures](../../../../evaluation/standards-effectiveness/fixtures/scenarios.md).
It compares current canonical guidance with the frozen
[baseline scores](../../../../evaluation/standards-effectiveness/baseline-scores.md).
The review changes no fixture, scoring dimension, or baseline authority.

## Scores

| Scenario | A | O | W | C | V | L | R | P | E | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| S1 small fix | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 18/18 |
| S2 desktop workflow | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 17/18 |
| S3 durable worker | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 17/18 |
| S4 Rust FFI | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 18/18 |
| S5 persisted break | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 18/18 |
| S6 dependency release | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 17/18 |
| S7 hardware capability | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 17/18 |

**Aggregate:** 122/126 (96.8%), compared with the frozen 43/126 (34.1%)
baseline. Every scenario and every dimension improves or preserves its baseline
score.

## Dimension Evidence

- **Applicability:** Core and the
  [Router](../../../../STANDARDS-ROUTER.md) prohibit whole-library loading,
  select modules from observable conditions, follow explicit dependencies, and
  return unresolved routing instead of guessing. S1 has one exact positive and
  exclusion route. Rust FFI and persisted-schema conditions have explicit
  language, boundary, workflow, and topic routes.
- **Objective fidelity:**
  [Planning](../../../../workflows/planning.md#acceptance-claims) binds plan
  status to observable acceptance claims, and
  [Verification](../../../../workflows/verification.md) separates evidence
  kind, required environment, and execution mode.
- **Ownership:** Canonical module metadata names one owner and the Router
  separates workflow, profile, boundary, language, and topic responsibilities.
  Frontend and bridge projections cannot acquire backend business-policy
  ownership.
- **Complection control:** Policy, profiles, non-normative reference material,
  active state, execution history, findings, and durable decisions have
  separate owners. Active plans no longer retain accepted execution narrative.
- **Verification fidelity:** User-visible, durable, cross-boundary, release,
  and required-real-environment claims name evidence at the boundary that owns
  the behavior. Simulated or smoke evidence cannot satisfy a stronger claim.
- **Current-state legibility:** Planning defines current lifecycle, acceptance,
  blocker, milestone, and exactly-one-next-slice projections; ledgers own dated
  history.
- **Re-plan containment:** Planning requires a named trigger, replacement of
  the binding decision, supersession of the old direction, downstream gate
  updates, and no fallback preservation.
- **Process proportionality:** A bounded local change may use an inline
  checklist, conditional profiles apply only from observable facts, and
  verification scope follows the affected claim and risk.
- **Contract evolution:**
  [Contracts](../../../../topics/contracts.md) derives compatibility,
  migration, unsupported outcomes, and fallback decisions from real consumer
  and persistence authority rather than universal append-only behavior.

## Applicability Gaps

Four fixtures retain a score of `1` for applicability:

| Scenario | Expected role not explicitly routable | Current safe behavior |
| --- | --- | --- |
| S2 | Desktop application profile | Frontend, IPC, Architecture, Accessibility, and Security own the relevant generic contracts; no desktop specialization is guessed. |
| S3 | Service/worker application profile | Persistence, IPC, Concurrency, Resilience, Diagnostics, Security, Architecture, Planning, and Verification own the generic contracts; no worker specialization is guessed. |
| S6 | General shipped-application profile | Dependencies, Release, Security, Build, Tooling, and Verification are routable, but no general application profile owns application-specific specialization. |
| S7 | Hardware topic or application specialization | Verification represents `required-real` hardware evidence and typed unavailable outcomes, but the Router has no canonical hardware owner. |

These are missing optional canonical specializations, not authorization to use
legacy guidance, infer a nearby profile, or create empty placeholders. The
accepted information architecture explicitly prohibits placeholder modules.
Parent Milestone 8 must decide each role from downstream evidence: create a
bounded owner when real specialization is required, or revise the expected role
with recorded evidence when generic owners are sufficient.

## Recovery Result

The planning recovery satisfies scenario rescoring without changing its
objective or introducing transition tooling. The remaining applicability gaps
do not block an ordinary-plan pilot, but they must remain visible to the parent
final-evaluation milestone.
