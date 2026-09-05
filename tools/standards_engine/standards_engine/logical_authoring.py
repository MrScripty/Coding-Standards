from __future__ import annotations

import hashlib
import json
import re
import tempfile
import tomllib
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Protocol

from tools.standards_applicability.standards_applicability import compile_fact_schema

from tools.repository_git.repository_git import (
    GitRepositoryError,
    RepositoryPath,
    git_output,
)
from tools.standards_metadata.standards_metadata import (
    CANONICAL_MODULE_CORPUS,
    POLICY_UNIT_REGISTRY,
    FrozenContentSource,
    PolicyUnit,
    PolicyUnitTombstone,
    load_canonical_standards_corpus,
    load_canonical_module_corpus,
)
from tools.standards_policy_impact.standards_policy_impact import (
    DEFAULT_REGISTRY as POLICY_IMPACT_REGISTRY,
    thaw,
)
from tools.standards_verifier.standards_verifier import (
    EngineError,
    suite_input_projection_bytes,
)

from .authoring import AuthoringError, AuthoringFailure


_CANONICAL_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
_SEMANTIC_ID = re.compile(r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)*$")
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_SUITE_INPUTS = "evaluation/standards-effectiveness/generated/suite-inputs.json"
_POLICY_UNIT_ROOT = "evaluation/standards-effectiveness/policy-units"
_POLICY_IMPACT_ROOT = "evaluation/standards-effectiveness/policy-impact"
_RELATIONSHIP_KINDS = frozenset(
    {
        "normative-consumer",
        "router-projection",
        "prompt-projection",
        "template-projection",
        "reference-projection",
        "fixture-projection",
        "enforcement-suite-projection",
        "documentation-projection",
        "implementation-projection",
    }
)


def _error(code: str, outcome: str, message: str) -> AuthoringError:
    return AuthoringError(AuthoringFailure(code, outcome, message))  # type: ignore[arg-type]


def _invalid(code: str, message: str) -> AuthoringError:
    return _error(code, "invalid", message)


def _unsupported(code: str, message: str) -> AuthoringError:
    return _error(code, "unsupported", message)


def _mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, Mapping) or any(type(key) is not str for key in value):
        raise _invalid("AUTHORING.INVALID_ARGUMENTS", f"{label} must be an object")
    return dict(value)


def _exact(value: Mapping[str, object], fields: set[str], label: str) -> None:
    if set(value) != fields:
        raise _invalid(
            "AUTHORING.INVALID_ARGUMENTS",
            f"{label} has missing or unknown members",
        )


def _text(value: object, label: str) -> str:
    if (
        type(value) is not str
        or not value.strip()
        or any(0xD800 <= ord(character) <= 0xDFFF for character in value)
    ):
        raise _invalid(
            "AUTHORING.INVALID_ARGUMENTS", f"{label} must be non-empty Unicode text"
        )
    return value


def _semantic_id(value: object, label: str) -> str:
    selected = _text(value, label)
    if _SEMANTIC_ID.fullmatch(selected) is None:
        raise _invalid(
            "AUTHORING.INVALID_CANONICAL_ID",
            f"{label} must use the canonical standards ID grammar",
        )
    return selected


def _canonical_id(value: object, label: str) -> str:
    selected = _text(value, label)
    if _CANONICAL_ID.fullmatch(selected) is None:
        raise _invalid(
            "AUTHORING.INVALID_CANONICAL_ID",
            f"{label} must use the canonical ID grammar",
        )
    return selected


def _ids(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise _invalid("AUTHORING.INVALID_ARGUMENTS", f"{label} must be an array")
    selected = tuple(sorted(_semantic_id(item, label) for item in value))
    if len(set(selected)) != len(selected):
        raise _invalid("AUTHORING.DUPLICATE_EDIT", f"{label} contains duplicates")
    return selected


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest_value(domain: str, value: object) -> str:
    framed = f"{domain}\0{_canonical_json(value)}".encode("utf-8")
    return f"sha256:{hashlib.sha256(framed).hexdigest()}"


@dataclass(frozen=True, slots=True, order=True)
class EvidenceReference:
    id: str
    digest: str
    provider_contract: str
    provider_contract_version: str

    @classmethod
    def from_mapping(cls, value: object) -> EvidenceReference:
        raw = _mapping(value, "evidence reference")
        _exact(
            raw,
            {"id", "digest", "provider_contract", "provider_contract_version"},
            "evidence reference",
        )
        identity = _text(raw["id"], "evidence ID")
        provider = _text(raw["provider_contract"], "evidence provider contract")
        digest = _text(raw["digest"], "evidence digest")
        if (
            _CANONICAL_ID.fullmatch(identity) is None
            or _CANONICAL_ID.fullmatch(provider) is None
        ):
            raise _invalid(
                "AUTHORING.INVALID_ARGUMENTS",
                "evidence identity and provider must use the canonical ID grammar",
            )
        if _DIGEST.fullmatch(digest) is None:
            raise _invalid(
                "AUTHORING.INVALID_ARGUMENTS", "evidence digest must be sha256"
            )
        return cls(
            identity,
            digest,
            provider,
            _text(raw["provider_contract_version"], "provider contract version"),
        )

    def as_contract(self) -> dict[str, object]:
        return {
            "id": self.id,
            "digest": self.digest,
            "provider_contract": self.provider_contract,
            "provider_contract_version": self.provider_contract_version,
        }


@dataclass(frozen=True, slots=True)
class ChangePurpose:
    summary: str
    rationale: str
    evidence: tuple[EvidenceReference, ...]

    @classmethod
    def from_mapping(cls, value: object) -> ChangePurpose:
        raw = _mapping(value, "change-set purpose")
        _exact(raw, {"summary", "rationale", "evidence"}, "change-set purpose")
        evidence_value = raw["evidence"]
        if not isinstance(evidence_value, list) or not evidence_value:
            raise _invalid(
                "AUTHORING.EVIDENCE_REQUIRED",
                "change-set purpose requires explicit evidence",
            )
        evidence = tuple(
            sorted(EvidenceReference.from_mapping(item) for item in evidence_value)
        )
        if len(set(evidence)) != len(evidence):
            raise _invalid(
                "AUTHORING.EVIDENCE_REQUIRED",
                "change-set evidence references must be unique",
            )
        return cls(
            _text(raw["summary"], "change-set summary"),
            _text(raw["rationale"], "change-set rationale"),
            evidence,
        )

    def as_contract(self) -> dict[str, object]:
        return {
            "summary": self.summary,
            "rationale": self.rationale,
            "evidence": [item.as_contract() for item in self.evidence],
        }


class LogicalEdit(Protocol):
    @property
    def facet(self) -> tuple[str, ...]: ...

    def as_contract(self) -> dict[str, object]: ...


@dataclass(frozen=True, slots=True)
class RevisePolicyUnit:
    policy: str
    title: str
    body: str
    semantics: Mapping[str, object]

    @property
    def facet(self) -> tuple[str, ...]:
        return ("policy", self.policy)

    @classmethod
    def from_mapping(cls, raw: Mapping[str, object]) -> RevisePolicyUnit:
        _exact(
            raw,
            {"kind", "policy", "title", "body", "semantics"},
            "revise-policy-unit edit",
        )
        semantics = _semantic_intent(raw["semantics"])
        return cls(
            _semantic_id(raw["policy"], "policy ID"),
            _text(raw["title"], "policy title"),
            _text(raw["body"], "authored policy body"),
            MappingProxyType(dict(semantics)),
        )

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "revise-policy-unit",
            "policy": self.policy,
            "title": self.title,
            "body": self.body,
            "semantics": dict(self.semantics),
        }


def _semantic_intent(value: object) -> Mapping[str, object]:
    raw = _mapping(value, "policy semantic intent")
    kind = raw.get("kind")
    if kind == "preserve":
        _exact(raw, {"kind", "semantic_revision", "intent"}, "preserved semantics")
        revision = raw["semantic_revision"]
        if type(revision) is not int or revision < 1:
            raise _invalid(
                "AUTHORING.INVALID_SEMANTIC_REVISION",
                "semantic revision must be positive",
            )
    elif kind == "change":
        _exact(
            raw,
            {
                "kind",
                "accepted_semantic_revision",
                "proposed_semantic_revision",
                "intent",
            },
            "changed semantics",
        )
        accepted = raw["accepted_semantic_revision"]
        proposed = raw["proposed_semantic_revision"]
        if (
            type(accepted) is not int
            or accepted < 1
            or type(proposed) is not int
            or proposed != accepted + 1
        ):
            raise _invalid(
                "AUTHORING.INVALID_SEMANTIC_REVISION",
                "changed semantics must advance the accepted revision by one",
            )
    else:
        raise _invalid(
            "AUTHORING.INVALID_SEMANTIC_REVISION", "semantic intent kind is invalid"
        )
    _text(raw["intent"], "semantic intent")
    return dict(sorted(raw.items()))


@dataclass(frozen=True, slots=True)
class StructuredEdit:
    kind: str
    target: str
    facet_name: str
    payload: str

    @property
    def facet(self) -> tuple[str, ...]:
        return (self.facet_name, self.target)

    def as_contract(self) -> dict[str, object]:
        value = json.loads(self.payload)
        if type(value) is not dict:  # pragma: no cover - constructed internally
            raise RuntimeError("structured edit payload is not an object")
        return value


def _structured(
    raw: Mapping[str, object], *, target: str, facet: str
) -> StructuredEdit:
    return StructuredEdit(str(raw["kind"]), target, facet, _canonical_json(raw))


@dataclass(frozen=True, slots=True)
class ReplaceStandardRelationships:
    standard: str
    requires: tuple[str, ...]
    specializes: tuple[str, ...]
    rationale: str

    @property
    def facet(self) -> tuple[str, ...]:
        return ("module-relationships", self.standard)

    @classmethod
    def from_mapping(cls, raw: Mapping[str, object]) -> ReplaceStandardRelationships:
        _exact(
            raw,
            {"kind", "standard", "requires", "specializes", "rationale"},
            "replace-standard-relationships edit",
        )
        return cls(
            _semantic_id(raw["standard"], "standard ID"),
            _ids(raw["requires"], "Requires"),
            _ids(raw["specializes"], "Specializes"),
            _text(raw["rationale"], "relationship rationale"),
        )

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "replace-standard-relationships",
            "standard": self.standard,
            "requires": list(self.requires),
            "specializes": list(self.specializes),
            "rationale": self.rationale,
        }


