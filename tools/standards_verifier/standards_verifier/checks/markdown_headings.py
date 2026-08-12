from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file


ATX_HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+|$)")
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def _literal_list(value: Any, field: str, suite: str, check: str) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
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


def _heading_level(value: Any, suite: str, check: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 6:
        raise EngineError(
            Diagnostic(
                "CONFIG.HEADING_LEVEL",
                "invalid",
                "heading level must be an integer from 1 through 6",
                suite=suite,
                check=check,
                field="level",
                observed=str(value),
            )
        )
    return value


def _selected_headings(content: str, level: int) -> tuple[tuple[int, str], ...]:
    selected = []
    fence_character: str | None = None
    fence_length = 0
    for line_number, line in enumerate(content.splitlines(), start=1):
        fence = FENCE_OPEN.match(line)
        if fence_character is not None:
            if (
                fence is not None
                and fence.group(1)[0] == fence_character
                and len(fence.group(1)) >= fence_length
                and not line[fence.end() :].strip()
            ):
                fence_character = None
                fence_length = 0
            continue
        if fence is not None:
            fence_character = fence.group(1)[0]
            fence_length = len(fence.group(1))
            continue
        heading = ATX_HEADING.match(line)
        if heading is not None and len(heading.group(1)) == level:
            selected.append((line_number, line))
    return tuple(selected)


@dataclass(frozen=True, slots=True)
class MarkdownHeadingsCheck:
    id: str
    path: str
    level: int
    required: tuple[str, ...]
    prohibited: tuple[str, ...]

    def run(self, context: CheckContext) -> list[Diagnostic]:
        source = contained_file(
            context.repo_root,
            self.path,
            suite=context.suite_id,
            check=self.id,
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
                    check=self.id,
                    path=self.path,
                )
            ) from error

        headings = _selected_headings(content, self.level)
        if not headings:
            return [
                Diagnostic(
                    "ASSERT.MARKDOWN_HEADING_SELECTION",
                    "invalid",
                    "no heading matches the configured level",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    field="level",
                    expected=str(self.level),
                    observed="no matches",
                )
            ]

        diagnostics = []
        for line_number, heading in headings:
            for literal in self.required:
                if literal not in heading:
                    diagnostics.append(
                        Diagnostic(
                            "ASSERT.MARKDOWN_HEADING_REQUIRED",
                            "invalid",
                            "selected heading lacks a required literal",
                            suite=context.suite_id,
                            check=self.id,
                            path=self.path,
                            row=line_number,
                            expected=literal,
                            observed=heading,
                        )
                    )
            for literal in self.prohibited:
                if literal in heading:
                    diagnostics.append(
                        Diagnostic(
                            "ASSERT.MARKDOWN_HEADING_PROHIBITED",
                            "invalid",
                            "selected heading contains a prohibited literal",
                            suite=context.suite_id,
                            check=self.id,
                            path=self.path,
                            row=line_number,
                            expected="absent",
                            observed=literal,
                        )
                    )
        return diagnostics


def parse_markdown_headings_check(
    raw: dict[str, Any], suite_id: str
) -> MarkdownHeadingsCheck:
    allowed = {"id", "type", "path", "level", "required", "prohibited"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "markdown_headings check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    path = raw.get("path")
    if not isinstance(check_id, str) or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    if not isinstance(path, str) or not path:
        raise EngineError(
            Diagnostic(
                "CONFIG.PATH",
                "invalid",
                "path must be a non-empty string",
                suite=suite_id,
                check=check_id,
            )
        )
    level = _heading_level(raw.get("level"), suite_id, check_id)
    required = _literal_list(raw.get("required", []), "required", suite_id, check_id)
    prohibited = _literal_list(
        raw.get("prohibited", []), "prohibited", suite_id, check_id
    )
    if not required and not prohibited:
        raise EngineError(
            Diagnostic(
                "CONFIG.EMPTY_CHECK",
                "invalid",
                "markdown_headings check has no literal constraints",
                suite=suite_id,
                check=check_id,
            )
        )
    overlap = set(required) & set(prohibited)
    if overlap:
        raise EngineError(
            Diagnostic(
                "CONFIG.CONTRADICTORY_TEXT",
                "invalid",
                "a literal cannot be both required and prohibited",
                suite=suite_id,
                check=check_id,
                observed=sorted(overlap)[0],
            )
        )
    return MarkdownHeadingsCheck(
        check_id,
        path,
        level,
        required,
        prohibited,
    )
