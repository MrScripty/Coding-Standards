from __future__ import annotations

from dataclasses import dataclass

from .errors import MetadataFailure


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
class CanonicalModuleCorpus:
    path: str
    members: tuple[str, ...]
    modules: tuple[ModuleMetadata, ...]

    @property
    def normative_modules(self) -> tuple[ModuleMetadata, ...]:
        return tuple(module for module in self.modules if module.role != "reference")

    def resolve(self, value: str) -> ModuleMetadata | None:
        for module in self.modules:
            if value in (module.module_id, module.path):
                return module
        return None


@dataclass(frozen=True, slots=True)
class MetadataValidation:
    modules: tuple[ModuleMetadata, ...]
    failures: tuple[MetadataFailure, ...]
