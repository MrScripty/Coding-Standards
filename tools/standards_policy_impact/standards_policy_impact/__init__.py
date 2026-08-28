"""Typed policy-impact declarations compiled into graph and semantic views."""

from .compiler import (
    DEFAULT_AUTHORING_CONTRACT,
    CATALOG_SOURCE_ID,
    DEFAULT_REGISTRY,
    POLICY_GROUP,
    RELATIONSHIP_KIND_CONTRACT_VERSION,
    SEMANTIC_GROUP,
    SOURCE_ID,
    compile_policy_impact,
    policy_impact_edge_id,
)
from .errors import PolicyImpactError, PolicyImpactFailure
from .model import (
    CompiledPolicyImpactSet,
    PolicyImpactArtifact,
    PolicyImpactSemantics,
    PolicyImpactSource,
    RelationshipKind,
    thaw,
)
from .authority import (
    COMPILED_POLICY_IMPACT_CODEC,
    POLICY_IMPACT_CODECS,
    CompiledPolicyImpactAuthority,
    CompiledPolicyImpactCodec,
)

__all__ = (
    "DEFAULT_AUTHORING_CONTRACT",
    "CATALOG_SOURCE_ID",
    "DEFAULT_REGISTRY",
    "POLICY_GROUP",
    "RELATIONSHIP_KIND_CONTRACT_VERSION",
    "SEMANTIC_GROUP",
    "SOURCE_ID",
    "CompiledPolicyImpactSet",
    "CompiledPolicyImpactAuthority",
    "CompiledPolicyImpactCodec",
    "COMPILED_POLICY_IMPACT_CODEC",
    "POLICY_IMPACT_CODECS",
    "PolicyImpactArtifact",
    "PolicyImpactError",
    "PolicyImpactFailure",
    "PolicyImpactSemantics",
    "PolicyImpactSource",
    "RelationshipKind",
    "compile_policy_impact",
    "policy_impact_edge_id",
    "thaw",
)
