from __future__ import annotations

import re
import tomllib
from pathlib import PurePosixPath
from typing import Any, Iterable

from .errors import MetadataError, MetadataFailure
from .model import CanonicalModuleCorpus, MetadataValidation, ModuleMetadata
from .paths import normalized_repository_path
from .source import ContentSource, ContentSourceInput, content_source


CANONICAL_MODULE_CORPUS = (
    "evaluation/standards-effectiveness/canonical-module-corpus.toml"
)
FIELDS = (
    "ID",
    "Role",
    "Level",
    "Applies when",
    "Does not apply when",
    "Requires",
    "Specializes",
    "Verification",
    "Canonical owner",
)
SYMBOLIC_FIELDS = ("ID", "Role", "Level", "Canonical owner")
PROSE_FIELDS = ("Applies when", "Does not apply when", "Verification")
RELATION_FIELDS = ("Requires", "Specializes")
ROLES = frozenset({"core", "router", "workflow", "profile", "topic", "reference"})
LEVELS = frozenset({"MUST", "SHOULD", "PROFILE", "REFERENCE"})
ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)*$")
TOKEN_PATTERN = re.compile(r"^`([^`]+)`$")


def _failure(
    code: str,
    message: str,
    *,
    path: str,
    outcome: str = "invalid",
    row: int | None = None,
    field: str | None = None,
    expected: str | None = None,
    observed: str | None = None,
) -> MetadataFailure:
    return MetadataFailure(
        code,
        outcome,
        message,
        path=path,
        row=row,
        field=field,
        expected=expected,
        observed=observed,
    )


def _field_values(text: str) -> dict[str, list[tuple[int, str]]]:
    values = {field: [] for field in FIELDS}
    for row, line in enumerate(text.splitlines(), start=1):
        for field in FIELDS:
            marker = f"- {field}:"
            if line == marker:
                values[field].append((row, ""))
            elif line.startswith(f"{marker} "):
                values[field].append((row, line[len(marker) + 1 :]))
    return values


def _symbolic(
    path: str,
    field: str,
    row: int,
    value: str,
    failures: list[MetadataFailure],
) -> str | None:
    match = TOKEN_PATTERN.fullmatch(value)
    if match is None:
        failures.append(
            _failure(
                "METADATA.SYMBOLIC_FORMAT",
                "symbolic metadata value must be one backticked token",
                path=path,
                row=row,
                field=field,
                observed=value,
            )
        )
        return None
    return match.group(1)


def _relation(
    path: str,
    field: str,
    row: int,
    value: str,
    failures: list[MetadataFailure],
) -> tuple[str, ...] | None:
    if value == "`none`":
        return ()
    items: list[str] = []
    malformed = False
    for raw_item in value.split(","):
        item = raw_item.strip(" ")
        match = TOKEN_PATTERN.fullmatch(item)
        if (
            match is None
            or match.group(1) == "none"
            or ID_PATTERN.fullmatch(match.group(1)) is None
        ):
            malformed = True
        else:
            items.append(match.group(1))
    if malformed or not items:
        failures.append(
            _failure(
                "METADATA.RELATION_FORMAT",
                "relation must contain backticked module IDs or one none token",
                path=path,
                row=row,
                field=field,
                observed=value,
            )
        )
        return None
    if len(set(items)) != len(items):
        failures.append(
            _failure(
                "METADATA.RELATION_DUPLICATE",
                "relation targets must be unique",
                path=path,
                row=row,
                field=field,
                observed=value,
            )
        )
        return None
    return tuple(items)


