from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, CheckFileInput, present_inputs
from ..paths import contained_path
from .table import read_table_rows


MIGRATION_TERMINAL_TRIGGER = "zero-bash-accepted"
MIGRATION_CHECK_KINDS = ("execution_train",)

TRAIN_HEADER = (
    "order",
    "wave",
    "start_id",
    "end_id",
    "source",
    "owner",
    "owner_state",
    "activation",
    "checkpoint",
)
DECOMPOSITION_HEADER = (
    "baseline_order",
    "child_order",
    "ids",
    "source",
    "owner",
    "owner_state",
    "activation",
    "checkpoint",
    "rationale",
    "owner_transition",
)
OWNER_MAP_HEADER = (
    "id",
    "current_path",
    "line",
    "future_owner",
    "disposition",
    "heading",
)
DISPOSITIONS_HEADER = ("id", "source", "target", "disposition", "rationale")

WAVES = frozenset(
    {
        "trust-boundaries",
        "lifecycle-runtime",
        "process-dependencies",
        "application-boundaries",
        "reference-index-closure",
    }
)
OWNER_STATES = frozenset({"exists", "missing"})
ACTIVATIONS = frozenset({"pre-slice-review", "owner-review", "final-closure"})
CHECKPOINTS = frozenset({"focused", "full-suite"})
OWNER_TRANSITIONS = frozenset({"none", "missing-to-exists"})
IDENTIFIER = re.compile(r"STD-([0-9]{4})\Z")


@dataclass(frozen=True, slots=True)
class OwnerRecord:
    source: str
    owner: str


@dataclass(frozen=True, slots=True)
class TrainRow:
    line: int
    order: int
    wave: str
    start_id: str
    end_id: str
    source: str
    owner: str
    owner_state: str
    activation: str
    checkpoint: str


@dataclass(frozen=True, slots=True)
class DecompositionRow:
    line: int
    baseline_order: int
    child_order: int
    ids: tuple[str, ...]
    source: str
    owner: str
    owner_state: str
    activation: str
    checkpoint: str
    rationale: str
    owner_transition: str


@dataclass(frozen=True, slots=True)
class _Violation(Exception):
    code: str
    message: str
    path: str
    row: int | None = None
    field: str | None = None
    expected: str | None = None
    observed: str | None = None


