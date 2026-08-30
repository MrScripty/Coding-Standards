from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from tools.repository_git.repository_git import indexed_paths
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    encode_identity_value,
)

from .config import extend_catalog, load_registry_catalog
from .model import CheckContext, CheckFileInput, CheckRepositoryIndexInput
from .paths import contained_file, contained_path


DEFAULT_REGISTRY = "evaluation/standards-effectiveness/suite-registry.toml"
DEFAULT_PROJECTION = "evaluation/standards-effectiveness/generated/suite-inputs.json"
CONTRACT = "standards-analysis:suite-input-manifest:v2"
SCHEMA_VERSION = 2


def file_digest(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def repository_index_digest(paths: Sequence[str]) -> str:
    encoded = encode_identity_value(
        IdentityObject(
            (
                ("domain", "standards-analysis:repository-index:v1"),
                ("paths", IdentityArray(paths)),
            )
        )
    )
    return file_digest(encoded)


@dataclass(frozen=True, slots=True, order=True)
class SuiteInputUse:
    suite: str
    check: str
    role: str

    def as_projection(self) -> dict[str, str]:
        return {"suite": self.suite, "check": self.check, "role": self.role}


@dataclass(frozen=True, slots=True)
class SuiteFileInput:
    path: str
    state: str
    digest: str | None
    uses: tuple[SuiteInputUse, ...]

    def as_projection(self) -> dict[str, object]:
        value: dict[str, object] = {
            "path": self.path,
            "state": self.state,
            "uses": [use.as_projection() for use in self.uses],
        }
        if self.digest is not None:
            value["digest"] = self.digest
        return value


@dataclass(frozen=True, slots=True)
class RepositoryIndexObservation:
    digest: str
    uses: tuple[SuiteInputUse, ...]

    def as_projection(self) -> dict[str, object]:
        return {
            "digest": self.digest,
            "uses": [use.as_projection() for use in self.uses],
        }


@dataclass(frozen=True, slots=True)
class SuiteInputManifest:
    registry_path: str
    registry_digest: str
    suites: tuple[tuple[str, str, str], ...]
    files: tuple[SuiteFileInput, ...]
    repository_index: RepositoryIndexObservation | None

    def as_projection(self) -> dict[str, object]:
        return {
            "schema_version": SCHEMA_VERSION,
            "contract": CONTRACT,
            "registry": {
                "path": self.registry_path,
                "digest": self.registry_digest,
            },
            "suites": [
                {"id": suite_id, "path": path, "digest": digest}
                for suite_id, path, digest in self.suites
            ],
            "files": [item.as_projection() for item in self.files],
            "repository_index": (
                self.repository_index.as_projection()
                if self.repository_index is not None
                else None
            ),
        }


def suite_input_manifest_bytes(manifest: SuiteInputManifest) -> bytes:
    return (
        json.dumps(
            manifest.as_projection(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def compile_suite_input_manifest(
    root: Path,
    registry_path: str = DEFAULT_REGISTRY,
) -> SuiteInputManifest:
    repo_root = root.resolve()
    catalog = load_registry_catalog(repo_root, registry_path)
    catalog = extend_catalog(repo_root, catalog, catalog.suite_ids)
    file_uses: dict[tuple[str, str], set[SuiteInputUse]] = {}
    index_uses: set[SuiteInputUse] = set()
    for suite in catalog.suites:
        context = CheckContext(repo_root, suite.id, catalog)
        for check in suite.checks:
            for declaration in check.authority_inputs(context):
                use = SuiteInputUse(suite.id, check.id, declaration.role)
                if isinstance(declaration, CheckRepositoryIndexInput):
                    index_uses.add(use)
                elif isinstance(declaration, CheckFileInput):
                    key = (declaration.path, declaration.state)
                    file_uses.setdefault(key, set()).add(use)
                else:
                    raise TypeError(
                        "check returned an unsupported authority input: "
                        f"{type(declaration).__module__}."
                        f"{type(declaration).__qualname__}"
                    )

    states: dict[str, str] = {}
    for path, state in file_uses:
        previous = states.setdefault(path, state)
        if previous != state:
            raise ValueError(
                f"suite input has contradictory states: {path}: {previous}, {state}"
            )

    files = []
    for (path, state), uses in sorted(file_uses.items()):
        if state == "present":
            source = contained_file(repo_root, path)
            digest: str | None = file_digest(source.read_bytes())
        else:
            candidate = contained_path(repo_root, path)
            if candidate.exists() or candidate.is_symlink():
                raise ValueError(f"suite input must be absent: {path}")
            digest = None
        files.append(SuiteFileInput(path, state, digest, tuple(sorted(uses))))

    registry = contained_file(repo_root, registry_path)
    suites = tuple(
        (
            entry.id,
            entry.path,
            file_digest(contained_file(repo_root, entry.path).read_bytes()),
        )
        for entry in catalog.entries
    )
    index = None
    if index_uses:
        index = RepositoryIndexObservation(
            repository_index_digest(indexed_paths(repo_root)),
            tuple(sorted(index_uses)),
        )
    return SuiteInputManifest(
        registry_path,
        file_digest(registry.read_bytes()),
        suites,
        tuple(files),
        index,
    )


def compile_suite_input_projection(
    root: Path,
    registry_path: str = DEFAULT_REGISTRY,
) -> dict[str, object]:
    return compile_suite_input_manifest(root, registry_path).as_projection()


def suite_input_projection_bytes(root: Path) -> bytes:
    return suite_input_manifest_bytes(compile_suite_input_manifest(root))


def check_suite_input_projection(root: Path) -> int:
    expected = suite_input_projection_bytes(root)
    path = root / DEFAULT_PROJECTION
    if not path.is_file() or path.read_bytes() != expected:
        print(f"STALE {DEFAULT_PROJECTION}")
        return 2
    return 0


def write_suite_input_projection(root: Path) -> int:
    path = root / DEFAULT_PROJECTION
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(suite_input_projection_bytes(root))
    return 0
