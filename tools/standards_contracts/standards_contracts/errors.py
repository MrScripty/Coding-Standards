from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ContractFailure:
    outcome: str
    code: str
    message: str
    definition: str | None = None
    instance_pointer: str = ""
    schema_pointer: str = ""
    keyword: str | None = None
    causes: tuple[ContractFailure, ...] = ()


class ContractError(ValueError):
    def __init__(self, failure: ContractFailure) -> None:
        self.failure = failure
        super().__init__(f"{failure.code}: {failure.message}")


def failure(
    code: str,
    message: str,
    *,
    outcome: str = "invalid",
    definition: str | None = None,
    schema_pointer: str = "",
) -> ContractError:
    return ContractError(
        ContractFailure(
            outcome=outcome,
            code=code,
            message=message,
            definition=definition,
            schema_pointer=schema_pointer,
        )
    )


__all__ = ("ContractError", "ContractFailure")
