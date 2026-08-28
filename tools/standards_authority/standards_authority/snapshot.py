from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass
from typing import Iterable

from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    IdentityValue,
    hash_identity,
)

from .errors import invalid
from .model import AuthorityReference, CodecContext, validate_scalar


@dataclass(frozen=True, slots=True, order=True, init=False)
class RepositoryPath:
    components: tuple[str, ...]

    def __init__(self, components: Iterable[str]) -> None:
        exact = tuple(components)
        if not exact:
            raise invalid("CAPTURE.EMPTY_PATH", "repository path must not be empty")
        for component in exact:
            validate_scalar(component, "path component", nonempty=True)
            encoded = component.encode("utf-8")
            if len(encoded) > 255:
                raise invalid(
                    "CAPTURE.COMPONENT_TOO_LONG",
                    "path component exceeds 255 UTF-8 bytes",
                )
            if component in {".", "..", ".git"}:
                raise invalid(
                    "CAPTURE.CONTROL_PATH", f"path component {component!r} is reserved"
                )
            if "/" in component or "\0" in component:
                raise invalid(
                    "CAPTURE.INVALID_COMPONENT",
                    "path component contains slash or NUL",
                )
        object.__setattr__(self, "components", exact)

    def __str__(self) -> str:
        return "/".join(self.components)


@dataclass(frozen=True, slots=True, order=True)
class SnapshotFile:
    path: RepositoryPath
    content: bytes

    def __post_init__(self) -> None:
        if type(self.content) is not bytes:
            raise invalid("CAPTURE.INVALID_CONTENT", "snapshot content must be bytes")


@dataclass(frozen=True, slots=True, init=False)
class CaptureRequest:
    files: tuple[RepositoryPath, ...]

    def __init__(self, files: Iterable[RepositoryPath]) -> None:
        exact = tuple(sorted(files))
        if not exact:
            raise invalid("CAPTURE.EMPTY_REQUEST", "capture request must not be empty")
        if len(set(exact)) != len(exact):
            raise invalid("CAPTURE.DUPLICATE_PATH", "capture paths must be unique")
        object.__setattr__(self, "files", exact)


@dataclass(frozen=True, slots=True, init=False)
class ContentSnapshot:
    files: tuple[SnapshotFile, ...]

    def __init__(self, files: Iterable[SnapshotFile]) -> None:
        exact = tuple(sorted(files, key=lambda item: item.path))
        if not exact:
            raise invalid(
                "CAPTURE.EMPTY_SNAPSHOT", "content snapshot must not be empty"
            )
        paths = tuple(item.path for item in exact)
        if len(set(paths)) != len(paths):
            raise invalid("CAPTURE.DUPLICATE_PATH", "snapshot paths must be unique")
        object.__setattr__(self, "files", exact)


class ContentSnapshotCodec:
    object_kind = "content-snapshot"
    payload_contract = "content-snapshot.v2"
    allowed_dependency_kinds = frozenset[str]()

    def encode(self, value: ContentSnapshot) -> IdentityValue:
        return IdentityObject(
            (
                (
                    "files",
                    IdentityArray(self._encode_file(item) for item in value.files),
                ),
            )
        )

    def decode(self, payload: IdentityValue, context: CodecContext) -> ContentSnapshot:
        del context
        members = _members(payload, {"files"}, "snapshot")
        raw_files = members["files"]
        if type(raw_files) is not IdentityArray:
            raise invalid("CAPTURE.INVALID_FILES", "files must be an array")
        files: list[SnapshotFile] = []
        for raw_file in raw_files.values:
            item = _members(
                raw_file,
                {"path", "content_base64", "sha256", "byte_length"},
                "snapshot file",
            )
            raw_path = item["path"]
            if type(raw_path) is not IdentityArray or not all(
                type(component) is str for component in raw_path.values
            ):
                raise invalid("CAPTURE.INVALID_PATH", "path must be a string array")
            encoded = _string(item["content_base64"], "content_base64")
            try:
                content = base64.b64decode(encoded, validate=True)
            except ValueError as error:
                raise invalid("CAPTURE.INVALID_BASE64", str(error)) from error
            canonical = base64.b64encode(content).decode("ascii")
            if encoded != canonical:
                raise invalid(
                    "CAPTURE.NONCANONICAL_BASE64",
                    "content Base64 is not padded canonical",
                )
            length = item["byte_length"]
            if type(length) is not int or length < 0 or length != len(content):
                raise invalid(
                    "CAPTURE.LENGTH_MISMATCH", "byte length does not match content"
                )
            digest = _string(item["sha256"], "sha256")
            if digest != hashlib.sha256(content).hexdigest():
                raise invalid(
                    "CAPTURE.DIGEST_MISMATCH", "SHA-256 does not match content"
                )
            files.append(
                SnapshotFile(RepositoryPath(raw_path.values), content)  # type: ignore[arg-type]
            )
        return ContentSnapshot(files)

    def semantic_id(self, value: ContentSnapshot, context: CodecContext) -> str:
        del context
        material = IdentityObject(
            (
                (
                    "files",
                    IdentityArray(
                        IdentityObject(
                            (
                                ("path", IdentityArray(item.path.components)),
                                (
                                    "exact_bytes",
                                    IdentityArray(int(byte) for byte in item.content),
                                ),
                            )
                        )
                        for item in value.files
                    ),
                ),
            )
        )
        return hash_identity(
            "coding-standards:content-snapshot:v2", "content-snapshot", material
        )

    def direct_dependencies(
        self, value: ContentSnapshot
    ) -> tuple[AuthorityReference, ...]:
        del value
        return ()

    @staticmethod
    def _encode_file(item: SnapshotFile) -> IdentityObject:
        return IdentityObject(
            (
                ("path", IdentityArray(item.path.components)),
                ("content_base64", base64.b64encode(item.content).decode("ascii")),
                ("sha256", hashlib.sha256(item.content).hexdigest()),
                ("byte_length", len(item.content)),
            )
        )


def _members(
    value: IdentityValue, expected: set[str], description: str
) -> dict[str, IdentityValue]:
    if type(value) is not IdentityObject:
        raise invalid("CAPTURE.INVALID_PAYLOAD", f"{description} must be an object")
    members = dict(value.members)
    if set(members) != expected:
        raise invalid(
            "CAPTURE.INVALID_PAYLOAD_FIELDS",
            f"{description} fields differ from the payload contract",
        )
    return members


def _string(value: IdentityValue, field: str) -> str:
    if type(value) is not str:
        raise invalid("CAPTURE.INVALID_PAYLOAD", f"{field} must be a string")
    return value


CONTENT_SNAPSHOT_CODEC = ContentSnapshotCodec()

__all__ = (
    "CONTENT_SNAPSHOT_CODEC",
    "CaptureRequest",
    "ContentSnapshot",
    "ContentSnapshotCodec",
    "RepositoryPath",
    "SnapshotFile",
)
