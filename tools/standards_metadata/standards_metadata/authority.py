from __future__ import annotations

from dataclasses import dataclass

from tools.standards_authority.standards_authority import (
    AuthorityReference,
    CodecContext,
    CodecSet,
    invalid,
)
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    IdentityValue,
    hash_identity,
)

from .model import CanonicalModuleCorpus, CanonicalStandardsCorpus, ModuleMetadata
from .policy_units import PolicyUnit, PolicyUnitCorpus, PolicyUnitTombstone


@dataclass(frozen=True, slots=True)
class CanonicalCorpusAuthority:
    content: AuthorityReference
    corpus: CanonicalStandardsCorpus

    def __post_init__(self) -> None:
        if self.content.object_kind != "content-snapshot":
            raise invalid(
                "METADATA.INVALID_CONTENT_AUTHORITY",
                "canonical metadata must reference a content snapshot",
            )


class CanonicalStandardsCorpusCodec:
    object_kind = "canonical-standards-corpus"
    payload_contract = "canonical-standards-corpus.v1"
    allowed_dependency_kinds = frozenset({"content-snapshot"})

    def encode(self, value: CanonicalCorpusAuthority) -> IdentityValue:
        return _authority_value(value)

    def decode(
        self, payload: IdentityValue, context: CodecContext
    ) -> CanonicalCorpusAuthority:
        members = _members(payload, {"content", "modules", "policy_units"}, "corpus")
        content = _decode_reference(members["content"])
        context.resolve(content)
        module_members = _members(
            members["modules"], {"registry", "members", "values"}, "module corpus"
        )
        modules = tuple(
            _decode_module(item) for item in _array(module_members["values"], "modules")
        )
        module_corpus = CanonicalModuleCorpus(
            _string(module_members["registry"], "module registry"),
            tuple(_strings(module_members["members"], "module members")),
            modules,
        )
        policy_members = _members(
            members["policy_units"],
            {"registry", "sources", "active", "retired"},
            "policy-unit corpus",
        )
        policy_corpus = PolicyUnitCorpus(
            _string(policy_members["registry"], "policy-unit registry"),
            tuple(_strings(policy_members["sources"], "policy-unit sources")),
            tuple(
                _decode_policy_unit(item)
                for item in _array(policy_members["active"], "active policy units")
            ),
            tuple(
                _decode_tombstone(item)
                for item in _array(policy_members["retired"], "retired policy units")
            ),
        )
        return CanonicalCorpusAuthority(
            content, CanonicalStandardsCorpus(module_corpus, policy_corpus)
        )

    def semantic_id(
        self, value: CanonicalCorpusAuthority, context: CodecContext
    ) -> str:
        context.resolve(value.content)
        return hash_identity(
            "coding-standards:canonical-standards-corpus:v1",
            "canonical-standards-corpus",
            _authority_value(value),
        )

    def direct_dependencies(
        self, value: CanonicalCorpusAuthority
    ) -> tuple[AuthorityReference, ...]:
        return (value.content,)


def _authority_value(value: CanonicalCorpusAuthority) -> IdentityObject:
    modules = value.corpus.module_corpus
    policy = value.corpus.policy_unit_corpus
    return IdentityObject(
        (
            ("content", _reference_value(value.content)),
            (
                "modules",
                IdentityObject(
                    (
                        ("registry", modules.path),
                        ("members", IdentityArray(modules.members)),
                        ("values", IdentityArray(_module_value(item) for item in modules.modules)),
                    )
                ),
            ),
            (
                "policy_units",
                IdentityObject(
                    (
                        ("registry", policy.registry),
                        ("sources", IdentityArray(policy.sources)),
                        ("active", IdentityArray(_policy_unit_value(item) for item in policy.units)),
                        ("retired", IdentityArray(_tombstone_value(item) for item in policy.tombstones)),
                    )
                ),
            ),
        )
    )


def _module_value(value: ModuleMetadata) -> IdentityObject:
    return IdentityObject(
        (
            ("path", value.path),
            ("module_id", value.module_id),
            ("role", value.role),
            ("level", value.level),
            ("applies_when", value.applies_when),
            ("excludes", value.excludes),
            ("requires", IdentityArray(value.requires)),
            ("specializes", IdentityArray(value.specializes)),
            ("verification", value.verification),
            ("owner", value.owner),
        )
    )


def _decode_module(value: IdentityValue) -> ModuleMetadata:
    members = _members(
        value,
        {
            "path",
            "module_id",
            "role",
            "level",
            "applies_when",
            "excludes",
            "requires",
            "specializes",
            "verification",
            "owner",
        },
        "module metadata",
    )
    return ModuleMetadata(
        _string(members["path"], "path"),
        _string(members["module_id"], "module_id"),
        _string(members["role"], "role"),
        _string(members["level"], "level"),
        _string(members["applies_when"], "applies_when"),
        _string(members["excludes"], "excludes"),
        tuple(_strings(members["requires"], "requires")),
        tuple(_strings(members["specializes"], "specializes")),
        _string(members["verification"], "verification"),
        _string(members["owner"], "owner"),
    )


