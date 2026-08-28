from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

FailureKind = Literal["invalid", "unavailable", "unsupported"]


@dataclass(frozen=True, slots=True)
class AuthorityFailure:
    kind: FailureKind
    code: str
    message: str


class AuthorityError(RuntimeError):
    def __init__(self, failure: AuthorityFailure) -> None:
        self.failure = failure
        super().__init__(f"{failure.code}: {failure.message}")


def invalid(code: str, message: str) -> AuthorityError:
    return AuthorityError(AuthorityFailure("invalid", code, message))


def unavailable(code: str, message: str) -> AuthorityError:
    return AuthorityError(AuthorityFailure("unavailable", code, message))


def unsupported(code: str, message: str) -> AuthorityError:
    return AuthorityError(AuthorityFailure("unsupported", code, message))


__all__ = ("AuthorityError", "AuthorityFailure", "FailureKind")
