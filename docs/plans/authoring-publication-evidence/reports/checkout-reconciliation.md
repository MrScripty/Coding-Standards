# Checkout reconciliation and retained implementation

Date: 2026-10-22.

The user authorized committing retained work, discarding obsolete differences
and leaving a clean repository. The starting accepted revision was
`188beda1fa477d21d576c233dd8c7f4c4c267d23`.

## Accepted standards and checkout state

The starting checkout had 75 tracked differences and 129 untracked files. The
Git index exactly matched accepted `main`. Of the tracked differences, 51 were
older standards, prompts or metadata: 31 matched `daa70d98`, and 20 matched
`72963ad590ca`, including absence of files introduced later. Those differences
were restored to accepted `main`. The generated suite-input manifest was rebuilt
through the Engine after reconciliation.

A fresh MCP snapshot identified `188beda1` as its source revision. Exact readback
of Router, Security, Concurrency, Untrusted Execution, Planning, Discovery,
Implementation and Rust matched that commit byte for byte. Their older disk
copies were not the authority served by MCP. No normative wording, exposure
decision, policy registration or coverage certificate was changed by cleanup.

Publication constructs an isolated candidate from captured authority and declared
edits, then advances the canonical ref. Earlier checkout conflicts preserved
older files; successive publications therefore accumulated apparent reversals.
The recorded Planning and application-exposure results retain those original
conflicted observations.

## Retained implementation

Interface 47 retains the existing guarded checkout reconciliation in Repository
Git and the Engine. Successful apply and explicitly authorized publication
completion use Git's two-tree update for the exact published transition.
Unrelated work is retained; overlapping changes block reconciliation. Default
recovery remains observational. Publication stays applied if checkout recovery
is unavailable. This behavior does not overwrite accumulated older conflicts.

Private interaction recording, its SQLite owner, MCP composition, focused tests
and qualification evidence are retained. The running MCP implementation digest
matched the uncommitted workspace implementation at cleanup admission. The
earlier isolated observation campaign remains evidence for its recorded source,
not a claim that the combined Interface 47 source ran all 1,255 tests.

The old observation-era approval-reset edit in `test_supporting_workflow.py` was
discarded. A1 already supplies a test-owned unexposed standard for the negative
case. The duplicate reset committed a refreshed manifest without its overlaid
contract bytes, causing `SUITE_INPUT.STALE_FILE` during snapshot capture. Keeping
the accepted fixture restored both direct and cached workflow consumers.

## Evidence and open work

The [proposal index](../../../proposals/README.md) distinguishes applied changes,
unapplied drafts and the pending Rust coverage certificate. Requests, rejected
attempts and captured review evidence are retained with their original identities.
Committing those records does not apply a proposal or renew a certificate.

The CI-efficiency candidate's temporary checkout is no longer present at its
recorded `/tmp` location. Its retained plan and diagnostic reports describe
historical work; hosted candidate qualification and acceptance remain pending.
Existing output-delivery and downstream pilot acceptance limits are preserved.

## Validation

The initial Engine repository verification after restoring accepted standards
passed all 73 suites and 121 checks. The integrated candidate passed 124 targeted
tests across eleven groups: Repository Git, contract compilation, private
recording, real MCP observation transport, publication recovery, real MCP
publication and cold readback, snapshot handoff, runtime identity, schema
presentation, routing facts, and the direct/cached supporting workflow. Exact
commands, source-change disposition and log digests are in the
[validation record](checkout-validation.json).

Whitespace checks pass for implementation and edited documentation. The original
profiler output and frozen Planning consumer review retain their terminal blank
lines; the review's bytes still match its three frozen review-request references.

After staging the complete retained file set, both the Engine's generated-input
refresh and a separate read-only repository verification passed all 73 suites
and 121 checks. The [validation record](checkout-validation.json) retains both
structured results.
