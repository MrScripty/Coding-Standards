from __future__ import annotations

import csv
import io
import subprocess
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from tools.standards_metadata.standards_metadata import (
    MetadataError,
    load_canonical_standards_corpus,
)
from tools.standards_policy_impact.standards_policy_impact import (
    PolicyImpactError,
    compile_policy_impact,
)

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file


EVIDENCE_HEADER = (
    "accepted_source",
    "accepted_relation",
    "accepted_consumer",
    "accepted_declaration_source",
    "accepted_fingerprint",
    "proposed_source",
    "proposed_relation",
    "proposed_consumer",
    "proposed_declaration_source",
    "proposed_fingerprint",
    "disposition",
)


@dataclass(frozen=True, slots=True)
class MigrationCase:
    id: str
    registry: str
    expected: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MigrationRecord:
    source: str
    relation: str
    consumer: str
    declaration_source: str
    fingerprint: str

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.source, self.relation, self.consumer)


@dataclass(frozen=True, slots=True)
class EvidenceRow:
    accepted: MigrationRecord | None
    proposed: MigrationRecord | None
    disposition: str


@dataclass(frozen=True, slots=True)
class PolicyImpactMigrationCheck:
    id: str
    evidence: str
    accepted_tree: str
    accepted_registry: str
    proposed_registry: str
    cases: tuple[MigrationCase, ...]

    def run(self, context: CheckContext) -> list[Diagnostic]:
        rows = _load_evidence(context, self.id, self.evidence)
        with _materialized_tree(context, self.id, self.accepted_tree) as accepted_name:
            accepted = _compile(
                Path(accepted_name),
                self.accepted_registry,
                context,
                self.id,
            )
        proposed = _compile(
            context.repo_root,
            self.proposed_registry,
            context,
            self.id,
        )
        diagnostics = _compare(rows, accepted, proposed, context, self.id, self.evidence)
        for case in self.cases:
            observed = tuple(
                item.code
                for item in _compare(
                    rows,
                    accepted,
                    _compile(context.repo_root, case.registry, context, self.id),
                    context,
                    self.id,
                    self.evidence,
                )
            )
            if observed != case.expected:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.POLICY_IMPACT_MIGRATION_FIXTURE",
                        "migration fixture diagnostics do not match",
                        path=case.registry,
                        field=case.id,
                        expected=",".join(case.expected) or "pass",
                        observed=",".join(observed) or "pass",
                    )
                )
        return diagnostics


def _compile(
    root: Path,
    registry: str,
    context: CheckContext,
    check: str,
) -> tuple[MigrationRecord, ...]:
    try:
        corpus = load_canonical_standards_corpus(root)
        compiled = compile_policy_impact(root, corpus, registry)
    except (MetadataError, PolicyImpactError) as error:
        failure = error.failure
        raise EngineError(
            Diagnostic(
                failure.code,
                failure.outcome,
                failure.message,
                suite=context.suite_id,
                check=check,
                path=failure.path,
                field=failure.field,
                observed=failure.observed,
            )
        ) from error
    return tuple(
        MigrationRecord(
            semantics.source,
            semantics.relation,
            semantics.consumer,
            semantics.declaration_source,
            semantics.dependency_fingerprint,
        )
        for semantics in sorted(
            compiled.semantics.values(),
            key=lambda item: (item.source, item.relation, item.consumer),
        )
    )


def _materialized_tree(
    context: CheckContext,
    check: str,
    tree: str,
) -> tempfile.TemporaryDirectory:
    if len(tree) != 40 or any(character not in "0123456789abcdef" for character in tree):
        raise EngineError(
            Diagnostic(
                "CONFIG.POLICY_IMPACT_MIGRATION_TREE",
                "invalid",
                "accepted_tree must be a lowercase full Git tree identity",
                suite=context.suite_id,
                check=check,
                observed=tree,
            )
        )
    completed = subprocess.run(
        ("git", "archive", "--format=tar", tree),
        cwd=context.repo_root,
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise EngineError(
            Diagnostic(
                "POLICY_IMPACT_MIGRATION.ACCEPTED_TREE_UNAVAILABLE",
                "unavailable",
                "accepted policy-impact tree cannot be materialized",
                suite=context.suite_id,
                check=check,
                observed=tree,
            )
        )
    temporary = tempfile.TemporaryDirectory()
    destination = Path(temporary.name)
    try:
        with tarfile.open(fileobj=io.BytesIO(completed.stdout), mode="r:") as archive:
            for member in archive.getmembers():
                relative = PurePosixPath(member.name)
                if (
                    relative.is_absolute()
                    or ".." in relative.parts
                    or not (member.isdir() or member.isfile())
                ):
                    raise EngineError(
                        Diagnostic(
                            "POLICY_IMPACT_MIGRATION.ACCEPTED_TREE_INVALID",
                            "invalid",
                            "accepted policy-impact tree contains an unsupported entry",
                            suite=context.suite_id,
                            check=check,
                            path=member.name,
                        )
                    )
                target = destination.joinpath(*relative.parts)
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                source = archive.extractfile(member)
                if source is None:
                    raise AssertionError("regular archive member has no content")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read())
    except Exception:
        temporary.cleanup()
        raise
    return temporary


