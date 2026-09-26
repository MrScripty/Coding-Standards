"""Engine-owned workflow views over existing immutable domain records.

A context references the most advanced available record. Its linked identities
are reconstructed on each call; no transport session or mutable workflow exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tools.standards_analysis.standards_analysis import (
    AnalysisState,
    ProjectedRevisionMaterialRef,
)
from . import _generated_contract as c
from . import analysis_projection
from .authoring import (
    AuthoringError,
    AuthoringFailure,
    ProposalRevision,
    ProposalReadiness,
)

if TYPE_CHECKING:
    from .engine import StandardsEngine
    from .operation_materials import ProposalMaterials


ACTIONS = {
    "draft": ("analyze", "revise"),
    "needs-action": ("resolve_many", "resolve_workflow", "revise"),
    "complete": ("review", "revise"),
    "requires-change": ("revise",),
    "ready": ("apply", "revise"),
    "recovery-required": ("recover",),
    "applied": (),
    "stale": ("resume",),
    "rejected": (),
}
INPUTS = {
    "revise": ["change_set"],
    "resolve_workflow": ["submission"],
    "resolve_many": ["submissions"],
    "review": ["decisions"],
    "recover": ["action"],
}


def invalid(code, message):
    return AuthoringError(AuthoringFailure(code, "invalid", message))


@dataclass(frozen=True)
class BoundWorkflow:
    context: c.WorkflowContext
    revision: ProposalRevision
    analysis: AnalysisState | None = None
    readiness: ProposalReadiness | None = None


def bind(engine: StandardsEngine, context: c.WorkflowContext) -> BoundWorkflow:
    analysis = readiness = None
    if isinstance(context, c.ReadinessHandle):
        readiness = engine._authoring.read_readiness(context.id)
        analysis = engine._load_analysis(
            c.AnalysisHandle.from_value(engine._analysis_handle(readiness.analysis_id))
        )
    elif isinstance(context, c.AnalysisHandle):
        analysis = engine._load_analysis(context)
    if analysis is not None:
        material = analysis.proposed_material
        if not isinstance(material, ProjectedRevisionMaterialRef):
            raise invalid(
                "WORKFLOW.NOT_PROPOSAL", "Workflow context requires proposal analysis."
            )
        revision = engine._authoring.read_revision(material.revision_id)
        if (
            analysis.base_snapshot != revision.base_snapshot
            or material.base_snapshot != revision.base_snapshot
        ):
            raise invalid(
                "WORKFLOW.CONTEXT_MISMATCH",
                "Analysis and proposal snapshot authority differ.",
            )
        if readiness is not None and (
            readiness.revision_id != revision.revision_id
            or readiness.base_snapshot != revision.base_snapshot
        ):
            raise invalid(
                "WORKFLOW.CONTEXT_MISMATCH",
                "Readiness and analysis refer to different proposal authority.",
            )
    elif isinstance(context, c.ProposalRevisionHandle):
        revision = engine._authoring.read_revision(context.id)
    else:
        raise invalid("WORKFLOW.CONTEXT_INVALID", "Unsupported workflow context.")
    return BoundWorkflow(context, revision, analysis, readiness)


def publication_status(engine, readiness):
    """A rejected action leaves the durable admitted lifecycle intact."""
    try:
        application = engine._authoring.read_selected_application(readiness.readiness_id)
    except AuthoringError as error:
        if error.failure.code != "APPLICATION.NOT_ADMITTED":
            raise
        return "ready"
    return "applied" if engine._authoring.application_outcome(application) is not None else "recovery-required"


def view(engine, bound, outcome=None, materials: ProposalMaterials | None = None, *, detail="compact", include_work=False):
    context = bound.context.as_contract()
    status = "draft"
    compact_summary = None
    if isinstance(outcome, c.ApplicationRecoveryRequiredResult):
        status = "recovery-required"
    elif isinstance(outcome, (c.ApplyProposalResult, c.RecoverApplicationResult)):
        status = "applied"
    elif isinstance(outcome, c.RejectedResult):
        status = "rejected"
        if bound.readiness is not None:
            admitted = publication_status(engine, bound.readiness)
            if admitted in ("recovery-required", "applied"):
                status = admitted
    elif bound.readiness is not None:
        status = publication_status(engine, bound.readiness)
    elif bound.analysis is not None:
        if not isinstance(outcome, (c.PendingResult, c.CompleteResult)):
            inputs = (
                None if materials is None
                else engine._evaluation_materials(bound.analysis, materials)
            )
            evaluation = engine._evaluate(bound.analysis, inputs)
            if detail == "compact":
                compact_summary = analysis_projection._analysis_summary(evaluation)
            else:
                outcome = engine._analysis_result(evaluation)
        status = (compact_summary["status"] if compact_summary is not None else
                  "needs-action" if isinstance(outcome, c.PendingResult) else "complete")
        if status == "complete" and engine._review_requires_change(bound.analysis):
            status = "requires-change"
    if status not in ("recovery-required", "applied", "rejected"):
        current = engine._authoring.current_revision(bound.revision.proposal)
        if current.revision_id != bound.revision.revision_id:
            status = "stale"
    result = {
        "kind": "workflow-result",
        "context": context,
        "proposal": engine._proposal_handle(bound.revision.proposal),
        "revision": engine._proposal_revision_handle(bound.revision.revision_id),
        "status": status,
        "next_operations": [
            {
                "operation": operation,
                "required_inputs": INPUTS.get(operation, []),
            }
            for operation in ACTIONS[status]
        ],
    }
    if compact_summary is not None:
        result["outcome"] = compact_summary
    elif outcome is not None:
        from .workflow_presentation import summarize
        result["outcome"] = (summarize(outcome)
                             if detail == "compact" and isinstance(outcome, (c.PendingResult, c.CompleteResult))
                             else outcome.as_contract())
    if include_work and detail == "compact" and status == "needs-action" and isinstance(outcome, c.PendingResult):
        from .workflow_presentation import pending_work
        result["work"] = pending_work(outcome)
    return c.WorkflowResult.from_value(result)


def analyze_revision(engine, revision, materials: ProposalMaterials, *, detail="compact"):
    result = engine._analyze_proposal(c.AnalyzeProposalCall(revision), materials)
    context = (
        result.handle
        if isinstance(result, (c.PendingResult, c.CompleteResult))
        else revision
    )
    return view(engine, bind(engine, context), result, materials, detail=detail, include_work=True)


def propose(engine, call, materials: ProposalMaterials):
    try:
        arguments = call.as_contract()
        snapshot = arguments.get("snapshot")
        if snapshot is None:
            captured = engine.create_snapshot(
                c.CreateSnapshotCall(kind="create-snapshot")
            )
            if isinstance(captured, c.RejectedResult):
                return captured
            snapshot = captured.as_contract()["snapshot"]["snapshot"]
        result = engine._create_proposal(
            c.CreateProposalCall.from_value(
                {
                    "kind": "create-proposal",
                    "base_snapshot": snapshot,
                    "change_set": arguments["change_set"],
                }
            ),
            materials,
        )
        if isinstance(result, c.RejectedResult):
            return result
        return analyze_revision(engine, result.revision, materials, detail=arguments.get("detail", "compact"))
    except engine._domain_errors() as error:
        return engine._domain_rejection(error)


def advance(engine, operation, call, materials: ProposalMaterials | None = None):
    try:
        bound = bind(engine, call.context)
        detail = call.as_contract().get("detail", "compact")
        if operation == "workflow_status":
            return view(engine, bound, materials=materials, detail=detail)
        current = view(engine, bound, materials=materials)
        if operation == "resume" and current.status not in (
            "applied",
            "recovery-required",
        ):
            revision = engine._authoring.current_revision(bound.revision.proposal)
            context = c.ProposalRevisionHandle.from_value(
                engine._proposal_revision_handle(revision.revision_id)
            )
            return view(engine, bind(engine, context), detail=detail)
        if (
            operation not in {item.operation for item in current.next_operations}
            and not (operation == "recover" and current.status == "applied" and bound.readiness is not None)
        ):
            return engine._reject(
                "WORKFLOW.OPERATION_NOT_AVAILABLE",
                "invalid",
                "The requested action is not a continuation of this exact workflow state.",
                details={"status": current.status, "operation": operation},
            )
        revision = current.revision
        arguments = call.as_contract()
        if operation == "revise":
            assert materials is not None
            result = engine._revise_proposal(
                c.ReviseProposalCall.from_value(
                    {
                        "kind": "revise-proposal",
                        "expected_revision": revision.as_contract(),
                        "change_set": arguments["change_set"],
                    }
                ),
                materials,
            )
            if isinstance(result, c.RejectedResult):
                return view(engine, bound, result, materials, detail=detail)
            return analyze_revision(engine, result.revision, materials, detail=arguments.get("detail", "compact"))
        if operation == "analyze":
            assert materials is not None
            return analyze_revision(engine, revision, materials, detail=detail)
        if operation == "resolve_workflow":
            result = engine._resolve(
                c.ResolveCall.from_value(
                    {
                        "analysis": engine._analysis_handle(bound.analysis.analysis_id),
                        "submission": arguments["submission"],
                    }
                ),
                materials,
            )
            context = (
                result.handle
                if isinstance(result, (c.PendingResult, c.CompleteResult))
                else call.context
            )
        elif operation == "review":
            result = engine.review_proposal(
                c.ReviewProposalCall.from_value(
                    {
                        "kind": "review-proposal",
                        "analysis": engine._analysis_handle(bound.analysis.analysis_id),
                        "decisions": arguments["decisions"],
                    }
                )
            )
            context = (
                result.readiness
                if isinstance(result, c.ReviewProposalResult)
                else call.context
            )
        elif operation == "apply":
            result = engine.apply_proposal(
                c.ApplyProposalCall.from_value(
                    {"kind": "apply-proposal", "readiness": call.context.as_contract()}
                )
            )
            context = call.context
        elif operation == "recover":
            result = engine.recover_application(
                c.RecoverApplicationCall.from_value(
                    {
                        "kind": "recover-application",
                        "readiness": call.context.as_contract(),
                        "action": arguments.get("action", "observe"),
                    }
                )
            )
            context = call.context
        else:
            raise invalid(
                "WORKFLOW.OPERATION_INVALID", "Unsupported workflow operation."
            )
        return view(
            engine, bound if context == call.context else bind(engine, context), result, materials,
            detail=detail, include_work=True
        )
    except engine._domain_errors() as error:
        return engine._domain_rejection(error)
