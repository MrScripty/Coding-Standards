from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnalysisFailure:
    code: str
    outcome: str
    message: str
    path: str | None = None
    field: str | None = None
    observed: str | None = None
    validation_phase: str | None = None
    evidence_reference: str | None = None
    provider_contract: str | None = None
    provider_contract_version: str | None = None
    source_kind: str | None = None
    material_identity: str | None = None
    expected_digest: str | None = None
    observed_digest: str | None = None
    next_action: str | None = None


class AnalysisError(Exception):
    def __init__(self, failure: AnalysisFailure) -> None:
        super().__init__(failure.message)
        self.failure = failure
