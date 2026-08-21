from __future__ import annotations

from typing import Literal, cast

from ..diagnostics import Diagnostic, EngineError


MatchCase = Literal["sensitive", "insensitive"]


def parse_match_case(
    value: object,
    *,
    suite: str,
    check: str,
) -> MatchCase:
    if value not in ("sensitive", "insensitive"):
        raise EngineError(
            Diagnostic(
                "CONFIG.MATCH_CASE",
                "invalid",
                "match_case must be 'sensitive' or 'insensitive'",
                suite=suite,
                check=check,
                field="match_case",
                observed=str(value),
            )
        )
    return cast(MatchCase, value)


def literal_key(value: str, match_case: MatchCase) -> str:
    return value if match_case == "sensitive" else value.casefold()


def validate_literal_sets(
    required: tuple[str, ...],
    prohibited: tuple[str, ...],
    match_case: MatchCase,
    *,
    suite: str,
    check: str,
) -> None:
    for field, values in (("required", required), ("prohibited", prohibited)):
        keys = tuple(literal_key(item, match_case) for item in values)
        if len(set(keys)) != len(keys):
            raise EngineError(
                Diagnostic(
                    "CONFIG.DUPLICATE_VALUE",
                    "invalid",
                    "field contains duplicate values under selected case matching",
                    suite=suite,
                    check=check,
                    field=field,
                )
            )

    prohibited_keys = {literal_key(item, match_case) for item in prohibited}
    overlap = tuple(
        item
        for item in required
        if literal_key(item, match_case) in prohibited_keys
    )
    if overlap:
        raise EngineError(
            Diagnostic(
                "CONFIG.CONTRADICTORY_TEXT",
                "invalid",
                "a literal cannot be both required and prohibited under selected case matching",
                suite=suite,
                check=check,
                observed=sorted(overlap)[0],
            )
        )
