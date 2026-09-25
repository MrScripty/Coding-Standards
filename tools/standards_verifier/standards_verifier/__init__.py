"""Strict, repository-local standards verification engine."""

from .cli import run_complete_verification
from .diagnostics import EngineError
from .model import CompleteVerificationResult
from .suite_inputs import (
    suite_input_projection_bytes,
    suite_input_projection_bytes_from_content,
    write_suite_input_projection,
)

from .entrypoints import (
    git_reachability_main,
    repository_graph_main,
    verifier_main,
)

__all__ = (
    "CompleteVerificationResult",
    "EngineError",
    "git_reachability_main",
    "repository_graph_main",
    "run_complete_verification",
    "suite_input_projection_bytes",
    "suite_input_projection_bytes_from_content",
    "verifier_main",
    "write_suite_input_projection",
)
