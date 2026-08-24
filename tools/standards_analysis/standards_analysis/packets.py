from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from .changes import ChangedPolicyUnit, ClassifiedChange, ReviewScope
from .coverage import CoverageAttestation
from .errors import AnalysisError, AnalysisFailure
from .obligations import ApplicabilityQuestion, DecisionFingerprint, Obligation
from .serialization import canonical_json_bytes, identity
from .reading import ReadingPlanEntry
from .snapshots import AnalysisVersions


PACKET_DOMAIN = "coding-standards:packet:v3"
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
SNAPSHOT_PATTERN = re.compile(r"^snapshot:sha256:[0-9a-f]{64}$")


def _error(code: str, message: str, *, observed: str | None = None) -> AnalysisError:
    return AnalysisError(
        AnalysisFailure(code, "invalid", message, observed=observed)
    )


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {str(key): _freeze(item) for key, item in value.items()}
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


def _snapshot(value: Mapping[str, object], field: str) -> Mapping[str, object]:
    copied = dict(value)
    if (
        set(copied) != {"kind", "id", "schema_version"}
        or copied.get("kind") != "snapshot-handle"
        or copied.get("schema_version") != 1
        or not isinstance(copied.get("id"), str)
        or SNAPSHOT_PATTERN.fullmatch(str(copied["id"])) is None
    ):
        raise _error(
            "PACKET.SNAPSHOT_HANDLE",
            "packet snapshot handles must be canonical schema-version-1 handles",
            observed=field,
        )
    return _freeze(copied)  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class NextOperation:
    operation: str
    request_kind: str
    target: str | None = None
    obligation_id: str | None = None

    def as_contract(self) -> dict[str, object]:
        value: dict[str, object] = {
            "operation": self.operation,
            "request_kind": self.request_kind,
        }
        if self.target is not None:
            value["target"] = self.target
        if self.obligation_id is not None:
            value["obligation_id"] = self.obligation_id
        return value


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    id: str
    digest: str
    provider_contract_version: str

    def __post_init__(self) -> None:
        if (
            not self.id
            or not self.provider_contract_version
            or DIGEST_PATTERN.fullmatch(self.digest) is None
        ):
            raise _error(
                "SUBMISSION.EVIDENCE",
                "evidence requires an ID, provider contract, and SHA-256 digest",
                observed=self.id,
            )

    def as_contract(self) -> dict[str, str]:
        return {
            "id": self.id,
            "digest": self.digest,
            "provider_contract_version": self.provider_contract_version,
        }


@dataclass(frozen=True, slots=True)
class FactAnswerSubmission:
    question_id: str
    answer: Mapping[str, object]
    evidence: tuple[EvidenceReference, ...]
    kind: str = "fact-answer"

    def __post_init__(self) -> None:
        object.__setattr__(self, "answer", _freeze(self.answer))
        _require_evidence(self.evidence)

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "question_id": self.question_id,
            "answer": _thaw(self.answer),
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
        if self.result not in {
            "updated",
            "reviewed-no-change",
            "not-applicable",
            "blocked",
        } or not self.rationale:
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
        if self.result not in {
            "confirmed",
            "resolved-no-impact",
            "requires-change",
            "blocked",
        } or not self.rationale:
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
    FactAnswerSubmission
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
class PendingPacket:
    id: str
    base_snapshot: Mapping[str, object]
    proposed_snapshot: Mapping[str, object]
    changes: tuple[ClassifiedChange, ...]
    obligations: tuple[Obligation, ...]
    questions: tuple[ApplicabilityQuestion, ...]
    reading_plan: tuple[ReadingPlanEntry, ...]
    next_operations: tuple[NextOperation, ...]
    provenance: AnalysisVersions
    summary: str = ""

    @property
    def changed_units(self) -> tuple[ChangedPolicyUnit, ...]:
        return tuple(
            unit for change in self.changes for unit in change.changed_units
        )

    @property
    def handle(self) -> dict[str, object]:
        return {
            "kind": "packet-handle",
            "id": self.id,
            "base_snapshot": _thaw(self.base_snapshot),
            "proposed_snapshot": _thaw(self.proposed_snapshot),
            "schema_version": 3,
        }

    def as_contract(self) -> dict[str, object]:
        value: dict[str, object] = {
            "kind": "pending-packet",
            "handle": self.handle,
            "state": "needs-action",
            "changes": [item.descriptor.as_contract() for item in self.changes],
            "changed_units": [item.as_contract() for item in self.changed_units],
            "obligations": [item.as_contract() for item in self.obligations],
            "questions": [item.as_contract() for item in self.questions],
            "reading_plan": [item.as_contract() for item in self.reading_plan],
            "next_operations": [
                item.as_contract() for item in self.next_operations
            ],
            "provenance": self.provenance.as_contract(),
        }
        if self.summary:
            value["summary"] = self.summary
        return value


