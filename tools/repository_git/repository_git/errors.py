from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

FailureKind = Literal["invalid", "unavailable", "unsupported"]


@dataclass(frozen=True, slots=True)
class GitCommandObservation:
    operation: str
    exit_code: int
    reason: str
    stderr_excerpt: str

    def as_contract(self) -> dict[str, object]:
        return {
            "operation": self.operation,
            "exit_code": self.exit_code,
            "reason": self.reason,
            "stderr_excerpt": self.stderr_excerpt,
        }


@dataclass(frozen=True, slots=True)
class GitRepositoryFailure:
    kind: FailureKind
    code: str
    message: str
    command: GitCommandObservation | None = None


class GitRepositoryError(RuntimeError):
    def __init__(self, failure: GitRepositoryFailure) -> None:
        self.failure = failure
        super().__init__(f"{failure.code}: {failure.message}")


def invalid(code: str, message: str) -> GitRepositoryError:
    return GitRepositoryError(GitRepositoryFailure("invalid", code, message))


def unavailable(code: str, message: str) -> GitRepositoryError:
    return GitRepositoryError(GitRepositoryFailure("unavailable", code, message))


def unsupported(code: str, message: str) -> GitRepositoryError:
    return GitRepositoryError(GitRepositoryFailure("unsupported", code, message))


__all__ = (
    "FailureKind",
    "GitCommandObservation",
    "GitRepositoryError",
    "GitRepositoryFailure",
)
