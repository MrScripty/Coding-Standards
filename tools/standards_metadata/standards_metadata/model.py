from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .errors import MetadataFailure

if TYPE_CHECKING:
    from .policy_units import PolicyUnit, PolicyUnitCorpus, PolicyUnitTombstone


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


@dataclass(frozen=True, slots=True)
class CanonicalStandardsCorpus:
    module_corpus: CanonicalModuleCorpus
    policy_unit_corpus: "PolicyUnitCorpus"

    @property
    def modules(self) -> tuple[ModuleMetadata, ...]:
        return self.module_corpus.modules

    @property
    def policy_units(self) -> tuple["PolicyUnit", ...]:
        return self.policy_unit_corpus.units

    def resolve_module(self, value: str) -> ModuleMetadata | None:
        return self.module_corpus.resolve(value)

    def resolve_policy_unit(
        self,
        value: str,
    ) -> "PolicyUnit | PolicyUnitTombstone | None":
        return self.policy_unit_corpus.resolve(value)
