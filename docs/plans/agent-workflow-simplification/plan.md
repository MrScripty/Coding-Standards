# Agent Workflow Simplification

Status: Verifying (implementation complete; qualification gates remain). Base: `c4470f9e683da1e494eeeac3497e72e079221bac`.
Operation: implement this bounded Engine interface slice on an isolated branch.
The user authorized implementation and a changed-files ZIP, not remote publication.

## Objective and admission

Reduce mechanical work in multi-turn standards interactions. Pending compact
mutation results supply the first bounded page of actual unresolved work;
focused continuations and compact summaries inherit the enclosing immutable
context. Agent instructions teach grouped reads, same-analysis decision batches,
and the analysis already performed by propose/revise. Preserve every actual
fact, evidence, decision, review, publication and recovery boundary.

The existing focused workflow, Analysis projections and detail-page owner suffice.
This is an interface presentation change, not a new workflow store or lifecycle.
The first pending section is fact requirements when present, otherwise required
obligations. Status reads remain summary-only. Full diagnostic results remain
available. Whole records, exact observations and explicit oversized-record reads
retain the existing detail contract. Inline pages use already-produced pending
results, avoiding another load/evaluation or any provider/authorization work.

## Contract and cutover

Interface 38 is a coordinated replacement of the focused result presentation.
Requests, Analysis state/request versions, handles and persisted store formats
remain unchanged. `context` occurs once in the focused action envelope. Work
handles remain complete, independently usable authority references. Relative
work continuations acquire `analysis` from their enclosing context when invoked.
Restart the Engine and refresh/reconnect clients; retain all existing handles
and stores. Historical contexts reconstruct through the new presentation.

No normative policy, application exposure, provenance, provider, authorization,
readiness or publication semantics are changed. Authoring skill references are
implementation-maintenance instructions, updated with their actual API owner.

## Explicit write set

- `tools/standards_engine/standards_engine/{agent_workflow,analysis_projection,decision_batch,workflow_presentation,mcp}.py`.
- Canonical Engine schema/interface, generated Python and tool projections, and
  authored examples under `tools/standards_engine/contracts/`.
- Focused regression tests, affected presentation/runtime-version assertions,
  and the cold MCP batch consumer under `tools/standards_engine/tests/`.
- Engine READMEs/PURPOSE-SEPARATION and `.agents/skills/standards-engine/` skill
  plus navigation, authoring and environment reference instructions.
- This plan, ledger, issues, verification report and generated suite-input manifest.

Directly affected consumers may be added with an explicit ledger entry. Unrelated
source, normative standards and user state remain outside the write set.

## Acceptance evidence

1. Before/after real Engine interaction traces: number of calls, serialized
   arguments/results, exact results and preserved explicit terminal actions.
   Byte counts are not a tokenizer, billing or model-performance claim.
2. Focused domain tests: inline facts/impact/coverage work, exact page equivalence,
   byte pressure, oversized records, stale/foreign work rejection, cold readback,
   lightweight status, and no additional evaluation/publication for presentation.
3. Generated freshness, authored examples, schema rejection and actual stdio
   consumption; existing batching, publication, recovery and purpose-isolation tests.
4. Repository complete structural checkpoint and affected package/Engine tests.
5. Supported locked Python 3.11/3.12 and actual configured client qualification;
   independent external review before accepted integration. Missing qualification
   remains explicit rather than being replaced by weaker local evidence.

## Deferred alternatives

Keep schema-description compatibility because supported-client rendering was its
original authority. Route-plus-content and request-local evidence deduplication
remain follow-on candidates pending representative client measurements. Neither
is necessary for this slice's interaction improvement.

## Next slice

The bounded implementation and local verification are complete. Use
`verification.md` for the evidence and reviewable ZIP contents. Final acceptance remains with the named qualification
and independent review evidence; no remote push or merge is part of this task.
