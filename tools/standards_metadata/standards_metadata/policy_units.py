from __future__ import annotations

import hashlib
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .errors import MetadataError, MetadataFailure
from .model import CanonicalModuleCorpus, CanonicalStandardsCorpus
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    encode_identity_value,
)


POLICY_UNIT_REGISTRY = "evaluation/standards-effectiveness/policy-units/registry.toml"
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
HEADING_PATTERN = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")


def _digest_bytes(value: bytes) -> str:
    return f"sha256:{hashlib.sha256(value).hexdigest()}"


@dataclass(frozen=True, slots=True)
class PolicyUnit:
    id: str
    module: str
    heading_path: tuple[str, ...]
    semantic_revision: int
    aliases: tuple[str, ...]
    predecessors: tuple[str, ...]
    successors: tuple[str, ...]
    document: str
    content: str
    representation_digest: str
    structural_digest: str
    source: str

    def as_declaration(self) -> dict[str, object]:
        value: dict[str, object] = {
            "kind": "policy-unit",
            "id": self.id,
            "module": self.module,
            "heading_path": list(self.heading_path),
            "semantic_revision": self.semantic_revision,
            "lifecycle": "active",
        }
        if self.aliases:
            value["aliases"] = list(self.aliases)
        if self.predecessors:
            value["predecessors"] = list(self.predecessors)
        if self.successors:
            value["successors"] = list(self.successors)
        return value


@dataclass(frozen=True, slots=True)
class PolicyUnitTombstone:
    id: str
    retired_semantic_revision: int
    successors: tuple[str, ...]
    evidence: str
    source: str

    def as_declaration(self) -> dict[str, object]:
        return {
            "kind": "policy-unit-tombstone",
            "id": self.id,
            "retired_semantic_revision": self.retired_semantic_revision,
            "successors": list(self.successors),
            "evidence": self.evidence,
        }


@dataclass(frozen=True, slots=True)
class PolicyUnitCorpus:
    registry: str
    sources: tuple[str, ...]
    units: tuple[PolicyUnit, ...]
    tombstones: tuple[PolicyUnitTombstone, ...]

    def resolve(self, value: str) -> PolicyUnit | PolicyUnitTombstone | None:
        for unit in self.units:
            if value == unit.id or value in unit.aliases:
                return unit
        for tombstone in self.tombstones:
            if value == tombstone.id:
                return tombstone
        return None

    def active_by_id(self, value: str) -> PolicyUnit | None:
        return next((unit for unit in self.units if unit.id == value), None)

    def for_module(self, module_id: str) -> tuple[PolicyUnit, ...]:
        return tuple(unit for unit in self.units if unit.module == module_id)


@dataclass(frozen=True, slots=True)
class UnmappedModuleProjection:
    module: str
    document: str
    mapped_policy_units: tuple[str, ...]
    whole_representation_digest: str
    digest: str


def _error(
    code: str,
    message: str,
    *,
    path: str,
    field: str | None = None,
    observed: str | None = None,
) -> MetadataError:
    return MetadataError(
        MetadataFailure(
            code,
            "invalid",
            message,
            path=path,
            field=field,
            observed=observed,
        )
    )


def _path(root: Path, value: str) -> Path:
    logical = PurePosixPath(value)
    resolved_root = root.resolve()
    candidate = (resolved_root / Path(*logical.parts)).resolve(strict=False)
    if (
        not value
        or logical.is_absolute()
        or ".." in logical.parts
        or value.startswith("./")
        or str(logical) != value
        or not candidate.is_relative_to(resolved_root)
    ):
        raise _error(
            "POLICY_UNIT.PATH",
            "policy-unit source must be a contained normalized repository path",
            path=value,
        )
    if not candidate.is_file():
        raise MetadataError(
            MetadataFailure(
                "POLICY_UNIT.INPUT_UNAVAILABLE",
                "unavailable",
                "policy-unit source is unavailable",
                path=value,
            )
        )
    return candidate


def _toml(root: Path, path: str) -> dict[str, Any]:
    source = _path(root, path)
    try:
        with source.open("rb") as handle:
            return tomllib.load(handle)
    except tomllib.TOMLDecodeError as error:
        raise _error("POLICY_UNIT.INVALID_TOML", str(error), path=path) from error


