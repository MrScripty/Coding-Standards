from __future__ import annotations

import unittest

from tools.standards_engine.standards_engine import render_text


class TextRenderingTest(unittest.TestCase):
    def test_packet_projection_is_deterministic_and_work_focused(self) -> None:
        packet = {
            "kind": "pending-result",
            "handle": {"id": "analysis:sha256:" + "1" * 64},
            "fact_requirements": [
                {
                    "handle": {"id": "fact-requirement:sha256:" + "2" * 64},
                    "fact": "change.requires-review",
                }
            ],
            "obligations": [
                {
                    "id": "obligation:sha256:" + "3" * 64,
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
        first = render_text(packet)
        second = render_text(packet)

        self.assertEqual(first, second)
        self.assertIn("FACT REQUIREMENTS", first)
        self.assertIn("REVIEWS", first)
        self.assertIn("NEXT", first)
        self.assertNotIn("TOML", first)

    def test_rejection_projection_uses_only_typed_fields(self) -> None:
        rendered = render_text(
            {
                "kind": "rejected-result",
                "code": "SUBMISSION.CONTEXT_MISMATCH",
                "outcome": "invalid",
                "message": "The submission does not address current work.",
            }
        )
        self.assertEqual(
            rendered,
            "REJECTED SUBMISSION.CONTEXT_MISMATCH\n"
            "OUTCOME invalid\n"
            "MESSAGE The submission does not address current work.\n",
        )


if __name__ == "__main__":
    unittest.main()