def build_pending_packet(
    base_snapshot: Mapping[str, object],
    proposed_snapshot: Mapping[str, object],
    changes: Iterable[ClassifiedChange],
    obligations: Iterable[Obligation],
    questions: Iterable[ApplicabilityQuestion] = (),
    reading_plan: Iterable[ReadingPlanEntry] = (),
    *,
    provenance: AnalysisVersions | None = None,
    summary: str = "",
) -> PendingPacket:
    base = _snapshot(base_snapshot, "base_snapshot")
    proposed = _snapshot(proposed_snapshot, "proposed_snapshot")
    selected_changes = tuple(
        sorted(
            changes,
            key=lambda item: canonical_json_bytes(item.descriptor.as_contract()),
        )
    )
    selected_obligations = tuple(sorted(obligations, key=lambda item: item.id))
    selected_questions = tuple(sorted(questions, key=lambda item: item.id))
    selected_reading = tuple(reading_plan)
    _unique(
        "PACKET.DUPLICATE_OBLIGATION",
        (item.id for item in selected_obligations),
    )
    _unique("PACKET.DUPLICATE_QUESTION", (item.id for item in selected_questions))
    if not selected_obligations or all(
        item.state == "resolved" for item in selected_obligations
    ):
        raise _error(
            "PACKET.NO_OUTSTANDING_WORK",
            "a pending packet requires at least one unresolved obligation",
        )
    versions = provenance or AnalysisVersions()
    operations = _next_operations(selected_obligations, selected_questions)
    projection = {
        "handle": {
            "base_snapshot": _thaw(base),
            "proposed_snapshot": _thaw(proposed),
        },
        "changes": [item.descriptor.as_contract() for item in selected_changes],
        "changed_units": [
            unit.as_contract()
            for change in selected_changes
            for unit in change.changed_units
        ],
        "obligations": [item.as_contract() for item in selected_obligations],
        "questions": [item.as_contract() for item in selected_questions],
        "reading_plan": [item.as_contract() for item in selected_reading],
        "provenance": _identity_provenance(versions),
    }
    return PendingPacket(
        identity(PACKET_DOMAIN, "packet", projection),
        base,
        proposed,
        selected_changes,
        selected_obligations,
        selected_questions,
        selected_reading,
        operations,
        versions,
        summary,
    )


def _unique(code: str, values: Iterable[str]) -> None:
    selected = tuple(values)
    if len(set(selected)) != len(selected):
        duplicate = next(value for value in selected if selected.count(value) > 1)
        raise _error(code, "packet work identities must be unique", observed=duplicate)


def _next_operations(
    obligations: tuple[Obligation, ...],
    questions: tuple[ApplicabilityQuestion, ...],
) -> tuple[NextOperation, ...]:
    operations: list[NextOperation] = []
    for question in questions:
        if question.state == "required":
            operations.append(NextOperation("resolve", "fact-answer", question.id))
    for obligation in obligations:
        if obligation.state != "required":
            continue
        for submission in obligation.permitted_submissions:
            if submission == "fact-answer" and questions:
                continue
            operations.append(
                NextOperation(
                    "resolve",
                    submission,
                    obligation.target,
                    obligation.id,
                )
            )
    return tuple(
        sorted(
            set(operations),
            key=lambda item: (
                item.operation,
                item.request_kind,
                item.target or "",
                item.obligation_id or "",
            ),
        )
    )


def _identity_provenance(versions: AnalysisVersions) -> dict[str, object]:
    value = versions.as_contract()
    return {
        "analysis_contract_version": value["analysis_contract_version"],
        "packet_schema_version": value["packet_schema_version"],
        "interface_schema_version": value["interface_schema_version"],
        "applicability_version": value["applicability_version"],
        "metadata_api_version": value["metadata_api_version"],
        "graph_engine_contract_version": value["graph_engine_contract_version"],
        "parser_versions": value["parser_versions"],
        "evidence_provider_contract_versions": value[
            "evidence_provider_contract_versions"
        ],
    }


__all__ = (
    "ConsumerDispositionSubmission",
    "CoverageAttestationSubmission",
    "EvidenceReference",
    "FactAnswerSubmission",
    "ImpactDispositionSubmission",
    "NextOperation",
    "PACKET_DOMAIN",
    "PendingPacket",
    "ReadingPlanEntry",
    "Submission",
    "build_pending_packet",
)
