from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from .changes import ChangedPolicyUnit, ClassifiedChange
from .coverage import ConsumerCoverageCertificate, CoverageAttestation
from .errors import AnalysisError, AnalysisFailure
from .facts import (
    AnalysisContext,
    AuthorizationReference,
    EvidenceReference,
    FactObservation,
    FactRequirement,
)
from .obligations import DecisionFingerprint, Obligation
from .reading import ReadingPlanEntry
from .serialization import canonical_json_bytes
from .snapshots import AnalysisVersions


def _error(
    code: str,
    message: str,
    *,
    outcome: str = "invalid",
    observed: str | None = None,
) -> AnalysisError:
    return AnalysisError(AnalysisFailure(code, outcome, message, observed=observed))


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {str(key): _freeze(item) for key, item in sorted(value.items())}
        )
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class NextOperation:
    operation: str
    request_kind: str
    target: str | None = None
    obligation_id: str | None = None
    requirement_id: str | None = None

    def as_contract(self) -> dict[str, object]:
        value: dict[str, object] = {
            "operation": self.operation,
            "request_kind": self.request_kind,
        }
        if self.target is not None:
            value["target"] = self.target
        if self.obligation_id is not None:
            value["obligation_id"] = self.obligation_id
        if self.requirement_id is not None:
            value["requirement_id"] = self.requirement_id
        return value


@dataclass(frozen=True, slots=True)
class ProvideFactSubmission:
    requirement: Mapping[str, object]
    value: Mapping[str, object]
    evidence: tuple[EvidenceReference, ...]
    kind: str = "provide-fact"

    def __post_init__(self) -> None:
        selected = dict(self.requirement)
        if (
            set(selected) != {"kind", "id", "schema_version"}
            or selected.get("kind") != "fact-requirement-handle"
            or selected.get("schema_version") != 1
            or not isinstance(selected.get("id"), str)
        ):
            raise _error(
                "SUBMISSION.FACT_REQUIREMENT",
                "provide-fact requires one canonical requirement handle",
            )
        object.__setattr__(self, "requirement", _freeze(selected))
        object.__setattr__(self, "value", _freeze(self.value))
        _require_evidence(self.evidence)

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "requirement": _thaw(self.requirement),
            "value": _thaw(self.value),
            "evidence": [item.as_contract() for item in self.evidence],
        }


@dataclass(frozen=True, slots=True)
class ConsumerDispositionSubmission:
    obligation_id: str
    result: str
    rationale: str
    evidence: tuple[EvidenceReference, ...]
    fingerprint: DecisionFingerprint
    kind: str = "consumer-disposition"

    def __post_init__(self) -> None:
        if (
            self.result
            not in {
                "updated",
                "reviewed-no-change",
                "not-applicable",
                "blocked",
            }
            or not self.rationale
        ):
            raise _error(
                "SUBMISSION.CONSUMER_DISPOSITION",
                "consumer disposition result and rationale are invalid",
                observed=self.result,
            )
        _require_evidence(self.evidence)

    def as_contract(self) -> dict[str, object]:
        return _disposition_contract(self)


@dataclass(frozen=True, slots=True)
class ImpactDispositionSubmission:
    obligation_id: str
    result: str
    rationale: str
    evidence: tuple[EvidenceReference, ...]
    fingerprint: DecisionFingerprint
    kind: str = "impact-disposition"

    def __post_init__(self) -> None:
        if (
            self.result
            not in {
                "confirmed",
                "resolved-no-impact",
                "requires-change",
                "blocked",
            }
            or not self.rationale
        ):
            raise _error(
                "SUBMISSION.IMPACT_DISPOSITION",
                "impact disposition result and rationale are invalid",
                observed=self.result,
            )
        _require_evidence(self.evidence)

    def as_contract(self) -> dict[str, object]:
        return _disposition_contract(self)


@dataclass(frozen=True, slots=True)
class CoverageAttestationSubmission:
    obligation_id: str
    attestation: CoverageAttestation
    kind: str = "coverage-attestation"

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "obligation_id": self.obligation_id,
            "attestation": self.attestation.as_projection(),
        }


Submission = (
    ProvideFactSubmission
    | ConsumerDispositionSubmission
    | ImpactDispositionSubmission
    | CoverageAttestationSubmission
)


