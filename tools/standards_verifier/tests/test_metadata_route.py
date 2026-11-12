from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.diagnostics import EngineError
from standards_verifier.engine import Verifier
from standards_verifier.suite_inputs import compile_suite_input_projection


ROUTER_PROJECTION = "evaluation/standards-effectiveness/router-projection.toml"
DECISIONS_HEADER = ("case", "routing.activities", "routing.topics", "architecture", "route")
DECISIONS = (
    ("local", "implementation,verification", "none", "exclude", "route"),
    ("shared", "implementation,verification", "architecture", "select", "route"),
    ("unknown", "implementation,verification", "unknown", "unresolved", "unresolved"),
)
ROUTES = (
    (
        "local",
        "router,workflow.implementation,workflow.verification",
        "core,router,workflow.implementation,workflow.verification",
    ),
    (
        "shared",
        "router,topic.architecture,workflow.implementation,workflow.verification",
        "core,router,workflow.implementation,workflow.verification,"
        "topic.contracts,topic.architecture",
    ),
    ("unknown", "unresolved", "unresolved"),
)
FACT = """
[[facts]]
id = "{id}"
semantic_revision = 1
type = "{type}"
nullable = false
values = [{values}]
aliases = []
meaning = "Fixture fact."
context_kind = "task-route"
answer_contract = "fact-value.v1"
evidence_contract = "evidence-reference.v1"
authorization_capability = "standards.analyze"
prompt = "Fixture prompt?"
"""
SUITE = """
schema_version = 1
id = "routing"
owner = "test.routing"
description = "Metadata route fixture"

[[checks]]
id = "routes"
type = "metadata_route"
path = "decisions.tsv"
header = [{header}]
facts = [{facts}]
expectations_path = "routes.tsv"
route_column = "route"
resolved = "route"
unresolved = "unresolved"
{extra}
[[checks.selections]]
column = "architecture"
selected = "select"
excluded = "exclude"
module = "{module}"
"""


def quoted(values: tuple[str, ...]) -> str:
    return ", ".join(f'"{value}"' for value in values)


class MetadataRouteTest(unittest.TestCase):
    """Scenarios are routed by the Router projection, not by the table itself."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write_module("core.md", "core", role="core")
        self.write_module(
            "STANDARDS-ROUTER.md",
            "router",
            requires=("core",),
            body="""
            | Condition | Select |
            | --- | --- |
            | Code changes | [Implementation](implementation.md) |
            | A claim is checked | [Verification](verification.md) |
            | Contracts change | [Contracts](contracts.md) |
            | Authority moves | [Architecture](architecture.md) |
            """,
        )
        self.write_module("implementation.md", "workflow.implementation", requires=("core",))
        self.write_module("verification.md", "workflow.verification", requires=("core",))
        self.write_module(
            "contracts.md", "topic.contracts", requires=("core", "workflow.verification")
        )
        self.write_module(
            "architecture.md", "topic.architecture", requires=("core", "topic.contracts")
        )
        self.write(
            "evaluation/standards-effectiveness/canonical-module-corpus.toml",
            "schema_version = 1\n"
            'members = ["core.md", "STANDARDS-ROUTER.md", "implementation.md", '
            '"verification.md", "contracts.md", "architecture.md"]\n',
        )
        self.write_router()
        self.write_table("decisions.tsv", DECISIONS_HEADER, DECISIONS)
        self.write_table("routes.tsv", ("case", "direct_modules", "requires_closure"), ROUTES)
        self.write_suite()
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

    def write_table(
        self, path: str, header: tuple[str, ...], rows: tuple[tuple[str, ...], ...]
    ) -> None:
        self.write(path, "".join("\t".join(row) + "\n" for row in (header, *rows)))

    def write_suite(
        self,
        *,
        header: tuple[str, ...] = DECISIONS_HEADER,
        facts: tuple[str, ...] = ("routing.activities", "routing.topics"),
        module: str = "topic.architecture",
        extra: str = "",
    ) -> None:
        self.write(
            "suite.toml",
            SUITE.format(
                header=quoted(header), facts=quoted(facts), module=module, extra=extra
            ),
        )

    def write_router(
        self,
        *,
        architecture: str = "architecture",
        topics: tuple[str, ...] = ("architecture", "contracts"),
    ) -> None:
        """A four-rule Router; contracts is also reachable through a detail fact."""
        facts = "".join(
            FACT.format(id=fact, type=kind, values=quoted(values))
            for fact, kind, values in (
                ("routing.activities", "enum-set", ("implementation", "verification")),
                ("routing.topics", "enum-set", topics),
                ("routing.details", "enum-set", ("topic.contracts",)),
                ("routing.reviewed", "boolean", ()),
            )
        )
        self.write(
            ROUTER_PROJECTION,
            'schema_version = 2\nid = "router.fixture"\nowner = "router"\n'
            'source = "STANDARDS-ROUTER.md"\nbase_modules = ["router"]\n'
            + facts
            + f"""
