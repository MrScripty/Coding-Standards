# Logical Authoring

Use this workflow for standards changes. The Engine accepts canonical IDs,
authored content, explicit semantics, rationale, evidence, and opaque handles.
Repository representation remains private.

## Proposal Lifecycle

1. Form one non-empty `StandardsChangeSet` with an evidence-backed purpose and
   the smallest complete set of explicit edits. Use the `propose` tool schema.
2. Call `propose` with that change set and a retained snapshot, or omit snapshot
   to capture current accepted authority. The Engine creates the proposal and
   analyzes it. Retain its returned `context` and act on that result directly.
3. For compact `needs-action`, inspect the `work` variant and summary counts in
   `outcome`. An inline page supplies `items`; deferred work supplies an explicit
   read selection as described below. Submit ready explicit evidence/owner
   decisions together with `resolve_many` and that context. The entire batch binds the original Analysis;
   a rejection records no decisions. Use `resolve_workflow` for one decision.
   The result supplies the exact successor context and its next work page.
4. If meaning must change, call `revise` with the context and an atomic change
   set. It derives the exact expected revision and analyzes the successor.
   Stale contexts reject instead of selecting a newer head.
5. `complete` analysis can be explicitly `review`ed with consumer, impact, and
   audit acceptances and their evidence. `requires-change` permits revision,
   not review. User authorization must cover the requested review.
6. `ready` returns a readiness context. Call `apply` once when authorized. It
   verifies the exact candidate (including coverage-audit publication) through
   the Engine's complete checkpoint before local publication.
7. For `recovery-required`, retain that same readiness context. `recover` with
   `action: "observe"` reconciles durable publication without Git writes.
   Explicit `action: "complete-publication"` requires current authority and
   revalidates and publishes only the same admitted candidate. Follow the
   returned outcome rather than issuing another `apply`.

`propose` and `revise` already analyze. Continue from the returned result rather
than adding an `analyze` or status call after each successful operation.
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

## Bounded Pending Work

The compact `outcome` is a summary, not a native `pending-result`. Its counts
cover every section. Successful pending `propose`, `revise`, `analyze`,
`resolve_many` and `resolve_workflow` results include one `work` page, preferring
`fact_requirements` when facts are missing, otherwise `pending_obligations`.
A page contains at most eight whole items and 64 KiB of page JSON; it is not a
claim that the full Analysis or all sections have been returned.

For a fact item, use `item.requirement.handle` in the explicit `provide-fact`
submission. For an obligation item, inspect `item.obligation` and its permitted
submission, fingerprint and meaning, then use `item.work`. Audit work uses a
coverage-requirement handle in `claim.requirement`, not an obligation handle.
Each decision keeps its own actual evidence and authorization requirements.
A batch has 1–128 submissions with a 256 KiB serialized-submissions limit.

Focused actions in `next_operations` inherit the enclosing `context`; send it
once alongside their remaining caller inputs. For more items, call
`workflow_details` with `analysis: result.context` plus the unchanged fields of
`work.next`. Those fields bind the same section and observation. Standalone
`workflow_details` responses retain their complete `next` request, including
`analysis`. For another section, explicitly select it using the same context.

If the first record is oversized, `work.kind` is `workflow-work-deferred`.
The mutation has succeeded and retains its context and counts. Its `request`
selects one exact full record without the compact cap; add `analysis` from the
enclosing context and choose that read explicitly when the client can receive
it. Preserve a deferred or otherwise unavailable read as pending work.

After a decision, use the newly returned context and work. Old handles remain
valid only for their historical Analysis, and newly revealed work is decided in
a later round. `workflow_status` stays summary-only; full diagnostic results
retain their native fields and omit inline work. Neither presentation choice
changes review, approval, publication or recovery authority.

## Edit Selection

Use the installed `propose` schema as the authority for edit variants and fields.
The main authoring operations are:

- `create-standard`
- `revise-standard`
- `register-policy-unit`
- `register-consumer`
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
- `rewrite-navigation-index`
- `put-provenance` / `retire-provenance`
- `approve-application-content` / `withdraw-application-content`
- `revise-operational-artifact`

