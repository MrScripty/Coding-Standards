from __future__ import annotations

import csv
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.engine import Verifier


class MetadataRouteTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write_module("core.md", "core", role="core")
        self.write_module("implementation.md", "workflow.implementation", requires=("core",))
        self.write_module("verification.md", "workflow.verification", requires=("core",))
        self.write_module(
            "contracts.md",
            "topic.contracts",
            requires=("core", "workflow.verification"),
        )
        self.write_module(
            "architecture.md",
            "topic.architecture",
            requires=("core", "topic.contracts"),
        )
        self.write(
            "evaluation/standards-effectiveness/canonical-module-corpus.toml",
            "schema_version = 1\n"
            'members = ["core.md", "implementation.md", "verification.md", '
            '"contracts.md", "architecture.md"]\n',
        )
        self.write(
            "decisions.tsv",
            "case\tarchitecture\troute\n"
            "local\texclude\troute\n"
            "shared\tselect\troute\n"
            "unknown\tunresolved\tunresolved\n",
        )
        self.write(
            "routes.tsv",
            "case\tdirect_modules\trequires_closure\n"
            "local\tworkflow.implementation,workflow.verification\t"
            "core,workflow.implementation,workflow.verification\n"
            "shared\ttopic.architecture,workflow.implementation,"
            "workflow.verification\tcore,workflow.implementation,"
            "workflow.verification,topic.contracts,topic.architecture\n"
            "unknown\tunresolved\tunresolved\n",
        )
        self.write(
            "suite.toml",
            """
            schema_version = 1
            id = "routing"
            owner = "test.routing"
            description = "Metadata route fixture"

            [[checks]]
            id = "routes"
            type = "metadata_route"
            path = "decisions.tsv"
            header = ["case", "architecture", "route"]
            expectations_path = "routes.tsv"
            route_column = "route"
            resolved = "route"
            unresolved = "unresolved"
            base_modules = ["workflow.implementation", "workflow.verification"]
            [[checks.selections]]
            column = "architecture"
            selected = "select"
            excluded = "exclude"
            module = "topic.architecture"
            """,
        )
        self.write(
            "registry.toml",
            "schema_version = 1\n\n"
            "[[suites]]\n"
            'id = "routing"\n'
            'path = "suite.toml"\n'
            "requires = []\n",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    @staticmethod
    def relation(values: tuple[str, ...]) -> str:
        return "`none`" if not values else ", ".join(f"`{value}`" for value in values)

    def write_module(
        self,
        path: str,
        module_id: str,
        *,
        role: str = "workflow",
        requires: tuple[str, ...] = (),
    ) -> None:
        level = "MUST"
        self.write(
            path,
            f"""
            # Module

            **Standards metadata**

            - ID: `{module_id}`
            - Role: `{role}`
            - Level: `{level}`
            - Applies when: The fixture applies.
            - Does not apply when: The fixture does not apply.
            - Requires: {self.relation(requires)}
            - Specializes: `none`
            - Verification: Focused route evidence.
            - Canonical owner: `{path}`
            """,
        )

    def result(self):
        return Verifier(self.root, "registry.toml").run(("routing",))[0]

    def mutate_route(self, case: str, field: str, value: str) -> None:
        with (self.root / "routes.tsv").open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle, delimiter="\t"))
        column = rows[0].index(field)
        for row in rows[1:]:
            if row[0] == case:
                row[column] = value
        with (self.root / "routes.tsv").open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle, delimiter="\t", lineterminator="\n").writerows(rows)

    def test_exact_direct_modules_and_graph_closure_pass(self) -> None:
        self.assertEqual(self.result().status, "passed")

    def test_direct_module_mutation_fails(self) -> None:
        self.mutate_route(
            "shared",
            "direct_modules",
            "workflow.implementation,workflow.verification",
        )
        self.assertIn(
            "ASSERT.ROUTING_DIRECT_MODULES",
            [item.code for item in self.result().diagnostics],
        )

    def test_requires_closure_mutation_fails(self) -> None:
        self.mutate_route(
            "shared",
            "requires_closure",
            "core,workflow.implementation,workflow.verification",
        )
        self.assertIn(
            "ASSERT.ROUTING_REQUIRES_CLOSURE",
            [item.code for item in self.result().diagnostics],
        )

    def test_unresolved_route_cannot_claim_resolved_selection(self) -> None:
        path = self.root / "decisions.tsv"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "unknown\tunresolved", "unknown\tselect"
            ),
            encoding="utf-8",
        )
        self.assertIn(
            "ASSERT.ROUTING_UNRESOLVED_SELECTION",
            [item.code for item in self.result().diagnostics],
        )

    def test_expectation_case_coverage_is_exact(self) -> None:
        path = self.root / "routes.tsv"
        lines = path.read_text(encoding="utf-8").splitlines()
        path.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
        self.assertIn(
            "ASSERT.ROUTING_CASE_COVERAGE",
            [item.code for item in self.result().diagnostics],
        )


if __name__ == "__main__":
    unittest.main()
