from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from .predicates import parse_predicate
from .table import Projection, project_table_rows, read_table_rows


def _strings(value: Any, field: str, suite: str, check: str) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.STRING_LIST",
                "invalid",
                "field must contain unique non-empty strings",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return tuple(value)


@dataclass(frozen=True, slots=True)
class RelationSide:
    path: str
    header: tuple[str, ...]
    projection: Projection


@dataclass(frozen=True, slots=True)
class RelationCheck:
    id: str
    mode: str
    left: RelationSide
    right: RelationSide

    def run(self, context: CheckContext) -> list[Diagnostic]:
        root = context.repo_root
        if not isinstance(root, Path):
            raise TypeError("check context repository root must be a Path")
        left_rows = read_table_rows(
            root,
            self.left.path,
            self.left.header,
            suite=context.suite_id,
            check=self.id,
        )
        right_rows = read_table_rows(
            root,
            self.right.path,
            self.right.header,
            suite=context.suite_id,
            check=self.id,
        )
        left = project_table_rows(left_rows, self.left.projection)
        right = project_table_rows(right_rows, self.right.projection)
        if self.mode == "set":
            if len(set(left)) != len(left) or len(set(right)) != len(right):
                return [
                    Diagnostic(
                        "ASSERT.RELATION_DUPLICATE",
                        "invalid",
                        "set relation projections must contain unique rows",
                        suite=context.suite_id,
                        check=self.id,
                        expected="unique projections",
                        observed=f"left={len(left)}/{len(set(left))},right={len(right)}/{len(set(right))}",
                    )
                ]
            left = tuple(sorted(left))
            right = tuple(sorted(right))
        if left == right:
            return []
        return [
            Diagnostic(
                "ASSERT.TABLE_RELATION",
                "invalid",
                "table projections do not satisfy the declared relation",
                suite=context.suite_id,
                check=self.id,
                expected=repr(left),
                observed=repr(right),
            )
        ]


def _side(raw: Any, suite: str, check: str, label: str) -> RelationSide:
    if not isinstance(raw, dict):
        raise EngineError(
            Diagnostic(
                "CONFIG.RELATION_SIDE",
                "invalid",
                "relation side must be a TOML table",
                suite=suite,
                check=check,
                field=label,
            )
        )
    allowed = {"path", "header", "columns", "order", "where", "split"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "relation side contains unknown fields",
                suite=suite,
                check=check,
                field=f"{label}.{sorted(unknown)[0]}",
            )
        )
    path = raw.get("path")
    if not isinstance(path, str) or not path:
        raise EngineError(
            Diagnostic(
                "CONFIG.PATH",
                "invalid",
                "relation side path must be a non-empty string",
                suite=suite,
                check=check,
                field=label,
            )
        )
    header = _strings(raw.get("header"), f"{label}.header", suite, check)
    columns = _strings(raw.get("columns"), f"{label}.columns", suite, check)
    unknown_columns = set(columns) - set(header)
    if unknown_columns:
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_COLUMN",
                "invalid",
                "relation projection references an unknown column",
                suite=suite,
                check=check,
                field=sorted(unknown_columns)[0],
            )
        )
    order = raw.get("order")
    if order not in {"source", "lexical"}:
        raise EngineError(
            Diagnostic(
                "CONFIG.PROJECTION_ORDER",
                "invalid",
                "relation projection order must be source or lexical",
                suite=suite,
                check=check,
                field=label,
                observed=str(order),
            )
        )
    where = None
    if "where" in raw:
        where = parse_predicate(raw["where"], suite, check)
        unknown_fields = where.fields() - set(header)
        if unknown_fields:
            raise EngineError(
                Diagnostic(
                    "CONFIG.TABLE_COLUMN",
                    "invalid",
                    "relation predicate references an unknown column",
                    suite=suite,
                    check=check,
                    field=sorted(unknown_fields)[0],
                )
            )
    split_field = None
    split_delimiter = None
    if "split" in raw:
        split = raw["split"]
        if (
            not isinstance(split, dict)
            or set(split) != {"field", "delimiter"}
            or split.get("field") not in columns
            or not isinstance(split.get("delimiter"), str)
            or not split["delimiter"]
        ):
            raise EngineError(
                Diagnostic(
                    "CONFIG.PROJECTION_SPLIT",
                    "invalid",
                    "split requires one selected field and a non-empty delimiter",
                    suite=suite,
                    check=check,
                    field=label,
                )
            )
        split_field = split["field"]
        split_delimiter = split["delimiter"]
    projection = Projection(
        columns,
        order,
        (),
        where,
        split_field,
        split_delimiter,
    )
    return RelationSide(path, header, projection)


def parse_relation_check(raw: dict[str, Any], suite_id: str) -> RelationCheck:
    allowed = {"id", "type", "mode", "left", "right"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "relation check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    if not isinstance(check_id, str) or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    mode = raw.get("mode")
    if mode not in {"ordered", "set"}:
        raise EngineError(
            Diagnostic(
                "CONFIG.RELATION_MODE",
                "invalid",
                "relation mode must be ordered or set",
                suite=suite_id,
                check=check_id,
                observed=str(mode),
            )
        )
    left = _side(raw.get("left"), suite_id, check_id, "left")
    right = _side(raw.get("right"), suite_id, check_id, "right")
    if len(left.projection.columns) != len(right.projection.columns):
        raise EngineError(
            Diagnostic(
                "CONFIG.RELATION_WIDTH",
                "invalid",
                "relation projections must select the same number of columns",
                suite=suite_id,
                check=check_id,
                expected=str(len(left.projection.columns)),
                observed=str(len(right.projection.columns)),
            )
        )
    return RelationCheck(check_id, mode, left, right)
