from __future__ import annotations

import csv
import hashlib
import io
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence

from .diagnostics import EngineError
from .inventory import collect_inventory
from .paths import contained_file


MIGRATION_TERMINAL_TRIGGER = "zero-bash-accepted"


OUTPUT_PATH = Path(
    "evaluation/standards-effectiveness/generated/"
    "numeric-comparison-candidates.tsv"
)
HEADER = (
    "candidate_id",
    "checker",
    "line",
    "column",
    "matcher",
    "operator",
    "numeric_literals",
    "expression",
    "source_fingerprint",
    "source_text",
)

_NUMBER = r"[-+]?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)"
_OPERAND = (
    r'(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|'
    r"\$\{[^}\n]+\}|\$[A-Za-z_][A-Za-z0-9_]*|\$[0-9]+|"
    r"[A-Za-z_][A-Za-z0-9_]*|" + _NUMBER + r")"
)
_SHELL_NUMERIC = re.compile(
    rf"(?P<left>{_OPERAND})\s+"
    r"(?P<operator>-(?:eq|ne|lt|le|gt|ge))\s+"
    rf"(?P<right>{_OPERAND})"
)
_SYMBOLIC_NUMERIC = re.compile(
    rf"(?P<left>{_OPERAND})\s*"
    r"(?P<operator>==|!=|<=|>=|<|>)\s*"
    rf"(?P<right>{_OPERAND})"
)
_NUMBER_VALUE = re.compile(rf"{_NUMBER}")


@dataclass(frozen=True, slots=True)
class NumericAuditDiagnostic(Exception):
    code: str
    outcome: str
    message: str
    exit_code: int
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
class NumericCandidate:
    candidate_id: str
    checker: str
    line: int
    column: int
    matcher: str
    operator: str
    numeric_literals: tuple[str, ...]
    expression: str
    source_fingerprint: str
    source_text: str


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _numeric_literals(left: str, right: str) -> tuple[str, ...]:
    return tuple(
        value
        for operand in (left, right)
        if _NUMBER_VALUE.fullmatch(value := _unquote(operand)) is not None
    )


def _candidate_id(
    checker: str,
    matcher: str,
    expression: str,
    occurrence: int,
) -> str:
    source = "\0".join((checker, matcher, expression, str(occurrence)))
    return "numeric-" + hashlib.sha256(source.encode("utf-8")).hexdigest()


def _source_fingerprint(source_text: str) -> str:
    return hashlib.sha256(source_text.encode("utf-8")).hexdigest()


def _candidate_matches(source_text: str) -> Iterable[tuple[str, re.Match[str]]]:
    for matcher, pattern in (
        ("shell-numeric", _SHELL_NUMERIC),
        ("symbolic-numeric", _SYMBOLIC_NUMERIC),
    ):
        for match in pattern.finditer(source_text):
            if _numeric_literals(match.group("left"), match.group("right")):
                yield matcher, match