def _edit(value: object) -> LogicalEdit:
    raw = _mapping(value, "logical edit")
    kind = raw.get("kind")
    if kind == "revise-policy-unit":
        return RevisePolicyUnit.from_mapping(raw)
    if kind == "replace-standard-relationships":
        return ReplaceStandardRelationships.from_mapping(raw)
    if kind == "create-standard":
        _exact(
            raw,
            {"kind", "standard", "requires", "specializes", "policy_units"},
            "create-standard edit",
        )
        standard = _standard_content(raw["standard"])
        requires = _ids(raw["requires"], "Requires")
        specializes = _ids(raw["specializes"], "Specializes")
        units = raw["policy_units"]
        if not isinstance(units, list):
            raise _invalid(
                "AUTHORING.INVALID_ARGUMENTS", "policy_units must be an array"
            )
        normalized_units = [_new_policy_unit(item) for item in units]
        unit_ids = [item["id"] for item in normalized_units]
        if len(set(unit_ids)) != len(unit_ids):
            raise _invalid(
                "AUTHORING.DUPLICATE_EDIT", "new policy-unit IDs must be unique"
            )
        normalized = {
            "kind": kind,
            "standard": standard,
            "requires": list(requires),
            "specializes": list(specializes),
            "policy_units": sorted(normalized_units, key=lambda item: str(item["id"])),
        }
        return _structured(normalized, target=str(standard["id"]), facet="standard")
    if kind in {
        "put-routing-rule",
        "remove-routing-rule",
        "put-routing-fact",
        "remove-routing-fact",
    }:
        field = "rule" if kind.endswith("rule") else "fact"
        _exact(raw, {"kind", field, "rationale"}, f"{kind} edit")
        _text(raw["rationale"], "routing change rationale")
        value = raw[field]
        if kind.startswith("put-"):
            value = _mapping(value, f"routing {field}")
            fields = (
                {"id", "target", "when", "condition"}
                if field == "rule"
                else {
                    "id",
                    "semantic_revision",
                    "type",
                    "nullable",
                    "values",
                    "aliases",
                    "meaning",
                    "prompt",
                }
            )
            _exact(value, fields, f"routing {field}")
            identifier = _semantic_id(value["id"], f"routing {field} ID")
            if field == "fact":
                if (
                    type(value["semantic_revision"]) is not int
                    or value["semantic_revision"] < 1
                ):
                    raise _invalid(
                        "AUTHORING.INVALID_SEMANTIC_REVISION",
                        "routing fact revision must be positive",
                    )
                _text(value["meaning"], "routing fact meaning")
                _text(value["prompt"], "routing fact prompt")
            if field == "rule":
                _semantic_id(value["target"], "route target")
                _mapping(value["when"], "route applicability")
                condition = _text(value["condition"], "route condition")
                if any(character in condition for character in "\r\n"):
                    raise _invalid(
                        "AUTHORING.INVALID_ARGUMENTS",
                        "route condition must be one paragraph",
                    )
        else:
            identifier = _semantic_id(value, f"routing {field} ID")
        return _structured(raw, target=identifier, facet=f"routing-{field}")
    if kind == "audit-policy-unit":
        _exact(raw, {"kind", "policy", "rationale"}, "coverage audit edit")
        policy = _semantic_id(raw["policy"], "policy ID")
        _text(raw["rationale"], "coverage audit rationale")
        return _structured(raw, target=policy, facet="coverage-audit")
    if kind == "revise-standard":
        _exact(raw, {"kind", "standard"}, "revise-standard edit")
        standard = _standard_content(raw["standard"])
        return _structured(raw, target=str(standard["id"]), facet="standard")
    if kind == "rewrite-navigation-index":
        fields = {"kind", "entrypoint", "destinations", "rationale"}
        if "retargets" in raw:
            fields.add("retargets")
            if not isinstance(raw["retargets"], list):
                raise _invalid(
                    "AUTHORING.INVALID_ARGUMENTS",
                    "Retarget dispositions must be a list.",
                )
            for retarget in raw["retargets"]:
                record = _mapping(retarget, "navigation retarget")
                _exact(record, {"entrypoint", "standard"}, "navigation retarget")
                if not isinstance(
                    _relationship_consumer(record["entrypoint"]), Mapping
                ):
                    raise _invalid(
                        "AUTHORING.INVALID_TARGET_HANDLE",
                        "Retargets require entrypoint handles.",
                    )
                _semantic_id(record["standard"], "navigation destination")
        _exact(raw, fields, "navigation index edit")
        target = _relationship_consumer(raw["entrypoint"])
        if not isinstance(target, Mapping):
            raise _invalid(
                "AUTHORING.INVALID_TARGET_HANDLE",
                "Navigation requires an opaque entrypoint handle.",
            )
        destinations = raw["destinations"]
        if not isinstance(destinations, list) or not destinations:
            raise _invalid(
                "AUTHORING.INVALID_ARGUMENTS",
                "Navigation requires at least one canonical destination.",
            )
        for destination in destinations:
            _semantic_id(destination, "navigation destination")
        if len(set(destinations)) != len(destinations):
            raise _invalid(
                "AUTHORING.INVALID_ARGUMENTS", "Navigation destinations must be unique."
            )
        _text(raw["rationale"], "navigation rationale")
        return _structured(raw, target=str(target["id"]), facet="navigation-index")
    if kind == "move-policy-unit":
        fields = {"kind", "policy", "standard", "semantics"}
        if "after_policy" in raw:
            fields.add("after_policy")
            _semantic_id(raw["after_policy"], "policy placement anchor")
        _exact(raw, fields, "move-policy-unit edit")
        policy = _semantic_id(raw["policy"], "policy ID")
        _semantic_id(raw["standard"], "destination standard ID")
        normalized = dict(raw)
        normalized["semantics"] = _semantic_intent(raw["semantics"])
        return _structured(normalized, target=policy, facet="policy")
    if kind == "retire-policy-unit":
        _exact(
            raw,
            {
                "kind",
                "policy",
                "retired_semantic_revision",
                "successors",
                "relationship_dispositions",
                "evidence",
            },
            "retire-policy-unit edit",
        )
        policy = _semantic_id(raw["policy"], "policy ID")
        revision = raw["retired_semantic_revision"]
        if type(revision) is not int or revision < 1:
            raise _invalid(
                "AUTHORING.INVALID_SEMANTIC_REVISION",
                "retired revision must be positive",
            )
        successors = _ids(raw["successors"], "policy successors")
        if policy in successors:
            raise _invalid(
                "AUTHORING.INVALID_SUCCESSOR", "a retired policy cannot succeed itself"
            )
        normalized = dict(raw)
        normalized["successors"] = list(successors)
        normalized["evidence"] = [
            item.as_contract()
            for item in _evidence_list(raw["evidence"], "retirement evidence")
        ]
        normalized["relationship_dispositions"] = _normalized_dispositions(
            raw["relationship_dispositions"]
        )
        return _structured(normalized, target=policy, facet="policy")
    if kind == "retire-standard":
        _exact(
            raw,
            {"kind", "standard", "successors", "relationship_dispositions", "evidence"},
            "retire-standard edit",
        )
        standard = _semantic_id(raw["standard"], "standard ID")
        successors = _ids(raw["successors"], "standard successors")
        if standard in successors:
            raise _invalid(
                "AUTHORING.INVALID_SUCCESSOR",
                "a retired standard cannot succeed itself",
            )
        normalized = dict(raw)
        normalized["successors"] = list(successors)
        normalized["evidence"] = [
            item.as_contract()
            for item in _evidence_list(raw["evidence"], "retirement evidence")
        ]
        normalized["relationship_dispositions"] = _normalized_dispositions(
            raw["relationship_dispositions"]
        )
        return _structured(normalized, target=standard, facet="standard")
    if kind in {"put-policy-relationship", "remove-policy-relationship"}:
        _exact(raw, {"kind", "relationship"}, f"{kind} edit")
        relationship = _policy_relationship(raw["relationship"])
        key = _canonical_json(
            {
                "source": relationship["source_policy"],
                "consumer": relationship["consumer"],
                "relation": relationship["relation"],
            }
        )
        return _structured(
            {"kind": kind, "relationship": relationship},
            target=key,
            facet="policy-relationship",
        )
    if type(kind) is not str:
        raise _invalid("AUTHORING.INVALID_ARGUMENTS", "logical edit requires a kind")
    raise _unsupported(
        "AUTHORING.UNSUPPORTED_EDIT", f"logical edit kind {kind!r} is unsupported"
    )


def _standard_content(value: object) -> dict[str, object]:
    raw = _mapping(value, "standard content")
    fields = {
        "id",
        "title",
        "role",
        "level",
        "applies_when",
        "does_not_apply_when",
        "verification",
        "body",
    }
    _exact(raw, fields, "standard content")
    _semantic_id(raw["id"], "standard ID")
    for field in fields - {"id", "role", "level"}:
        _text(raw[field], field)
    if raw["role"] not in {
        "core",
        "router",
        "workflow",
        "profile",
        "topic",
        "reference",
    }:
        raise _invalid("AUTHORING.INVALID_ARGUMENTS", "standard role is invalid")
    if raw["level"] not in {"MUST", "SHOULD", "PROFILE", "REFERENCE"}:
        raise _invalid("AUTHORING.INVALID_ARGUMENTS", "standard level is invalid")
    return raw


def _new_policy_unit(value: object) -> dict[str, object]:
    raw = _mapping(value, "new policy unit")
    _exact(
        raw,
        {
            "id",
            "heading_chain",
            "semantic_revision",
            "intent",
            "aliases",
            "predecessors",
            "successors",
        },
        "new policy unit",
    )
    _semantic_id(raw["id"], "policy ID")
    headings = raw["heading_chain"]
    if not isinstance(headings, list) or not headings:
        raise _invalid("AUTHORING.INVALID_ARGUMENTS", "heading_chain must be non-empty")
    tuple(_text(item, "policy heading") for item in headings)
    if type(raw["semantic_revision"]) is not int or raw["semantic_revision"] != 1:
        raise _invalid(
            "AUTHORING.INVALID_SEMANTIC_REVISION",
            "new policy units start at revision one",
        )
    _text(raw["intent"], "semantic intent")
    normalized = dict(raw)
    for field in ("aliases", "predecessors", "successors"):
        normalized[field] = list(_ids(raw[field], field))
    return normalized


def _evidence_list(value: object, label: str) -> tuple[EvidenceReference, ...]:
    if not isinstance(value, list) or not value:
        raise _invalid("AUTHORING.EVIDENCE_REQUIRED", f"{label} must be non-empty")
    selected = tuple(sorted(EvidenceReference.from_mapping(item) for item in value))
    if len(set(selected)) != len(selected):
        raise _invalid("AUTHORING.EVIDENCE_REQUIRED", f"{label} must be unique")
    return selected


