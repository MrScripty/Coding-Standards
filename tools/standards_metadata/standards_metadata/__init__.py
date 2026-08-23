"""Neutral canonical standards metadata loading and structural validation."""

from .errors import MetadataError, MetadataFailure
from .corpus import load_canonical_standards_corpus
from .loader import (
    CANONICAL_MODULE_CORPUS,
    load_canonical_module_corpus,
    load_module_metadata,
    validate_module_metadata,
)
from .model import (
    CanonicalModuleCorpus,
    CanonicalStandardsCorpus,
    MetadataValidation,
    ModuleMetadata,
)
from .policy_units import (
    POLICY_UNIT_REGISTRY,
    PolicyUnit,
    PolicyUnitCorpus,
    PolicyUnitTombstone,
    load_policy_unit_corpus,
    markdown_structural_digest,
)
from .serialization import canonical_json_bytes, digest_bytes

__all__ = (
    "CANONICAL_MODULE_CORPUS",
    "POLICY_UNIT_REGISTRY",
    "CanonicalModuleCorpus",
    "CanonicalStandardsCorpus",
    "MetadataError",
    "MetadataFailure",
    "MetadataValidation",
    "ModuleMetadata",
    "PolicyUnit",
    "PolicyUnitCorpus",
    "PolicyUnitTombstone",
    "canonical_json_bytes",
    "digest_bytes",
    "load_canonical_standards_corpus",
    "load_canonical_module_corpus",
    "load_policy_unit_corpus",
    "load_module_metadata",
    "markdown_structural_digest",
    "validate_module_metadata",
)