def _strings(
    value: Any,
    *,
    path: str,
    field: str,
    non_empty: bool = False,
) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or (non_empty and not value)
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise _error(
            "POLICY_UNIT.STRING_LIST",
            "field must contain unique non-empty strings",
            path=path,
            field=field,
        )
    return tuple(value)


def _id(value: Any, *, path: str, field: str) -> str:
    if not isinstance(value, str) or ID_PATTERN.fullmatch(value) is None:
        raise _error(
            "POLICY_UNIT.ID",
            "policy-unit identities must use the canonical ID grammar",
            path=path,
            field=field,
            observed=str(value),
        )
    if value.startswith("STD-"):
        raise _error(
            "POLICY_UNIT.LEGACY_ID",
            "legacy migration IDs are not policy-unit identities",
            path=path,
            field=field,
            observed=value,
        )
    return value


def _headings(text: str) -> list[tuple[tuple[str, ...], int, int]]:
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line.encode("utf-8")))
    stack: list[str] = []
    found: list[tuple[tuple[str, ...], int, int]] = []
    fenced = False
    pending: list[tuple[tuple[str, ...], int, int]] = []
    for index, line in enumerate(lines):
        stripped = line.rstrip("\r\n")
        if stripped.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        if fenced:
            continue
        match = HEADING_PATTERN.fullmatch(stripped)
        if match is None:
            continue
        level = len(match.group(1))
        title = match.group(2).strip()
        if level == 1:
            stack = []
            heading_path = (title,)
        else:
            stack = stack[: level - 2]
            stack.append(title)
            heading_path = tuple(stack)
        pending.append((heading_path, offsets[index], level))
    for position, (heading_path, start, level) in enumerate(pending):
        end = offsets[-1]
        for _next_path, next_start, next_level in pending[position + 1 :]:
            if next_level <= level:
                end = next_start
                break
        found.append((heading_path, start, end))
    return found


def markdown_structural_digest(section: bytes) -> str:
    text = section.decode("utf-8")
    blocks: list[str] = []
    paragraph: list[str] = []
    fenced = False

    def flush() -> None:
        if paragraph:
            blocks.append(" ".join(item.strip() for item in paragraph))
            paragraph.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            flush()
            fenced = not fenced
            blocks.append(stripped)
        elif fenced:
            blocks.append(line.rstrip())
        elif not stripped:
            flush()
        elif HEADING_PATTERN.fullmatch(line) or stripped.startswith(("- ", "* ", "+ ", "> ", "|")):
            flush()
            blocks.append(stripped)
        else:
            paragraph.append(stripped)
    flush()
    structure = encode_identity_value(
        IdentityObject(
            (
                ("parser", "markdown-heading-v2"),
                ("blocks", IdentityArray(blocks)),
            )
        )
    )
    return _digest_bytes(structure)


def _resolve_scope(
    root: Path,
    document: str,
    heading_path: tuple[str, ...],
) -> tuple[str, str, str]:
    source = _path(root, document)
    raw = source.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise _error("POLICY_UNIT.INVALID_UTF8", str(error), path=document) from error
    matches = [item for item in _headings(text) if item[0] == heading_path]
    if len(matches) != 1:
        raise _error(
            "POLICY_UNIT.LOCATOR_COUNT",
            "policy-unit heading path must resolve exactly once",
            path=document,
            field="heading_path",
            observed=str(len(matches)),
        )
    _, start, end = matches[0]
    section = raw[start:end]
    return (
        _digest_bytes(section),
        markdown_structural_digest(section),
        section.decode("utf-8"),
    )