def _read_source(path: Path, relative: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise NumericAuditDiagnostic(
            code="NUMERIC_AUDIT.INVALID_UTF8",
            outcome="invalid",
            message="candidate source is not valid UTF-8",
            exit_code=2,
            path=relative,
        ) from error


def _resolve_checker(root: Path, value: str) -> Path:
    try:
        return contained_file(root, value)
    except EngineError as error:
        diagnostic = error.diagnostic
        raise NumericAuditDiagnostic(
            code=f"NUMERIC_AUDIT.{diagnostic.code}",
            outcome=diagnostic.outcome,
            message=diagnostic.message,
            exit_code=error.exit_code,
            path=value,
        ) from error


def collect_candidates(
    root: Path,
    checker_paths: Sequence[str] | None = None,
) -> tuple[NumericCandidate, ...]:
    root = root.resolve()
    paths = (
        tuple(record.checker for record in collect_inventory(root))
        if checker_paths is None
        else tuple(checker_paths)
    )
    if len(paths) != len(set(paths)):
        raise NumericAuditDiagnostic(
            code="NUMERIC_AUDIT.DUPLICATE_CHECKER",
            outcome="invalid",
            message="canonical verifier scope contains duplicate paths",
            exit_code=2,
        )

    candidates: list[NumericCandidate] = []
    for checker in sorted(paths):
        path = _resolve_checker(root, checker)
        content = _read_source(path, checker)
        occurrences: dict[tuple[str, str], int] = defaultdict(int)
        for line_number, source_text in enumerate(content.splitlines(), start=1):
            matches = sorted(
                _candidate_matches(source_text),
                key=lambda item: (item[1].start(), item[0], item[1].end()),
            )
            for matcher, match in matches:
                expression = match.group(0)
                signature = (matcher, expression)
                occurrence = occurrences[signature]
                occurrences[signature] += 1
                candidates.append(
                    NumericCandidate(
                        candidate_id=_candidate_id(
                            checker,
                            matcher,
                            expression,
                            occurrence,
                        ),
                        checker=checker,
                        line=line_number,
                        column=match.start() + 1,
                        matcher=matcher,
                        operator=match.group("operator"),
                        numeric_literals=_numeric_literals(
                            match.group("left"),
                            match.group("right"),
                        ),
                        expression=expression,
                        source_fingerprint=_source_fingerprint(source_text),
                        source_text=source_text,
                    )
                )
    return tuple(
        sorted(
            candidates,
            key=lambda item: (
                item.checker,
                item.line,
                item.column,
                item.matcher,
                item.candidate_id,
            ),
        )
    )


def render_candidates(candidates: Iterable[NumericCandidate]) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(HEADER)
    for candidate in candidates:
        writer.writerow(
            (
                candidate.candidate_id,
                candidate.checker,
                candidate.line,
                candidate.column,
                candidate.matcher,
                candidate.operator,
                ",".join(candidate.numeric_literals),
                candidate.expression,
                candidate.source_fingerprint,
                candidate.source_text,
            )
        )
    return output.getvalue()


def expected_snapshot(root: Path) -> str:
    return render_candidates(collect_candidates(root))


def _parse_snapshot(content: str, path: str) -> None:
    try:
        rows = list(csv.reader(io.StringIO(content), delimiter="\t", strict=True))
    except csv.Error as error:
        raise NumericAuditDiagnostic(
            code="NUMERIC_AUDIT.MALFORMED_SNAPSHOT",
            outcome="invalid",
            message="generated candidate snapshot is not valid TSV",
            exit_code=2,
            path=path,
        ) from error
    if not rows or tuple(rows[0]) != HEADER:
        raise NumericAuditDiagnostic(
            code="NUMERIC_AUDIT.SNAPSHOT_HEADER",
            outcome="invalid",
            message="generated candidate snapshot has an unexpected header",
            exit_code=2,
            path=path,
        )
    candidate_ids: set[str] = set()
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(HEADER) or not all(row):
            raise NumericAuditDiagnostic(
                code="NUMERIC_AUDIT.MALFORMED_SNAPSHOT",
                outcome="invalid",
                message="generated candidate row has missing or extra fields",
                exit_code=2,
                path=path,
                row=row_number,
            )
        candidate_id = row[0]
        if candidate_id in candidate_ids:
            raise NumericAuditDiagnostic(
                code="NUMERIC_AUDIT.DUPLICATE_CANDIDATE",
                outcome="invalid",
                message="generated candidate identity is duplicated",
                exit_code=2,
                path=path,
                row=row_number,
            )
        candidate_ids.add(candidate_id)


def _target(root: Path, output_path: Path) -> Path:
    value = output_path.as_posix()
    pure = PurePosixPath(value)
    if not value or pure.is_absolute() or ".." in pure.parts:
        raise NumericAuditDiagnostic(
            code="NUMERIC_AUDIT.OUTPUT_OUTSIDE_REPOSITORY",
            outcome="invalid",
            message="snapshot path must be repository-relative without parent traversal",
            exit_code=2,
            path=value,
        )
    target = (root.resolve() / Path(*pure.parts)).resolve(strict=False)
    if not target.is_relative_to(root.resolve()):
        raise NumericAuditDiagnostic(
            code="NUMERIC_AUDIT.OUTPUT_OUTSIDE_REPOSITORY",
            outcome="invalid",
            message="resolved snapshot path escapes the repository root",
            exit_code=2,
            path=value,
        )
    return target


def write_snapshot(root: Path, output_path: Path = OUTPUT_PATH) -> int:
    try:
        target = _target(root, output_path)
        content = expected_snapshot(root)
        if target.exists():
            try:
                observed = target.read_text(encoding="utf-8")
            except UnicodeDecodeError as error:
                raise NumericAuditDiagnostic(
                    code="NUMERIC_AUDIT.INVALID_UTF8",
                    outcome="invalid",
                    message="existing candidate snapshot is not valid UTF-8",
                    exit_code=2,
                    path=output_path.as_posix(),
                ) from error
            _parse_snapshot(observed, output_path.as_posix())
            if observed != content:
                raise NumericAuditDiagnostic(
                    code="NUMERIC_AUDIT.SNAPSHOT_IMMUTABLE",
                    outcome="invalid",
                    message="existing candidate baseline cannot be overwritten",
                    exit_code=2,
                    path=output_path.as_posix(),
                )
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    except NumericAuditDiagnostic as error:
        print(error)
        return error.exit_code
    count = len(content.splitlines()) - 1
    print(f"WROTE {output_path.as_posix()} ({count} derived candidates)")
    return 0
