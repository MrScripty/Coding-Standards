from __future__ import annotations

from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import Check
from .contract_projection import parse_contract_projection_check
from .markdown_link_coverage import parse_markdown_link_coverage_check
from .markdown_links import parse_markdown_links_check
from .markdown_targets import parse_markdown_targets_check
from .metadata import parse_metadata_graph_check
from .metadata_route import parse_metadata_route_check
from .plan_contract import parse_plan_contract_check
from .policy_impact import parse_policy_impact_check
from .python_package_contract import parse_python_package_contract_check


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
    if kind == "contract_projection":
        return parse_contract_projection_check(raw, suite_id)
    if kind == "markdown_targets":
        return parse_markdown_targets_check(raw, suite_id)
    if kind == "markdown_links":
        return parse_markdown_links_check(raw, suite_id)
    if kind == "markdown_link_coverage":
        return parse_markdown_link_coverage_check(raw, suite_id)
    if kind == "plan_contract":
        return parse_plan_contract_check(raw, suite_id)
    if kind == "policy_impact":
        return parse_policy_impact_check(raw, suite_id)
    if kind == "python_package_contract":
        return parse_python_package_contract_check(raw, suite_id)
    if kind == "metadata_graph":
        return parse_metadata_graph_check(raw, suite_id)
    if kind == "metadata_route":
        return parse_metadata_route_check(raw, suite_id)
    raise EngineError(
        Diagnostic(
            code="CONFIG.UNKNOWN_CHECK",
            outcome="invalid",
            message="check type is not supported",
            suite=suite_id,
            observed=str(kind),
        )
    )
