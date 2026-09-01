from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError


@dataclass(frozen=True, slots=True)
class Predicate:
    kind: str
    field: str | None = None
    other_field: str | None = None
    values: tuple[str, ...] = ()
    children: tuple["Predicate", ...] = ()

    def evaluate(self, row: dict[str, str]) -> bool:
        if self.kind == "all":
            return all(child.evaluate(row) for child in self.children)
        if self.kind == "any":
            return any(child.evaluate(row) for child in self.children)
        if self.kind == "not":
            return not self.children[0].evaluate(row)
        assert self.field is not None
        observed = row[self.field]
        if self.kind == "eq":
            return observed == self.values[0]
        if self.kind == "ne":
            return observed != self.values[0]
        if self.kind == "in":
            return observed in self.values
        if self.kind == "not_in":
            return observed not in self.values
        if self.kind == "eq_field":
            assert self.other_field is not None
            return observed == row[self.other_field]
        if self.kind == "ne_field":
            assert self.other_field is not None
            return observed != row[self.other_field]
        raise AssertionError(f"unhandled predicate kind: {self.kind}")

    def fields(self) -> set[str]:
        if self.field is not None:
            if self.other_field is not None:
                return {self.field, self.other_field}
            return {self.field}
        return set().union(*(child.fields() for child in self.children))


def parse_predicate(raw: Any, suite: str, check: str) -> Predicate:
    if not isinstance(raw, dict):
        raise EngineError(
            Diagnostic(
                "CONFIG.PREDICATE",
                "invalid",
                "predicate must be a TOML table",
                suite=suite,
                check=check,
            )
        )
    branches = [key for key in ("all", "any", "not") if key in raw]
    if branches:
        if len(branches) != 1 or len(raw) != 1:
            raise EngineError(
                Diagnostic(
                    "CONFIG.PREDICATE_SHAPE",
                    "invalid",
                    "predicate branch must contain exactly one of all, any, or not",
                    suite=suite,
                    check=check,
                )
            )
        kind = branches[0]
        value = raw[kind]
        if kind == "not":
            return Predicate(
                kind="not", children=(parse_predicate(value, suite, check),)
            )
        if not isinstance(value, list) or not value:
            raise EngineError(
                Diagnostic(
                    "CONFIG.PREDICATE_CHILDREN",
                    "invalid",
                    f"{kind} predicate requires a non-empty array",
                    suite=suite,
                    check=check,
                )
            )
        return Predicate(
            kind=kind,
            children=tuple(parse_predicate(child, suite, check) for child in value),
        )

    field = raw.get("field")
    op = raw.get("op")
    if not isinstance(field, str) or not field or op not in {
        "eq",
        "ne",
        "in",
        "not_in",
        "eq_field",
        "ne_field",
    }:
        raise EngineError(
            Diagnostic(
                "CONFIG.PREDICATE_LEAF",
                "invalid",
                "predicate leaf requires field and a supported operator",
                suite=suite,
                check=check,
            )
        )
    if op in {"eq_field", "ne_field"}:
        other_field = raw.get("other_field")
        if (
            set(raw) != {"field", "op", "other_field"}
            or not isinstance(other_field, str)
            or not other_field
        ):
            raise EngineError(
                Diagnostic(
                    "CONFIG.PREDICATE_FIELD_VALUE",
                    "invalid",
                    f"{op} predicate requires one non-empty other_field",
                    suite=suite,
                    check=check,
                )
            )
        return Predicate(kind=op, field=field, other_field=other_field)
    if op in {"eq", "ne"}:
        if set(raw) != {"field", "op", "value"} or not isinstance(
            raw.get("value"), str
        ):
            raise EngineError(
                Diagnostic(
                    "CONFIG.PREDICATE_VALUE",
                    "invalid",
                    f"{op} predicate requires one string value",
                    suite=suite,
                    check=check,
                )
            )
        return Predicate(kind=op, field=field, values=(raw["value"],))
    values = raw.get("values")
    if (
        set(raw) != {"field", "op", "values"}
        or not isinstance(values, list)
        or not values
        or any(not isinstance(value, str) for value in values)
        or len(set(values)) != len(values)
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.PREDICATE_VALUES",
                "invalid",
                f"{op} predicate requires unique string values",
                suite=suite,
                check=check,
            )
        )
    return Predicate(kind=op, field=field, values=tuple(values))