def _dispositions(value: object) -> tuple[Mapping[str, object], ...]:
    if not isinstance(value, list):
        raise _invalid(
            "AUTHORING.INVALID_ARGUMENTS", "relationship dispositions must be an array"
        )
    selected = tuple(_mapping(item, "relationship disposition") for item in value)
    for item in selected:
        required = {"relationship", "disposition", "rationale", "evidence"}
        optional = {"replacement_consumer"}
        if not required <= set(item) or set(item) - required - optional:
            raise _invalid(
                "AUTHORING.INVALID_ARGUMENTS",
                "relationship disposition has invalid members",
            )
        if item["disposition"] not in {"remove", "retarget"}:
            raise _invalid(
                "AUTHORING.INVALID_ARGUMENTS", "relationship disposition is invalid"
            )
        _text(item["rationale"], "relationship disposition rationale")
        _evidence_list(item["evidence"], "relationship disposition evidence")
        relationship = _mapping(item["relationship"], "relationship key")
        relationship_kind = relationship.get("kind")
        if relationship_kind == "module-relationship":
            _exact(
                relationship,
                {"kind", "relation", "source", "target"},
                "module relationship key",
            )
            if relationship["relation"] not in {"requires", "specializes"}:
                raise _invalid(
                    "AUTHORING.INVALID_ARGUMENTS",
                    "module relationship kind is invalid",
                )
            _semantic_id(relationship["source"], "relationship source")
            _semantic_id(relationship["target"], "relationship target")
        elif relationship_kind == "policy-relationship":
            _exact(
                relationship,
                {"kind", "source_policy", "consumer", "relation"},
                "policy relationship key",
            )
            _semantic_id(relationship["source_policy"], "relationship source policy")
            _relationship_consumer(relationship["consumer"])
            if relationship["relation"] not in _RELATIONSHIP_KINDS:
                raise _invalid(
                    "AUTHORING.INVALID_ARGUMENTS",
                    "policy relationship kind is invalid",
                )
        else:
            raise _invalid(
                "AUTHORING.INVALID_ARGUMENTS", "relationship key kind is invalid"
            )
        replacement = item.get("replacement_consumer")
        if item["disposition"] == "retarget":
            if replacement is None:
                raise _invalid(
                    "AUTHORING.MISSING_SEMANTIC_DECISION",
                    "retarget disposition requires a replacement consumer",
                )
            _relationship_consumer(replacement)
        elif replacement is not None:
            raise _invalid(
                "AUTHORING.INVALID_ARGUMENTS",
                "remove disposition cannot name a replacement consumer",
            )
    return selected


def _normalized_dispositions(value: object) -> list[dict[str, object]]:
    selected = []
    for disposition in _dispositions(value):
        normalized = dict(disposition)
        normalized["relationship"] = dict(
            _mapping(disposition["relationship"], "relationship key")
        )
        normalized["evidence"] = [
            item.as_contract()
            for item in _evidence_list(
                disposition["evidence"], "relationship disposition evidence"
            )
        ]
        selected.append(normalized)
    normalized = sorted(selected, key=_canonical_json)
    if len({_disposition_key(item) for item in normalized}) != len(normalized):
        raise _invalid(
            "AUTHORING.DUPLICATE_EDIT",
            "relationship dispositions must identify unique relationships",
        )
    return normalized


def _policy_relationship(value: object) -> dict[str, object]:
    raw = _mapping(value, "policy relationship")
    _exact(
        raw,
        {
            "source_policy",
            "consumer",
            "relation",
            "applicability",
            "source_scope",
            "consumer_scope",
            "evidence_owner",
            "rationale",
        },
        "policy relationship",
    )
    _semantic_id(raw["source_policy"], "relationship source policy")
    _relationship_consumer(raw["consumer"])
    if raw["relation"] not in _RELATIONSHIP_KINDS:
        raise _invalid("AUTHORING.INVALID_ARGUMENTS", "relationship kind is invalid")
    if not isinstance(raw["applicability"], Mapping):
        raise _invalid(
            "AUTHORING.INVALID_ARGUMENTS",
            "relationship applicability must be an object",
        )
    if _contains_null(raw["applicability"]):
        raise _unsupported(
            "AUTHORING.UNSUPPORTED_APPLICABILITY",
            "relationship applicability contains a scalar the canonical TOML authority cannot represent",
        )
    for field in ("source_scope", "consumer_scope"):
        if raw[field] is not None and not isinstance(raw[field], Mapping):
            raise _invalid(
                "AUTHORING.INVALID_ARGUMENTS", f"{field} must be an object or null"
            )
    _canonical_id(raw["evidence_owner"], "relationship evidence owner")
    _text(raw["rationale"], "relationship rationale")
    return raw


