from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .checks.metadata import ModuleMetadata, load_module_metadata_graph
from .diagnostics import Diagnostic, EngineError
from .paths import contained_file


CANONICAL_MODULE_CORPUS = (
    "evaluation/standards-effectiveness/canonical-module-corpus.toml"
)


@dataclass(frozen=True, slots=True)
class CanonicalModuleCorpus:
    path: str
    members: tuple[str, ...]
    modules: tuple[ModuleMetadata, ...]

    @property
    def normative_modules(self) -> tuple[ModuleMetadata, ...]:
        return tuple(module for module in self.modules if module.role != "reference")


def _load_toml(path: Path, display_path: str) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            raw = tomllib.load(handle)
    except tomllib.TOMLDecodeError as error:
        raise EngineError(
            Diagnostic(
                "CONFIG.INVALID_TOML",
                "invalid",
                str(error),
                path=display_path,
            )
        ) from error
    if not isinstance(raw, dict):
        raise EngineError(
            Diagnostic(
                "CONFIG.CANONICAL_CORPUS_ROOT",
                "invalid",
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
        raise EngineError(
            Diagnostic(
                "CONFIG.CANONICAL_CORPUS_MEMBERS",
                "invalid",
                "members must contain non-empty repository-relative paths",
                path=manifest_path,
                field="members",
            )
        )
    if len(set(raw)) != len(raw):
        raise EngineError(
            Diagnostic(
                "CONFIG.CANONICAL_CORPUS_DUPLICATE",
                "invalid",
                "canonical corpus members must be unique",
                path=manifest_path,
                field="members",
            )
        )

    members = tuple(raw)
    for member in members:
        normalized = PurePosixPath(member)
        if (
            normalized.is_absolute()
            or ".." in normalized.parts
            or member.startswith("./")
            or str(normalized) != member
        ):
            raise EngineError(
                Diagnostic(
                    "PATH.OUTSIDE_REPOSITORY",
                    "invalid",
                    "canonical corpus member must be a normalized repository-relative path",
                    path=member,
                )
            )
    return members


def load_canonical_module_corpus(
    root: Path,
    manifest_path: str = CANONICAL_MODULE_CORPUS,
) -> CanonicalModuleCorpus:
    manifest = contained_file(root, manifest_path)
    raw = _load_toml(manifest, manifest_path)
    required = {"schema_version", "members"}
    if set(raw) != required:
        unexpected = sorted(set(raw) - required)
        missing = sorted(required - set(raw))
        raise EngineError(
            Diagnostic(
                "CONFIG.CANONICAL_CORPUS_FIELDS",
                "invalid",
                "canonical corpus requires exactly schema_version and members",
                path=manifest_path,
                field=(unexpected or missing)[0],
            )
        )
    if raw["schema_version"] != 1:
        raise EngineError(
            Diagnostic(
                "CONFIG.SCHEMA_VERSION",
                "invalid",
                "canonical corpus schema version must be 1",
                path=manifest_path,
                expected="1",
                observed=str(raw["schema_version"]),
            )
        )

    members = _members(raw["members"], manifest_path)
    modules = load_module_metadata_graph(
        root,
        members,
        suite="repository-graph",
        check="canonical-module-corpus",
    )
    return CanonicalModuleCorpus(manifest_path, members, modules)
