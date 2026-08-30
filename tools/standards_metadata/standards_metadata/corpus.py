from __future__ import annotations

from .loader import CANONICAL_MODULE_CORPUS, load_canonical_module_corpus
from .model import CanonicalStandardsCorpus
from .policy_units import POLICY_UNIT_REGISTRY, load_policy_unit_corpus
from .source import ContentSourceInput, content_source


def load_canonical_standards_corpus(
    source: ContentSourceInput,
    module_registry: str = CANONICAL_MODULE_CORPUS,
    policy_unit_registry: str = POLICY_UNIT_REGISTRY,
) -> CanonicalStandardsCorpus:
    selected_source = content_source(source)
    modules = load_canonical_module_corpus(selected_source, module_registry)
    policy_units = load_policy_unit_corpus(
        selected_source,
        modules,
        policy_unit_registry,
    )
    return CanonicalStandardsCorpus(modules, policy_units)
