"""Captured decision records and exact application-exposure declarations.

This owner validates structure and bindings. Editorial review decides which
content belongs in an application context.
"""
from __future__ import annotations

import hashlib
import json
import re
import tomllib
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .errors import MetadataError, MetadataFailure
from .source import ContentSource

APPLICATION_CONTENT = "evaluation/standards-effectiveness/application-content.toml"
DECISION_PROVENANCE = "evaluation/standards-effectiveness/decision-provenance.toml"
_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
ORIGINS = frozenset({"documented-original", "reconstructed-history", "current-justification", "unrecorded"})


def _invalid(message: str) -> MetadataError:
    return MetadataError(MetadataFailure("SUPPORT.INVALID_CONTENT", "invalid", message))


def content_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(b"standards-support-v1\x00" + encoded).hexdigest()


def _text(value: object, label: str, *, empty: bool = False) -> str:
    if (type(value) is not str or (not empty and not value.strip())
            or any(0xD800 <= ord(char) <= 0xDFFF for char in value)):
        raise _invalid(f"{label} requires Unicode text.")
    return value


def _identity(value: object, label: str) -> str:
    selected = _text(value, label)
    if _ID.fullmatch(selected) is None:
        raise _invalid(f"{label} requires a canonical identity.")
    return selected


def _digest(value: object) -> str:
    selected = _text(value, "Content binding")
    if _DIGEST.fullmatch(selected) is None:
        raise _invalid("Content binding requires a SHA-256 identity.")
    return selected


