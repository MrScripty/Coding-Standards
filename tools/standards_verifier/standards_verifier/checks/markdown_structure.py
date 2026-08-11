from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file


HEADING_PATTERN = re.compile(r"^#{1,6} .*$")


def _headings(value: Any, suite: str, check: str) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or any(
            not isinstance(item, str)
            or not item
            or HEADING_PATTERN.fullmatch(item) is None
            for item in value
        )
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.MARKDOWN_HEADINGS",
                "invalid",
                "headings must contain valid non-empty ATX heading lines",
                suite=suite,
                check=check,
                field="headings",
            )
        )
    if len(set(value)) != len(value):
        raise EngineError(
            Diagnostic(
                "CONFIG.DUPLICATE_VALUE",
                "invalid",
                "headings must be unique",
                suite=suite,
                check=check,
                field="headings",
            )
        )
    return tuple(value)


def _maximum_lines(value: Any, suite: str, check: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise EngineError(
            Diagnostic(
                "CONFIG.POSITIVE_INTEGER",
                "invalid",
                "maximum_lines must be a positive integer",
                suite=suite,
                check=check,
                field="maximum_lines",
            )
        )
    return value


@dataclass(frozen=True, slots=True)
class MarkdownStructureCheck:
    id: str
    path: str
    headings: tuple[str, ...]
    maximum_lines: int

    def run(self, context: CheckContext) -> list[Diagnostic]:
        source = contained_file(
            context.repo_root,
            self.path,
            suite=context.suite_id,
            check=self.id,
        )
        content_bytes = source.read_bytes()
        try:
            content = content_bytes.decode("utf-8")
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

        observed_headings = tuple(
            line for line in content.splitlines() if HEADING_PATTERN.match(line)
        )
        observed_lines = content_bytes.count(b"\n")
        diagnostics = []
        if observed_headings != self.headings:
            diagnostics.append(
                Diagnostic(
                    "ASSERT.MARKDOWN_HEADINGS",
                    "invalid",
                    "Markdown headings do not match the exact ordered contract",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    expected=" | ".join(self.headings),
                    observed=" | ".join(observed_headings),
                )
            )
        if observed_lines > self.maximum_lines:
            diagnostics.append(
                Diagnostic(
                    "ASSERT.LINE_LIMIT",
                    "invalid",
                    "raw newline count exceeds the inclusive maximum",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    expected=f"<= {self.maximum_lines}",
                    observed=str(observed_lines),
                )
            )
        return diagnostics


def parse_markdown_structure_check(
    raw: dict[str, Any], suite_id: str
) -> MarkdownStructureCheck:
    allowed = {"id", "type", "path", "headings", "maximum_lines"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "markdown_structure check contains unknown fields",
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
                "path must be a non-empty string",
                suite=suite_id,
                check=check_id,
                field="path",
            )
        )
    return MarkdownStructureCheck(
        check_id,
        path,
        _headings(raw.get("headings"), suite_id, check_id),
        _maximum_lines(raw.get("maximum_lines"), suite_id, check_id),
    )
