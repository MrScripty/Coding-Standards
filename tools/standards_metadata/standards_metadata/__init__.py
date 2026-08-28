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
    UnmappedModuleProjection,
    load_policy_unit_corpus,
    markdown_structural_digest,
    project_unmapped_module,
)
from .authority import (
    CANONICAL_STANDARDS_CORPUS_CODEC,
    METADATA_CODECS,
    CanonicalCorpusAuthority,
    CanonicalStandardsCorpusCodec,
)

__all__ = (
    "CANONICAL_MODULE_CORPUS",
    "CANONICAL_STANDARDS_CORPUS_CODEC",
    "METADATA_CODECS",
    "POLICY_UNIT_REGISTRY",
    "CanonicalModuleCorpus",
    "CanonicalStandardsCorpus",
    "CanonicalCorpusAuthority",
    "CanonicalStandardsCorpusCodec",
    "MetadataError",
    "MetadataFailure",
    "MetadataValidation",
    "ModuleMetadata",
    "PolicyUnit",
    "PolicyUnitCorpus",
    "PolicyUnitTombstone",
    "UnmappedModuleProjection",
    "load_canonical_standards_corpus",
    "load_canonical_module_corpus",
    "load_policy_unit_corpus",
    "load_module_metadata",
    "markdown_structural_digest",
    "project_unmapped_module",
    "validate_module_metadata",
)
