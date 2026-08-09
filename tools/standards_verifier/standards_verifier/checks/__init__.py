from __future__ import annotations

from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import Check
from .acceptance_claims import parse_acceptance_claims_check
from .decision import parse_decision_check
from .exact_text import parse_exact_text_check
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
    if kind == "exact_text":
        return parse_exact_text_check(raw, suite_id)
    if kind == "table":
        return parse_table_check(raw, suite_id)
    if kind == "acceptance_claims":
        return parse_acceptance_claims_check(raw, suite_id)
    if kind == "relation":
        return parse_relation_check(raw, suite_id)
    raise EngineError(
        Diagnostic(
            code="CONFIG.UNKNOWN_CHECK",
            outcome="invalid",
            message="check type is not supported",
            suite=suite_id,
            observed=str(kind),
        )
    )
