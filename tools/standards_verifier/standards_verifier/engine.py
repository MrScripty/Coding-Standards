from __future__ import annotations

from pathlib import Path

from .config import load_catalog
from .diagnostics import Diagnostic, EngineError
from .graph_adapters import SUITE_DEPENDENCIES, suite_dependency_registry
from .model import CheckContext, Suite, SuiteResult


class Verifier:
    def __init__(
        self,
        repo_root: Path,
        registry_path: str = "evaluation/standards-effectiveness/suite-registry.toml",
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.catalog = load_catalog(self.repo_root, registry_path)
        self.dependency_graph = suite_dependency_registry(
            self.repo_root,
            self.catalog.entries,
            registry_path,
            include_path_aliases=True,
        )

    def list_suites(self) -> tuple[str, ...]:
        return tuple(entry.id for entry in self.catalog.entries)

    def run(self, selected: tuple[str, ...] | None = None) -> list[SuiteResult]:
        selected_ids = self._selection(selected)
        order = self._execution_order(selected_ids)
        results = []
        by_id: dict[str, SuiteResult] = {}
        for suite_id in order:
            entry = self.catalog.entry(suite_id)
            failed_dependencies = [
                dependency
                for dependency in entry.requires
                if by_id[dependency].status != "passed"
            ]
            if failed_dependencies:
                result = SuiteResult(
                    id=suite_id,
                    status="blocked",
                    check_count=0,
                    diagnostics=[
                        Diagnostic(
                            code="SUITE.DEPENDENCY_FAILED",
                            outcome="unavailable",
                            message="suite dependency did not pass",
                            suite=suite_id,
                            observed=dependency,
                        )
                        for dependency in failed_dependencies
                    ],
                    exit_code=3,
                )
            else:
                result = self._run_suite(self.catalog.suite(suite_id))
            results.append(result)
            by_id[suite_id] = result
        return results

    def _selection(self, selected: tuple[str, ...] | None) -> tuple[str, ...]:
        if selected is None:
            return self.list_suites()
        if not selected:
            raise EngineError(Diagnostic("SELECTION.EMPTY", "invalid", "at least one suite must be selected"))
        if len(set(selected)) != len(selected):
            raise EngineError(Diagnostic("SELECTION.DUPLICATE", "invalid", "selected suite IDs must be unique"))
        for suite_id in selected:
            if suite_id not in self.catalog.suite_ids:
                raise EngineError(Diagnostic("SELECTION.UNKNOWN_SUITE", "unavailable", "selected suite is not registered", suite=suite_id), exit_code=3)
        return selected

    def _execution_order(self, selected: tuple[str, ...]) -> tuple[str, ...]:
        return self.dependency_graph.dependency_order(
            SUITE_DEPENDENCIES,
            selected,
            preferred_order=(entry.id for entry in self.catalog.entries),
        )

    def _run_suite(self, suite: Suite) -> SuiteResult:
        diagnostics = []
        exit_code = 0
        context = CheckContext(
            self.repo_root,
            suite.id,
            self.catalog,
        )
        for check in suite.checks:
            try:
                diagnostics.extend(check.run(context))
            except EngineError as error:
                diagnostics.append(error.diagnostic)
                exit_code = max(exit_code, error.exit_code)
        if diagnostics and exit_code == 0:
            exit_code = 1
        return SuiteResult(
            id=suite.id,
            status="failed" if diagnostics else "passed",
            check_count=len(suite.checks),
            diagnostics=diagnostics,
            exit_code=exit_code,
        )
