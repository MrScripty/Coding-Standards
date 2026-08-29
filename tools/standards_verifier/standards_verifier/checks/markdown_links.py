from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs
from ..paths import contained_file
from .table import (
    ProjectedTableSource,
    parse_projected_table_source,
    read_projected_table_rows,
)


LINK_PATTERN = re.compile(r"\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:")


def _paths(value: Any, suite: str, check: str) -> tuple[str, ...]:
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
                "paths must contain unique non-empty strings",
                suite=suite,
                check=check,
                field="paths",
            )
        )
    return tuple(value)


@dataclass(frozen=True, slots=True)
class LocalMarkdownTarget:
    destination: str
    repository_path: str
    resolved_path: Path


def local_markdown_targets(
    context: CheckContext,
    check_id: str,
    display_path: str,
) -> tuple[LocalMarkdownTarget, ...]:
    root = context.repo_root.resolve()
    source = contained_file(
        root,
        display_path,
        suite=context.suite_id,
        check=check_id,
    )
    try:
        content = source.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise EngineError(
            Diagnostic(
                "INPUT.INVALID_UTF8",
                "invalid",
                str(error),
                suite=context.suite_id,
                check=check_id,
                path=display_path,
            )
        ) from error

    targets = []
    for match in LINK_PATTERN.finditer(content):
        destination = match.group(1)
        if destination.startswith(EXTERNAL_PREFIXES):
            continue

        target = destination.split("#", 1)[0]
        if not target:
            candidate = source
        else:
            relative = PurePosixPath(target)
            if relative.is_absolute():
                raise EngineError(
                    Diagnostic(
                        "PATH.LINK_OUTSIDE_REPOSITORY",
                        "invalid",
                        "Markdown link target must be repository-relative",
                        suite=context.suite_id,
                        check=check_id,
                        path=display_path,
                        observed=destination,
                    )
                )
            candidate = (source.parent / Path(*relative.parts)).resolve(strict=False)

        if not candidate.is_relative_to(root):
            raise EngineError(
                Diagnostic(
                    "PATH.LINK_OUTSIDE_REPOSITORY",
                    "invalid",
                    "Markdown link target escapes the repository root",
                    suite=context.suite_id,
                    check=check_id,
                    path=display_path,
                    observed=destination,
                )
            )
        targets.append(
            LocalMarkdownTarget(
                destination=destination,
                repository_path=candidate.relative_to(root).as_posix(),
                resolved_path=candidate,
            )
        )
    return tuple(targets)


@dataclass(frozen=True, slots=True)
class MarkdownLinksCheck:
    id: str
    paths: tuple[str, ...] | None
    members: ProjectedTableSource | None

    def _selected_paths(self, context: CheckContext) -> tuple[str, ...]:
        if self.members is None:
            if self.paths is None:
                raise TypeError("Markdown link paths or members are required")
            return self.paths
        projected = read_projected_table_rows(context, self.id, self.members)
        return tuple(value for (value,) in projected)

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        paths = self._selected_paths(context)
        target_paths = tuple(
            target.repository_path
            for path in paths
            for target in local_markdown_targets(context, self.id, path)
        )
        declarations = list(present_inputs("markdown", *paths))
        if self.members is not None:
            declarations.extend(present_inputs("members", self.members.path))
        declarations.extend(present_inputs("link-target", *target_paths))
        return tuple(declarations)

    def run(self, context: CheckContext) -> list[Diagnostic]:
        paths = self._selected_paths(context)
        if self.members is not None:
            if (
                not paths
                or any(not value for value in paths)
                or len(set(paths)) != len(paths)
            ):
                return [
                    Diagnostic(
                        "ASSERT.MARKDOWN_LINK_MEMBERS",
                        "invalid",
                        "Markdown link members must be unique and non-empty",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.members.path,
                    )
                ]
        for display_path in paths:
            for target in local_markdown_targets(context, self.id, display_path):
                if not target.resolved_path.exists():
                    raise EngineError(
                        Diagnostic(
                            "INPUT.LINK_TARGET_UNAVAILABLE",
                            "unavailable",
                            "Markdown link target does not exist",
                            suite=context.suite_id,
                            check=self.id,
                            path=display_path,
                            observed=target.destination,
                        )
                    )
        return []


def parse_markdown_links_check(
    raw: dict[str, Any], suite_id: str
) -> MarkdownLinksCheck:
    allowed = {"id", "type", "paths", "members"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "markdown_links check contains unknown fields",
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
    has_paths = "paths" in raw
    has_members = "members" in raw
    if has_paths == has_members:
        raise EngineError(
            Diagnostic(
                "CONFIG.MARKDOWN_LINK_SOURCES",
                "invalid",
                "markdown_links requires exactly one of paths or members",
                suite=suite_id,
                check=check_id,
            )
        )
    if has_paths:
        return MarkdownLinksCheck(
            check_id,
            _paths(raw.get("paths"), suite_id, check_id),
            None,
        )
    members = parse_projected_table_source(
        raw.get("members"),
        suite_id,
        check_id,
        "members",
        invalid_code="CONFIG.MARKDOWN_LINK_MEMBERS",
        source_name="Markdown link member source",
        projection_name="Markdown link member projection",
        predicate_name="Markdown link member predicate",
    )
    if (
        len(members.projection.columns) != 1
        or members.projection.split_field is not None
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.MARKDOWN_LINK_MEMBERS",
                "invalid",
                "Markdown link members must select one unsplit column",
                suite=suite_id,
                check=check_id,
            )
        )
    return MarkdownLinksCheck(check_id, None, members)
