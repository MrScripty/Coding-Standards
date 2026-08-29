from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Sequence


class GitIndexError(RuntimeError):
    def __init__(self, code: str, outcome: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.outcome = outcome


def sanitized_git_environment() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}


def indexed_paths(root: Path) -> tuple[str, ...]:
    output = _git(root, ("ls-files", "-z", "--full-name"))
    return tuple(sorted(_nul_fields(output, "Git index path output")))


def staged_name_status(
    root: Path, base: str, pathspecs: Sequence[str]
) -> tuple[str, ...]:
    output = _git(
        root,
        (
            "diff",
            "--cached",
            "--name-status",
            "-z",
            "--find-renames",
            "--find-copies",
            base,
            "--",
            *pathspecs,
        ),
    )
    return _nul_fields(output, "Git staged name-status output")


def materialize_index(root: Path, destination: Path) -> None:
    prefix = str(destination.resolve()) + os.sep
    _git(root, ("checkout-index", "--all", "--force", f"--prefix={prefix}"))


def _git(root: Path, arguments: Sequence[str]) -> bytes:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=False,
            capture_output=True,
            env=sanitized_git_environment(),
        )
    except OSError as error:
        raise GitIndexError(
            "GIT.UNAVAILABLE", "unavailable", f"Git execution failed: {error}"
        ) from error
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise GitIndexError(
            "GIT.INDEX_UNAVAILABLE",
            "unavailable",
            f"Git command failed with exit {completed.returncode}: {detail}",
        )
    return completed.stdout


def _nul_fields(output: bytes, description: str) -> tuple[str, ...]:
    if not output:
        return ()
    if not output.endswith(b"\0"):
        raise GitIndexError(
            "GIT.INDEX_OUTPUT", "invalid", f"{description} is not NUL terminated"
        )
    try:
        fields = output[:-1].decode("utf-8").split("\0")
    except UnicodeDecodeError as error:
        raise GitIndexError(
            "GIT.INDEX_UTF8", "invalid", f"{description} is not UTF-8"
        ) from error
    if any(not field for field in fields):
        raise GitIndexError(
            "GIT.INDEX_OUTPUT", "invalid", f"{description} contains an empty field"
        )
    return tuple(fields)


__all__ = (
    "GitIndexError",
    "indexed_paths",
    "materialize_index",
    "sanitized_git_environment",
    "staged_name_status",
)