def _contains_null(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, Mapping):
        return any(_contains_null(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_null(item) for item in value)
    return False


def _relationship_consumer(value: object) -> object:
    if type(value) is str:
        return _semantic_id(value, "relationship consumer")
    raw = _mapping(value, "relationship consumer handle")
    _exact(
        raw,
        {"kind", "snapshot", "id", "schema_version"},
        "relationship consumer handle",
    )
    if raw["kind"] != "authoring-target-handle" or raw["schema_version"] != 5:
        raise _invalid(
            "AUTHORING.INVALID_TARGET_HANDLE", "authoring target handle is invalid"
        )
    snapshot = _mapping(raw["snapshot"], "authoring target snapshot")
    _exact(snapshot, {"kind", "id", "schema_version"}, "authoring target snapshot")
    if snapshot["kind"] != "snapshot-handle" or snapshot["schema_version"] != 5:
        raise _invalid(
            "AUTHORING.INVALID_TARGET_HANDLE", "authoring target snapshot is invalid"
        )
    _text(snapshot["id"], "authoring target snapshot ID")
    digest = _text(raw["id"], "authoring target ID")
    if _DIGEST.fullmatch(digest) is None:
        raise _invalid(
            "AUTHORING.INVALID_TARGET_HANDLE", "authoring target ID must be sha256"
        )
    return raw


@dataclass(frozen=True, slots=True)
class StandardsChangeSet:
    purpose: ChangePurpose
    edits: tuple[LogicalEdit, ...]

    @classmethod
    def from_mapping(cls, value: object) -> StandardsChangeSet:
        raw = _mapping(value, "standards change set")
        _exact(raw, {"purpose", "edits"}, "standards change set")
        edits_value = raw["edits"]
        if not isinstance(edits_value, list) or not edits_value:
            raise _invalid(
                "AUTHORING.INVALID_ARGUMENTS",
                "standards change set requires at least one logical edit",
            )
        selected = tuple(
            sorted(
                (_edit(item) for item in edits_value),
                key=lambda item: _canonical_json(item.as_contract()),
            )
        )
        facets = [item.facet for item in selected]
        if len(set(facets)) != len(facets):
            raise _invalid(
                "AUTHORING.DUPLICATE_EDIT",
                "one change set cannot write one logical facet more than once",
            )
        return cls(ChangePurpose.from_mapping(raw["purpose"]), selected)

    def as_contract(self) -> dict[str, object]:
        return {
            "purpose": self.purpose.as_contract(),
            "edits": [item.as_contract() for item in self.edits],
        }


@dataclass(frozen=True, slots=True)
class LogicalProgram:
    change_sets: tuple[StandardsChangeSet, ...] = ()

    def __init__(self, change_sets: Iterable[StandardsChangeSet] = ()) -> None:
        selected = tuple(change_sets)
        if any(type(item) is not StandardsChangeSet for item in selected):
            raise _invalid(
                "AUTHORING.INVALID_LOGICAL_PROGRAM",
                "logical program requires exact StandardsChangeSet values",
            )
        object.__setattr__(self, "change_sets", selected)


@dataclass(frozen=True, slots=True)
class LogicalProjection:
    source: FrozenContentSource
    compiled: Any
    semantic_proposals: tuple[dict[str, object], ...]
    analysis_policy_ids: tuple[str, ...]
    analysis_module_ids: tuple[str, ...]
    repository_paths: tuple[str, ...]


class LogicalAuthoringCompiler:
    """Compile a logical program into one private canonical content projection."""

    def __init__(self, compile_authorities: Callable[[FrozenContentSource], object]):
        if not callable(compile_authorities):
            raise _invalid(
                "AUTHORING.INVALID_COMPILER",
                "logical authoring requires the current authority compiler",
            )
        self._compile_authorities = compile_authorities

    def compile(
        self,
        base: FrozenContentSource,
        program: LogicalProgram,
        *,
        base_snapshot: str | None = None,
        base_repository_paths: Iterable[str],
    ) -> LogicalProjection:
        if type(base) is not FrozenContentSource or type(program) is not LogicalProgram:
            raise _invalid(
                "AUTHORING.INVALID_LOGICAL_PROGRAM",
                "logical compilation requires exact frozen content and program values",
            )
        selected_repository_paths = _repository_paths(base_repository_paths)
        base_file_paths = frozenset(dict(base.files))

        def compile_current(current: dict[str, bytes]) -> Any:
            _refresh_suite_input_projection(
                current,
                base_file_paths,
                selected_repository_paths,
            )
            return self._compile_authorities(FrozenContentSource(current))

        base_compiled = self._compile_authorities(base)
        files = dict(base.files)
        repository_paths = selected_repository_paths
        for change_set in program.change_sets:
            before = dict(files)
            routing_edits = [
                edit.as_contract()
                for edit in change_set.edits
                if edit.as_contract()["kind"] in _ROUTING_EDITS
            ]
            routing_applied = False
            for edit in sorted(change_set.edits, key=_projection_order):
                if edit.as_contract()["kind"] in _ROUTING_EDITS:
                    if not routing_applied:
                        _edit_routing(files, routing_edits)
                        routing_applied = True
                    continue
                self._apply_edit(
                    files,
                    edit,
                    base_compiled,
                    base_snapshot,
                    compile_current,
                )
            if files == before and not any(
                edit.as_contract()["kind"] == "audit-policy-unit"
                for edit in change_set.edits
            ):
                raise _invalid(
                    "AUTHORING.NO_EFFECT",
                    "logical change set does not change the current standards projection",
                )
            repository_paths = _refresh_suite_input_projection(
                files,
                base_file_paths,
                selected_repository_paths,
            )
        source = FrozenContentSource(files)
        compiled = self._compile_authorities(source)
        _validate_final_standard_successors(compiled, program)
        return LogicalProjection(
            source,
            compiled,
            _semantic_proposals(base_compiled, compiled, program),
            _analysis_policy_ids(base_compiled, compiled, program),
            _analysis_module_ids(program),
            repository_paths,
        )

    def _apply_edit(
        self,
        files: dict[str, bytes],
        edit: LogicalEdit,
        base_compiled: Any,
        base_snapshot: str | None,
        compile_current: Callable[[dict[str, bytes]], Any],
    ) -> None:
        if isinstance(edit, ReplaceStandardRelationships):
            self._replace_standard_relationships(files, edit)
            return
        if isinstance(edit, RevisePolicyUnit):
            self._revise_policy_unit(files, edit, base_compiled.corpus)
            return
        if not isinstance(edit, StructuredEdit):  # pragma: no cover - closed parser
            raise _unsupported(
                "AUTHORING.UNSUPPORTED_EDIT", "logical edit has no projection"
            )
        raw = edit.as_contract()
        kind = raw["kind"]
        if kind == "audit-policy-unit":
            current = compile_current(files)
            if raw["policy"] not in current.coverage.views:
                raise _invalid(
                    "AUTHORING.UNKNOWN_POLICY",
                    "Coverage audit requires a registered policy unit.",
                )
            if raw["policy"] in current.repository_coverage.covered_subjects:
                raise _invalid(
                    "AUTHORING.COVERAGE_CURRENT",
                    "The policy already has a current coverage certificate.",
                )
        elif kind in {
            "put-routing-rule",
            "remove-routing-rule",
            "put-routing-fact",
            "remove-routing-fact",
        }:
            _edit_routing(files, [raw])
        elif kind == "create-standard":
            self._create_standard(files, raw)
        elif kind == "revise-standard":
            self._revise_standard(files, raw)
        elif kind == "rewrite-navigation-index":
            from .navigation_indexes import rewrite_index

            rewrite_index(
                files,
                raw,
                base_compiled.navigation_indexes,
                compile_current(files).corpus,
                base_snapshot,
            )
        elif kind == "move-policy-unit":
            self._move_policy_unit(files, raw, base_compiled.corpus, compile_current)
        elif kind == "retire-policy-unit":
            self._retire_policy_unit(files, raw, base_snapshot, compile_current)
        elif kind == "retire-standard":
            self._retire_standard(files, raw, base_snapshot, compile_current)
        elif kind == "put-policy-relationship":
            self._put_policy_relationship(
                files,
                raw["relationship"],
                base_snapshot,
                compile_current,
            )
        elif kind == "remove-policy-relationship":
            self._remove_policy_relationship(
                files,
                raw["relationship"],
                base_snapshot,
                compile_current,
            )
        else:  # pragma: no cover - closed parser
            raise _unsupported(
                "AUTHORING.UNSUPPORTED_EDIT", f"edit {kind!r} has no projection"
            )

    def _create_standard(
        self,
        files: dict[str, bytes],
        edit: Mapping[str, object],
    ) -> None:
        corpus = load_canonical_standards_corpus(FrozenContentSource(files))
        standard = _mapping(edit["standard"], "standard content")
        standard_id = str(standard["id"])
        if corpus.resolve_module(standard_id) is not None:
            raise _invalid(
                "AUTHORING.STANDARD_EXISTS",
                f"standard {standard_id!r} already exists",
            )
        path = _new_standard_path(standard_id, str(standard["role"]))
        if path in files:
            raise _invalid(
                "AUTHORING.STANDARD_EXISTS",
                f"derived standard path for {standard_id!r} already exists",
            )
        units_value = edit["policy_units"]
        assert isinstance(units_value, list)
        units = [_mapping(item, "new policy unit") for item in units_value]
        for unit in units:
            if corpus.resolve_policy_unit(str(unit["id"])) is not None:
                raise _invalid(
                    "AUTHORING.POLICY_UNIT_EXISTS",
                    f"policy unit {unit['id']!r} already exists",
                )
        files[path] = _render_standard(
            standard,
            tuple(str(item) for item in edit["requires"]),  # type: ignore[arg-type]
            tuple(str(item) for item in edit["specializes"]),  # type: ignore[arg-type]
            path,
        )
        _set_registry_list(
            files, CANONICAL_MODULE_CORPUS, "members", path, present=True
        )
        if units:
            sidecar = _policy_sidecar_path(standard_id)
            if sidecar in files:
                raise _invalid(
                    "AUTHORING.PROJECTION_DISAGREEMENT",
                    f"derived policy-unit sidecar for {standard_id!r} already exists",
                )
            files[sidecar] = _render_policy_sidecar(
                [
                    {
                        "id": unit["id"],
                        "module": standard_id,
                        "heading_path": unit["heading_chain"],
                        "semantic_revision": 1,
                        "aliases": unit["aliases"],
                        "predecessors": unit["predecessors"],
                        "successors": unit["successors"],
                    }
                    for unit in units
                ],
                [],
            )
            _set_registry_list(
                files, POLICY_UNIT_REGISTRY, "sources", sidecar, present=True
            )

    @staticmethod
    def _revise_standard(
        files: dict[str, bytes],
        edit: Mapping[str, object],
    ) -> None:
        corpus = load_canonical_standards_corpus(FrozenContentSource(files))
        standard = _mapping(edit["standard"], "standard content")
        standard_id = str(standard["id"])
        module = corpus.resolve_module(standard_id)
        if module is None or module.module_id != standard_id:
            raise _error(
                "AUTHORING.STANDARD_UNAVAILABLE",
                "unavailable",
                f"standard {standard_id!r} is unavailable",
            )
        if standard["role"] != module.role:
            raise _unsupported(
                "AUTHORING.STANDARD_RELOCATION_UNSUPPORTED",
                "revise-standard cannot change canonical role or physical placement",
            )
        files[module.path] = _render_standard(
            standard,
            module.requires,
            module.specializes,
            module.path,
        )

    @staticmethod
    def _replace_standard_relationships(
        files: dict[str, bytes],
        edit: ReplaceStandardRelationships,
    ) -> None:
        source = FrozenContentSource(files)
        module = load_canonical_standards_corpus(source).resolve_module(edit.standard)
        if module is None:
            raise _error(
                "AUTHORING.STANDARD_UNAVAILABLE",
                "unavailable",
                f"standard {edit.standard!r} is unavailable",
            )
        text = files[module.path].decode("utf-8")
        requires = _metadata_relationship_value(edit.requires)
        specializes = _metadata_relationship_value(edit.specializes)
        text = _replace_metadata_line(text, "Requires", requires)
        text = _replace_metadata_line(text, "Specializes", specializes)
        files[module.path] = text.encode("utf-8")

    @staticmethod
    def _revise_policy_unit(
        files: dict[str, bytes],
        edit: RevisePolicyUnit,
        base_corpus: Any,
    ) -> None:
        corpus = load_canonical_standards_corpus(FrozenContentSource(files))
        unit = corpus.resolve_policy_unit(edit.policy)
        if not isinstance(unit, PolicyUnit):
            raise _error(
                "AUTHORING.POLICY_UNIT_UNAVAILABLE",
                "unavailable",
                f"policy unit {edit.policy!r} is unavailable",
            )
        document = files[unit.document].decode("utf-8")
        if document.count(unit.content) != 1:
            raise _invalid(
                "AUTHORING.PROJECTION_DISAGREEMENT",
                f"policy unit {edit.policy!r} does not have one exact source section",
            )
        semantic_revision = _semantic_revision(
            edit.policy,
            unit,
            edit.semantics,
            base_corpus,
        )
        level = "#" * (len(unit.heading_path) + 1)
        body = edit.body.rstrip() + "\n"
        replacement = f"{level} {edit.title}\n\n{body}"
        files[unit.document] = document.replace(unit.content, replacement).encode(
            "utf-8"
        )
        units, tombstones = _policy_sidecar(files[unit.source])
        declaration = _active_declaration(units, edit.policy)
        declaration["heading_path"] = [*unit.heading_path[:-1], edit.title]
        declaration["semantic_revision"] = semantic_revision
        files[unit.source] = _render_policy_sidecar(units, tombstones)

    def _move_policy_unit(
        self,
        files: dict[str, bytes],
        edit: Mapping[str, object],
        base_corpus: Any,
        compile_current: Callable[[dict[str, bytes]], Any],
    ) -> None:
        compiled = compile_current(files)
        corpus = compiled.corpus
        policy = str(edit["policy"])
        unit = corpus.policy_unit_corpus.active_by_id(policy)
        if unit is None:
            raise _error(
                "AUTHORING.POLICY_UNIT_UNAVAILABLE",
                "unavailable",
                f"policy unit {policy!r} is unavailable",
            )
        destination_id = str(edit["standard"])
        destination = corpus.resolve_module(destination_id)
        if destination is None or destination.module_id != destination_id:
            raise _error(
                "AUTHORING.STANDARD_UNAVAILABLE",
                "unavailable",
                f"destination standard {destination_id!r} is unavailable",
            )
        anchor = None
        if "after_policy" in edit:
            anchor = corpus.policy_unit_corpus.active_by_id(str(edit["after_policy"]))
            if anchor is None or anchor.module != destination_id or anchor.id == policy:
                raise _invalid(
                    "AUTHORING.INVALID_PLACEMENT",
                    "policy placement anchor must be another active unit in the destination standard",
                )
        semantic_revision = _semantic_revision(
            policy,
            unit,
            _mapping(edit["semantics"], "policy semantic intent"),
            base_corpus,
        )
        source_text = files[unit.document].decode("utf-8")
        if source_text.count(unit.content) != 1:
            raise _invalid(
                "AUTHORING.PROJECTION_DISAGREEMENT",
                f"policy unit {policy!r} does not have one exact source section",
            )
        files[unit.document] = source_text.replace(unit.content, "").encode("utf-8")
        destination_text = files[destination.path].decode("utf-8")
        content = unit.content.rstrip() + "\n"
        if anchor is None:
            destination_text = destination_text.rstrip() + "\n\n" + content
        else:
            anchor_content = anchor.content
            if destination_text.count(anchor_content) != 1:
                raise _invalid(
                    "AUTHORING.PROJECTION_DISAGREEMENT",
                    "policy placement anchor does not have one exact source section",
                )
            destination_text = destination_text.replace(
                anchor_content,
                anchor_content.rstrip() + "\n\n" + content,
            )
        files[destination.path] = destination_text.encode("utf-8")

        old_units, old_tombstones = _policy_sidecar(files[unit.source])
        declaration = _pop_active_declaration(old_units, policy)
        declaration["module"] = destination_id
        declaration["semantic_revision"] = semantic_revision
        destination_sidecar = _ensure_policy_sidecar(files, destination_id)
        if destination_sidecar == unit.source:
            old_units.append(declaration)
            files[unit.source] = _render_policy_sidecar(old_units, old_tombstones)
        else:
            files[unit.source] = _render_policy_sidecar(old_units, old_tombstones)
            new_units, new_tombstones = _policy_sidecar(files[destination_sidecar])
            new_units.append(declaration)
            files[destination_sidecar] = _render_policy_sidecar(
                new_units, new_tombstones
            )
        relationships = [
            _relationship_from_semantics(item)
            for item in compiled.policy_impact.semantics.values()
            if item.source == policy
        ]
        if relationships:
            source_paths = {
                item.declaration_source
                for item in compiled.policy_impact.semantics.values()
                if item.source == policy
            }
            for path in source_paths:
                owner, current = _policy_impact_file(files[path])
                retained = [
                    item for item in current if str(item["source_policy"]) != policy
                ]
                files[path] = _render_policy_impact(owner, retained)
            destination_path = _policy_impact_source_for_owner(files, destination_id)
            owner, current = _policy_impact_file(files[destination_path])
            current.extend(relationships)
            files[destination_path] = _render_policy_impact(owner, current)

    def _put_policy_relationship(
        self,
        files: dict[str, bytes],
        value: object,
        base_snapshot: str | None,
        compile_current: Callable[[dict[str, bytes]], Any],
    ) -> None:
        compiled = compile_current(files)
        relationship = _resolved_policy_relationship(
            _mapping(value, "policy relationship"),
            compiled,
            base_snapshot,
        )
        self._put_resolved_policy_relationship(files, compiled, relationship)

    @staticmethod
    def _put_resolved_policy_relationship(
        files: dict[str, bytes],
        compiled: Any,
        relationship: Mapping[str, object],
    ) -> None:
        source = compiled.corpus.policy_unit_corpus.active_by_id(
            str(relationship["source_policy"])
        )
        if source is None:
            raise _error(
                "AUTHORING.POLICY_UNIT_UNAVAILABLE",
                "unavailable",
                f"policy unit {relationship['source_policy']!r} is unavailable",
            )
        path = _policy_impact_source(files, compiled, source)
        owner, relationships = _policy_impact_file(files[path])
        if owner != source.module:
            raise _invalid(
                "AUTHORING.PROJECTION_DISAGREEMENT",
                "policy-impact declaration owner disagrees with the source policy",
            )
        key = _policy_relationship_key(relationship)
        retained = [
            item for item in relationships if _policy_relationship_key(item) != key
        ]
        retained.append(relationship)
        files[path] = _render_policy_impact(owner, retained)

    def _remove_policy_relationship(
        self,
        files: dict[str, bytes],
        value: object,
        base_snapshot: str | None,
        compile_current: Callable[[dict[str, bytes]], Any],
    ) -> None:
        compiled = compile_current(files)
        requested = _resolved_policy_relationship(
            _mapping(value, "policy relationship"),
            compiled,
            base_snapshot,
        )
        key = _policy_relationship_key(requested)
        semantics = _policy_semantics_by_key(compiled, key)
        if semantics is None:
            raise _error(
                "AUTHORING.RELATIONSHIP_UNAVAILABLE",
                "unavailable",
                "policy relationship is unavailable",
            )
        existing = _relationship_from_semantics(semantics)
        if _canonical_json(existing) != _canonical_json(requested):
            raise _invalid(
                "AUTHORING.RELATIONSHIP_STALE",
                "remove-policy-relationship must bind the exact current relationship",
            )
        _remove_compiled_relationship(files, semantics)

    def _retire_policy_unit(
        self,
        files: dict[str, bytes],
        edit: Mapping[str, object],
        base_snapshot: str | None,
        compile_current: Callable[[dict[str, bytes]], Any],
    ) -> None:
        compiled = compile_current(files)
        policy = str(edit["policy"])
        unit = compiled.corpus.policy_unit_corpus.active_by_id(policy)
        if unit is None:
            raise _error(
                "AUTHORING.POLICY_UNIT_UNAVAILABLE",
                "unavailable",
                f"policy unit {policy!r} is unavailable",
            )
        if edit["retired_semantic_revision"] != unit.semantic_revision:
            raise _invalid(
                "AUTHORING.INVALID_SEMANTIC_REVISION",
                "retirement must bind the current accepted semantic revision",
            )
        incident = {
            _policy_relationship_key(_relationship_from_semantics(item)): item
            for item in compiled.policy_impact.semantics.values()
            if item.source == policy or item.consumer == policy
        }
        dispositions = _resolved_dispositions(
            edit["relationship_dispositions"], compiled, base_snapshot
        )
        supplied = {_disposition_key(item): item for item in dispositions}
        if set(supplied) != set(incident):
            raise _invalid(
                "AUTHORING.MISSING_SEMANTIC_DECISION",
                "policy retirement requires one disposition for every incident relationship and no others",
            )
        for key in sorted(supplied):
            self._apply_policy_disposition(
                files,
                incident[key],
                supplied[key],
                base_snapshot,
                compile_current,
            )

        document = files[unit.document].decode("utf-8")
        if document.count(unit.content) != 1:
            raise _invalid(
                "AUTHORING.PROJECTION_DISAGREEMENT",
                f"policy unit {policy!r} does not have one exact source section",
            )
        files[unit.document] = document.replace(unit.content, "").encode("utf-8")
        units, tombstones = _policy_sidecar(files[unit.source])
        _pop_active_declaration(units, policy)
        evidence = _evidence_list(edit["evidence"], "retirement evidence")
        successors = sorted(str(item) for item in edit["successors"])  # type: ignore[arg-type]
        tombstones.append(
            {
                "id": policy,
                "retired_semantic_revision": unit.semantic_revision,
                "successors": successors,
                "evidence": evidence[0].id,
            }
        )
        files[unit.source] = _render_policy_sidecar(units, tombstones)
        for successor_id in successors:
            successor = compiled.corpus.policy_unit_corpus.active_by_id(successor_id)
            if successor is None:
                raise _invalid(
                    "AUTHORING.INVALID_SUCCESSOR",
                    f"policy successor {successor_id!r} is unavailable",
                )
            successor_units, successor_tombstones = _policy_sidecar(
                files[successor.source]
            )
            declaration = _active_declaration(successor_units, successor_id)
            predecessors = set(
                str(item) for item in declaration.get("predecessors", [])
            )
            predecessors.add(policy)
            declaration["predecessors"] = sorted(predecessors)
            files[successor.source] = _render_policy_sidecar(
                successor_units, successor_tombstones
            )

    def _retire_standard(
        self,
        files: dict[str, bytes],
        edit: Mapping[str, object],
        base_snapshot: str | None,
        compile_current: Callable[[dict[str, bytes]], Any],
    ) -> None:
        compiled = compile_current(files)
        standard = str(edit["standard"])
        module = compiled.corpus.resolve_module(standard)
        if module is None or module.module_id != standard:
            raise _error(
                "AUTHORING.STANDARD_UNAVAILABLE",
                "unavailable",
                f"standard {standard!r} is unavailable",
            )
        active_units = compiled.corpus.policy_unit_corpus.for_module(standard)
        if active_units:
            raise _invalid(
                "AUTHORING.POLICY_UNITS_ACTIVE",
                "retire every registered policy unit before retiring its standard",
            )
        for successor in edit["successors"]:  # type: ignore[union-attr]
            candidate = compiled.corpus.resolve_module(str(successor))
            if candidate is None or candidate.module_id != successor:
                raise _invalid(
                    "AUTHORING.INVALID_SUCCESSOR",
                    f"standard successor {successor!r} is unavailable",
                )
        module_incident: dict[str, Mapping[str, object]] = {}
        for candidate in compiled.corpus.modules:
            for relation, targets in (
                ("requires", candidate.requires),
                ("specializes", candidate.specializes),
            ):
                for target in targets:
                    if candidate.module_id == standard or target == standard:
                        key = {
                            "kind": "module-relationship",
                            "relation": relation,
                            "source": candidate.module_id,
                            "target": target,
                        }
                        module_incident[_canonical_json(key)] = key
        policy_incident = {
            _policy_relationship_key(_relationship_from_semantics(item)): item
            for item in compiled.policy_impact.semantics.values()
            if item.consumer == standard
        }
        dispositions = _resolved_dispositions(
            edit["relationship_dispositions"], compiled, base_snapshot
        )
        supplied = {_disposition_key(item): item for item in dispositions}
        expected = set(module_incident) | set(policy_incident)
        if set(supplied) != expected:
            raise _invalid(
                "AUTHORING.MISSING_SEMANTIC_DECISION",
                "standard retirement requires one disposition for every incident relationship and no others",
            )
        for encoded in sorted(supplied):
            disposition = supplied[encoded]
            key = _mapping(disposition["relationship"], "relationship key")
            if key.get("kind") == "module-relationship":
                self._apply_module_disposition(files, key, disposition)
            else:
                semantics = policy_incident[encoded]
                self._apply_policy_disposition(
                    files,
                    semantics,
                    disposition,
                    base_snapshot,
                    compile_current,
                )
        impact_registry = _impact_registry(files[POLICY_IMPACT_REGISTRY])
        for path_value in impact_registry["declaration_sources"]:  # type: ignore[union-attr]
            path = str(path_value)
            owner, relationships = _policy_impact_file(files[path])
            if owner != standard:
                continue
            if relationships:
                raise _invalid(
                    "AUTHORING.MISSING_SEMANTIC_DECISION",
                    "standard retirement left relationships in its policy-impact authority",
                )
            files.pop(path)
            _set_impact_source(files, path, present=False)
        files.pop(module.path)
        _set_registry_list(
            files, CANONICAL_MODULE_CORPUS, "members", module.path, present=False
        )

    @staticmethod
    def _apply_module_disposition(
        files: dict[str, bytes],
        key: Mapping[str, object],
        disposition: Mapping[str, object],
    ) -> None:
        corpus = load_canonical_standards_corpus(FrozenContentSource(files))
        source = corpus.resolve_module(str(key["source"]))
        if source is None or source.module_id != key["source"]:
            raise _error(
                "AUTHORING.RELATIONSHIP_UNAVAILABLE",
                "unavailable",
                "module relationship source is unavailable",
            )
        relation = str(key["relation"])
        targets = set(source.requires if relation == "requires" else source.specializes)
        target = str(key["target"])
        if target not in targets:
            raise _error(
                "AUTHORING.RELATIONSHIP_UNAVAILABLE",
                "unavailable",
                "module relationship is unavailable",
            )
        targets.remove(target)
        if disposition["disposition"] == "retarget":
            replacement = disposition["replacement_consumer"]
            if type(replacement) is not str:
                raise _invalid(
                    "AUTHORING.INVALID_RELATIONSHIP_TARGET",
                    "module relationships can only retarget another standard",
                )
            targets.add(replacement)
        text = files[source.path].decode("utf-8")
        files[source.path] = _replace_metadata_line(
            text,
            "Requires" if relation == "requires" else "Specializes",
            _metadata_relationship_value(tuple(sorted(targets))),
        ).encode("utf-8")

    def _apply_policy_disposition(
        self,
        files: dict[str, bytes],
        semantics: Any,
        disposition: Mapping[str, object],
        base_snapshot: str | None,
        compile_current: Callable[[dict[str, bytes]], Any],
    ) -> None:
        existing = _relationship_from_semantics(semantics)
        _remove_compiled_relationship(files, semantics)
        if disposition["disposition"] == "retarget":
            replacement = disposition["replacement_consumer"]
            updated = {**existing, "consumer": replacement}
            compiled = compile_current(files)
            self._put_resolved_policy_relationship(files, compiled, updated)


def _metadata_relationship_value(values: tuple[str, ...]) -> str:
    return "`none`" if not values else ", ".join(f"`{value}`" for value in values)


def _replace_metadata_line(text: str, field: str, value: str) -> str:
    pattern = re.compile(rf"^- {re.escape(field)}: .*?$", re.MULTILINE)
    if len(pattern.findall(text)) != 1:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            f"standard metadata must contain one {field} field",
        )
    return pattern.sub(f"- {field}: {value}", text)


