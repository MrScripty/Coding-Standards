from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .diagnostics import EngineError
from .inventory import collect_inventory
from .numeric_audit import HEADER as BASELINE_HEADER
from .numeric_audit import NumericAuditDiagnostic, collect_candidates
from .paths import contained_file, contained_path


MIGRATION_TERMINAL_TRIGGER = "zero-bash-accepted"


PACKAGES_PATH = Path(
    "evaluation/standards-effectiveness/numeric-candidate-retirement-packages.tsv"
)
RETIREMENTS_PATH = Path(
    "evaluation/standards-effectiveness/generated/numeric-candidate-retirements.tsv"
)
BASELINE_PATH = Path(
    "evaluation/standards-effectiveness/generated/numeric-comparison-candidates.tsv"
)
PACKAGES_HEADER = ("package_id", "owner", "semantic_outcome", "state")
RETIREMENTS_HEADER = ("candidate_id", "package_id")
PACKAGE_STATES = frozenset({"admitted", "accepted"})


@dataclass(frozen=True, slots=True)
class NumericRetirementDiagnostic(Exception):
    code: str
    outcome: str
    message: str
    exit_code: int = 2
    path: str | None = None
    row: int | None = None

    def __str__(self) -> str:
        context = []
        if self.path is not None:
            context.append(f"path={self.path}")
        if self.row is not None:
            context.append(f"row={self.row}")
        location = f" ({', '.join(context)})" if context else ""
        return f"{self.code} [{self.outcome}]{location}: {self.message}"


@dataclass(frozen=True, slots=True)
class RetirementState:
    baseline_checkers: dict[str, str]
    current_ids: frozenset[str]
    live_checkers: frozenset[str]
    packages: dict[str, tuple[str, str, str]]
    retirements: dict[str, str]

    @property
    def missing_live_ids(self) -> frozenset[str]:
        return frozenset(
            candidate_id
            for candidate_id, checker in self.baseline_checkers.items()
            if checker in self.live_checkers and candidate_id not in self.current_ids
        )


def _translate_input_error(error: EngineError, path: str) -> NumericRetirementDiagnostic:
    return NumericRetirementDiagnostic(
        code=f"NUMERIC_RETIREMENT.{error.diagnostic.code}",
        outcome=error.diagnostic.outcome,
        message=error.diagnostic.message,
        exit_code=error.exit_code,
        path=path,
    )


def _read_rows(
    root: Path, path: Path, header: tuple[str, ...]
) -> list[tuple[str, ...]]:
    relative = path.as_posix()
    try:
        target = contained_file(root, relative)
    except EngineError as error:
        raise _translate_input_error(error, relative) from error
    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise NumericRetirementDiagnostic(
            "NUMERIC_RETIREMENT.INVALID_UTF8",
            "invalid",
            "numeric retirement input is not valid UTF-8",
            path=relative,
        ) from error
    try:
        rows = list(csv.reader(io.StringIO(content), delimiter="\t", strict=True))
    except csv.Error as error:
        raise NumericRetirementDiagnostic(
            "NUMERIC_RETIREMENT.MALFORMED_TABLE",
            "invalid",
            "numeric retirement input is not valid TSV",
            path=relative,
        ) from error
    if not rows or tuple(rows[0]) != header:
        raise NumericRetirementDiagnostic(
            "NUMERIC_RETIREMENT.TABLE_HEADER",
            "invalid",
            "numeric retirement input has an unexpected header",
            path=relative,
        )
    result: list[tuple[str, ...]] = []
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(header) or not all(row):
            raise NumericRetirementDiagnostic(
                "NUMERIC_RETIREMENT.MALFORMED_TABLE",
                "invalid",
                "numeric retirement row has missing or extra fields",
                path=relative,
                row=row_number,
            )
        result.append(tuple(row))
    return result


def _unique_rows(
    rows: Iterable[tuple[str, ...]], *, path: Path, identity: str
) -> dict[str, tuple[str, ...]]:
    indexed: dict[str, tuple[str, ...]] = {}
    for row_number, row in enumerate(rows, start=2):
        key = row[0]
        if key in indexed:
            raise NumericRetirementDiagnostic(
                "NUMERIC_RETIREMENT.DUPLICATE_IDENTITY",
                "invalid",
                f"{identity} must occur exactly once",
                path=path.as_posix(),
                row=row_number,
            )
        indexed[key] = row
    return indexed


