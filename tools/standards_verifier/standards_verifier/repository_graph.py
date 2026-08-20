from __future__ import annotations

from pathlib import Path

from tools.graph_engine.graph_engine import EdgeRegistry, InvalidSourceError
from tools.graph_engine.graph_engine.manifest import load_registry as load_graph_registry

from .checks.metadata import MetadataGraphCheck, ModuleMetadata, load_module_metadata
from .config import load_registry as load_suite_registry
from .config import load_suite
from .diagnostics import EngineError
from .graph_adapters import metadata_dependency_source, suite_dependency_source


SUITE_REGISTRY = "evaluation/standards-effectiveness/suite-registry.toml"


def _metadata_modules(root: Path) -> tuple[ModuleMetadata, ...]:
    entries = load_suite_registry(root, SUITE_REGISTRY)
    paths = {
        path
        for entry in entries
        for check in load_suite(root, entry).checks
        if isinstance(check, MetadataGraphCheck) and check.paths is not None
        for path in check.paths
    }
    modules: dict[str, ModuleMetadata] = {}
    try:
        for path in sorted(paths):
            module = load_module_metadata(
                root,
                path,
                suite="repository-graph",
                check="metadata-provider",
            )
            previous = modules.get(module.module_id)
            if previous is not None and previous != module:
                raise InvalidSourceError(
                    "metadata provider resolves one module ID to conflicting declarations",
                    node=module.module_id,
                    path=path,
                )
            modules[module.module_id] = module
    except EngineError as error:
        diagnostic = error.diagnostic
        raise InvalidSourceError(
            "metadata provider could not load canonical module metadata",
            code=diagnostic.code,
            path=diagnostic.path or "",
        ) from error
    return tuple(modules[key] for key in sorted(modules))


def load_repository_registry(root: Path, source_registry: str) -> EdgeRegistry:
    repo_root = root.resolve()
    try:
        entries = load_suite_registry(repo_root, SUITE_REGISTRY)
    except EngineError as error:
        diagnostic = error.diagnostic
        raise InvalidSourceError(
            "suite dependency provider could not load the suite registry",
            code=diagnostic.code,
            path=diagnostic.path or SUITE_REGISTRY,
        ) from error
    providers = {
        "standards-verifier.suite-dependencies": suite_dependency_source(
            entries,
            SUITE_REGISTRY,
            include_path_aliases=True,
        ),
        "standards-verifier.metadata-dependencies": metadata_dependency_source(
            _metadata_modules(repo_root)
        ),
    }
    return load_graph_registry(
        repo_root,
        source_registry,
        providers=providers,
    )
