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


def details(engine: StandardsEngine, call: c.WorkflowDetailsCall):
    """Read one bounded section of a fresh evaluation without publishing it."""
    try:
        state = engine._load_analysis(call.analysis)
        evaluation = engine._evaluate(state)
        arguments = call.as_contract()
        section = arguments["section"]
        offset, limit = arguments.get("offset", 0), arguments.get("limit", 8)
        if section == "pending_obligations":
            items = [{"kind": "workflow-obligation-work",
                      "obligation": engine._obligation_projection(state, item),
                      "work": engine._obligation_work_handle(evaluation, item)}
                     for item in evaluation.obligations if item.state == "required"]
        elif section == "obligations":
            items = [engine._obligation_projection(state, item) for item in evaluation.obligations]
        elif section == "fact_requirements":
            items = [engine._requirement_work(state, item) for item in evaluation.pending_requirements]
        elif section == "coverage_certificates":
            items = [engine._certificate_projection(state, item) for item in evaluation.coverage
                     if item.certificate is not None]
        elif section == "dispositions":
            items = engine._disposition_projections(state)
        elif section == "fact_observations":
            items = engine._observation_projections(state)
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
        result = {
            "kind": "workflow-details-result", "analysis": call.analysis.as_contract(),
            "section": section, "observation": observed, "offset": offset,
            "total": len(items), "items": items[offset:stop],
        }
        if stop < len(items):
            result["next"] = {"analysis": call.analysis.as_contract(), "section": section,
                              "observation": observed, "offset": stop, "limit": limit}
        if len(json.dumps(result).encode()) > PAGE_BYTES:
            return engine._reject("WORKFLOW.RESULT_LIMIT", "unsupported",
                                  "Select a smaller detail page or inspect one returned work handle.",
                                  details={"limit_bytes": PAGE_BYTES})
        return c.WorkflowDetailsResult.from_value(result)
    except engine._domain_errors() as error:
        return engine._domain_rejection(error)
