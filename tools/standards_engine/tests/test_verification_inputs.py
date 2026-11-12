from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine.tools import (
    LocalAlwaysAllowAuthorizer,
    _contracts,
)
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree


class VerificationInputFreshnessTest(unittest.TestCase):
    """The Engine checkpoint and its refresh agree about a stale manifest."""

    def test_read_only_checkpoint_rejects_a_stale_manifest_and_refresh_repairs_it(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "repository"
            _clone_tracked_worktree(repository)
            # No check reads this file; only the pinned list of tracked files changes.
            added = repository / "docs" / "added-without-a-refresh.md"
            added.write_text("A file tracked after the manifest was generated.\n")
            subprocess.run(
                ("git", "-C", str(repository), "add", "--", str(added)), check=True
            )
            with StandardsEngine.open_repository(
                repository,
                store_path=Path(temporary) / "engine.sqlite3",
                execution_context=AnalysisExecutionContext(
                    LocalAlwaysAllowAuthorizer(repository)
                ),
                purpose="authoring",
            ) as engine:
                facade = AgentToolFacade(engine, _contracts(repository))

                def verify(refresh: bool) -> dict[str, object]:
                    result = facade.verify_repository(
                        {
                            "kind": "verify-repository",
                            "refresh_verification_inputs": refresh,
                        }
                    )
                    self.assertEqual(result["kind"], "verify-repository-result", result)
                    return result["verification"]

                stale = verify(False)
                self.assertFalse(stale["passed"])
                self.assertEqual(
                    [item["code"] for item in stale["failures"]],
                    ["SUITE_INPUT.STALE_MANIFEST"],
                )
                self.assertGreater(stale["suites"], 0)

                # The refresh verifies what it wrote, manifest included.
                self.assertTrue(verify(True)["passed"])


if __name__ == "__main__":
    unittest.main()
