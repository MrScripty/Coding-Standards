from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.standards_engine.contracts.validate_contracts import validate
from tools.standards_engine.standards_engine import (
    InspectCall,
    PolicyInspectionResult,
    QueryCall,
    ReadRequest,
    ReadResult,
    RejectedResult,
    RelatedRequest,
    RelatedResult,
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

    def test_module_read_and_inspection_use_derived_whole_artifact_authority(self) -> None:
        result = self.engine.query(
            QueryCall(self.engine.snapshot, ReadRequest("workflow.verification"))
        )

        self.assertIsInstance(result, ReadResult)
        value = self.assert_contract("ReadResult", result)
        self.assertEqual(value["policy"]["scope"], {"kind": "whole-artifact"})
        self.assertIn("# Verification", value["content"])

        inspection = self.engine.inspect(
            InspectCall(value["policy"]["handle"])
        )
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

    def test_nontransitive_group_and_unknown_group_return_typed_rejections(self) -> None:
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

        navigation = self.engine.inspect(InspectCall(value["handle"]))
        navigation_value = self.assert_contract("NavigationInspectionResult", navigation)
        self.assertEqual(navigation_value["navigation"]["handle"], value["handle"])

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

    def test_policy_unit_target_is_normalized_and_malformed_native_calls_are_rejected(self) -> None:
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
        self.assertEqual(related_value["target"], "workflow.verification")

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
