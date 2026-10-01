# Authoring experience — source review and planning evidence

## Disposition

The current code supports four reported friction mechanisms. The most important
changes concern the publication result and evidence preparation/resolution, not
removing integrity checks. A changed-evidence rejection is correct; the incomplete
readiness explanation and late discovery are the problems. Git ref publication is
also correct within its current contract; it intentionally leaves the index and
worktree untouched. The interface does not make that distinction sufficiently useful
for the agent's next operation.

This is a new source review and a planning delivery. It is not an independent external
acceptance review of earlier code authored in this conversation, a production repair,
or a status change for existing plans. The attached historical external report is
historical evidence with its own source/CI limits; it is not substituted for current
source or used to reopen accepted slices.

## Source and method

- Candidate: `149ba317e9397519bc181a048ecf76aef129a69c`.
- Tree: `fdd40edc1eea85398e97b740a595a42631614d0b`; interface 45.
- Runtime source has no `tools/` change from parent `39d55dc3`; the latest commit
  publishes Security/Concurrency guidance, metadata and coverage. The review does
  not infer that this is the exact original feedback session: its handles and
  transcript were not supplied.
- Exact Actions artifact `11036434347`, from run `36574954850`, verified against
  SHA-256 `34d36acefcb3b9c4be1bf096797bbd3c111f893f2c8bb2ca8c0e2d00be802f0f`.
- Scope: publication/recovery/receipt path, local evidence authorization and portable
  coverage, focused workflow reuse, application preview, related contracts and tests,
  current governing standards and baseline CI. This is not a whole-repository audit.
- Read-only source checkout; probes create and operate only on task-owned disposable
  repositories/stores. No user checkout, retained production state, remote branch,
  acceptance record or provider configuration changed.

## F1 — Applied target, unresolved checkout (confirmed)

`publish_candidate` imports verified objects and performs an expected-old
`update-ref` on `refs/heads/main`. It deliberately does not replace the user's index
or worktree. The ordinary `apply-proposal-result` returns an application handle and
`status: applied`; the focused workflow adds its usual context but no commit/ref/
index/worktree observation. A later applied `workflow_status` likewise does not
expose the selected publication's material receipt and current checkout condition.

**Probe:** a real facade proposed and reviewed a new reference, then published it
with both a staged and unstaged unrelated README change and an untracked file.
The real candidate verifier ran. Apply returned `applied`; main advanced; the exact
index bytes and user README bytes were preserved. Relative to the new main, Git
reported staged reversals of generated metadata and a staged deletion of the new
reference. This is the agent-visible state from the report, not an overwritten-user-
change reproduction.

