"""Strict, repository-local standards verification engine."""

from .cli import run_complete_verification
from .model import CompleteVerificationResult

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
    "CompleteVerificationResult",
    "git_reachability_main",
    "numeric_audit_main",
    "numeric_retirements_main",
    "repository_graph_main",
    "run_complete_verification",
    "verifier_main",
)
