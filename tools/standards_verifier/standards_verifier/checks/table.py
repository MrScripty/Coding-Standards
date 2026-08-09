from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file
from .predicates import Predicate, parse_predicate


def _strings(value: Any, field: str, suite: str, check: str) -> tuple[str, ...]:
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
                "field must contain unique non-empty strings",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return tuple(value)


@dataclass(frozen=True, slots=True)
class Projection:
    columns: tuple[str, ...]
    order: str
    expected: tuple[tuple[str, ...], ...]
    where: Predicate | None = None
    split_field: str | None = None
    split_delimiter: str | None = None


def read_table_rows(
    root: Path,
    path: str,
    header: tuple[str, ...],
    *,
    suite: str,
    check: str,
) -> list[dict[str, str]]:
    source = contained_file(root, path, suite=suite, check=check)
    try:
        with source.open("r", encoding="utf-8", newline="") as handle:
            values = list(csv.reader(handle, delimiter="\t"))
    except UnicodeDecodeError as error:
        raise EngineError(
            Diagnostic(
                "INPUT.INVALID_UTF8",
                "invalid",
                str(error),
                suite=suite,
                check=check,
                path=path,
            )
        ) from error
    if not values:
        raise EngineError(
            Diagnostic(
                "TABLE.EMPTY",
                "invalid",
                "table requires an exact header",
                suite=suite,
                check=check,
                path=path,
            )
        )
    if tuple(values[0]) != header:
        raise EngineError(
            Diagnostic(
                "TABLE.HEADER_CONTRACT",
                "invalid",
                "table header does not match the configured header",
                suite=suite,
                check=check,
                path=path,
                expected="\t".join(header),
                observed="\t".join(values[0]),
            )
        )

    rows = []
    for line_number, row_values in enumerate(values[1:], start=2):
        if len(row_values) != len(header):
            raise EngineError(
                Diagnostic(
                    "TABLE.ROW_WIDTH",
                    "invalid",
                    "table row width does not match the header",
                    suite=suite,
                    check=check,
                    path=path,
                    row=line_number,
                    expected=str(len(header)),
                    observed=str(len(row_values)),
                )
            )
        rows.append(dict(zip(header, row_values, strict=True)))
    return rows


def project_table_rows(
    rows: list[dict[str, str]], projection: Projection
) -> tuple[tuple[str, ...], ...]:
    projected = []
    for row in rows:
        if projection.where is not None and not projection.where.evaluate(row):
            continue
        selected = tuple(row[field] for field in projection.columns)
        if projection.split_field is None:
            projected.append(selected)
            continue
        split_index = projection.columns.index(projection.split_field)
        parts = selected[split_index].split(projection.split_delimiter)
        for part in parts:
            expanded = list(selected)
            expanded[split_index] = part
            projected.append(tuple(expanded))
    if projection.order == "lexical":
        projected.sort()
    return tuple(projected)


@dataclass(frozen=True, slots=True)
class TableCheck:
    id: str
    path: str
    header: tuple[str, ...]
    row_count: int | None
    non_empty: tuple[str, ...]
    domains: dict[str, tuple[str, ...]]
    unique: tuple[tuple[str, ...], ...]
    projections: tuple[Projection, ...]

    def run(self, context: CheckContext) -> list[Diagnostic]:
        root = context.repo_root
        if not isinstance(root, Path):
            raise TypeError("check context repository root must be a Path")
        rows = read_table_rows(
            root,
            self.path,
            self.header,
            suite=context.suite_id,
            check=self.id,
        )

        diagnostics: list[Diagnostic] = []
        if self.row_count is not None and len(rows) != self.row_count:
            diagnostics.append(
                Diagnostic(
                    "ASSERT.TABLE_ROW_COUNT",
                    "invalid",
                    "table row count does not match",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    expected=str(self.row_count),
                    observed=str(len(rows)),
                )
            )

        for line_number, row in enumerate(rows, start=2):
            for field in self.non_empty:
                if not row[field]:
                    diagnostics.append(
                        Diagnostic(
                            "ASSERT.TABLE_EMPTY_VALUE",
                            "invalid",
                            "table field must not be empty",
                            suite=context.suite_id,
                            check=self.id,
                            path=self.path,
                            row=line_number,
                            field=field,
                        )
                    )
            for field, domain in self.domains.items():
                if row[field] not in domain:
                    diagnostics.append(
                        Diagnostic(
                            "ASSERT.TABLE_DOMAIN",
                            "invalid",
                            "table value is outside its literal domain",
                            suite=context.suite_id,
                            check=self.id,
                            path=self.path,
                            row=line_number,
                            field=field,
                            expected=",".join(domain),
                            observed=row[field],
                        )
                    )

        for key in self.unique:
            seen: dict[tuple[str, ...], int] = {}
            for line_number, row in enumerate(rows, start=2):
                value = tuple(row[field] for field in key)
                if value in seen:
                    diagnostics.append(
                        Diagnostic(
                            "ASSERT.TABLE_DUPLICATE_KEY",
                            "invalid",
                            "table key is duplicated",
                            suite=context.suite_id,
                            check=self.id,
                            path=self.path,
                            row=line_number,
                            field=",".join(key),
                            expected="unique",
                            observed="\t".join(value),
                        )
                    )
                else:
                    seen[value] = line_number

        for projection in self.projections:
            actual = project_table_rows(rows, projection)
            if actual != projection.expected:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.TABLE_PROJECTION",
                        "invalid",
                        "table projection does not match",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        expected=repr(projection.expected),
                        observed=repr(actual),
                    )
                )
        return diagnostics


