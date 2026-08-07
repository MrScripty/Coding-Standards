from __future__ import annotations

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
from standards_verifier.diagnostics import EngineError
from standards_verifier.engine import Verifier
from standards_verifier.paths import contained_file


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

    def write_text_suite(self, suite_id: str, path: str = "evidence.md") -> str:
        suite_path = f"suites/{suite_id}.toml"
        self.write(
            suite_path,
            f"""
            schema_version = 1
            id = {json.dumps(suite_id)}
            owner = "test.owner"
            description = "Test suite"

            [[checks]]
            id = "text"
            type = "text"
            path = {json.dumps(path)}
            required = ["required"]
            prohibited = ["forbidden"]
            """,
        )
        return suite_path

    def write_decision_suite(self, expected: str = "typed-invalid") -> str:
        self.write(
            "decisions.tsv",
            f"""
            case\tstate\tcapability\tfallback\texpected
            accepted\taccepted\tsupported\tnone\tallow
            invalid\taccepted\tsupported\tlegacy\t{expected}
            unavailable\tmissing\tsupported\tnone\ttyped-unavailable
            unsupported\taccepted\tunsupported\tnone\ttyped-unsupported
            """,
        )
        self.write(
            "suites/decision.toml",
            """
            schema_version = 1
            id = "decision"
            owner = "test.owner"
            description = "Decision suite"

            [[checks]]
            id = "outcomes"
            type = "decision"
            path = "decisions.tsv"
            expected_column = "expected"
            default = "allow"

            [checks.domains]
            case = ["*"]
            state = ["accepted", "missing"]
            capability = ["supported", "unsupported"]
            fallback = ["none", "legacy"]
            expected = ["allow", "typed-invalid", "typed-unavailable", "typed-unsupported"]

            [[checks.rules]]
            outcome = "typed-invalid"
            [checks.rules.when]
            any = [{ field = "fallback", op = "ne", value = "none" }]

            [[checks.rules]]
            outcome = "typed-unsupported"
            [checks.rules.when]
            all = [
              { field = "capability", op = "in", values = ["unsupported"] },
              { field = "state", op = "eq", value = "accepted" },
            ]

            [[checks.rules]]
            outcome = "typed-unavailable"
            [checks.rules.when]
            any = [
              { field = "state", op = "eq", value = "missing" },
              { not = { field = "capability", op = "in", values = ["supported", "unsupported"] } },
            ]
            """,
        )
        return "suites/decision.toml"

    def test_text_and_decision_suites_pass(self) -> None:
        self.write("evidence.md", "required\n")
        text_suite = self.write_text_suite("text")
        decision_suite = self.write_decision_suite()
        self.write_registry(
            [("text", text_suite, []), ("decision", decision_suite, ["text"])]
        )

        results = Verifier(self.root, self.registry).run(("decision",))

        self.assertEqual([result.id for result in results], ["text", "decision"])
        self.assertTrue(all(result.status == "passed" for result in results))

    def test_dependency_diamond_executes_each_suite_once(self) -> None:
        self.write("evidence.md", "required\n")
        entries = []
        for suite_id, requires in (
            ("base", []),
            ("left", ["base"]),
            ("right", ["base"]),
            ("top", ["left", "right"]),
        ):
            entries.append((suite_id, self.write_text_suite(suite_id), requires))
        self.write_registry(entries)

        results = Verifier(self.root, self.registry).run(("top",))

        self.assertEqual([result.id for result in results], ["base", "left", "right", "top"])
        self.assertEqual(len({result.id for result in results}), 4)

    def test_dependency_order_does_not_depend_on_registry_order(self) -> None:
        self.write("evidence.md", "required\n")
        dependent = self.write_text_suite("dependent")
        dependency = self.write_text_suite("dependency")
        self.write_registry(
            [
                ("dependent", dependent, ["dependency"]),
                ("dependency", dependency, []),
            ]
        )

        results = Verifier(self.root, self.registry).run(("dependent",))

        self.assertEqual([result.id for result in results], ["dependency", "dependent"])

    def test_decision_mismatch_has_stable_diagnostic(self) -> None:
        suite_path = self.write_decision_suite(expected="allow")
        self.write_registry([("decision", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.diagnostics[0].code, "ASSERT.DECISION_OUTCOME")
        self.assertEqual(result.diagnostics[0].row, 3)

    def test_unknown_suite_field_is_invalid(self) -> None:
        self.write("evidence.md", "required\n")
        suite_path = self.write_text_suite("text")
        with (self.root / suite_path).open("a", encoding="utf-8") as handle:
            handle.write("unknown = true\n")
        self.write_registry([("text", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")

    def test_malformed_toml_is_invalid(self) -> None:
        self.write(self.registry, "schema_version = [\n")

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.INVALID_TOML")

    def test_dependency_cycle_is_invalid(self) -> None:
        self.write("evidence.md", "required\n")
        first = self.write_text_suite("first")
        second = self.write_text_suite("second")
        self.write_registry([("first", first, ["second"]), ("second", second, ["first"])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.DEPENDENCY_CYCLE")

    def test_missing_evidence_is_unavailable(self) -> None:
        suite_path = self.write_text_suite("text", path="missing.md")
        self.write_registry([("text", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")
        self.assertEqual(result.diagnostics[0].outcome, "unavailable")

    def test_parent_path_and_symlink_escape_are_invalid(self) -> None:
        self.write("inside.md", "required\n")
        with self.assertRaises(EngineError) as parent_error:
            contained_file(self.root, "../outside.md")
        self.assertEqual(parent_error.exception.diagnostic.code, "PATH.OUTSIDE_REPOSITORY")

        outside = Path(self.temp_dir.name).parent / "standards-verifier-outside.md"
        outside.write_text("required\n", encoding="utf-8")
        try:
            (self.root / "link.md").symlink_to(outside)
            with self.assertRaises(EngineError) as symlink_error:
                contained_file(self.root, "link.md")
            self.assertEqual(symlink_error.exception.diagnostic.code, "PATH.OUTSIDE_REPOSITORY")
        finally:
            outside.unlink(missing_ok=True)

    def test_cli_json_preserves_typed_diagnostics(self) -> None:
        suite_path = self.write_text_suite("text", path="missing.md")
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
        self.assertEqual(payload["results"][0]["diagnostics"][0]["outcome"], "unavailable")


if __name__ == "__main__":
    unittest.main()