def _parse_module(
    source: ContentSource,
    path: str,
) -> tuple[ModuleMetadata | None, list[MetadataFailure]]:
    try:
        raw = source.read_bytes(path)
    except MetadataError as error:
        return None, [error.failure]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        return None, [
            _failure(
                "INPUT.INVALID_UTF8",
                str(error),
                path=path,
            )
        ]

    failures: list[MetadataFailure] = []
    matches = _field_values(text)
    selected: dict[str, tuple[int, str]] = {}
    for field in FIELDS:
        occurrences = matches[field]
        if len(occurrences) != 1:
            failures.append(
                _failure(
                    "METADATA.FIELD_COUNT",
                    "metadata field must occur exactly once",
                    path=path,
                    field=field,
                    expected="1",
                    observed=str(len(occurrences)),
                )
            )
        else:
            selected[field] = occurrences[0]
    if failures:
        return None, failures

    symbols: dict[str, str] = {}
    for field in SYMBOLIC_FIELDS:
        row, value = selected[field]
        parsed = _symbolic(path, field, row, value, failures)
        if parsed is not None:
            symbols[field] = parsed

    prose: dict[str, str] = {}
    for field in PROSE_FIELDS:
        row, value = selected[field]
        if not value or not value.strip(" "):
            failures.append(
                _failure(
                    "METADATA.PROSE_EMPTY",
                    "prose metadata value must not be empty",
                    path=path,
                    row=row,
                    field=field,
                )
            )
        else:
            prose[field] = value

    relations: dict[str, tuple[str, ...]] = {}
    for field in RELATION_FIELDS:
        row, value = selected[field]
        parsed = _relation(path, field, row, value, failures)
        if parsed is not None:
            relations[field] = parsed
    if failures:
        return None, failures

    module_id = symbols["ID"]
    role = symbols["Role"]
    level = symbols["Level"]
    owner = symbols["Canonical owner"]
    requires = relations["Requires"]
    specializes = relations["Specializes"]

    if ID_PATTERN.fullmatch(module_id) is None:
        failures.append(
            _failure(
                "METADATA.ID_FORMAT",
                "module ID must be lowercase and dot-separated",
                path=path,
                field="ID",
                observed=module_id,
            )
        )
    if role not in ROLES:
        failures.append(
            _failure(
                "METADATA.ROLE",
                "metadata role is not supported",
                path=path,
                field="Role",
                observed=role,
            )
        )
    if level not in LEVELS:
        failures.append(
            _failure(
                "METADATA.LEVEL",
                "metadata level is not supported",
                path=path,
                field="Level",
                observed=level,
            )
        )
    expected_level = {
        "core": "MUST",
        "profile": "PROFILE",
        "reference": "REFERENCE",
    }.get(role)
    if expected_level is not None and level in LEVELS and level != expected_level:
        failures.append(
            _failure(
                "METADATA.ROLE_LEVEL",
                "metadata role requires its canonical level",
                path=path,
                field="Level",
                expected=expected_level,
                observed=level,
            )
        )

    owner_path = PurePosixPath(owner)
    if (
        not owner
        or owner_path.is_absolute()
        or ".." in owner_path.parts
        or owner.startswith("./")
        or str(owner_path) != owner
        or owner != path
    ):
        failures.append(
            _failure(
                "METADATA.CANONICAL_OWNER",
                "canonical owner must equal the normalized declaring path",
                path=path,
                field="Canonical owner",
                expected=path,
                observed=owner,
            )
        )
    if module_id in requires or module_id in specializes:
        failures.append(
            _failure(
                "METADATA.SELF_EDGE",
                "module cannot require or specialize itself",
                path=path,
                field="Requires,Specializes",
                observed=module_id,
            )
        )
    if role != "profile" and specializes:
        failures.append(
            _failure(
                "METADATA.SPECIALIZATION_ROLE",
                "only profiles may specialize modules",
                path=path,
                field="Specializes",
                observed=role,
            )
        )
    if prose["Applies when"] == "none" and prose["Does not apply when"] == "none":
        failures.append(
            _failure(
                "METADATA.APPLICABILITY",
                "applicability and exclusion cannot both be none",
                path=path,
                field="Applies when,Does not apply when",
            )
        )
    if failures:
        return None, failures
    return (
        ModuleMetadata(
            path=path,
            module_id=module_id,
            role=role,
            level=level,
            applies_when=prose["Applies when"],
            excludes=prose["Does not apply when"],
            requires=requires,
            specializes=specializes,
            verification=prose["Verification"],
            owner=owner,
        ),
        [],
    )


def _find_cycle(
    modules: tuple[ModuleMetadata, ...],
    relations: dict[str, tuple[str, ...]],
) -> tuple[str, ...] | None:
    color: dict[str, int] = {module.module_id: 0 for module in modules}
    for module in modules:
        root = module.module_id
        if color[root] != 0:
            continue
        path: list[str] = [root]
        color[root] = 1
        stack: list[tuple[str, int]] = [(root, 0)]
        while stack:
            node, index = stack[-1]
            targets = relations[node]
            if index == len(targets):
                color[node] = 2
                stack.pop()
                path.pop()
                continue
            target = targets[index]
            stack[-1] = (node, index + 1)
            if color[target] == 0:
                color[target] = 1
                path.append(target)
                stack.append((target, 0))
            elif color[target] == 1:
                start = path.index(target)
                return (*path[start:], target)
    return None


