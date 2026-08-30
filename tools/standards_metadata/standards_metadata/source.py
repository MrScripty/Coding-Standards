from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Protocol

from .errors import MetadataError, MetadataFailure
from .paths import contained_file, normalized_repository_path


class ContentSource(Protocol):
    """Read exact bytes by normalized logical repository path."""

    def read_bytes(self, path: str) -> bytes: ...


class DirectoryContentSource:
    """Filesystem Adapter for repository tools and focused fixtures."""

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()

    def read_bytes(self, path: str) -> bytes:
        return contained_file(self._root, path).read_bytes()


class FrozenContentSource:
    """Immutable in-memory Adapter over an exact logical path-byte set."""

    def __init__(
        self,
        files: Mapping[str, bytes] | Iterable[tuple[str, bytes]],
    ) -> None:
        items = files.items() if isinstance(files, Mapping) else files
        selected: dict[str, bytes] = {}
        for raw_path, raw_content in items:
            path = str(normalized_repository_path(raw_path))
            content = bytes(raw_content)
            previous = selected.get(path)
            if previous is not None and previous != content:
                raise MetadataError(
                    MetadataFailure(
                        "CONTENT.CONTRADICTORY_PATH",
                        "invalid",
                        "one logical path cannot identify different bytes",
                        path=path,
                    )
                )
            selected[path] = content
        self._files = selected

    def read_bytes(self, path: str) -> bytes:
        normalized = str(normalized_repository_path(path))
        try:
            return self._files[normalized]
        except KeyError as error:
            raise MetadataError(
                MetadataFailure(
                    "INPUT.UNAVAILABLE",
                    "unavailable",
                    "required input does not exist",
                    path=normalized,
                )
            ) from error

    @property
    def files(self) -> tuple[tuple[str, bytes], ...]:
        return tuple(sorted(self._files.items()))


class RecordingContentSource:
    """Record exact reads while rejecting mutable or contradictory results."""

    def __init__(self, source: ContentSource) -> None:
        self._source = source
        self._requested: dict[str, bytes] = {}

    def read_bytes(self, path: str) -> bytes:
        normalized = str(normalized_repository_path(path))
        content = bytes(self._source.read_bytes(normalized))
        previous = self._requested.get(normalized)
        if previous is not None and previous != content:
            raise MetadataError(
                MetadataFailure(
                    "CONTENT.CONTRADICTORY_READ",
                    "invalid",
                    "a logical path changed during one authority compilation",
                    path=normalized,
                )
            )
        self._requested[normalized] = content
        return content

    def freeze(self) -> FrozenContentSource:
        return FrozenContentSource(self._requested)

    @property
    def requested_paths(self) -> tuple[str, ...]:
        return tuple(sorted(self._requested))


ContentSourceInput = ContentSource | Path


def content_source(value: ContentSourceInput) -> ContentSource:
    if isinstance(value, Path):
        return DirectoryContentSource(value)
    return value
