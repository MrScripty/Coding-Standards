from __future__ import annotations

import contextlib
import io
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.diagnostics import EngineError
from standards_verifier.policy_impact import load_policy_impact
from standards_verifier.policy_impact_cli import main


class PolicyImpactTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write(
            "workflows/planning.md",
            """
            # Planning Workflow

            **Standards metadata**

            - ID: `workflow.planning`
            - Role: `workflow`
            - Level: `MUST`
            - Applies when: Planned work requires stable sequencing.
            - Does not apply when: Work is bounded and local.
            - Requires: `none`
            - Specializes: `none`
            - Verification: Policy impact fixtures.
            - Canonical owner: `workflows/planning.md`
            """,
        )
        self.write("prompts/a.md", "# A\n")
        self.write("prompts/b.md", "# B\n")
        self.write("suites/evidence.toml", "schema_version = 1\n")
        self.write(
            "registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "evidence"
            path = "suites/evidence.toml"
            requires = []
            """,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def manifest(self, edges: str, *, owner_id: str = "workflow.planning") -> str:
        return textwrap.dedent(
            f"""
            schema_version = 1

            [[owners]]
            id = {owner_id!r}
            path = "workflows/planning.md"
            coverage = "audited"

            {edges}
            """
        ).replace("'", '"').lstrip()

    def edge(self, consumer: str, *, relation: str = "prompt-projection") -> str:
        return textwrap.dedent(
            f"""
            [[edges]]
            owner = "workflow.planning"
            consumer = "{consumer}"
            relation = "{relation}"
            applicability = "Consumer applies when Planning changes."
            evidence_owner = "suite:evidence"
            """
        )

    def load(self, content: str):
        self.write("impact.toml", content)
        return load_policy_impact(
            self.root,
            "impact.toml",
            {"evidence": "suites/evidence.toml"},
        )

    def test_loads_audited_edges_and_queries_in_deterministic_order(self) -> None:
        impact = self.load(
            self.manifest(self.edge("prompts/b.md") + self.edge("prompts/a.md"))
        )

        self.assertEqual(
            [edge.consumer for edge in impact.consumers_for("workflow.planning")],
            ["prompts/a.md", "prompts/b.md"],
        )

    def test_rejects_owner_that_does_not_match_canonical_metadata(self) -> None:
        with self.assertRaises(EngineError) as raised:
            self.load(self.manifest(self.edge("prompts/a.md"), owner_id="workflow.unknown"))

        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.UNKNOWN_OWNER")

    def test_rejects_unknown_evidence_owner(self) -> None:
        content = self.manifest(self.edge("prompts/a.md")).replace(
            "suite:evidence", "suite:missing"
        )

        with self.assertRaises(EngineError) as raised:
            self.load(content)

        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.EVIDENCE_OWNER")

    def test_rejects_consumer_that_does_not_match_relation(self) -> None:
        with self.assertRaises(EngineError) as raised:
            self.load(self.manifest(self.edge("prompts/a.md", relation="template-projection")))

        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.UNKNOWN_CONSUMER")

    def test_uncovered_owner_query_is_unavailable(self) -> None:
        impact = self.load(self.manifest(self.edge("prompts/a.md")))

        with self.assertRaises(EngineError) as raised:
            impact.consumers_for("workflow.unknown")

        self.assertEqual(raised.exception.exit_code, 3)
        self.assertEqual(
            raised.exception.diagnostic.code,
            "POLICY_IMPACT.OWNER_NOT_AUDITED",
        )

    def test_query_cli_renders_tsv(self) -> None:
        self.write("impact.toml", self.manifest(self.edge("prompts/a.md")))
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            exit_code = main(
                [
                    "--repo-root",
                    str(self.root),
                    "--registry",
                    "registry.toml",
                    "--manifest",
                    "impact.toml",
                    "--owner",
                    "workflow.planning",
                ],
                default_repo_root=self.root,
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "owner\tconsumer\trelation\tapplicability\tevidence_owner",
                "workflow.planning\tprompts/a.md\tprompt-projection\tConsumer applies when Planning changes.\tsuite:evidence",
            ],
        )
