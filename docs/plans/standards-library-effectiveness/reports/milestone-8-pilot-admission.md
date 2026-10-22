# Milestone 8 downstream pilot admission

**Status:** bounded admission; pilot execution and A3–A5 acceptance pending.
**Standards source:** `39d55dc330d44ecf940364ceada9d2527f7c7ea0` until an
explicitly recorded successor is selected. This source identity identifies the
guidance available to a pilot; it does not accept the separate packaging or
test-strengthening plans.

## Decision boundary

Use two already-needed tasks in different downstream repositories. Each task gets
one recorded starting revision, intended outcome, repository constraints, and
claim-matched evaluation before work starts. Do not use an invented fixture as a
downstream pilot, load the whole library, or change the Standards Engine to make
the pilot possible. A repository with unrelated working changes needs an isolated
starting tree or an explicit inventory of those changes before its task is admitted.
The pilot agent may implement the repository task only under that repository's
own authority and workflow; this admission makes no downstream write.

The pilots assess whether selected standards help ordinary work: functional
correctness, appropriate responsibility and contracts, proportionate effort,
routing sufficiency, and accurate completion. They do not certify all possible
repositories or show a causal improvement without a comparable control.

## Required pilot record, fixed before execution

| Field | Required observation |
| --- | --- |
| Task identity | Repository, exact starting commit/tree, current dirty-state disposition, task source, owner, and bounded requested outcome. |
| Constraints | Existing project rules, affected public/persisted contracts, environment, known blockers, and actions that need separate authority. |
| Standards route | Exact standards revision; observed routing facts; selected module IDs/paths and prerequisites; unanswered facts; excluded modules; actual material read. |
| Acceptance | Functional claim and required evidence kind, environment, execution mode, plus independent review and necessary repairs. |
| Effort | Agent/model configuration, turns, routing/read calls, repeated reads, malformed calls, repair turns, and human corrections when observable. |
| Proportionality | Added abstractions, compatibility paths, documentation, process steps, and whether each was needed by a real contract or risk. |
| Result | Final revision, checks, review findings, owner disposition, remaining limits, and whether the agent finished the requested outcome. |

An independent reviewer recommends; the downstream acceptance owner records the
task decision. A successful check or favorable review does not change plan status
by itself. Where an observation is unavailable, record `unobserved` and the
reason; do not replace it with an estimate.

## Selected real tasks

The repository owner selected **Pumas-Library** and **Pantograph** as the two
different downstream repositories. The following bounded tasks are drawn from
their active records. They are admitted for task-brief preparation, not yet for
pilot execution or A3 credit; confirm each exact outcome and frozen start tree
with its repository owner at execution.

| Pilot | Existing task and source | Observed starting condition | Pilot boundary |
| --- | --- | --- | --- |
| Pumas-Library | Verify the rebuilt Linux direct-install Torch candidate through the local package, repairing only a demonstrated defect. Its `docs/plans/torch-cross-platform-runtime-management/plan.md` names this as the next slice. | `04e7f1568f00693c0ef26c77e0150e5e4dd112ea`, tree `3c7e1cafec1ccb52233f6e5513a8fe6d7bbe82b9`; branch `work/torch-version-management`; untracked `docs/breif/future.md` is outside the pilot and requires isolation. | One Linux packaged install/inspect/select/start/stop and cancellation/error evidence for the current direct-install candidate. Windows/macOS and release publication stay with their separate gates. |
| Pantograph | Qualify the existing RPC-01 producer identity/replacement and outage boundary, repairing only a demonstrated Pantograph consumer defect. Its `docs/plans/domain-architecture-and-multimodal/{plan,issues}.md` retain RPC-A03's cursor gaps, cross-instance replacement and stale-selection recovery as open. | `019caf4aa7d93ca735e78da40b2cd262e1d8c52e`, tree `adcaad060583caef938c86981f273ad7ce839582`; branch `codex/pantograph-rpc-workflow-2026-09-26`; modified and untracked root proposals are outside the pilot and require isolation. | One retained, producer-selected fixture through Pantograph's existing RPC consumer; check failure/outage/replacement behavior and no guessed identity or fallback. Real image/embedding/desktop acceptance stays separately gated. |

The two tasks are separable: Pumas's installer is not Pantograph's RPC model
consumer, and Pantograph's replacement check uses a pinned producer fixture,
not the Pumas checkout under pilot. If fresh repository facts make either task
already complete or dependent on the other, replace it with another needed,
bounded task before freezing the pilot brief; do not count a retrospective test.

## Comparison and scoring

Reuse the seven fixed [scenario fixtures](../../../../evaluation/standards-effectiveness/fixtures/scenarios.md),
their [0–2 rubric](../../../../evaluation/standards-effectiveness/verification-guide.md#scoring),
the [frozen baseline](../../../../evaluation/standards-effectiveness/baseline-scores.md),
and the [current rescore](../../../archive/plans/planning-proportionality-recovery/reports/scenario-rescore.md).
The 122/126 rescore is a guidance review, not pilot evidence. Do not rerun it just
to make a second report; revisit a dimension only if a pilot exposes a concrete
applicability or ownership gap. Keep the four recorded applicability gaps visible.

If a paired comparison is practical, hold the task brief, starting tree,
available project material, model settings, verification, and scorer constant.
Record the different standards exposure and any unavoidable differences. Score
the two outcomes independently against the same task criteria; do not infer a
universal effect from two tasks. If a fair pair would duplicate real work or
misrepresent the baseline, use one real execution with an explicit observational
limit instead.

## Separate follow-on claims

After observing both pilots, publish a short adoption/version entrypoint that
shows how a repository identifies its standards revision, begins a normal task,
routes and reads only relevant guidance, and deliberately updates. Distinguish
installing or pointing at a new standards revision from migrating that
repository's persisted data, public contracts, or accepted workflows. Link to
canonical owners rather than copying rules. A recurring, demonstrated setup
problem may justify a separate small tooling decision.

For A5, manually inspect the Core, Router, selected pilot routes, and their
linked guidance as consumed. Record concrete competing instructions, duplicated
obligations, unclear normative levels, broad routing, or process demands beyond
the task's risk. Check stack neutrality and one normative owner. Preserve safety,
concurrency, interoperability, accessibility, and correctness obligations; change
source only for a demonstrated problem through the Standards Engine workflow.

## Admission gates and endpoint

1. Reconcile packaging's exact-source CI, independent review, and acceptance-owner
   decision. Keep its first packet's disclosed evidence gaps visible.
2. Reconcile test strengthening's exact `39d55dc3` supported CI, independent
   review, and acceptance-owner decision. Its five local behavior claims remain
   separate from those gates.
3. Record both eligible real task briefs and freeze their start conditions.
4. Execute, verify, and review the two tasks; record the scenario comparison.
5. Publish adoption/version guidance; finish the A5 manual review; accept the
   broader objective only when A3–A5 have their own evidence and owner decisions.

The earlier routing-fact ergonomics plan remains Accepted. Deferred hash/equality,
float-zero, dynamic-import, or broader storage observations are not new
implementation obligations in this sequence.
