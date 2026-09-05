from __future__ import annotations

import unittest
from pathlib import Path

from tools.standards_engine.standards_engine import RejectedResult, render_text


REPO_ROOT = Path(__file__).resolve().parents[3]


class TextRenderingTest(unittest.TestCase):
    def test_navigation_indexes_preserve_authority_and_exact_content(self):
        content = "# navigation.old\n\n- [Owner](owner.md)\n"
        rendered = render_text(
            {
                "kind": "navigation-indexes-result",
                "authority": {"id": "snapshot:exact"},
                "indexes": [
                    {
                        "id": "navigation.old",
                        "destinations": ["topic.owner"],
                        "content": content,
                    }
                ],
            }
        )
        self.assertIn("snapshot:exact", rendered)
        self.assertIn("NON-NORMATIVE", rendered)
        self.assertIn(content, rendered)

    def test_coverage_projection_preserves_subject_and_status(self):
        for status in ("current-attestation", "review-required"):
            subject = "workflow.planning.acceptance-claims"
            rendered = render_text(
                {
                    "kind": "read-result",
                    "coverage": {"subjects": [{"subject": subject, "status": status}]},
                }
            )
            self.assertIn(subject, rendered)
            self.assertIn(status, rendered)

    def test_verification_projection_preserves_revision_and_diagnostic_identity(self):
        revision = "proposal-revision:sha256:" + "a" * 64
        report = {
            "passed": False,
            "exit_code": 1,
            "suites": 1,
            "checks": 1,
            "failures": [
                {
                    "code": "ASSERT.MARKDOWN_TARGET_MISSING",
                    "message": "Required destination is absent.",
                    "suite": "navigation",
                    "check": "owners",
                }
            ],
        }
        for kind in ("verify-repository-result", "verify-proposal-result"):
            rendered = render_text(
                {"kind": kind, "verification": report, "revision": {"id": revision}}
            )
            self.assertIn(revision, rendered)
            self.assertIn(report["failures"][0]["code"], rendered)

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

    def test_unknown_result_variant_is_a_programming_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported Standards Engine"):
            render_text({"kind": "future-result"})


if __name__ == "__main__":
    unittest.main()
