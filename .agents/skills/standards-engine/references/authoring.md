# Logical Authoring

Use this workflow for standards changes. The Engine accepts canonical IDs,
authored content, explicit semantics, rationale, evidence, and opaque handles.
Repository representation remains private.

## Proposal Lifecycle

1. Form one non-empty `StandardsChangeSet` with an evidence-backed purpose and
   the smallest complete set of explicit edits. Use the `propose` tool schema.
2. Call `propose` with that change set and a retained snapshot, or omit snapshot
   to capture current accepted authority. The Engine creates the proposal and
   analyzes it. Retain its returned `context`.
3. For `needs-action`, inspect `outcome.fact_requirements`, `outcome.obligations`,
   and the projected work. Use `resolve_workflow` with the current context and
   one actual evidence/owner-decision submission. A returned context identifies
   the exact resulting immutable analysis branch.
4. If meaning must change, call `revise` with the context and an atomic change
   set. It derives the exact expected revision and analyzes the successor.
   Stale contexts reject instead of selecting a newer head.
5. `complete` analysis can be explicitly `review`ed with consumer, impact, and
   audit acceptances and their evidence. `requires-change` permits revision,
   not review. User authorization must cover the requested review.
6. `ready` returns a readiness context. Call `apply` once when authorized. It
   verifies the exact candidate (including coverage-audit publication) through
   the Engine's complete checkpoint before local publication.
7. For `recovery-required`, call `recover` using that same context. It observes
   durable state without verification, publication, retries, or rollback.

Use `workflow_status` to reconstruct exact state after reconnecting. A `stale`
context remains historical; `resume` explicitly selects the proposal's current
revision and returns a draft context for `analyze` or `revise`. Existing Analysis
branches remain immutable branches; there is no hidden latest-analysis pointer.
If all task context is lost, use advanced `find_proposals` and pass the selected
revision as context to resume explicitly.

`query_proposal` and the returned `revision` remain available for exact historical
reads and relationship discovery. Native preflight `verify_proposal` is in the
advanced catalog; it does not replace review or the verification inside apply.
A verification or Analysis failure after proposal creation retains a revision
context when available, so the created proposal is not mistaken for absent work.

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

Use the `propose` tool definition for their current exact fields. In
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

Before editing routes, use focused `read` or `query_proposal` with a Router read
request: `{"target":"router","include_routing":true}` for `read` (add the native
`kind: "read"` inside the request for `query_proposal`). The
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
readiness with `review`. `apply` verifies the candidate containing the receipt
and reauthorizes publication through the configured Engine auditor. If a
separate preflight is needed, advanced `verify_proposal` requires both the
returned revision and readiness context for a coverage-audit proposal.

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

These administrative calls use the explicit advanced MCP catalog.

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

## Evidence Catalog Maintenance

Use the advanced MCP catalog for these operations.

Use `maintain_evidence` for explicit certificate/check/suite retirements,
evidence descriptions, and consumer registrations. Use its tool schema and
supply the current Git revision plus exact review evidence. Preview with
`apply: false`; inspect changed/removed paths and `verification.passed`.
`apply: true` verifies the candidate again and updates only unchanged affected
working-tree paths. Commit the resulting maintenance with its review record.
This operation does not change normative policy, certify completeness, publish
Git refs, or require replacement attestations for deleted stale claims.

Use `plan.unregister_policy_subjects` for explicit review-registration pruning.
This removes selected subjects and their incident policy relationships without
removing standard text or module routing. Review the retained and removed scopes
in the evidence record; unregistered text still receives ordinary whole-artifact
change analysis. Use `retire-policy-unit` instead only when the normative policy
itself is being retired. Maintenance prunes claims against the final candidate's
requirements, including claims invalidated by the registration changes.
