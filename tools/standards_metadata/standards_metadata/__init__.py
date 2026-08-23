"""Neutral canonical standards metadata loading and structural validation."""

from .errors import MetadataError, MetadataFailure
from .loader import (
    CANONICAL_MODULE_CORPUS,
    load_canonical_module_corpus,
    load_module_metadata,
    validate_module_metadata,
)
from .model import CanonicalModuleCorpus, MetadataValidation, ModuleMetadata

__all__ = (
    "CANONICAL_MODULE_CORPUS",
    "CanonicalModuleCorpus",
    "MetadataError",
    "MetadataFailure",
    "MetadataValidation",
    "ModuleMetadata",
    "load_canonical_module_corpus",
    "load_module_metadata",
    "validate_module_metadata",
)
