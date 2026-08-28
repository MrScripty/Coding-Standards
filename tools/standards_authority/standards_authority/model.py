from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Literal, Protocol, TypeVar

from tools.standards_identity.standards_identity import IdentityValue

from .errors import invalid

MAX_ENVELOPE_BYTES = 67_108_864


def validate_scalar(value: object, field: str, *, nonempty: bool = False) -> str:
    if type(value) is not str:
        raise invalid("AUTHORITY.INVALID_STRING", f"{field} must be a string")
    if nonempty and not value:
        raise invalid("AUTHORITY.EMPTY_STRING", f"{field} must not be empty")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise invalid(
            "AUTHORITY.INVALID_UNICODE",
            f"{field} must contain only Unicode scalar values",
        )
    return value


@dataclass(frozen=True, slots=True, order=True)
class AuthorityReference:
    object_kind: str
    semantic_id: str

    def __post_init__(self) -> None:
        validate_scalar(self.object_kind, "object_kind", nonempty=True)
        validate_scalar(self.semantic_id, "semantic_id", nonempty=True)


@dataclass(frozen=True, slots=True)
class AuthorityHandle:
    object_kind: str
    semantic_id: str

    def __post_init__(self) -> None:
        validate_scalar(self.object_kind, "object_kind", nonempty=True)
        validate_scalar(self.semantic_id, "semantic_id", nonempty=True)

    @property
    def reference(self) -> AuthorityReference:
        return AuthorityReference(self.object_kind, self.semantic_id)


@dataclass(frozen=True, slots=True)
class AuthorityEnvelope:
    object_kind: str
    semantic_id: str
    direct_dependencies: tuple[AuthorityReference, ...]
    payload_contract: str
    payload: IdentityValue

    def __post_init__(self) -> None:
        validate_scalar(self.object_kind, "object_kind", nonempty=True)
        validate_scalar(self.semantic_id, "semantic_id", nonempty=True)
        validate_scalar(self.payload_contract, "payload_contract", nonempty=True)
        expected = tuple(sorted(self.direct_dependencies))
        if self.direct_dependencies != expected:
            raise invalid(
                "AUTHORITY.UNSORTED_DEPENDENCIES",
                "direct dependencies must be sorted by object kind and semantic ID",
            )
        if len(set(self.direct_dependencies)) != len(self.direct_dependencies):
            raise invalid(
                "AUTHORITY.DUPLICATE_DEPENDENCY",
                "direct dependencies must be unique",
            )

    @property
    def handle(self) -> AuthorityHandle:
        return AuthorityHandle(self.object_kind, self.semantic_id)


T = TypeVar("T")


class CodecContext(Protocol):
    def resolve(self, reference: AuthorityReference) -> object: ...

    def transitive_dependencies(
        self, roots: Iterable[AuthorityReference]
    ) -> tuple[AuthorityReference, ...]: ...


class AuthorityCodec(Protocol, Generic[T]):
    object_kind: str
    payload_contract: str
    allowed_dependency_kinds: frozenset[str]

    def encode(self, value: T) -> IdentityValue: ...

    def decode(self, payload: IdentityValue, context: CodecContext) -> T: ...

    def semantic_id(self, value: T, context: CodecContext) -> str: ...

    def direct_dependencies(self, value: T) -> tuple[AuthorityReference, ...]: ...


@dataclass(frozen=True, slots=True, init=False)
class CodecSet:
    codecs: tuple[AuthorityCodec[object], ...]

    def __init__(self, codecs: Iterable[AuthorityCodec[object]]) -> None:
        exact = tuple(codecs)
        kinds: set[str] = set()
        contracts: set[tuple[str, str]] = set()
        for codec in exact:
            validate_scalar(codec.object_kind, "codec object_kind", nonempty=True)
            validate_scalar(
                codec.payload_contract, "codec payload_contract", nonempty=True
            )
            if codec.object_kind in kinds:
                raise invalid(
                    "AUTHORITY.DUPLICATE_CODEC_KIND",
                    f"duplicate codec for {codec.object_kind!r}",
                )
            key = (codec.object_kind, codec.payload_contract)
            if key in contracts:
                raise invalid(
                    "AUTHORITY.DUPLICATE_CODEC_CONTRACT",
                    f"duplicate codec contract {key!r}",
                )
            kinds.add(codec.object_kind)
            contracts.add(key)
        object.__setattr__(self, "codecs", exact)


PutResult = Literal["inserted", "existing-identical"]


@dataclass(frozen=True, slots=True)
class RecoveryReceipt:
    source: str
    destination: str
    source_digest: str
    destination_digest: str


__all__ = (
    "AuthorityCodec",
    "AuthorityEnvelope",
    "AuthorityHandle",
    "AuthorityReference",
    "CodecContext",
    "CodecSet",
    "MAX_ENVELOPE_BYTES",
    "PutResult",
    "RecoveryReceipt",
    "validate_scalar",
)
