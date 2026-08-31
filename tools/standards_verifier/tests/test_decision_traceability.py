from __future__ import annotations

# ruff: noqa: E402 - the standalone verifier package root precedes local imports.

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from tools.decision_traceability.decision_traceability import (
    TraceabilityError,
    normalize_path,
)
from tools.decision_traceability.verify_contract import run_contract


class DecisionTraceabilityTest(unittest.TestCase):
    def test_normalize_path_accepts_exact_and_prefix_paths(self) -> None:
        self.assertEqual(normalize_path("./src/api/public.ts"), "src/api/public.ts")
        self.assertEqual(normalize_path("src/engine/"), "src/engine/")

    def test_normalize_path_rejects_escaping_or_ambiguous_paths(self) -> None:
        for path in ("", "/src/api", "../src/api", "src/../api", "src//api", "C:/src"):
            with self.subTest(path=path), self.assertRaises(TraceabilityError):
                normalize_path(path)

    def test_reviewed_isolated_git_contract(self) -> None:
        run_contract()


if __name__ == "__main__":
    unittest.main()
