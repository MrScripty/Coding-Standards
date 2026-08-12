from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from .table import (
    ProjectedTableSource,
    parse_projected_table_source,
    project_table_rows,
    read_table_rows,
)


@dataclass(frozen=True, slots=True)
class InclusionCheck:
    id: str
    members: ProjectedTableSource
    container: ProjectedTableSource

    def run(self, context: CheckContext) -> list[Diagnostic]:
        root = context.repo_root
        if not isinstance(root, Path):
            raise TypeError("check context repository root must be a Path")
        member_rows = read_table_rows(
            root,
            self.members.path,
            self.members.header,
            suite=context.suite_id,
            check=self.id,
        )
        container_rows = read_table_rows(
            root,
            self.container.path,
            self.container.header,
            suite=context.suite_id,
            check=self.id,
        )
        members = project_table_rows(member_rows, self.members.projection)
        container = project_table_rows(container_rows, self.container.projection)
        unique_members = set(members)
        unique_container = set(container)
        if len(unique_members) != len(members) or len(unique_container) != len(
            container
        ):
            return [
                Diagnostic(
                    "ASSERT.INCLUSION_DUPLICATE",
                    "invalid",
                    "inclusion projections must contain unique rows",
                    suite=context.suite_id,
                    check=self.id,
                    expected="unique projections",
                    observed=(
                        f"members={len(members)}/{len(unique_members)},"
                        f"container={len(container)}/{len(unique_container)}"
                    ),
                )
            ]
        missing = tuple(sorted(unique_members - unique_container))
        if not missing:
            return []
        return [
            Diagnostic(
                "ASSERT.TABLE_INCLUSION",
                "invalid",
                "container does not contain every declared member",
                suite=context.suite_id,
                check=self.id,
                expected="all members present in container",
                observed=repr(missing),
            )
        ]


def parse_inclusion_check(raw: dict[str, Any], suite_id: str) -> InclusionCheck:
    allowed = {"id", "type", "members", "container"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "inclusion check contains unknown fields",
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
    source_options = {
        "invalid_code": "CONFIG.INCLUSION_COLLECTION",
        "source_name": "inclusion collection",
        "projection_name": "inclusion projection",
        "predicate_name": "inclusion predicate",
    }
    members = parse_projected_table_source(
        raw.get("members"), suite_id, check_id, "members", **source_options
    )
    container = parse_projected_table_source(
        raw.get("container"), suite_id, check_id, "container", **source_options
    )
    if len(members.projection.columns) != len(container.projection.columns):
        raise EngineError(
            Diagnostic(
                "CONFIG.INCLUSION_WIDTH",
                "invalid",
                "inclusion projections must select the same number of columns",
                suite=suite_id,
                check=check_id,
                expected=str(len(members.projection.columns)),
                observed=str(len(container.projection.columns)),
            )
        )
    return InclusionCheck(check_id, members, container)