[[rules]]
id = "route.workflow.implementation"
target = "workflow.implementation"
when = {{ fact = "routing.activities", operator = "contains", value = "implementation" }}

[[rules]]
id = "route.workflow.verification"
target = "workflow.verification"
when = {{ fact = "routing.activities", operator = "contains", value = "verification" }}

[[rules]]
id = "route.topic.architecture"
target = "topic.architecture"
when = {{ fact = "routing.topics", operator = "contains", value = "{architecture}" }}

[[rules]]
id = "route.topic.contracts"
target = "topic.contracts"
when = {{ operator = "any", expressions = [{{ fact = "routing.topics", operator = "contains", value = "contracts" }}, {{ fact = "routing.details", operator = "contains", value = "topic.contracts" }}] }}
""",
        )

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
        body: str = "",
    ) -> None:
        metadata = f"""
            # Module

            **Standards metadata**

            - ID: `{module_id}`
            - Role: `{role}`
            - Level: `MUST`
            - Applies when: The fixture applies.
            - Does not apply when: The fixture does not apply.
            - Requires: {self.relation(requires)}
            - Specializes: `none`
            - Verification: Focused route evidence.
            - Canonical owner: `{path}`
            """
        self.write(path, textwrap.dedent(metadata).lstrip() + textwrap.dedent(body))

    def result(self):
        return Verifier(self.root, "registry.toml").run(("routing",))[0]

    def codes(self) -> list[str]:
        return [item.code for item in self.result().diagnostics]

    def replace(self, path: str, old: str, new: str) -> None:
        target = self.root / path
        content = target.read_text(encoding="utf-8")
        self.assertEqual(content.count(old), 1, old)
        target.write_text(content.replace(old, new), encoding="utf-8")

    def test_scenarios_the_router_agrees_with_pass(self) -> None:
        result = self.result()

        self.assertEqual((result.status, result.diagnostics), ("passed", []))

    def test_a_changed_router_rule_fails_the_scenarios_it_decides(self) -> None:
        self.write_router(architecture="contracts")

        diagnostics = self.result().diagnostics

        self.assertEqual(
            [(item.code, item.field, item.expected, item.observed) for item in diagnostics],
            [
                ("ASSERT.ROUTING_SELECTION", "shared.architecture", "select", "exclude"),
                (
                    "ASSERT.ROUTING_DIRECT_MODULES",
                    "shared",
                    "router,topic.architecture,workflow.implementation,workflow.verification",
                    "router,workflow.implementation,workflow.verification",
                ),
                (
                    "ASSERT.ROUTING_REQUIRES_CLOSURE",
                    "shared",
                    "core,router,workflow.implementation,workflow.verification,"
                    "topic.contracts,topic.architecture",
                    "core,router,workflow.implementation,workflow.verification",
                ),
            ],
        )

    def test_scenario_facts_decide_the_route(self) -> None:
        self.replace("decisions.tsv", "\tarchitecture\tselect", "\tnone\tselect")

        self.assertEqual(
            self.codes(),
            [
                "ASSERT.ROUTING_SELECTION",
                "ASSERT.ROUTING_DIRECT_MODULES",
                "ASSERT.ROUTING_REQUIRES_CLOSURE",
            ],
        )

    def test_a_table_without_scenarios_fails(self) -> None:
        self.write_table("decisions.tsv", DECISIONS_HEADER, ())
        self.write_table("routes.tsv", ("case", "direct_modules", "requires_closure"), ())

        result = self.result()

        self.assertEqual(result.status, "failed")
        self.assertEqual(self.codes(), ["ROUTING.NO_SCENARIOS"])

    def test_a_column_the_router_does_not_declare_fails(self) -> None:
        header = ("case", "routing.activities", "module_boundary", "architecture", "route")
        self.write_table("decisions.tsv", header, DECISIONS)
        self.write_suite(header=header, facts=("routing.activities", "module_boundary"))

        diagnostics = self.result().diagnostics

        self.assertEqual(
            [(item.code, item.observed) for item in diagnostics],
            [("ROUTING.UNKNOWN_FACT", "module_boundary")],
        )

    def test_a_value_the_router_does_not_declare_fails(self) -> None:
        self.replace("decisions.tsv", "\tarchitecture\tselect", "\tboundary\tselect")

        diagnostics = self.result().diagnostics

        self.assertEqual(
            [(item.code, item.row, item.field, item.observed) for item in diagnostics],
            [("ROUTING.FACT_VALUE", 3, "routing.topics", "boundary")],
        )

    def test_an_unknown_fact_is_unresolved_rather_than_excluded(self) -> None:
        self.replace("decisions.tsv", "unknown\tunresolved\tunresolved", "unknown\texclude\troute")

        diagnostics = self.result().diagnostics

        self.assertEqual(
            [(item.code, item.expected, item.observed) for item in diagnostics],
            [
                ("ASSERT.ROUTING_SELECTION", "exclude", "unresolved"),
                ("ASSERT.ROUTING_RESOLUTION", "route", "unresolved,routing.topics"),
            ],
        )

    def test_an_unresolved_route_has_no_reviewed_module_list(self) -> None:
        self.replace("routes.tsv", "unknown\tunresolved\tunresolved", "unknown\trouter\tcore,router")

        self.assertEqual(self.codes(), ["ASSERT.ROUTING_UNRESOLVED_EXPECTATION"])

    def test_a_fact_without_a_column_does_not_apply_to_the_scenario(self) -> None:
        # Neither routing.details nor the scalar routing.reviewed has a column:
        # the contracts rule that reads routing.details is decided, not unresolved.
        self.assertEqual(self.result().status, "passed")

        header = (*DECISIONS_HEADER[:3], "routing.details", *DECISIONS_HEADER[3:])
        rows = tuple((*row[:3], "unknown", *row[3:]) for row in DECISIONS)
        self.write_table("decisions.tsv", header, rows)
        self.write_suite(
            header=header,
            facts=("routing.activities", "routing.topics", "routing.details"),
        )

        self.assertEqual(
            [(item.code, item.field) for item in self.result().diagnostics],
            [("ASSERT.ROUTING_RESOLUTION", "local"), ("ASSERT.ROUTING_RESOLUTION", "shared")],
        )

    def test_reviewed_direct_modules_must_match_the_router(self) -> None:
        self.replace(
            "routes.tsv",
            "shared\trouter,topic.architecture,",
            "shared\trouter,",
        )

        self.assertEqual(self.codes(), ["ASSERT.ROUTING_DIRECT_MODULES"])

    def test_reviewed_requires_closure_must_match_the_graph(self) -> None:
        self.replace("routes.tsv", ",topic.contracts,topic.architecture", ",topic.architecture")

        self.assertEqual(self.codes(), ["ASSERT.ROUTING_REQUIRES_CLOSURE"])

    def test_expectation_case_coverage_is_exact(self) -> None:
        self.write_table(
            "routes.tsv", ("case", "direct_modules", "requires_closure"), ROUTES[:-1]
        )

        self.assertEqual(self.codes(), ["ASSERT.ROUTING_CASE_COVERAGE"])

    def test_expected_selection_must_name_a_module_the_router_can_select(self) -> None:
        self.write_suite(module="core")

        diagnostics = self.result().diagnostics

        self.assertEqual(
            [(item.code, item.observed) for item in diagnostics],
            [("ROUTING.UNROUTED_MODULE", "core")],
        )

    def test_scenario_columns_support_set_valued_facts_without_keyword_collisions(self) -> None:
        header = (*DECISIONS_HEADER[:3], "routing.details", *DECISIONS_HEADER[3:])
        rows = tuple((*row[:3], "none", *row[3:]) for row in DECISIONS)
        self.write_table("decisions.tsv", header, rows)
        self.write_suite(
            header=header,
            facts=("routing.activities", "routing.topics", "routing.details"),
        )
        self.assertEqual(self.result().status, "passed")

        self.write_router(topics=("architecture", "contracts", "none"))
        self.assertEqual(self.codes(), ["ROUTING.FACT_TOKEN_COLLISION"])

        self.write_router()
        scalar = (*DECISIONS_HEADER[:3], "routing.reviewed", *DECISIONS_HEADER[3:])
        self.write_table("decisions.tsv", scalar, rows)
        self.write_suite(
            header=scalar,
            facts=("routing.activities", "routing.topics", "routing.reviewed"),
        )
        result = self.result()
        self.assertEqual(self.codes(), ["ROUTING.FACT_TYPE"])
        self.assertEqual(result.exit_code, 4)

    def test_every_column_has_a_role_and_the_router_supplies_the_base(self) -> None:
        for change, code, field in (
            ({"header": (*DECISIONS_HEADER, "notes")}, "CONFIG.ROUTING_HEADER", "notes"),
            ({"facts": ("routing.activities",)}, "CONFIG.ROUTING_HEADER", "routing.topics"),
            ({"facts": ("routing.activities", "routing.topics", "architecture")},
             "CONFIG.ROUTING_SELECTIONS", None),
            ({"extra": 'base_modules = ["router"]'}, "CONFIG.UNKNOWN_FIELD", "base_modules"),
        ):
            with self.subTest(change=change):
                self.write_suite(**change)
                with self.assertRaises(EngineError) as caught:
                    Verifier(self.root, "registry.toml").run()
                diagnostic = caught.exception.diagnostic
                self.assertEqual((diagnostic.code, diagnostic.field), (code, field))

    def test_an_invalid_router_projection_fails_the_check(self) -> None:
        self.replace(ROUTER_PROJECTION, 'base_modules = ["router"]', 'base_modules = ["absent"]')

        diagnostics = self.result().diagnostics

        self.assertEqual(
            [(item.code, item.path) for item in diagnostics],
            [("ROUTER_PROJECTION.INVALID", ROUTER_PROJECTION)],
        )

    def test_router_projection_and_corpus_are_declared_inputs(self) -> None:
        projection = compile_suite_input_projection(self.root, "registry.toml")
        roles = {
            item["path"]: [use["role"] for use in item["uses"]]
            for item in projection["files"]
        }

        self.assertEqual(roles[ROUTER_PROJECTION], ["router-projection"])
        self.assertEqual(roles["STANDARDS-ROUTER.md"], ["canonical-module"])
        self.assertEqual(roles["decisions.tsv"], ["routing-cases"])
        self.assertEqual(roles["routes.tsv"], ["routing-expectations"])


if __name__ == "__main__":
    unittest.main()
