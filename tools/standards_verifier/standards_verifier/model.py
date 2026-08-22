from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from .diagnostics import Diagnostic


class Check(Protocol):
    id: str

    def run(self, context: "CheckContext") -> list[Diagnostic]: ...


class CompleteSuiteCatalogCheck:
    """Marker for checks whose invariant inspects every registered suite body."""

    __slots__ = ()


@dataclass(frozen=True, slots=True)
class Suite:
    id: str
    owner: str
    description: str
    checks: tuple[Check, ...]


@dataclass(frozen=True, slots=True)
class RegistryEntry:
    id: str
    path: str
    requires: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SuiteCatalog:
    registry_path: str
    entries: tuple[RegistryEntry, ...]
    suites: tuple[Suite, ...]

    def __post_init__(self) -> None:
        entry_ids = tuple(entry.id for entry in self.entries)
        suite_ids = tuple(suite.id for suite in self.suites)
        if len(set(suite_ids)) != len(suite_ids):
            raise ValueError("catalog suite IDs must be unique")
        loaded = frozenset(suite_ids)
        if tuple(suite_id for suite_id in entry_ids if suite_id in loaded) != suite_ids:
            raise ValueError(
                "catalog suites must be a registry-ordered subset of entries"
            )

    @classmethod
    def empty(cls) -> "SuiteCatalog":
        return cls("", (), ())

    @property
    def suite_ids(self) -> frozenset[str]:
        return frozenset(entry.id for entry in self.entries)

    @property
    def suite_paths(self) -> tuple[tuple[str, str], ...]:
        return tuple((entry.id, entry.path) for entry in self.entries)

    def entry(self, suite_id: str) -> RegistryEntry:
        for entry in self.entries:
            if entry.id == suite_id:
                return entry
        raise KeyError(f"suite is absent from the catalog: {suite_id}")

    def suite(self, suite_id: str) -> Suite:
        for suite in self.suites:
            if suite.id == suite_id:
                return suite
        raise KeyError(f"suite is absent from the catalog: {suite_id}")

    def suite_for_path(self, path: str) -> Suite | None:
        for entry in self.entries:
            if entry.path == path:
                return next(
                    (suite for suite in self.suites if suite.id == entry.id),
                    None,
                )
        return None


@dataclass(frozen=True, slots=True)
class CheckContext:
    repo_root: Path
    suite_id: str
    catalog: SuiteCatalog


@dataclass(slots=True)
class SuiteResult:
    id: str
    status: str
    check_count: int
    diagnostics: list[Diagnostic] = field(default_factory=list)
    exit_code: int = 0

    def as_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "status": self.status,
            "check_count": self.check_count,
            "diagnostics": [diagnostic.as_dict() for diagnostic in self.diagnostics],
        }
