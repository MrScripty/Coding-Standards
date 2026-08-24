from __future__ import annotations

import json
import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.standards_engine.contracts.validate_contracts import validate
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
    RouteRequest,
    RouteResult,
    RelationshipInspectionResult,
    StandardsEngine,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json").read_text(
        encoding="utf-8"
    )
)


class NavigationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = StandardsEngine.open_repository(REPO_ROOT)

    def assert_contract(self, definition: str, result) -> dict[str, object]:
        value = result.as_contract()
        validate(SCHEMA, SCHEMA["$defs"][definition], value, "$result")
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

    def test_route_selects_direct_modules_and_graph_derived_closure(self) -> None:
        result = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RouteRequest(
                    self.route_facts(
                        **{
                            "routing.activities": ["implementation", "verification"],
                            "routing.applications": ["library"],
                            "routing.languages": ["rust"],
                        }
                    )
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
        persistence = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RouteRequest(
                    self.route_facts(
                        **{
                            "routing.activities": ["implementation", "verification"],
                            "routing.boundaries": ["persistence"],
                        }
                    )
                ),
            )
        ).as_contract()
        self.assertIn(
            "topic.contracts",
            {item["target"] for item in persistence["reading_plan"]},
        )

    def test_snapshot_binds_coverage_authority_and_attestation_inputs(self) -> None:
        result = self.engine.inspect(InspectCall(self.engine.snapshot))
        value = self.assert_contract("SnapshotInspectionResult", result)
        scope = set(value["snapshot"]["scope"])

        self.assertTrue(
            {
                "evaluation/standards-effectiveness/policy-coverage/horizons.toml",
                "evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml",
                "evaluation/standards-effectiveness/policy-coverage/attestations/workflow.planning.toml",
                "evaluation/standards-effectiveness/policy-coverage/attestations/workflow.commit.toml",
                "docs/plans/standards-engine-navigation-analysis/reports/milestone-4-horizon-v2-audit.md",
            }.issubset(scope)
        )

    def test_route_unknown_categories_remain_visible_and_invalid_facts_reject(
        self,
    ) -> None:
        facts = self.route_facts()
        facts["routing.topics"] = {"type": "enum-set", "state": "unknown"}
        result = self.engine.query(QueryCall(self.engine.snapshot, RouteRequest(facts)))
        value = self.assert_contract("RouteResult", result)
        self.assertEqual(
            [item["id"] for item in value["unresolved_questions"]],
            ["question.routing.topics"],
        )
        self.assertTrue(
            all(
                item["state"] == "unresolved"
                for item in value["reading_plan"]
                if item["target"].startswith("topic.")
            )
        )

        invalid = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RouteRequest(
                    {
                        "routing.undeclared": {
                            "type": "boolean",
                            "state": "known",
                            "value": True,
                        }
                    }
                ),
            )
        )
        invalid_value = self.assert_contract("RejectedResult", invalid)
        self.assertEqual(invalid_value["code"], "APPLICABILITY.INVALID")

    def test_verifier_change_fixture_matches_public_route_projection(self) -> None:
        decisions_path = (
            REPO_ROOT
            / "evaluation/standards-effectiveness/fixtures/routing/verifier-change-decisions.tsv"
        )
        routes_path = (
            REPO_ROOT
            / "evaluation/standards-effectiveness/fixtures/routing/verifier-change-routes.tsv"
        )
        with decisions_path.open(encoding="utf-8", newline="") as handle:
            decisions = {
                row["case"]: row for row in csv.DictReader(handle, delimiter="\t")
            }
        with routes_path.open(encoding="utf-8", newline="") as handle:
            routes = {
                row["case"]: row for row in csv.DictReader(handle, delimiter="\t")
            }

        for case, row in decisions.items():
            facts = self.route_facts(
                **{
                    "routing.activities": [
                        "implementation",
                        "verification",
                        *(["planning"] if row["expected_planning"] == "select" else []),
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
                QueryCall(self.engine.snapshot, RouteRequest(facts))
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
            self.assertEqual(
                direct, set(routes[case]["direct_modules"].split(",")), case
            )
            self.assertEqual(
                closure, set(routes[case]["requires_closure"].split(",")), case
            )

    def test_route_retains_direct_and_every_dependency_cause(self) -> None:
        value = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RouteRequest(
                    self.route_facts(
                        **{
                            "routing.activities": [
                                "implementation",
                                "verification",
                                "planning",
                            ]
                        }
                    )
                ),
            )
        ).as_contract()
        entries = {item["target"]: item for item in value["reading_plan"]}
        core_reasons = entries["core"]["reasons"]
        implementation_reasons = entries["workflow.implementation"]["reasons"]
        self.assertTrue(
            any(reason["kind"] == "routing-rule" for reason in implementation_reasons)
        )
        self.assertTrue(
            any(reason["kind"] == "requires" for reason in implementation_reasons)
        )
        requires = [reason for reason in core_reasons if reason["kind"] == "requires"]
        self.assertEqual(
            len(requires),
            len({(reason["edge"], reason["source"]) for reason in requires}),
        )
        self.assertGreaterEqual(len(requires), 3)

    def test_route_result_can_drive_same_snapshot_read(self) -> None:
        route = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RouteRequest(
                    self.route_facts(**{"routing.activities": ["implementation"]})
                ),
            )
        ).as_contract()
        target = next(
            item["target"]
            for item in route["reading_plan"]
            if item["target"] == "workflow.implementation"
        )
        read = self.engine.query(QueryCall(self.engine.snapshot, ReadRequest(target)))
        self.assertIsInstance(read, ReadResult)

    def test_module_read_uses_immutable_snapshot_content_after_source_mutation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            shutil.copytree(
                REPO_ROOT,
                root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            engine = StandardsEngine.open_repository(root)
            issued = dict(engine.snapshot)
            original = engine.query(
                QueryCall(issued, ReadRequest("workflow.verification"))
            ).as_contract()["content"]

            source = root / "workflows/verification.md"
            source.write_text(
                source.read_text(encoding="utf-8") + "\nMUTATED AFTER SNAPSHOT\n",
                encoding="utf-8",
            )

            repeated = engine.query(
                QueryCall(issued, ReadRequest("workflow.verification"))
            ).as_contract()
            self.assertEqual(repeated["content"], original)
            self.assertNotIn("MUTATED AFTER SNAPSHOT", repeated["content"])

    def test_navigation_next_operations_bind_the_issued_snapshot(self) -> None:
        result = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RouteRequest(
                    self.route_facts(**{"routing.activities": ["implementation"]})
                ),
            )
        ).as_contract()

        self.assertTrue(result["next_operations"])
        self.assertTrue(
            all(
                operation["snapshot"] == self.engine.snapshot
                for operation in result["next_operations"]
            )
        )

    def test_structured_agent_tool_routes_then_reads_without_repository_paths(
        self,
    ) -> None:
        tool = AgentToolFacade.open_repository(REPO_ROOT)
        route = tool.query(
            {
                "snapshot": dict(tool.snapshot),
                "request": {
                    "kind": "route",
                    "facts": self.route_facts(
                        **{"routing.activities": ["implementation"]}
                    ),
                },
            }
        )
        self.assertEqual(route["kind"], "route-result")
        selected = {
            item["target"]
            for item in route["reading_plan"]
            if item["state"] == "selected"
        }
        self.assertIn("workflow.implementation", selected)

        read = tool.query(
            {
                "snapshot": dict(tool.snapshot),
                "request": {"kind": "read", "target": "workflow.implementation"},
            }
        )
        self.assertEqual(read["kind"], "read-result")
        self.assertNotIn("path", read)

        invalid = tool.query(
            {
                "snapshot": dict(tool.snapshot),
                "request": {
                    "kind": "read",
                    "target": "workflow.implementation",
                    "extra": True,
                },
            }
        )
        self.assertEqual(invalid["code"], "INTERFACE.INVALID_ARGUMENTS")

    def test_module_read_and_inspection_use_derived_whole_artifact_authority(
        self,
    ) -> None:
        result = self.engine.query(
            QueryCall(self.engine.snapshot, ReadRequest("workflow.verification"))
        )

        self.assertIsInstance(result, ReadResult)
        value = self.assert_contract("ReadResult", result)
        self.assertEqual(value["policy"]["scope"], {"kind": "whole-artifact"})
        self.assertIn("# Verification", value["content"])

        inspection = self.engine.inspect(InspectCall(value["policy"]["handle"]))
        self.assertIsInstance(inspection, PolicyInspectionResult)
        inspected = self.assert_contract("PolicyInspectionResult", inspection)
        self.assertEqual(inspected["declaration"]["kind"], "canonical-module")
        self.assertEqual(inspected["declaration"]["id"], "workflow.verification")

    def test_policy_unit_read_and_inspection_use_exact_structured_scope(self) -> None:
        policy_id = "workflow.verification.acceptance-claims"
        result = self.engine.query(
            QueryCall(self.engine.snapshot, ReadRequest(policy_id))
        )

        self.assertIsInstance(result, ReadResult)
        value = self.assert_contract("ReadResult", result)
        self.assertEqual(
            value["policy"]["scope"],
            {"kind": "structured", "heading_path": ["Acceptance Is A Set Of Claims"]},
        )
        self.assertTrue(value["content"].startswith("## Acceptance Is A Set Of Claims"))

        inspection = self.engine.inspect(InspectCall(value["policy"]["handle"]))
        inspected = self.assert_contract("PolicyInspectionResult", inspection)
        self.assertEqual(inspected["declaration"]["kind"], "policy-unit")
        self.assertEqual(inspected["declaration"]["id"], policy_id)

    def test_related_uses_exact_groups_and_generic_transitive_traversal(self) -> None:
        direct = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RelatedRequest(
                    "workflow.planning",
                    ("standards-requires",),
                    "outgoing",
                ),
            )
        )
        self.assertIsInstance(direct, RelatedResult)
        direct_value = self.assert_contract("RelatedResult", direct)
        direct_targets = {item["target"] for item in direct_value["relationships"]}
        self.assertIn("workflow.verification", direct_targets)
        self.assertEqual(
            direct_value["policy_unit_mapping"]["state"],
            "policy-units-present",
        )

        transitive = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RelatedRequest(
                    "workflow.planning",
                    ("standards-requires",),
                    "outgoing",
                    transitive=True,
                ),
            )
        )
        transitive_value = self.assert_contract("RelatedResult", transitive)
        transitive_targets = {
            item["target"] for item in transitive_value["relationships"]
        }
        self.assertIn("core", transitive_targets)

    def test_nontransitive_group_and_unknown_group_return_typed_rejections(
        self,
    ) -> None:
        forbidden = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RelatedRequest(
                    "workflow.planning",
                    ("policy-impact",),
                    "outgoing",
                    transitive=True,
                ),
            )
        )
        self.assertIsInstance(forbidden, RejectedResult)
        forbidden_value = self.assert_contract("RejectedResult", forbidden)
        self.assertEqual(forbidden_value["code"], "GRAPH.FORBIDDEN_TRAVERSAL")

        unknown = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RelatedRequest("workflow.planning", ("missing-group",), "outgoing"),
            )
        )
        unknown_value = self.assert_contract("RejectedResult", unknown)
        self.assertEqual(unknown_value["code"], "GRAPH.UNKNOWN_GROUP")

    def test_relationship_and_navigation_handles_are_exactly_inspectable(self) -> None:
        result = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RelatedRequest(
                    "workflow.planning",
                    ("standards-requires",),
                    "outgoing",
                ),
            )
        )
        value = result.as_contract()
        relationship_handle = value["relationships"][0]["handle"]
        relationship = self.engine.inspect(InspectCall(relationship_handle))

        self.assertIsInstance(relationship, RelationshipInspectionResult)
        inspected = self.assert_contract("RelationshipInspectionResult", relationship)
        self.assertEqual(
            inspected["relationship"]["handle"]["id"],
            relationship_handle["id"],
        )
        self.assertIsNone(inspected["policy_semantics"])

        policy_result = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RelatedRequest(
                    "workflow.planning",
                    ("policy-impact",),
                    "outgoing",
                ),
            )
        ).as_contract()
        policy_handle = policy_result["relationships"][0]["handle"]
        policy_inspection = self.assert_contract(
            "RelationshipInspectionResult",
            self.engine.inspect(InspectCall(policy_handle)),
        )
        semantics = policy_inspection["policy_semantics"]
        self.assertIsNotNone(semantics)
        assert semantics is not None
        self.assertEqual(semantics["edge_id"], policy_handle["id"])
        self.assertTrue(semantics["source"].startswith("workflow.planning."))
        self.assertNotEqual(semantics["source"], "workflow.planning")
        program = semantics["applicability_program"]
        self.assertEqual(program["normalized_expression"], {"operator": "always"})
        self.assertEqual(program["referenced_facts"], [])
        self.assertEqual(program["language_version"], 1)
        self.assertTrue(program["schema_digest"].startswith("sha256:"))
        self.assertTrue(program["dependency_digest"].startswith("sha256:"))
        self.assertEqual(semantics["propagation"], "source-to-consumer")
        self.assertTrue(semantics["evidence_owner"].startswith("suite:"))
        self.assertTrue(semantics["rationale"])
        self.assertTrue(
            semantics["declaration_source"].endswith("workflow.planning.toml")
        )

        navigation = self.engine.inspect(InspectCall(value["handle"]))
        navigation_value = self.assert_contract(
            "NavigationInspectionResult", navigation
        )
        self.assertEqual(navigation_value["navigation"]["handle"], value["handle"])

    def test_every_advertised_coverage_handle_is_inspectable(self) -> None:
        cases = (
            (
                "views",
                "CoverageAuthorityViewInspectionResult",
                "coverage_view",
            ),
            (
                "requirements",
                "CoverageRequirementInspectionResult",
                "requirement",
            ),
            (
                "attestations",
                "CoverageAttestationInspectionResult",
                "attestation",
            ),
            (
                "certificates",
                "CertificateInspectionResult",
                "certificate",
            ),
        )
        for collection, definition, field in cases:
            with self.subTest(collection=collection):
                artifact = next(
                    iter(getattr(self.engine._coverage, collection).values())
                )
                projection = artifact.as_projection()
                result = self.engine.inspect(InspectCall(projection["handle"]))
                value = self.assert_contract(definition, result)
                self.assertEqual(value[field], projection)

    def test_agent_facade_does_not_relabel_engine_programming_errors(self) -> None:
        class FailingEngine:
            snapshot = self.engine.snapshot

            def query(self, _call):
                raise ValueError("engine invariant failure")

        tool = AgentToolFacade(FailingEngine(), SCHEMA)
        with self.assertRaisesRegex(ValueError, "engine invariant failure"):
            tool.query(
                {
                    "snapshot": dict(self.engine.snapshot),
                    "request": {
                        "kind": "read",
                        "target": "workflow.verification",
                    },
                }
            )

    def test_stale_snapshot_and_repository_path_read_do_not_fall_back(self) -> None:
        stale = dict(self.engine.snapshot)
        stale["id"] = f"snapshot:sha256:{'0' * 64}"
        stale_result = self.engine.query(
            QueryCall(stale, ReadRequest("workflow.verification"))
        )
        stale_value = self.assert_contract("RejectedResult", stale_result)
        self.assertEqual(stale_value["outcome"], "stale")

        path_result = self.engine.query(
            QueryCall(self.engine.snapshot, ReadRequest("workflows/verification.md"))
        )
        path_value = self.assert_contract("RejectedResult", path_result)
        self.assertEqual(path_value["code"], "NAVIGATION.UNKNOWN_POLICY")

    def test_policy_unit_target_is_normalized_and_malformed_native_calls_are_rejected(
        self,
    ) -> None:
        related = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RelatedRequest(
                    "workflow.verification.acceptance-claims",
                    ("standards-requires",),
                    "outgoing",
                ),
            )
        )
        related_value = self.assert_contract("RelatedResult", related)
        self.assertEqual(
            related_value["target"],
            "workflow.verification.acceptance-claims",
        )
        self.assertEqual(
            related_value["policy_unit_mapping"]["state"],
            "exact-policy-unit",
        )

        unmapped = self.engine.query(
            QueryCall(
                self.engine.snapshot,
                RelatedRequest("core", ("policy-impact",), "outgoing"),
            )
        )
        unmapped_value = self.assert_contract("RelatedResult", unmapped)
        self.assertEqual(
            unmapped_value["policy_unit_mapping"],
            {
                "state": "incomplete",
                "reason": "no-policy-units",
                "policy_units": [],
            },
        )

        malformed = (
            ReadRequest(""),
            RelatedRequest("workflow.planning", (), "outgoing"),
            RelatedRequest("workflow.planning", ("standards-requires",), "sideways"),
            RelatedRequest(
                "workflow.planning",
                ("standards-requires",),
                "outgoing",
                transitive=1,
            ),
        )
        for request in malformed:
            with self.subTest(request=request):
                result = self.engine.query(QueryCall(self.engine.snapshot, request))
                value = self.assert_contract("RejectedResult", result)
                self.assertEqual(value["outcome"], "invalid")


if __name__ == "__main__":
    unittest.main()
