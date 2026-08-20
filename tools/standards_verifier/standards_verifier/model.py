from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from .diagnostics import Diagnostic


class Check(Protocol):
    id: str

    def run(self, context: "CheckContext") -> list[Diagnostic]: ...


@dataclass(frozen=True, slots=True)
class CheckContext:
    repo_root: Path
    suite_id: str
    registered_suite_ids: frozenset[str]
    registered_suite_paths: tuple[tuple[str, str], ...]


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