def _unit(
    root: Path,
    corpus: CanonicalModuleCorpus,
    source: str,
    raw: Any,
) -> PolicyUnit:
    if not isinstance(raw, dict):
        raise _error("POLICY_UNIT.DECLARATION", "policy unit must be a table", path=source)
    required = {"id", "module", "heading_path", "semantic_revision"}
    optional = {"aliases", "predecessors", "successors"}
    if not required <= set(raw) or set(raw) - required - optional:
        raise _error(
            "POLICY_UNIT.FIELDS",
            "policy unit has missing or unknown fields",
            path=source,
        )
    unit_id = _id(raw["id"], path=source, field="id")
    module_id = _id(raw["module"], path=source, field="module")
    module = corpus.resolve(module_id)
    if module is None or module.module_id != module_id:
        raise _error(
            "POLICY_UNIT.UNKNOWN_MODULE",
            "policy unit module must resolve by canonical module ID",
            path=source,
            field="module",
            observed=module_id,
        )
    headings = _strings(raw["heading_path"], path=source, field="heading_path", non_empty=True)
    revision = raw["semantic_revision"]
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
        raise _error(
            "POLICY_UNIT.SEMANTIC_REVISION",
            "semantic revision must be a positive integer",
            path=source,
            field="semantic_revision",
        )
    aliases = _strings(raw.get("aliases", []), path=source, field="aliases")
    predecessors = _strings(raw.get("predecessors", []), path=source, field="predecessors")
    successors = _strings(raw.get("successors", []), path=source, field="successors")
    for field, values in (("aliases", aliases), ("predecessors", predecessors), ("successors", successors)):
        for value in values:
            _id(value, path=source, field=field)
    if unit_id in (*aliases, *predecessors, *successors):
        raise _error(
            "POLICY_UNIT.SELF_REFERENCE",
            "policy unit cannot alias, precede, or succeed itself",
            path=source,
            observed=unit_id,
        )
    representation, structural, content = _resolve_scope(root, module.path, headings)
    return PolicyUnit(
        unit_id,
        module_id,
        headings,
        revision,
        aliases,
        predecessors,
        successors,
        module.path,
        content,
        representation,
        structural,
        source,
    )


def _tombstone(source: str, raw: Any) -> PolicyUnitTombstone:
    required = {"id", "retired_semantic_revision", "successors", "evidence"}
    if not isinstance(raw, dict) or set(raw) != required:
        raise _error(
            "POLICY_UNIT.TOMBSTONE_FIELDS",
            "tombstone requires exactly id, retired_semantic_revision, successors, and evidence",
            path=source,
        )
    tombstone_id = _id(raw["id"], path=source, field="id")
    revision = raw["retired_semantic_revision"]
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
        raise _error(
            "POLICY_UNIT.SEMANTIC_REVISION",
            "retired semantic revision must be a positive integer",
            path=source,
            field="retired_semantic_revision",
        )
    successors = _strings(raw["successors"], path=source, field="successors")
    for successor in successors:
        _id(successor, path=source, field="successors")
    if tombstone_id in successors:
        raise _error(
            "POLICY_UNIT.SELF_REFERENCE",
            "policy-unit tombstone cannot succeed itself",
            path=source,
            observed=tombstone_id,
        )
    evidence = _id(raw["evidence"], path=source, field="evidence")
    return PolicyUnitTombstone(tombstone_id, revision, successors, evidence, source)


def _validate_lifecycle(
    units: tuple[PolicyUnit, ...],
    tombstones: tuple[PolicyUnitTombstone, ...],
) -> None:
    active = {unit.id: unit for unit in units}
    retired = {item.id: item for item in tombstones}
    identities = [unit.id for unit in units] + [item.id for item in tombstones]
    aliases = [alias for unit in units for alias in unit.aliases]
    locators = [(unit.module, unit.heading_path) for unit in units]
    if len(set(identities)) != len(identities) or set(identities) & set(aliases) or len(set(aliases)) != len(aliases):
        raise _error(
            "POLICY_UNIT.IDENTITY_CONFLICT",
            "policy-unit IDs, tombstones, and aliases must be globally unambiguous",
            path=POLICY_UNIT_REGISTRY,
        )
    if len(set(locators)) != len(locators):
        raise _error(
            "POLICY_UNIT.LOCATOR_CONFLICT",
            "one active policy-unit locator cannot own multiple identities",
            path=POLICY_UNIT_REGISTRY,
        )
    ordered_locators = sorted(locators)
    for index, (module, heading_path) in enumerate(ordered_locators):
        for other_module, other_path in ordered_locators[index + 1 :]:
            if other_module != module:
                continue
            shorter = min(len(heading_path), len(other_path))
            if heading_path[:shorter] == other_path[:shorter]:
                raise _error(
                    "POLICY_UNIT.LOCATOR_OVERLAP",
                    "active policy-unit heading scopes must not overlap",
                    path=POLICY_UNIT_REGISTRY,
                    observed=f"{module}:{'/'.join(heading_path)}",
                )
    for item in tombstones:
        for successor in item.successors:
            target = active.get(successor)
            if target is None or item.id not in target.predecessors:
                raise _error(
                    "POLICY_UNIT.SUCCESSOR_MISMATCH",
                    "tombstone successors and active predecessors must be reciprocal",
                    path=item.source,
                    observed=successor,
                )
    for unit in units:
        for predecessor in unit.predecessors:
            item = retired.get(predecessor)
            if item is None or unit.id not in item.successors:
                raise _error(
                    "POLICY_UNIT.PREDECESSOR_MISMATCH",
                    "active predecessors and tombstone successors must be reciprocal",
                    path=unit.source,
                    observed=predecessor,
                )


