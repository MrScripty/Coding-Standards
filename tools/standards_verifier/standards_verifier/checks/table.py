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


@dataclass(frozen=True, slots=True)
class ProjectedTableSource:
    path: str
    header: tuple[str, ...]
    projection: Projection


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


def read_projected_table_rows(
    context: CheckContext,
    check: str,
    source: ProjectedTableSource,
) -> tuple[tuple[str, ...], ...]:
    rows = read_table_rows(
        context.repo_root,
        source.path,
        source.header,
        suite=context.suite_id,
        check=check,
    )
    return project_table_rows(rows, source.projection)


def _parse_projection_contract(
    raw: Any,
    header: tuple[str, ...],
    suite: str,
    check: str,
    *,
    allowed: set[str],
    expected_required: bool,
    label: str | None,
    projection_name: str,
    predicate_name: str,
) -> Projection:
    if not isinstance(raw, dict):
        raise EngineError(
            Diagnostic(
                "CONFIG.PROJECTION",
                "invalid",
                f"{projection_name} must be a TOML table",
                suite=suite,
                check=check,
                field=label,
            )
        )
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                f"{projection_name} contains unknown fields",
                suite=suite,
                check=check,
                field=(
                    f"{label}.{sorted(unknown)[0]}"
                    if label is not None
                    else sorted(unknown)[0]
                ),
            )
        )
    columns_field = f"{label}.columns" if label is not None else "columns"
    columns = _strings(raw.get("columns"), columns_field, suite, check)
    unknown_columns = set(columns) - set(header)
    if unknown_columns:
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_COLUMN",
                "invalid",
                f"{projection_name} references an unknown column",
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
                f"{projection_name} order must be source or lexical",
                suite=suite,
                check=check,
                field=label,
                observed=str(order),
            )
        )
    expected: tuple[tuple[str, ...], ...] = ()
    if expected_required:
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
        expected = tuple(tuple(row) for row in raw_expected)
    where = None
    if "where" in raw:
        where = parse_predicate(raw["where"], suite, check)
        unknown_fields = where.fields() - set(header)
        if unknown_fields:
            raise EngineError(
                Diagnostic(
                    "CONFIG.TABLE_COLUMN",
                    "invalid",
                    f"{predicate_name} references an unknown column",
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
                    field=label,
                )
            )
        split_field = split["field"]
        split_delimiter = split["delimiter"]
    return Projection(
        columns,
        order,
        expected,
        where,
        split_field,
        split_delimiter,
    )


def parse_projected_table_source(
    raw: Any,
    suite: str,
    check: str,
    label: str,
    *,
    invalid_code: str,
    source_name: str,
    projection_name: str,
    predicate_name: str,
) -> ProjectedTableSource:
    if not isinstance(raw, dict):
        raise EngineError(
            Diagnostic(
                invalid_code,
                "invalid",
                f"{source_name} must be a TOML table",
                suite=suite,
                check=check,
                field=label,
            )
        )
    allowed = {"path", "header", "columns", "order", "where", "split"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                f"{source_name} contains unknown fields",
                suite=suite,
                check=check,
                field=f"{label}.{sorted(unknown)[0]}",
            )
        )
    path = raw.get("path")
    if not isinstance(path, str) or not path:
        raise EngineError(
            Diagnostic(
                "CONFIG.PATH",
                "invalid",
                f"{source_name} path must be a non-empty string",
                suite=suite,
                check=check,
                field=label,
            )
        )
    header = _strings(raw.get("header"), f"{label}.header", suite, check)
    projection = _parse_projection_contract(
        raw,
        header,
        suite,
        check,
        allowed=allowed,
        expected_required=False,
        label=label,
        projection_name=projection_name,
        predicate_name=predicate_name,
    )
    return ProjectedTableSource(path, header, projection)
