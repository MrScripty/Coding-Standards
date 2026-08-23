from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApplicabilityFailure:
    code: str
    outcome: str
    message: str
    field: str | None = None
    observed: str | None = None


class ApplicabilityError(Exception):
    def __init__(self, failure: ApplicabilityFailure) -> None:
        super().__init__(failure.message)
        self.failure = failure
