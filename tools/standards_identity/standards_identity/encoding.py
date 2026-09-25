from __future__ import annotations

import hashlib
import re
import struct
from dataclasses import dataclass
from typing import Iterable, TypeAlias, Union

from .errors import invalid

_FRAME_PREFIX = b"coding-standards:identity:v2\0"
_DOMAIN = re.compile(r"[a-z0-9][a-z0-9.:-]*\Z", re.ASCII)
_ID_PREFIX = re.compile(r"[a-z][a-z0-9.-]*\Z", re.ASCII)
_DECIMAL_CHUNK_BASE = 1_000_000_000
_DECIMAL_CHUNK_WIDTH = 9
# Exact decimal tokens for the byte domain; larger integers retain the
# arbitrary-precision encoder and its independence from Python's digit limit.
_BYTE_TOKENS = tuple(str(value).encode("ascii") for value in range(256))
# Bound the temporary join index for large byte arrays; encoded output remains exact.
_BYTE_CHUNK_SIZE = 64 * 1024
_SURROGATE = re.compile(r"[\ud800-\udfff]")
_ESCAPED_CHARACTER = re.compile(r'["\\\x00-\x1f]')
_STRING_ESCAPES = {
    '"': '\\"',
    "\\": "\\\\",
    **{chr(value): f"\\u{value:04x}" for value in range(32)},
}


@dataclass(frozen=True, slots=True, init=False, eq=False, repr=False)
class IdentityArray:
    # Exact bytes already prove the element domain and immutable ownership.
    # Other iterables retain the existing validated tuple representation.
    _values: tuple[IdentityValue, ...] | bytes

    def __init__(self, values: Iterable[IdentityValue]) -> None:
        if type(values) is bytes:
            immutable = values
        else:
            immutable = tuple(values)
            for value in immutable:
                _validate_value(value)
        object.__setattr__(self, "_values", immutable)

    @property
    def values(self) -> tuple[IdentityValue, ...]:
        """Expose the same immutable element sequence for either storage form."""
        return tuple(self._values)

    def __eq__(self, other: object) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        if type(self._values) is type(other._values):
            return self._values == other._values
        return self.values == other.values

    def __hash__(self) -> int:
        return hash((self.values,))

    def __repr__(self) -> str:
        return f"IdentityArray(values={self.values!r})"


@dataclass(frozen=True, slots=True, init=False)
class IdentityObject:
    members: tuple[tuple[str, IdentityValue], ...]

    def __init__(self, members: Iterable[tuple[str, IdentityValue]]) -> None:
        immutable = tuple(members)
        seen: set[str] = set()
        normalized: list[tuple[str, IdentityValue]] = []
        for member in immutable:
            if type(member) is not tuple or len(member) != 2:
                raise invalid(
                    "IDENTITY.INVALID_OBJECT_MEMBER",
                    "object members must be two-item tuples",
                )
            key, value = member
            if type(key) is not str:
                raise invalid(
                    "IDENTITY.INVALID_OBJECT_KEY",
                    "object keys must be exact strings",
                )
            _validate_scalar_string(key)
            if key in seen:
                raise invalid(
                    "IDENTITY.DUPLICATE_OBJECT_KEY",
                    f"duplicate object key {key!r}",
                )
            _validate_value(value)
            seen.add(key)
            normalized.append((key, value))
        normalized.sort(key=lambda item: tuple(map(ord, item[0])))
        object.__setattr__(self, "members", tuple(normalized))


IdentityValue: TypeAlias = Union[
    None,
    bool,
    int,
    str,
    IdentityArray,
    IdentityObject,
]


def encode_identity_value(value: IdentityValue) -> bytes:
    """Encode one immutable identity-v2 value exactly."""
    _validate_value(value)
    return _encode(value)


def hash_identity(domain: str, id_prefix: str, value: IdentityValue) -> str:
    """Hash an owner-defined identity record in the identity-v2 frame."""
    if type(domain) is not str or _DOMAIN.fullmatch(domain) is None:
        raise invalid(
            "IDENTITY.INVALID_DOMAIN",
            "domain must match [a-z0-9][a-z0-9.:-]*",
        )
    if type(id_prefix) is not str or _ID_PREFIX.fullmatch(id_prefix) is None:
        raise invalid(
            "IDENTITY.INVALID_PREFIX",
            "ID prefix must match [a-z][a-z0-9.-]*",
        )

    domain_bytes = domain.encode("ascii")
    prefix_bytes = id_prefix.encode("ascii")
    encoded = encode_identity_value(value)
    if len(domain_bytes) > 0xFFFF_FFFF or len(prefix_bytes) > 0xFFFF_FFFF:
        raise invalid("IDENTITY.FRAME_TOO_LARGE", "domain or prefix exceeds u32")
    if len(encoded) > 0xFFFF_FFFF_FFFF_FFFF:
        raise invalid("IDENTITY.FRAME_TOO_LARGE", "encoded value exceeds u64")

    frame = b"".join(
        (
            _FRAME_PREFIX,
            struct.pack(">I", len(domain_bytes)),
            domain_bytes,
            struct.pack(">I", len(prefix_bytes)),
            prefix_bytes,
            struct.pack(">Q", len(encoded)),
            encoded,
        )
    )
    return f"{id_prefix}:sha256:{hashlib.sha256(frame).hexdigest()}"


