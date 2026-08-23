from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tools.standards_metadata.standards_metadata import (
    MetadataError,
    load_canonical_module_corpus,
)

from ..diagnostics import Diagnostic, EngineError
from ..graph_adapters import METADATA_REQUIRES, metadata_dependency_registry
from ..model import CheckContext
from .table import read_table_rows


EXPECTATIONS_HEADER = ("case", "direct_modules", "requires_closure")


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
    expectations_path: str
    route_column: str
    resolved: str
    unresolved: str
    base_modules: tuple[str, ...]
    selections: tuple[RouteSelection, ...]

    def run(self, context: CheckContext) -> list[Diagnostic]:
        rows = read_table_rows(
            context.repo_root,
            self.path,
            self.header,
            suite=context.suite_id,
            check=self.id,
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
        cases = [row["case"] for row in rows]
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
        except MetadataError as error:
            failure = error.failure
            raise EngineError(
                Diagnostic(
                    failure.code,
                    failure.outcome,
                    failure.message,
                    suite=context.suite_id,
                    check=self.id,
                    path=failure.path,
                    row=failure.row,
                    field=failure.field,
                    expected=failure.expected,
                    observed=failure.observed,
                )
            ) from error
        known_modules = {module.module_id for module in corpus.modules}
        graph = metadata_dependency_registry(context.repo_root, corpus.modules)
        for row_number, row in enumerate(rows, start=2):
            case = row["case"]
            expected_direct, expected_closure = indexed[case]
            route = row[self.route_column]
            if route == self.unresolved:
                selected_values = {row[item.column] for item in self.selections}
                if selected_values != {self.unresolved}:
                    diagnostics.append(
                        self._diagnostic(
                            context,
                            "ASSERT.ROUTING_UNRESOLVED_SELECTION",
                            "an unresolved route cannot contain resolved topic selections",
                            row=row_number,
                            field=case,
                            observed=",".join(sorted(selected_values)),
                        )
                    )
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
            if route != self.resolved:
                diagnostics.append(
                    self._diagnostic(
                        context,
                        "ASSERT.ROUTING_STATE",
                        "route state is neither resolved nor unresolved",
                        row=row_number,
                        field=self.route_column,
                        observed=route,
                    )
                )
                continue

            direct = set(self.base_modules)
            invalid_selection = False
            for selection in self.selections:
                value = row[selection.column]
                if value == selection.selected:
                    direct.add(selection.module)
                elif value != selection.excluded:
                    diagnostics.append(
                        self._diagnostic(
                            context,
                            "ASSERT.ROUTING_INCOMPLETE",
                            "a resolved route contains an unresolved or unknown selection",
                            row=row_number,
                            field=selection.column,
                            observed=value,
                        )
                    )
                    invalid_selection = True
            if invalid_selection:
                continue
            unknown = direct - known_modules
            if unknown:
                diagnostics.append(
                    self._diagnostic(
                        context,
                        "ASSERT.ROUTING_UNKNOWN_MODULE",
                        "selected route module is not canonical",
                        row=row_number,
                        field=case,
                        observed=sorted(unknown)[0],
                    )
                )
                continue

            observed_direct = tuple(sorted(direct))
            observed_closure = graph.dependency_order(
                METADATA_REQUIRES,
                selected=observed_direct,
            )
            if observed_direct != expected_direct:
                diagnostics.append(
                    self._diagnostic(
                        context,
                        "ASSERT.ROUTING_DIRECT_MODULES",
                        "direct route modules do not match reviewed expectations",
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
        if not value or any(not item for item in values) or len(set(values)) != len(values):
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
        "expectations_path",
        "route_column",
        "resolved",
        "unresolved",
        "base_modules",
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
    for field in ("path", "expectations_path", "route_column", "resolved", "unresolved"):
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
    if "case" not in header or strings["route_column"] not in header:
        raise EngineError(
            Diagnostic(
                "CONFIG.ROUTING_HEADER",
                "invalid",
                "routing header must contain case and route columns",
                suite=suite,
                check=check,
            )
        )
    base_modules = _strings(raw.get("base_modules"), "base_modules", suite, check)
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
        if not isinstance(item, dict) or set(item) != {"column", "selected", "excluded", "module"}:
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
        if item["column"] not in header:
            raise EngineError(
                Diagnostic(
                    "CONFIG.ROUTING_HEADER",
                    "invalid",
                    "routing selection column is absent from the header",
                    suite=suite,
                    check=check,
                    field=item["column"],
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
    if len({item.column for item in selections}) != len(selections):
        raise EngineError(
            Diagnostic(
                "CONFIG.ROUTING_SELECTIONS",
                "invalid",
                "routing selection columns must be unique",
                suite=suite,
                check=check,
            )
        )
    return MetadataRouteCheck(
        check,
        strings["path"],
        header,
        strings["expectations_path"],
        strings["route_column"],
        strings["resolved"],
        strings["unresolved"],
        base_modules,
        tuple(selections),
    )