def load_state(
    root: Path,
    *,
    baseline_path: Path = BASELINE_PATH,
    packages_path: Path = PACKAGES_PATH,
    retirements_path: Path = RETIREMENTS_PATH,
) -> RetirementState:
    baseline_rows = _read_rows(root, baseline_path, BASELINE_HEADER)
    package_rows = _read_rows(root, packages_path, PACKAGES_HEADER)
    retirement_rows = _read_rows(root, retirements_path, RETIREMENTS_HEADER)
    baseline = _unique_rows(
        baseline_rows, path=baseline_path, identity="baseline candidate identity"
    )
    raw_packages = _unique_rows(
        package_rows, path=packages_path, identity="retirement package identity"
    )
    raw_retirements = _unique_rows(
        retirement_rows, path=retirements_path, identity="retired candidate identity"
    )
    packages: dict[str, tuple[str, str, str]] = {}
    for row_number, (package_id, owner, semantic_outcome, state) in enumerate(
        raw_packages.values(), start=2
    ):
        if state not in PACKAGE_STATES:
            raise NumericRetirementDiagnostic(
                "NUMERIC_RETIREMENT.PACKAGE_STATE",
                "invalid",
                "retirement package state must be admitted or accepted",
                path=packages_path.as_posix(),
                row=row_number,
            )
        packages[package_id] = (owner, semantic_outcome, state)
    retirements = {
        candidate_id: package_id
        for candidate_id, package_id in raw_retirements.values()
    }
    for row_number, (candidate_id, package_id) in enumerate(
        raw_retirements.values(), start=2
    ):
        if candidate_id not in baseline:
            raise NumericRetirementDiagnostic(
                "NUMERIC_RETIREMENT.UNKNOWN_CANDIDATE",
                "invalid",
                "retired candidate is absent from the immutable baseline",
                path=retirements_path.as_posix(),
                row=row_number,
            )
        if package_id not in packages:
            raise NumericRetirementDiagnostic(
                "NUMERIC_RETIREMENT.PACKAGE_UNAVAILABLE",
                "unavailable",
                "retired candidate has no explicit package authority",
                exit_code=3,
                path=retirements_path.as_posix(),
                row=row_number,
            )
    try:
        live_checkers = frozenset(
            record.checker for record in collect_inventory(root)
        )
        current_ids = frozenset(
            candidate.candidate_id
            for candidate in collect_candidates(root, tuple(sorted(live_checkers)))
        )
    except NumericAuditDiagnostic as error:
        raise NumericRetirementDiagnostic(
            error.code,
            error.outcome,
            error.message,
            error.exit_code,
            error.path,
            error.row,
        ) from error
    return RetirementState(
        baseline_checkers={candidate_id: row[1] for candidate_id, row in baseline.items()},
        current_ids=current_ids,
        live_checkers=live_checkers,
        packages=packages,
        retirements=retirements,
    )


def validate_state(state: RetirementState) -> None:
    for candidate_id, package_id in sorted(state.retirements.items()):
        if candidate_id in state.current_ids:
            raise NumericRetirementDiagnostic(
                "NUMERIC_RETIREMENT.CANDIDATE_STILL_PRESENT",
                "invalid",
                "retirement evidence names a candidate that is still present",
                path=RETIREMENTS_PATH.as_posix(),
            )
        if state.packages[package_id][2] != "accepted":
            raise NumericRetirementDiagnostic(
                "NUMERIC_RETIREMENT.PACKAGE_NOT_ACCEPTED",
                "invalid",
                "retirement evidence requires an accepted package",
                path=PACKAGES_PATH.as_posix(),
            )
    unexplained = state.missing_live_ids - state.retirements.keys()
    if unexplained:
        candidate_id = sorted(unexplained)[0]
        raise NumericRetirementDiagnostic(
            "NUMERIC_RETIREMENT.UNAUTHORIZED_CANDIDATE",
            "invalid",
            "live-checker candidate disappearance has no retirement evidence",
            path=state.baseline_checkers[candidate_id],
        )


def _render_retirements(retirements: dict[str, str]) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(RETIREMENTS_HEADER)
    for candidate_id, package_id in sorted(retirements.items()):
        writer.writerow((candidate_id, package_id))
    return output.getvalue()


def check_retirements(root: Path) -> int:
    try:
        validate_state(load_state(root))
    except NumericRetirementDiagnostic as error:
        print(error)
        return error.exit_code
    print(f"PASS {RETIREMENTS_PATH.as_posix()}")
    return 0


def record_retirements(root: Path, package_id: str) -> int:
    try:
        state = load_state(root)
        package = state.packages.get(package_id)
        if package is None:
            raise NumericRetirementDiagnostic(
                "NUMERIC_RETIREMENT.PACKAGE_UNAVAILABLE",
                "unavailable",
                "selected retirement package does not exist",
                exit_code=3,
                path=PACKAGES_PATH.as_posix(),
            )
        existing_ids = set(state.retirements)
        new_ids = state.missing_live_ids - existing_ids
        for candidate_id, existing_package in state.retirements.items():
            if candidate_id in state.current_ids:
                raise NumericRetirementDiagnostic(
                    "NUMERIC_RETIREMENT.CANDIDATE_STILL_PRESENT",
                    "invalid",
                    "retirement evidence names a candidate that is still present",
                    path=RETIREMENTS_PATH.as_posix(),
                )
            if state.packages[existing_package][2] not in {"admitted", "accepted"}:
                raise NumericRetirementDiagnostic(
                    "NUMERIC_RETIREMENT.PACKAGE_STATE",
                    "invalid",
                    "existing retirement evidence has an invalid package state",
                    path=PACKAGES_PATH.as_posix(),
                )
        if new_ids and package[2] != "admitted":
            raise NumericRetirementDiagnostic(
                "NUMERIC_RETIREMENT.PACKAGE_IMMUTABLE",
                "invalid",
                "new candidate identities may be recorded only for an admitted package",
                path=PACKAGES_PATH.as_posix(),
            )
        updated = dict(state.retirements)
        updated.update((candidate_id, package_id) for candidate_id in new_ids)
        target = contained_path(root, RETIREMENTS_PATH.as_posix())
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_render_retirements(updated), encoding="utf-8")
    except EngineError as error:
        diagnostic = error.diagnostic
        print(diagnostic.render())
        return error.exit_code
    except NumericRetirementDiagnostic as error:
        print(error)
        return error.exit_code
    print(
        f"WROTE {RETIREMENTS_PATH.as_posix()} "
        f"({len(new_ids)} derived candidates assigned to {package_id})"
    )
    return 0