def _policy_unit_value(value: PolicyUnit) -> IdentityObject:
    return IdentityObject(
        (
            ("id", value.id),
            ("module", value.module),
            ("heading_path", IdentityArray(value.heading_path)),
            ("semantic_revision", value.semantic_revision),
            ("aliases", IdentityArray(value.aliases)),
            ("predecessors", IdentityArray(value.predecessors)),
            ("successors", IdentityArray(value.successors)),
            ("document", value.document),
            ("content", value.content),
            ("representation_digest", value.representation_digest),
            ("structural_digest", value.structural_digest),
            ("source", value.source),
        )
    )


def _decode_policy_unit(value: IdentityValue) -> PolicyUnit:
    members = _members(
        value,
        {
            "id",
            "module",
            "heading_path",
            "semantic_revision",
            "aliases",
            "predecessors",
            "successors",
            "document",
            "content",
            "representation_digest",
            "structural_digest",
            "source",
        },
        "policy unit",
    )
    return PolicyUnit(
        _string(members["id"], "id"),
        _string(members["module"], "module"),
        tuple(_strings(members["heading_path"], "heading_path")),
        _positive_integer(members["semantic_revision"], "semantic_revision"),
        tuple(_strings(members["aliases"], "aliases")),
        tuple(_strings(members["predecessors"], "predecessors")),
        tuple(_strings(members["successors"], "successors")),
        _string(members["document"], "document"),
        _string(members["content"], "content", allow_empty=True),
        _string(members["representation_digest"], "representation_digest"),
        _string(members["structural_digest"], "structural_digest"),
        _string(members["source"], "source"),
    )


def _tombstone_value(value: PolicyUnitTombstone) -> IdentityObject:
    return IdentityObject(
        (
            ("id", value.id),
            ("retired_semantic_revision", value.retired_semantic_revision),
            ("successors", IdentityArray(value.successors)),
            ("evidence", value.evidence),
            ("source", value.source),
        )
    )


def _decode_tombstone(value: IdentityValue) -> PolicyUnitTombstone:
    members = _members(
        value,
        {"id", "retired_semantic_revision", "successors", "evidence", "source"},
        "policy-unit tombstone",
    )
    return PolicyUnitTombstone(
        _string(members["id"], "id"),
        _positive_integer(
            members["retired_semantic_revision"], "retired_semantic_revision"
        ),
        tuple(_strings(members["successors"], "successors")),
        _string(members["evidence"], "evidence"),
        _string(members["source"], "source"),
    )


def _reference_value(value: AuthorityReference) -> IdentityObject:
    return IdentityObject(
        (("object_kind", value.object_kind), ("semantic_id", value.semantic_id))
    )


def _decode_reference(value: IdentityValue) -> AuthorityReference:
    members = _members(value, {"object_kind", "semantic_id"}, "reference")
    return AuthorityReference(
        _string(members["object_kind"], "object_kind"),
        _string(members["semantic_id"], "semantic_id"),
    )


def _members(
    value: IdentityValue, expected: set[str], description: str
) -> dict[str, IdentityValue]:
    if type(value) is not IdentityObject:
        raise invalid("METADATA.INVALID_PAYLOAD", f"{description} must be an object")
    members = dict(value.members)
    if set(members) != expected:
        raise invalid(
            "METADATA.INVALID_PAYLOAD_FIELDS",
            f"{description} fields differ from the payload contract",
        )
    return members


def _array(value: IdentityValue, description: str) -> tuple[IdentityValue, ...]:
    if type(value) is not IdentityArray:
        raise invalid("METADATA.INVALID_PAYLOAD", f"{description} must be an array")
    return value.values


def _strings(value: IdentityValue, description: str) -> tuple[str, ...]:
    selected = _array(value, description)
    if any(type(item) is not str for item in selected):
        raise invalid(
            "METADATA.INVALID_PAYLOAD", f"{description} must contain strings"
        )
    return selected  # type: ignore[return-value]


def _string(value: IdentityValue, field: str, *, allow_empty: bool = False) -> str:
    if type(value) is not str or (not allow_empty and not value):
        raise invalid("METADATA.INVALID_PAYLOAD", f"{field} must be a string")
    return value


def _positive_integer(value: IdentityValue, field: str) -> int:
    if type(value) is not int or value < 1:
        raise invalid(
            "METADATA.INVALID_PAYLOAD", f"{field} must be a positive exact integer"
        )
    return value


CANONICAL_STANDARDS_CORPUS_CODEC = CanonicalStandardsCorpusCodec()
METADATA_CODECS = CodecSet(
    "standards-metadata", (CANONICAL_STANDARDS_CORPUS_CODEC,)
)

__all__ = (
    "CANONICAL_STANDARDS_CORPUS_CODEC",
    "METADATA_CODECS",
    "CanonicalCorpusAuthority",
    "CanonicalStandardsCorpusCodec",
)
