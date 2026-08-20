from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file, contained_path
from .table import (
    ProjectedTableSource,
    parse_projected_table_source,
    project_table_rows,
    read_table_rows,
)


def _check_id(raw: dict[str, Any], suite: str) -> str:
    check_id = raw.get("id")
    if not isinstance(check_id, str) or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite,
            )
        )
    return check_id


def _source(
    raw: Any,
    suite: str,
    check: str,
    label: str,
    contract: str,
) -> ProjectedTableSource:
    source = parse_projected_table_source(
        raw,
        suite,
        check,
        label,
        invalid_code=f"CONFIG.{contract}_SOURCE",
        source_name=f"{label} source",
        projection_name=f"{label} projection",
        predicate_name=f"{label} predicate",
    )
    if len(source.projection.columns) != 1:
        raise EngineError(
            Diagnostic(
                f"CONFIG.{contract}_WIDTH",
                "invalid",
                f"{label} projection must select exactly one column",
                suite=suite,
                check=check,
                field=label,
                expected="1",
                observed=str(len(source.projection.columns)),
            )
        )
    return source


def _values(
    context: CheckContext,
    check_id: str,
    source: ProjectedTableSource,
    role: str,
    *,
    require_unique: bool,
) -> tuple[tuple[str, ...], list[Diagnostic]]:
    rows = read_table_rows(
        context.repo_root,
        source.path,
        source.header,
        suite=context.suite_id,
        check=check_id,
    )
    projected = project_table_rows(rows, source.projection)
    values = tuple(value for (value,) in projected)
    diagnostics = []
    for value in values:
        if not value:
            diagnostics.append(
                Diagnostic(
                    "ASSERT.DERIVED_VALUE_EMPTY",
                    "invalid",
                    "projected identity must be non-empty",
                    suite=context.suite_id,
                    check=check_id,
                    path=source.path,
                    field=role,
                )
            )
    if require_unique and len(set(values)) != len(values):
        diagnostics.append(
            Diagnostic(
                "ASSERT.DERIVED_VALUE_DUPLICATE",
                "invalid",
                "projected identities must be unique",
                suite=context.suite_id,
                check=check_id,
                path=source.path,
                field=role,
                expected="unique identities",
                observed=f"{len(values)}/{len(set(values))}",
            )
        )
    return values, diagnostics


@dataclass(frozen=True, slots=True)
class RepositorySubjectsCheck:
    id: str
    subjects: ProjectedTableSource

    def run(self, context: CheckContext) -> list[Diagnostic]:
        subjects, diagnostics = _values(
            context,
            self.id,
            self.subjects,
            "subjects",
            require_unique=True,
        )
        if diagnostics:
            return diagnostics

        for subject in subjects:
            kind, separator, identity = subject.partition(":")
            if not separator or not identity or kind not in {"checker", "suite"}:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.REPOSITORY_SUBJECT_TYPE",
                        "invalid",
                        "subject must be checker:<path> or suite:<registered-id>",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.subjects.path,
                        expected="checker:<path>|suite:<registered-id>",
                        observed=subject,
                    )
                )
                continue
            if kind == "suite":
                if identity not in context.registered_suite_ids:
                    raise EngineError(
                        Diagnostic(
                            "INPUT.SUITE_UNAVAILABLE",
                            "unavailable",
                            "subject names an unregistered suite",
                            suite=context.suite_id,
                            check=self.id,
                            path=self.subjects.path,
                            observed=identity,
                        ),
                        exit_code=3,
                    )
                continue

            candidate = contained_path(
                context.repo_root,
                identity,
                suite=context.suite_id,
                check=self.id,
            )
            if candidate.is_symlink():
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.REPOSITORY_SUBJECT_SYMLINK",
                        "invalid",
                        "checker subject must not be a symlink",
                        suite=context.suite_id,
                        check=self.id,
                        path=identity,
                    )
                )
                continue
            contained_file(
                context.repo_root,
                identity,
                suite=context.suite_id,
                check=self.id,
            )
        return diagnostics


@dataclass(frozen=True, slots=True)
class RepositoryPathsCheck:
    id: str
    paths: ProjectedTableSource

    def run(self, context: CheckContext) -> list[Diagnostic]:
        paths, diagnostics = _values(
            context,
            self.id,
            self.paths,
            "paths",
            require_unique=False,
        )
        if not paths:
            diagnostics.append(
                Diagnostic(
                    "ASSERT.REPOSITORY_PATHS_EMPTY",
                    "invalid",
                    "path projection must select at least one path",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.paths.path,
                    expected="nonempty paths",
                    observed="empty",
                )
            )
        if diagnostics:
            return diagnostics

        for path in dict.fromkeys(paths):
            candidate = contained_path(
                context.repo_root,
                path,
                suite=context.suite_id,
                check=self.id,
            )
            if candidate.is_symlink():
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.REPOSITORY_PATH_SYMLINK",
                        "invalid",
                        "repository path must not be a symlink",
                        suite=context.suite_id,
                        check=self.id,
                        path=path,
                    )
                )
                continue
            contained_file(
                context.repo_root,
                path,
                suite=context.suite_id,
                check=self.id,
            )
        return diagnostics


