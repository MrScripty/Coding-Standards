from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Sequence

from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    encode_identity_value,
)
from tools.standards_metadata.standards_metadata import (
    FrozenContentSource,
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
from .model import CheckInputContext, CheckFileInput, CheckRepositoryIndexInput
from .input_sources import DirectoryInputs, FrozenInputs, SuiteInputSource


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
    *,
    repository_paths: Sequence[str] | None = None,
) -> SuiteInputManifest:
    return _compile_suite_input_manifest(DirectoryInputs(root, repository_paths), registry_path)


def _compile_suite_input_manifest(
    inputs: SuiteInputSource,
    registry_path: str,
) -> SuiteInputManifest:
    catalog = load_registry_catalog(inputs, registry_path)
    catalog = extend_catalog(inputs, catalog, catalog.suite_ids)
    file_uses: dict[tuple[str, str], set[SuiteInputUse]] = {}
    index_uses: set[SuiteInputUse] = set()
    for suite in catalog.suites:
        context = CheckInputContext(inputs, suite.id, catalog)
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
            digest: str | None = file_digest(inputs.read_bytes(path))
        else:
            if inputs.exists(path):
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

    registry = inputs.read_bytes(registry_path)
    suites = tuple(
        SuiteDefinitionInput(
            entry.id,
            entry.path,
            file_digest(inputs.read_bytes(entry.path)),
            entry.requires,
        )
        for entry in catalog.entries
    )
    index = None
    if index_uses:
        observed_paths = inputs.indexed_paths()
        index = RepositoryIndexObservation(
            repository_index_digest(observed_paths),
            tuple(sorted(index_uses)),
        )
    return SuiteInputManifest(
        registry_path,
        file_digest(registry),
        suites,
        tuple(files),
        index,
    )


def compile_suite_input_projection(
    root: Path,
    registry_path: str = DEFAULT_REGISTRY,
    *,
    repository_paths: Sequence[str] | None = None,
) -> dict[str, object]:
    return compile_suite_input_manifest(
        root, registry_path, repository_paths=repository_paths
    ).as_projection()


def suite_input_projection_bytes(
    root: Path,
    *,
    repository_paths: Sequence[str] | None = None,
) -> bytes:
    return suite_input_manifest_bytes(
        compile_suite_input_manifest(root, repository_paths=repository_paths)
    )


def suite_input_projection_bytes_from_content(
    source: FrozenContentSource,
    *,
    repository_paths: Sequence[str],
) -> bytes:
    """Compile the exact manifest from captured bytes and explicit membership."""
    return suite_input_manifest_bytes(
        _compile_suite_input_manifest(FrozenInputs(source, repository_paths), DEFAULT_REGISTRY)
    )


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