def _load_evidence(
    context: CheckContext,
    check: str,
    path: str,
) -> tuple[EvidenceRow, ...]:
    source = contained_file(
        context.repo_root,
        path,
        suite=context.suite_id,
        check=check,
    )
    with source.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != EVIDENCE_HEADER:
            raise EngineError(
                Diagnostic(
                    "CONFIG.POLICY_IMPACT_MIGRATION_HEADER",
                    "invalid",
                    "migration evidence has the wrong header",
                    suite=context.suite_id,
                    check=check,
                    path=path,
                )
            )
        rows = tuple(
            _evidence_row(raw, context, check, path, line)
            for line, raw in enumerate(reader, 2)
        )
    if not rows:
        raise EngineError(
            Diagnostic(
                "CONFIG.POLICY_IMPACT_MIGRATION_EMPTY",
                "invalid",
                "migration evidence must contain at least one disposition",
                suite=context.suite_id,
                check=check,
                path=path,
            )
        )
    return rows


def _evidence_row(
    raw: dict[str, str],
    context: CheckContext,
    check: str,
    path: str,
    line: int,
) -> EvidenceRow:
    accepted = _record(raw, "accepted", context, check, path, line)
    proposed = _record(raw, "proposed", context, check, path, line)
    if accepted is None and proposed is None:
        raise EngineError(
            Diagnostic(
                "CONFIG.POLICY_IMPACT_MIGRATION_ROW",
                "invalid",
                "migration row must identify accepted or proposed semantics",
                suite=context.suite_id,
                check=check,
                path=path,
                row=line,
            )
        )
    disposition = raw["disposition"]
    expected = _expected_disposition(accepted, proposed)
    if disposition != expected:
        raise EngineError(
            Diagnostic(
                "CONFIG.POLICY_IMPACT_MIGRATION_DISPOSITION",
                "invalid",
                "migration disposition does not match its exact semantic states",
                suite=context.suite_id,
                check=check,
                path=path,
                row=line,
                field="disposition",
                expected=expected,
                observed=disposition,
            )
        )
    return EvidenceRow(accepted, proposed, disposition)


def _record(
    raw: dict[str, str],
    prefix: str,
    context: CheckContext,
    check: str,
    path: str,
    line: int,
) -> MigrationRecord | None:
    values = tuple(
        raw[f"{prefix}_{field}"]
        for field in ("source", "relation", "consumer", "declaration_source", "fingerprint")
    )
    if not any(values):
        return None
    if not all(values):
        raise EngineError(
            Diagnostic(
                "CONFIG.POLICY_IMPACT_MIGRATION_RECORD",
                "invalid",
                "migration semantic record must be wholly present or absent",
                suite=context.suite_id,
                check=check,
                path=path,
                row=line,
                field=prefix,
            )
        )
    return MigrationRecord(*values)


def _expected_disposition(
    accepted: MigrationRecord | None,
    proposed: MigrationRecord | None,
) -> str:
    if accepted is None:
        return "add"
    if proposed is None:
        return "retire"
    if accepted.key != proposed.key:
        return "replace"
    return "retain" if accepted.fingerprint == proposed.fingerprint else "correct"


def _compare(
    rows: tuple[EvidenceRow, ...],
    accepted: tuple[MigrationRecord, ...],
    proposed: tuple[MigrationRecord, ...],
    context: CheckContext,
    check: str,
    path: str,
) -> list[Diagnostic]:
    expected_accepted = _indexed(rows, "accepted", context, check, path)
    expected_proposed = _indexed(rows, "proposed", context, check, path)
    actual_accepted = {record.key: record for record in accepted}
    actual_proposed = {record.key: record for record in proposed}

    expected_sources = {record.declaration_source for record in expected_proposed.values()}
    actual_sources = {record.declaration_source for record in actual_proposed.values()}
    missing_sources = sorted(expected_sources - actual_sources)
    unexpected_sources = sorted(actual_sources - expected_sources)
    if missing_sources:
        return [
            _diagnostic(
                context,
                check,
                "POLICY_IMPACT_MIGRATION.MISSING_SOURCE",
                "closed policy-impact registry omits an admitted declaration source",
                path=path,
                expected="|".join(sorted(expected_sources)),
                observed="|".join(sorted(actual_sources)),
            )
        ]
    if unexpected_sources:
        return [
            _diagnostic(
                context,
                check,
                "POLICY_IMPACT_MIGRATION.UNEXPECTED_SOURCE",
                "closed policy-impact registry includes an undisposed declaration source",
                path=path,
                expected="|".join(sorted(expected_sources)),
                observed="|".join(sorted(actual_sources)),
            )
        ]

    diagnostics: list[Diagnostic] = []
    for label, expected, actual in (
        ("accepted", expected_accepted, actual_accepted),
        ("proposed", expected_proposed, actual_proposed),
    ):
        if set(expected) != set(actual):
            diagnostics.append(
                _diagnostic(
                    context,
                    check,
                    f"POLICY_IMPACT_MIGRATION.{label.upper()}_SET",
                    f"{label} relationship natural keys differ from migration evidence",
                    path=path,
                    expected=repr(sorted(expected)),
                    observed=repr(sorted(actual)),
                )
            )
            continue
        changed = sorted(
            key
            for key in expected
            if expected[key] != actual[key]
        )
        if changed:
            diagnostics.append(
                _diagnostic(
                    context,
                    check,
                    f"POLICY_IMPACT_MIGRATION.{label.upper()}_SEMANTICS",
                    f"{label} relationship semantics differ from migration evidence",
                    path=path,
                    observed=repr(changed),
                )
            )
    return diagnostics