def _validate_graph(modules: tuple[ModuleMetadata, ...]) -> tuple[MetadataFailure, ...]:
    failures: list[MetadataFailure] = []
    by_id: dict[str, ModuleMetadata] = {}
    for module in modules:
        previous = by_id.get(module.module_id)
        if previous is not None:
            failures.append(
                _failure(
                    "METADATA.DUPLICATE_ID",
                    "module ID must be unique",
                    path=module.path,
                    field="ID",
                    expected=previous.path,
                    observed=module.module_id,
                )
            )
        else:
            by_id[module.module_id] = module
    if failures:
        return tuple(failures)

    for module in modules:
        for relation, targets in (
            ("Requires", module.requires),
            ("Specializes", module.specializes),
        ):
            for target in targets:
                if target not in by_id:
                    failures.append(
                        _failure(
                            "METADATA.UNRESOLVED_TARGET",
                            "relation target does not resolve to a selected module",
                            path=module.path,
                            field=relation,
                            observed=target,
                        )
                    )
    if failures:
        return tuple(failures)

    relations = (
        ("METADATA.REQUIRES_CYCLE", {m.module_id: m.requires for m in modules}),
        (
            "METADATA.SPECIALIZES_CYCLE",
            {m.module_id: m.specializes for m in modules},
        ),
        (
            "METADATA.COMBINED_CYCLE",
            {m.module_id: (*m.requires, *m.specializes) for m in modules},
        ),
    )
    for code, adjacency in relations:
        cycle = _find_cycle(modules, adjacency)
        if cycle is not None:
            failures.append(
                _failure(
                    code,
                    "metadata relation graph contains a cycle",
                    path=by_id[cycle[0]].path,
                    observed=" -> ".join(cycle),
                )
            )
    return tuple(failures)


def validate_module_metadata(
    source: ContentSourceInput,
    paths: Iterable[str],
) -> MetadataValidation:
    selected_source = content_source(source)
    modules: list[ModuleMetadata] = []
    failures: list[MetadataFailure] = []
    for path in paths:
        module, module_failures = _parse_module(selected_source, path)
        failures.extend(module_failures)
        if module is not None:
            modules.append(module)
    if failures:
        return MetadataValidation((), tuple(failures))
    selected = tuple(modules)
    graph_failures = _validate_graph(selected)
    return MetadataValidation(() if graph_failures else selected, graph_failures)


def load_module_metadata(source: ContentSourceInput, path: str) -> ModuleMetadata:
    module, failures = _parse_module(content_source(source), path)
    if failures:
        raise MetadataError(failures[0])
    assert module is not None
    return module


def _load_toml(source: ContentSource, display_path: str) -> dict[str, Any]:
    try:
        raw = tomllib.loads(source.read_bytes(display_path).decode("utf-8"))
    except UnicodeDecodeError as error:
        raise MetadataError(
            _failure("INPUT.INVALID_UTF8", str(error), path=display_path)
        ) from error
    except tomllib.TOMLDecodeError as error:
        raise MetadataError(
            _failure("CONFIG.INVALID_TOML", str(error), path=display_path)
        ) from error
    if not isinstance(raw, dict):
        raise MetadataError(
            _failure(
                "CONFIG.CANONICAL_CORPUS_ROOT",
                "canonical corpus root must be a table",
                path=display_path,
            )
        )
    return raw


def _members(raw: Any, manifest_path: str) -> tuple[str, ...]:
    if (
        not isinstance(raw, list)
        or not raw
        or any(not isinstance(member, str) or not member for member in raw)
    ):
        raise MetadataError(
            _failure(
                "CONFIG.CANONICAL_CORPUS_MEMBERS",
                "members must contain non-empty repository-relative paths",
                path=manifest_path,
                field="members",
            )
        )
    if len(set(raw)) != len(raw):
        raise MetadataError(
            _failure(
                "CONFIG.CANONICAL_CORPUS_DUPLICATE",
                "canonical corpus members must be unique",
                path=manifest_path,
                field="members",
            )
        )
    members = tuple(raw)
    for member in members:
        try:
            normalized_repository_path(member)
        except MetadataError as error:
            raise MetadataError(
                _failure(
                    error.failure.code,
                    "canonical corpus member must be a normalized repository-relative path",
                    path=member,
                )
            ) from error
    return members


def load_canonical_module_corpus(
    source: ContentSourceInput,
    manifest_path: str = CANONICAL_MODULE_CORPUS,
) -> CanonicalModuleCorpus:
    selected_source = content_source(source)
    raw = _load_toml(selected_source, manifest_path)
    required = {"schema_version", "members"}
    if set(raw) != required:
        unexpected = sorted(set(raw) - required)
        missing = sorted(required - set(raw))
        raise MetadataError(
            _failure(
                "CONFIG.CANONICAL_CORPUS_FIELDS",
                "canonical corpus requires exactly schema_version and members",
                path=manifest_path,
                field=(unexpected or missing)[0],
            )
        )
    if raw["schema_version"] != 1:
        raise MetadataError(
            _failure(
                "CONFIG.SCHEMA_VERSION",
                "canonical corpus schema version must be 1",
                path=manifest_path,
                expected="1",
                observed=str(raw["schema_version"]),
            )
        )
    members = _members(raw["members"], manifest_path)
    validation = validate_module_metadata(selected_source, members)
    if validation.failures:
        raise MetadataError(validation.failures[0])
    return CanonicalModuleCorpus(manifest_path, members, validation.modules)
