from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs
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


@dataclass(frozen=True, slots=True)
class MemberScope:
    source: ProjectedTableSource
    key: str


@dataclass(frozen=True, slots=True)
class RowConstraint:
    id: str
    where: Predicate | None
    require: Predicate


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


@dataclass(frozen=True, slots=True)
class TableCheck:
    id: str
    path: str
    header: tuple[str, ...]
    non_empty: tuple[str, ...]
    domains: dict[str, tuple[str, ...]]
    unique: tuple[tuple[str, ...], ...]
    projections: tuple[Projection, ...]
    where: Predicate | None
    members: MemberScope | None
    row_constraints: tuple[RowConstraint, ...]

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        declarations = list(present_inputs("table", self.path))
        if self.members is not None:
            declarations.extend(present_inputs("members", self.members.source.path))
        return tuple(declarations)

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
        if self.members is None:
            scoped_rows = [
                (line_number, row)
                for line_number, row in enumerate(rows, start=2)
                if self.where is None or self.where.evaluate(row)
            ]
        else:
            scoped_rows, scope_diagnostics = self._resolve_members(root, rows, context)
            diagnostics.extend(scope_diagnostics)

        for line_number, row in scoped_rows:
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
            for line_number, row in scoped_rows:
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

        for constraint in self.row_constraints:
            for line_number, row in scoped_rows:
                if constraint.where is not None and not constraint.where.evaluate(row):
                    continue
                if constraint.require.evaluate(row):
                    continue
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.TABLE_ROW_CONSTRAINT",
                        "invalid",
                        "table row does not satisfy the named constraint",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=line_number,
                        field=constraint.id,
                        expected="constraint satisfied",
                        observed="constraint violated",
                    )
                )

        for projection in self.projections:
            actual = project_table_rows([row for _, row in scoped_rows], projection)
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

    def _resolve_members(
        self,
        root: Path,
        rows: list[dict[str, str]],
        context: CheckContext,
    ) -> tuple[list[tuple[int, dict[str, str]]], list[Diagnostic]]:
        if self.members is None:
            raise TypeError("member scope is required")
        member_rows = read_table_rows(
            root,
            self.members.source.path,
            self.members.source.header,
            suite=context.suite_id,
            check=self.id,
        )
        projected = project_table_rows(member_rows, self.members.source.projection)
        diagnostics: list[Diagnostic] = []
        if not projected:
            diagnostics.append(
                Diagnostic(
                    "ASSERT.TABLE_MEMBERS_EMPTY",
                    "invalid",
                    "table member scope must select at least one identity",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.members.source.path,
                    expected="nonempty unique members",
                    observed="empty",
                )
            )
            return [], diagnostics

        members: list[str] = []
        seen_members: set[str] = set()
        for (member,) in projected:
            if not member:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.TABLE_MEMBER_EMPTY",
                        "invalid",
                        "table member identity must not be empty",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.members.source.path,
                        expected="nonempty member",
                        observed="empty",
                    )
                )
                continue
            if member in seen_members:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.TABLE_MEMBER_DUPLICATE",
                        "invalid",
                        "table member identity is duplicated",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.members.source.path,
                        field=self.members.key,
                        expected="unique members",
                        observed=member,
                    )
                )
                continue
            seen_members.add(member)
            members.append(member)

        canonical: dict[str, list[tuple[int, dict[str, str]]]] = {}
        for line_number, row in enumerate(rows, start=2):
            canonical.setdefault(row[self.members.key], []).append((line_number, row))

        scoped_rows: list[tuple[int, dict[str, str]]] = []
        for member in members:
            matches = canonical.get(member, [])
            if not matches:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.TABLE_MEMBER_MISSING",
                        "invalid",
                        "declared table member has no canonical row",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        field=self.members.key,
                        expected=member,
                        observed="absent",
                    )
                )
                continue
            if len(matches) != 1:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.TABLE_MEMBER_ROW_DUPLICATE",
                        "invalid",
                        "declared table member resolves to multiple canonical rows",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        field=self.members.key,
                        expected="one canonical row",
                        observed=f"{member}:{len(matches)}",
                    )
                )
                continue
            scoped_rows.append(matches[0])
        return scoped_rows, diagnostics


def _projection(
    raw: Any, header: tuple[str, ...], suite: str, check: str
) -> Projection:
    return _parse_projection_contract(
        raw,
        header,
        suite,
        check,
        allowed={"columns", "order", "expected", "where", "split"},
        expected_required=True,
        label=None,
        projection_name="projection",
        predicate_name="projection predicate",
    )


