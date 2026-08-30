from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Iterable, Literal

from .errors import invalid

MAX_AGGREGATE_BYTES = 16 * 1024 * 1024
MAX_CHILD_BYTES = 4 * 1024 * 1024
Lifecycle = Literal["active", "quarantined"]
PutResult = Literal["inserted", "existing-identical"]


def _scalar(value: str, description: str) -> None:
    if type(value) is not str or not value:
        raise invalid("SNAPSHOT.INVALID_VALUE", f"{description} must be nonempty")
    if "\0" in value or any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise invalid(
            "SNAPSHOT.INVALID_VALUE",
            f"{description} must contain Unicode scalar values without NUL",
        )


@dataclass(frozen=True, slots=True, order=True, init=False)
class SnapshotPath:
    components: tuple[str, ...]

    def __init__(self, components: Iterable[str]) -> None:
        if type(components) is str:
            raise invalid(
                "SNAPSHOT.INVALID_PATH",
                "snapshot path components cannot be one string",
            )
        selected = tuple(components)
        if not selected:
            raise invalid("SNAPSHOT.EMPTY_PATH", "snapshot path must be nonempty")
        for component in selected:
            _scalar(component, "path component")
            if component in {".", ".."} or component.casefold() == ".git":
                raise invalid(
                    "SNAPSHOT.CONTROL_PATH", f"path component {component!r} is reserved"
                )
            if "/" in component or "\\" in component:
                raise invalid(
                    "SNAPSHOT.INVALID_PATH",
                    "path components cannot contain separators",
                )
        object.__setattr__(self, "components", selected)

    @classmethod
    def parse(cls, value: str) -> SnapshotPath:
        _scalar(value, "snapshot path")
        if value.startswith("/") or "\\" in value:
            raise invalid(
                "SNAPSHOT.INVALID_PATH", "snapshot path must be relative POSIX form"
            )
        components = value.split("/")
        if any(not component for component in components):
            raise invalid(
                "SNAPSHOT.INVALID_PATH", "snapshot path has an empty component"
            )
        return cls(components)

    def __str__(self) -> str:
        return "/".join(self.components)


@dataclass(frozen=True, slots=True, order=True)
class SnapshotId:
    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str or not self.value.startswith("snapshot:v1:"):
            raise invalid("SNAPSHOT.INVALID_ID", "snapshot ID has an invalid domain")
        raw = self.value.removeprefix("snapshot:v1:")
        try:
            parsed = uuid.UUID(raw)
        except (ValueError, AttributeError) as error:
            raise invalid(
                "SNAPSHOT.INVALID_ID", "snapshot ID UUID is invalid"
            ) from error
        if parsed.version != 4 or str(parsed) != raw:
            raise invalid(
                "SNAPSHOT.INVALID_ID", "snapshot ID requires canonical UUID version 4"
            )

    @classmethod
    def from_uuid(cls, value: uuid.UUID) -> SnapshotId:
        if type(value) is not uuid.UUID or value.version != 4:
            raise invalid(
                "SNAPSHOT.INVALID_ID", "snapshot ID source must be UUID version 4"
            )
        return cls(f"snapshot:v1:{value}")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, order=True)
class SnapshotFile:
    path: SnapshotPath
    content: bytes

    def __post_init__(self) -> None:
        if type(self.path) is not SnapshotPath or type(self.content) is not bytes:
            raise invalid(
                "SNAPSHOT.INVALID_CONTENT",
                "snapshot file requires a SnapshotPath and exact bytes",
            )


@dataclass(frozen=True, slots=True, init=False)
class CapturedContent:
    source_revision: str
    files: tuple[SnapshotFile, ...]

    def __init__(self, source_revision: str, files: Iterable[SnapshotFile]) -> None:
        _scalar(source_revision, "source revision")
        supplied = tuple(files)
        if any(type(item) is not SnapshotFile for item in supplied):
            raise invalid(
                "SNAPSHOT.INVALID_CAPTURE",
                "captured files must be exact SnapshotFile values",
            )
        selected = tuple(sorted(supplied, key=lambda item: item.path))
        paths = tuple(item.path for item in selected)
        if not selected or len(set(paths)) != len(paths):
            raise invalid(
                "SNAPSHOT.INVALID_CAPTURE",
                "captured content must contain unique nonempty paths",
            )
        object.__setattr__(self, "source_revision", source_revision)
        object.__setattr__(self, "files", selected)


@dataclass(frozen=True, slots=True, order=True)
class SnapshotSummary:
    snapshot: SnapshotId
    lifecycle: Lifecycle
    source_revision: str
    created_at: int
    purge_deadline: int | None

    def __post_init__(self) -> None:
        if type(self.snapshot) is not SnapshotId:
            raise invalid("SNAPSHOT.INVALID_SUMMARY", "summary requires a SnapshotId")
        _scalar(self.source_revision, "source revision")
        if (
            self.lifecycle not in ("active", "quarantined")
            or type(self.created_at) is not int
            or self.created_at < 0
            or (
                self.purge_deadline is not None
                and (type(self.purge_deadline) is not int or self.purge_deadline < 0)
            )
            or (self.lifecycle == "active" and self.purge_deadline is not None)
            or (self.lifecycle == "quarantined" and self.purge_deadline is None)
        ):
            raise invalid(
                "SNAPSHOT.INVALID_SUMMARY",
                "summary lifecycle and time fields are contradictory",
            )


