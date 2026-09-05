from __future__ import annotations

# ruff: noqa: E402 - the standalone verifier package root precedes local imports.

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))


class FileContractsTest(unittest.TestCase):
    def test_navigation_contract_accepts_rewording_but_requires_real_links(self):
        from standards_verifier.checks.markdown_targets import (
            parse_markdown_targets_check,
        )
        from standards_verifier.model import CheckContext, SuiteCatalog

        self.write("topics/policy.md", "# Policy")
        check = parse_markdown_targets_check(
            {
                "id": "navigation",
                "type": "markdown_targets",
                "path": "docs/index.md",
                "required": ["topics/policy.md"],
            },
            "files",
        )
        context = CheckContext(self.root, "files", SuiteCatalog.empty())
        for prose in (
            "See [Policy](../topics/policy.md).",
            "Different introduction.\n\n[Guidance](../topics/policy.md#detail) concludes this index.",
        ):
            self.write("docs/index.md", prose)
            self.assertEqual(check.run(context), [])
        self.write("docs/index.md", "The path topics/policy.md appears only as prose.")
        self.assertEqual(
            [item.code for item in check.run(context)],
            ["ASSERT.MARKDOWN_TARGET_MISSING"],
        )

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.external_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.external_dir.cleanup()
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
