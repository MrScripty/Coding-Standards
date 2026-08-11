from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..inventory import collect_inventory
from ..model import CheckContext
from ..numeric_audit import HEADER, NumericAuditDiagnostic, collect_candidates
from .table import read_table_rows


DECISIONS_HEADER = ("candidate_id", "semantic_class")
PACKAGES_HEADER = (
    "train_order",
    "package_id",
    "subject",
    "owner",
    "risk",
    "semantic_outcome",
    "write_set",
    "prerequisites",
    "verification",
    "state",
)
PACKAGE_SUBJECT_PREFIX = "checker:"


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


def _require_non_empty(
    rows: list[dict[str, str]],
    fields: tuple[str, ...],
    *,
    path: str,
    suite: str,
    check: str,
) -> None:
    for row_number, row in enumerate(rows, start=2):
        for field in fields:
            if not row[field]:
                raise EngineError(
                    Diagnostic(
                        "NUMERIC_LIFECYCLE.EMPTY_VALUE",
                        "invalid",
                        "lifecycle evidence field must not be empty",
                        suite=suite,
                        check=check,
                        path=path,
                        row=row_number,
                        field=field,
                    )
                )


def _index_unique(
    rows: list[dict[str, str]],
    field: str,
    *,
    path: str,
    suite: str,
    check: str,
) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row_number, row in enumerate(rows, start=2):
        value = row[field]
        if value in indexed:
            raise EngineError(
                Diagnostic(
                    "NUMERIC_LIFECYCLE.DUPLICATE_IDENTITY",
                    "invalid",
                    "lifecycle evidence identity must occur exactly once",
                    suite=suite,
                    check=check,
                    path=path,
                    row=row_number,
                    field=field,
                    observed=value,
                )
            )
        indexed[value] = row
    return indexed


def _validate_historical_checker(
    value: str, *, path: str, row: int, suite: str, check: str
) -> None:
    parsed = PurePosixPath(value)
    if parsed.is_absolute() or ".." in parsed.parts:
        raise EngineError(
            Diagnostic(
                "NUMERIC_LIFECYCLE.INVALID_CHECKER_PATH",
                "invalid",
                "historical checker must be a repository-relative path without parent traversal",
                suite=suite,
                check=check,
                path=path,
                row=row,
                field="checker",
                observed=value,
            )
        )


def _translate_audit_error(
    error: NumericAuditDiagnostic, *, suite: str, check: str
) -> EngineError:
    return EngineError(
        Diagnostic(
            error.code,
            error.outcome,
            error.message,
            suite=suite,
            check=check,
            path=error.path,
            row=error.row,
        ),
        exit_code=error.exit_code,
    )


