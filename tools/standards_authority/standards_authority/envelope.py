from __future__ import annotations

import json

from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityError,
    IdentityObject,
    IdentityValue,
    encode_identity_value,
)

from .errors import AuthorityError, invalid, unsupported
from .model import (
    MAX_ENVELOPE_BYTES,
    AuthorityEnvelope,
    AuthorityHandle,
    AuthorityReference,
)

_ENVELOPE_FIELDS = {
    "envelope_kind",
    "envelope_version",
    "object_kind",
    "semantic_id",
    "direct_dependencies",
    "payload_contract",
    "payload",
}
_REFERENCE_FIELDS = {"object_kind", "semantic_id"}


class _ObjectPairs(list[tuple[str, object]]):
    pass


def encode_envelope(envelope: AuthorityEnvelope) -> bytes:
    dependencies = IdentityArray(
        IdentityObject(
            (
                ("object_kind", reference.object_kind),
                ("semantic_id", reference.semantic_id),
            )
        )
        for reference in envelope.direct_dependencies
    )
    value = IdentityObject(
        (
            ("envelope_kind", "authority-envelope"),
            ("envelope_version", 1),
            ("object_kind", envelope.object_kind),
            ("semantic_id", envelope.semantic_id),
            ("direct_dependencies", dependencies),
            ("payload_contract", envelope.payload_contract),
            ("payload", envelope.payload),
        )
    )
    try:
        encoded = encode_identity_value(value)
    except IdentityError as error:
        raise invalid("AUTHORITY.INVALID_ENVELOPE", str(error)) from error
    if len(encoded) > MAX_ENVELOPE_BYTES:
        raise unsupported(
            "AUTHORITY.ENVELOPE_TOO_LARGE",
            f"canonical envelope exceeds {MAX_ENVELOPE_BYTES} bytes",
        )
    return encoded


def decode_envelope(encoded: bytes) -> AuthorityEnvelope:
    if type(encoded) is not bytes:
        raise invalid("AUTHORITY.INVALID_ENVELOPE_BYTES", "envelope must be bytes")
    if len(encoded) > MAX_ENVELOPE_BYTES:
        raise unsupported(
            "AUTHORITY.ENVELOPE_TOO_LARGE",
            f"encoded envelope exceeds {MAX_ENVELOPE_BYTES} bytes",
        )
    try:
        raw = json.loads(
            encoded,
            object_pairs_hook=_ObjectPairs,
            parse_int=_parse_integer,
            parse_float=_reject_non_integer,
            parse_constant=_reject_non_integer,
        )
        value = _to_identity(raw)
    except AuthorityError:
        raise
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        RecursionError,
        TypeError,
        ValueError,
    ) as error:
        raise invalid("AUTHORITY.MALFORMED_ENVELOPE", str(error)) from error
    if type(value) is not IdentityObject:
        raise invalid("AUTHORITY.INVALID_ENVELOPE", "envelope must be an object")
    members = dict(value.members)
    if set(members) != _ENVELOPE_FIELDS:
        raise invalid(
            "AUTHORITY.INVALID_ENVELOPE_FIELDS",
            "envelope must contain exactly the seven v1 fields",
        )
    kind = members["envelope_kind"]
    version = members["envelope_version"]
    if type(kind) is not str:
        raise invalid(
            "AUTHORITY.INVALID_ENVELOPE_KIND", "envelope kind must be a string"
        )
    if kind != "authority-envelope":
        raise unsupported(
            "AUTHORITY.UNSUPPORTED_ENVELOPE_KIND",
            f"unsupported envelope kind {kind!r}",
        )
    if type(version) is not int or version <= 0:
        raise invalid(
            "AUTHORITY.INVALID_ENVELOPE_VERSION",
            "envelope version must be a positive integer",
        )
    if version != 1:
        raise unsupported(
            "AUTHORITY.UNSUPPORTED_ENVELOPE_VERSION",
            f"unsupported envelope version {version}",
        )
    dependencies = _decode_references(members["direct_dependencies"])
    envelope = AuthorityEnvelope(
        object_kind=_exact_string(members["object_kind"], "object_kind"),
        semantic_id=_exact_string(members["semantic_id"], "semantic_id"),
        direct_dependencies=dependencies,
        payload_contract=_exact_string(members["payload_contract"], "payload_contract"),
        payload=members["payload"],
    )
    if encode_envelope(envelope) != encoded:
        raise invalid(
            "AUTHORITY.NONCANONICAL_ENVELOPE",
            "envelope bytes are not the canonical identity-v2 encoding",
        )
    return envelope


def encode_storage_key(handle: AuthorityHandle) -> str:
    return encode_identity_value(
        IdentityObject(
            (
                ("object_kind", handle.object_kind),
                ("semantic_id", handle.semantic_id),
            )
        )
    ).decode("utf-8")


def _decode_references(value: IdentityValue) -> tuple[AuthorityReference, ...]:
    if type(value) is not IdentityArray:
        raise invalid(
            "AUTHORITY.INVALID_DEPENDENCIES", "direct_dependencies must be an array"
        )
    references: list[AuthorityReference] = []
    for item in value.values:
        if type(item) is not IdentityObject:
            raise invalid(
                "AUTHORITY.INVALID_REFERENCE", "dependency reference must be an object"
            )
        members = dict(item.members)
        if set(members) != _REFERENCE_FIELDS:
            raise invalid(
                "AUTHORITY.INVALID_REFERENCE_FIELDS",
                "dependency reference must contain exactly object_kind and semantic_id",
            )
        references.append(
            AuthorityReference(
                _exact_string(members["object_kind"], "reference object_kind"),
                _exact_string(members["semantic_id"], "reference semantic_id"),
            )
        )
    return tuple(references)


def _to_identity(value: object) -> IdentityValue:
    if value is None or type(value) in {bool, int, str}:
        return value  # type: ignore[return-value]
    if type(value) is list:
        return IdentityArray(_to_identity(item) for item in value)
    if type(value) is _ObjectPairs:
        keys: set[str] = set()
        members: list[tuple[str, IdentityValue]] = []
        for key, member in value:
            if key in keys:
                raise invalid(
                    "AUTHORITY.DUPLICATE_OBJECT_KEY", f"duplicate object key {key!r}"
                )
            keys.add(key)
            members.append((key, _to_identity(member)))
        try:
            return IdentityObject(members)
        except IdentityError as error:
            raise invalid("AUTHORITY.INVALID_IDENTITY_VALUE", str(error)) from error
    raise invalid(
        "AUTHORITY.INVALID_IDENTITY_VALUE",
        "envelope contains a value outside identity encoding v2",
    )


def _exact_string(value: IdentityValue, field: str) -> str:
    if type(value) is not str or not value:
        raise invalid("AUTHORITY.INVALID_STRING", f"{field} must be a nonempty string")
    return value


def _reject_non_integer(value: str) -> object:
    raise invalid(
        "AUTHORITY.INVALID_NUMBER",
        f"identity encoding v2 does not admit non-integer number {value!r}",
    )


def _parse_integer(value: str) -> int:
    negative = value.startswith("-")
    digits = value[1:] if negative else value
    result = 0
    first = len(digits) % 9 or 9
    offset = 0
    while offset < len(digits):
        width = first if offset == 0 else 9
        chunk = digits[offset : offset + width]
        result = result * (10**width) + int(chunk)
        offset += width
    return -result if negative else result


__all__ = ("decode_envelope", "encode_envelope", "encode_storage_key")