def frame_path_bytes(path: Iterable[str], content: bytes) -> IdentityObject:
    """Frame one caller-validated logical path and exact byte string."""
    if type(path) is str:
        raise invalid(
            "IDENTITY.INVALID_PATH_FRAME",
            "path components cannot be supplied as one string",
        )
    components = tuple(path)
    if not components or any(type(component) is not str for component in components):
        raise invalid(
            "IDENTITY.INVALID_PATH_FRAME",
            "path frame requires nonempty exact string components",
        )
    if type(content) is not bytes:
        raise invalid("IDENTITY.INVALID_BYTES_FRAME", "byte frame requires exact bytes")
    return IdentityObject(
        (
            ("path", IdentityArray(components)),
            ("bytes", IdentityArray(content)),
        )
    )


def frame_path_byte_set(
    entries: Iterable[tuple[Iterable[str], bytes]],
) -> IdentityArray:
    """Frame a path-keyed byte set in codepoint path order."""
    selected: list[tuple[tuple[str, ...], IdentityObject]] = []
    for path, content in entries:
        components = tuple(path)
        selected.append((components, frame_path_bytes(components, content)))
    selected.sort(key=lambda item: tuple(tuple(map(ord, part)) for part in item[0]))
    paths = tuple(path for path, _frame in selected)
    if not selected or len(set(paths)) != len(paths):
        raise invalid(
            "IDENTITY.INVALID_PATH_SET",
            "path-byte set must be nonempty with unique paths",
        )
    return IdentityArray(frame for _path, frame in selected)


def _validate_value(value: object) -> None:
    value_type = type(value)
    if value is None or value_type is bool or value_type is int:
        return
    if value_type is str:
        _validate_scalar_string(value)
        return
    if value_type is IdentityArray or value_type is IdentityObject:
        return
    raise invalid(
        "IDENTITY.INVALID_VALUE",
        "identity values must be immutable supported exact types",
    )


def _validate_scalar_string(value: str) -> None:
    if _SURROGATE.search(value) is not None:
        raise invalid(
            "IDENTITY.INVALID_UNICODE",
            "strings must contain Unicode scalar values",
        )


def _encode(value: IdentityValue) -> bytes:
    value_type = type(value)
    if value is None:
        return b"null"
    if value_type is bool:
        return b"true" if value else b"false"
    if value_type is int:
        return _BYTE_TOKENS[value] if 0 <= value < 256 else _encode_integer(value)
    if value_type is str:
        return _encode_string(value)
    if value_type is IdentityArray:
        if type(value._values) is bytes:
            return _encode_byte_array(value._values)
        return b"[" + b",".join(_encode(item) for item in value._values) + b"]"
    if value_type is IdentityObject:
        encoded_members = (
            _encode_string(key) + b":" + _encode(member_value)
            for key, member_value in value.members
        )
        return b"{" + b",".join(encoded_members) + b"}"
    raise AssertionError("validated identity value has an unknown type")


def _encode_byte_array(value: bytes) -> bytes:
    """Emit identity-v2 integer-array syntax with bounded per-byte join scratch."""
    chunks = (
        b",".join(map(_BYTE_TOKENS.__getitem__, value[start : start + _BYTE_CHUNK_SIZE]))
        for start in range(0, len(value), _BYTE_CHUNK_SIZE)
    )
    return b"[" + b",".join(chunks) + b"]"


def _encode_integer(value: int) -> bytes:
    if value == 0:
        return b"0"
    negative = value < 0
    remaining = -value if negative else value
    chunks: list[int] = []
    while remaining:
        remaining, chunk = divmod(remaining, _DECIMAL_CHUNK_BASE)
        chunks.append(chunk)
    encoded = str(chunks.pop()).encode("ascii")
    suffix = b"".join(
        f"{chunk:0{_DECIMAL_CHUNK_WIDTH}d}".encode("ascii")
        for chunk in reversed(chunks)
    )
    return (b"-" if negative else b"") + encoded + suffix


def _encode_string(value: str) -> bytes:
    # The pattern copies ordinary Unicode segments as a whole. Controls keep
    # identity-v2's lowercase \u00xx spelling rather than JSON's short escapes.
    escaped = _ESCAPED_CHARACTER.sub(lambda match: _STRING_ESCAPES[match[0]], value)
    return b'"' + escaped.encode("utf-8") + b'"'


__all__ = (
    "IdentityArray",
    "IdentityObject",
    "IdentityValue",
    "encode_identity_value",
    "frame_path_byte_set",
    "frame_path_bytes",
    "hash_identity",
)
