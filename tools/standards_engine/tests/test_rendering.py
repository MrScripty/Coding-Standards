from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.standards_engine.standards_engine import RejectedResult, render_text


REPO_ROOT = Path(__file__).resolve().parents[3]


class TextRenderingTest(unittest.TestCase):
    def test_pending_projection_is_deterministic_and_work_focused(self) -> None:
        pending = {
            "kind": "pending-result",
            "handle": {"id": "analysis-root:sha256:" + "1" * 64},
            "fact_requirements": [
                {
                    "requirement": {
                        "handle": {"child_id": "sha256:" + "2" * 64},
                        "fact": "change.requires-review",
                    },
                }
            ],
            "obligations": [
                {
                    "handle": {"child_id": "sha256:" + "3" * 64},
                    "target": "workflow.documentation",
                    "state": "required",
                }
            ],
            "next_operations": [
                {
                    "operation": "resolve",
                    "request_kind": "provide-fact",
                    "target": "change.requires-review",
                }
            ],
        }
        first = render_text(pending)
        second = render_text(pending)

        self.assertEqual(first, second)
        self.assertIn("FACT REQUIREMENTS", first)
        self.assertIn("REVIEWS", first)
        self.assertIn("NEXT", first)
        self.assertNotIn("TOML", first)

    def test_rejection_projection_accepts_the_generated_result_type(self) -> None:
        result = RejectedResult.from_value(
            {
                "kind": "rejected-result",
                "code": "SUBMISSION.CONTEXT_MISMATCH",
                "outcome": "invalid",
                "message": "The submission does not address current work.",
                "details": {},
                "next_operations": [],
            }
        )
        self.assertEqual(
            render_text(result),
            "REJECTED SUBMISSION.CONTEXT_MISMATCH\n"
            "OUTCOME invalid\n"
            "MESSAGE The submission does not address current work.\n",
        )

    def test_proposal_projection_exposes_only_opaque_handles(self) -> None:
        proposal = "proposal:v1:00000000-0000-4000-8000-000000000001"
        revision = "proposal-revision:sha256:" + "a" * 64

        self.assertEqual(
            render_text(
                {
                    "kind": "create-proposal-result",
                    "proposal": {"id": proposal},
                    "revision": {"id": revision},
                }
            ),
            f"CREATE-PROPOSAL-RESULT {proposal} {revision}\n",
        )

    def test_projected_navigation_renders_revision_authority(self) -> None:
        revision = "proposal-revision:sha256:" + "a" * 64

        self.assertEqual(
            render_text(
                {
                    "kind": "proposal-read-result",
                    "revision": {"id": revision},
                    "policy": {"id": "workflow.planning"},
                    "relationships": [],
                }
            ),
            f"NAVIGATION {revision}\n  POLICY workflow.planning\n",
        )

    def test_proposal_review_renders_only_opaque_authority(self) -> None:
        revision = "proposal-revision:sha256:" + "a" * 64
        readiness = "readiness:sha256:" + "b" * 64

        self.assertEqual(
            render_text(
                {
                    "kind": "review-proposal-result",
                    "readiness": {"id": readiness},
                    "revision": {"id": revision},
                    "status": "ready",
                }
            ),
            f"PROPOSAL REVIEW {revision} {readiness} [ready]\n",
        )

    def test_every_public_result_kind_has_a_rendering_dispatch(self) -> None:
        schema = json.loads(
            (
                REPO_ROOT
                / "tools/standards_engine/contracts/a1-contract.schema.json"
            ).read_text(encoding="utf-8")
        )
        kinds = {
            node["properties"]["kind"]["const"]
            for node in schema["$defs"].values()
            if isinstance(node, dict)
            and isinstance(node.get("properties"), dict)
            and isinstance(node["properties"].get("kind"), dict)
            and isinstance(node["properties"]["kind"].get("const"), str)
            and (
                node["properties"]["kind"]["const"].endswith("-result")
                or node["properties"]["kind"]["const"] == "analysis-state"
            )
        }
        directly_rendered = {
            "pending-result",
            "complete-result",
            "analysis-state",
            "route-result",
            "read-result",
            "related-result",
            "rejected-result",
            "create-snapshot-result",
            "find-snapshots-result",
            "delete-snapshot-result",
            "undelete-snapshot-result",
            "create-proposal-result",
            "find-proposals-result",
            "revise-proposal-result",
            "review-proposal-result",
            "apply-proposal-result",
            "application-recovery-required-result",
            "proposal-route-result",
            "proposal-read-result",
            "proposal-related-result",
        }
        unsupported = {
            kind
            for kind in kinds
            if kind not in directly_rendered and not kind.endswith("-inspection-result")
        }
        self.assertEqual(unsupported, set())

    def test_unknown_result_variant_is_a_programming_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported Standards Engine"):
            render_text({"kind": "future-result"})


if __name__ == "__main__":
    unittest.main()
