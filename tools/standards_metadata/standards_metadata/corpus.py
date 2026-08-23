from __future__ import annotations

from pathlib import Path

from .loader import CANONICAL_MODULE_CORPUS, load_canonical_module_corpus
from .model import CanonicalStandardsCorpus
from .policy_units import POLICY_UNIT_REGISTRY, load_policy_unit_corpus


def load_canonical_standards_corpus(
    root: Path,
    module_registry: str = CANONICAL_MODULE_CORPUS,
    policy_unit_registry: str = POLICY_UNIT_REGISTRY,
) -> CanonicalStandardsCorpus:
    modules = load_canonical_module_corpus(root, module_registry)
    policy_units = load_policy_unit_corpus(root, modules, policy_unit_registry)
    return CanonicalStandardsCorpus(modules, policy_units)
