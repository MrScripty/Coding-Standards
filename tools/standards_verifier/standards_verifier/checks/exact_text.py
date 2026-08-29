from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs
from ..paths import contained_file


@dataclass(frozen=True, slots=True)
class ExactTextCheck:
    id: str
    path: str
    expected: str

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        return present_inputs("content", self.path)

    def run(self, context: CheckContext) -> list[Diagnostic]:
        source = contained_file(
            context.repo_root,
            self.path,
            suite=context.suite_id,
            check=self.id,
        )
        observed = source.read_bytes()
        expected = self.expected.encode("utf-8")
        if observed == expected:
            return []

        mismatch = next(
            (
                offset
                for offset, (observed_byte, expected_byte) in enumerate(
                    zip(observed, expected, strict=False)
                )
                if observed_byte != expected_byte
            ),
            min(len(observed), len(expected)),
        )
        return [
            Diagnostic(
                code="ASSERT.EXACT_TEXT",
                outcome="invalid",
                message="file bytes do not match inline expected UTF-8 content",
                suite=context.suite_id,
                check=self.id,
                path=self.path,
                expected=f"{len(expected)} bytes",
                observed=f"{len(observed)} bytes; first mismatch at byte {mismatch}",
            )
        ]


def parse_exact_text_check(raw: dict[str, Any], suite_id: str) -> ExactTextCheck:
    allowed = {"id", "type", "path", "expected"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                code="CONFIG.UNKNOWN_FIELD",
                outcome="invalid",
                message="exact_text check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )

    check_id = raw.get("id")
    path = raw.get("path")
    expected = raw.get("expected")
    if not isinstance(check_id, str) or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    if not isinstance(path, str) or not path:
        raise EngineError(
            Diagnostic(
                "CONFIG.PATH",
                "invalid",
                "path must be a non-empty string",
                suite=suite_id,
                check=check_id,
            )
        )
    if not isinstance(expected, str):
        raise EngineError(
            Diagnostic(
                "CONFIG.EXACT_TEXT_EXPECTED",
                "invalid",
                "expected must be a string",
                suite=suite_id,
                check=check_id,
                field="expected",
            )
        )
    return ExactTextCheck(check_id, path, expected)