Required improvement: preserve isolation, expose both outcomes, and provide only an
explicit guarded reconciliation action. Do not make apply reset the checkout. Code:
[Git publication](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/repository_git/repository_git/repository.py#L631-L692), [apply](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/standards_engine/engine.py#L1329-L1464), [workflow projection](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/standards_engine/agent_workflow.py#L105-L178).

**Feasibility:** on this private fixture `git read-tree -m -u old new` synchronized
the published paths and preserved the unrelated README's staged/unstaged distinction
and untracked file. A separate overlapping-file fixture refused with exit 128,
preserving its index, conflicting bytes and target. This validates one primitive,
not a complete Engine API, concurrent-editor exclusion or interruption recovery.
Those are explicit implementation gates in A3.

## F2 — One evidence reference is resolved against different material (confirmed)

The local facade authorizer uses `DirectoryContentSource(root)` for all
`repository-content@1` references. Decisions therefore read the working tree. Final
coverage publication separately reads those same IDs from the proposed destination
source. Its portable receipt reader later reads them from the published source.
These are three concrete material contexts; the four-field reference identifies
path/digest/provider but not which originating source the author intended.

**Probe:** an audit of `workflow.commit.commit-message` was combined with a change
to `prompts/planning.md`. The unchanged working-tree prompt served as explicit
fixture evidence. The actual resolve sequence reached complete, and review returned
ready. Both explicit `verify_proposal` with that readiness and apply returned
`ANALYSIS.EVIDENCE_DIGEST_MISMATCH`. Main and the working-tree evidence remained
unchanged. No captured evidence was fabricated or production approval submitted.

Important qualification: an existing explicit candidate verification operation
already catches the mismatch before apply. The interface's ordinary review-to-ready
path does not perform that evidence-destination preflight. The fix is not to remove
candidate checking, require blind apply retries, or claim readiness guarantees final
authority can never change. Share the deterministic evidence preparation and make
its failures visible earlier.

Code: [local resolution](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/standards_engine/tools.py#L54-L106), [portable publication](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_analysis/standards_analysis/coverage_publication.py#L124-L178),
[portable readback](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_analysis/standards_analysis/coverage_publication.py#L202-L223), [review boundary](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/standards_engine/engine.py#L1252-L1326).

The plan proposes explicit captured evidence bundles because current portable
coverage deliberately requires repository-content version 1. A broad source-label
field or simply permitting external references would not update the receipt reader's
meaning. A self-contained managed artifact can preserve the existing reference
carrier and portable resolution while retaining original baseline/candidate/imported
provenance. That is a design proposal with a required vertical proof, not an
implemented or universally validated new evidence system.

## F3 — Missing evidence diagnostic context (confirmed)

The mismatch above returned an empty `details` object: no reference, phase, path,
expected/actual digest or source identity. `ResolvedEvidence` raises a message-only
AnalysisFailure. The generic Engine adapter also projects most domain failures as
only code/outcome/message, discarding optional contextual fields that some other
owners supply. Fix the producer and the authorized projection; do not make a generic
adapter emit arbitrary raw values or private material to application clients.

Code: [digest validation](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_analysis/standards_analysis/trust.py#L70-L88), [domain rejection](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/standards_engine/engine.py#L3460-L3484).

## F4 — Existing valid reuse is not connected to focused revise (confirmed, bounded)

Focused `revise` creates/analyzes the successor without passing its selected prior
Analysis. `_analyze_proposal` starts a new state with repository coverage, not prior
session dispositions. Meanwhile native `prepare(prior_analysis=...)` already uses
`_reuse_prior`, which checks execution contract and reevaluates retained decisions.

**Probe:** one normative fixture obligation was resolved to complete. Adding an
unrelated reference through focused revise returned needs-action again. One old/new
obligation fingerprint was exactly identical. Applying the existing `_reuse_prior`
to the real successor in memory retained the one disposition and evaluation became
complete. No derived Analysis was published by this feasibility check; current
source/evidence/authorization owners still ran.

This establishes one safely reusable Analysis decision, not permission to carry
all decisions or final readiness across revisions. Final review subjects expressly
include Analysis/revision/target. The plan retains that stronger binding and exposes
why other decisions became stale.

Code: [fresh proposal Analysis](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/standards_engine/engine.py#L1183-L1248), [focused revise](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/standards_engine/agent_workflow.py#L219-L265),
[existing validated reuse](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/standards_engine/engine.py#L2456-L2496), [readiness ownership](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/standards_engine/authoring.py#L780-L848).

## F5 — Candidate exposure failure loses the blocking identity (confirmed)

The qualification traversal knows exactly which module fails current exposure,
but raises an empty `_UnqualifiedContent`. Authoring preview then emits the generic
application rejection plus a suggestion to inspect exposure elsewhere.

**Probe:** changing only a Router rule's displayed condition made Router exposure
`needs-review`. The real candidate route preview returned `APPLICATION.CONTENT_UNAVAILABLE`
with no blocker details. A separate authorized Router read returned its exposure
state. This is appropriate denial with an avoidable explanation round trip.

Return structured internal blockers and expose them only through the authorized
preview. Do not make ordinary application errors disclose private module names or
authorization state. Code: [qualification](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/standards_engine/context_projection.py#L110-L126), [preview](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/standards_engine/context_projection.py#L250-L268).

## F6 — Baseline CI fixture now assumes obsolete production exposure

Current source workflow `36574954850`, job `109428068403`, failed its Engine phase:
611 executions, two errors. Both enter
`test_supporting_workflow.test_coordinated_publication_and_provenance_only_revision`
(directly and through the process-reuse wrapper). The test indexes `empty['code']`
after reading topic.security and expecting content-unavailable. The latest
publication makes that real topic visible, so the positive result has no error code.
A separate run of the fixture setup and its initial application read reproduced
`application-read-result` without a `code` field. This is a fixture setup assumption
exposed by a standards change, not proof of an application-authorization bypass.

Repair the starting fixture to control its own exposed/unexposed module and retain
positive and negative assertions. Do not revoke real Security exposure or merely
accept either result. This repair belongs in candidate verification; the plan must
not assume baseline CI is green. The pre-Engine supporting selections all passed.
The workflow stops after Engine failure, so it did not reach its final structural
command. A separate local structural invocation passed. Code: [fixture](https://github.com/MrScripty/Coding-Standards/blob/149ba317e9397519bc181a048ecf76aef129a69c/tools/standards_engine/tests/test_supporting_workflow.py#L78-L86).

## Reported concerns not promoted to unproved defects

The exact client's abbreviated declarations, pagination effort, and response token
cost were not measured here; no live model session was run. Existing compact
summaries and selective input/output discovery already exist. The plan improves
current task examples and measures the coherent authoring workflow, but does not
restore eager embedded schemas or create short-ID resolution as an assumed cure.
The reported invalid read_many call remains a caller error; its required snapshot
belongs in the example, not removed from the authority contract.

External evidence is supported architecturally through authorization adapters, but
the inspected local adapter deliberately accepts only repository-content@1. Do not
mistake that deployed boundary for a missing generic network provider or make
outside URLs trusted by labelling them external.

## Verification and limitations

Actual local selected suites: 22 Engine authoring/recovery/digest tests passed;
125 Analysis tests passed; 40 Repository Git tests passed and one permission-
dependent case skipped. Total: **187 passed, one skipped, zero failures** across
188 test executions. Full Engine/remaining package suites were not rerun.
The complete structural checkpoint separately passed 73 suites / 121 checks.
The pinned hosted run is failed as recorded above; local selection does not replace it.

The four actual-facade scenarios and two feasibility experiments are separate from
those unit-test totals. Normal publication used the actual verifier. Existing
recovery tests use their declared verifier substitute for injected faults; this is
not represented as independent full-verifier evidence for each recovery scenario.
Two initial probe drafts failed before the relevant observation (missing fixture
condition/unhashable fingerprint), and one used a colliding fixture directory name.
The corrected probes passed; originals and their errors remain in the evidence.
A supplementary CI-fixture probe initially omitted class-level setup and was
corrected before making its observation; that setup mistake is recorded separately.
None was a production-code failure or silently counted as a successful test.

Environment: Python 3.13.5, Git 2.47.3, jsonschema 4.26.0, rpds-py 2026.5.1. No
local supported locked Python 3.12 run, no platform other than Linux, no hostile
concurrent checkout trial and no external/model reviewer were executed. The original
feedback's exact private records remain unavailable. The new plan, links and its
required fields are checked separately; validation of a plan is not acceptance of
its unimplemented claims.

## Selected implementation sequence

A1: truthful publication/checkout observations and early evidence diagnostics.
A2: explicit immutable evidence acquisition/export with preserved portable semantics.
A3: opt-in guarded checkout reconciliation with owned partial outcomes.
A4: scoped exposure explanation and existing validated Analysis reuse, with examples.
A5: exact supported integration, actual disposable agent task and independent review.

There is no source patch in this delivery. Use the canonical plan for future `start`
admission; current findings do not reopen prior accepted scopes.

## Corroborating Git contract

The official read-tree documentation specifies its two-tree carry-forward behavior,
including preservation of unrelated local changes and refusal of overlapping changes.
The observed fixture supports that bounded use; it does not establish atomicity of
Git refs, the index and arbitrary filesystem writes together.

- https://git-scm.com/docs/git-read-tree
- https://git-scm.com/docs/git-update-ref/2.45.0