@dataclass(frozen=True, slots=True)
class FindSnapshotsRequest:
    lifecycle: Lifecycle = "active"
    after: SnapshotId | None = None
    limit: int = 50

    def __post_init__(self) -> None:
        if self.lifecycle not in ("active", "quarantined"):
            raise invalid("SNAPSHOT.INVALID_LIFECYCLE", "unknown lifecycle filter")
        if type(self.limit) is not int or not 1 <= self.limit <= 500:
            raise invalid(
                "SNAPSHOT.INVALID_LIMIT", "discovery limit must be 1 through 500"
            )
        if self.after is not None and type(self.after) is not SnapshotId:
            raise invalid(
                "SNAPSHOT.INVALID_CONTINUATION",
                "discovery continuation must be a SnapshotId",
            )


@dataclass(frozen=True, slots=True)
class SnapshotPage:
    snapshots: tuple[SnapshotSummary, ...]
    continuation: SnapshotId | None

    def __post_init__(self) -> None:
        if (
            type(self.snapshots) is not tuple
            or any(type(item) is not SnapshotSummary for item in self.snapshots)
            or (
                self.continuation is not None
                and type(self.continuation) is not SnapshotId
            )
        ):
            raise invalid(
                "SNAPSHOT.INVALID_PAGE",
                "snapshot page contains an invalid summary or continuation",
            )


@dataclass(frozen=True, slots=True)
class DeleteSnapshotResult:
    snapshot: SnapshotId
    purge_deadline: int

    def __post_init__(self) -> None:
        if (
            type(self.snapshot) is not SnapshotId
            or type(self.purge_deadline) is not int
            or self.purge_deadline < 0
        ):
            raise invalid(
                "SNAPSHOT.INVALID_DELETION",
                "deletion result requires a SnapshotId and nonnegative deadline",
            )


@dataclass(frozen=True, slots=True, order=True)
class AggregateChild:
    kind: str
    child_id: str
    payload: bytes

    def __post_init__(self) -> None:
        _scalar(self.kind, "child kind")
        _scalar(self.child_id, "child ID")
        if type(self.payload) is not bytes:
            raise invalid(
                "AGGREGATE.INVALID_CHILD", "child payload must be exact bytes"
            )
        if len(self.payload) > MAX_CHILD_BYTES:
            raise invalid(
                "AGGREGATE.CHILD_TOO_LARGE", "child payload exceeds its bound"
            )


@dataclass(frozen=True, slots=True, order=True)
class ChildHandle:
    aggregate_id: str
    kind: str
    child_id: str

    def __post_init__(self) -> None:
        _scalar(self.aggregate_id, "aggregate ID")
        _scalar(self.kind, "child kind")
        _scalar(self.child_id, "child ID")


@dataclass(frozen=True, slots=True, init=False)
class AggregateRecord:
    aggregate_id: str
    kind: str
    payload: bytes
    snapshots: tuple[SnapshotId, ...]
    children: tuple[AggregateChild, ...]

    def __init__(
        self,
        aggregate_id: str,
        kind: str,
        payload: bytes,
        snapshots: Iterable[SnapshotId],
        children: Iterable[AggregateChild] = (),
    ) -> None:
        _scalar(aggregate_id, "aggregate ID")
        _scalar(kind, "aggregate kind")
        if type(payload) is not bytes or len(payload) > MAX_AGGREGATE_BYTES:
            raise invalid(
                "AGGREGATE.INVALID_PAYLOAD",
                "aggregate payload must be exact bytes within its bound",
            )
        supplied_snapshots = tuple(snapshots)
        if any(type(item) is not SnapshotId for item in supplied_snapshots):
            raise invalid(
                "AGGREGATE.INVALID_DEPENDENCIES",
                "aggregate dependencies must be exact SnapshotId values",
            )
        selected_snapshots = tuple(sorted(supplied_snapshots))
        if not selected_snapshots or len(set(selected_snapshots)) != len(
            selected_snapshots
        ):
            raise invalid(
                "AGGREGATE.INVALID_DEPENDENCIES",
                "aggregate must depend on unique nonempty snapshot roots",
            )
        supplied_children = tuple(children)
        if any(type(item) is not AggregateChild for item in supplied_children):
            raise invalid(
                "AGGREGATE.INVALID_CHILD",
                "aggregate children must be exact AggregateChild values",
            )
        selected_children = tuple(sorted(supplied_children))
        keys = tuple((item.kind, item.child_id) for item in selected_children)
        if len(set(keys)) != len(keys):
            raise invalid(
                "AGGREGATE.DUPLICATE_CHILD", "aggregate child keys must be unique"
            )
        object.__setattr__(self, "aggregate_id", aggregate_id)
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "payload", payload)
        object.__setattr__(self, "snapshots", selected_snapshots)
        object.__setattr__(self, "children", selected_children)


__all__ = (
    "AggregateChild",
    "AggregateRecord",
    "CapturedContent",
    "ChildHandle",
    "DeleteSnapshotResult",
    "FindSnapshotsRequest",
    "Lifecycle",
    "MAX_AGGREGATE_BYTES",
    "MAX_CHILD_BYTES",
    "PutResult",
    "SnapshotFile",
    "SnapshotId",
    "SnapshotPage",
    "SnapshotPath",
    "SnapshotSummary",
)
