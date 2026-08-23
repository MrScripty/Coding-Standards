from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetadataFailure:
    code: str
    outcome: str
    message: str
    path: str | None = None
    row: int | None = None
    field: str | None = None
    expected: str | None = None
    observed: str | None = None


class MetadataError(Exception):
    def __init__(self, failure: MetadataFailure) -> None:
        super().__init__(failure.message)
        self.failure = failure
