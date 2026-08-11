from __future__ import annotations

import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.diagnostics import EngineError
from standards_verifier.engine import Verifier


class RoutingChecksTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.external_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.registry = "registry.toml"

    def tearDown(self) -> None:
        self.external_dir.cleanup()
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_registry(self, suite_path: str) -> None:
        self.write(
            self.registry,
            f"""
            schema_version = 1

            [[suites]]
            id = "routing"
            path = {json.dumps(suite_path)}
            requires = []
            """,
        )

    def write_markdown_suite(
        self,
        *,
        paths: str = '["docs/index.md"]',
        extra: str = "",
    ) -> str:
        suite_path = "suites/routing.toml"
        self.write(
            suite_path,
            f"""
            schema_version = 1
            id = "routing"
            owner = "test.owner"
            description = "Markdown link test"

            [[checks]]
            id = "links"
            type = "markdown_links"
            paths = {paths}
            {extra}
            """,
        )
        return suite_path

    def write_line_budget_suite(
        self,
        *,
        paths: str = '["docs/a.md", "docs/b.md"]',
        baseline_path: str = "metrics.tsv",
        baseline_key: str = "total",
        numerator: str = "1",
        denominator: str = "4",
        extra: str = "",
    ) -> str:
        suite_path = "suites/routing.toml"
        self.write(
            suite_path,
            f"""
            schema_version = 1
            id = "routing"
            owner = "test.owner"
            description = "Line budget test"

            [[checks]]
            id = "budget"
            type = "line_budget"
            paths = {paths}
            baseline_path = {json.dumps(baseline_path)}
            baseline_key = {json.dumps(baseline_key)}
            maximum_numerator = {numerator}
            maximum_denominator = {denominator}
            {extra}
            """,
        )
        return suite_path

    def result(self, suite_path: str):
        self.write_registry(suite_path)
        return Verifier(self.root, self.registry).run()[0]

    def prepare_budget(self, baseline: str = "20") -> None:
        self.write("docs/a.md", "a\nb\n")
        self.write("docs/b.md", "c\nd\n")
        self.write("metrics.tsv", f"metric\tvalue\ntotal\t{baseline}\n")

    def test_markdown_links_accept_nested_fragments_and_external_targets(self) -> None:
        self.write(
            "docs/index.md",
            """
            [nested](nested/target.md#section)
            [self](#heading)
            [web](https://example.com/page)
            [plain](http://example.com)
            [mail](mailto:test@example.com)
            """,
        )
        self.write("docs/nested/target.md", "target\n")

        result = self.result(self.write_markdown_suite())

        self.assertEqual(result.status, "passed")

    def test_markdown_links_missing_target_is_unavailable(self) -> None:
        self.write("docs/index.md", "[missing](missing.md)\n")

        result = self.result(self.write_markdown_suite())

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.LINK_TARGET_UNAVAILABLE")

    def test_markdown_links_absolute_target_is_invalid(self) -> None:
        self.write("docs/index.md", "[absolute](/etc/passwd)\n")

        result = self.result(self.write_markdown_suite())

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "PATH.LINK_OUTSIDE_REPOSITORY")

    def test_markdown_links_parent_escape_is_invalid(self) -> None:
        self.write("docs/index.md", "[escape](../../outside.md)\n")

        result = self.result(self.write_markdown_suite())

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "PATH.LINK_OUTSIDE_REPOSITORY")

    def test_markdown_links_symlink_escape_is_invalid(self) -> None:
        external = Path(self.external_dir.name)
        (external / "target.md").write_text("target\n", encoding="utf-8")
        (self.root / "docs").mkdir(parents=True)
        (self.root / "docs" / "escape").symlink_to(external, target_is_directory=True)
        self.write("docs/index.md", "[escape](escape/target.md)\n")

        result = self.result(self.write_markdown_suite())

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "PATH.LINK_OUTSIDE_REPOSITORY")

    def test_markdown_links_missing_source_is_unavailable(self) -> None:
        result = self.result(self.write_markdown_suite(paths='["missing.md"]'))

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_markdown_links_invalid_utf8_is_invalid(self) -> None:
        target = self.root / "docs/index.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"\xff")

        result = self.result(self.write_markdown_suite())

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "INPUT.INVALID_UTF8")

    def test_markdown_links_paths_must_be_non_empty_and_unique(self) -> None:
        for paths in ("[]", '["docs/index.md", "docs/index.md"]'):
            with self.subTest(paths=paths):
                suite_path = self.write_markdown_suite(paths=paths)
                self.write_registry(suite_path)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, self.registry)
                self.assertEqual(raised.exception.diagnostic.code, "CONFIG.STRING_LIST")

    def test_markdown_links_unknown_field_is_invalid(self) -> None:
        suite_path = self.write_markdown_suite(extra="network = true")
        self.write_registry(suite_path)

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")
        self.assertEqual(raised.exception.diagnostic.field, "network")

    def test_line_budget_passes_strict_integer_ratio(self) -> None:
        self.prepare_budget("20")

        result = self.result(self.write_line_budget_suite())

        self.assertEqual(result.status, "passed")

    def test_line_budget_counts_raw_newline_bytes(self) -> None:
        self.write("docs/a.md", "a\nb")
        self.write("metrics.tsv", "metric\tvalue\ntotal\t5\n")

        result = self.result(
            self.write_line_budget_suite(paths='["docs/a.md"]')
        )

        self.assertEqual(result.status, "passed")

    def test_line_budget_rejects_equality_and_excess(self) -> None:
        for baseline in ("16", "12"):
            with self.subTest(baseline=baseline):
                self.prepare_budget(baseline)
                result = self.result(self.write_line_budget_suite())
                self.assertEqual(result.exit_code, 1)
                self.assertEqual(result.diagnostics[0].code, "ASSERT.LINE_BUDGET")

    def test_line_budget_requires_exact_metric_header(self) -> None:
        self.prepare_budget()
        self.write("metrics.tsv", "name\tvalue\ntotal\t20\n")

        result = self.result(self.write_line_budget_suite())

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "TABLE.HEADER_CONTRACT")

    def test_line_budget_rejects_malformed_metric_row(self) -> None:
        self.prepare_budget()
        self.write("metrics.tsv", "metric\tvalue\ntotal\n")

        result = self.result(self.write_line_budget_suite())

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "TABLE.ROW_WIDTH")

    def test_line_budget_rejects_duplicate_metric(self) -> None:
        self.prepare_budget()
        self.write("metrics.tsv", "metric\tvalue\ntotal\t20\ntotal\t21\n")

        result = self.result(self.write_line_budget_suite())

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "TABLE.DUPLICATE_BASELINE_KEY")

    def test_line_budget_missing_metric_is_unavailable(self) -> None:
        self.prepare_budget()

        result = self.result(
            self.write_line_budget_suite(baseline_key="missing")
        )

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.BASELINE_KEY_UNAVAILABLE")

    def test_line_budget_requires_positive_decimal_metric(self) -> None:
        for baseline in ("0", "1.5", "-1", "٢"):
            with self.subTest(baseline=baseline):
                self.prepare_budget(baseline)
                result = self.result(self.write_line_budget_suite())
                self.assertEqual(result.exit_code, 2)
                self.assertEqual(result.diagnostics[0].code, "TABLE.BASELINE_VALUE")

    def test_line_budget_missing_input_is_unavailable(self) -> None:
        self.write("metrics.tsv", "metric\tvalue\ntotal\t20\n")

        result = self.result(
            self.write_line_budget_suite(paths='["missing.md"]')
        )

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_line_budget_missing_baseline_is_unavailable(self) -> None:
        self.write("docs/a.md", "a\n")

        result = self.result(
            self.write_line_budget_suite(
                paths='["docs/a.md"]',
                baseline_path="missing.tsv",
            )
        )

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_line_budget_path_escape_is_invalid(self) -> None:
        self.prepare_budget()

        result = self.result(
            self.write_line_budget_suite(paths='["../outside.md"]')
        )

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_line_budget_baseline_escape_is_invalid(self) -> None:
        self.write("docs/a.md", "a\n")

        result = self.result(
            self.write_line_budget_suite(
                paths='["docs/a.md"]',
                baseline_path="../outside.tsv",
            )
        )

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_line_budget_paths_must_be_non_empty_and_unique(self) -> None:
        for paths in ("[]", '["docs/a.md", "docs/a.md"]'):
            with self.subTest(paths=paths):
                suite_path = self.write_line_budget_suite(paths=paths)
                self.write_registry(suite_path)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, self.registry)
                self.assertEqual(raised.exception.diagnostic.code, "CONFIG.STRING_LIST")

    def test_line_budget_ratio_must_use_positive_integers(self) -> None:
        for numerator, denominator in (("0", "4"), ("1", "0"), ("true", "4")):
            with self.subTest(numerator=numerator, denominator=denominator):
                suite_path = self.write_line_budget_suite(
                    numerator=numerator,
                    denominator=denominator,
                )
                self.write_registry(suite_path)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, self.registry)
                self.assertEqual(
                    raised.exception.diagnostic.code,
                    "CONFIG.POSITIVE_INTEGER",
                )

    def test_line_budget_unknown_field_is_invalid(self) -> None:
        suite_path = self.write_line_budget_suite(extra='measure = "words"')
        self.write_registry(suite_path)

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")
        self.assertEqual(raised.exception.diagnostic.field, "measure")


if __name__ == "__main__":
    unittest.main()
