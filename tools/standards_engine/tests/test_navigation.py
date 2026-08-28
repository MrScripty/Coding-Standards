from __future__ import annotations

import csv
import json
import shutil
import tempfile
import tomllib
import unittest
from pathlib import Path

from tools.standards_contracts.standards_contracts import compile_contracts
from tools.standards_engine.standards_engine import (
    AgentToolFacade,
    InspectCall,
    PolicyInspectionResult,
    QueryCall,
    ReadRequest,
    ReadResult,
    RejectedResult,
    RelatedRequest,
    RelatedResult,
    RelationshipInspectionResult,
    RouteRequest,
    RouteResult,
    StandardsAuthorityViewHandle,
    StandardsEngine,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


def _contracts():
    schema = json.loads(
        (
            REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json"
        ).read_text(encoding="utf-8")
    )
    with (
        REPO_ROOT / "tools/standards_engine/contracts/a1-interface.toml"
    ).open("rb") as source:
        interface = tomllib.load(source)
    return compile_contracts(schema, interface)


class NavigationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = StandardsEngine.open_repository(REPO_ROOT, durable=False)
        cls.contracts = _contracts()

    def assert_contract(self, definition: str, result) -> dict[str, object]:
        value = result.as_contract()
        self.contracts.validate(definition, value)
        return value

    @staticmethod
    def route_facts(**overrides: object) -> dict[str, object]:
        values: dict[str, object] = {
            "routing.activities": [],
            "routing.workflow-profiles": [],
            "routing.applications": [],
            "routing.boundaries": [],
            "routing.languages": [],
            "routing.frameworks": [],
            "routing.topics": [],
        }
        values.update(overrides)
        return {
            key: (
                value
                if isinstance(value, dict)
                else {"type": "enum-set", "state": "known", "value": value}
            )
            for key, value in values.items()
        }

    def test_route_selects_direct_modules_and_required_closure(self) -> None:
        result = self.engine.query(
            QueryCall(
                self.engine.view,
                RouteRequest(
                    "route",
                    self.route_facts(
                        **{
                            "routing.activities": ["implementation", "verification"],
                            "routing.applications": ["library"],
                            "routing.languages": ["rust"],
                        }
                    ),
                ),
            )
        )

        self.assertIsInstance(result, RouteResult)
        value = self.assert_contract("RouteResult", result)
        self.assertEqual(value["unresolved_questions"], [])
        self.assertEqual(
            {item["target"] for item in value["reading_plan"]},
            {
                "core",
                "router",
                "workflow.implementation",
                "workflow.verification",
                "profile.application.library",
                "profile.language.rust",
            },
        )
        self.assertEqual(
            [item["target"] for item in value["reading_plan"][:2]],
            ["core", "router"],
        )

    def test_route_fixture_matches_public_projection(self) -> None:
        decisions_path = (
            REPO_ROOT
            / "evaluation/standards-effectiveness/fixtures/routing/"
            "verifier-change-decisions.tsv"
        )
        routes_path = (
            REPO_ROOT
            / "evaluation/standards-effectiveness/fixtures/routing/"
            "verifier-change-routes.tsv"
        )
        with decisions_path.open(encoding="utf-8", newline="") as source:
            decisions = {
                row["case"]: row for row in csv.DictReader(source, delimiter="\t")
            }
        with routes_path.open(encoding="utf-8", newline="") as source:
            routes = {
                row["case"]: row for row in csv.DictReader(source, delimiter="\t")
            }

        for case, row in decisions.items():
            facts = self.route_facts(
                **{
                    "routing.activities": [
                        "implementation",
                        "verification",
                        *(
                            ["planning"]
                            if row["expected_planning"] == "select"
                            else []
                        ),
                    ],
                    "routing.topics": [
                        *(
                            ["architecture"]
                            if row["expected_architecture"] == "select"
                            else []
                        ),
                        *(
                            ["performance"]
                            if row["expected_performance"] == "select"
                            else []
                        ),
                    ],
                }
            )
            if row["expected_route"] == "unresolved":
                facts["routing.topics"] = {"type": "enum-set", "state": "unknown"}
            result = self.engine.query(
                QueryCall(self.engine.view, RouteRequest("route", facts))
            )
            value = self.assert_contract("RouteResult", result)
            if row["expected_route"] == "unresolved":
                self.assertTrue(value["unresolved_questions"], case)
                continue
            direct = {
                item["target"]
                for item in value["reading_plan"]
                if any(reason["kind"] == "routing-rule" for reason in item["reasons"])
            }
            closure = {item["target"] for item in value["reading_plan"]} - {"router"}
            self.assertEqual(direct, set(routes[case]["direct_modules"].split(",")), case)
            self.assertEqual(
                closure, set(routes[case]["requires_closure"].split(",")), case
            )

    def test_unknown_and_invalid_route_facts_have_typed_results(self) -> None:
        facts = self.route_facts()
        facts["routing.topics"] = {"type": "enum-set", "state": "unknown"}
        result = self.engine.query(
            QueryCall(self.engine.view, RouteRequest("route", facts))
        )
        value = self.assert_contract("RouteResult", result)
        self.assertEqual(
            [item["id"] for item in value["unresolved_questions"]],
            ["question.routing.topics"],
        )

        invalid = self.engine.query(
            QueryCall(
                self.engine.view,
                RouteRequest(
                    "route",
                    {
                        "routing.undeclared": {
                            "type": "boolean",
                            "state": "known",
                            "value": True,
                        }
                    },
                ),
            )
        )
        self.assertIsInstance(invalid, RejectedResult)
        self.assertEqual(invalid.code, "APPLICABILITY.INVALID")

    def test_snapshot_contains_coverage_attestation_evidence(self) -> None:
        inspection = self.engine.inspect(InspectCall(self.engine.snapshot))
        value = self.assert_contract("ContentSnapshotInspectionResult", inspection)
        scope = {
            "/".join(item["path"]["components"])
            for item in value["content_snapshot"]["files"]
        }
        registry_path = (
            "evaluation/standards-effectiveness/policy-coverage/"
            "attestation-sources.toml"
        )
        with (REPO_ROOT / registry_path).open("rb") as source:
            registry = tomllib.load(source)
        expected = {
            "evaluation/standards-effectiveness/policy-coverage/horizons.toml",
            registry_path,
            *registry["sources"],
        }
        for attestation_path in registry["sources"]:
            with (REPO_ROOT / attestation_path).open("rb") as source:
                declaration = tomllib.load(source)
            for attestation in declaration["attestations"]:
                expected.update(attestation["evidence"])
                expected.update(attestation["explicit_exclusions"])
        self.assertTrue(expected.issubset(scope))

    def test_attestation_bytes_do_not_invalidate_semantic_authorities(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            shutil.copytree(
                REPO_ROOT,
                root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            first = StandardsEngine.open_repository(root, durable=False)
            first_view = first.inspect(InspectCall(first.view))

            registry_path = (
                root
                / "evaluation/standards-effectiveness/policy-coverage/"
                "attestation-sources.toml"
            )
            with registry_path.open("rb") as source:
                attestation_path = tomllib.load(source)["sources"][0]
            attestation = root / attestation_path
            attestation.write_text(
                attestation.read_text(encoding="utf-8")
                + "\n# Representation-only attestation note.\n",
                encoding="utf-8",
            )

            second = StandardsEngine.open_repository(root, durable=False)
            second_view = second.inspect(InspectCall(second.view))

            self.assertNotEqual(first.snapshot, second.snapshot)
            self.assertNotEqual(first.view, second.view)
            self.assertEqual(
                first_view.operation_contracts,
                second_view.operation_contracts,
            )
            self.assertEqual(first_view.authorities, second_view.authorities)

    def test_module_read_and_inspection_use_captured_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            shutil.copytree(
                REPO_ROOT,
                root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            engine = StandardsEngine.open_repository(root, durable=False)
            original = engine.query(
                QueryCall(engine.view, ReadRequest("read", "workflow.verification"))
            )
            self.assertIsInstance(original, ReadResult)
            original_content = original.content
            policy_handle = original.policy.handle
            original_inspection = engine.inspect(InspectCall(policy_handle))
            self.assertIsInstance(original_inspection, PolicyInspectionResult)

            source = root / "workflows/verification.md"
            source.write_text(
                source.read_text(encoding="utf-8") + "\nMUTATED AFTER CAPTURE\n",
                encoding="utf-8",
            )

            repeated = engine.query(
                QueryCall(engine.view, ReadRequest("read", "workflow.verification"))
            )
            inspection = engine.inspect(InspectCall(policy_handle))
            self.assertEqual(repeated.content, original_content)
            self.assertNotIn("MUTATED AFTER CAPTURE", repeated.content)
            self.assertIsInstance(inspection, PolicyInspectionResult)
            self.assertEqual(
                inspection.representation_digest,
                original_inspection.representation_digest,
            )

    def test_advertised_policy_and_relationship_handles_are_inspectable(self) -> None:
        read = self.engine.query(
            QueryCall(self.engine.view, ReadRequest("read", "workflow.verification"))
        )
        self.assertIsInstance(read, ReadResult)
        policy = self.engine.inspect(InspectCall(read.policy.handle))
        self.assertIsInstance(policy, PolicyInspectionResult)

        related = self.engine.query(
            QueryCall(
                self.engine.view,
                RelatedRequest(
                    "related",
                    "workflow.verification",
                    ("standards-requires",),
                    "outgoing",
                    False,
                ),
            )
        )
        self.assertIsInstance(related, RelatedResult)
        self.assertTrue(related.relationships)
        relationship = self.engine.inspect(
            InspectCall(related.relationships[0].handle)
        )
        self.assertIsInstance(relationship, RelationshipInspectionResult)

    def test_navigation_operations_bind_the_exact_authority_view(self) -> None:
        route = self.engine.query(
            QueryCall(
                self.engine.view,
                RouteRequest(
                    "route",
                    self.route_facts(**{"routing.activities": ["implementation"]}),
                ),
            )
        )
        self.assertIsInstance(route, RouteResult)
        self.assertTrue(route.next_operations)
        self.assertTrue(
            all(operation.view == self.engine.view for operation in route.next_operations)
        )

    def test_unknown_view_and_repository_path_do_not_fall_back(self) -> None:
        missing_view = StandardsAuthorityViewHandle.from_value(
            {
                "kind": "standards-authority-view-handle",
                "id": "standards-authority-view:sha256:" + "0" * 64,
                "schema_version": 4,
            }
        )
        unavailable = self.engine.query(
            QueryCall(missing_view, ReadRequest("read", "workflow.verification"))
        )
        self.assertIsInstance(unavailable, RejectedResult)
        self.assertEqual(unavailable.outcome, "unavailable")

        path_read = self.engine.query(
            QueryCall(self.engine.view, ReadRequest("read", "workflows/verification.md"))
        )
        self.assertIsInstance(path_read, RejectedResult)

    def test_agent_facade_uses_structured_authority_handles(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            shutil.copytree(
                REPO_ROOT,
                root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            tool = AgentToolFacade.open_repository(root)
            route = tool.query(
                {
                    "view": tool.view,
                    "request": {
                        "kind": "route",
                        "facts": self.route_facts(
                            **{"routing.activities": ["implementation"]}
                        ),
                    },
                }
            )
            self.assertEqual(route["kind"], "route-result")
            read = tool.query(
                {
                    "view": tool.view,
                    "request": {"kind": "read", "target": "workflow.implementation"},
                }
            )
            self.assertEqual(read["kind"], "read-result")


if __name__ == "__main__":
    unittest.main()
