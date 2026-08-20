from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file


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
    paths: tuple[str, ...]

    def run(self, context: CheckContext) -> list[Diagnostic]:
        for display_path in self.paths:
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
                        ),
                        exit_code=3,
                    )
        return []


def parse_markdown_links_check(
    raw: dict[str, Any], suite_id: str
) -> MarkdownLinksCheck:
    allowed = {"id", "type", "paths"}
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
    return MarkdownLinksCheck(check_id, _paths(raw.get("paths"), suite_id, check_id))