@dataclass(frozen=True, slots=True)
class KeyCoverageCheck:
    id: str
    keys: ProjectedTableSource
    records: ProjectedTableSource

    def run(self, context: CheckContext) -> list[Diagnostic]:
        keys, key_diagnostics = _values(
            context,
            self.id,
            self.keys,
            "keys",
            require_unique=True,
        )
        records, record_diagnostics = _values(
            context,
            self.id,
            self.records,
            "records",
            require_unique=False,
        )
        diagnostics = [*key_diagnostics, *record_diagnostics]
        if not keys:
            diagnostics.append(
                Diagnostic(
                    "ASSERT.KEY_COVERAGE_EMPTY_KEYS",
                    "invalid",
                    "key projection must select at least one key",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.keys.path,
                    expected="nonempty keys",
                    observed="empty",
                )
            )
        if diagnostics:
            return diagnostics

        record_set = set(records)
        return [
            Diagnostic(
                "ASSERT.KEY_COVERAGE_MISSING",
                "invalid",
                "derived key has no matching record",
                suite=context.suite_id,
                check=self.id,
                path=self.records.path,
                expected=key,
                observed="absent",
            )
            for key in keys
            if key not in record_set
        ]


@dataclass(frozen=True, slots=True)
class TableTextAbsenceCheck:
    id: str
    path: str
    literals: ProjectedTableSource

    def run(self, context: CheckContext) -> list[Diagnostic]:
        literals, diagnostics = _values(
            context,
            self.id,
            self.literals,
            "literals",
            require_unique=True,
        )
        if diagnostics:
            return diagnostics
        source = contained_file(
            context.repo_root,
            self.path,
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
                    path=self.path,
                )
            ) from error
        return [
            Diagnostic(
                "ASSERT.TABLE_TEXT_PRESENT",
                "invalid",
                "table-derived literal is present in the target text",
                suite=context.suite_id,
                check=self.id,
                path=self.path,
                expected="absent",
                observed=literal,
            )
            for literal in literals
            if literal in content
        ]


def parse_repository_subjects_check(
    raw: dict[str, Any], suite_id: str
) -> RepositorySubjectsCheck:
    allowed = {"id", "type", "subjects"}
    _reject_unknown(raw, allowed, suite_id, "repository subjects")
    check_id = _check_id(raw, suite_id)
    subjects = _source(
        raw.get("subjects"), suite_id, check_id, "subjects", "REPOSITORY_SUBJECTS"
    )
    return RepositorySubjectsCheck(check_id, subjects)


def parse_repository_paths_check(
    raw: dict[str, Any], suite_id: str
) -> RepositoryPathsCheck:
    allowed = {"id", "type", "paths"}
    _reject_unknown(raw, allowed, suite_id, "repository paths")
    check_id = _check_id(raw, suite_id)
    paths = _source(
        raw.get("paths"), suite_id, check_id, "paths", "REPOSITORY_PATHS"
    )
    return RepositoryPathsCheck(check_id, paths)


def parse_key_coverage_check(
    raw: dict[str, Any], suite_id: str
) -> KeyCoverageCheck:
    allowed = {"id", "type", "keys", "records"}
    _reject_unknown(raw, allowed, suite_id, "key coverage")
    check_id = _check_id(raw, suite_id)
    keys = _source(raw.get("keys"), suite_id, check_id, "keys", "KEY_COVERAGE")
    records = _source(
        raw.get("records"), suite_id, check_id, "records", "KEY_COVERAGE"
    )
    return KeyCoverageCheck(check_id, keys, records)


def parse_table_text_absence_check(
    raw: dict[str, Any], suite_id: str
) -> TableTextAbsenceCheck:
    allowed = {"id", "type", "path", "literals"}
    _reject_unknown(raw, allowed, suite_id, "table text absence")
    check_id = _check_id(raw, suite_id)
    path = raw.get("path")
    if not isinstance(path, str) or not path:
        raise EngineError(
            Diagnostic(
                "CONFIG.PATH",
                "invalid",
                "target path must be a non-empty string",
                suite=suite_id,
                check=check_id,
                field="path",
            )
        )
    literals = _source(
        raw.get("literals"), suite_id, check_id, "literals", "TABLE_TEXT_ABSENCE"
    )
    return TableTextAbsenceCheck(check_id, path, literals)


def _reject_unknown(
    raw: dict[str, Any], allowed: set[str], suite: str, name: str
) -> None:
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                f"{name} check contains unknown fields",
                suite=suite,
                field=sorted(unknown)[0],
            )
        )
