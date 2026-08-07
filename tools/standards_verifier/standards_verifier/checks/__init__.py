from __future__ import annotations

from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import Check
from .decision import parse_decision_check
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
    raise EngineError(
        Diagnostic(
            code="CONFIG.UNKNOWN_CHECK",
            outcome="invalid",
            message="check type is not supported",
            suite=suite_id,
            observed=str(kind),
        )
    )
