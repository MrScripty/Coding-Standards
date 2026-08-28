"""Strict, repository-local standards verification engine."""

from .entrypoints import (
    generated_artifacts_main,
    git_reachability_main,
    numeric_audit_main,
    numeric_retirements_main,
    repository_graph_main,
    verifier_main,
)

__all__ = (
    "generated_artifacts_main",
    "git_reachability_main",
    "numeric_audit_main",
    "numeric_retirements_main",
    "repository_graph_main",
    "verifier_main",
)