@dataclass(frozen=True, slots=True)
class ExecutionTrainCheck:
    id: str
    train_path: str
    decomposition_path: str
    owner_map_path: str
    dispositions_path: str
    expected_train_rows: int
    expected_baseline_ids: int
    expected_checkpoints: int

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        owners = self._declared_owner_paths(context)
        owner_inputs = tuple(
            CheckFileInput(
                owner,
                "present"
                if contained_path(
                    context.repo_root,
                    owner,
                    suite=context.suite_id,
                    check=self.id,
                ).exists()
                else "absent",
                "owner-state",
            )
            for owner in owners
        )
        return (
            *present_inputs("execution-train", self.train_path),
            *present_inputs("execution-decomposition", self.decomposition_path),
            *present_inputs("owner-map", self.owner_map_path),
            *present_inputs("dispositions", self.dispositions_path),
            *owner_inputs,
        )

    def run(self, context: CheckContext) -> list[Diagnostic]:
        try:
            self._validate(context)
        except _Violation as violation:
            return [
                Diagnostic(
                    violation.code,
                    "invalid",
                    violation.message,
                    suite=context.suite_id,
                    check=self.id,
                    path=violation.path,
                    row=violation.row,
                    field=violation.field,
                    expected=violation.expected,
                    observed=violation.observed,
                )
            ]
        return []

    def _declared_owner_paths(self, context: CheckContext) -> tuple[str, ...]:
        train = read_table_rows(
            context.repo_root,
            self.train_path,
            TRAIN_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        decomposition = read_table_rows(
            context.repo_root,
            self.decomposition_path,
            DECOMPOSITION_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        return tuple(
            sorted({row["owner"] for row in (*train, *decomposition) if row["owner"]})
        )

    def _validate(self, context: CheckContext) -> None:
        owner_rows = read_table_rows(
            context.repo_root,
            self.owner_map_path,
            OWNER_MAP_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        owners: dict[str, OwnerRecord] = {}
        for line, row in enumerate(owner_rows, start=2):
            identifier = row["id"]
            self._identifier_number(identifier, self.owner_map_path, line, "id")
            if identifier in owners:
                self._fail(
                    "ASSERT.EXECUTION_TRAIN.DUPLICATE_OWNER_ID",
                    "owner map identifier is duplicated",
                    self.owner_map_path,
                    line,
                    "id",
                    expected="unique",
                    observed=identifier,
                )
            if not row["current_path"] or not row["future_owner"]:
                self._fail(
                    "ASSERT.EXECUTION_TRAIN.OWNER_MAP",
                    "owner map source and owner must be non-empty",
                    self.owner_map_path,
                    line,
                )
            owners[identifier] = OwnerRecord(
                row["current_path"], row["future_owner"]
            )

        disposition_rows = read_table_rows(
            context.repo_root,
            self.dispositions_path,
            DISPOSITIONS_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        disposed: set[str] = set()
        for line, row in enumerate(disposition_rows, start=2):
            identifier = row["id"]
            self._identifier_number(
                identifier, self.dispositions_path, line, "id"
            )
            if identifier in disposed:
                self._fail(
                    "ASSERT.EXECUTION_TRAIN.DUPLICATE_DISPOSITION",
                    "disposition identifier is duplicated",
                    self.dispositions_path,
                    line,
                    "id",
                    expected="unique",
                    observed=identifier,
                )
            disposed.add(identifier)

        decomposition = self._decomposition_rows(context)
        if not decomposition:
            self._fail(
                "ASSERT.EXECUTION_TRAIN.EMPTY_DECOMPOSITION",
                "execution decomposition must contain at least one row",
                self.decomposition_path,
            )
        by_order: dict[int, list[DecompositionRow]] = {}
        for row in decomposition:
            by_order.setdefault(row.baseline_order, []).append(row)

        train = self._train_rows(context)
        if len(train) != self.expected_train_rows:
            self._fail(
                "ASSERT.EXECUTION_TRAIN.ROW_COUNT",
                "execution train row count differs from the immutable baseline",
                self.train_path,
                expected=str(self.expected_train_rows),
                observed=str(len(train)),
            )

        seen: set[str] = set()
        completed_id_count = 0
        checkpoint_count = 0
        active_label: str | None = None
        declared_transitions: set[str] = set()
        completed_transitions: set[str] = set()
        used_decomposition_orders: set[int] = set()

        def process_cluster(label: str, ids: tuple[str, ...], line: int) -> None:
            nonlocal active_label, completed_id_count
            if not ids:
                self._fail(
                    "ASSERT.EXECUTION_TRAIN.EMPTY_CLUSTER",
                    "logical cluster must contain at least one identifier",
                    self.decomposition_path,
                    line,
                    "ids",
                )
            completed = sum(identifier in disposed for identifier in ids)
            if completed == len(ids):
                if active_label is not None:
                    self._fail(
                        "ASSERT.EXECUTION_TRAIN.ACTIVE_ORDER",
                        "completed logical cluster appears after the active frontier",
                        self.decomposition_path,
                        line,
                        expected=f"pending after {active_label}",
                        observed=label,
                    )
                completed_id_count += len(ids)
            elif completed == 0:
                if active_label is None:
                    active_label = label
            else:
                self._fail(
                    "ASSERT.EXECUTION_TRAIN.PARTIAL_CLUSTER",
                    "logical cluster is partially disposed",
                    self.decomposition_path,
                    line,
                    "ids",
                    expected="all or none",
                    observed=f"{completed}/{len(ids)}",
                )

        for row in train:
            identifiers = tuple(
                f"STD-{number:04d}"
                for number in range(
                    self._identifier_number(
                        row.start_id, self.train_path, row.line, "start_id"
                    ),
                    self._identifier_number(
                        row.end_id, self.train_path, row.line, "end_id"
                    )
                    + 1,
                )
            )
            if not identifiers:
                self._fail(
                    "ASSERT.EXECUTION_TRAIN.RANGE",
                    "execution train range is reversed",
                    self.train_path,
                    row.line,
                    "start_id,end_id",
                    observed=f"{row.start_id},{row.end_id}",
                )
            for identifier in identifiers:
                if identifier in seen:
                    self._fail(
                        "ASSERT.EXECUTION_TRAIN.DUPLICATE_ID",
                        "execution train identifier appears more than once",
                        self.train_path,
                        row.line,
                        "start_id,end_id",
                        expected="unique",
                        observed=identifier,
                    )
                owner = owners.get(identifier)
                if owner is None:
                    self._fail(
                        "ASSERT.EXECUTION_TRAIN.OWNER_MAP",
                        "execution train identifier is absent from the owner map",
                        self.owner_map_path,
                        field="id",
                        observed=identifier,
                    )
                if owner.source != row.source or owner.owner != row.owner:
                    self._fail(
                        "ASSERT.EXECUTION_TRAIN.OWNER_ALIGNMENT",
                        "execution train source or owner differs from the owner map",
                        self.train_path,
                        row.line,
                        "source,owner",
                        expected=f"{owner.source},{owner.owner}",
                        observed=f"{row.source},{row.owner}",
                    )
                seen.add(identifier)

            effective_owner_state = row.owner_state
            if row.owner in completed_transitions:
                if row.owner_state != "missing":
                    self._fail(
                        "ASSERT.EXECUTION_TRAIN.OWNER_TRANSITION",
                        "a completed creation may only override a missing baseline",
                        self.train_path,
                        row.line,
                        "owner_state",
                        expected="missing",
                        observed=row.owner_state,
                    )
                effective_owner_state = "exists"

            children = by_order.get(row.order)
            if children:
                used_decomposition_orders.add(row.order)
                child_seen: set[str] = set()
                transition_complete = False
                transition_count = 0
                for expected_child_order, child in enumerate(children, start=1):
                    if child.child_order != expected_child_order:
                        self._fail(
                            "ASSERT.EXECUTION_TRAIN.CHILD_ORDER",
                            "decomposition child order is not contiguous",
                            self.decomposition_path,
                            child.line,
                            "child_order",
                            expected=str(expected_child_order),
                            observed=str(child.child_order),
                        )
                    if child.source != row.source:
                        self._fail(
                            "ASSERT.EXECUTION_TRAIN.CHILD_SOURCE",
                            "decomposition child source differs from its baseline",
                            self.decomposition_path,
                            child.line,
                            "source",
                            expected=row.source,
                            observed=child.source,
                        )
                    if (
                        child.activation == "final-closure"
                        and row.wave != "reference-index-closure"
                    ):
                        self._fail(
                            "ASSERT.EXECUTION_TRAIN.FINAL_CLOSURE",
                            "final closure is outside the reference-index wave",
                            self.decomposition_path,
                            child.line,
                            "activation",
                        )
                    if child.owner_transition == "missing-to-exists":
                        transition_count += 1
                        if (
                            transition_count != 1
                            or row.owner_state != "missing"
                            or child.owner != row.owner
                            or child.owner in declared_transitions
                            or child.owner_state != "exists"
                            or child.activation != "owner-review"
                        ):
                            self._fail(
                                "ASSERT.EXECUTION_TRAIN.OWNER_TRANSITION",
                                "owner creation transition is contradictory or "
                                "duplicated",
                                self.decomposition_path,
                                child.line,
                                "owner_transition",
                                observed=child.owner_transition,
                            )
                        declared_transitions.add(child.owner)
                        transitioned = sum(
                            identifier in disposed for identifier in child.ids
                        )
                        if transitioned not in {0, len(child.ids)}:
                            self._fail(
                                "ASSERT.EXECUTION_TRAIN.PARTIAL_TRANSITION",
                                "owner creation transition is partially complete",
                                self.decomposition_path,
                                child.line,
                                "ids",
                                expected="all or none",
                                observed=f"{transitioned}/{len(child.ids)}",
                            )
                        transition_complete = transitioned == len(child.ids)
                    elif child.owner != row.owner:
                        if (
                            child.owner_state == "missing"
                            and child.activation != "owner-review"
                        ):
                            self._fail(
                                "ASSERT.EXECUTION_TRAIN.OWNER_STATE",
                                "missing child owner requires owner-review "
                                "activation",
                                self.decomposition_path,
                                child.line,
                                "activation",
                                expected="owner-review",
                                observed=child.activation,
                            )
                        self._assert_owner_path(
                            context,
                            child.owner,
                            child.owner_state,
                            self.decomposition_path,
                            child.line,
                        )

                    for identifier in child.ids:
                        if identifier not in identifiers or identifier in child_seen:
                            self._fail(
                                "ASSERT.EXECUTION_TRAIN.DECOMPOSITION_COVERAGE",
                                "decomposition identifier is duplicated or outside "
                                "its baseline",
                                self.decomposition_path,
                                child.line,
                                "ids",
                                observed=identifier,
                            )
                        owner = owners.get(identifier)
                        if owner is None or owner.source != row.source:
                            self._fail(
                                "ASSERT.EXECUTION_TRAIN.CHILD_SOURCE",
                                "decomposition identifier source differs from the "
                                "owner map",
                                self.decomposition_path,
                                child.line,
                                "ids",
                                observed=identifier,
                            )
                        child_seen.add(identifier)
                    process_cluster(
                        f"{row.order}.{child.child_order}", child.ids, child.line
                    )
                if child_seen != set(identifiers):
                    self._fail(
                        "ASSERT.EXECUTION_TRAIN.DECOMPOSITION_COVERAGE",
                        "decomposition children do not exactly cover their baseline",
                        self.decomposition_path,
                        children[0].line,
                        "ids",
                        expected=str(len(identifiers)),
                        observed=str(len(child_seen)),
                    )
                if transition_count > 1:
                    self._fail(
                        "ASSERT.EXECUTION_TRAIN.OWNER_TRANSITION",
                        "baseline row declares more than one owner transition",
                        self.decomposition_path,
                        children[0].line,
                    )
                if transition_complete:
                    completed_transitions.add(row.owner)
                    effective_owner_state = "exists"
            else:
                process_cluster(str(row.order), identifiers, row.line)

            self._assert_owner_path(
                context,
                row.owner,
                effective_owner_state,
                self.train_path,
                row.line,
            )
            if row.checkpoint == "full-suite":
                checkpoint_count += 1

        unknown_orders = sorted(set(by_order) - used_decomposition_orders)
        if unknown_orders:
            self._fail(
                "ASSERT.EXECUTION_TRAIN.UNKNOWN_BASELINE",
                "decomposition references an unknown baseline order",
                self.decomposition_path,
                field="baseline_order",
                observed=",".join(str(order) for order in unknown_orders),
            )
        if len(seen) != self.expected_baseline_ids:
            self._fail(
                "ASSERT.EXECUTION_TRAIN.BASELINE_COUNT",
                "execution train identifier count differs from the immutable baseline",
                self.train_path,
                expected=str(self.expected_baseline_ids),
                observed=str(len(seen)),
            )
        if checkpoint_count != self.expected_checkpoints:
            self._fail(
                "ASSERT.EXECUTION_TRAIN.CHECKPOINT_COUNT",
                "full-suite checkpoint count differs from the immutable baseline",
                self.train_path,
                expected=str(self.expected_checkpoints),
                observed=str(checkpoint_count),
            )

        remaining = set(owners) - disposed
        expected_remaining = len(seen) - completed_id_count
        if len(remaining) != expected_remaining or not remaining.issubset(seen):
            self._fail(
                "ASSERT.EXECUTION_TRAIN.REMAINING_COVERAGE",
                "remaining owner-map identifiers do not equal train progress",
                self.owner_map_path,
                expected=f"{expected_remaining} identifiers within train",
                observed=f"{len(remaining)} identifiers",
            )

    def _train_rows(self, context: CheckContext) -> tuple[TrainRow, ...]:
        rows = read_table_rows(
            context.repo_root,
            self.train_path,
            TRAIN_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        parsed: list[TrainRow] = []
        for expected_order, (line, row) in enumerate(
            zip(range(2, len(rows) + 2), rows), start=1
        ):
            order = self._positive_integer(
                row["order"], self.train_path, line, "order"
            )
            if order != expected_order:
                self._fail(
                    "ASSERT.EXECUTION_TRAIN.ORDER",
                    "execution train order is not contiguous",
                    self.train_path,
                    line,
                    "order",
                    expected=str(expected_order),
                    observed=str(order),
                )
            self._domain(row["wave"], WAVES, self.train_path, line, "wave")
            self._domain(
                row["owner_state"],
                OWNER_STATES,
                self.train_path,
                line,
                "owner_state",
            )
            self._domain(
                row["activation"],
                ACTIVATIONS,
                self.train_path,
                line,
                "activation",
            )
            self._domain(
                row["checkpoint"],
                CHECKPOINTS,
                self.train_path,
                line,
                "checkpoint",
            )
            if not row["source"] or not row["owner"]:
                self._fail(
                    "ASSERT.EXECUTION_TRAIN.EMPTY_VALUE",
                    "execution train source and owner must be non-empty",
                    self.train_path,
                    line,
                )
            if row["owner_state"] == "missing" and row["activation"] != "owner-review":
                self._fail(
                    "ASSERT.EXECUTION_TRAIN.OWNER_STATE",
                    "missing owner requires owner-review activation",
                    self.train_path,
                    line,
                    "activation",
                    expected="owner-review",
                    observed=row["activation"],
                )
            if (
                row["activation"] == "final-closure"
                and row["wave"] != "reference-index-closure"
            ):
                self._fail(
                    "ASSERT.EXECUTION_TRAIN.FINAL_CLOSURE",
                    "final closure is outside the reference-index wave",
                    self.train_path,
                    line,
                    "activation",
                )
            parsed.append(
                TrainRow(
                    line,
                    order,
                    row["wave"],
                    row["start_id"],
                    row["end_id"],
                    row["source"],
                    row["owner"],
                    row["owner_state"],
                    row["activation"],
                    row["checkpoint"],
                )
            )
        return tuple(parsed)

    def _decomposition_rows(
        self, context: CheckContext
    ) -> tuple[DecompositionRow, ...]:
        rows = read_table_rows(
            context.repo_root,
            self.decomposition_path,
            DECOMPOSITION_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        parsed: list[DecompositionRow] = []
        for line, row in enumerate(rows, start=2):
            for field in ("ids", "source", "owner", "rationale"):
                if not row[field]:
                    self._fail(
                        "ASSERT.EXECUTION_TRAIN.EMPTY_VALUE",
                        "decomposition required value is empty",
                        self.decomposition_path,
                        line,
                        field,
                    )
            self._domain(
                row["owner_state"],
                OWNER_STATES,
                self.decomposition_path,
                line,
                "owner_state",
            )
            self._domain(
                row["activation"],
                ACTIVATIONS,
                self.decomposition_path,
                line,
                "activation",
            )
            self._domain(
                row["checkpoint"],
                {"focused"},
                self.decomposition_path,
                line,
                "checkpoint",
            )
            self._domain(
                row["owner_transition"],
                OWNER_TRANSITIONS,
                self.decomposition_path,
                line,
                "owner_transition",
            )
            ids = tuple(row["ids"].split(","))
            for identifier in ids:
                self._identifier_number(
                    identifier, self.decomposition_path, line, "ids"
                )
            parsed.append(
                DecompositionRow(
                    line,
                    self._positive_integer(
                        row["baseline_order"],
                        self.decomposition_path,
                        line,
                        "baseline_order",
                    ),
                    self._positive_integer(
                        row["child_order"],
                        self.decomposition_path,
                        line,
                        "child_order",
                    ),
                    ids,
                    row["source"],
                    row["owner"],
                    row["owner_state"],
                    row["activation"],
                    row["checkpoint"],
                    row["rationale"],
                    row["owner_transition"],
                )
            )
        return tuple(parsed)

    def _assert_owner_path(
        self,
        context: CheckContext,
        owner: str,
        expected_state: str,
        source_path: str,
        line: int,
    ) -> None:
        path = contained_path(
            context.repo_root,
            owner,
            suite=context.suite_id,
            check=self.id,
        )
        observed = "exists" if path.exists() else "missing"
        if observed != expected_state:
            self._fail(
                "ASSERT.EXECUTION_TRAIN.OWNER_PATH",
                "owner path state differs from the effective lifecycle state",
                source_path,
                line,
                "owner_state",
                expected=expected_state,
                observed=observed,
            )

    def _identifier_number(
        self, value: str, path: str, line: int, field: str
    ) -> int:
        match = IDENTIFIER.fullmatch(value)
        if match is None:
            self._fail(
                "ASSERT.EXECUTION_TRAIN.IDENTIFIER",
                "identifier must use exact STD-NNNN form",
                path,
                line,
                field,
                observed=value,
            )
        return int(match.group(1))

    def _positive_integer(
        self, value: str, path: str, line: int, field: str
    ) -> int:
        if not value.isascii() or not value.isdigit() or int(value) < 1:
            self._fail(
                "ASSERT.EXECUTION_TRAIN.INTEGER",
                "field must be a positive base-10 integer",
                path,
                line,
                field,
                observed=value,
            )
        return int(value)

    def _domain(
        self,
        value: str,
        allowed: frozenset[str] | set[str],
        path: str,
        line: int,
        field: str,
    ) -> None:
        if value not in allowed:
            self._fail(
                "ASSERT.EXECUTION_TRAIN.DOMAIN",
                "field value is outside its closed domain",
                path,
                line,
                field,
                expected=",".join(sorted(allowed)),
                observed=value,
            )

    def _fail(
        self,
        code: str,
        message: str,
        path: str,
        row: int | None = None,
        field: str | None = None,
        *,
        expected: str | None = None,
        observed: str | None = None,
    ) -> None:
        raise _Violation(code, message, path, row, field, expected, observed)


def _required_string(
    raw: dict[str, Any], field: str, suite_id: str, check_id: str
) -> str:
    value = raw.get(field)
    if type(value) is not str or not value:
        raise EngineError(
            Diagnostic(
                "CONFIG.STRING",
                "invalid",
                "execution_train paths must be non-empty strings",
                suite=suite_id,
                check=check_id,
                field=field,
            )
        )
    return value


def _required_positive_integer(
    raw: dict[str, Any], field: str, suite_id: str, check_id: str
) -> int:
    value = raw.get(field)
    if type(value) is not int or value < 1:
        raise EngineError(
            Diagnostic(
                "CONFIG.INTEGER",
                "invalid",
                "execution_train counts must be positive integers",
                suite=suite_id,
                check=check_id,
                field=field,
            )
        )
    return value


def parse_execution_train_check(
    raw: dict[str, Any], suite_id: str
) -> ExecutionTrainCheck:
    allowed = {
        "id",
        "type",
        "train_path",
        "decomposition_path",
        "owner_map_path",
        "dispositions_path",
        "expected_train_rows",
        "expected_baseline_ids",
        "expected_checkpoints",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "execution_train check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    if type(check_id) is not str or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    return ExecutionTrainCheck(
        check_id,
        _required_string(raw, "train_path", suite_id, check_id),
        _required_string(raw, "decomposition_path", suite_id, check_id),
        _required_string(raw, "owner_map_path", suite_id, check_id),
        _required_string(raw, "dispositions_path", suite_id, check_id),
        _required_positive_integer(raw, "expected_train_rows", suite_id, check_id),
        _required_positive_integer(
            raw, "expected_baseline_ids", suite_id, check_id
        ),
        _required_positive_integer(
            raw, "expected_checkpoints", suite_id, check_id
        ),
    )


__all__ = ("ExecutionTrainCheck", "parse_execution_train_check")
