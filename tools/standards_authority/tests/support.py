from __future__ import annotations

from dataclasses import dataclass

from tools.standards_authority.standards_authority import (
    AuthorityReference,
    CodecContext,
)
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    IdentityValue,
    hash_identity,
)


@dataclass(frozen=True, slots=True)
class FixtureValue:
    name: str
    dependencies: tuple[AuthorityReference, ...] = ()


class FixtureCodec:
    payload_contract = "fixture.v1"

    def __init__(self, object_kind: str, allowed: frozenset[str]) -> None:
        self.object_kind = object_kind
        self.allowed_dependency_kinds = allowed

    def encode(self, value: FixtureValue) -> IdentityValue:
        return IdentityObject(
            (
                ("name", value.name),
                (
                    "dependencies",
                    IdentityArray(
                        IdentityObject(
                            (
                                ("object_kind", item.object_kind),
                                ("semantic_id", item.semantic_id),
                            )
                        )
                        for item in value.dependencies
                    ),
                ),
            )
        )

    def decode(self, payload: IdentityValue, context: CodecContext) -> FixtureValue:
        del context
        assert type(payload) is IdentityObject
        members = dict(payload.members)
        assert set(members) == {"name", "dependencies"}
        name = members["name"]
        dependencies = members["dependencies"]
        assert type(name) is str
        assert type(dependencies) is IdentityArray
        refs: list[AuthorityReference] = []
        for raw in dependencies.values:
            assert type(raw) is IdentityObject
            fields = dict(raw.members)
            refs.append(
                AuthorityReference(fields["object_kind"], fields["semantic_id"])  # type: ignore[arg-type]
            )
        return FixtureValue(name, tuple(refs))

    def semantic_id(self, value: FixtureValue, context: CodecContext) -> str:
        del context
        return hash_identity(
            f"coding-standards:{self.object_kind}:v1",
            self.object_kind,
            self.encode(value),
        )

    def direct_dependencies(
        self, value: FixtureValue
    ) -> tuple[AuthorityReference, ...]:
        return value.dependencies
