from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IdentityFailure:
    code: str
    message: str


class IdentityError(ValueError):
    def __init__(self, failure: IdentityFailure) -> None:
        self.failure = failure
        super().__init__(f"{failure.code}: {failure.message}")


def invalid(code: str, message: str) -> IdentityError:
    return IdentityError(IdentityFailure(code=code, message=message))


__all__ = ("IdentityError", "IdentityFailure")