def _projection_order(edit: LogicalEdit) -> tuple[int, str]:
    kind = str(edit.as_contract()["kind"])
    priority = {
        "create-standard": 0,
        "put-routing-fact": 45,
        "revise-standard": 10,
        "rewrite-navigation-index": 65,
        "put-routing-rule": 45,
        "remove-routing-rule": 45,
        "remove-routing-fact": 45,
        "revise-policy-unit": 20,
        "move-policy-unit": 30,
        "replace-standard-relationships": 40,
        "put-policy-relationship": 40,
        "remove-policy-relationship": 40,
        "retire-policy-unit": 50,
        "retire-standard": 60,
        "audit-policy-unit": 70,
    }
    return priority[kind], _canonical_json(edit.as_contract())


def authoring_target_id(snapshot: str, consumer: str) -> str:
    return _digest_value(
        "coding-standards:authoring-target:v1",
        {"snapshot": snapshot, "consumer": consumer},
    )


def _new_standard_path(standard: str, role: str) -> str:
    parts = standard.split(".")
    if role == "topic" and len(parts) >= 2 and parts[0] == "topic":
        return "topics/" + "/".join(parts[1:]) + ".md"
    if role == "workflow" and len(parts) >= 2 and parts[0] == "workflow":
        return "workflows/" + "/".join(parts[1:]) + ".md"
    if role == "reference" and len(parts) >= 3 and parts[0] == "reference":
        return "reference/" + "/".join(parts[1:]) + ".md"
    if role == "profile" and len(parts) >= 3 and parts[0] == "profile":
        roots = {
            "application": "applications",
            "boundary": "boundaries",
            "framework": "frameworks",
            "language": "languages",
            "workflow": "workflows",
        }
        root = roots.get(parts[1])
        if root is not None:
            return "profiles/" + root + "/" + "/".join(parts[2:]) + ".md"
    raise _unsupported(
        "AUTHORING.STANDARD_PLACEMENT_UNSUPPORTED",
        f"standard {standard!r} does not have an unambiguous canonical placement",
    )


