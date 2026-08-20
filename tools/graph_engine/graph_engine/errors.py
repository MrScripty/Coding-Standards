from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class GraphFailure:
    code: str
    message: str
    details: Mapping[str, str]


class GraphError(Exception):
    """Base class for neutral graph failures."""

    code = "GRAPH.ERROR"

    def __init__(self, message: str, **details: str) -> None:
        super().__init__(message)
        self.failure = GraphFailure(self.code, message, dict(sorted(details.items())))


class UnknownNodeError(GraphError):
    code = "GRAPH.UNKNOWN_NODE"


class UnknownGroupError(GraphError):
    code = "GRAPH.UNKNOWN_GROUP"


class UnknownEdgeError(GraphError):
    code = "GRAPH.UNKNOWN_EDGE"


class MissingArtifactError(GraphError):
    code = "GRAPH.MISSING_ARTIFACT"


class InvalidEdgeError(GraphError):
    code = "GRAPH.INVALID_EDGE"


class InvalidGroupError(GraphError):
    code = "GRAPH.INVALID_GROUP"


class InvalidSourceError(GraphError):
    code = "GRAPH.INVALID_SOURCE"


class ForbiddenTraversalError(GraphError):
    code = "GRAPH.FORBIDDEN_TRAVERSAL"


class AliasConflictError(GraphError):
    code = "GRAPH.ALIAS_CONFLICT"


class PathEscapeError(GraphError):
    code = "GRAPH.PATH_ESCAPE"


class UnsafeOutputError(GraphError):
    code = "GRAPH.UNSAFE_OUTPUT"