@dataclass(frozen=True, slots=True)
class NumericLifecycleCheck:
    id: str
    baseline_path: str
    decisions_path: str
    packages_path: str

    def run(self, context: CheckContext) -> list[Diagnostic]:
        baseline_rows = read_table_rows(
            context.repo_root,
            self.baseline_path,
            HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        decision_rows = read_table_rows(
            context.repo_root,
            self.decisions_path,
            DECISIONS_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        package_rows = read_table_rows(
            context.repo_root,
            self.packages_path,
            PACKAGES_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        _require_non_empty(
            baseline_rows,
            HEADER,
            path=self.baseline_path,
            suite=context.suite_id,
            check=self.id,
        )
        _require_non_empty(
            decision_rows,
            DECISIONS_HEADER,
            path=self.decisions_path,
            suite=context.suite_id,
            check=self.id,
        )
        baseline = _index_unique(
            baseline_rows,
            "candidate_id",
            path=self.baseline_path,
            suite=context.suite_id,
            check=self.id,
        )
        decisions = _index_unique(
            decision_rows,
            "candidate_id",
            path=self.decisions_path,
            suite=context.suite_id,
            check=self.id,
        )
        for row_number, row in enumerate(baseline_rows, start=2):
            _validate_historical_checker(
                row["checker"],
                path=self.baseline_path,
                row=row_number,
                suite=context.suite_id,
                check=self.id,
            )

        baseline_ids = set(baseline)
        decision_ids = set(decisions)
        if decision_ids != baseline_ids:
            return [
                Diagnostic(
                    "ASSERT.NUMERIC_LIFECYCLE_DECISIONS",
                    "invalid",
                    "reviewed decision identities must equal immutable baseline identities",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.decisions_path,
                    expected=",".join(sorted(baseline_ids - decision_ids)),
                    observed=",".join(sorted(decision_ids - baseline_ids)),
                )
            ]

        try:
            inventory = collect_inventory(context.repo_root)
        except UnicodeDecodeError as error:
            raise EngineError(
                Diagnostic(
                    "NUMERIC_LIFECYCLE.INVENTORY_INVALID_UTF8",
                    "invalid",
                    "canonical checker inventory contains invalid UTF-8",
                    suite=context.suite_id,
                    check=self.id,
                )
            ) from error
        live_checkers = {record.checker for record in inventory}
        try:
            current_candidates = collect_candidates(
                context.repo_root,
                tuple(sorted(live_checkers)),
            )
        except NumericAuditDiagnostic as error:
            raise _translate_audit_error(
                error, suite=context.suite_id, check=self.id
            ) from error
        current = {candidate.candidate_id: candidate for candidate in current_candidates}
        current_ids = set(current)

        new_ids = sorted(current_ids - baseline_ids)
        if new_ids:
            return [
                Diagnostic(
                    "ASSERT.NUMERIC_LIFECYCLE_NEW_CANDIDATE",
                    "invalid",
                    "current derivation contains an identity absent from the immutable baseline",
                    suite=context.suite_id,
                    check=self.id,
                    path=current[candidate_id].checker,
                    observed=candidate_id,
                )
                for candidate_id in new_ids
            ]

        missing_ids = baseline_ids - current_ids
        if not missing_ids:
            return []
        missing_checkers = sorted(
            {baseline[candidate_id]["checker"] for candidate_id in missing_ids}
        )
        still_live = [checker for checker in missing_checkers if checker in live_checkers]
        if still_live:
            return [
                Diagnostic(
                    "ASSERT.NUMERIC_LIFECYCLE_CHECKER_STILL_LIVE",
                    "invalid",
                    "candidate disappearance is not authorized while its checker remains live",
                    suite=context.suite_id,
                    check=self.id,
                    path=checker,
                )
                for checker in still_live
            ]

        diagnostics: list[Diagnostic] = []
        for checker in missing_checkers:
            subject = f"{PACKAGE_SUBJECT_PREFIX}{checker}"
            packages = [row for row in package_rows if row["subject"] == subject]
            if not packages:
                raise EngineError(
                    Diagnostic(
                        "NUMERIC_LIFECYCLE.PACKAGE_UNAVAILABLE",
                        "unavailable",
                        "retired checker has no explicit migration-package authority",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.packages_path,
                        expected=subject,
                    ),
                    exit_code=3,
                )
            if len(packages) != 1:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.NUMERIC_LIFECYCLE_AMBIGUOUS_PACKAGE",
                        "invalid",
                        "retired checker must join exactly one migration package",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.packages_path,
                        expected="1",
                        observed=str(len(packages)),
                    )
                )
                continue
            package = packages[0]
            if package["state"] != "accepted":
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.NUMERIC_LIFECYCLE_PACKAGE_STATE",
                        "invalid",
                        "retired checker package must be accepted",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.packages_path,
                        field="state",
                        expected="accepted",
                        observed=package["state"],
                    )
                )
                continue
            if not package["owner"]:
                raise EngineError(
                    Diagnostic(
                        "NUMERIC_LIFECYCLE.OWNER_UNAVAILABLE",
                        "unavailable",
                        "accepted checker package must supply an explicit owner",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.packages_path,
                        field="owner",
                    ),
                    exit_code=3,
                )
        return diagnostics


def parse_numeric_lifecycle_check(
    raw: dict[str, Any], suite_id: str
) -> NumericLifecycleCheck:
    allowed = {
        "id",
        "type",
        "baseline_path",
        "decisions_path",
        "packages_path",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "numeric_audit_lifecycle check contains unknown fields",
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
    return NumericLifecycleCheck(
        check_id,
        _string(raw.get("baseline_path"), "baseline_path", suite_id, check_id),
        _string(raw.get("decisions_path"), "decisions_path", suite_id, check_id),
        _string(raw.get("packages_path"), "packages_path", suite_id, check_id),
    )
