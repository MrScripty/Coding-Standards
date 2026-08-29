from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tools.standards_metadata.standards_metadata import (
    MetadataFailure,
    validate_module_metadata,
)

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs


@dataclass(frozen=True, slots=True)
class MetadataCase:
    id: str
    paths: tuple[str, ...]
    expected: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MetadataGraphCheck:
    id: str
    paths: tuple[str, ...] | None
    cases: tuple[MetadataCase, ...] | None

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        paths = self.paths or tuple(
            path for case in self.cases or () for path in case.paths
        )
        return present_inputs("metadata", *paths)

    def run(self, context: CheckContext) -> list[Diagnostic]:
        if self.paths is not None:
            return _validate_graph(context, self.id, self.paths)

        diagnostics: list[Diagnostic] = []
        assert self.cases is not None
        for case in self.cases:
            observed = tuple(
                item.code for item in _validate_graph(context, self.id, case.paths)
            )
            if observed != case.expected:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.METADATA_FIXTURE",
                        "invalid",
                        "metadata fixture diagnostics do not match",
                        suite=context.suite_id,
                        check=self.id,
                        field=case.id,
                        expected=",".join(case.expected) or "pass",
                        observed=",".join(observed) or "pass",
                    )
                )
        return diagnostics


def _diagnostic(
    context: CheckContext,
    check: str,
    failure: MetadataFailure,
) -> Diagnostic:
    return Diagnostic(
        failure.code,
        failure.outcome,
        failure.message,
        suite=context.suite_id,
        check=check,
        path=failure.path,
        row=failure.row,
        field=failure.field,
        expected=failure.expected,
        observed=failure.observed,
    )


def _validate_graph(
    context: CheckContext,
    check: str,
    paths: tuple[str, ...],
) -> list[Diagnostic]:
    result = validate_module_metadata(context.repo_root, paths)
    diagnostics = [_diagnostic(context, check, failure) for failure in result.failures]
    if diagnostics and diagnostics[0].code.startswith(("INPUT.", "PATH.")):
        raise EngineError(diagnostics[0])
    return diagnostics


def _strings(
    value: Any,
    *,
    suite: str,
    check: str,
    field: str,
) -> tuple[str, ...]:
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
                "field must contain unique non-empty strings",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return tuple(value)


def parse_metadata_graph_check(
    raw: dict[str, Any],
    suite_id: str,
) -> MetadataGraphCheck:
    allowed = {"id", "type", "paths", "cases"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "metadata graph check contains unknown fields",
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
    has_cases = "cases" in raw
    if has_paths == has_cases:
        raise EngineError(
            Diagnostic(
                "CONFIG.METADATA_MODE",
                "invalid",
                "metadata graph requires exactly one of paths or cases",
                suite=suite_id,
                check=check_id,
            )
        )
    if has_paths:
        return MetadataGraphCheck(
            check_id,
            _strings(
                raw["paths"],
                suite=suite_id,
                check=check_id,
                field="paths",
            ),
            None,
        )

    raw_cases = raw["cases"]
    if not isinstance(raw_cases, list) or not raw_cases:
        raise EngineError(
            Diagnostic(
                "CONFIG.METADATA_CASES",
                "invalid",
                "metadata fixture mode requires cases",
                suite=suite_id,
                check=check_id,
                field="cases",
            )
        )
    cases: list[MetadataCase] = []
    seen: set[str] = set()
    for raw_case in raw_cases:
        if not isinstance(raw_case, dict) or set(raw_case) != {
            "id",
            "paths",
            "expected",
        }:
            raise EngineError(
                Diagnostic(
                    "CONFIG.METADATA_CASE",
                    "invalid",
                    "metadata case requires exactly id, paths, and expected",
                    suite=suite_id,
                    check=check_id,
                )
            )
        case_id = raw_case["id"]
        expected = raw_case["expected"]
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise EngineError(
                Diagnostic(
                    "CONFIG.METADATA_CASE_ID",
                    "invalid",
                    "metadata case IDs must be unique non-empty strings",
                    suite=suite_id,
                    check=check_id,
                    observed=str(case_id),
                )
            )
        if (
            not isinstance(expected, list)
            or any(not isinstance(item, str) or not item for item in expected)
            or len(set(expected)) != len(expected)
        ):
            raise EngineError(
                Diagnostic(
                    "CONFIG.METADATA_EXPECTED",
                    "invalid",
                    "expected diagnostics must be unique non-empty strings",
                    suite=suite_id,
                    check=check_id,
                    field=case_id,
                )
            )
        seen.add(case_id)
        cases.append(
            MetadataCase(
                case_id,
                _strings(
                    raw_case["paths"],
                    suite=suite_id,
                    check=check_id,
                    field=f"{case_id}.paths",
                ),
                tuple(expected),
            )
        )
    return MetadataGraphCheck(check_id, None, tuple(cases))
