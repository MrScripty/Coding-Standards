from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .diagnostics import Diagnostic
from .inventory import collect_inventory


@dataclass(frozen=True, slots=True)
class RetainedCheckerResult:
    checker_count: int
    diagnostic: Diagnostic | None = None

    @property
    def exit_code(self) -> int:
        if self.diagnostic is None:
            return 0
        return 3 if self.diagnostic.outcome == "unavailable" else 2


def run_retained_checkers(repo_root: Path) -> RetainedCheckerResult:
    root = repo_root.resolve()
    records = sorted(collect_inventory(root), key=lambda record: record.checker)
    completed = 0

    for record in records:
        checker = root / record.checker
        print(f"RUN {checker.name}", flush=True)
        try:
            result = subprocess.run([str(checker)], cwd=root, check=False)
        except OSError as error:
            return RetainedCheckerResult(
                checker_count=completed,
                diagnostic=Diagnostic(
                    "CHECKPOINT.CHECKER_UNAVAILABLE",
                    "unavailable",
                    f"retained checker could not be executed: {error}",
                    path=record.checker,
                ),
            )
        if result.returncode != 0:
            return RetainedCheckerResult(
                checker_count=completed,
                diagnostic=Diagnostic(
                    "CHECKPOINT.CHECKER_FAILED",
                    "invalid",
                    "retained checker returned a nonzero status",
                    path=record.checker,
                    expected="0",
                    observed=str(result.returncode),
                ),
            )
        completed += 1

    return RetainedCheckerResult(checker_count=completed)