def _require_evidence(evidence: tuple[EvidenceReference, ...]) -> None:
    if not evidence:
        raise _error(
            "SUBMISSION.EVIDENCE_REQUIRED",
            "a review submission requires at least one evidence reference",
        )
    identities = [item.id for item in evidence]
    if len(set(identities)) != len(identities):
        raise _error(
            "SUBMISSION.DUPLICATE_EVIDENCE",
            "evidence references must have unique identities",
            observed=sorted(identities)[0],
        )


def _disposition_contract(
    value: ConsumerDispositionSubmission | ImpactDispositionSubmission,
) -> dict[str, object]:
    return {
        "kind": value.kind,
        "obligation_id": value.obligation_id,
        "result": value.result,
        "rationale": value.rationale,
        "evidence": [item.as_contract() for item in value.evidence],
        "fingerprint": value.fingerprint.as_contract(),
    }


@dataclass(frozen=True, slots=True)
class DispositionRecord:
    obligation_id: str
    kind: str
    result: str
    rationale: str
    evidence: tuple[EvidenceReference, ...]
    authorization: AuthorizationReference
    fingerprint: DecisionFingerprint

    def as_contract(self) -> dict[str, object]:
        return {
            "obligation_id": self.obligation_id,
            "kind": self.kind,
            "result": self.result,
            "rationale": self.rationale,
            "evidence": [item.as_contract() for item in self.evidence],
            "authorization": self.authorization.as_contract(),
            "fingerprint": self.fingerprint.as_contract(),
        }


@dataclass(frozen=True, slots=True)
class CoverageDecision:
    attestation: CoverageAttestation
    authorization: AuthorizationReference

    def as_contract(self) -> dict[str, object]:
        return {
            "attestation": self.attestation.as_projection(),
            "authorization": self.authorization.as_contract(),
        }


@dataclass(frozen=True, slots=True)
class PendingResult:
    analysis: Mapping[str, object]
    context: AnalysisContext
    changes: tuple[ClassifiedChange, ...]
    obligations: tuple[Obligation, ...]
    fact_requirements: tuple[FactRequirement, ...]
    reading_plan: tuple[ReadingPlanEntry, ...]
    next_operations: tuple[NextOperation, ...]
    provenance: AnalysisVersions
    summary: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "analysis", _freeze(self.analysis))

    @property
    def id(self) -> str:
        return str(self.analysis["id"])

    @property
    def handle(self) -> dict[str, object]:
        return _thaw(self.analysis)  # type: ignore[return-value]

    @property
    def changed_units(self) -> tuple[ChangedPolicyUnit, ...]:
        return tuple(unit for change in self.changes for unit in change.changed_units)

    def as_contract(self) -> dict[str, object]:
        value: dict[str, object] = {
            "kind": "pending-result",
            "handle": self.handle,
            "status": "needs-action",
            "context": self.context.as_contract(),
            "changes": [item.descriptor.as_contract() for item in self.changes],
            "changed_units": [item.as_contract() for item in self.changed_units],
            "obligations": [item.as_contract() for item in self.obligations],
            "fact_requirements": [
                item.as_contract() for item in self.fact_requirements
            ],
            "reading_plan": [item.as_contract() for item in self.reading_plan],
            "next_operations": [item.as_contract() for item in self.next_operations],
            "provenance": self.provenance.as_contract(),
        }
        if self.summary:
            value["summary"] = self.summary
        return value


