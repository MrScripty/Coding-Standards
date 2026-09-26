"""Pure Analysis-to-interface projections within the existing Engine owner.

These functions receive immutable Analysis values. They do not load stores,
select proposal heads, authorize decisions, invoke providers or publish records.
Analysis remains the semantic owner; this module only constructs the existing
public values and child-record payloads from an already evaluated Analysis.
"""
from __future__ import annotations

from tools.standards_analysis.standards_analysis import (
    AnalysisEvaluation,
    AnalysisState as DomainAnalysisState,
    child_id as analysis_child_id,
    plain_record,
)

from ._generated_contract import CompleteResult, PendingResult


def _analysis_result(
    evaluation: AnalysisEvaluation,
) -> PendingResult | CompleteResult:
    state = evaluation.state
    handle = _analysis_handle(state.analysis_id)
    context = _context_projection(evaluation)
    changed_units = [
        unit.as_contract()
        for change in evaluation.changes
        for unit in change.changed_units
    ]
    if not evaluation.complete:
        requirements = [
            _requirement_work(state, item)
            for item in evaluation.pending_requirements
        ]
        obligations = [
            _obligation_projection(state, item)
            for item in evaluation.obligations
        ]
        next_operations = [
            {
                "operation": "resolve",
                "request_kind": "provide-fact",
                "target": item.fact.id,
                "work": _analysis_child_handle(
                    state.analysis_id, "fact-requirement", item.id
                ),
                "analysis": handle,
            }
            for item in evaluation.pending_requirements
        ]
        next_operations.extend(
            {
                "operation": "resolve",
                "request_kind": item.permitted_submissions[0],
                "target": item.target,
                "work": _obligation_work_handle(evaluation, item),
                "analysis": handle,
            }
            for item in evaluation.obligations
            if item.state == "required"
        )
        return PendingResult.from_value(
            {
                "kind": "pending-result",
                "handle": handle,
                "status": "needs-action",
                "context": context,
                "changes": [_plain(item) for item in state.changes],
                "changed_units": changed_units,
                "obligations": obligations,
                "fact_requirements": requirements,
                "reading_plan": [
                    item.as_contract() for item in evaluation.reading_plan
                ],
                "next_operations": next_operations,
                "summary": "The bounded analysis requires additional decisions.",
            }
        )
    certificates = [
        _certificate_projection(state, item)
        for item in evaluation.coverage
        if item.certificate is not None
    ]
    return CompleteResult.from_value(
        {
            "kind": "complete-result",
            "handle": handle,
            "status": "complete",
            "context": context,
            "changes": [_plain(item) for item in state.changes],
            "changed_units": changed_units,
            "coverage_certificates": certificates,
            "fact_observations": _observation_projections(state),
            "dispositions": _disposition_projections(state),
            "reading_plan": [
                item.as_contract() for item in evaluation.reading_plan
            ],
            "completion": {
                "required_coverage_subjects": [
                    item.subject for item in evaluation.coverage
                ],
                "certificate_subjects": [
                    item.subject
                    for item in evaluation.coverage
                    if item.certificate is not None
                ],
                "reached_consumer_obligations": [
                    item.id
                    for item in evaluation.reached_obligations
                    if item.kind == "consumer-review"
                ],
                "disposition_obligations": [
                    str(_plain(item)["obligation_id"])
                    for item in state.dispositions
                ],
                "required_fact_requirements": [
                    f"fact-requirement:{item.id}"
                    for item in evaluation.requirements
                ],
                "observed_fact_requirements": [
                    f"fact-requirement:{_plain(item)['requirement_id']}"
                    for item in state.fact_observations
                    if _plain(item)["requirement_id"]
                    in {value.id for value in evaluation.requirements}
                ],
                "non_consumer_obligations_resolved": True,
                "applicability_resolved": True,
                "authorization_valid": True,
                "evidence_valid": True,
            },
            "summary": "The bounded analysis is complete.",
        }
    )



