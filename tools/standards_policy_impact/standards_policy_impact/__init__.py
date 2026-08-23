"""Typed policy-impact declarations compiled into graph and semantic views."""

from .compiler import (
    CATALOG_SOURCE_ID,
    DEFAULT_REGISTRY,
    POLICY_GROUP,
    RELATIONSHIP_KIND_CONTRACT_VERSION,
    RELATIONSHIP_KINDS,
    SEMANTIC_GROUP,
    SOURCE_ID,
    compile_policy_impact,
    policy_impact_edge_id,
)
from .errors import PolicyImpactError, PolicyImpactFailure
from .model import (
    CompiledPolicyImpactSet,
    PolicyImpactSemantics,
    PolicyImpactSource,
    RelationshipKind,
    thaw,
)

__all__ = (
    "CATALOG_SOURCE_ID",
    "DEFAULT_REGISTRY",
    "POLICY_GROUP",
    "RELATIONSHIP_KIND_CONTRACT_VERSION",
    "RELATIONSHIP_KINDS",
    "SEMANTIC_GROUP",
    "SOURCE_ID",
    "CompiledPolicyImpactSet",
    "PolicyImpactError",
    "PolicyImpactFailure",
    "PolicyImpactSemantics",
    "PolicyImpactSource",
    "RelationshipKind",
    "compile_policy_impact",
    "policy_impact_edge_id",
    "thaw",
)
