from __future__ import annotations

from pathlib import Path, PurePosixPath

from .errors import MetadataError, MetadataFailure


def normalized_repository_path(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or ".." in path.parts
        or value.startswith("./")
        or str(path) != value
    ):
        raise MetadataError(
            MetadataFailure(
                "PATH.OUTSIDE_REPOSITORY",
                "invalid",
                "path must be a normalized repository-relative path",
                path=value,
            )
        )
    return path


def contained_file(root: Path, value: str) -> Path:
    path = normalized_repository_path(value)
    resolved_root = root.resolve()
    candidate = resolved_root / Path(*path.parts)
    resolved = candidate.resolve(strict=False)
    if not resolved.is_relative_to(resolved_root):
        raise MetadataError(
            MetadataFailure(
                "PATH.OUTSIDE_REPOSITORY",
                "invalid",
                "resolved path escapes the repository root",
                path=value,
            )
        )
    if not resolved.exists():
        raise MetadataError(
            MetadataFailure(
                "INPUT.UNAVAILABLE",
                "unavailable",
                "required input does not exist",
                path=value,
            )
        )
    if not resolved.is_file():
        raise MetadataError(
            MetadataFailure(
                "INPUT.NOT_FILE",
                "invalid",
                "required input is not a regular file",
                path=value,
            )
        )
    return resolved