def _render_standard(
    standard: Mapping[str, object],
    requires: tuple[str, ...],
    specializes: tuple[str, ...],
    path: str,
) -> bytes:
    body = str(standard["body"]).strip()
    text = (
        f"# {standard['title']}\n\n"
        "**Standards metadata**\n\n"
        f"- ID: `{standard['id']}`\n"
        f"- Role: `{standard['role']}`\n"
        f"- Level: `{standard['level']}`\n"
        f"- Applies when: {standard['applies_when']}\n"
        f"- Does not apply when: {standard['does_not_apply_when']}\n"
        f"- Requires: {_metadata_relationship_value(requires)}\n"
        f"- Specializes: {_metadata_relationship_value(specializes)}\n"
        f"- Verification: {standard['verification']}\n"
        f"- Canonical owner: `{path}`\n\n"
        f"{body}\n"
    )
    return text.encode("utf-8")


def _toml_string(value: object) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def _toml_array(values: Iterable[object]) -> str:
    return "[" + ", ".join(_toml_string(item) for item in values) + "]"


def _toml_inline(value: object) -> str:
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        return str(value)
    if type(value) is str:
        return _toml_string(value)
    if isinstance(value, list):
        return "[" + ", ".join(_toml_inline(item) for item in value) + "]"
    if isinstance(value, Mapping):
        return (
            "{ "
            + ", ".join(
                f"{key} = {_toml_inline(item)}" for key, item in sorted(value.items())
            )
            + " }"
        )
    raise _invalid(
        "AUTHORING.INVALID_ARGUMENTS",
        "value cannot be represented by a fixed TOML authority",
    )


def _simple_registry(content: bytes, field: str) -> list[str]:
    try:
        raw = tomllib.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT", "registry is invalid TOML"
        ) from error
    if set(raw) != {"schema_version", field} or raw["schema_version"] != 1:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT", "registry contract is unsupported"
        )
    values = raw[field]
    if not isinstance(values, list) or any(type(item) is not str for item in values):
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT", "registry members are invalid"
        )
    return list(values)


def _set_registry_list(
    files: dict[str, bytes],
    path: str,
    field: str,
    value: str,
    *,
    present: bool,
) -> None:
    values = _simple_registry(files[path], field)
    if present:
        if value in values:
            raise _invalid(
                "AUTHORING.PROJECTION_DISAGREEMENT",
                f"registry already contains {value!r}",
            )
        values.append(value)
    else:
        if value not in values:
            raise _invalid(
                "AUTHORING.PROJECTION_DISAGREEMENT",
                f"registry does not contain {value!r}",
            )
        values.remove(value)
    selected = sorted(values)
    body = "\n".join(f"  {_toml_string(item)}," for item in selected)
    files[path] = f"schema_version = 1\n{field} = [\n{body}\n]\n".encode("utf-8")


def _policy_sidecar_path(module: str) -> str:
    return f"{_POLICY_UNIT_ROOT}/{module}.toml"


def _policy_sidecar(
    content: bytes,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    try:
        raw = tomllib.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT", "policy-unit sidecar is invalid TOML"
        ) from error
    if raw.get("schema_version") != 1 or set(raw) - {
        "schema_version",
        "policy_unit",
        "tombstone",
    }:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            "policy-unit sidecar contract is unsupported",
        )
    units = raw.get("policy_unit", [])
    tombstones = raw.get("tombstone", [])
    if not isinstance(units, list) or not isinstance(tombstones, list):
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT", "policy-unit declarations are invalid"
        )
    return [dict(item) for item in units], [dict(item) for item in tombstones]


def _render_policy_sidecar(
    units: Iterable[Mapping[str, object]],
    tombstones: Iterable[Mapping[str, object]],
) -> bytes:
    lines = ["schema_version = 1"]
    for item in sorted(units, key=lambda value: str(value["id"])):
        lines.extend(
            [
                "",
                "[[policy_unit]]",
                f"id = {_toml_string(item['id'])}",
                f"module = {_toml_string(item['module'])}",
                f"heading_path = {_toml_array(item['heading_path'])}",  # type: ignore[arg-type]
                f"semantic_revision = {item['semantic_revision']}",
            ]
        )
        for field in ("aliases", "predecessors", "successors"):
            values = item.get(field, [])
            if values:
                lines.append(f"{field} = {_toml_array(values)}")  # type: ignore[arg-type]
    for item in sorted(tombstones, key=lambda value: str(value["id"])):
        lines.extend(
            [
                "",
                "[[tombstone]]",
                f"id = {_toml_string(item['id'])}",
                f"retired_semantic_revision = {item['retired_semantic_revision']}",
                f"successors = {_toml_array(item['successors'])}",  # type: ignore[arg-type]
                f"evidence = {_toml_string(item['evidence'])}",
            ]
        )
    return ("\n".join(lines) + "\n").encode("utf-8")


def _active_declaration(
    units: list[dict[str, object]], policy: str
) -> dict[str, object]:
    matches = [item for item in units if item.get("id") == policy]
    if len(matches) != 1:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            f"policy-unit sidecar must declare {policy!r} exactly once",
        )
    return matches[0]


def _pop_active_declaration(
    units: list[dict[str, object]], policy: str
) -> dict[str, object]:
    selected = _active_declaration(units, policy)
    units.remove(selected)
    return selected


def _ensure_policy_sidecar(files: dict[str, bytes], module: str) -> str:
    sources = _simple_registry(files[POLICY_UNIT_REGISTRY], "sources")
    for path in sources:
        units, _ = _policy_sidecar(files[path])
        if any(item.get("module") == module for item in units):
            return path
    path = _policy_sidecar_path(module)
    if path in files:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            "derived policy-unit sidecar already exists but is unregistered",
        )
    files[path] = _render_policy_sidecar([], [])
    _set_registry_list(files, POLICY_UNIT_REGISTRY, "sources", path, present=True)
    return path


def _semantic_revision(
    policy: str,
    current: PolicyUnit,
    semantics: Mapping[str, object],
    base_corpus: Any,
) -> int:
    kind = semantics["kind"]
    if kind == "preserve":
        if semantics["semantic_revision"] != current.semantic_revision:
            raise _invalid(
                "AUTHORING.INVALID_SEMANTIC_REVISION",
                "preserved semantics must bind the current semantic revision",
            )
        return current.semantic_revision
    accepted = base_corpus.policy_unit_corpus.active_by_id(policy)
    if accepted is None:
        raise _invalid(
            "AUTHORING.INVALID_SEMANTIC_REVISION",
            "a policy added by this proposal must remain at semantic revision one",
        )
    if (
        semantics["accepted_semantic_revision"] != accepted.semantic_revision
        or semantics["proposed_semantic_revision"] != accepted.semantic_revision + 1
        or current.semantic_revision != accepted.semantic_revision
    ):
        raise _invalid(
            "AUTHORING.INVALID_SEMANTIC_REVISION",
            "semantic change must bind the base accepted revision and its single proposed successor",
        )
    # A1c keeps the accepted semantic revision in the proposed corpus. The
    # requested successor is carried separately by SemanticProposal until an
    # accepted application materializes it.
    return accepted.semantic_revision


def _impact_registry(content: bytes) -> dict[str, object]:
    try:
        raw = tomllib.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            "policy-impact registry is invalid TOML",
        ) from error
    expected = {
        "schema_version",
        "source_id",
        "authoring_contract",
        "node_catalog",
        "fact_catalog",
        "suite_registry",
        "declaration_sources",
    }
    if set(raw) != expected or raw.get("schema_version") != 2:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            "policy-impact registry contract is unsupported",
        )
    return dict(raw)


def _render_impact_registry(raw: Mapping[str, object]) -> bytes:
    sources = sorted(str(item) for item in raw["declaration_sources"])  # type: ignore[arg-type]
    body = "\n".join(f"  {_toml_string(item)}," for item in sources)
    return (
        "schema_version = 2\n"
        f"source_id = {_toml_string(raw['source_id'])}\n"
        f"authoring_contract = {_toml_string(raw['authoring_contract'])}\n"
        f"node_catalog = {_toml_string(raw['node_catalog'])}\n"
        f"fact_catalog = {_toml_string(raw['fact_catalog'])}\n"
        f"suite_registry = {_toml_string(raw['suite_registry'])}\n"
        f"declaration_sources = [\n{body}\n]\n"
    ).encode("utf-8")


