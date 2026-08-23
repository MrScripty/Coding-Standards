"""Read-only standards snapshots and policy-unit analysis foundations."""

from .errors import AnalysisError, AnalysisFailure
from .applicability import ApplicabilityEvaluator, FactDefinition, FactState, Truth
from .policy_units import (
    POLICY_UNIT_REGISTRY,
    PolicyUnit,
    PolicyUnitCorpus,
    PolicyUnitTombstone,
    load_policy_unit_corpus,
    markdown_structural_digest,
)
from .serialization import canonical_json_bytes, digest_bytes, identity
from .routing import (
    ROUTER_PROJECTION,
    RouteFact,
    RouteRule,
    RouterProjection,
    load_router_projection,
)
from .snapshots import AnalysisVersions, compile_snapshot

__all__ = (
    "POLICY_UNIT_REGISTRY",
    "AnalysisError",
    "AnalysisFailure",
    "ApplicabilityEvaluator",
    "FactDefinition",
    "FactState",
    "AnalysisVersions",
    "PolicyUnit",
    "PolicyUnitCorpus",
    "PolicyUnitTombstone",
    "ROUTER_PROJECTION",
    "RouteFact",
    "RouteRule",
    "RouterProjection",
    "Truth",
    "canonical_json_bytes",
    "compile_snapshot",
    "digest_bytes",
    "identity",
    "load_policy_unit_corpus",
    "load_router_projection",
    "markdown_structural_digest",
)
