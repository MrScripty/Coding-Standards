"""Route declared task scenarios through the Router and compare the outcome.

Each scenario row states task facts in the Router's own vocabulary. The check
binds them, asks the Router projection what it selects, and compares that with
the row's expected selections and with the reviewed route table. Nothing in a
row is compared with another column of the same table.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tools.standards_analysis.standards_analysis import (
    ROUTER_PROJECTION,
    AnalysisError,
    RouteDecision,
    RouterProjection,
    load_router_projection,
)
from tools.standards_applicability.standards_applicability import (
    ApplicabilityError,
    FactSet,
)
from tools.standards_metadata.standards_metadata import (
    MetadataError,
    load_canonical_module_corpus,
)

from ..diagnostics import OUTCOMES, Diagnostic, EngineError
from tools.standards_graph.standards_graph import (
    METADATA_REQUIRES,
    metadata_dependency_registry,
)
from ..model import CheckAuthorityInput, CheckContext, CheckInputContext, present_inputs
from .table import read_table_rows


EXPECTATIONS_HEADER = ("case", "direct_modules", "requires_closure")
CASE_COLUMN = "case"
# A fact cell is a comma-separated value list or one of these two words.
NO_VALUES = "none"
UNKNOWN_VALUE = "unknown"
SET_FACT_TYPES = frozenset({"enum-set", "string-set"})


@dataclass(frozen=True, slots=True)
class RouteSelection:
    column: str
    selected: str
    excluded: str
    module: str


@dataclass(frozen=True, slots=True)
class MetadataRouteCheck:
    id: str
    path: str
    header: tuple[str, ...]
    facts: tuple[str, ...]
    expectations_path: str
    route_column: str
    resolved: str
    unresolved: str
    selections: tuple[RouteSelection, ...]

    def authority_inputs(
        self, context: CheckInputContext
    ) -> tuple[CheckAuthorityInput, ...]:
        corpus = load_canonical_module_corpus(context.inputs)
        return (
            *present_inputs("routing-cases", self.path),
            *present_inputs("routing-expectations", self.expectations_path),
            *present_inputs("router-projection", ROUTER_PROJECTION),
            *present_inputs("canonical-module-corpus", corpus.path),
            *present_inputs("canonical-module", *corpus.members),
        )

    def run(self, context: CheckContext) -> list[Diagnostic]:
        rows = read_table_rows(
            context.repo_root,
            self.path,
            self.header,
            suite=context.suite_id,
            check=self.id,
        )
        if not rows:
            raise EngineError(
                Diagnostic(
                    "ROUTING.NO_SCENARIOS",
                    "invalid",
                    "routing decision table declares no scenario",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                )
            )
        expectations = read_table_rows(
            context.repo_root,
            self.expectations_path,
            EXPECTATIONS_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        indexed = self._expectations(context, expectations)
        diagnostics: list[Diagnostic] = []
        cases = [row[CASE_COLUMN] for row in rows]
        if len(set(cases)) != len(cases):
            raise EngineError(
                Diagnostic(
                    "ROUTING.DUPLICATE_CASE",
                    "invalid",
                    "routing decision cases must be unique",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                )
            )
        if set(cases) != set(indexed):
            diagnostics.append(
                self._diagnostic(
                    context,
                    "ASSERT.ROUTING_CASE_COVERAGE",
                    "route expectations must cover every decision case exactly",
                    expected=",".join(sorted(cases)),
                    observed=",".join(sorted(indexed)),
                )
            )
            return diagnostics

        try:
            corpus = load_canonical_module_corpus(context.repo_root)
            router = load_router_projection(context.repo_root, corpus)
        except (MetadataError, AnalysisError) as error:
            raise self._authority_error(context, error.failure) from error
        self._require_router_vocabulary(context, router)
        graph = metadata_dependency_registry(context.repo_root, corpus.modules)
        for row_number, row in enumerate(rows, start=2):
            case = row[CASE_COLUMN]
            decision = router.decide(self._bind(context, router, row, row_number))
            observed_route = (
                self.unresolved if decision.unresolved_facts else self.resolved
            )
            expected_route = row[self.route_column]
            if expected_route not in {self.resolved, self.unresolved}:
                diagnostics.append(
                    self._diagnostic(
                        context,
                        "ASSERT.ROUTING_STATE",
                        "route state is neither resolved nor unresolved",
                        row=row_number,
                        field=self.route_column,
                        observed=expected_route,
                    )
                )
                continue
            diagnostics.extend(
                self._selection_diagnostics(context, decision, row, row_number)
            )
            if observed_route != expected_route:
                diagnostics.append(
                    self._diagnostic(
                        context,
                        "ASSERT.ROUTING_RESOLUTION",
                        "the Router's resolution does not match the scenario",
                        row=row_number,
                        field=case,
                        expected=expected_route,
                        observed=",".join((observed_route, *decision.unresolved_facts)),
                    )
                )
                continue

            expected_direct, expected_closure = indexed[case]
            if observed_route == self.unresolved:
                if (expected_direct, expected_closure) != (
                    (self.unresolved,),
                    (self.unresolved,),
                ):
                    diagnostics.append(
                        self._diagnostic(
                            context,
                            "ASSERT.ROUTING_UNRESOLVED_EXPECTATION",
                            "an unresolved route must use unresolved expectations",
                            row=row_number,
                            field=case,
                        )
                    )
                continue
            observed_direct = tuple(sorted(decision.selected))
            observed_closure = graph.dependency_order(
                METADATA_REQUIRES,
                selected=observed_direct,
            )
            if observed_direct != expected_direct:
                diagnostics.append(
                    self._diagnostic(
                        context,
                        "ASSERT.ROUTING_DIRECT_MODULES",
                        "modules the Router selects do not match reviewed expectations",
                        row=row_number,
                        field=case,
                        expected=",".join(expected_direct),
                        observed=",".join(observed_direct),
                    )
                )
            if observed_closure != expected_closure:
                diagnostics.append(
                    self._diagnostic(
                        context,
                        "ASSERT.ROUTING_REQUIRES_CLOSURE",
                        "graph-derived Requires closure does not match reviewed expectations",
                        row=row_number,
                        field=case,
                        expected=",".join(expected_closure),
                        observed=",".join(observed_closure),
                    )
                )
        return diagnostics

    def _require_router_vocabulary(
        self, context: CheckContext, router: RouterProjection
    ) -> None:
        """Reject a table written in names the Router does not declare."""
        for fact_id in self.facts:
            definition = router.fact_schema.resolve(fact_id)
            if definition is None or definition.id != fact_id:
                raise self._vocabulary_error(
                    context,
                    "ROUTING.UNKNOWN_FACT",
                    "invalid",
                    "scenario column is not a fact the Router declares",
                    fact_id,
                )
            if definition.type not in SET_FACT_TYPES:
                raise self._vocabulary_error(
                    context,
                    "ROUTING.FACT_TYPE",
                    "unsupported",
                    "scenario columns support set-valued Router facts only",
                    fact_id,
                )
            if {NO_VALUES, UNKNOWN_VALUE} & set(definition.values):
                raise self._vocabulary_error(
                    context,
                    "ROUTING.FACT_TOKEN_COLLISION",
                    "unsupported",
                    "a Router fact value collides with a scenario cell keyword",
                    fact_id,
                )
        routable = {*router.base_modules, *(rule.target for rule in router.rules)}
        for selection in self.selections:
            if selection.module not in routable:
                raise self._vocabulary_error(
                    context,
                    "ROUTING.UNROUTED_MODULE",
                    "invalid",
                    "expected selection names a module the Router never selects",
                    selection.module,
                )

    def _bind(
        self,
        context: CheckContext,
        router: RouterProjection,
        row: dict[str, str],
        row_number: int,
    ) -> FactSet:
        """Bind one scenario; a fact without a column does not apply to it."""
        values: dict[str, object] = {}
        for definition in router.facts:
            if definition.id not in self.facts:
                values[definition.id] = {"type": definition.type, "state": "known-absent"}
                continue
            cell = row[definition.id]
            if cell == UNKNOWN_VALUE:
                values[definition.id] = {"type": definition.type, "state": "unknown"}
            else:
                values[definition.id] = {
                    "type": definition.type,
                    "state": "known",
                    "value": [] if cell == NO_VALUES else cell.split(","),
                }
        try:
            return router.fact_schema.bind(values)
        except ApplicabilityError as error:
            failure = error.failure
            raise EngineError(
                Diagnostic(
                    "ROUTING.FACT_VALUE",
                    "invalid",
                    f"scenario fact cell is not a Router value: {failure.message}",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    row=row_number,
                    field=failure.field,
                    observed=row.get(failure.field or "", failure.observed),
                )
            ) from error

    def _selection_diagnostics(
        self,
        context: CheckContext,
        decision: RouteDecision,
        row: dict[str, str],
        row_number: int,
    ) -> list[Diagnostic]:
        diagnostics = []
        unresolved_targets = set(decision.unresolved_targets)
        for selection in self.selections:
            expected = row[selection.column]
            if selection.module in decision.selected:
                observed = selection.selected
            elif selection.module in unresolved_targets:
                observed = self.unresolved
            else:
                observed = selection.excluded
            if expected not in {selection.selected, selection.excluded, self.unresolved}:
                diagnostics.append(
                    self._diagnostic(
                        context,
                        "ASSERT.ROUTING_SELECTION_VALUE",
                        "expected selection is not a declared selection value",
                        row=row_number,
                        field=selection.column,
                        observed=expected,
                    )
                )
            elif expected != observed:
                diagnostics.append(
                    self._diagnostic(
                        context,
                        "ASSERT.ROUTING_SELECTION",
                        "the Router's selection does not match the scenario",
                        row=row_number,
                        field=f"{row[CASE_COLUMN]}.{selection.column}",
                        expected=expected,
                        observed=observed,
                    )
                )
        return diagnostics

    def _vocabulary_error(
        self,
        context: CheckContext,
        code: str,
        outcome: str,
        message: str,
        observed: str,
    ) -> EngineError:
        return EngineError(
            Diagnostic(
                code,
                outcome,
                message,
                suite=context.suite_id,
                check=self.id,
                path=self.path,
                observed=observed,
            )
        )

    def _authority_error(self, context: CheckContext, failure: Any) -> EngineError:
        return EngineError(
            Diagnostic(
                failure.code,
                failure.outcome if failure.outcome in OUTCOMES else "invalid",
                failure.message,
                suite=context.suite_id,
                check=self.id,
                path=failure.path,
                row=getattr(failure, "row", None),
                field=failure.field,
                expected=getattr(failure, "expected", None),
                observed=failure.observed,
            )
        )

    def _expectations(
        self,
        context: CheckContext,
        rows: list[dict[str, str]],
    ) -> dict[str, tuple[tuple[str, ...], tuple[str, ...]]]:
        indexed: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {}
        for row_number, row in enumerate(rows, start=2):
            case = row["case"]
            if not case or case in indexed:
                raise EngineError(
                    Diagnostic(
                        "ROUTING.EXPECTATION_CASE",
                        "invalid",
                        "route expectation cases must be unique and non-empty",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.expectations_path,
                        row=row_number,
                        field="case",
                    )
                )
            direct = self._module_list(context, row["direct_modules"], row_number)
            closure = self._module_list(context, row["requires_closure"], row_number)
            indexed[case] = (direct, closure)
        return indexed

    def _module_list(
        self,
        context: CheckContext,
        value: str,
        row: int,
    ) -> tuple[str, ...]:
        values = tuple(value.split(","))
        if (
            not value
            or any(not item for item in values)
            or len(set(values)) != len(values)
        ):
            raise EngineError(
                Diagnostic(
                    "ROUTING.MODULE_LIST",
                    "invalid",
                    "route module lists must contain unique comma-separated IDs",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.expectations_path,
                    row=row,
                )
            )
        return values

    def _diagnostic(
        self,
        context: CheckContext,
        code: str,
        message: str,
        *,
        row: int | None = None,
        field: str | None = None,
        expected: str | None = None,
        observed: str | None = None,
    ) -> Diagnostic:
        return Diagnostic(
            code,
            "invalid",
            message,
            suite=context.suite_id,
            check=self.id,
            path=self.path,
            row=row,
            field=field,
            expected=expected,
            observed=observed,
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


def parse_metadata_route_check(raw: dict[str, Any], suite: str) -> MetadataRouteCheck:
    allowed = {
        "id",
        "type",
        "path",
        "header",
        "facts",
        "expectations_path",
        "route_column",
        "resolved",
        "unresolved",
        "selections",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "metadata route check contains unknown fields",
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
    strings = {}
    for field in (
        "path",
        "expectations_path",
        "route_column",
        "resolved",
        "unresolved",
    ):
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
        strings[field] = value
    header = _strings(raw.get("header"), "header", suite, check)
    facts = _strings(raw.get("facts"), "facts", suite, check)
    raw_selections = raw.get("selections")
    if not isinstance(raw_selections, list) or not raw_selections:
        raise EngineError(
            Diagnostic(
                "CONFIG.ROUTING_SELECTIONS",
                "invalid",
                "routing check requires selection mappings",
                suite=suite,
                check=check,
            )
        )
    selections = []
    for item in raw_selections:
        if not isinstance(item, dict) or set(item) != {
            "column",
            "selected",
            "excluded",
            "module",
        }:
            raise EngineError(
                Diagnostic(
                    "CONFIG.ROUTING_SELECTION",
                    "invalid",
                    "routing selection requires column, selected, excluded, and module",
                    suite=suite,
                    check=check,
                )
            )
        if any(not isinstance(item[field], str) or not item[field] for field in item):
            raise EngineError(
                Diagnostic(
                    "CONFIG.ROUTING_SELECTION",
                    "invalid",
                    "routing selection values must be non-empty strings",
                    suite=suite,
                    check=check,
                )
            )
        selections.append(
            RouteSelection(
                item["column"],
                item["selected"],
                item["excluded"],
                item["module"],
            )
        )
    # Every column has exactly one role, so no column can go unread.
    roles = (
        CASE_COLUMN,
        *facts,
        *(item.column for item in selections),
        strings["route_column"],
    )
    if len(set(roles)) != len(roles):
        raise EngineError(
            Diagnostic(
                "CONFIG.ROUTING_SELECTIONS",
                "invalid",
                "case, fact, selection, and route columns must be distinct",
                suite=suite,
                check=check,
            )
        )
    if set(roles) != set(header):
        stray = sorted(set(header) ^ set(roles))[0]
        raise EngineError(
            Diagnostic(
                "CONFIG.ROUTING_HEADER",
                "invalid",
                "routing header must be exactly case, the fact columns, the "
                "selection columns, and the route column",
                suite=suite,
                check=check,
                field=stray,
            )
        )
    return MetadataRouteCheck(
        check,
        strings["path"],
        header,
        facts,
        strings["expectations_path"],
        strings["route_column"],
        strings["resolved"],
        strings["unresolved"],
        tuple(selections),
    )
