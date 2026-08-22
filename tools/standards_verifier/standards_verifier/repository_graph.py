from __future__ import annotations

from pathlib import Path

from tools.graph_engine.graph_engine import EdgeRegistry, InvalidSourceError
from tools.graph_engine.graph_engine.manifest import load_registry as load_graph_registry

from .canonical_modules import load_canonical_module_corpus
from .config import load_registry as load_suite_registry
from .diagnostics import EngineError
from .graph_adapters import metadata_dependency_source, suite_dependency_source


SUITE_REGISTRY = "evaluation/standards-effectiveness/suite-registry.toml"


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
    try:
        corpus = load_canonical_module_corpus(repo_root)
    except EngineError as error:
        diagnostic = error.diagnostic
        raise InvalidSourceError(
            "metadata provider could not load the canonical module corpus",
            code=diagnostic.code,
            path=diagnostic.path or "",
        ) from error
    providers = {
        "standards-verifier.suite-dependencies": suite_dependency_source(
            entries,
            SUITE_REGISTRY,
            include_path_aliases=True,
        ),
        "standards-verifier.metadata-dependencies": metadata_dependency_source(
            corpus.modules
        ),
    }
    return load_graph_registry(
        repo_root,
        source_registry,
        providers=providers,
    )