def _analysis_summary(evaluation: AnalysisEvaluation) -> dict[str, object]:
    """Project compact status without constructing omitted full-result records.

    Section order and presence match summarizing the full public result, not
    every section that can be requested independently through detail reads.
    The caller retains evaluation, lifecycle checks and result validation.
    """
    complete = evaluation.complete
    if complete:
        counts = {
            "coverage_certificates": sum(
                item.certificate is not None for item in evaluation.coverage
            ),
            "dispositions": len(evaluation.state.dispositions),
            "fact_observations": len(evaluation.state.fact_observations),
        }
        required = pending_facts = 0
    else:
        pending_facts = len(evaluation.pending_requirements)
        required = sum(item.state == "required" for item in evaluation.obligations)
        counts = {
            "obligations": len(evaluation.obligations),
            "fact_requirements": pending_facts,
        }
    counts.update({
        "reading_plan": len(evaluation.reading_plan),
        "changed_units": sum(len(change.changed_units) for change in evaluation.changes),
        "pending_obligations": required,
    })
    return {
        "kind": "workflow-analysis-summary",
        "status": "complete" if complete else "needs-action",
        "required_obligations": required,
        "pending_facts": pending_facts,
        "sections": [{"section": key, "count": count} for key, count in counts.items()],
        "details": {"operation": "workflow_details"},
    }


def _analysis_children(
    evaluation: AnalysisEvaluation,
) -> tuple[tuple[str, str, dict[str, object]], ...]:
    state = evaluation.state
    children: list[tuple[str, str, dict[str, object]]] = [
        ("context", evaluation.context_id, _context_projection(evaluation))
    ]
    children.extend(
        (
            "fact-requirement",
            item.id,
            _requirement_projection(state, item),
        )
        for item in evaluation.requirements
    )
    children.extend(
        (
            "obligation",
            _obligation_child_id(item.id),
            _obligation_projection(state, item),
        )
        for item in evaluation.obligations
    )
    children.extend(
        (
            "coverage-requirement",
            item.requirement_id,
            _coverage_requirement_projection(state, item),
        )
        for item in evaluation.coverage
    )
    children.extend(
        (
            "coverage-certificate",
            item.certificate_id,
            _certificate_projection(state, item),
        )
        for item in evaluation.coverage
        if item.certificate_id is not None
    )
    children.extend(
        (
            "fact-observation",
            value["handle"]["child_id"],
            value,
        )
        for value in _observation_projections(state)
    )
    return tuple(children)


def _obligation_work_handle(
    evaluation: AnalysisEvaluation,
    obligation: object,
) -> dict[str, object]:
    if obligation.kind == "audit-coverage":
        coverage = next(
            item
            for item in evaluation.coverage
            if item.subject == obligation.target
        )
        return _analysis_child_handle(
            evaluation.state.analysis_id,
            "coverage-requirement",
            coverage.requirement_id,
        )
    return _analysis_child_handle(
        evaluation.state.analysis_id,
        "obligation",
        _obligation_child_id(obligation.id),
    )


def _context_projection(
    evaluation: AnalysisEvaluation,
) -> dict[str, object]:
    return {
        "kind": "analysis-context",
        "handle": _analysis_child_handle(
            evaluation.state.analysis_id,
            "context",
            evaluation.context_id,
        ),
        **dict(evaluation.context),
    }


def _requirement_projection(
    state: DomainAnalysisState,
    requirement: object,
) -> dict[str, object]:
    value = dict(requirement.projection)
    context_id = str(value.pop("context_id"))
    return {
        "kind": "fact-requirement",
        "handle": _analysis_child_handle(
            state.analysis_id,
            "fact-requirement",
            requirement.id,
        ),
        **value,
        "context": _analysis_child_handle(
            state.analysis_id,
            "context",
            context_id,
        ),
    }


def _requirement_work(
    state: DomainAnalysisState,
    requirement: object,
) -> dict[str, object]:
    return {
        "requirement": _requirement_projection(state, requirement),
        "prompt": requirement.prompt,
        "dependent_programs": list(requirement.dependent_programs),
    }


