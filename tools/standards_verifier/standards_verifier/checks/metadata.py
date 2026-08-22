from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..graph_adapters import (
    METADATA_DEPENDENCIES,
    METADATA_REQUIRES,
    METADATA_SPECIALIZES,
    metadata_dependency_registry,
)
from ..model import CheckContext, SuiteCatalog
from ..paths import contained_file


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


@dataclass(frozen=True, slots=True)
class ModuleMetadata:
    path: str
    module_id: str
    role: str
    level: str
    applies_when: str
    excludes: str
    requires: tuple[str, ...]
    specializes: tuple[str, ...]
    verification: str
    owner: str


@dataclass(frozen=True, slots=True)
class MetadataCase:
    id: str
    paths: tuple[str, ...]
    expected: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MetadataGraphCheck:
    id: str
    paths: tuple[str, ...] | None
    cases: tuple[MetadataCase, ...] | None

    def run(self, context: CheckContext) -> list[Diagnostic]:
        if self.paths is not None:
            return _validate_graph(context, self.id, self.paths)

        diagnostics: list[Diagnostic] = []
        assert self.cases is not None
        for case in self.cases:
            observed = tuple(
                item.code for item in _validate_graph(context, self.id, case.paths)
            )
            if observed != case.expected:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.METADATA_FIXTURE",
                        "invalid",
                        "metadata fixture diagnostics do not match",
                        suite=context.suite_id,
                        check=self.id,
                        field=case.id,
                        expected=",".join(case.expected) or "pass",
                        observed=",".join(observed) or "pass",
                    )
                )
        return diagnostics


def load_module_metadata(
    root: Path,
    path: str,
    *,
    suite: str,
    check: str,
) -> ModuleMetadata:
    context = CheckContext(root, suite, SuiteCatalog.empty())
    module, diagnostics = _parse_module(context, check, path)
    if diagnostics:
        raise EngineError(diagnostics[0])
    assert module is not None
    return module


def load_module_metadata_graph(
    root: Path,
    paths: tuple[str, ...],
    *,
    suite: str,
    check: str,
) -> tuple[ModuleMetadata, ...]:
    context = CheckContext(root, suite, SuiteCatalog.empty())
    modules, diagnostics = _validated_modules(context, check, paths)
    if diagnostics:
        raise EngineError(diagnostics[0])
    return modules


def _diagnostic(
    context: CheckContext,
    check: str,
    code: str,
    message: str,
    *,
    path: str,
    row: int | None = None,
    field: str | None = None,
    expected: str | None = None,
    observed: str | None = None,
) -> Diagnostic:
    return Diagnostic(
        code,
        "invalid",
        message,
        suite=context.suite_id,
        check=check,
        path=path,
        row=row,
        field=field,
        expected=expected,
        observed=observed,
    )