Use the `propose` tool definition for their current exact fields. In
particular:

- whole-standard body changes must include companion policy-unit semantic
  decisions when registered policy meaning changes; `scope_updates` supplies a
  complete registered-scope disposition when a whole-module rewrite changes
  headings or explicitly preserves meaning across structural changes;
- preserved policy meaning uses the schema's preserve variant, while changed
  meaning states accepted and proposed semantic revisions plus intent;
- relationship changes state their meaning, applicability, evidence owner,
  and rationale explicitly;
- retirement supplies complete successor and relationship dispositions; and
- previously registered non-standard consumers use the returned
  `authoring-target-handle`; a consumer registered in the same proposal may use
  its explicit canonical consumer ID.

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

## Register Policies And Consumers

Use `register-policy-unit` for a newly identified scope in an existing standard.
Select a stable policy ID, uniquely resolved heading chain, semantic revision one,
intent and lineage. Registration preserves existing identities and source text.
State changed or preserved semantics explicitly when also revising the owner.

Use `register-consumer` for an actual unregistered consumer already tracked in the
proposal's original repository revision. Supply its canonical ID, repository-relative
path, artifact kind and evidence or projection authority. Hidden directories use
the same containment requirements. The Engine captures original bytes for replay
and publication; it owns catalog and source bindings.

Declare each actual semantic relationship separately. Registration and relationships
can share the change set with newly created policy scopes. Read the candidate to
confirm identity and content, then disposition its consumer and coverage obligations.
Registration itself does not certify coverage. Fixtures and implementations remain
read-only through the content editor; registered Markdown documentation, prompts
and templates support `revise-operational-artifact`.

## Inspect The Candidate Application View

After material review, call authoring `preview_application` with the exact revision
and an application read, route or related request. Inspect the complete returned
content, required closure, relationship filtering and qualification results. Repair
missing qualifications or retain authoring-only material outside application exposure.
Candidate previews remain bound to the revision and do not publish a snapshot.

Refresh the client catalog after an engine update and inspect initialization's
interface and purpose. Reopen preserved work with `workflow_status`; use `resume`
only to explicitly select its current revision. Preserve the proposal's captured
base and follow any stale-base disposition returned by the Engine.

## Navigation Index Correction

For a legacy navigation correction, call `read` with target
`navigation-indexes`. Reuse the result's snapshot `authority` and read a returned
navigation ID to inspect its current content. `rewrite-navigation-index` takes
the returned `entrypoint` handle, explicitly selected canonical destination IDs,
and rationale. The Engine renders the index and requires an evidence-backed
impact disposition for its exact candidate. Use `query_proposal` to read that
candidate before resolving and reviewing it. Navigation results do not confer
normative policy authority. An older snapshot without registrations returns
`NAVIGATION.INDEX_UNAVAILABLE`; capture new authority explicitly when needed.

When a declared destination check requires an obsolete legacy link, supply an
explicit `retargets` disposition with that legacy entrypoint's snapshot-bound
handle and its selected canonical `standard`. The Engine updates the matching
checks atomically with the index. Other required destinations remain enforced;
unused or stale dispositions are rejected.

Index rewrites preserve declared section routes for explicitly selected
canonical owners. Select every required owner; the Engine rejects omissions.
Required artifact routes, such as the Plan template, remain outside this edit's
canonical-standard selection. Do not weaken their coverage inventory to proceed.

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

## Purpose-separated supporting content

Use the [implementation operation map](../../../../tools/standards_engine/PURPOSE-SEPARATION.md#authoring-operation-map)
for the code-to-content handoff. Read operational aids to obtain their captured
authoring target. Submit provenance content and an explicit exposure decision
in the same coherent change as applicable; the Engine binds final candidate
content. Provenance-only maintenance retains unchanged normative revisions.
Application eligibility starts empty and becomes active only after reviewed
publication, not after merely creating a draft.
