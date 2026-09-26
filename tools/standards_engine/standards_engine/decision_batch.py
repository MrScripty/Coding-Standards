"""Stage explicit decisions with the ordinary validator and one durable result."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING

from . import _generated_contract as c
from . import analysis_projection
from .agent_workflow import bind, view

if TYPE_CHECKING:
    from .engine import StandardsEngine
    from .operation_materials import ProposalMaterials


INPUT_BYTES = 256 * 1024


def _work(submission: dict) -> tuple[dict, str]:
    kind = submission["kind"]
    if kind == "provide-fact":
        return submission["requirement"], "fact-requirement"
    if kind == "coverage-attestation":
        return submission["claim"]["requirement"], "coverage-requirement"
    return submission["obligation"], "obligation"


def resolve_many(engine: StandardsEngine, call: c.ResolveManyCall, materials: ProposalMaterials):
    """All submissions bind the original context; only the final state is stored.

The snapshot store's existing head guard makes this local publication atomic.
External authorizer/evidence observations remain ordinary per-decision effects.
"""
    index = None
    try:
        arguments = call.as_contract()
        submitted = arguments["submissions"]
        if len(json.dumps(submitted).encode()) > INPUT_BYTES:
            return engine._reject("WORKFLOW.INPUT_LIMIT", "invalid",
                                  "Select a smaller batch of explicit decisions.",
                                  details={"limit_bytes": INPUT_BYTES})
        bound = bind(engine, call.context)
        current = engine._authoring.current_revision(bound.revision.proposal)
        if current.revision_id != bound.revision.revision_id:
            return engine._reject("WORKFLOW.STALE_CONTEXT", "invalid",
                                  "Resume and analyze the current proposal revision.")
        state = bound.analysis
        inputs = engine._evaluation_materials(state, materials)
        evaluation = engine._evaluate(state, inputs)
        selectable = {
            ("fact-requirement", item.id) for item in evaluation.pending_requirements
        } | {
            ("obligation", analysis_projection._obligation_child_id(item.id))
            for item in evaluation.obligations if item.state == "required"
        } | {
            ("coverage-requirement", item.requirement_id) for item in evaluation.coverage
            if any(obligation.kind == "audit-coverage" and obligation.state == "required"
                   and obligation.target == item.subject for obligation in evaluation.obligations)
        }
        seen = set()
        for index, raw in enumerate(submitted):
            work, kind = _work(raw)
            handle = c.AnalysisChildHandle.from_value(work)
            engine._current_child(handle, state, kind)
            key = (kind, handle.child_id)
            if key not in selectable:
                engine._not_applicable()
            if key in seen:
                return engine._reject("WORKFLOW.DUPLICATE_DECISION", "invalid",
                                      "Supply one decision for each selected work item.",
                                      details={"submission_index": index})
            seen.add(key)
        for index, raw in enumerate(submitted):
            # These dictionaries are freshly decoded from immutable request values.
            # Rebind only after proving that every supplied handle belonged to the
            # original context. The ordinary validator still checks current work,
            # fingerprint, evidence, capability and authorization at each step.
            work, _ = _work(raw)
            work["analysis"] = analysis_projection._analysis_handle(evaluation.state.analysis_id)
            local = c.ResolveCall.from_value({
                "analysis": analysis_projection._analysis_handle(evaluation.state.analysis_id),
                "submission": raw,
            })
            successor = engine._apply_submission(evaluation, local)
            evaluation = engine._evaluate(successor, inputs)
        state, evaluation = engine._apply_providers(evaluation.state, evaluation, inputs)
        record = state.aggregate(analysis_projection._analysis_children(evaluation))
        published = engine._snapshots.publish_aggregate_if_root_head(
            str(bound.revision.proposal), bound.revision.revision_id, record)
        if published == "stale":
            return engine._reject("WORKFLOW.STALE_CONTEXT", "invalid",
                                  "The proposal advanced before the decision batch was recorded.")
        context = c.AnalysisHandle.from_value(analysis_projection._analysis_handle(state.analysis_id))
        return view(engine, bind(engine, context), analysis_projection._analysis_result(evaluation), materials,
                    detail=arguments.get("detail", "compact"))
    except engine._domain_errors() as error:
        rejected = engine._domain_rejection(error).as_contract()
        if index is not None:
            rejected["details"]["submission_index"] = index
        return c.RejectedResult.from_value(rejected)
