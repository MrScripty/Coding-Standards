from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs
from ..paths import contained_file
from .literal_matching import (
    MatchCase,
    literal_key,
    parse_match_case,
    validate_literal_sets,
)


def _string_list(value: Any, field: str, suite: str, check: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise EngineError(
            Diagnostic(
                code="CONFIG.STRING_LIST",
                outcome="invalid",
                message="field must be an array of non-empty strings",
                suite=suite,
                check=check,
                field=field,
            )
        )
    if len(set(value)) != len(value):
        raise EngineError(
            Diagnostic(
                code="CONFIG.DUPLICATE_VALUE",
                outcome="invalid",
                message="field contains duplicate values",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return tuple(value)


@dataclass(frozen=True, slots=True)
class TextCheck:
    id: str
    path: str
    required: tuple[str, ...]
    prohibited: tuple[str, ...]
    match_case: MatchCase

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        return present_inputs("content", self.path)

    def run(self, context: CheckContext) -> list[Diagnostic]:
        root = context.repo_root
        if not isinstance(root, Path):
            raise TypeError("check context repository root must be a Path")
        source = contained_file(root, self.path, suite=context.suite_id, check=self.id)
        try:
            content = source.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise EngineError(
                Diagnostic(
                    code="INPUT.INVALID_UTF8",
                    outcome="invalid",
                    message=str(error),
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                )
            ) from error

        searchable = literal_key(content, self.match_case)
        diagnostics = []
        for literal in self.required:
            if literal_key(literal, self.match_case) not in searchable:
                diagnostics.append(
                    Diagnostic(
                        code="ASSERT.TEXT_REQUIRED",
                        outcome="invalid",
                        message="required literal is absent",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        expected=literal,
                        observed="absent",
                    )
                )
        for literal in self.prohibited:
            if literal_key(literal, self.match_case) in searchable:
                diagnostics.append(
                    Diagnostic(
                        code="ASSERT.TEXT_PROHIBITED",
                        outcome="invalid",
                        message="prohibited literal is present",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        expected="absent",
                        observed=literal,
                    )
                )
        return diagnostics


def parse_text_check(raw: dict[str, Any], suite_id: str) -> TextCheck:
    allowed = {"id", "type", "path", "required", "prohibited", "match_case"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                code="CONFIG.UNKNOWN_FIELD",
                outcome="invalid",
                message="text check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    path = raw.get("path")
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
    required = _string_list(raw.get("required", []), "required", suite_id, check_id)
    prohibited = _string_list(
        raw.get("prohibited", []), "prohibited", suite_id, check_id
    )
    match_case = parse_match_case(
        raw.get("match_case", "sensitive"),
        suite=suite_id,
        check=check_id,
    )
    validate_literal_sets(
        required,
        prohibited,
        match_case,
        suite=suite_id,
        check=check_id,
    )
    if not required and not prohibited:
        raise EngineError(
            Diagnostic(
                "CONFIG.EMPTY_CHECK",
                "invalid",
                "text check has no assertions",
                suite=suite_id,
                check=check_id,
            )
        )
    return TextCheck(check_id, path, required, prohibited, match_case)
