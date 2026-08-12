from __future__ import annotations

from pathlib import Path, PurePosixPath

from .diagnostics import Diagnostic, EngineError


def contained_path(
    root: Path,
    value: str,
    *,
    suite: str | None = None,
    check: str | None = None,
) -> Path:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts:
        raise EngineError(
            Diagnostic(
                code="PATH.OUTSIDE_REPOSITORY",
                outcome="invalid",
                message="path must be a non-empty repository-relative path without parent traversal",
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
                code="PATH.OUTSIDE_REPOSITORY",
                outcome="invalid",
                message="resolved path escapes the repository root",
                suite=suite,
                check=check,
                path=value,
            )
        )
    return candidate


def contained_file(
    root: Path,
    value: str,
    *,
    suite: str | None = None,
    check: str | None = None,
) -> Path:
    candidate = contained_path(
        root,
        value,
        suite=suite,
        check=check,
    )
    resolved_candidate = candidate.resolve(strict=False)
    if not resolved_candidate.exists():
        raise EngineError(
            Diagnostic(
                code="INPUT.UNAVAILABLE",
                outcome="unavailable",
                message="required input does not exist",
                suite=suite,
                check=check,
                path=value,
            ),
            exit_code=3,
        )
    if not resolved_candidate.is_file():
        raise EngineError(
            Diagnostic(
                code="INPUT.NOT_FILE",
                outcome="invalid",
                message="required input is not a regular file",
                suite=suite,
                check=check,
                path=value,
            )
        )
    return resolved_candidate
