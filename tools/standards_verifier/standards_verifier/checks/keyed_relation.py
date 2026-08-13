from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from .predicates import Predicate, parse_predicate
from .table import (
    ProjectedTableSource,
    parse_projected_table_source,
    project_table_rows,
    read_table_rows,
)


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
class KeyedRecordSource:
    path: str
    header: tuple[str, ...]
    key: str
    values: tuple[str, ...]
    where: Predicate | None


def _parse_record_source(
    raw: Any, suite: str, check: str, label: str
) -> KeyedRecordSource:
    if not isinstance(raw, dict):
        raise EngineError(
            Diagnostic(
                "CONFIG.KEYED_RELATION_SOURCE",
                "invalid",
                "keyed relation record source must be a TOML table",
                suite=suite,
                check=check,
                field=label,
            )
        )
    allowed = {"path", "header", "key", "values", "where"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "keyed relation record source contains unknown fields",
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
                "keyed relation record path must be a non-empty string",
                suite=suite,
                check=check,
                field=label,
            )
        )
    header = _strings(raw.get("header"), f"{label}.header", suite, check)
    key = raw.get("key")
    if not isinstance(key, str) or not key or key not in header:
        raise EngineError(
            Diagnostic(
                "CONFIG.KEYED_RELATION_KEY",
                "invalid",
                "record key must name one header column",
                suite=suite,
                check=check,
                field=f"{label}.key",
                observed=str(key),
            )
        )
    values = _strings(raw.get("values"), f"{label}.values", suite, check)
    unknown_values = set(values) - set(header)
    if unknown_values or key in values:
        raise EngineError(
            Diagnostic(
                "CONFIG.KEYED_RELATION_VALUES",
                "invalid",
                "record values must name header columns distinct from the key",
                suite=suite,
                check=check,
                field=f"{label}.values",
                observed=(key if key in values else sorted(unknown_values)[0]),
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
                    "keyed relation predicate references an unknown column",
                    suite=suite,
                    check=check,
                    field=sorted(unknown_fields)[0],
                )
            )
    return KeyedRecordSource(path, header, key, values, where)


def _records_by_key(
    rows: list[dict[str, str]], source: KeyedRecordSource
) -> dict[str, list[tuple[str, ...]]]:
    records: dict[str, list[tuple[str, ...]]] = {}
    for row in rows:
        if source.where is not None and not source.where.evaluate(row):
            continue
        records.setdefault(row[source.key], []).append(
            tuple(row[field] for field in source.values)
        )
    return records


@dataclass(frozen=True, slots=True)
class KeyedRelationCheck:
    id: str
    keys: ProjectedTableSource
    expected: KeyedRecordSource
    observed: KeyedRecordSource

    def run(self, context: CheckContext) -> list[Diagnostic]:
        root = context.repo_root
        if not isinstance(root, Path):
            raise TypeError("check context repository root must be a Path")
        key_rows = read_table_rows(
            root,
            self.keys.path,
            self.keys.header,
            suite=context.suite_id,
            check=self.id,
        )
        keys = project_table_rows(key_rows, self.keys.projection)
        if not keys:
            return [
                Diagnostic(
                    "ASSERT.KEYED_RELATION_EMPTY_KEYS",
                    "invalid",
                    "key projection must select at least one key",
                    suite=context.suite_id,
                    check=self.id,
                    expected="nonempty keys",
                    observed="empty",
                )
            ]
        if len(set(keys)) != len(keys):
            return [
                Diagnostic(
                    "ASSERT.KEYED_RELATION_DUPLICATE_KEY",
                    "invalid",
                    "key projection must contain unique keys",
                    suite=context.suite_id,
                    check=self.id,
                    expected="unique keys",
                    observed=f"{len(keys)}/{len(set(keys))}",
                )
            ]

        expected_rows = read_table_rows(
            root,
            self.expected.path,
            self.expected.header,
            suite=context.suite_id,
            check=self.id,
        )
        observed_rows = read_table_rows(
            root,
            self.observed.path,
            self.observed.header,
            suite=context.suite_id,
            check=self.id,
        )
        expected = _records_by_key(expected_rows, self.expected)
        observed = _records_by_key(observed_rows, self.observed)

        diagnostics = []
        for (key,) in keys:
            expected_matches = expected.get(key, [])
            observed_matches = observed.get(key, [])
            for role, matches in (
                ("expected", expected_matches),
                ("observed", observed_matches),
            ):
                if not matches:
                    diagnostics.append(
                        Diagnostic(
                            "ASSERT.KEYED_RELATION_MISSING",
                            "invalid",
                            "derived key has no record in a keyed source",
                            suite=context.suite_id,
                            check=self.id,
                            field=role,
                            expected=key,
                            observed="absent",
                        )
                    )
                elif len(matches) > 1:
                    diagnostics.append(
                        Diagnostic(
                            "ASSERT.KEYED_RELATION_DUPLICATE_RECORD",
                            "invalid",
                            "derived key resolves to multiple records",
                            suite=context.suite_id,
                            check=self.id,
                            field=role,
                            expected="one record",
                            observed=f"{key}:{len(matches)}",
                        )
                    )
            if len(expected_matches) == 1 and len(observed_matches) == 1:
                if expected_matches[0] != observed_matches[0]:
                    diagnostics.append(
                        Diagnostic(
                            "ASSERT.KEYED_RELATION_MISMATCH",
                            "invalid",
                            "keyed record values do not match",
                            suite=context.suite_id,
                            check=self.id,
                            field=key,
                            expected=repr(expected_matches[0]),
                            observed=repr(observed_matches[0]),
                        )
                    )
        return diagnostics


def parse_keyed_relation_check(
    raw: dict[str, Any], suite_id: str
) -> KeyedRelationCheck:
    allowed = {"id", "type", "keys", "expected", "observed"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "keyed_relation check contains unknown fields",
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
    keys = parse_projected_table_source(
        raw.get("keys"),
        suite_id,
        check_id,
        "keys",
        invalid_code="CONFIG.KEYED_RELATION_KEYS",
        source_name="keyed relation key source",
        projection_name="key projection",
        predicate_name="key predicate",
    )
    if len(keys.projection.columns) != 1:
        raise EngineError(
            Diagnostic(
                "CONFIG.KEYED_RELATION_KEY_WIDTH",
                "invalid",
                "key projection must select exactly one column",
                suite=suite_id,
                check=check_id,
                expected="1",
                observed=str(len(keys.projection.columns)),
            )
        )
    expected = _parse_record_source(
        raw.get("expected"), suite_id, check_id, "expected"
    )
    observed = _parse_record_source(
        raw.get("observed"), suite_id, check_id, "observed"
    )
    if len(expected.values) != len(observed.values):
        raise EngineError(
            Diagnostic(
                "CONFIG.KEYED_RELATION_VALUE_WIDTH",
                "invalid",
                "expected and observed value projections must have equal width",
                suite=suite_id,
                check=check_id,
                expected=str(len(expected.values)),
                observed=str(len(observed.values)),
            )
        )
    return KeyedRelationCheck(check_id, keys, expected, observed)
