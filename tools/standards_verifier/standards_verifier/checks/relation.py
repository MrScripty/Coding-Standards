from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs
from .table import (
    ProjectedTableSource,
    parse_projected_table_source,
    read_projected_table_rows,
)


@dataclass(frozen=True, slots=True)
class RelationCheck:
    id: str
    mode: str
    left: ProjectedTableSource
    right: ProjectedTableSource

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        return (
            *present_inputs("left", self.left.path),
            *present_inputs("right", self.right.path),
        )

    def run(self, context: CheckContext) -> list[Diagnostic]:
        root = context.repo_root
        if not isinstance(root, Path):
            raise TypeError("check context repository root must be a Path")
        left = read_projected_table_rows(context, self.id, self.left)
        right = read_projected_table_rows(context, self.id, self.right)
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
    source_options = {
        "invalid_code": "CONFIG.RELATION_SIDE",
        "source_name": "relation side",
        "projection_name": "relation projection",
        "predicate_name": "relation predicate",
    }
    left = parse_projected_table_source(
        raw.get("left"), suite_id, check_id, "left", **source_options
    )
    right = parse_projected_table_source(
        raw.get("right"), suite_id, check_id, "right", **source_options
    )
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
