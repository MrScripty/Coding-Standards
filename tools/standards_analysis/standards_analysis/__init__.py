"""Read-only standards snapshots and policy-unit analysis foundations."""

from .errors import AnalysisError, AnalysisFailure
from .changes import (
    CHANGE_GRAPH_GROUPS,
    POLICY_IMPACT,
    STANDARDS_REQUIRES,
    STANDARDS_SPECIALIZES,
    ChangeClassification,
    ChangeDescriptor,
    ChangeKind,
    ChangedPolicyUnit,
    ClassifiedChange,
    GraphSeedSelection,
    ReviewScope,
    SemanticProposal,
    SemanticState,
    classify_changes,
)
from .impact import (
    ImpactCandidate,
    ImpactSelection,
    ImpactTrace,
    select_impact,
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
    "AnalysisError",
    "AnalysisFailure",
    "AnalysisVersions",
    "CHANGE_GRAPH_GROUPS",
    "ChangeClassification",
    "ChangeDescriptor",
    "ChangeKind",
    "ChangedPolicyUnit",
    "ClassifiedChange",
    "GraphSeedSelection",
    "ImpactCandidate",
    "ImpactSelection",
    "ImpactTrace",
    "POLICY_IMPACT",
    "ROUTER_PROJECTION",
    "RouteFact",
    "RouteRule",
    "RouterProjection",
    "ReviewScope",
    "STANDARDS_REQUIRES",
    "STANDARDS_SPECIALIZES",
    "SemanticProposal",
    "SemanticState",
    "canonical_json_bytes",
    "classify_changes",
    "compile_snapshot",
    "digest_bytes",
    "identity",
    "load_router_projection",
    "select_impact",
)