def _row_constraint(
    raw: Any, header: tuple[str, ...], suite: str, check: str
) -> RowConstraint:
    if not isinstance(raw, dict):
        raise EngineError(
            Diagnostic(
                "CONFIG.ROW_CONSTRAINT",
                "invalid",
                "row constraint must be a TOML table",
                suite=suite,
                check=check,
            )
        )
    allowed = {"id", "where", "require"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "row constraint contains unknown fields",
                suite=suite,
                check=check,
                field=sorted(unknown)[0],
            )
        )
    constraint_id = raw.get("id")
    if not isinstance(constraint_id, str) or not constraint_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.ROW_CONSTRAINT_ID",
                "invalid",
                "row constraint id must be a non-empty string",
                suite=suite,
                check=check,
                field="id",
            )
        )
    where = None
    if "where" in raw:
        where = parse_predicate(raw["where"], suite, check)
    if "require" not in raw:
        raise EngineError(
            Diagnostic(
                "CONFIG.ROW_CONSTRAINT_REQUIRE",
                "invalid",
                "row constraint requires one predicate",
                suite=suite,
                check=check,
                field=constraint_id,
            )
        )
    require = parse_predicate(raw["require"], suite, check)
    referenced = require.fields()
    if where is not None:
        referenced |= where.fields()
    unknown_columns = referenced - set(header)
    if unknown_columns:
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_COLUMN",
                "invalid",
                "row constraint references an unknown column",
                suite=suite,
                check=check,
                field=sorted(unknown_columns)[0],
            )
        )
    return RowConstraint(constraint_id, where, require)


def _member_scope(
    raw: Any,
    header: tuple[str, ...],
    suite: str,
    check: str,
    *,
    label: str = "members",
) -> MemberScope:
    if not isinstance(raw, dict):
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_MEMBERS",
                "invalid",
                "table members must be a TOML table",
                suite=suite,
                check=check,
                field=label,
            )
        )
    key = raw.get("key")
    if not isinstance(key, str) or not key or key not in header:
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_MEMBER_KEY",
                "invalid",
                "table member key must name one canonical table column",
                suite=suite,
                check=check,
                field=f"{label}.key",
                observed=str(key),
            )
        )
    source_raw = dict(raw)
    source_raw.pop("key")
    source = parse_projected_table_source(
        source_raw,
        suite,
        check,
        label,
        invalid_code="CONFIG.TABLE_MEMBERS",
        source_name="table member source",
        projection_name="table member projection",
        predicate_name="table member predicate",
    )
    if len(source.projection.columns) != 1 or source.projection.split_field is not None:
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_MEMBER_PROJECTION",
                "invalid",
                "table member projection must select exactly one unsplit column",
                suite=suite,
                check=check,
                field=f"{label}.columns",
            )
        )
    return MemberScope(source, key)


def parse_table_check(raw: dict[str, Any], suite_id: str) -> TableCheck:
    allowed = {
        "id",
        "type",
        "path",
        "header",
        "non_empty",
        "domains",
        "unique",
        "projections",
        "where",
        "members",
        "row_constraints",
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
    unique = tuple(_strings(key, "unique", suite_id, check_id) for key in raw_unique)
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
    where = None
    if "where" in raw:
        where = parse_predicate(raw["where"], suite_id, check_id)
        unknown_fields = where.fields() - set(header)
        if unknown_fields:
            raise EngineError(
                Diagnostic(
                    "CONFIG.TABLE_COLUMN",
                    "invalid",
                    "table scope references an unknown column",
                    suite=suite_id,
                    check=check_id,
                    field=sorted(unknown_fields)[0],
                )
            )
    members = None
    if "members" in raw:
        members = _member_scope(raw["members"], header, suite_id, check_id)
    if where is not None and members is not None:
        raise EngineError(
            Diagnostic(
                "CONFIG.TABLE_SCOPE",
                "invalid",
                "table where and members scopes are mutually exclusive",
                suite=suite_id,
                check=check_id,
            )
        )
    raw_row_constraints = raw.get("row_constraints", [])
    if not isinstance(raw_row_constraints, list):
        raise EngineError(
            Diagnostic(
                "CONFIG.ROW_CONSTRAINTS",
                "invalid",
                "row_constraints must be an array of TOML tables",
                suite=suite_id,
                check=check_id,
            )
        )
    row_constraints = tuple(
        _row_constraint(value, header, suite_id, check_id)
        for value in raw_row_constraints
    )
    constraint_ids = [constraint.id for constraint in row_constraints]
    if len(set(constraint_ids)) != len(constraint_ids):
        raise EngineError(
            Diagnostic(
                "CONFIG.ROW_CONSTRAINT_ID",
                "invalid",
                "row constraint ids must be unique",
                suite=suite_id,
                check=check_id,
            )
        )
    if (
        not non_empty
        and not domains
        and not unique
        and not projections
        and not row_constraints
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
        non_empty,
        domains,
        unique,
        projections,
        where,
        members,
        row_constraints,
    )