@dataclass(frozen=True, slots=True)
class CompleteResult:
    analysis: Mapping[str, object]
    base_snapshot: Mapping[str, object]
    proposed_snapshot: Mapping[str, object]
    context: AnalysisContext
    changes: tuple[ClassifiedChange, ...]
    coverage_certificates: tuple[ConsumerCoverageCertificate, ...]
    fact_observations: tuple[FactObservation, ...]
    dispositions: tuple[DispositionRecord, ...]
    reading_plan: tuple[ReadingPlanEntry, ...]
    completion: Mapping[str, object]
    provenance: AnalysisVersions
    summary: str = ""

    def __post_init__(self) -> None:
        for field in ("analysis", "base_snapshot", "proposed_snapshot", "completion"):
            object.__setattr__(self, field, _freeze(getattr(self, field)))

    @property
    def id(self) -> str:
        return str(self.analysis["id"])

    @property
    def handle(self) -> dict[str, object]:
        return _thaw(self.analysis)  # type: ignore[return-value]

    def as_contract(self) -> dict[str, object]:
        value: dict[str, object] = {
            "kind": "complete-result",
            "handle": self.handle,
            "base_snapshot": _thaw(self.base_snapshot),
            "proposed_snapshot": _thaw(self.proposed_snapshot),
            "status": "complete",
            "context": self.context.as_contract(),
            "changes": [item.descriptor.as_contract() for item in self.changes],
            "changed_units": [
                unit.as_contract()
                for change in self.changes
                for unit in change.changed_units
            ],
            "coverage_certificates": [
                item.as_projection()["handle"] for item in self.coverage_certificates
            ],
            "fact_observations": [
                item.as_contract() for item in self.fact_observations
            ],
            "dispositions": [item.as_contract() for item in self.dispositions],
            "reading_plan": [item.as_contract() for item in self.reading_plan],
            "completion": _thaw(self.completion),
            "provenance": self.provenance.as_contract(),
        }
        if self.summary:
            value["summary"] = self.summary
        return value


AnalysisResult = PendingResult | CompleteResult


def build_pending_result(
    analysis: Mapping[str, object],
    changes: Iterable[ClassifiedChange],
    obligations: Iterable[Obligation],
    fact_requirements: Iterable[FactRequirement],
    reading_plan: Iterable[ReadingPlanEntry],
    *,
    context: AnalysisContext,
    provenance: AnalysisVersions | None = None,
    summary: str = "",
) -> PendingResult:
    selected_changes = tuple(
        sorted(
            changes,
            key=lambda item: canonical_json_bytes(item.descriptor.as_contract()),
        )
    )
    selected_obligations = tuple(sorted(obligations, key=lambda item: item.id))
    selected_requirements = tuple(sorted(fact_requirements, key=lambda item: item.id))
    _unique(
        "RESULT.DUPLICATE_OBLIGATION",
        (item.id for item in selected_obligations),
    )
    _unique(
        "RESULT.DUPLICATE_FACT_REQUIREMENT",
        (item.id for item in selected_requirements),
    )
    if not selected_requirements and (
        not selected_obligations
        or all(item.state == "resolved" for item in selected_obligations)
    ):
        raise _error(
            "RESULT.NO_OUTSTANDING_WORK",
            "a pending result requires unresolved work",
        )
    return PendingResult(
        analysis,
        context,
        selected_changes,
        selected_obligations,
        selected_requirements,
        tuple(reading_plan),
        _next_operations(selected_obligations, selected_requirements),
        provenance or AnalysisVersions(),
        summary,
    )


def _unique(code: str, values: Iterable[str]) -> None:
    selected = tuple(values)
    if len(set(selected)) != len(selected):
        duplicate = next(value for value in selected if selected.count(value) > 1)
        raise _error(code, "result work identities must be unique", observed=duplicate)


def _next_operations(
    obligations: tuple[Obligation, ...],
    requirements: tuple[FactRequirement, ...],
) -> tuple[NextOperation, ...]:
    operations = [
        NextOperation(
            "resolve",
            "provide-fact",
            requirement.fact,
            requirement_id=requirement.id,
        )
        for requirement in requirements
    ]
    operations.extend(
        NextOperation(
            "resolve",
            submission,
            obligation.target,
            obligation.id,
        )
        for obligation in obligations
        if obligation.state == "required"
        for submission in obligation.permitted_submissions
    )
    return tuple(
        sorted(
            set(operations),
            key=lambda item: (
                item.operation,
                item.request_kind,
                item.target or "",
                item.obligation_id or "",
                item.requirement_id or "",
            ),
        )
    )


__all__ = (
    "AnalysisResult",
    "CompleteResult",
    "ConsumerDispositionSubmission",
    "CoverageAttestationSubmission",
    "CoverageDecision",
    "DispositionRecord",
    "ImpactDispositionSubmission",
    "NextOperation",
    "PendingResult",
    "ProvideFactSubmission",
    "Submission",
    "build_pending_result",
)
