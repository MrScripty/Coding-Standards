from __future__ import annotations

import contextlib
import io
import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch


ENGINE_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.cli import main
from standards_verifier.complete_checkpoint import run_retained_checkers
from standards_verifier.inventory import CheckerRecord


def record(path: str) -> CheckerRecord:
    return CheckerRecord(
        checker=path,
        lines=1,
        inbound_count=0,
        inbound_files=(),
        executable_inbound_files=(),
        contract_inbound_files=(),
        documentation_inbound_files=(),
        verifier_dependencies=(),
        helper_dependencies=(),
        uses_sed=False,
        uses_awk=False,
        uses_rg=False,
        uses_decision_table=False,
    )


class CompleteCheckpointTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_registry(self) -> None:
        self.write(
            "registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "suite"
            path = "suite.toml"
            requires = []
            """,
        )
        self.write(
            "suite.toml",
            """
            schema_version = 1
            id = "suite"
            owner = "test.owner"
            description = "Complete checkpoint fixture"

            [[checks]]
            id = "text"
            type = "text"
            path = "evidence.md"
            required = ["required"]
            prohibited = []
            """,
        )
        self.write("evidence.md", "required\n")

    @patch("standards_verifier.complete_checkpoint.subprocess.run")
    @patch("standards_verifier.complete_checkpoint.print")
    @patch("standards_verifier.complete_checkpoint.collect_inventory")
    def test_retained_checkers_run_in_deterministic_order(self, collect, output, run) -> None:
        collect.return_value = (
            record("evaluation/standards-effectiveness/verify-b.sh"),
            record("evaluation/standards-effectiveness/verify-a.sh"),
        )
        run.return_value = subprocess.CompletedProcess([], 0)

        result = run_retained_checkers(self.root)

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.checker_count, 2)
        self.assertEqual(
            [call.args[0][0] for call in run.call_args_list],
            [
                str(self.root / "evaluation/standards-effectiveness/verify-a.sh"),
                str(self.root / "evaluation/standards-effectiveness/verify-b.sh"),
            ],
        )
        self.assertTrue(all(call.kwargs == {"flush": True} for call in output.call_args_list))

    @patch("standards_verifier.complete_checkpoint.subprocess.run")
    @patch("standards_verifier.complete_checkpoint.collect_inventory")
    def test_retained_checker_failure_is_typed_and_fail_fast(self, collect, run) -> None:
        collect.return_value = tuple(record(f"verify-{name}.sh") for name in ("a", "b", "c"))
        run.side_effect = (
            subprocess.CompletedProcess([], 0),
            subprocess.CompletedProcess([], 7),
        )

        result = run_retained_checkers(self.root)

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.checker_count, 1)
        self.assertEqual(result.diagnostic.code, "CHECKPOINT.CHECKER_FAILED")
        self.assertEqual(result.diagnostic.observed, "7")
        self.assertEqual(run.call_count, 2)

    @patch("standards_verifier.complete_checkpoint.subprocess.run")
    @patch("standards_verifier.complete_checkpoint.collect_inventory")
    def test_unavailable_retained_checker_is_typed(self, collect, run) -> None:
        collect.return_value = (record("verify-missing.sh"),)
        run.side_effect = FileNotFoundError("missing")

        result = run_retained_checkers(self.root)

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostic.code, "CHECKPOINT.CHECKER_UNAVAILABLE")

    @patch("standards_verifier.complete_checkpoint.subprocess.run")
    @patch("standards_verifier.complete_checkpoint.collect_inventory", return_value=())
    def test_empty_retained_inventory_passes(self, collect, run) -> None:
        result = run_retained_checkers(self.root)

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.checker_count, 0)
        run.assert_not_called()

    def test_complete_rejects_selection_and_format_conflicts(self) -> None:
        for arguments, code in (
            (["--complete", "--suite", "suite"], "SELECTION.CONFLICT"),
            (["--complete", "--format", "json"], "SELECTION.FORMAT_CONFLICT"),
        ):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = main(arguments, default_repo_root=self.root)
            self.assertEqual(status, 2)
            self.assertIn(code, output.getvalue())

    @patch("standards_verifier.cli.run_retained_checkers")
    @patch("standards_verifier.cli.check_generated_artifacts", return_value=0)
    def test_complete_checks_generated_evidence_and_runs_all_suites(self, generated, retained) -> None:
        self.write_registry()
        retained.return_value = type("Result", (), {"diagnostic": None, "checker_count": 0})()
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            status = main(
                ["--repo-root", str(self.root), "--registry", "registry.toml", "--complete"],
                default_repo_root=self.root,
            )

        self.assertEqual(status, 0)
        generated.assert_called_once_with(self.root)
        retained.assert_called_once_with(self.root)
        self.assertIn("PASS suite", output.getvalue())

    @patch("standards_verifier.cli.Verifier")
    @patch("standards_verifier.cli.run_retained_checkers")
    @patch("standards_verifier.cli.check_generated_artifacts", return_value=2)
    def test_stale_generated_evidence_prevents_all_execution(
        self,
        generated,
        retained,
        verifier,
    ) -> None:
        status = main(
            ["--repo-root", str(self.root), "--complete"],
            default_repo_root=self.root,
        )

        self.assertEqual(status, 2)
        generated.assert_called_once_with(self.root)
        verifier.assert_not_called()
        retained.assert_not_called()

    @patch("standards_verifier.cli.run_retained_checkers")
    @patch("standards_verifier.cli.check_generated_artifacts", return_value=0)
    def test_declarative_failure_prevents_retained_execution(self, generated, retained) -> None:
        self.write_registry()
        self.write("evidence.md", "forbidden\n")

        status = main(
            ["--repo-root", str(self.root), "--registry", "registry.toml", "--complete"],
            default_repo_root=self.root,
        )

        self.assertNotEqual(status, 0)
        generated.assert_called_once_with(self.root)
        retained.assert_not_called()


if __name__ == "__main__":
    unittest.main()
