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


class AnalysisError(Exception):
    def __init__(self, failure: AnalysisFailure) -> None:
        super().__init__(failure.message)
        self.failure = failure
