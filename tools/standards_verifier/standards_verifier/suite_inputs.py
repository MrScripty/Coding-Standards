from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Sequence

from tools.repository_git.repository_git import indexed_paths
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    encode_identity_value,
)
from tools.standards_metadata.standards_metadata import (
    SUITE_INPUT_CONTRACT,
    SUITE_INPUT_SCHEMA_VERSION,
    RepositoryIndexObservation,
    SuiteDefinitionInput,
    SuiteFileInput,
    SuiteInputManifest,
    SuiteInputUse,
    file_digest,
    suite_input_manifest_bytes,
)

from .config import extend_catalog, load_registry_catalog
from .diagnostics import Diagnostic, EngineError
from .model import CheckContext, CheckFileInput, CheckRepositoryIndexInput
from .paths import contained_file, contained_path


DEFAULT_REGISTRY = "evaluation/standards-effectiveness/suite-registry.toml"
DEFAULT_PROJECTION = "evaluation/standards-effectiveness/generated/suite-inputs.json"
CONTRACT = SUITE_INPUT_CONTRACT
SCHEMA_VERSION = SUITE_INPUT_SCHEMA_VERSION


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
            raise EngineError(
                Diagnostic(
                    "INPUT.CONTRADICTORY_STATE",
                    "invalid",
                    "suite input declarations require contradictory path states",
                    path=path,
                    expected=previous,
                    observed=state,
                )
            )

    files = []
    for (path, state), uses in sorted(file_uses.items()):
        if state == "present":
            source = contained_file(repo_root, path)
            digest: str | None = file_digest(source.read_bytes())
        else:
            candidate = contained_path(repo_root, path)
            if candidate.exists() or candidate.is_symlink():
                raise EngineError(
                    Diagnostic(
                        "INPUT.EXPECTED_ABSENT",
                        "invalid",
                        "suite input declared absent is present",
                        path=path,
                    )
                )
            digest = None
        files.append(SuiteFileInput(path, state, digest, tuple(sorted(uses))))

    registry = contained_file(repo_root, registry_path)
    suites = tuple(
        SuiteDefinitionInput(
            entry.id,
            entry.path,
            file_digest(contained_file(repo_root, entry.path).read_bytes()),
            entry.requires,
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


def check_suite_input_projection(
    root: Path,
    *,
    output: Callable[[str], None] = print,
) -> int:
    expected = suite_input_projection_bytes(root)
    path = root / DEFAULT_PROJECTION
    if not path.is_file() or path.read_bytes() != expected:
        output(f"STALE {DEFAULT_PROJECTION}")
        return 2
    return 0


def write_suite_input_projection(root: Path) -> int:
    path = root / DEFAULT_PROJECTION
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(suite_input_projection_bytes(root))
    return 0