def load_policy_unit_corpus(
    root: Path,
    modules: CanonicalModuleCorpus,
    registry_path: str = POLICY_UNIT_REGISTRY,
) -> PolicyUnitCorpus:
    registry = _toml(root, registry_path)
    if set(registry) != {"schema_version", "sources"} or registry["schema_version"] != 1:
        raise _error(
            "POLICY_UNIT.REGISTRY",
            "policy-unit registry requires schema_version 1 and sources",
            path=registry_path,
        )
    sources = _strings(registry["sources"], path=registry_path, field="sources", non_empty=True)
    units: list[PolicyUnit] = []
    tombstones: list[PolicyUnitTombstone] = []
    for source in sources:
        content = _toml(root, source)
        allowed = {"schema_version", "policy_unit", "tombstone"}
        if set(content) - allowed or content.get("schema_version") != 1:
            raise _error(
                "POLICY_UNIT.SIDECAR",
                "policy-unit sidecar requires schema_version 1 and known declaration arrays",
                path=source,
            )
        for raw in content.get("policy_unit", []):
            units.append(_unit(root, modules, source, raw))
        for raw in content.get("tombstone", []):
            tombstones.append(_tombstone(source, raw))
    selected_units = tuple(units)
    selected_tombstones = tuple(tombstones)
    _validate_lifecycle(selected_units, selected_tombstones)
    return PolicyUnitCorpus(registry_path, sources, selected_units, selected_tombstones)


def project_unmapped_module(
    root: Path,
    corpus: CanonicalStandardsCorpus,
    module_id: str,
) -> UnmappedModuleProjection:
    module = corpus.resolve_module(module_id)
    if module is None or module.module_id != module_id:
        raise _error(
            "POLICY_UNIT.UNKNOWN_MODULE",
            "unmapped projection requires one canonical module ID",
            path=module_id,
            observed=module_id,
        )
    source = _path(root.resolve(), module.path)
    raw = source.read_bytes()
    try:
        headings = _headings(raw.decode("utf-8"))
    except UnicodeDecodeError as error:
        raise _error("POLICY_UNIT.INVALID_UTF8", str(error), path=module.path) from error

    ranges: list[tuple[int, int, str]] = []
    for unit in corpus.policy_unit_corpus.for_module(module_id):
        matches = [item for item in headings if item[0] == unit.heading_path]
        if len(matches) != 1:
            raise _error(
                "POLICY_UNIT.LOCATOR_COUNT",
                "policy-unit heading path must resolve exactly once",
                path=module.path,
                field="heading_path",
                observed=str(len(matches)),
            )
        _, start, end = matches[0]
        ranges.append((start, end, unit.id))

    ranges.sort()
    for previous, current in zip(ranges, ranges[1:]):
        if current[0] < previous[1]:
            raise _error(
                "POLICY_UNIT.LOCATOR_OVERLAP",
                "active policy-unit heading scopes must not overlap",
                path=module.path,
                observed=f"{previous[2]}|{current[2]}",
            )

    unmapped = bytearray()
    position = 0
    for start, end, _unit_id in ranges:
        unmapped.extend(raw[position:start])
        position = end
    unmapped.extend(raw[position:])
    return UnmappedModuleProjection(
        module_id,
        module.path,
        tuple(unit_id for _start, _end, unit_id in ranges),
        _digest_bytes(raw),
        _digest_bytes(bytes(unmapped)),
    )
