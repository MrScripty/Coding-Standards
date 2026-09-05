# Logical Authoring

Use this workflow for standards changes. The Engine accepts canonical IDs,
authored content, explicit semantics, rationale, evidence, and opaque handles.
Repository representation remains private.

## Proposal Lifecycle

1. Call `create_snapshot`; use its returned Snapshot handle as the proposal
   base.
2. Form one non-empty `StandardsChangeSet` with an evidence-backed `purpose`
   and the smallest complete set of explicit edits. Inspect the live
   `create_proposal` schema before constructing it.
3. Call `create_proposal`. Retain both the proposal and exact revision handles.
4. Use `query_proposal` to read, route, or inspect relationships in that exact
   projected revision. For ordinary edits, run `verify_proposal` and inspect
   its report. Coverage-audit proposals require review readiness before
   verification. Call `analyze_proposal` with the revision handle; a passing
   checkpoint does not replace semantic review.
5. Resolve each pending Analysis requirement for which an authorized owner has
   supplied the exact decision and evidence through the public `resolve`
   operation. Otherwise stop and report the pending state. The Engine derives
   mechanical projection only.
6. If the proposal must change, call `revise_proposal` with the exact current
   `expected_revision` and another atomic change set, then analyze the returned
   revision. A stale revision is rejected rather than merged implicitly.
7. After Analysis is complete, `review_proposal` requires explicit consumer,
   impact, and audit decisions with evidence plus current trusted
   authorization. Retain the returned readiness handle.
8. For coverage audits, call `verify_proposal` with both the revision and
   readiness handles and require a passing result. Then call `apply_proposal`
   once with that readiness handle. Success means the
   exact candidate passed the complete checkpoint and was published to the
   configured local canonical ref.
9. If application returns recovery-required, call `recover_application` with
   the same readiness handle. Recovery observes durable state; it does not
   stage, verify, publish, retry, or roll back.

Use `find_proposals` to resume durable proposal heads and `query_proposal` to
reconstruct an exact historical revision after process replacement.

## Edit Selection

The closed edit variants are:

- `create-standard`
- `revise-standard`
- `revise-policy-unit`
- `move-policy-unit`
- `retire-policy-unit`
- `retire-standard`
- `replace-standard-relationships`
- `put-policy-relationship`
- `remove-policy-relationship`
- `put-routing-rule` / `remove-routing-rule`
- `put-routing-fact` / `remove-routing-fact`
- `audit-policy-unit`

Use `invoke.py --schema create_proposal` for their current exact fields. In
particular:

- whole-standard body changes must include companion policy-unit semantic
  decisions when registered policy meaning changes;
- preserved policy meaning uses the schema's preserve variant, while changed
  meaning states accepted and proposed semantic revisions plus intent;
- relationship changes state their meaning, applicability, evidence owner,
  and rationale explicitly;
- retirement supplies complete successor and relationship dispositions; and
- non-standard relationship consumers use an `authoring-target-handle`
  returned by Snapshot-bound relationship discovery.

Before editing routes, use `query` or `query_proposal` with a Router read
request: `{"kind":"read","target":"router","include_routing":true}`. The
returned `routing` field supplies editable rule and fact definitions.

Routing edits name canonical rule, fact, and target IDs. A rule supplies its
applicability expression and a readable condition. The Engine updates the
selection table and executable projection together. Include related fact and
rule changes in one change set; referenced facts cannot be removed alone.
Fact semantic changes increment their revision; prompt-only edits preserve it.

Every evidence reference must identify real, available exact bytes through a
recognized provider contract, and its digest must be the SHA-256 digest of
those bytes. A schema-valid placeholder, invented provider contract, or digest
of unrelated text is not evidence even when proposal-shape validation accepts
it. For the local facade, use provider `repository-content`, version `1`,
with a normalized repository-relative file path as the ID and the digest of
that file’s bytes. The adapter reads the file and verifies the digest.

Do not infer semantic relatedness, impact, lifecycle meaning, evidence
sufficiency, or successors from prose. If the user has not decided required
meaning, stop at the typed rejection or ask for that decision instead of
manufacturing closure.

## Coverage Audit Publication

Use `read` with `include_coverage: true` to identify registered policy units
requiring review. Add `audit-policy-unit` edits naming those policies and the
review rationale. These edits request certificate publication without changing
standard text. Already-current certificates need no renewal.

Resolve the exact coverage and consumer obligations, then obtain review
readiness. `verify_proposal` requires that readiness for an audit proposal so
it checks the candidate containing the receipt. Application reauthorizes the
review through the configured Engine auditor, checks destination evidence and
requirement identities, and publishes through the normal application lifecycle.

Repository publications use Engine audit authority. Receipt records preserve
the actual auditor separately from caller-supplied provenance, along with
pinned evidence and authorization proof. Evidence must exist in the destination
repository with the reviewed bytes. A changed authority or invalidated
requirement requires fresh review; switching authority does not renew a claim.
A subsequent Snapshot read reports the retained auditor with coverage status.

## Publication Boundary

The proposal head, readiness, and application selection are immutable and
content-bound. Preserve their handles exactly. The Engine owns candidate files,
the complete verifier, proposal-specific conventional commit construction, and
the local-ref compare-and-swap.

Application does not push a remote. A local applied result is the terminal
outcome for this workflow.

## Repository Verification

Use `verify_repository` to check the current working tree. Set
`refresh_verification_inputs` to `false` for a read-only checkpoint. When
source edits have made the generated suite-input manifest stale, set it to
`true` to let the Engine rebuild that projection before checking. This option
requires the bound `standards.verify` authority. Inspect `verification.passed`
and the reported failures; the result kind alone does not mean success.

Repository verification does not create an accepted Snapshot. Snapshot capture
still reads the committed revision. Proposal verification materializes an
isolated candidate and runs the same checkpoint used by application; it does
not publish a ref or supply review decisions. Application rechecks the candidate.
