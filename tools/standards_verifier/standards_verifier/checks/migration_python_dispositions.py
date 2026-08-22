from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file, contained_path
from .table import read_table_rows


MIGRATION_TERMINAL_TRIGGER = "zero-bash-accepted"
MIGRATION_CHECK_KINDS = ("migration_python_dispositions",)
DISPOSITION_HEADER = (
    "subject_kind",
    "subject",
    "path",
    "disposition",
    "current_consumer",
    "post_zero_consumer",
    "terminal_trigger",
    "evidence_owner",
    "rationale",
)


@dataclass(frozen=True, slots=True)
class MigrationCandidate:
    kind: str
    subject: str
    path: str


@dataclass(frozen=True, slots=True)
class MigrationPythonDispositionsCheck:
    id: str
    path: str
    package_path: str
    terminal_trigger: str

    def run(self, context: CheckContext) -> list[Diagnostic]:
        candidates = self._candidates(context)
        rows = read_table_rows(
            context.repo_root,
            self.path,
            DISPOSITION_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        dispositions = {
            (row["subject_kind"], row["subject"]): row
            for row in rows
            if row["subject_kind"] in {"module", "check-kind"}
            and row["terminal_trigger"] == self.terminal_trigger
        }
        expected = {(candidate.kind, candidate.subject): candidate for candidate in candidates}
        diagnostics: list[Diagnostic] = []
        for key in sorted(expected.keys() - dispositions.keys()):
            candidate = expected[key]
            diagnostics.append(
                self._diagnostic(
                    context,
                    "ASSERT.MIGRATION_PYTHON_DISPOSITION",
                    "declared migration Python candidate has no terminal disposition",
                    field=key[0],
                    expected=candidate.subject,
                    observed="missing",
                )
            )
        for key in sorted(dispositions.keys() - expected.keys()):
            diagnostics.append(
                self._diagnostic(
                    context,
                    "ASSERT.MIGRATION_PYTHON_CANDIDATE",
                    "terminal disposition has no declared migration Python candidate",
                    field=key[0],
                    expected="declared candidate",
                    observed=key[1],
                )
            )
        for key in sorted(expected.keys() & dispositions.keys()):
            candidate = expected[key]
            observed_path = dispositions[key]["path"]
            if observed_path != candidate.path:
                diagnostics.append(
                    self._diagnostic(
                        context,
                        "ASSERT.MIGRATION_PYTHON_PATH",
                        "candidate and disposition paths do not match",
                        field=candidate.subject,
                        expected=candidate.path,
                        observed=observed_path,
                    )
                )
        return diagnostics

    def _candidates(self, context: CheckContext) -> tuple[MigrationCandidate, ...]:
        package = contained_path(
            context.repo_root,
            self.package_path,
            suite=context.suite_id,
            check=self.id,
        )
        if not package.exists() or not package.is_dir():
            raise EngineError(
                Diagnostic(
                    "INPUT.UNAVAILABLE",
                    "unavailable",
                    "migration Python package does not exist",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.package_path,
                )
            )
        candidates: list[MigrationCandidate] = []
        check_kinds: set[str] = set()
        for source in sorted(package.rglob("*.py")):
            relative = source.relative_to(context.repo_root).as_posix()
            resolved = contained_file(
                context.repo_root,
                relative,
                suite=context.suite_id,
                check=self.id,
            )
            try:
                tree = ast.parse(resolved.read_text(encoding="utf-8"), filename=relative)
            except (SyntaxError, UnicodeDecodeError) as error:
                raise EngineError(
                    Diagnostic(
                        "MIGRATION_PYTHON.INVALID_SOURCE",
                        "invalid",
                        str(error),
                        suite=context.suite_id,
                        check=self.id,
                        path=relative,
                    )
                ) from error
            trigger = self._constant(tree, "MIGRATION_TERMINAL_TRIGGER", relative, context)
            kinds = self._constant(tree, "MIGRATION_CHECK_KINDS", relative, context)
            if trigger is None and kinds is None:
                continue
            if trigger != self.terminal_trigger:
                raise EngineError(
                    Diagnostic(
                        "MIGRATION_PYTHON.TRIGGER",
                        "invalid",
                        "migration declaration has an unknown terminal trigger",
                        suite=context.suite_id,
                        check=self.id,
                        path=relative,
                        observed=str(trigger),
                    )
                )
            module = self._module_id(source.relative_to(package))
            candidates.append(MigrationCandidate("module", module, relative))
            if kinds is None:
                continue
            if (
                not isinstance(kinds, (tuple, list))
                or not kinds
                or any(not isinstance(kind, str) or not kind for kind in kinds)
                or len(set(kinds)) != len(kinds)
            ):
                raise EngineError(
                    Diagnostic(
                        "MIGRATION_PYTHON.CHECK_KINDS",
                        "invalid",
                        "migration check kinds must be unique non-empty strings",
                        suite=context.suite_id,
                        check=self.id,
                        path=relative,
                    )
                )
            for kind in kinds:
                if kind in check_kinds:
                    raise EngineError(
                        Diagnostic(
                            "MIGRATION_PYTHON.DUPLICATE_CHECK_KIND",
                            "invalid",
                            "migration check kind is declared more than once",
                            suite=context.suite_id,
                            check=self.id,
                            path=relative,
                            observed=kind,
                        )
                    )
                check_kinds.add(kind)
                candidates.append(MigrationCandidate("check-kind", kind, relative))
        return tuple(sorted(candidates, key=lambda item: (item.kind, item.subject)))

    def _constant(
        self,
        tree: ast.Module,
        name: str,
        path: str,
        context: CheckContext,
    ) -> object | None:
        values = []
        for statement in tree.body:
            value = None
            targets: list[ast.expr] = []
            if isinstance(statement, ast.Assign):
                value = statement.value
                targets = statement.targets
            elif isinstance(statement, ast.AnnAssign):
                value = statement.value
                targets = [statement.target]
            if value is None or not any(
                isinstance(target, ast.Name) and target.id == name
                for target in targets
            ):
                continue
            try:
                values.append(ast.literal_eval(value))
            except (ValueError, TypeError) as error:
                raise EngineError(
                    Diagnostic(
                        "MIGRATION_PYTHON.DECLARATION",
                        "invalid",
                        "migration declaration must be a literal value",
                        suite=context.suite_id,
                        check=self.id,
                        path=path,
                        field=name,
                    )
                ) from error
        if len(values) > 1:
            raise EngineError(
                Diagnostic(
                    "MIGRATION_PYTHON.DECLARATION",
                    "invalid",
                    "migration declaration must occur at most once",
                    suite=context.suite_id,
                    check=self.id,
                    path=path,
                    field=name,
                )
            )
        return values[0] if values else None

    @staticmethod
    def _module_id(relative: Path) -> str:
        parts = list(relative.with_suffix("").parts)
        if parts[-1] == "__init__":
            parts.pop()
        return ".".join(("standards_verifier", *parts))

    def _diagnostic(
        self,
        context: CheckContext,
        code: str,
        message: str,
        *,
        field: str,
        expected: str,
        observed: str,
    ) -> Diagnostic:
        return Diagnostic(
            code,
            "invalid",
            message,
            suite=context.suite_id,
            check=self.id,
            path=self.path,
            field=field,
            expected=expected,
            observed=observed,
        )


def parse_migration_python_dispositions_check(
    raw: dict[str, Any], suite: str
) -> MigrationPythonDispositionsCheck:
    allowed = {"id", "type", "path", "package_path", "terminal_trigger"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "migration Python dispositions check contains unknown fields",
                suite=suite,
                field=sorted(unknown)[0],
            )
        )
    check = raw.get("id")
    if not isinstance(check, str) or not check:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite,
            )
        )
    values = []
    for field in ("path", "package_path", "terminal_trigger"):
        value = raw.get(field)
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
        values.append(value)
    return MigrationPythonDispositionsCheck(check, *values)
