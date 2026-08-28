from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Literal, TypeVar

from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    IdentityValue,
    hash_identity,
)

from .errors import invalid
from .model import AuthorityReference, CodecContext, validate_scalar

Operation = Literal["route", "read", "related", "analysis"]
T = TypeVar("T")


@dataclass(frozen=True, slots=True, order=True)
class ExecutionAuthorityRoot:
    side: str
    role: str
    reference: AuthorityReference

    def __post_init__(self) -> None:
        validate_scalar(self.side, "execution side", nonempty=True)
        validate_scalar(self.role, "execution role", nonempty=True)


@dataclass(frozen=True, slots=True, init=False)
class ExecutionClosure:
    operation: Operation
    roots: tuple[ExecutionAuthorityRoot, ...]

    def __init__(
        self, operation: Operation, roots: Iterable[ExecutionAuthorityRoot]
    ) -> None:
        if operation not in {"route", "read", "related", "analysis"}:
            raise invalid("AUTHORITY.INVALID_OPERATION", repr(operation))
        exact = tuple(sorted(roots))
        if not exact:
            raise invalid(
                "AUTHORITY.EMPTY_CLOSURE", "execution roots must not be empty"
            )
        keys = tuple(
            (
                item.side,
                item.role,
                item.reference.object_kind,
                item.reference.semantic_id,
            )
            for item in exact
        )
        if len(set(keys)) != len(keys):
            raise invalid("AUTHORITY.DUPLICATE_ROOT", "execution roots must be unique")
        object.__setattr__(self, "operation", operation)
        object.__setattr__(self, "roots", exact)


@dataclass(frozen=True, slots=True, init=False)
class AuthorityBoundValue(Generic[T]):
    value: T
    direct_dependencies: tuple[ExecutionAuthorityRoot, ...]

    def __init__(self, value: T, direct_dependencies: Iterable[ExecutionAuthorityRoot]):
        exact = tuple(sorted(direct_dependencies))
        if len(set(exact)) != len(exact):
            raise invalid(
                "AUTHORITY.DUPLICATE_BOUND_DEPENDENCY",
                "authority-bound dependencies must be unique",
            )
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "direct_dependencies", exact)


class ExecutionClosureCodec:
    object_kind = "execution-closure"
    payload_contract = "execution-closure.v2"

    def __init__(self, allowed_dependency_kinds: Iterable[str]) -> None:
        self.allowed_dependency_kinds = frozenset(allowed_dependency_kinds)

    def encode(self, value: ExecutionClosure) -> IdentityValue:
        return IdentityObject(
            (
                ("operation", value.operation),
                ("roots", IdentityArray(_root_value(root) for root in value.roots)),
            )
        )

    def decode(self, payload: IdentityValue, context: CodecContext) -> ExecutionClosure:
        del context
        members = _members(payload, {"operation", "roots"}, "execution closure")
        operation = members["operation"]
        raw_roots = members["roots"]
        if type(operation) is not str or operation not in {
            "route",
            "read",
            "related",
            "analysis",
        }:
            raise invalid("AUTHORITY.INVALID_OPERATION", repr(operation))
        if type(raw_roots) is not IdentityArray:
            raise invalid("AUTHORITY.INVALID_ROOTS", "roots must be an array")
        roots: list[ExecutionAuthorityRoot] = []
        for raw_root in raw_roots.values:
            item = _members(
                raw_root,
                {"side", "role", "object_kind", "semantic_id"},
                "execution root",
            )
            roots.append(
                ExecutionAuthorityRoot(
                    _string(item["side"], "side"),
                    _string(item["role"], "role"),
                    AuthorityReference(
                        _string(item["object_kind"], "object_kind"),
                        _string(item["semantic_id"], "semantic_id"),
                    ),
                )
            )
        return ExecutionClosure(operation, roots)  # type: ignore[arg-type]

    def semantic_id(self, value: ExecutionClosure, context: CodecContext) -> str:
        roots = tuple(root.reference for root in value.roots)
        derived = context.transitive_dependencies(roots)
        material = IdentityObject(
            (
                ("operation", value.operation),
                ("roots", IdentityArray(_root_value(root) for root in value.roots)),
                (
                    "transitive_dependencies",
                    IdentityArray(_reference_value(item) for item in derived),
                ),
            )
        )
        return hash_identity(
            "coding-standards:execution-closure:v2", "execution-closure", material
        )

    def direct_dependencies(
        self, value: ExecutionClosure
    ) -> tuple[AuthorityReference, ...]:
        return tuple(sorted({root.reference for root in value.roots}))


def _root_value(root: ExecutionAuthorityRoot) -> IdentityObject:
    return IdentityObject(
        (
            ("side", root.side),
            ("role", root.role),
            ("object_kind", root.reference.object_kind),
            ("semantic_id", root.reference.semantic_id),
        )
    )


def _reference_value(reference: AuthorityReference) -> IdentityObject:
    return IdentityObject(
        (
            ("object_kind", reference.object_kind),
            ("semantic_id", reference.semantic_id),
        )
    )


def _members(
    value: IdentityValue, expected: set[str], description: str
) -> dict[str, IdentityValue]:
    if type(value) is not IdentityObject:
        raise invalid("AUTHORITY.INVALID_PAYLOAD", f"{description} must be an object")
    members = dict(value.members)
    if set(members) != expected:
        raise invalid(
            "AUTHORITY.INVALID_PAYLOAD_FIELDS",
            f"{description} fields differ from the payload contract",
        )
    return members


def _string(value: IdentityValue, field: str) -> str:
    if type(value) is not str or not value:
        raise invalid("AUTHORITY.INVALID_PAYLOAD", f"{field} must be nonempty string")
    return value


__all__ = (
    "AuthorityBoundValue",
    "ExecutionAuthorityRoot",
    "ExecutionClosure",
    "ExecutionClosureCodec",
    "Operation",
)
