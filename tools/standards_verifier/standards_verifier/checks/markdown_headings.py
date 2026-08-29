from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs
from ..paths import contained_file
from .markdown import scan_headings


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


@dataclass(frozen=True, slots=True)
class MarkdownHeadingsCheck:
    id: str
    path: str
    level: int
    required: tuple[str, ...]
    prohibited: tuple[str, ...]

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

        headings = tuple(
            item for item in scan_headings(content) if item.level == self.level
        )
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
        for heading in headings:
            for literal in self.required:
                if literal not in heading.text:
                    diagnostics.append(
                        Diagnostic(
                            "ASSERT.MARKDOWN_HEADING_REQUIRED",
                            "invalid",
                            "selected heading lacks a required literal",
                            suite=context.suite_id,
                            check=self.id,
                            path=self.path,
                            row=heading.line_number,
                            expected=literal,
                            observed=heading.text,
                        )
                    )
            for literal in self.prohibited:
                if literal in heading.text:
                    diagnostics.append(
                        Diagnostic(
                            "ASSERT.MARKDOWN_HEADING_PROHIBITED",
                            "invalid",
                            "selected heading contains a prohibited literal",
                            suite=context.suite_id,
                            check=self.id,
                            path=self.path,
                            row=heading.line_number,
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