def _set_impact_source(files: dict[str, bytes], path: str, *, present: bool) -> None:
    raw = _impact_registry(files[POLICY_IMPACT_REGISTRY])
    values = list(raw["declaration_sources"])  # type: ignore[arg-type]
    if present:
        if path in values:
            raise _invalid(
                "AUTHORING.PROJECTION_DISAGREEMENT",
                "policy-impact source is already registered",
            )
        values.append(path)
    else:
        if path not in values:
            raise _invalid(
                "AUTHORING.PROJECTION_DISAGREEMENT",
                "policy-impact source is not registered",
            )
        values.remove(path)
    raw["declaration_sources"] = values
    files[POLICY_IMPACT_REGISTRY] = _render_impact_registry(raw)


def _policy_impact_file(content: bytes) -> tuple[str, list[dict[str, object]]]:
    try:
        raw = tomllib.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT", "policy-impact source is invalid TOML"
        ) from error
    if (
        set(raw) != {"schema_version", "owner", "relationships"}
        or raw.get("schema_version") != 2
    ):
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            "policy-impact source contract is unsupported",
        )
    relationships = raw["relationships"]
    if not isinstance(relationships, list):
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            "policy-impact relationships are invalid",
        )
    selected = []
    for item in relationships:
        value = dict(item)
        value["source_policy"] = value.pop("source")
        value.setdefault("source_scope", None)
        value.setdefault("consumer_scope", None)
        selected.append(value)
    return str(raw["owner"]), selected


def _render_policy_impact(
    owner: str, relationships: Iterable[Mapping[str, object]]
) -> bytes:
    lines = ["schema_version = 2", f"owner = {_toml_string(owner)}"]
    selected = sorted(relationships, key=_policy_relationship_key)
    if not selected:
        lines.append("relationships = []")
    for item in selected:
        lines.extend(
            [
                "",
                "[[relationships]]",
                f"source = {_toml_string(item['source_policy'])}",
                f"consumer = {_toml_string(item['consumer'])}",
                f"relation = {_toml_string(item['relation'])}",
                f"applicability = {_toml_inline(item['applicability'])}",
            ]
        )
        for field in ("source_scope", "consumer_scope"):
            if item[field] is not None:
                lines.append(f"{field} = {_toml_inline(item[field])}")
        lines.extend(
            [
                f"evidence_owner = {_toml_string(item['evidence_owner'])}",
                f"rationale = {_toml_string(item['rationale'])}",
            ]
        )
    return ("\n".join(lines) + "\n").encode("utf-8")


def _policy_impact_source(
    files: dict[str, bytes], compiled: Any, unit: PolicyUnit
) -> str:
    paths = {
        item.declaration_source
        for item in compiled.policy_impact.semantics.values()
        if item.source == unit.id
    }
    if len(paths) == 1:
        return paths.pop()
    return _policy_impact_source_for_owner(files, unit.module)


def _policy_impact_source_for_owner(files: dict[str, bytes], owner_id: str) -> str:
    registry = _impact_registry(files[POLICY_IMPACT_REGISTRY])
    for path in registry["declaration_sources"]:  # type: ignore[union-attr]
        owner, _ = _policy_impact_file(files[str(path)])
        if owner == owner_id:
            return str(path)
    path = f"{_POLICY_IMPACT_ROOT}/{owner_id}.toml"
    if path in files:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            "derived policy-impact source already exists but is unregistered",
        )
    files[path] = _render_policy_impact(owner_id, [])
    _set_impact_source(files, path, present=True)
    return path


def _policy_relationship_key(value: Mapping[str, object]) -> str:
    return _canonical_json(
        {
            "kind": "policy-relationship",
            "source_policy": value.get("source_policy", value.get("source")),
            "consumer": value["consumer"],
            "relation": value["relation"],
        }
    )


def _relationship_from_semantics(value: Any) -> dict[str, object]:
    return {
        "source_policy": value.source,
        "consumer": value.consumer,
        "relation": value.relation,
        "applicability": value.applicability_program.as_expression(),
        "source_scope": thaw(value.source_scope),
        "consumer_scope": thaw(value.consumer_scope),
        "evidence_owner": value.evidence_owner,
        "rationale": value.rationale,
    }


def _policy_semantics_by_key(compiled: Any, key: str) -> Any | None:
    return next(
        (
            item
            for item in compiled.policy_impact.semantics.values()
            if _policy_relationship_key(_relationship_from_semantics(item)) == key
        ),
        None,
    )


def _remove_compiled_relationship(files: dict[str, bytes], semantics: Any) -> None:
    owner, relationships = _policy_impact_file(files[semantics.declaration_source])
    key = _policy_relationship_key(_relationship_from_semantics(semantics))
    retained = [item for item in relationships if _policy_relationship_key(item) != key]
    if len(retained) != len(relationships) - 1:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            "compiled policy relationship does not resolve exactly once in its authority",
        )
    files[semantics.declaration_source] = _render_policy_impact(owner, retained)


def _resolve_consumer(value: object, compiled: Any, base_snapshot: str | None) -> str:
    if type(value) is str:
        if value in compiled.policy_impact.artifacts:
            raise _invalid(
                "AUTHORING.TARGET_HANDLE_REQUIRED",
                "non-standard relationship consumers require a Snapshot-bound authoring target handle",
            )
        return value
    handle = _mapping(value, "authoring target handle")
    snapshot = _mapping(handle["snapshot"], "authoring target snapshot")
    if base_snapshot is None or snapshot["id"] != base_snapshot:
        raise _invalid(
            "AUTHORING.TARGET_SNAPSHOT_MISMATCH",
            "authoring target handle does not bind the proposal base Snapshot",
        )
    matches = [
        identity
        for identity in compiled.policy_impact.artifacts
        if authoring_target_id(base_snapshot, identity) == handle["id"]
    ]
    if len(matches) != 1:
        raise _error(
            "AUTHORING.TARGET_UNAVAILABLE",
            "unavailable",
            "authoring target handle does not resolve in the base Snapshot catalog",
        )
    return matches[0]


def _resolved_policy_relationship(
    value: Mapping[str, object],
    compiled: Any,
    base_snapshot: str | None,
) -> dict[str, object]:
    return {
        **value,
        "consumer": _resolve_consumer(value["consumer"], compiled, base_snapshot),
    }


def _resolved_dispositions(
    value: object,
    compiled: Any,
    base_snapshot: str | None,
) -> tuple[dict[str, object], ...]:
    dispositions = _dispositions(value)
    resolved = []
    for disposition in dispositions:
        item = dict(disposition)
        relationship = dict(_mapping(item["relationship"], "relationship key"))
        if relationship["kind"] == "policy-relationship":
            relationship["consumer"] = _resolve_consumer(
                relationship["consumer"], compiled, base_snapshot
            )
        item["relationship"] = relationship
        if item["disposition"] == "retarget":
            item["replacement_consumer"] = _resolve_consumer(
                item["replacement_consumer"], compiled, base_snapshot
            )
        resolved.append(item)
    return tuple(resolved)


def _disposition_key(value: Mapping[str, object]) -> str:
    relationship = _mapping(value["relationship"], "relationship key")
    if relationship["kind"] == "policy-relationship":
        return _policy_relationship_key(relationship)
    return _canonical_json(relationship)


def _analysis_policy_ids(
    base_compiled: Any,
    compiled: Any,
    program: LogicalProgram,
) -> tuple[str, ...]:
    """Select existing policies whose explicit relationships changed."""

    accepted = {unit.id: unit for unit in base_compiled.corpus.policy_unit_corpus.units}
    proposed = {unit.id: unit for unit in compiled.corpus.policy_unit_corpus.units}
    selected: set[str] = set()
    for change_set in program.change_sets:
        for edit in change_set.edits:
            raw = edit.as_contract()
            kind = raw["kind"]
            if kind == "audit-policy-unit":
                selected.add(str(raw["policy"]))
                continue
            if kind not in {
                "put-policy-relationship",
                "remove-policy-relationship",
            }:
                continue
            relationship = _mapping(raw["relationship"], "policy relationship")
            selected.add(str(relationship["source_policy"]))
    return tuple(sorted(set(accepted).intersection(proposed, selected)))


def _analysis_module_ids(program: LogicalProgram) -> tuple[str, ...]:
    selected: set[str] = set()
    for change_set in program.change_sets:
        for edit in change_set.edits:
            raw = edit.as_contract()
            kind = raw["kind"]
            if kind == "create-standard":
                standard = _mapping(raw["standard"], "standard content")
                selected.add(str(standard["id"]))
            elif kind in {
                "put-routing-rule",
                "remove-routing-rule",
                "put-routing-fact",
                "remove-routing-fact",
            }:
                selected.add("router")
            elif kind == "revise-standard":
                standard = _mapping(raw["standard"], "standard content")
                selected.add(str(standard["id"]))
            elif kind in {
                "replace-standard-relationships",
                "retire-standard",
            }:
                selected.add(str(raw["standard"]))
    return tuple(sorted(selected))


def _validate_final_standard_successors(
    compiled: Any,
    program: LogicalProgram,
) -> None:
    for change_set in program.change_sets:
        for edit in change_set.edits:
            raw = edit.as_contract()
            if raw["kind"] != "retire-standard":
                continue
            for successor in raw["successors"]:  # type: ignore[union-attr]
                candidate = compiled.corpus.resolve_module(str(successor))
                if candidate is None or candidate.module_id != successor:
                    raise _invalid(
                        "AUTHORING.INVALID_SUCCESSOR",
                        f"standard successor {successor!r} is unavailable in the final proposal",
                    )


