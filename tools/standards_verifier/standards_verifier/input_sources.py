"""Authoritative inputs for declaration discovery and suite-manifest compilation.

Executing checks remains filesystem-owned. Frozen proposal input reads expose
only explicit membership and supplied bytes; membership alone never supplies data.
"""
from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Protocol, Sequence

from tools.repository_git.repository_git import GitRepositoryError, RepositoryPath, indexed_paths
from tools.standards_metadata.standards_metadata import FrozenContentSource, MetadataError

from .diagnostics import Diagnostic, EngineError
from .paths import contained_file, contained_path, repository_path


class SuiteInputSource(Protocol):
    def read_bytes(self, path: str, *, suite: str | None = None, check: str | None = None) -> bytes: ...
    def exists(self, path: str) -> bool: ...
    def indexed_paths(self) -> tuple[str, ...]: ...
    def link_target(self, source: str, target: str, *, suite: str, check: str, destination: str) -> str: ...


def repository_path_observation(paths: Sequence[str]) -> tuple[str, ...]:
    try:
        selected = tuple(sorted(str(RepositoryPath.parse(path)) for path in paths if type(path) is str))
    except GitRepositoryError as error:
        raise EngineError(Diagnostic(
            "INPUT.INVALID_REPOSITORY_PATH", "invalid",
            "explicit repository path observation is invalid",
        )) from error
    if len(selected) != len(paths) or len(set(selected)) != len(selected):
        raise EngineError(Diagnostic(
            "INPUT.INVALID_REPOSITORY_PATHS", "invalid",
            "explicit repository path observation must contain unique strings",
        ))
    return selected


def _link_escape(source: str, destination: str, suite: str, check: str, *, absolute: bool = False) -> EngineError:
    return EngineError(Diagnostic(
        "PATH.LINK_OUTSIDE_REPOSITORY", "invalid",
        "Markdown link target must be repository-relative" if absolute else "Markdown link target escapes the repository root",
        suite=suite, check=check, path=source, observed=destination,
    ))


class DirectoryInputs:
    """Read actual candidate files with the verifier's existing containment checks."""
    def __init__(self, root: Path, repository_paths: Sequence[str] | None = None) -> None:
        self.root = root.resolve()
        self._paths = None if repository_paths is None else repository_path_observation(repository_paths)

    def read_bytes(self, path: str, *, suite: str | None = None, check: str | None = None) -> bytes:
        return contained_file(self.root, path, suite=suite, check=check).read_bytes()

    def exists(self, path: str) -> bool:
        candidate = contained_path(self.root, path)
        return candidate.exists() or candidate.is_symlink()

    def indexed_paths(self) -> tuple[str, ...]:
        return indexed_paths(self.root) if self._paths is None else self._paths

    def link_target(self, source: str, target: str, *, suite: str, check: str, destination: str) -> str:
        original = contained_file(self.root, source, suite=suite, check=check)
        relative = PurePosixPath(target)
        if relative.is_absolute():
            raise _link_escape(source, destination, suite, check, absolute=True)
        candidate = (original.parent / Path(*relative.parts)).resolve(strict=False) if target else original
        if not candidate.is_relative_to(self.root):
            raise _link_escape(source, destination, suite, check)
        return candidate.relative_to(self.root).as_posix()


class FrozenInputs:
    """One exact regular-file population and its captured byte source."""
    def __init__(self, source: FrozenContentSource, repository_paths: Sequence[str]) -> None:
        self._source = source
        self._paths = repository_path_observation(repository_paths)
        self._files = frozenset(self._paths)
        self._directories = frozenset(
            str(parent) for path in self._paths for parent in PurePosixPath(path).parents
        )
        if self._files & self._directories or not {path for path, _ in source.files} <= self._files:
            raise EngineError(Diagnostic(
                "INPUT.CONTRADICTORY_MEMBERSHIP", "invalid",
                "captured bytes and regular-file repository membership disagree",
            ))

    def read_bytes(self, path: str, *, suite: str | None = None, check: str | None = None) -> bytes:
        selected = str(repository_path(path, suite=suite, check=check))
        if selected in self._directories:
            raise EngineError(Diagnostic(
                "INPUT.NOT_FILE", "invalid", "required input is not a regular file",
                suite=suite, check=check, path=path,
            ))
        if selected not in self._files:
            raise EngineError(Diagnostic(
                "INPUT.UNAVAILABLE", "unavailable", "required input does not exist",
                suite=suite, check=check, path=path,
            ))
        try:
            return self._source.read_bytes(selected)
        except MetadataError as error:
            if error.failure.code != "INPUT.UNAVAILABLE":
                raise
            raise EngineError(Diagnostic(
                "INPUT.UNAVAILABLE", "unavailable", "required input bytes were not captured",
                suite=suite, check=check, path=path,
            )) from error

    def exists(self, path: str) -> bool:
        selected = str(repository_path(path))
        return selected in self._files or selected in self._directories

    def indexed_paths(self) -> tuple[str, ...]:
        return self._paths

    def link_target(self, source: str, target: str, *, suite: str, check: str, destination: str) -> str:
        selected = repository_path(source, suite=suite, check=check)
        relative = PurePosixPath(target)
        if relative.is_absolute():
            raise _link_escape(source, destination, suite, check, absolute=True)
        parts = list(selected.parent.parts) if target else list(selected.parts)
        for component in relative.parts if target else ():
            if component == "..":
                if not parts:
                    raise _link_escape(source, destination, suite, check)
                parts.pop()
            else:
                parts.append(component)
        return str(PurePosixPath(*parts))


def input_source(value: Path | SuiteInputSource) -> SuiteInputSource:
    return DirectoryInputs(value) if isinstance(value, Path) else value
