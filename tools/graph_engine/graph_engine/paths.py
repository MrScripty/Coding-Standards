from __future__ import annotations

from pathlib import Path, PurePosixPath

from .errors import MissingArtifactError, PathEscapeError


def contained_path(root: Path, value: str, *, must_exist: bool) -> Path:
    logical = PurePosixPath(value)
    resolved_root = root.resolve()
    candidate = (resolved_root / Path(*logical.parts)).resolve(strict=False)
    if (
        not value
        or logical.is_absolute()
        or ".." in logical.parts
        or not candidate.is_relative_to(resolved_root)
    ):
        raise PathEscapeError("path escapes the repository", path=value)
    if must_exist and not candidate.exists():
        raise MissingArtifactError("repository artifact does not exist", path=value)
    if must_exist and candidate.is_symlink():
        candidate = candidate.resolve()
    if not candidate.is_relative_to(resolved_root):
        raise PathEscapeError("resolved path escapes the repository", path=value)
    return candidate


def repository_locator(root: Path, value: str) -> str:
    candidate = contained_path(root, value, must_exist=True)
    return candidate.relative_to(root.resolve()).as_posix()