def _semantic_proposals(
    base_compiled: Any,
    compiled: Any,
    program: LogicalProgram,
) -> tuple[dict[str, object], ...]:
    semantic_intents: dict[str, tuple[int | None, str]] = {}
    for change_set in program.change_sets:
        for edit in change_set.edits:
            if isinstance(edit, RevisePolicyUnit):
                if edit.semantics["kind"] == "change":
                    semantic_intents[edit.policy] = (
                        int(edit.semantics["accepted_semantic_revision"]),
                        str(edit.semantics["intent"]),
                    )
            elif isinstance(edit, StructuredEdit):
                raw = edit.as_contract()
                if raw["kind"] == "create-standard":
                    for unit_value in raw["policy_units"]:  # type: ignore[union-attr]
                        unit = _mapping(unit_value, "new policy unit")
                        semantic_intents[str(unit["id"])] = (None, str(unit["intent"]))
                elif raw["kind"] == "move-policy-unit":
                    semantics = _mapping(raw["semantics"], "policy semantic intent")
                    if semantics["kind"] == "change":
                        semantic_intents[str(raw["policy"])] = (
                            int(semantics["accepted_semantic_revision"]),
                            str(semantics["intent"]),
                        )
    base_corpus = base_compiled.corpus
    proposed_corpus = compiled.corpus
    proposals: list[dict[str, object]] = []
    accepted_by_id = {item.id: item for item in base_corpus.policy_unit_corpus.units}
    proposed_by_id = {
        item.id: item for item in proposed_corpus.policy_unit_corpus.units
    }
    for policy, proposed in sorted(proposed_by_id.items()):
        accepted = accepted_by_id.get(policy)
        changed_structure = (
            accepted is None
            or accepted.structural_digest != proposed.structural_digest
            or accepted.semantic_revision != proposed.semantic_revision
        )
        semantic = semantic_intents.get(policy)
        if changed_structure and semantic is None:
            raise _invalid(
                "AUTHORING.SEMANTICS_REQUIRED",
                f"policy unit {policy!r} changed structurally without explicit semantic intent",
            )
        if semantic is None:
            continue
        accepted_revision, intent = semantic
        expected_revision = 1 if accepted is None else accepted.semantic_revision + 1
        if accepted_revision != (
            None if accepted is None else accepted.semantic_revision
        ):
            raise _invalid(
                "AUTHORING.INVALID_SEMANTIC_REVISION",
                f"semantic intent for {policy!r} does not bind the base revision",
            )
        corpus_revision = 1 if accepted is None else accepted.semantic_revision
        if proposed.semantic_revision != corpus_revision:
            raise _invalid(
                "AUTHORING.INVALID_SEMANTIC_REVISION",
                f"proposed corpus for {policy!r} must retain accepted revision {corpus_revision}",
            )
        proposals.append(
            {
                "policy": policy,
                "accepted_semantic_revision": accepted_revision,
                "proposed_semantic_revision": expected_revision,
                "intent": intent,
                "structural_digest": proposed.structural_digest,
            }
        )
    orphaned = sorted(
        policy
        for policy in set(semantic_intents) - set(proposed_by_id)
        if not isinstance(
            proposed_corpus.resolve_policy_unit(policy), PolicyUnitTombstone
        )
    )
    if orphaned:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            f"semantic intent for {orphaned[0]!r} has no active proposed policy unit",
        )
    return tuple(proposals)


def _repository_paths(paths: Iterable[str]) -> tuple[str, ...]:
    try:
        selected = tuple(sorted(str(RepositoryPath.parse(path)) for path in paths))
    except (GitRepositoryError, TypeError) as error:
        raise _invalid(
            "AUTHORING.INVALID_REPOSITORY_PATHS",
            "base repository path observation is invalid",
        ) from error
    if not selected or len(set(selected)) != len(selected):
        raise _invalid(
            "AUTHORING.INVALID_REPOSITORY_PATHS",
            "base repository path observation must contain unique paths",
        )
    return selected


def _refresh_suite_input_projection(
    files: dict[str, bytes],
    base_file_paths: frozenset[str],
    base_repository_paths: tuple[str, ...],
) -> tuple[str, ...]:
    """Delegate the proposed manifest to its canonical compiler."""

    try:
        current_paths = {str(RepositoryPath.parse(path)) for path in files}
        if not base_file_paths <= set(base_repository_paths):
            raise _invalid(
                "AUTHORING.PROJECTION_DISAGREEMENT",
                "captured authority paths are absent from the base revision",
            )
        proposed_paths = tuple(
            sorted(
                (set(base_repository_paths) - (base_file_paths - current_paths))
                | (current_paths - base_file_paths)
            )
        )
        with tempfile.TemporaryDirectory(
            prefix="coding-standards-logical-authoring-"
        ) as temporary:
            root = Path(temporary)
            for raw_path in proposed_paths:
                path = RepositoryPath.parse(raw_path)
                destination = root.joinpath(*path.components)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.touch()
            for raw_path, content in files.items():
                path = RepositoryPath.parse(raw_path)
                destination = root.joinpath(*path.components)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(content)
            git_output(root, ("init", "--quiet"))
            git_output(root, ("add", "--force", "--all", "--"))
            files[_SUITE_INPUTS] = suite_input_projection_bytes(
                root,
                repository_paths=proposed_paths,
            )
        return proposed_paths
    except AuthoringError:
        raise
    except EngineError as error:
        diagnostic = error.diagnostic
        raise _error(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            diagnostic.outcome,
            f"canonical suite-input projection failed: {diagnostic.render()}",
        ) from error
    except GitRepositoryError as error:
        raise _invalid(
            "AUTHORING.PROJECTION_DISAGREEMENT",
            "logical projection contains an invalid repository path",
        ) from error
    except OSError as error:
        raise _error(
            "AUTHORING.PROJECTION_UNAVAILABLE",
            "unavailable",
            "canonical suite-input projection could not be materialized",
        ) from error


__all__ = (
    "ChangePurpose",
    "EvidenceReference",
    "LogicalAuthoringCompiler",
    "LogicalProjection",
    "LogicalProgram",
    "ReplaceStandardRelationships",
    "RevisePolicyUnit",
    "StandardsChangeSet",
    "authoring_target_id",
)


_ROUTING_EDITS = frozenset(
    {
        "put-routing-rule",
        "remove-routing-rule",
        "put-routing-fact",
        "remove-routing-fact",
    }
)


def _routing_fact_signature(definition: Mapping[str, object]) -> dict[str, object]:
    """Use the fact owner's semantics, including unordered values and nonsemantic aliases."""
    schema = compile_fact_schema(
        {
            "kind": "applicability-fact-schema",
            "id": "router.authoring-fact",
            "version": 2,
            "facts": [dict(definition)],
        }
    )
    signature = schema.definitions[0].semantic_projection()
    del signature["semantic_revision"]
    return signature


def _edit_routing(files: dict[str, bytes], edits: list[Mapping[str, object]]) -> None:
    path = "evaluation/standards-effectiveness/router-projection.toml"
    raw = tomllib.loads(files[path].decode("utf-8"))
    guidance = []
    for edit in edits:
        kind = str(edit["kind"])
        field = "rule" if kind.endswith("rule") else "fact"
        collection = "rules" if field == "rule" else "facts"
        value = edit[field]
        identifier = value["id"] if isinstance(value, Mapping) else value
        prior = next(
            (item for item in raw[collection] if item["id"] == identifier), None
        )
        if kind.startswith("remove-"):
            if prior is None:
                raise _invalid(
                    "AUTHORING.ROUTING_ENTRY_UNKNOWN", "routing entry does not exist"
                )
            raw[collection].remove(prior)
            if field == "rule":
                guidance.append((prior["target"], None, None))
            continue
        assert isinstance(value, Mapping)
        if field == "fact":
            replacement = dict(value)
            replacement.update(
                context_kind="task-route",
                answer_contract="fact-value.v1",
                evidence_contract="evidence-reference.v1",
                authorization_capability="standards.analyze",
            )
            changed = prior is not None and _routing_fact_signature(
                prior
            ) != _routing_fact_signature(replacement)
            expected_revision = (
                1 if prior is None else prior["semantic_revision"] + int(changed)
            )
            if value["semantic_revision"] != expected_revision:
                raise _invalid(
                    "AUTHORING.INVALID_SEMANTIC_REVISION",
                    "routing fact revision must track its semantic change",
                )

        else:
            replacement = {key: value[key] for key in ("id", "target", "when")}
            guidance.append(
                (
                    prior["target"] if prior else None,
                    value["target"],
                    value["condition"],
                )
            )
        if prior is None:
            raw[collection].append(replacement)
        else:
            raw[collection][raw[collection].index(prior)] = replacement
    targets = [rule["target"] for rule in raw["rules"]]
    if len(set(targets)) != len(targets):
        raise _invalid(
            "AUTHORING.DUPLICATE_ROUTE_TARGET", "a route already owns this target"
        )
    if guidance:
        _project_route_guidance(files, guidance, set(targets))
    header = [
        f"{key} = {_toml_inline(value)}"
        for key, value in raw.items()
        if key not in {"facts", "rules"}
    ]
    for name in ("facts", "rules"):
        for item in sorted(raw[name], key=lambda item: item["id"]):
            header.extend(["", f"[[{name}]]"])
            header.extend(
                f"{key} = {_toml_inline(value)}" for key, value in item.items()
            )
    files[path] = ("\n".join(header) + "\n").encode("utf-8")


def _project_route_guidance(
    files: dict[str, bytes],
    edits: list[tuple[str | None, str | None, str | None]],
    selected_targets: set[str],
) -> None:
    modules = load_canonical_module_corpus(FrozenContentSource(files))

    def target_path(identifier: str) -> str:
        module = modules.resolve(identifier)
        if module is None or module.role == "reference":
            raise _invalid(
                "AUTHORING.ROUTE_TARGET_UNKNOWN",
                "route target must be a normative standard",
            )
        return module.path

    source = "STANDARDS-ROUTER.md"
    text = files[source].decode("utf-8")
    start_marker, end_marker = (
        "## Workflow Selection",
        "## S1 Rust Library Bug-Fix Route",
    )
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise _invalid(
            "AUTHORING.ROUTING_GUIDANCE_AMBIGUOUS",
            "route selection boundaries must be unique",
        )
    start, end = text.index(start_marker), text.index(end_marker)
    if end <= start:
        raise _invalid(
            "AUTHORING.ROUTING_GUIDANCE_AMBIGUOUS",
            "route selection boundaries are reversed",
        )
    section = text[start:end]
    original = section.splitlines(keepends=True)
    lines = original.copy()
    additions = []
    retired_links = []
    for old_target, target, condition in edits:
        old_path = target_path(old_target) if old_target is not None else None
        path = target_path(target) if target is not None else None
        replacement = ""
        if path is not None:
            title = files[path].decode("utf-8").splitlines()[0].removeprefix("# ")
            title = title.replace("|", "\\|")
            cell = str(condition).replace("\\", "\\\\").replace("|", "\\|")
            replacement = f"| {cell} | [{title}]({path}) |\n"
        old_link = (
            re.compile(r"\[[^]]+\]\(" + re.escape(old_path) + r"(?:#[^)]*)?\)")
            if old_path is not None
            else None
        )
        rows = [
            index
            for index, line in enumerate(original)
            if line.startswith("|") and old_link and old_link.search(line)
        ]
        if old_path is not None and len(rows) != 1:
            raise _invalid(
                "AUTHORING.ROUTING_GUIDANCE_AMBIGUOUS",
                "route target must have exactly one selection row",
            )
        if rows:
            lines[rows[0]] = replacement
        elif replacement:
            additions.append(replacement)
        if old_link is not None and old_target not in selected_targets:
            retired_links.append(old_link)
    # Readable explanatory links cannot preserve a removed selection. Row replacements
    # are already final, so swaps never rewrite each other's new destination.
    for index, line in enumerate(original):
        if not line.startswith("|"):
            for pattern in retired_links:
                lines[index] = pattern.sub(
                    lambda match: match[0].split("]", 1)[0][1:], lines[index]
                )
    if additions:
        if "## Additional Routing Rules\n" not in section:
            lines.extend(
                [
                    "\n## Additional Routing Rules\n\n| Condition | Select |\n| --- | --- |\n"
                ]
            )
        else:
            while lines and not lines[-1].strip():
                lines.pop()
        lines.extend([*additions, "\n"])
    files[source] = (text[:start] + "".join(lines) + text[end:]).encode("utf-8")
