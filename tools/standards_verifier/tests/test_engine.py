from __future__ import annotations

# ruff: noqa: E402 - standalone package imports follow the local source path.

import contextlib
import io
import json
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.cli import main
from standards_verifier.diagnostics import Diagnostic, EngineError
from standards_verifier.engine import Verifier
from standards_verifier.paths import contained_file, contained_path, repository_path


class EngineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.registry = "registry.toml"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_registry(self, entries: list[tuple[str, str, list[str]]]) -> None:
        body = ["schema_version = 1", ""]
        for suite_id, path, requires in entries:
            dependencies = ", ".join(json.dumps(value) for value in requires)
            body.extend(
                [
                    "[[suites]]",
                    f"id = {json.dumps(suite_id)}",
                    f"path = {json.dumps(path)}",
                    f"requires = [{dependencies}]",
                    "",
                ]
            )
        self.write(self.registry, "\n".join(body))

    def write_navigation_suite(self, suite_id: str, path: str = "evidence.md") -> str:
        self.write("target.md", "# Target\n")
        suite_path = f"suites/{suite_id}.toml"
        self.write(
            suite_path,
            f"""
            schema_version = 1
            id = {json.dumps(suite_id)}
            owner = "test.owner"
            description = "Test suite"

            [[checks]]
            id = "navigation"
            type = "markdown_targets"
            path = {json.dumps(path)}
            required = ["target.md"]
            """,
        )
        return suite_path

    def test_dependency_diamond_executes_each_suite_once(self) -> None:
        self.write("evidence.md", "[Target](target.md)\n")
        entries = []
        for suite_id, requires in (
            ("base", []),
            ("left", ["base"]),
            ("right", ["base"]),
            ("top", ["left", "right"]),
        ):
            entries.append((suite_id, self.write_navigation_suite(suite_id), requires))
        self.write_registry(entries)

        results = Verifier(self.root, self.registry).run(("top",))

        self.assertEqual(
            [result.id for result in results], ["base", "left", "right", "top"]
        )
        self.assertEqual(len({result.id for result in results}), 4)

    def test_dependency_order_does_not_depend_on_registry_order(self) -> None:
        self.write("evidence.md", "[Target](target.md)\n")
        dependent = self.write_navigation_suite("dependent")
        dependency = self.write_navigation_suite("dependency")
        self.write_registry(
            [
                ("dependent", dependent, ["dependency"]),
                ("dependency", dependency, []),
            ]
        )

        results = Verifier(self.root, self.registry).run(("dependent",))

        self.assertEqual([result.id for result in results], ["dependency", "dependent"])

    def test_dependency_graph_resolves_registered_suite_ids_and_paths(self) -> None:
        self.write("evidence.md", "[Target](target.md)\n")
        suite_path = self.write_navigation_suite("text")
        self.write_registry([("text", suite_path, [])])

        verifier = Verifier(self.root, self.registry)

        self.assertEqual(verifier.dependency_graph.resolve("text"), "text")
        self.assertEqual(verifier.dependency_graph.resolve(suite_path), "text")

    def test_engine_errors_derive_exit_status_from_the_typed_outcome(self) -> None:
        for outcome, expected_exit in (
            ("invalid", 2),
            ("unavailable", 3),
            ("unsupported", 4),
        ):
            with self.subTest(outcome=outcome):
                error = EngineError(Diagnostic("TEST.OUTCOME", outcome, "test"))
                self.assertEqual(error.exit_code, expected_exit)

    def test_unknown_check_field_is_invalid(self) -> None:
        self.write("evidence.md", "[Target](target.md)\n")
        suite_path = self.write_navigation_suite("text")
        with (self.root / suite_path).open("a", encoding="utf-8") as handle:
            handle.write("unknown = true\n")
        self.write_registry([("text", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry).run()

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.MARKDOWN_TARGETS")

    def test_cli_list_does_not_parse_suite_bodies(self) -> None:
        self.write("suites/broken.toml", "not = [valid\n")
        self.write_registry([("broken", "suites/broken.toml", [])])
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            status = main(
                [
                    "--repo-root",
                    str(self.root),
                    "--registry",
                    self.registry,
                    "--list",
                ],
                default_repo_root=self.root,
            )

        self.assertEqual(status, 0)
        self.assertEqual(output.getvalue(), "broken\n")

    def test_complete_runs_the_full_python_suite_catalog(self) -> None:
        self.write("evidence.md", "[Target](target.md)\n")
        first = self.write_navigation_suite("first")
        second = self.write_navigation_suite("second")
        self.write_registry([("first", first, []), ("second", second, [])])
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            status = main(
                [
                    "--repo-root",
                    str(self.root),
                    "--registry",
                    self.registry,
                    "--complete",
                ],
                default_repo_root=self.root,
            )

        self.assertEqual(status, 0)
        self.assertIn("PASS first", output.getvalue())
        self.assertIn("PASS second", output.getvalue())
        self.assertIn(
            "SUMMARY selected=2 passed=2 failed=0 blocked=0", output.getvalue()
        )

    def test_complete_supports_structured_json_output(self) -> None:
        self.write("evidence.md", "[Target](target.md)\n")
        suite_path = self.write_navigation_suite("text")
        self.write_registry([("text", suite_path, [])])
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            status = main(
                [
                    "--repo-root",
                    str(self.root),
                    "--registry",
                    self.registry,
                    "--complete",
                    "--format",
                    "json",
                ],
                default_repo_root=self.root,
            )

        payload = json.loads(output.getvalue())
        self.assertEqual(status, 0)
        self.assertEqual(
            payload["summary"],
            {
                "selected": 1,
                "passed": 1,
                "failed": 0,
                "blocked": 0,
            },
        )
        self.assertEqual(payload["results"][0]["id"], "text")

    def test_focused_selection_ignores_unrelated_malformed_suite(self) -> None:
        self.write("evidence.md", "[Target](target.md)\n")
        selected = self.write_navigation_suite("selected")
        self.write("suites/broken.toml", "not = [valid\n")
        self.write_registry(
            [
                ("selected", selected, []),
                ("broken", "suites/broken.toml", []),
            ]
        )

        results = Verifier(self.root, self.registry).run(("selected",))

        self.assertEqual([result.id for result in results], ["selected"])
        self.assertEqual(results[0].status, "passed")

    def test_focused_selection_validates_malformed_dependency(self) -> None:
        self.write("evidence.md", "[Target](target.md)\n")
        selected = self.write_navigation_suite("selected")
        self.write("suites/broken.toml", "not = [valid\n")
        self.write_registry(
            [
                ("selected", selected, ["broken"]),
                ("broken", "suites/broken.toml", []),
            ]
        )

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry).run(("selected",))

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.INVALID_TOML")
        self.assertEqual(raised.exception.diagnostic.path, "suites/broken.toml")

    def test_all_validates_unrelated_malformed_suite(self) -> None:
        self.write("evidence.md", "[Target](target.md)\n")
        selected = self.write_navigation_suite("selected")
        self.write("suites/broken.toml", "not = [valid\n")
        self.write_registry(
            [
                ("selected", selected, []),
                ("broken", "suites/broken.toml", []),
            ]
        )

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry).run()

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.INVALID_TOML")
        self.assertEqual(raised.exception.diagnostic.path, "suites/broken.toml")

    def test_malformed_toml_is_invalid(self) -> None:
        self.write(self.registry, "schema_version = [\n")

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry).run()

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.INVALID_TOML")

    def test_dependency_cycle_is_invalid(self) -> None:
        self.write("evidence.md", "[Target](target.md)\n")
        first = self.write_navigation_suite("first")
        second = self.write_navigation_suite("second")
        self.write_registry(
            [("first", first, ["second"]), ("second", second, ["first"])]
        )

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry).run()

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.DEPENDENCY_CYCLE")

    def test_missing_evidence_is_unavailable(self) -> None:
        suite_path = self.write_navigation_suite("text", path="missing.md")
        self.write_registry([("text", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")
        self.assertEqual(result.diagnostics[0].outcome, "unavailable")

    def test_parent_path_and_symlink_escape_are_invalid(self) -> None:
        self.write("inside.md", "[Target](target.md)\n")
        with self.assertRaises(EngineError) as parent_error:
            contained_file(self.root, "../outside.md")
        self.assertEqual(
            parent_error.exception.diagnostic.code, "PATH.OUTSIDE_REPOSITORY"
        )

        outside = Path(self.temp_dir.name).parent / "standards-verifier-outside.md"
        outside.write_text("[Target](target.md)\n", encoding="utf-8")
        try:
            (self.root / "link.md").symlink_to(outside)
            with self.assertRaises(EngineError) as symlink_error:
                contained_file(self.root, "link.md")
            self.assertEqual(
                symlink_error.exception.diagnostic.code, "PATH.OUTSIDE_REPOSITORY"
            )
        finally:
            outside.unlink(missing_ok=True)

    def test_contained_path_accepts_missing_directory_and_valid_symlink(
        self,
    ) -> None:
        (self.root / "directory").mkdir()
        (self.root / "link").symlink_to("directory", target_is_directory=True)

        self.assertEqual(
            contained_path(self.root, "missing.md"),
            self.root / "missing.md",
        )
        self.assertEqual(
            contained_path(self.root, "directory"),
            self.root / "directory",
        )
        self.assertEqual(
            contained_path(self.root, "link"),
            self.root / "link",
        )

    def test_repository_path_preserves_contained_path_lexical_contract(self) -> None:
        self.assertEqual(repository_path("missing.md").as_posix(), "missing.md")
        self.assertEqual(
            repository_path("directory/item.md").as_posix(), "directory/item.md"
        )
        for path in ("", "/absolute.md", "../outside.md"):
            with self.subTest(path=path):
                with self.assertRaises(EngineError) as raised:
                    repository_path(path)
                self.assertEqual(
                    raised.exception.diagnostic.code,
                    "PATH.OUTSIDE_REPOSITORY",
                )

    def test_contained_path_rejects_parent_and_symlink_escape(self) -> None:
        with self.assertRaises(EngineError) as parent_error:
            contained_path(self.root, "../outside.md")
        self.assertEqual(
            parent_error.exception.diagnostic.code,
            "PATH.OUTSIDE_REPOSITORY",
        )

        outside = Path(self.temp_dir.name).parent / "standards-path-outside"
        outside.mkdir(exist_ok=True)
        try:
            (self.root / "escape").symlink_to(
                outside,
                target_is_directory=True,
            )
            with self.assertRaises(EngineError) as symlink_error:
                contained_path(self.root, "escape/missing.md")
            self.assertEqual(
                symlink_error.exception.diagnostic.code,
                "PATH.OUTSIDE_REPOSITORY",
            )
        finally:
            outside.rmdir()

    def test_cli_json_preserves_typed_diagnostics(self) -> None:
        suite_path = self.write_navigation_suite("text", path="missing.md")
        self.write_registry([("text", suite_path, [])])
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            status = main(
                [
                    "--repo-root",
                    str(self.root),
                    "--registry",
                    self.registry,
                    "--all",
                    "--format",
                    "json",
                ],
                default_repo_root=self.root,
            )

        payload = json.loads(output.getvalue())
        self.assertEqual(status, 3)
        self.assertEqual(
            payload["results"][0]["diagnostics"][0]["outcome"], "unavailable"
        )

    def test_cli_formats_preserve_assertion_exit_classification(self) -> None:
        self.write("evidence.md", "The navigation link is missing.\n")
        suite_path = self.write_navigation_suite("navigation")
        self.write_registry([("navigation", suite_path, [])])

        for output_format in ("text", "json"):
            with self.subTest(output_format=output_format):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    status = main(
                        [
                            "--repo-root",
                            str(self.root),
                            "--registry",
                            self.registry,
                            "--all",
                            "--format",
                            output_format,
                        ],
                        default_repo_root=self.root,
                    )

                self.assertEqual(status, 1)
                self.assertIn("ASSERT.MARKDOWN_TARGET_MISSING", output.getvalue())


if __name__ == "__main__":
    unittest.main()
