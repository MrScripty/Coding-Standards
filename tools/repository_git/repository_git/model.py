from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .errors import invalid

_OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z", re.ASCII)


def _scalar(value: str, description: str) -> None:
    if type(value) is not str or not value:
        raise invalid("REPOSITORY_GIT.INVALID_VALUE", f"{description} must be nonempty")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise invalid(
            "REPOSITORY_GIT.INVALID_UNICODE",
            f"{description} must contain Unicode scalar values",
        )


@dataclass(frozen=True, slots=True, order=True, init=False)
class RepositoryPath:
    components: tuple[str, ...]

    def __init__(self, components: Iterable[str]) -> None:
        if type(components) is str:
            raise invalid(
                "REPOSITORY_GIT.INVALID_PATH",
                "repository path components cannot be one string",
            )
        selected = tuple(components)
        if not selected:
            raise invalid(
                "REPOSITORY_GIT.EMPTY_PATH", "repository path must be nonempty"
            )
        for component in selected:
            _scalar(component, "path component")
            if component in {".", ".."} or component.casefold() == ".git":
                raise invalid(
                    "REPOSITORY_GIT.CONTROL_PATH",
                    f"path component {component!r} is reserved",
                )
            if "/" in component or "\\" in component or "\0" in component:
                raise invalid(
                    "REPOSITORY_GIT.INVALID_PATH",
                    "path components cannot contain separators or NUL",
                )
            if len(component.encode("utf-8")) > 255:
                raise invalid(
                    "REPOSITORY_GIT.COMPONENT_TOO_LONG",
                    "path component exceeds 255 UTF-8 bytes",
                )
        object.__setattr__(self, "components", selected)

    @classmethod
    def parse(cls, value: str) -> RepositoryPath:
        _scalar(value, "repository path")
        if value.startswith("/") or "\\" in value:
            raise invalid(
                "REPOSITORY_GIT.INVALID_PATH",
                "repository path must use relative POSIX separators",
            )
        components = value.split("/")
        if any(not component for component in components):
            raise invalid(
                "REPOSITORY_GIT.INVALID_PATH",
                "repository path contains an empty component",
            )
        return cls(components)

    def __str__(self) -> str:
        return "/".join(self.components)


@dataclass(frozen=True, slots=True, order=True)
class RepositoryRevision:
    oid: str

    def __post_init__(self) -> None:
        if type(self.oid) is not str or _OID.fullmatch(self.oid) is None:
            raise invalid(
                "REPOSITORY_GIT.INVALID_OID",
                "revision must be one lowercase SHA-1 or SHA-256 object ID",
            )


@dataclass(frozen=True, slots=True, order=True)
class CapturedFile:
    path: RepositoryPath
    content: bytes

    def __post_init__(self) -> None:
        if type(self.path) is not RepositoryPath or type(self.content) is not bytes:
            raise invalid(
                "REPOSITORY_GIT.INVALID_CONTENT",
                "captured file requires a RepositoryPath and exact bytes",
            )


@dataclass(frozen=True, slots=True, init=False)
class RepositoryCapture:
    revision: RepositoryRevision
    files: tuple[CapturedFile, ...]

    def __init__(
        self, revision: RepositoryRevision, files: Iterable[CapturedFile]
    ) -> None:
        if type(revision) is not RepositoryRevision:
            raise invalid(
                "REPOSITORY_GIT.INVALID_CAPTURE",
                "capture revision must be an exact RepositoryRevision",
            )
        supplied = tuple(files)
        if any(type(item) is not CapturedFile for item in supplied):
            raise invalid(
                "REPOSITORY_GIT.INVALID_CAPTURE",
                "capture files must be exact CapturedFile values",
            )
        selected = tuple(sorted(supplied, key=lambda item: item.path))
        if not selected:
            raise invalid(
                "REPOSITORY_GIT.EMPTY_CAPTURE", "capture must contain at least one file"
            )
        paths = tuple(item.path for item in selected)
        if len(set(paths)) != len(paths):
            raise invalid(
                "REPOSITORY_GIT.DUPLICATE_PATH", "capture paths must be unique"
            )
        object.__setattr__(self, "revision", revision)
        object.__setattr__(self, "files", selected)


@dataclass(frozen=True, slots=True)
class MaterializedCandidate:
    root: Path
    expected: RepositoryRevision
    revision: RepositoryRevision

    def __post_init__(self) -> None:
        if (
            not isinstance(self.root, Path)
            or not self.root.is_absolute()
            or type(self.expected) is not RepositoryRevision
            or type(self.revision) is not RepositoryRevision
        ):
            raise invalid(
                "REPOSITORY_GIT.INVALID_CANDIDATE",
                "candidate requires an absolute root and exact revisions",
            )


@dataclass(frozen=True, slots=True)
class GitlinkRepository:
    prefix: RepositoryPath
    repository: Path

    def __post_init__(self) -> None:
        if (
            type(self.prefix) is not RepositoryPath
            or not isinstance(self.repository, Path)
            or not self.repository.is_absolute()
        ):
            raise invalid(
                "REPOSITORY_GIT.INVALID_GITLINK",
                "gitlink requires a RepositoryPath and absolute pathlib.Path",
            )


@dataclass(frozen=True, slots=True)
class GitCommandResult:
    returncode: int
    stdout: bytes
    stderr: bytes

    def __post_init__(self) -> None:
        if (
            type(self.returncode) is not int
            or type(self.stdout) is not bytes
            or type(self.stderr) is not bytes
        ):
            raise invalid(
                "REPOSITORY_GIT.INVALID_RESULT",
                "Git result requires an integer code and exact byte streams",
            )


__all__ = (
    "CapturedFile",
    "GitCommandResult",
    "GitlinkRepository",
    "MaterializedCandidate",
    "RepositoryCapture",
    "RepositoryPath",
    "RepositoryRevision",
)
