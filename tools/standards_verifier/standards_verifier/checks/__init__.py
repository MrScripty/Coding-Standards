from __future__ import annotations

from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import Check
from .acceptance_claims import parse_acceptance_claims_check
from .decision import parse_decision_check
from .edge_dispositions import parse_edge_dispositions_check
from .exact_text import parse_exact_text_check
from .git_index_paths import parse_git_index_paths_check
from .inclusion import parse_inclusion_check
from .keyed_relation import parse_keyed_relation_check
from .line_budget import parse_line_budget_check
from .markdown_heading_cardinality import parse_markdown_heading_cardinality_check
from .markdown_headings import parse_markdown_headings_check
from .markdown_links import parse_markdown_links_check
from .markdown_section_text import parse_markdown_section_text_check
from .markdown_structure import parse_markdown_structure_check
from .metadata import parse_metadata_graph_check
from .numeric_lifecycle import parse_numeric_lifecycle_check
from .path_state import parse_path_state_check
from .reference_inventory import parse_reference_inventory_check
from .relation import parse_relation_check
from .table import parse_table_check
from .text import parse_text_check


def parse_check(raw: Any, suite_id: str) -> Check:
    if not isinstance(raw, dict):
        raise EngineError(
            Diagnostic(
                code="CONFIG.CHECK_TYPE",
                outcome="invalid",
                message="each check must be a TOML table",
                suite=suite_id,
            )
        )
    kind = raw.get("type")
    if kind == "text":
        return parse_text_check(raw, suite_id)
    if kind == "decision":
        return parse_decision_check(raw, suite_id)
    if kind == "edge_dispositions":
        return parse_edge_dispositions_check(raw, suite_id)
    if kind == "exact_text":
        return parse_exact_text_check(raw, suite_id)
    if kind == "git_index_paths":
        return parse_git_index_paths_check(raw, suite_id)
    if kind == "inclusion":
        return parse_inclusion_check(raw, suite_id)
    if kind == "keyed_relation":
        return parse_keyed_relation_check(raw, suite_id)
    if kind == "markdown_links":
        return parse_markdown_links_check(raw, suite_id)
    if kind == "markdown_heading_cardinality":
        return parse_markdown_heading_cardinality_check(raw, suite_id)
    if kind == "markdown_headings":
        return parse_markdown_headings_check(raw, suite_id)
    if kind == "markdown_section_text":
        return parse_markdown_section_text_check(raw, suite_id)
    if kind == "markdown_structure":
        return parse_markdown_structure_check(raw, suite_id)
    if kind == "line_budget":
        return parse_line_budget_check(raw, suite_id)
    if kind == "path_state":
        return parse_path_state_check(raw, suite_id)
    if kind == "metadata_graph":
        return parse_metadata_graph_check(raw, suite_id)
    if kind == "reference_inventory":
        return parse_reference_inventory_check(raw, suite_id)
    if kind == "table":
        return parse_table_check(raw, suite_id)
    if kind == "acceptance_claims":
        return parse_acceptance_claims_check(raw, suite_id)
    if kind == "relation":
        return parse_relation_check(raw, suite_id)
    if kind == "numeric_audit_lifecycle":
        return parse_numeric_lifecycle_check(raw, suite_id)
    raise EngineError(
        Diagnostic(
            code="CONFIG.UNKNOWN_CHECK",
            outcome="invalid",
            message="check type is not supported",
            suite=suite_id,
            observed=str(kind),
        )
    )
