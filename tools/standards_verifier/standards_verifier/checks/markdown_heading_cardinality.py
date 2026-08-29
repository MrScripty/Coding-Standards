from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs
from ..paths import contained_file
from .markdown import scan_headings


CARDINALITIES = frozenset({"empty", "single", "nonempty"})


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


def _observed_state(selected: int) -> str:
    if selected == 0:
        return "empty"
    if selected == 1:
        return "single"
    return "multiple"


@dataclass(frozen=True, slots=True)
class MarkdownHeadingCardinalityCheck:
    id: str
    path: str
    level: int
    cardinality: str

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

        selected = sum(
            heading.level == self.level for heading in scan_headings(content)
        )
        observed = _observed_state(selected)
        matches = (
            self.cardinality == observed
            or self.cardinality == "nonempty"
            and observed != "empty"
        )
        if matches:
            return []
        return [
            Diagnostic(
                "ASSERT.MARKDOWN_HEADING_CARDINALITY",
                "invalid",
                "selected heading cardinality does not match",
                suite=context.suite_id,
                check=self.id,
                path=self.path,
                field="cardinality",
                expected=self.cardinality,
                observed=observed,
            )
        ]


def parse_markdown_heading_cardinality_check(
    raw: dict[str, Any], suite_id: str
) -> MarkdownHeadingCardinalityCheck:
    allowed = {"id", "type", "path", "level", "cardinality"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "markdown_heading_cardinality check contains unknown fields",
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
            )
        )
    level = _heading_level(raw.get("level"), suite_id, check_id)
    cardinality = raw.get("cardinality")
    if not isinstance(cardinality, str) or cardinality not in CARDINALITIES:
        raise EngineError(
            Diagnostic(
                "CONFIG.HEADING_CARDINALITY",
                "invalid",
                "cardinality must be empty, single, or nonempty",
                suite=suite_id,
                check=check_id,
                field="cardinality",
                observed=str(cardinality),
            )
        )
    return MarkdownHeadingCardinalityCheck(
        check_id,
        path,
        level,
        cardinality,
    )