def _strings(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise _invalid(f"{label} requires an array.")
    return tuple(_text(item, label) for item in value)


def _evidence(value: object) -> tuple[Mapping[str, str], ...]:
    if not isinstance(value, list):
        raise _invalid("Evidence requires an array.")
    result, seen = [], set()
    for item in value:
        if not isinstance(item, dict) or set(item) != {"id", "digest", "provider_contract", "provider_contract_version"}:
            raise _invalid("Evidence requires the canonical four-field reference.")
        row = {"id": _identity(item["id"], "Evidence identity"),
               "digest": _digest(item["digest"]),
               "provider_contract": _identity(item["provider_contract"], "Evidence provider"),
               "provider_contract_version": _text(item["provider_contract_version"], "Provider version")}
        key = tuple(sorted(row.items()))
        if key in seen:
            raise _invalid("Evidence references must be unique.")
        seen.add(key)
        result.append(MappingProxyType(row))
    return tuple(result)


@dataclass(frozen=True, slots=True)
class DecisionProvenance:
    id: str
    subject: str
    subject_binding: str
    origin: str
    rationale: str
    evidence: tuple[Mapping[str, str], ...]
    assumptions: tuple[str, ...] = ()
    limits: tuple[str, ...] = ()
    alternatives: tuple[str, ...] = ()
    reconsideration: tuple[str, ...] = ()
    supersedes: tuple[str, ...] = ()
    retired: bool = False

    @classmethod
    def from_mapping(cls, value: object) -> DecisionProvenance:
        required = {"id", "subject", "subject_binding", "origin", "rationale", "evidence"}
        lists = {"assumptions", "limits", "alternatives", "reconsideration", "supersedes"}
        if not isinstance(value, dict) or not required <= value.keys() or set(value) - required - lists - {"retired"}:
            raise _invalid("Decision provenance has missing or unknown fields.")
        identity = _identity(value["id"], "Provenance identity")
        if not identity.startswith("provenance."):
            raise _invalid("Decision provenance uses the provenance namespace.")
        origin = _text(value["origin"], "Origin")
        if origin not in ORIGINS:
            raise _invalid("Decision provenance origin is unsupported.")
        evidence = _evidence(value["evidence"])
        rationale = _text(value["rationale"], "Rationale", empty=origin == "unrecorded")
        if origin in {"documented-original", "reconstructed-history"} and not evidence:
            raise _invalid("Historical origin claims require evidence references.")
        values = {key: _strings(value.get(key, []), key) for key in lists}
        if len(set(values["supersedes"])) != len(values["supersedes"]) or identity in values["supersedes"]:
            raise _invalid("Provenance supersession identifies distinct predecessors.")
        for predecessor in values["supersedes"]:
            _identity(predecessor, "Predecessor")
        retired = value.get("retired", False)
        if type(retired) is not bool:
            raise _invalid("Provenance retirement must be boolean.")
        return cls(identity, _identity(value["subject"], "Subject"),
                   _digest(value["subject_binding"]), origin, rationale, evidence,
                   retired=retired, **values)

    def as_contract(self) -> dict[str, object]:
        return {"id": self.id, "subject": self.subject,
                "subject_binding": self.subject_binding, "origin": self.origin,
                "rationale": self.rationale, "evidence": [dict(item) for item in self.evidence],
                "retired": self.retired,
                **{field: list(getattr(self, field)) for field in
                   ("assumptions", "limits", "alternatives", "reconsideration", "supersedes")}}


@dataclass(frozen=True, slots=True)
class ApplicationExposure:
    target: str
    binding: str

    @classmethod
    def from_mapping(cls, value: object) -> ApplicationExposure:
        if not isinstance(value, dict) or set(value) != {"target", "binding"}:
            raise _invalid("Application exposure requires a target and reviewed binding.")
        return cls(_identity(value["target"], "Exposure target"), _digest(value["binding"]))

    def as_contract(self) -> dict[str, str]:
        return {"target": self.target, "binding": self.binding}


@dataclass(frozen=True, slots=True)
class SupportingContent:
    provenance: Mapping[str, DecisionProvenance]
    exposure: Mapping[str, ApplicationExposure]

    def __post_init__(self) -> None:
        object.__setattr__(self, "provenance", MappingProxyType(dict(sorted(self.provenance.items()))))
        object.__setattr__(self, "exposure", MappingProxyType(dict(sorted(self.exposure.items()))))

    def exposure_state(self, target: str, binding: str) -> str:
        reviewed = self.exposure.get(target)
        return "unreviewed" if reviewed is None else "current" if reviewed.binding == binding else "needs-review"


def _manifest(source: ContentSource, path: str, member: str) -> list[object]:
    try:
        raw = tomllib.loads(source.read_bytes(path).decode("utf-8"))
    except MetadataError as error:
        if error.failure.code != "INPUT.UNAVAILABLE":
            raise
        raise MetadataError(MetadataFailure(
            "SUPPORT.UNSUPPORTED_CAPTURE", "unsupported",
            "The captured content predates the supported content contract.")) from error
    except (ValueError, UnicodeError) as error:
        raise _invalid("Supporting content must be valid UTF-8 TOML.") from error
    if not isinstance(raw, dict) or set(raw) != {"schema_version", member}:
        raise _invalid("Supporting manifest has missing or unknown fields.")
    if type(raw["schema_version"]) is not int or raw["schema_version"] != 1:
        raise MetadataError(MetadataFailure("SUPPORT.UNSUPPORTED_VERSION", "unsupported", "Unsupported supporting-content schema."))
    if not isinstance(raw[member], list):
        raise _invalid("Supporting manifest entries require an array.")
    return raw[member]


def load_supporting_content(source: ContentSource) -> SupportingContent:
    records = [DecisionProvenance.from_mapping(item) for item in _manifest(source, DECISION_PROVENANCE, "records")]
    entries = [ApplicationExposure.from_mapping(item) for item in _manifest(source, APPLICATION_CONTENT, "entries")]
    if len({item.id for item in records}) != len(records) or len({item.target for item in entries}) != len(entries):
        raise _invalid("Supporting content identities must be unique.")
    index = {item.id: item for item in records}
    for record in records:
        if any(target not in index for target in record.supersedes):
            raise _invalid("Provenance supersession requires retained predecessors.")
    visiting, visited = set(), set()
    def visit(identity: str) -> None:
        if identity in visiting:
            raise _invalid("Provenance supersession requires an acyclic history.")
        if identity in visited:
            return
        visiting.add(identity)
        for predecessor in index[identity].supersedes:
            visit(predecessor)
        visiting.remove(identity)
        visited.add(identity)
    for identity in index:
        visit(identity)
    return SupportingContent(index, {item.target: item for item in entries})
