from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file
from .markdown_links import local_markdown_targets
from .table import (
    ProjectedTableSource,
    parse_projected_table_source,
    project_table_rows,
    read_table_rows,
)


@dataclass(frozen=True, slots=True)
class MarkdownLinkCoverageCheck:
    id: str
    path: str
    members: ProjectedTableSource

    def run(self, context: CheckContext) -> list[Diagnostic]:
        rows = read_table_rows(
            context.repo_root,
            self.members.path,
            self.members.header,
            suite=context.suite_id,
            check=self.id,
        )
        projected = project_table_rows(rows, self.members.projection)
        members = tuple(value for (value,) in projected)
        if not members:
            return [
                Diagnostic(
                    "ASSERT.MARKDOWN_LINK_COVERAGE_EMPTY",
                    "invalid",
                    "Markdown link coverage requires at least one member",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.members.path,
                    field="members",
                )
            ]
        if any(not member for member in members):
            return [
                Diagnostic(
                    "ASSERT.MARKDOWN_LINK_COVERAGE_MEMBER_EMPTY",
                    "invalid",
                    "Markdown link coverage members must be non-empty",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.members.path,
                    field="members",
                )
            ]
        if len(set(members)) != len(members):
            return [
                Diagnostic(
                    "ASSERT.MARKDOWN_LINK_COVERAGE_DUPLICATE",
                    "invalid",
                    "Markdown link coverage members must be unique",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.members.path,
                    field="members",
                    expected="unique members",
                    observed=f"{len(members)}/{len(set(members))}",
                )
            ]

        root = context.repo_root.resolve()
        normalized_members = []
        for member in members:
            target = contained_file(
                root,
                member,
                suite=context.suite_id,
                check=self.id,
            )
            normalized_members.append(target.relative_to(root).as_posix())
        if len(set(normalized_members)) != len(normalized_members):
            return [
                Diagnostic(
                    "ASSERT.MARKDOWN_LINK_COVERAGE_DUPLICATE",
                    "invalid",
                    "Markdown link coverage members must resolve uniquely",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.members.path,
                    field="members",
                    expected="unique resolved members",
                    observed=(
                        f"{len(normalized_members)}/{len(set(normalized_members))}"
                    ),
                )
            ]

        targets = {
            target.repository_path
            for target in local_markdown_targets(context, self.id, self.path)
        }
        return [
            Diagnostic(
                "ASSERT.MARKDOWN_LINK_COVERAGE_MISSING",
                "invalid",
                "projected member is not a local inline Markdown link target",
                suite=context.suite_id,
                check=self.id,
                path=self.path,
                field="members",
                expected=member,
                observed="absent",
            )
            for member in normalized_members
            if member not in targets
        ]


def parse_markdown_link_coverage_check(
    raw: dict[str, Any], suite_id: str
) -> MarkdownLinkCoverageCheck:
    allowed = {"id", "type", "path", "members"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "markdown_link_coverage check contains unknown fields",
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
    path = raw.get("path")
    if not isinstance(path, str) or not path:
        raise EngineError(
            Diagnostic(
                "CONFIG.PATH",
                "invalid",
                "Markdown source path must be a non-empty string",
                suite=suite_id,
                check=check_id,
                field="path",
            )
        )
    members = parse_projected_table_source(
        raw.get("members"),
        suite_id,
        check_id,
        "members",
        invalid_code="CONFIG.MARKDOWN_LINK_COVERAGE_MEMBERS",
        source_name="Markdown link coverage members",
        projection_name="Markdown link coverage member projection",
        predicate_name="Markdown link coverage member predicate",
    )
    if len(members.projection.columns) != 1:
        raise EngineError(
            Diagnostic(
                "CONFIG.MARKDOWN_LINK_COVERAGE_WIDTH",
                "invalid",
                "Markdown link coverage must project exactly one member column",
                suite=suite_id,
                check=check_id,
                field="members.columns",
                expected="1",
                observed=str(len(members.projection.columns)),
            )
        )
    return MarkdownLinkCoverageCheck(check_id, path, members)
