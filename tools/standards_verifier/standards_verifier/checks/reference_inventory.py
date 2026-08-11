from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file
from .table import read_table_rows


def _header(value: Any, field: str, suite: str, check: str) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.STRING_LIST",
                "invalid",
                "header must contain unique non-empty strings",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return tuple(value)


def _string(value: Any, field: str, suite: str, check: str) -> str:
    if not isinstance(value, str) or not value:
        raise EngineError(
            Diagnostic(
                "CONFIG.STRING",
                "invalid",
                "field must be a non-empty string",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return value


def _paths(
    rows: list[dict[str, str]],
    column: str,
    *,
    path: str,
    suite: str,
    check: str,
) -> tuple[str, ...]:
    values = tuple(row[column] for row in rows)
    seen: set[str] = set()
    for line_number, value in enumerate(values, start=2):
        if not value:
            raise EngineError(
                Diagnostic(
                    "TABLE.EMPTY_PATH",
                    "invalid",
                    "inventory path must not be empty",
                    suite=suite,
                    check=check,
                    path=path,
                    row=line_number,
                    field=column,
                )
            )
        if value in seen:
            raise EngineError(
                Diagnostic(
                    "TABLE.DUPLICATE_PATH",
                    "invalid",
                    "inventory path must occur exactly once",
                    suite=suite,
                    check=check,
                    path=path,
                    row=line_number,
                    field=column,
                    observed=value,
                )
            )
        seen.add(value)
    return values


@dataclass(frozen=True, slots=True)
class ReferenceInventoryCheck:
    id: str
    candidates_path: str
    candidates_header: tuple[str, ...]
    candidate_path_column: str
    manifest_path: str
    manifest_header: tuple[str, ...]
    manifest_path_column: str
    literal: str

    def run(self, context: CheckContext) -> list[Diagnostic]:
        candidate_rows = read_table_rows(
            context.repo_root,
            self.candidates_path,
            self.candidates_header,
            suite=context.suite_id,
            check=self.id,
        )
        manifest_rows = read_table_rows(
            context.repo_root,
            self.manifest_path,
            self.manifest_header,
            suite=context.suite_id,
            check=self.id,
        )
        candidates = _paths(
            candidate_rows,
            self.candidate_path_column,
            path=self.candidates_path,
            suite=context.suite_id,
            check=self.id,
        )
        manifested = _paths(
            manifest_rows,
            self.manifest_path_column,
            path=self.manifest_path,
            suite=context.suite_id,
            check=self.id,
        )

        selected: set[str] = set()
        for display_path in candidates:
            source = contained_file(
                context.repo_root,
                display_path,
                suite=context.suite_id,
                check=self.id,
            )
            try:
                content = source.read_text(encoding="utf-8")
            except UnicodeDecodeError as error:
                raise EngineError(
                    Diagnostic(
                        "INPUT.INVALID_UTF8",
                        "invalid",
                        str(error),
                        suite=context.suite_id,
                        check=self.id,
                        path=display_path,
                    )
                ) from error
            if self.literal in content:
                selected.add(display_path)

        for display_path in manifested:
            contained_file(
                context.repo_root,
                display_path,
                suite=context.suite_id,
                check=self.id,
            )
        expected = set(manifested)
        if selected == expected:
            return []
        return [
            Diagnostic(
                "ASSERT.REFERENCE_INVENTORY",
                "invalid",
                "literal-selected candidate paths do not match the manifest",
                suite=context.suite_id,
                check=self.id,
                path=self.manifest_path,
                expected=",".join(sorted(expected)),
                observed=",".join(sorted(selected)),
            )
        ]


def parse_reference_inventory_check(
    raw: dict[str, Any], suite_id: str
) -> ReferenceInventoryCheck:
    allowed = {
        "id",
        "type",
        "candidates_path",
        "candidates_header",
        "candidate_path_column",
        "manifest_path",
        "manifest_header",
        "manifest_path_column",
        "literal",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "reference_inventory check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    if not isinstance(check_id, str) or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    candidates_header = _header(
        raw.get("candidates_header"), "candidates_header", suite_id, check_id
    )
    manifest_header = _header(
        raw.get("manifest_header"), "manifest_header", suite_id, check_id
    )
    candidate_path_column = _string(
        raw.get("candidate_path_column"),
        "candidate_path_column",
        suite_id,
        check_id,
    )
    manifest_path_column = _string(
        raw.get("manifest_path_column"),
        "manifest_path_column",
        suite_id,
        check_id,
    )
    if candidate_path_column not in candidates_header:
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_COLUMN",
                "invalid",
                "candidate path column is absent from its header",
                suite=suite_id,
                check=check_id,
                field="candidate_path_column",
                observed=candidate_path_column,
            )
        )
    if manifest_path_column not in manifest_header:
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_COLUMN",
                "invalid",
                "manifest path column is absent from its header",
                suite=suite_id,
                check=check_id,
                field="manifest_path_column",
                observed=manifest_path_column,
            )
        )
    return ReferenceInventoryCheck(
        check_id,
        _string(raw.get("candidates_path"), "candidates_path", suite_id, check_id),
        candidates_header,
        candidate_path_column,
        _string(raw.get("manifest_path"), "manifest_path", suite_id, check_id),
        manifest_header,
        manifest_path_column,
        _string(raw.get("literal"), "literal", suite_id, check_id),
    )