def _projection(
    raw: Any, header: tuple[str, ...], suite: str, check: str
) -> Projection:
    if not isinstance(raw, dict):
        raise EngineError(
            Diagnostic(
                "CONFIG.PROJECTION",
                "invalid",
                "projection must be a TOML table",
                suite=suite,
                check=check,
            )
        )
    allowed = {"columns", "order", "expected", "where", "split"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "projection contains unknown fields",
                suite=suite,
                check=check,
                field=sorted(unknown)[0],
            )
        )
    columns = _strings(raw.get("columns"), "columns", suite, check)
    unknown_columns = set(columns) - set(header)
    if unknown_columns:
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_COLUMN",
                "invalid",
                "projection references an unknown column",
                suite=suite,
                check=check,
                field=sorted(unknown_columns)[0],
            )
        )
    order = raw.get("order")
    if order not in {"source", "lexical"}:
        raise EngineError(
            Diagnostic(
                "CONFIG.PROJECTION_ORDER",
                "invalid",
                "projection order must be source or lexical",
                suite=suite,
                check=check,
                observed=str(order),
            )
        )
    raw_expected = raw.get("expected")
    if not isinstance(raw_expected, list) or any(
        not isinstance(row, list)
        or len(row) != len(columns)
        or any(not isinstance(value, str) for value in row)
        for row in raw_expected
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.PROJECTION_EXPECTED",
                "invalid",
                "projection expected rows must match selected column width",
                suite=suite,
                check=check,
            )
        )
    where = None
    if "where" in raw:
        where = parse_predicate(raw["where"], suite, check)
        unknown_fields = where.fields() - set(header)
        if unknown_fields:
            raise EngineError(
                Diagnostic(
                    "CONFIG.TABLE_COLUMN",
                    "invalid",
                    "projection predicate references an unknown column",
                    suite=suite,
                    check=check,
                    field=sorted(unknown_fields)[0],
                )
            )
    split_field = None
    split_delimiter = None
    if "split" in raw:
        split = raw["split"]
        if (
            not isinstance(split, dict)
            or set(split) != {"field", "delimiter"}
            or split.get("field") not in columns
            or not isinstance(split.get("delimiter"), str)
            or not split["delimiter"]
        ):
            raise EngineError(
                Diagnostic(
                    "CONFIG.PROJECTION_SPLIT",
                    "invalid",
                    "split requires one selected field and a non-empty delimiter",
                    suite=suite,
                    check=check,
                )
            )
        split_field = split["field"]
        split_delimiter = split["delimiter"]
    return Projection(
        columns,
        order,
        tuple(tuple(row) for row in raw_expected),
        where,
        split_field,
        split_delimiter,
    )


def parse_table_check(raw: dict[str, Any], suite_id: str) -> TableCheck:
    allowed = {
        "id",
        "type",
        "path",
        "header",
        "row_count",
        "non_empty",
        "domains",
        "unique",
        "projections",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "table check contains unknown fields",
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
    header = _strings(raw.get("header"), "header", suite_id, check_id)
    row_count = raw.get("row_count")
    if row_count is not None and (
        not isinstance(row_count, int) or isinstance(row_count, bool) or row_count < 0
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.ROW_COUNT",
                "invalid",
                "row_count must be a non-negative integer",
                suite=suite_id,
                check=check_id,
            )
        )
    non_empty = tuple(raw.get("non_empty", []))
    if any(not isinstance(field, str) for field in non_empty) or len(
        set(non_empty)
    ) != len(non_empty):
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_COLUMNS",
                "invalid",
                "non_empty must contain unique column names",
                suite=suite_id,
                check=check_id,
            )
        )
    raw_domains = raw.get("domains", {})
    if not isinstance(raw_domains, dict):
        raise EngineError(
            Diagnostic(
                "CONFIG.DOMAINS",
                "invalid",
                "domains must be a TOML table",
                suite=suite_id,
                check=check_id,
            )
        )
    domains = {
        field: _strings(values, f"domains.{field}", suite_id, check_id)
        for field, values in raw_domains.items()
    }
    raw_unique = raw.get("unique", [])
    if not isinstance(raw_unique, list):
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_UNIQUE",
                "invalid",
                "unique must be an array of column arrays",
                suite=suite_id,
                check=check_id,
            )
        )
    unique = tuple(
        _strings(key, "unique", suite_id, check_id) for key in raw_unique
    )
    referenced = set(non_empty) | set(domains)
    referenced.update(field for key in unique for field in key)
    unknown_columns = referenced - set(header)
    if unknown_columns:
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_COLUMN",
                "invalid",
                "table assertion references an unknown column",
                suite=suite_id,
                check=check_id,
                field=sorted(unknown_columns)[0],
            )
        )
    if len(set(unique)) != len(unique):
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_UNIQUE",
                "invalid",
                "unique column keys must not be duplicated",
                suite=suite_id,
                check=check_id,
            )
        )
    raw_projections = raw.get("projections", [])
    if not isinstance(raw_projections, list):
        raise EngineError(
            Diagnostic(
                "CONFIG.PROJECTIONS",
                "invalid",
                "projections must be an array of TOML tables",
                suite=suite_id,
                check=check_id,
            )
        )
    projections = tuple(
        _projection(value, header, suite_id, check_id) for value in raw_projections
    )
    if (
        row_count is None
        and not non_empty
        and not domains
        and not unique
        and not projections
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.EMPTY_CHECK",
                "invalid",
                "table check requires at least one assertion beyond its header",
                suite=suite_id,
                check=check_id,
            )
        )
    return TableCheck(
        check_id,
        path,
        header,
        row_count,
        non_empty,
        domains,
        unique,
        projections,
    )
