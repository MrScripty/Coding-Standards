"""Bounded workflow views over authoritative Analysis results.

Summary and detail pages select information; they create no decisions, readiness,
or mutable paging state. Observation bindings prevent mixing contexts or sections.
Historical decisions remain historical; publication owns live evidence validation.
"""
from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING

from . import _generated_contract as c
from . import analysis_projection

if TYPE_CHECKING:
    from .engine import StandardsEngine
    from .operation_materials import ProposalMaterials


PAGE_BYTES = 64 * 1024
DEFAULT_PAGE_ITEMS = 8
SECTIONS = (
    "pending_obligations", "obligations", "fact_requirements",
    "coverage_certificates", "dispositions", "fact_observations",
    "reading_plan", "changed_units",
)


def summarize(outcome: c.PendingResult | c.CompleteResult) -> dict[str, object]:
    value = outcome.as_contract()
    obligations = value.get("obligations", [])
    required = sum(item["state"] == "required" for item in obligations)
    counts = {key: len(value[key]) for key in SECTIONS if key in value}
    counts["pending_obligations"] = required
    return {
        "kind": "workflow-analysis-summary",
        "status": value["status"],
        "required_obligations": required,
        "pending_facts": len(value.get("fact_requirements", [])),
        "sections": [{"section": key, "count": count} for key, count in counts.items()],
        "details": {"operation": "workflow_details"},
    }


def details(
    engine: StandardsEngine, call: c.WorkflowDetailsCall, materials: ProposalMaterials,
) -> c.WorkflowDetailsResult | c.RejectedResult:
    """Project one bounded section of an immutable Analysis without publishing it."""
    try:
        arguments = call.as_contract()
        full = arguments.get("detail", "compact") == "full"
        section = arguments["section"]
        # JSON Schema integer admits integral JSON numbers such as 1.0.
        # Validation is complete; normalize only the Python indexing representation.
        offset = int(arguments.get("offset", 0))
        limit = int(arguments.get("limit", 1 if full else DEFAULT_PAGE_ITEMS))
        if full and limit != 1:
            return engine._reject(
                "WORKFLOW.FULL_DETAIL_LIMIT", "invalid",
                "Full detail retrieves one complete record; omit limit or select 1.",
            )
        state = engine._load_analysis(call.analysis)
        # Reuse exact immutable inputs, not an earlier evaluation or page. The
        # material/evaluation owners retain durable, lifecycle and revision checks.
        inputs = engine._evaluation_materials(state, materials)
        evaluation = engine._evaluate(state, inputs)
        if section == "pending_obligations":
            items = [{"kind": "workflow-obligation-work",
                      "obligation": analysis_projection._obligation_projection(state, item),
                      "work": analysis_projection._obligation_work_handle(evaluation, item)}
                     for item in evaluation.obligations if item.state == "required"]
        elif section == "obligations":
            items = [analysis_projection._obligation_projection(state, item) for item in evaluation.obligations]
        elif section == "fact_requirements":
            items = [analysis_projection._requirement_work(state, item) for item in evaluation.pending_requirements]
        elif section == "coverage_certificates":
            items = [analysis_projection._certificate_projection(state, item) for item in evaluation.coverage
                     if item.certificate is not None]
        elif section == "dispositions":
            items = analysis_projection._disposition_projections(state)
        elif section == "fact_observations":
            items = analysis_projection._observation_projections(state)
        elif section == "reading_plan":
            items = [item.as_contract() for item in evaluation.reading_plan]
        else:  # The generated enum exhausts the selected sections.
            items = [unit.as_contract() for change in evaluation.changes for unit in change.changed_units]
        analysis = call.analysis.as_contract()
        observed = _observation(analysis, section, items)
        expected = arguments.get("observation")
        if (offset and expected is None) or (expected is not None and expected != observed):
            return engine._reject("WORKFLOW.OBSERVATION_CHANGED", "invalid",
                                  "Read the section from offset zero to obtain its current observation.")
        if offset > len(items):
            return engine._reject("WORKFLOW.PAGE_RANGE", "invalid",
                                  "Select an offset within the observed section.")
        result = _bounded_page(analysis, section, observed, items, offset, limit, full=full)
        if result is None:
            rejected = engine._reject(
                "WORKFLOW.RESULT_LIMIT", "unsupported",
                "One complete record exceeds the compact page limit. Explicitly "
                "select the returned full-detail request only when the client "
                "can receive its size-unbounded single-record result.",
                details={"limit_bytes": PAGE_BYTES, "offset": offset, "section": section},
            ).as_contract()
            rejected["next_operations"] = [{
                "operation": "workflow_details", "request_kind": "workflow-details",
                "request": {"analysis": analysis, **_full_selection(section, observed, offset)},
            }]
            return c.RejectedResult.from_value(rejected)
        return c.WorkflowDetailsResult.from_value(result)
    except engine._domain_errors() as error:
        return engine._domain_rejection(error)


