from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import (
    CheckAuthorityInput,
    CheckContext,
    absent_inputs,
    present_inputs,
)
from ..paths import contained_path


def _paths(value: Any, field: str, suite: str, check: str) -> tuple[str, ...]:
    if value is None:
        return ()
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
                "field must contain unique non-empty paths",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return tuple(value)


@dataclass(frozen=True, slots=True)
class PathStateCheck:
    id: str
    present: tuple[str, ...]
    absent: tuple[str, ...]

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        return (
            *present_inputs("required-present", *self.present),
            *absent_inputs("required-absent", *self.absent),
        )

    def run(self, context: CheckContext) -> list[Diagnostic]:
        diagnostics = []
        for display_path in self.present:
            candidate = contained_path(
                context.repo_root,
                display_path,
                suite=context.suite_id,
                check=self.id,
            )
            if not candidate.exists():
                raise EngineError(
                    Diagnostic(
                        "INPUT.UNAVAILABLE",
                        "unavailable",
                        "required path does not exist",
                        suite=context.suite_id,
                        check=self.id,
                        path=display_path,
                        expected="present",
                        observed="absent",
                    )
                )

        for display_path in self.absent:
            candidate = contained_path(
                context.repo_root,
                display_path,
                suite=context.suite_id,
                check=self.id,
            )
            if os.path.lexists(candidate):
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.PATH_PRESENT",
                        "invalid",
                        "path required to be absent is present",
                        suite=context.suite_id,
                        check=self.id,
                        path=display_path,
                        expected="absent",
                        observed="present",
                    )
                )
        return diagnostics


def parse_path_state_check(raw: dict[str, Any], suite_id: str) -> PathStateCheck:
    allowed = {"id", "type", "present", "absent"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "path_state check contains unknown fields",
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
    present = _paths(raw.get("present"), "present", suite_id, check_id)
    absent = _paths(raw.get("absent"), "absent", suite_id, check_id)
    if not present and not absent:
        raise EngineError(
            Diagnostic(
                "CONFIG.EMPTY_CHECK",
                "invalid",
                "path_state check requires present or absent paths",
                suite=suite_id,
                check=check_id,
            )
        )
    overlap = set(present) & set(absent)
    if overlap:
        raise EngineError(
            Diagnostic(
                "CONFIG.CONTRADICTORY_PATH_STATE",
                "invalid",
                "path cannot be both present and absent",
                suite=suite_id,
                check=check_id,
                path=sorted(overlap)[0],
            )
        )
    return PathStateCheck(check_id, present, absent)
