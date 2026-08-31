from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs
from ..paths import contained_file
from .literal_matching import (
    MatchCase,
    literal_key,
    parse_match_case,
    validate_literal_sets,
)
from .markdown import heading_level, scan_headings


SectionScope = Literal["subtree", "body"]


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


@dataclass(frozen=True, slots=True)
class MarkdownSectionTextCheck:
    id: str
    path: str
    heading: str
    heading_level: int
    required: tuple[str, ...]
    prohibited: tuple[str, ...]
    match_case: MatchCase
    scope: SectionScope

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        return present_inputs("content", self.path)

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

        headings = scan_headings(content)
        starts = tuple(item for item in headings if item.text == self.heading)
        if len(starts) != 1:
            return [
                Diagnostic(
                    "ASSERT.MARKDOWN_SECTION_SELECTION",
                    "invalid",
                    "section heading must occur exactly once outside fences",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    field="heading",
                    expected=self.heading,
                    observed=("absent" if not starts else f"{len(starts)} matches"),
                )
            ]

        start = starts[0]
        end_line = None
        for item in headings:
            if (
                item.line_number > start.line_number
                and (self.scope == "body" or item.level <= self.heading_level)
            ):
                end_line = item.line_number
                break
        lines = content.splitlines(keepends=True)
        section = "".join(
            lines[start.line_number - 1 : (end_line - 1) if end_line else None]
        )

        searchable = literal_key(section, self.match_case)
        diagnostics = []
        for literal in self.required:
            if literal_key(literal, self.match_case) not in searchable:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.MARKDOWN_SECTION_REQUIRED",
                        "invalid",
                        "selected Markdown section lacks a required literal",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=start.line_number,
                        expected=literal,
                        observed="absent",
                    )
                )
        for literal in self.prohibited:
            if literal_key(literal, self.match_case) in searchable:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.MARKDOWN_SECTION_PROHIBITED",
                        "invalid",
                        "selected Markdown section contains a prohibited literal",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=start.line_number,
                        expected="absent",
                        observed=literal,
                    )
                )
        return diagnostics


def parse_markdown_section_text_check(
    raw: dict[str, Any], suite_id: str
) -> MarkdownSectionTextCheck:
    allowed = {
        "id",
        "type",
        "path",
        "heading",
        "required",
        "prohibited",
        "match_case",
        "scope",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "markdown_section_text check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    path = raw.get("path")
    heading = raw.get("heading")
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
    level = heading_level(heading) if isinstance(heading, str) else None
    if (
        not isinstance(heading, str)
        or not heading
        or "\n" in heading
        or "\r" in heading
        or level is None
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.MARKDOWN_HEADING",
                "invalid",
                "heading must be one exact non-empty ATX heading",
                suite=suite_id,
                check=check_id,
                field="heading",
            )
        )
    required = _literal_list(raw.get("required", []), "required", suite_id, check_id)
    prohibited = _literal_list(
        raw.get("prohibited", []), "prohibited", suite_id, check_id
    )
    match_case = parse_match_case(
        raw.get("match_case", "sensitive"),
        suite=suite_id,
        check=check_id,
    )
    scope = raw.get("scope", "subtree")
    if not isinstance(scope, str) or scope not in {"subtree", "body"}:
        raise EngineError(
            Diagnostic(
                "CONFIG.MARKDOWN_SECTION_SCOPE",
                "invalid",
                "markdown section scope must be subtree or body",
                suite=suite_id,
                check=check_id,
                field="scope",
            )
        )
    if not required and not prohibited:
        raise EngineError(
            Diagnostic(
                "CONFIG.EMPTY_CHECK",
                "invalid",
                "markdown_section_text check has no literal constraints",
                suite=suite_id,
                check=check_id,
            )
        )
    validate_literal_sets(
        required,
        prohibited,
        match_case,
        suite=suite_id,
        check=check_id,
    )
    return MarkdownSectionTextCheck(
        check_id,
        path,
        heading,
        level,
        required,
        prohibited,
        match_case,
        scope,
    )
