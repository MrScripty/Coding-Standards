"""Router presentation is selected by table structure, not display headings."""
from __future__ import annotations

from pathlib import Path
import re
import unittest

from tools.standards_analysis.standards_analysis import AnalysisError, load_router_projection
from tools.standards_metadata.standards_metadata import (
    DirectoryContentSource, load_canonical_module_corpus,
)

ROOT = Path(__file__).resolve().parents[3]


class Overlay:
    def __init__(self, text: str):
        self.base = DirectoryContentSource(ROOT)
        self.text = text

    def read_bytes(self, path: str) -> bytes:
        return self.text.encode() if path == "STANDARDS-ROUTER.md" else self.base.read_bytes(path)


class RouterGuidanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / "STANDARDS-ROUTER.md").read_text()
        cls.modules = load_canonical_module_corpus(ROOT)

    def test_display_headings_are_free(self):
        edited = re.sub(r"(?m)^(#{1,6}) [^\n]+$", r"\1 Neutral display heading", self.text)
        original = load_router_projection(ROOT, self.modules)
        actual = load_router_projection(Overlay(edited), self.modules)
        self.assertEqual([(r.id, r.target) for r in actual.rules],
                         [(r.id, r.target) for r in original.rules])

    def test_historical_example_can_be_removed(self):
        # The regression remains usable after the real corpus retires the title.
        without_example = re.sub(
            r"(?ms)^## S1 Rust Library Bug-Fix Route\n.*?(?=^## |\Z)", "", self.text)
        with_example = without_example + "\n## S1 Rust Library Bug-Fix Route\n\nOptional explanatory material.\n"
        actual = load_router_projection(Overlay(without_example), self.modules)
        example = load_router_projection(Overlay(with_example), self.modules)
        self.assertEqual([(r.id, r.target) for r in actual.rules],
                         [(r.id, r.target) for r in example.rules])

    def parse(self, text):
        from tools.standards_analysis.standards_analysis import parse_router_guidance
        return parse_router_guidance(text, self.modules)

    def test_fenced_and_prose_links_are_not_selections(self):
        extra = '\n[Other](does-not-exist.md)\n\n```markdown\n| What | Where |\n| --- | --- |\n| A | [Fake](../escape.md) |\n```\n'
        self.assertEqual(self.parse(self.text + extra).targets, self.parse(self.text).targets)

    def test_reference_is_not_a_normative_route(self):
        reference = next(m for m in self.modules.modules if m.role == "reference")
        extra = f'\n| Example | Reference |\n| --- | --- |\n| Optional | [Help]({reference.path}) |\n'
        self.assertEqual(self.parse(self.text + extra).targets, self.parse(self.text).targets)
        self.assertEqual(self.parse(self.text + extra).insertion_offset, self.parse(self.text).insertion_offset)

    def test_escaping_and_exact_offsets(self):
        text = '| Situation | Destination |\n| :--- | ---: |\n| A \\| B | [Implementation](workflows/implementation.md) |\n'
        guidance = self.parse(text)
        row, = guidance.rows
        self.assertEqual(row.condition, 'A | B')
        self.assertEqual(row.targets, ('workflow.implementation',))
        self.assertEqual(text[row.start:row.end], '| A \\| B | [Implementation](workflows/implementation.md) |\n')
        self.assertEqual(guidance.insertion_offset, len(text))

    def test_invalid_destination_is_rejected(self):
        for path in ('../escape.md', '/root.md', './workflows/implementation.md', 'unknown.md'):
            with self.subTest(path=path), self.assertRaises(AnalysisError):
                self.parse(f'| Task | Select |\n| --- | --- |\n| A | [Rule]({path}) |\n')

    def test_code_and_html_comments_do_not_create_tables(self):
        text = '<!--\n| x | y |\n| --- | --- |\n| x | [bad](../bad.md) |\n-->\n'
        text += '~~~\n| x | y |\n| --- | --- |\n| x | [bad](../bad.md) |\n~~~\n'
        self.assertEqual(self.parse(self.text + text).targets, self.parse(self.text).targets)


if __name__ == '__main__':
    unittest.main()