def _field_values(
    text: str,
) -> dict[str, list[tuple[int, str]]]:
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
    context: CheckContext,
    check: str,
    path: str,
    field: str,
    row: int,
    value: str,
    diagnostics: list[Diagnostic],
) -> str | None:
    match = TOKEN_PATTERN.fullmatch(value)
    if match is None:
        diagnostics.append(
            _diagnostic(
                context,
                check,
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
    context: CheckContext,
    check: str,
    path: str,
    field: str,
    row: int,
    value: str,
    diagnostics: list[Diagnostic],
) -> tuple[str, ...] | None:
    if value == "`none`":
        return ()
    raw_items = value.split(",")
    items: list[str] = []
    malformed = False
    for raw_item in raw_items:
        item = raw_item.strip(" ")
        match = TOKEN_PATTERN.fullmatch(item)
        if (
            match is None
            or match.group(1) == "none"
            or ID_PATTERN.fullmatch(match.group(1)) is None
        ):
            malformed = True
            continue
        items.append(match.group(1))
    if malformed or not items:
        diagnostics.append(
            _diagnostic(
                context,
                check,
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
        diagnostics.append(
            _diagnostic(
                context,
                check,
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
    context: CheckContext,
    check: str,
    path: str,
) -> tuple[ModuleMetadata | None, list[Diagnostic]]:
    source = contained_file(
        context.repo_root,
        path,
        suite=context.suite_id,
        check=check,
    )
    try:
        text = source.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise EngineError(
            Diagnostic(
                "INPUT.INVALID_UTF8",
                "invalid",
                str(error),
                suite=context.suite_id,
                check=check,
                path=path,
            )
        ) from error

    diagnostics: list[Diagnostic] = []
    matches = _field_values(text)
    selected: dict[str, tuple[int, str]] = {}
    for field in FIELDS:
        occurrences = matches[field]
        if len(occurrences) != 1:
            diagnostics.append(
                _diagnostic(
                    context,
                    check,
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
    if diagnostics:
        return None, diagnostics

    symbols: dict[str, str] = {}
    for field in SYMBOLIC_FIELDS:
        row, value = selected[field]
        parsed = _symbolic(
            context, check, path, field, row, value, diagnostics
        )
        if parsed is not None:
            symbols[field] = parsed

    prose: dict[str, str] = {}
    for field in PROSE_FIELDS:
        row, value = selected[field]
        if not value or not value.strip(" "):
            diagnostics.append(
                _diagnostic(
                    context,
                    check,
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
        parsed = _relation(
            context, check, path, field, row, value, diagnostics
        )
        if parsed is not None:
            relations[field] = parsed

    if diagnostics:
        return None, diagnostics

    module_id = symbols["ID"]
    role = symbols["Role"]
    level = symbols["Level"]
    owner = symbols["Canonical owner"]
    requires = relations["Requires"]
    specializes = relations["Specializes"]

    if ID_PATTERN.fullmatch(module_id) is None:
        diagnostics.append(
            _diagnostic(
                context,
                check,
                "METADATA.ID_FORMAT",
                "module ID must be lowercase and dot-separated",
                path=path,
                field="ID",
                observed=module_id,
            )
        )
    if role not in ROLES:
        diagnostics.append(
            _diagnostic(
                context,
                check,
                "METADATA.ROLE",
                "metadata role is not supported",
                path=path,
                field="Role",
                observed=role,
            )
        )
    if level not in LEVELS:
        diagnostics.append(
            _diagnostic(
                context,
                check,
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
        diagnostics.append(
            _diagnostic(
                context,
                check,
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
        diagnostics.append(
            _diagnostic(
                context,
                check,
                "METADATA.CANONICAL_OWNER",
                "canonical owner must equal the normalized declaring path",
                path=path,
                field="Canonical owner",
                expected=path,
                observed=owner,
            )
        )
    if module_id in requires or module_id in specializes:
        diagnostics.append(
            _diagnostic(
                context,
                check,
                "METADATA.SELF_EDGE",
                "module cannot require or specialize itself",
                path=path,
                field="Requires,Specializes",
                observed=module_id,
            )
        )
    if role != "profile" and specializes:
        diagnostics.append(
            _diagnostic(
                context,
                check,
                "METADATA.SPECIALIZATION_ROLE",
                "only profiles may specialize modules",
                path=path,
                field="Specializes",
                observed=role,
            )
        )
    if prose["Applies when"] == "none" and prose["Does not apply when"] == "none":
        diagnostics.append(
            _diagnostic(
                context,
                check,
                "METADATA.APPLICABILITY",
                "applicability and exclusion cannot both be none",
                path=path,
                field="Applies when,Does not apply when",
            )
        )
    if diagnostics:
        return None, diagnostics

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


def _validate_graph(
    context: CheckContext,
    check: str,
    paths: tuple[str, ...],
) -> list[Diagnostic]:
    _, diagnostics = _validated_modules(context, check, paths)
    return diagnostics


def _validated_modules(
    context: CheckContext,
    check: str,
    paths: tuple[str, ...],
) -> tuple[tuple[ModuleMetadata, ...], list[Diagnostic]]:
    parsed: list[ModuleMetadata] = []
    diagnostics: list[Diagnostic] = []
    for path in paths:
        module, module_diagnostics = _parse_module(context, check, path)
        diagnostics.extend(module_diagnostics)
        if module is not None:
            parsed.append(module)
    if diagnostics:
        return (), diagnostics

    modules: dict[str, ModuleMetadata] = {}
    for module in parsed:
        previous = modules.get(module.module_id)
        if previous is not None:
            diagnostics.append(
                _diagnostic(
                    context,
                    check,
                    "METADATA.DUPLICATE_ID",
                    "module ID must be unique",
                    path=module.path,
                    field="ID",
                    expected=previous.path,
                    observed=module.module_id,
                )
            )
        else:
            modules[module.module_id] = module
    if diagnostics:
        return (), diagnostics

    for module in parsed:
        for relation, targets in (
            ("Requires", module.requires),
            ("Specializes", module.specializes),
        ):
            for target in targets:
                if target not in modules:
                    diagnostics.append(
                        _diagnostic(
                            context,
                            check,
                            "METADATA.UNRESOLVED_TARGET",
                            "relation target does not resolve to a selected module",
                            path=module.path,
                            field=relation,
                            observed=target,
                        )
                    )
    if diagnostics:
        return (), diagnostics

    graph = metadata_dependency_registry(context.repo_root, parsed)
    graphs = (
        ("METADATA.REQUIRES_CYCLE", METADATA_REQUIRES),
        ("METADATA.SPECIALIZES_CYCLE", METADATA_SPECIALIZES),
        ("METADATA.COMBINED_CYCLE", METADATA_DEPENDENCIES),
    )
    for code, group_id in graphs:
        cycle = graph.find_cycle(group_id)
        if cycle is not None:
            diagnostics.append(
                _diagnostic(
                    context,
                    check,
                    code,
                    "metadata relation graph contains a cycle",
                    path=modules[cycle[0]].path,
                    observed=" -> ".join(cycle),
                )
            )
    return tuple(parsed), diagnostics


def _strings(
    value: Any,
    *,
    suite: str,
    check: str,
    field: str,
) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.STRING_LIST",
                "invalid",
                "field must contain unique non-empty strings",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return tuple(value)


def parse_metadata_graph_check(
    raw: dict[str, Any],
    suite_id: str,
) -> MetadataGraphCheck:
    allowed = {"id", "type", "paths", "cases"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "metadata graph check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    if not isinstance(check_id, str) or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    has_paths = "paths" in raw
    has_cases = "cases" in raw
    if has_paths == has_cases:
        raise EngineError(
            Diagnostic(
                "CONFIG.METADATA_MODE",
                "invalid",
                "metadata graph requires exactly one of paths or cases",
                suite=suite_id,
                check=check_id,
            )
        )
    if has_paths:
        return MetadataGraphCheck(
            check_id,
            _strings(
                raw["paths"],
                suite=suite_id,
                check=check_id,
                field="paths",
            ),
            None,
        )

    raw_cases = raw["cases"]
    if not isinstance(raw_cases, list) or not raw_cases:
        raise EngineError(
            Diagnostic(
                "CONFIG.METADATA_CASES",
                "invalid",
                "metadata fixture mode requires cases",
                suite=suite_id,
                check=check_id,
                field="cases",
            )
        )
    cases: list[MetadataCase] = []
    seen: set[str] = set()
    for raw_case in raw_cases:
        if not isinstance(raw_case, dict) or set(raw_case) != {
            "id",
            "paths",
            "expected",
        }:
            raise EngineError(
                Diagnostic(
                    "CONFIG.METADATA_CASE",
                    "invalid",
                    "metadata case requires exactly id, paths, and expected",
                    suite=suite_id,
                    check=check_id,
                )
            )
        case_id = raw_case["id"]
        expected = raw_case["expected"]
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise EngineError(
                Diagnostic(
                    "CONFIG.METADATA_CASE_ID",
                    "invalid",
                    "metadata case IDs must be unique non-empty strings",
                    suite=suite_id,
                    check=check_id,
                    observed=str(case_id),
                )
            )
        if (
            not isinstance(expected, list)
            or any(not isinstance(item, str) or not item for item in expected)
            or len(set(expected)) != len(expected)
        ):
            raise EngineError(
                Diagnostic(
                    "CONFIG.METADATA_EXPECTED",
                    "invalid",
                    "expected diagnostics must be unique non-empty strings",
                    suite=suite_id,
                    check=check_id,
                    field=case_id,
                )
            )
        seen.add(case_id)
        cases.append(
            MetadataCase(
                case_id,
                _strings(
                    raw_case["paths"],
                    suite=suite_id,
                    check=check_id,
                    field=f"{case_id}.paths",
                ),
                tuple(expected),
            )
        )
    return MetadataGraphCheck(check_id, None, tuple(cases))
