from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from tools.repository_git.repository_git import GitRepositoryError, indexed_paths

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, CheckRepositoryIndexInput
from ..paths import contained_path, repository_path


def _tracked_paths(value: Any, suite: str, check: str) -> tuple[str, ...]:
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
                "tracked must contain unique non-empty paths",
                suite=suite,
                check=check,
                field="tracked",
            )
        )
    paths = []
    for item in value:
        path = repository_path(item, suite=suite, check=check)
        if path == PurePosixPath(".") or any(
            part in {"", "."} for part in item.split("/")
        ):
            raise EngineError(
                Diagnostic(
                    "CONFIG.GIT_INDEX_PATH",
                    "invalid",
                    "tracked path cannot contain empty or dot components",
                    suite=suite,
                    check=check,
                    path=item,
                )
            )
        paths.append(path.as_posix())
    return tuple(paths)


def read_git_index(root: Path, suite: str, check: str) -> frozenset[str]:
    try:
        entries = indexed_paths(root)
    except GitRepositoryError as error:
        raise EngineError(
            Diagnostic(
                error.failure.code,
                error.failure.kind,
                "Git index membership cannot be read",
                suite=suite,
                check=check,
                observed=error.failure.message,
            )
        ) from error
    return frozenset(entries)


@dataclass(frozen=True, slots=True)
class GitIndexPathsCheck:
    id: str
    tracked: tuple[str, ...]

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        return (CheckRepositoryIndexInput("tracked-path-membership"),)

    def run(self, context: CheckContext) -> list[Diagnostic]:
        entries = read_git_index(context.repo_root, context.suite_id, self.id)
        diagnostics = []
        for display_path in self.tracked:
            if display_path in entries:
                continue
            candidate = contained_path(
                context.repo_root,
                display_path,
                suite=context.suite_id,
                check=self.id,
            )
            observed = (
                "present-untracked"
                if os.path.lexists(candidate)
                else "absent-untracked"
            )
            diagnostics.append(
                Diagnostic(
                    "ASSERT.GIT_INDEX_UNTRACKED",
                    "invalid",
                    "required path is not tracked in the Git index",
                    suite=context.suite_id,
                    check=self.id,
                    path=display_path,
                    expected="tracked",
                    observed=observed,
                )
            )
        return diagnostics


def parse_git_index_paths_check(
    raw: dict[str, Any], suite_id: str
) -> GitIndexPathsCheck:
    allowed = {"id", "type", "tracked"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "git_index_paths check contains unknown fields",
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
    tracked = _tracked_paths(raw.get("tracked"), suite_id, check_id)
    return GitIndexPathsCheck(check_id, tracked)
