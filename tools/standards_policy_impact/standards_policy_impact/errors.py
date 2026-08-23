from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PolicyImpactFailure:
    code: str
    outcome: str
    message: str
    path: str | None = None
    field: str | None = None
    observed: str | None = None


class PolicyImpactError(ValueError):
    def __init__(self, failure: PolicyImpactFailure) -> None:
        super().__init__(failure.message)
        self.failure = failure