def _obligation_projection(
    state: DomainAnalysisState,
    obligation: object,
) -> dict[str, object]:
    value = obligation.as_contract()
    identifier = str(value.pop("id"))
    value["handle"] = _analysis_child_handle(
        state.analysis_id,
        "obligation",
        _obligation_child_id(identifier),
    )
    return value


def _coverage_requirement_projection(
    state: DomainAnalysisState,
    coverage: object,
) -> dict[str, object]:
    value = dict(coverage.requirement)
    value.pop("view_digest")
    return {
        "kind": "coverage-requirement",
        "handle": _analysis_child_handle(
            state.analysis_id,
            "coverage-requirement",
            coverage.requirement_id,
        ),
        **value,
    }


def _certificate_projection(
    state: DomainAnalysisState,
    coverage: object,
) -> dict[str, object]:
    if coverage.certificate is None or coverage.certificate_id is None:
        raise RuntimeError("certificate projection requires a certificate")
    value = dict(coverage.certificate)
    value.pop("attestation_digest")
    requirement_id = str(value.pop("requirement_id"))
    return {
        "kind": "coverage-certificate",
        "handle": _analysis_child_handle(
            state.analysis_id,
            "coverage-certificate",
            coverage.certificate_id,
        ),
        "requirement": _analysis_child_handle(
            state.analysis_id,
            "coverage-requirement",
            requirement_id,
        ),
        **value,
    }


def _observation_projections(
    state: DomainAnalysisState,
) -> list[dict[str, object]]:
    authorizations = _authorization_references(state)
    result = []
    for record in state.fact_observations:
        value = _plain(record)
        identifier = analysis_child_id(value)
        projected = {
            "kind": "fact-observation",
            "handle": _analysis_child_handle(
                state.analysis_id,
                "fact-observation",
                identifier,
            ),
            "requirement": _analysis_child_handle(
                state.analysis_id,
                "fact-requirement",
                str(value["requirement_id"]),
            ),
            "value": value["value"],
            "evidence": value["evidence"],
            "authorization": authorizations[str(value["authorization_id"])],
        }
        if value.get("provider") is not None:
            projected["provider"] = value["provider"]
        result.append(projected)
    return result


def _disposition_projections(
    state: DomainAnalysisState,
) -> list[dict[str, object]]:
    authorizations = _authorization_references(state)
    result = []
    for record in state.dispositions:
        value = _plain(record)
        obligation_id = str(value["obligation_id"])
        result.append(
            {
                "obligation": _analysis_child_handle(
                    state.analysis_id,
                    "obligation",
                    _obligation_child_id(obligation_id),
                ),
                "kind": value["kind"],
                "result": value["result"],
                "rationale": value["rationale"],
                "evidence": value["evidence"],
                "authorization": authorizations[str(value["authorization_id"])],
                "fingerprint": value["fingerprint"],
            }
        )
    return result


def _authorization_references(
    state: DomainAnalysisState,
) -> dict[str, dict[str, object]]:
    return {
        str(value["reference"]["id"]): dict(value["reference"])
        for record in state.authorization_records
        for value in (_plain(record),)
    }


def _plain(value: object) -> dict[str, object]:
    return plain_record(value)


def _analysis_handle(analysis_id: str) -> dict[str, object]:
    return {
        "kind": "analysis-handle",
        "id": analysis_id,
        "schema_version": 7,
    }


def _analysis_child_handle(
    analysis_id: str,
    child_kind: str,
    child_id: str,
) -> dict[str, object]:
    return {
        "kind": "analysis-child-handle",
        "analysis": _analysis_handle(analysis_id),
        "child_kind": child_kind,
        "child_id": child_id,
        "schema_version": 7,
    }


def _obligation_child_id(obligation_id: str) -> str:
    prefix = "obligation:"
    if not obligation_id.startswith(prefix):
        raise RuntimeError("obligation identity has an invalid domain")
    return obligation_id.removeprefix(prefix)