def pending_work(outcome: c.PendingResult) -> dict[str, object]:
    """Present already-issued work without another evaluation or evidence read.

    Audit obligations use their issued coverage-requirement continuation, not
    the obligation handle. Every actionable handle retains its exact Analysis
    identity; only enclosing page and navigation bindings are relative.
    """
    if outcome.fact_requirements:
        section = "fact_requirements"
        items = [item.as_contract() for item in outcome.fact_requirements]
    else:
        section = "pending_obligations"
        coverage = {item.target: item.work for item in outcome.next_operations
                    if item.request_kind == "coverage-attestation"}
        items = [
            {"kind": "workflow-obligation-work", "obligation": item.as_contract(),
             "work": (coverage[item.target] if item.kind == "audit-coverage" else item.handle).as_contract()}
            for item in outcome.obligations if item.state == "required"
        ]
    analysis = outcome.handle.as_contract()
    observed = _observation(analysis, section, items)
    page = _bounded_page(analysis, section, observed, items, 0, DEFAULT_PAGE_ITEMS)
    if page is None:
        return {
            "kind": "workflow-work-deferred", "code": "WORKFLOW.RESULT_LIMIT",
            "section": section, "total": len(items),
            "request": _full_selection(section, observed, 0),
        }
    # Budget the larger standalone representation so this relative projection
    # also fits. Its observation and continuation match an independent read.
    page.pop("analysis")
    page["kind"] = "workflow-work-page"
    if "next" in page:
        page["next"].pop("analysis")
    return page


def _observation(analysis: dict[str, object], section: str, items: list[dict[str, object]]) -> str:
    binding = {"analysis": analysis, "section": section, "items": items}
    return "sha256:" + hashlib.sha256(
        json.dumps(binding, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _full_selection(section: str, observed: str, offset: int) -> dict[str, object]:
    return {"section": section, "offset": offset, "limit": 1,
            "observation": observed, "detail": "full"}


def _bounded_page(
    analysis: dict[str, object], section: str, observed: str,
    items: list[dict[str, object]], offset: int, limit: int, *, full: bool = False,
) -> dict[str, object] | None:
    stop = min(offset + limit, len(items))
    result = _page(analysis, section, observed, items, offset, stop, limit)
    if not full:
        # At most sixteen candidate sizes. Keep complete records and the same
        # whole-section observation; never skip an oversized first record.
        while stop > offset and _page_size(result) > PAGE_BYTES:
            stop -= 1
            result = _page(analysis, section, observed, items, offset, stop, limit)
        if (stop == offset and offset < len(items)) or _page_size(result) > PAGE_BYTES:
            return None
    return result


def _page(
    analysis: dict[str, object], section: str, observed: str,
    items: list[dict[str, object]], offset: int, stop: int, limit: int,
) -> dict[str, object]:
    """Construct an exact contiguous page and its compact continuation."""
    result = {
        "kind": "workflow-details-result", "analysis": analysis,
        "section": section, "observation": observed, "offset": offset,
        "total": len(items), "items": items[offset:stop],
    }
    if stop < len(items):
        result["next"] = {
            "analysis": analysis, "section": section, "observation": observed,
            "offset": stop, "limit": limit,
        }
    return result


def _page_size(result: dict[str, object]) -> int:
    # Keep the existing result-JSON accounting (including escapes and next).
    # Transport envelopes and client-specific pretty-printing are not this cap.
    return len(json.dumps(result).encode("utf-8"))
