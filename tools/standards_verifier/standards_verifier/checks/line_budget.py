from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file
from .table import read_table_rows


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


def _positive_integer(value: Any, field: str, suite: str, check: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise EngineError(
            Diagnostic(
                "CONFIG.POSITIVE_INTEGER",
                "invalid",
                "field must be a positive integer",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return value


@dataclass(frozen=True, slots=True)
class LineBudgetCheck:
    id: str
    paths: tuple[str, ...]
    baseline_path: str
    baseline_key: str
    maximum_numerator: int
    maximum_denominator: int

    def run(self, context: CheckContext) -> list[Diagnostic]:
        observed = 0
        for display_path in self.paths:
            source = contained_file(
                context.repo_root,
                display_path,
                suite=context.suite_id,
                check=self.id,
            )
            observed += source.read_bytes().count(b"\n")

        rows = read_table_rows(
            context.repo_root,
            self.baseline_path,
            ("metric", "value"),
            suite=context.suite_id,
            check=self.id,
        )
        matches = [row for row in rows if row["metric"] == self.baseline_key]
        if not matches:
            raise EngineError(
                Diagnostic(
                    "INPUT.BASELINE_KEY_UNAVAILABLE",
                    "unavailable",
                    "required baseline metric is absent",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.baseline_path,
                    field="baseline_key",
                    observed=self.baseline_key,
                ),
                exit_code=3,
            )
        if len(matches) != 1:
            raise EngineError(
                Diagnostic(
                    "TABLE.DUPLICATE_BASELINE_KEY",
                    "invalid",
                    "baseline metric must occur exactly once",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.baseline_path,
                    field="baseline_key",
                    observed=self.baseline_key,
                )
            )

        raw_baseline = matches[0]["value"]
        if (
            not raw_baseline.isascii()
            or not raw_baseline.isdecimal()
            or int(raw_baseline) <= 0
        ):
            raise EngineError(
                Diagnostic(
                    "TABLE.BASELINE_VALUE",
                    "invalid",
                    "baseline metric value must be a positive ASCII decimal integer",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.baseline_path,
                    field="value",
                    observed=raw_baseline,
                )
            )
        baseline = int(raw_baseline)
        if (
            observed * self.maximum_denominator
            < baseline * self.maximum_numerator
        ):
            return []
        return [
            Diagnostic(
                "ASSERT.LINE_BUDGET",
                "invalid",
                "aggregate newline count does not satisfy the strict baseline ratio",
                suite=context.suite_id,
                check=self.id,
                path=",".join(self.paths),
                expected=(
                    f"observed*{self.maximum_denominator} < "
                    f"{baseline}*{self.maximum_numerator}"
                ),
                observed=str(observed),
            )
        ]


def parse_line_budget_check(raw: dict[str, Any], suite_id: str) -> LineBudgetCheck:
    allowed = {
        "id",
        "type",
        "paths",
        "baseline_path",
        "baseline_key",
        "maximum_numerator",
        "maximum_denominator",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "line_budget check contains unknown fields",
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
    baseline_path = raw.get("baseline_path")
    baseline_key = raw.get("baseline_key")
    if not isinstance(baseline_path, str) or not baseline_path:
        raise EngineError(
            Diagnostic(
                "CONFIG.PATH",
                "invalid",
                "baseline_path must be a non-empty string",
                suite=suite_id,
                check=check_id,
                field="baseline_path",
            )
        )
    if not isinstance(baseline_key, str) or not baseline_key:
        raise EngineError(
            Diagnostic(
                "CONFIG.BASELINE_KEY",
                "invalid",
                "baseline_key must be a non-empty string",
                suite=suite_id,
                check=check_id,
                field="baseline_key",
            )
        )
    return LineBudgetCheck(
        check_id,
        _paths(raw.get("paths"), suite_id, check_id),
        baseline_path,
        baseline_key,
        _positive_integer(
            raw.get("maximum_numerator"),
            "maximum_numerator",
            suite_id,
            check_id,
        ),
        _positive_integer(
            raw.get("maximum_denominator"),
            "maximum_denominator",
            suite_id,
            check_id,
        ),
    )
