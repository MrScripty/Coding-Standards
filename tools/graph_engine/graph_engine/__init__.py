"""Repository-neutral directed edge registration, queries, and traversal."""

from .errors import (
    AliasConflictError,
    ForbiddenTraversalError,
    GraphError,
    InvalidEdgeError,
    InvalidGroupError,
    InvalidSourceError,
    MissingArtifactError,
    PathEscapeError,
    UnknownEdgeError,
    UnknownGroupError,
    UnknownNodeError,
    UnsafeOutputError,
)
from .manifest import DEFAULT_SOURCE_REGISTRY, load_manifest, load_registry
from .paths import contained_path
from .cli import main as graph_query_main
from .model import (
    Direction,
    Edge,
    EdgeGroup,
    EdgeSource,
    GraphContribution,
    Node,
    Provenance,
    TraversalPolicy,
)
from .registry import EdgeRegistry, EdgeView, TraversalResult, TraversalStep
from .projection import load_graph_contribution, project_graph_contribution

__all__ = (
    "AliasConflictError",
    "DEFAULT_SOURCE_REGISTRY",
    "Direction",
    "Edge",
    "EdgeGroup",
    "EdgeRegistry",
    "EdgeSource",
    "EdgeView",
    "ForbiddenTraversalError",
    "GraphContribution",
    "GraphError",
    "InvalidEdgeError",
    "InvalidGroupError",
    "InvalidSourceError",
    "MissingArtifactError",
    "Node",
    "PathEscapeError",
    "Provenance",
    "TraversalPolicy",
    "TraversalResult",
    "TraversalStep",
    "UnknownEdgeError",
    "UnknownGroupError",
    "UnknownNodeError",
    "UnsafeOutputError",
    "load_registry",
    "load_manifest",
    "load_graph_contribution",
    "contained_path",
    "graph_query_main",
    "project_graph_contribution",
)
