from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from typing import Any

from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    IdentityValue,
    encode_identity_value,
    hash_identity,
)


def analysis_key(value: Any) -> IdentityValue:
    value_type = type(value)
    if value is None or value_type in {bool, int, str}:
        return value
    if isinstance(value, Mapping):
        if any(type(key) is not str for key in value):
            raise TypeError("analysis key object members must use exact string keys")
        return IdentityObject(
            (key, analysis_key(item))
            for key, item in value.items()
        )
    if isinstance(value, Sequence) and not isinstance(
        value,
        (str, bytes, bytearray),
    ):
        return IdentityArray(analysis_key(item) for item in value)
    raise TypeError(f"unsupported analysis key value: {value_type.__name__}")


def analysis_key_bytes(value: Any) -> bytes:
    return encode_identity_value(analysis_key(value))


def raw_digest(value: bytes) -> str:
    return f"sha256:{hashlib.sha256(value).hexdigest()}"


def analysis_value_digest(value: Any) -> str:
    return raw_digest(analysis_key_bytes(value))


def analysis_identity(domain: str, prefix: str, value: Any) -> str:
    return hash_identity(domain, prefix, analysis_key(value))


__all__ = (
    "analysis_identity",
    "analysis_key",
    "analysis_key_bytes",
    "analysis_value_digest",
    "raw_digest",
)
