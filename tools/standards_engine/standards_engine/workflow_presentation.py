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


PAGE_BYTES = 64 * 1024
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
        "handle": value["handle"],
        "status": value["status"],
        "required_obligations": required,
        "pending_facts": len(value.get("fact_requirements", [])),
        "sections": [{"section": key, "count": count} for key, count in counts.items()],
        "details": {"operation": "workflow_details", "analysis": value["handle"]},
    }


def details(
    engine: StandardsEngine, call: c.WorkflowDetailsCall,
) -> c.WorkflowDetailsResult | c.RejectedResult:
    """Project one bounded section of an immutable Analysis without publishing it."""
    try:
        arguments = call.as_contract()
        full = arguments.get("detail", "compact") == "full"
        section = arguments["section"]
        # JSON Schema integer admits integral JSON numbers such as 1.0.
        # Validation is complete; normalize only the Python indexing representation.
        offset = int(arguments.get("offset", 0))
        limit = int(arguments.get("limit", 1 if full else 8))
        if full and limit != 1:
            return engine._reject(
                "WORKFLOW.FULL_DETAIL_LIMIT", "invalid",
                "Full detail retrieves one complete record; omit limit or select 1.",
            )
        state = engine._load_analysis(call.analysis)
        evaluation = engine._evaluate(state)
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
        binding = {"analysis": call.analysis.as_contract(), "section": section, "items": items}
        observed = "sha256:" + hashlib.sha256(
            json.dumps(binding, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        expected = arguments.get("observation")
        if (offset and expected is None) or (expected is not None and expected != observed):
            return engine._reject("WORKFLOW.OBSERVATION_CHANGED", "invalid",
                                  "Read the section from offset zero to obtain its current observation.")
        if offset > len(items):
            return engine._reject("WORKFLOW.PAGE_RANGE", "invalid",
                                  "Select an offset within the observed section.")
        stop = min(offset + limit, len(items))
        analysis = call.analysis.as_contract()
        result = _page(analysis, section, observed, items, offset, stop, limit)
        if not full:
            # At most sixteen candidate sizes. Keep complete records and the same
            # whole-section observation; never skip an oversized first record.
            while stop > offset and _page_size(result) > PAGE_BYTES:
                stop -= 1
                result = _page(analysis, section, observed, items, offset, stop, limit)
            if (stop == offset and offset < len(items)) or _page_size(result) > PAGE_BYTES:
                request = {
                    "analysis": analysis, "section": section, "offset": offset,
                    "limit": 1, "observation": observed, "detail": "full",
                }
                rejected = engine._reject(
                    "WORKFLOW.RESULT_LIMIT", "unsupported",
                    "One complete record exceeds the compact page limit. Explicitly "
                    "select the returned full-detail request only when the client "
                    "can receive its size-unbounded single-record result.",
                    details={"limit_bytes": PAGE_BYTES, "offset": offset,
                             "section": section},
                ).as_contract()
                rejected["next_operations"] = [{
                    "operation": "workflow_details", "request_kind": "workflow-details",
                    "request": request,
                }]
                return c.RejectedResult.from_value(rejected)
        return c.WorkflowDetailsResult.from_value(result)
    except engine._domain_errors() as error:
        return engine._domain_rejection(error)


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
