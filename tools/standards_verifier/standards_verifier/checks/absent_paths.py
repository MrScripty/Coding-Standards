from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext


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


def _contained_candidate(
    root: Path,
    value: str,
    *,
    suite: str,
    check: str,
) -> Path:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise EngineError(
            Diagnostic(
                "PATH.OUTSIDE_REPOSITORY",
                "invalid",
                "path must be repository-relative without parent traversal",
                suite=suite,
                check=check,
                path=value,
            )
        )

    resolved_root = root.resolve()
    candidate = resolved_root / Path(*path.parts)
    resolved_candidate = candidate.resolve(strict=False)
    if not resolved_candidate.is_relative_to(resolved_root):
        raise EngineError(
            Diagnostic(
                "PATH.OUTSIDE_REPOSITORY",
                "invalid",
                "resolved path escapes the repository root",
                suite=suite,
                check=check,
                path=value,
            )
        )
    return candidate


@dataclass(frozen=True, slots=True)
class AbsentPathsCheck:
    id: str
    paths: tuple[str, ...]

    def run(self, context: CheckContext) -> list[Diagnostic]:
        diagnostics = []
        for display_path in self.paths:
            candidate = _contained_candidate(
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


def parse_absent_paths_check(
    raw: dict[str, Any], suite_id: str
) -> AbsentPathsCheck:
    allowed = {"id", "type", "paths"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "absent_paths check contains unknown fields",
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
    return AbsentPathsCheck(
        check_id,
        _paths(raw.get("paths"), suite_id, check_id),
    )
