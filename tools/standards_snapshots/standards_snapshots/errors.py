from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

FailureKind = Literal["invalid", "unavailable", "unsupported"]


@dataclass(frozen=True, slots=True)
class SnapshotFailure:
    kind: FailureKind
    code: str
    message: str


class SnapshotError(RuntimeError):
    def __init__(self, failure: SnapshotFailure) -> None:
        self.failure = failure
        super().__init__(f"{failure.code}: {failure.message}")


def invalid(code: str, message: str) -> SnapshotError:
    return SnapshotError(SnapshotFailure("invalid", code, message))


def unavailable(code: str, message: str) -> SnapshotError:
    return SnapshotError(SnapshotFailure("unavailable", code, message))


def unsupported(code: str, message: str) -> SnapshotError:
    return SnapshotError(SnapshotFailure("unsupported", code, message))


__all__ = ("FailureKind", "SnapshotError", "SnapshotFailure")