def _indexed(
    rows: tuple[EvidenceRow, ...],
    side: str,
    context: CheckContext,
    check: str,
    path: str,
) -> dict[tuple[str, str, str], MigrationRecord]:
    result: dict[tuple[str, str, str], MigrationRecord] = {}
    for row in rows:
        record = getattr(row, side)
        if record is None:
            continue
        if record.key in result:
            raise EngineError(
                Diagnostic(
                    "CONFIG.POLICY_IMPACT_MIGRATION_DUPLICATE",
                    "invalid",
                    "migration evidence duplicates one natural key",
                    suite=context.suite_id,
                    check=check,
                    path=path,
                    field=side,
                    observed="|".join(record.key),
                )
            )
        result[record.key] = record
    return result


def _diagnostic(
    context: CheckContext,
    check: str,
    code: str,
    message: str,
    *,
    path: str,
    field: str | None = None,
    expected: str | None = None,
    observed: str | None = None,
) -> Diagnostic:
    return Diagnostic(
        code,
        "invalid",
        message,
        suite=context.suite_id,
        check=check,
        path=path,
        field=field,
        expected=expected,
        observed=observed,
    )


def _required_string(raw: dict[str, Any], field: str, suite: str, check: str) -> str:
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
    return value


def parse_policy_impact_migration_check(
    raw: dict[str, Any],
    suite_id: str,
) -> PolicyImpactMigrationCheck:
    allowed = {
        "id",
        "type",
        "evidence",
        "accepted_tree",
        "accepted_registry",
        "proposed_registry",
        "cases",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "policy-impact migration check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = _required_string(raw, "id", suite_id, "policy-impact-migration")
    raw_cases = raw.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise EngineError(
            Diagnostic(
                "CONFIG.POLICY_IMPACT_MIGRATION_CASES",
                "invalid",
                "policy-impact migration check requires at least one negative case",
                suite=suite_id,
                check=check_id,
            )
        )
    cases: list[MigrationCase] = []
    seen: set[str] = set()
    for case in raw_cases:
        if not isinstance(case, dict) or set(case) != {"id", "registry", "expected"}:
            raise EngineError(
                Diagnostic(
                    "CONFIG.POLICY_IMPACT_MIGRATION_CASE",
                    "invalid",
                    "migration case requires exactly id, registry, and expected",
                    suite=suite_id,
                    check=check_id,
                )
            )
        case_id = case["id"]
        registry = case["registry"]
        expected = case["expected"]
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise EngineError(
                Diagnostic(
                    "CONFIG.POLICY_IMPACT_MIGRATION_CASE_ID",
                    "invalid",
                    "migration case ids must be unique non-empty strings",
                    suite=suite_id,
                    check=check_id,
                    observed=str(case_id),
                )
            )
        if not isinstance(registry, str) or not registry:
            raise EngineError(
                Diagnostic(
                    "CONFIG.POLICY_IMPACT_MIGRATION_CASE_REGISTRY",
                    "invalid",
                    "migration case registry must be a non-empty path",
                    suite=suite_id,
                    check=check_id,
                    field=case_id,
                )
            )
        if (
            not isinstance(expected, list)
            or any(not isinstance(item, str) or not item for item in expected)
            or len(set(expected)) != len(expected)
        ):
            raise EngineError(
                Diagnostic(
                    "CONFIG.POLICY_IMPACT_MIGRATION_CASE_EXPECTED",
                    "invalid",
                    "migration case diagnostics must be unique non-empty strings",
                    suite=suite_id,
                    check=check_id,
                    field=case_id,
                )
            )
        seen.add(case_id)
        cases.append(MigrationCase(case_id, registry, tuple(expected)))
    return PolicyImpactMigrationCheck(
        check_id,
        _required_string(raw, "evidence", suite_id, check_id),
        _required_string(raw, "accepted_tree", suite_id, check_id),
        _required_string(raw, "accepted_registry", suite_id, check_id),
        _required_string(raw, "proposed_registry", suite_id, check_id),
        tuple(cases),
    )
