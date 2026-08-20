from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from .checks import parse_check
from .diagnostics import Diagnostic, EngineError
from .graph_adapters import SUITE_DEPENDENCIES, suite_dependency_registry
from .model import RegistryEntry, Suite
from .paths import contained_file


def _load_toml(path: Path, display_path: str) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            value = tomllib.load(handle)
    except tomllib.TOMLDecodeError as error:
        raise EngineError(Diagnostic("CONFIG.INVALID_TOML", "invalid", str(error), path=display_path)) from error
    if not isinstance(value, dict):
        raise EngineError(Diagnostic("CONFIG.ROOT", "invalid", "TOML root must be a table", path=display_path))
    return value


def load_registry(root: Path, registry_path: str) -> tuple[RegistryEntry, ...]:
    path = contained_file(root, registry_path)
    raw = _load_toml(path, registry_path)
    if set(raw) != {"schema_version", "suites"}:
        unknown = sorted(set(raw) - {"schema_version", "suites"})
        raise EngineError(Diagnostic("CONFIG.REGISTRY_FIELDS", "invalid", "registry requires exactly schema_version and suites", path=registry_path, field=unknown[0] if unknown else None))
    if raw["schema_version"] != 1:
        raise EngineError(Diagnostic("CONFIG.SCHEMA_VERSION", "invalid", "registry schema version must be 1", path=registry_path, expected="1", observed=str(raw["schema_version"])))
    raw_entries = raw["suites"]
    if not isinstance(raw_entries, list) or not raw_entries:
        raise EngineError(Diagnostic("CONFIG.EMPTY_REGISTRY", "invalid", "registry requires at least one suite", path=registry_path))

    entries = []
    seen = set()
    for raw_entry in raw_entries:
        if not isinstance(raw_entry, dict) or set(raw_entry) != {"id", "path", "requires"}:
            raise EngineError(Diagnostic("CONFIG.REGISTRY_ENTRY", "invalid", "registry suite requires exactly id, path, and requires", path=registry_path))
        suite_id = raw_entry["id"]
        suite_path = raw_entry["path"]
        requires = raw_entry["requires"]
        if not isinstance(suite_id, str) or not suite_id or not isinstance(suite_path, str) or not suite_path:
            raise EngineError(Diagnostic("CONFIG.REGISTRY_VALUE", "invalid", "suite id and path must be non-empty strings", path=registry_path))
        if not isinstance(requires, list) or any(not isinstance(item, str) or not item for item in requires) or len(set(requires)) != len(requires):
            raise EngineError(Diagnostic("CONFIG.REGISTRY_DEPENDENCIES", "invalid", "requires must contain unique non-empty suite IDs", suite=suite_id, path=registry_path))
        if suite_id in seen:
            raise EngineError(Diagnostic("CONFIG.DUPLICATE_SUITE", "invalid", "suite ID is duplicated", suite=suite_id, path=registry_path))
        seen.add(suite_id)
        entries.append(RegistryEntry(suite_id, suite_path, tuple(requires)))

    known = {entry.id for entry in entries}
    for entry in entries:
        for dependency in entry.requires:
            if dependency == entry.id:
                raise EngineError(Diagnostic("CONFIG.SELF_DEPENDENCY", "invalid", "suite cannot depend on itself", suite=entry.id, path=registry_path))
            if dependency not in known:
                raise EngineError(Diagnostic("CONFIG.UNKNOWN_DEPENDENCY", "unavailable", "suite dependency is not registered", suite=entry.id, path=registry_path, observed=dependency), exit_code=3)
    _validate_acyclic(root, entries, registry_path)
    return tuple(entries)


def _validate_acyclic(
    root: Path, entries: list[RegistryEntry], registry_path: str
) -> None:
    graph = suite_dependency_registry(
        root,
        entries,
        registry_path,
        include_path_aliases=False,
    )
    cycle = graph.find_cycle(SUITE_DEPENDENCIES)
    if cycle is not None:
        raise EngineError(
            Diagnostic(
                "CONFIG.DEPENDENCY_CYCLE",
                "invalid",
                "suite dependency graph contains a cycle",
                suite=cycle[0],
                path=registry_path,
                observed=" -> ".join(cycle),
            )
        )


def load_suite(root: Path, entry: RegistryEntry) -> Suite:
    path = contained_file(root, entry.path, suite=entry.id)
    raw = _load_toml(path, entry.path)
    allowed = {"schema_version", "id", "owner", "description", "checks"}
    if set(raw) != allowed:
        unknown = sorted(set(raw) - allowed)
        missing = sorted(allowed - set(raw))
        raise EngineError(Diagnostic("CONFIG.SUITE_FIELDS", "invalid", "suite requires exactly schema_version, id, owner, description, and checks", suite=entry.id, path=entry.path, field=(unknown or missing)[0]))
    if raw["schema_version"] != 1:
        raise EngineError(Diagnostic("CONFIG.SCHEMA_VERSION", "invalid", "suite schema version must be 1", suite=entry.id, path=entry.path, expected="1", observed=str(raw["schema_version"])))
    if raw["id"] != entry.id:
        raise EngineError(Diagnostic("CONFIG.SUITE_ID_MISMATCH", "invalid", "suite ID does not match registry", suite=entry.id, path=entry.path, expected=entry.id, observed=str(raw["id"])))
    owner = raw["owner"]
    description = raw["description"]
    if not isinstance(owner, str) or not owner or not isinstance(description, str) or not description:
        raise EngineError(Diagnostic("CONFIG.SUITE_TEXT", "invalid", "suite owner and description must be non-empty strings", suite=entry.id, path=entry.path))
    raw_checks = raw["checks"]
    if not isinstance(raw_checks, list) or not raw_checks:
        raise EngineError(Diagnostic("CONFIG.EMPTY_SUITE", "invalid", "suite requires at least one check", suite=entry.id, path=entry.path))
    checks = tuple(parse_check(raw_check, entry.id) for raw_check in raw_checks)
    check_ids = [check.id for check in checks]
    if len(set(check_ids)) != len(check_ids):
        raise EngineError(Diagnostic("CONFIG.DUPLICATE_CHECK", "invalid", "check ID is duplicated within suite", suite=entry.id, path=entry.path))
    return Suite(entry.id, owner, description, checks)
