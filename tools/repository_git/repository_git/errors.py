from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

FailureKind = Literal["invalid", "unavailable", "unsupported"]


@dataclass(frozen=True, slots=True)
class GitRepositoryFailure:
    kind: FailureKind
    code: str
    message: str


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
    "GitRepositoryError",
    "GitRepositoryFailure",
)
