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

    def write_multi_decision_suite(
        self,
        *,
        expected_checksum: str = "no",
        extra: str = "",
        output_count: int = 3,
        duplicate_output: bool = False,
        lockfile_predicate_field: str = "ships_artifact",
        lockfile_default: str = "typed-unavailable",
        sbom_rule_outcome: str = "yes",
    ) -> str:
        self.write(
            "artifact-decisions.tsv",
            f"""
            case\tships_artifact\tbundles_dependencies\texternal_sbom_requirement\tchecksum_consumed\tresolved_closure_source\tconsumer_resolves\texpected_sbom\texpected_checksum\texpected_lockfile
            full\tyes\tyes\tno\tyes\tyes\tno\tyes\tyes\tyes
            consumer\tyes\tno\tno\tno\tno\tyes\tno\t{expected_checksum}\tno
            unresolved\tyes\tno\tno\tno\tno\tno\tno\tno\ttyped-unavailable
            internal\tno\tyes\tno\tno\tyes\tno\tno\tno\tno
            """,
        )
        checksum_column = "expected_sbom" if duplicate_output else "expected_checksum"
        output_blocks = [
            f"""
            [[checks.outputs]]
            column = "expected_sbom"
            default = "no"
            [[checks.outputs.rules]]
            outcome = {json.dumps(sbom_rule_outcome)}
            [checks.outputs.rules.when]
            all = [
              {{ field = "ships_artifact", op = "eq", value = "yes" }},
              {{ any = [
                {{ field = "bundles_dependencies", op = "eq", value = "yes" }},
                {{ field = "external_sbom_requirement", op = "eq", value = "yes" }},
              ] }},
            ]
            """,
            f"""
            [[checks.outputs]]
            column = {json.dumps(checksum_column)}
            default = "no"
            [[checks.outputs.rules]]
            outcome = "yes"
            [checks.outputs.rules.when]
            all = [
              {{ field = "ships_artifact", op = "eq", value = "yes" }},
              {{ field = "checksum_consumed", op = "eq", value = "yes" }},
            ]
            """,
            f"""
            [[checks.outputs]]
            column = "expected_lockfile"
            default = {json.dumps(lockfile_default)}
            [[checks.outputs.rules]]
            outcome = "yes"
            [checks.outputs.rules.when]
            all = [
              {{ field = {json.dumps(lockfile_predicate_field)}, op = "eq", value = "yes" }},
              {{ field = "resolved_closure_source", op = "eq", value = "yes" }},
            ]
            [[checks.outputs.rules]]
            outcome = "no"
            [checks.outputs.rules.when]
            any = [
              {{ field = "ships_artifact", op = "eq", value = "no" }},
              {{ field = "consumer_resolves", op = "eq", value = "yes" }},
            ]
            """,
        ]
        self.write(
            "suites/multi-decision.toml",
            f"""
            schema_version = 1
            id = "multi-decision"
            owner = "test.owner"
            description = "Multi-output decision suite"

            [[checks]]
            id = "artifact-outcomes"
            type = "decision"
            path = "artifact-decisions.tsv"
            {extra}
            input_columns = [
              "ships_artifact",
              "bundles_dependencies",
              "external_sbom_requirement",
              "checksum_consumed",
              "resolved_closure_source",
              "consumer_resolves",
            ]
            [checks.domains]
            case = ["*"]
            ships_artifact = ["yes", "no"]
            bundles_dependencies = ["yes", "no"]
            external_sbom_requirement = ["yes", "no"]
            checksum_consumed = ["yes", "no"]
            resolved_closure_source = ["yes", "no"]
            consumer_resolves = ["yes", "no"]
            expected_sbom = ["yes", "no"]
            expected_checksum = ["yes", "no"]
            expected_lockfile = ["yes", "no", "typed-unavailable"]
            {''.join(output_blocks[:output_count])}
            """,
        )
        return "suites/multi-decision.toml"

    def write_exact_text_suite(
        self,
        *,
        path: str = "exact.md",
        expected: str = "first\nsecond\n",
        extra: str = "",
    ) -> str:
        self.write(
            "suites/exact-text.toml",
            f'''
            schema_version = 1
            id = "exact-text"
            owner = "test.owner"
            description = "Exact text suite"

            [[checks]]
            id = "exact"
            type = "exact_text"
            path = {json.dumps(path)}
            expected = {json.dumps(expected)}
            {extra}
            ''',
        )
        return "suites/exact-text.toml"

    def write_table_suite(
        self,
        *,
        path: str = "rows.tsv",
        expected_state: str = "done",
        predicate_field: str = "state",
    ) -> str:
        self.write(
            "suites/table.toml",
            f"""
            schema_version = 1
            id = "table"
            owner = "test.owner"
            description = "Table suite"

            [[checks]]
            id = "structure"
            type = "table"
            path = {json.dumps(path)}
            header = ["id", "state", "tags"]
            non_empty = ["id", "state", "tags"]
            unique = [["id"]]
            [checks.domains]
            state = ["ready", "done"]

            [[checks.projections]]
            columns = ["id", "state"]
            order = "source"
            expected = [["a", "ready"], ["b", {json.dumps(expected_state)}]]

            [[checks.projections]]
            columns = ["tags"]
            order = "lexical"
            expected = [["alpha"], ["beta"], ["gamma"]]
            where = {{ field = {json.dumps(predicate_field)}, op = "in", values = ["ready", "done"] }}
            split = {{ field = "tags", delimiter = "," }}
            """,
        )
        return "suites/table.toml"

    def test_table_row_count_is_an_unknown_field(self) -> None:
        suite_path = self.write_table_suite()
        self.write_registry([("table", suite_path, [])])
        suite = self.root / suite_path
        suite.write_text(
            suite.read_text(encoding="utf-8").replace(
                'header = ["id", "state", "tags"]',
                'header = ["id", "state", "tags"]\nrow_count = 2',
            ),
            encoding="utf-8",
        )
        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)
        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")
        self.assertEqual(raised.exception.diagnostic.field, "row_count")

    def write_acceptance_claims_suite(
        self,
        *,
        path: str = "claims.tsv",
        expected: str = "satisfied",
        extra: str = "",
    ) -> str:
        self.write(
            "suites/claims.toml",
            f"""
            schema_version = 1
            id = "claims"
            owner = "test.owner"
            description = "Acceptance claims suite"

            [[checks]]
            id = "claims"
            type = "acceptance_claims"
            path = {json.dumps(path)}
            kinds = ["focused", "system"]
            environments = ["not-applicable", "representative"]
            modes = ["automated", "manual", "either"]
            {extra}
            """,
        )
        if path == "claims.tsv":
            self.write(
                path,
                "case\trequired_claims\tobserved_claims\texpected\n"
                "exact\tfocused@not-applicable@automated\t"
                f"focused@not-applicable@automated\t{expected}\n"
                "either\tsystem@representative@either\t"
                "system@representative@manual\tsatisfied\n",
            )
        return "suites/claims.toml"

    def write_relation_suite(
        self,
        *,
        right_path: str = "right.tsv",
        right_column: str = "values",
        extra: str = "",
    ) -> str:
        self.write(
            "left.tsv",
            "group\titems\nselected\tb,a\nignored\tz\n",
        )
        if right_path == "right.tsv":
            self.write(right_path, "scope\tvalues\nselected\ta\nselected\tb\n")
        self.write(
            "suites/relation.toml",
            f"""
            schema_version = 1
            id = "relation"
            owner = "test.owner"
            description = "Relation suite"

            [[checks]]
            id = "relation"
            type = "relation"
            mode = "set"
            {extra}

            [checks.left]
            path = "left.tsv"
            header = ["group", "items"]
            columns = ["items"]
            order = "source"
            where = {{ field = "group", op = "eq", value = "selected" }}
            split = {{ field = "items", delimiter = "," }}

            [checks.right]
            path = {json.dumps(right_path)}
            header = ["scope", "values"]
            columns = [{json.dumps(right_column)}]
            order = "source"
            where = {{ field = "scope", op = "eq", value = "selected" }}
            """,
        )
        return "suites/relation.toml"

    def write_inclusion_suite(
        self,
        *,
        container_path: str = "container.tsv",
        container_columns: str = 'columns = ["value"]',
        extra: str = "",
    ) -> str:
        self.write(
            "members.tsv",
            "group\titems\nselected\tb,a\nignored\tz\n",
        )
        if container_path == "container.tsv":
            self.write(
                container_path,
                "scope\tvalue\nselected\ta\nselected\tb\nselected\tc\nignored\tz\n",
            )
        self.write(
            "suites/inclusion.toml",
            f"""
            schema_version = 1
            id = "inclusion"
            owner = "test.owner"
            description = "Inclusion suite"

            [[checks]]
            id = "inclusion"
            type = "inclusion"
            {extra}

            [checks.members]
            path = "members.tsv"
            header = ["group", "items"]
            columns = ["items"]
            order = "source"
            where = {{ field = "group", op = "eq", value = "selected" }}
            split = {{ field = "items", delimiter = "," }}

            [checks.container]
            path = {json.dumps(container_path)}
            header = ["scope", "value"]
            {container_columns}
            order = "lexical"
            where = {{ field = "scope", op = "eq", value = "selected" }}
            """,
        )
        return "suites/inclusion.toml"

    def write_keyed_relation_suite(
        self,
        *,
        key_columns: str = '["items"]',
        expected_path: str = "expected.tsv",
        expected_values: str = '["owner", "disposition"]',
        observed_path: str = "observed.tsv",
        observed_values: str = '["target", "disposition"]',
        expected_extra: str = "",
        observed_extra: str = "",
        extra: str = "",
    ) -> str:
        self.write("keys.tsv", "row\titems\nselected\tb,a\nignored\tz\n")
        if expected_path == "expected.tsv":
            self.write(
                expected_path,
                "id\towner\tdisposition\na\towner-a\tmove\n"
                "b\towner-b\trefine\nx\tignored\tindex\n",
            )
        if observed_path == "observed.tsv":
            self.write(
                observed_path,
                "id\tsource\ttarget\tdisposition\n"
                "x\tlegacy\tignored\tindex\n"
                "b\tlegacy\towner-b\trefine\n"
                "a\tlegacy\towner-a\tmove\n",
            )
        self.write(
            "suites/keyed-relation.toml",
            f"""
            schema_version = 1
            id = "keyed-relation"
            owner = "test.owner"
            description = "Keyed relation suite"

            [[checks]]
            id = "keyed"
            type = "keyed_relation"
            {extra}

            [checks.keys]
            path = "keys.tsv"
            header = ["row", "items"]
            columns = {key_columns}
            order = "source"
            where = {{ field = "row", op = "eq", value = "selected" }}
            split = {{ field = "items", delimiter = "," }}

            [checks.expected]
            path = {json.dumps(expected_path)}
            header = ["id", "owner", "disposition"]
            key = "id"
            values = {expected_values}
            {expected_extra}

            [checks.observed]
            path = {json.dumps(observed_path)}
            header = ["id", "source", "target", "disposition"]
            key = "id"
            values = {observed_values}
            {observed_extra}
            """,
        )
        return "suites/keyed-relation.toml"

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

    def test_multi_output_decision_passes_with_typed_unavailable(self) -> None:
        suite_path = self.write_multi_decision_suite()
        self.write_registry([("multi-decision", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "passed")

    def test_multi_output_mismatch_identifies_output_column(self) -> None:
        suite_path = self.write_multi_decision_suite(expected_checksum="yes")
        self.write_registry([("multi-decision", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "ASSERT.DECISION_OUTCOME")
        self.assertEqual(result.diagnostics[0].field, "expected_checksum")

    def test_multi_output_rejects_mixed_single_output_fields(self) -> None:
        suite_path = self.write_multi_decision_suite(
            extra='expected_column = "expected_lockfile"'
        )
        self.write_registry([("multi-decision", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.DECISION_MODE")

    def test_multi_output_requires_at_least_two_outputs(self) -> None:
        suite_path = self.write_multi_decision_suite(output_count=1)
        self.write_registry([("multi-decision", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.DECISION_OUTPUTS")

    def test_multi_output_rejects_duplicate_output_columns(self) -> None:
        suite_path = self.write_multi_decision_suite(duplicate_output=True)
        self.write_registry([("multi-decision", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.DECISION_OUTPUT")

    def test_multi_output_domains_must_cover_exact_columns(self) -> None:
        suite_path = self.write_multi_decision_suite()
        suite = self.root / suite_path
        suite.write_text(
            suite.read_text(encoding="utf-8").replace(
                'expected_checksum = ["yes", "no"]\n', "", 1
            ),
            encoding="utf-8",
        )
        self.write_registry([("multi-decision", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.DECISION_COLUMNS")

    def test_multi_output_rejects_non_input_predicate(self) -> None:
        suite_path = self.write_multi_decision_suite(
            lockfile_predicate_field="expected_sbom"
        )
        self.write_registry([("multi-decision", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "DECISION.NON_INPUT_FIELD")
        self.assertEqual(raised.exception.diagnostic.field, "expected_sbom")

    def test_multi_output_requires_exact_header_order(self) -> None:
        suite_path = self.write_multi_decision_suite()
        fixture = self.root / "artifact-decisions.tsv"
        fixture.write_text(
            fixture.read_text(encoding="utf-8").replace(
                "expected_sbom\texpected_checksum",
                "expected_checksum\texpected_sbom",
                1,
            ),
            encoding="utf-8",
        )
        self.write_registry([("multi-decision", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "TABLE.HEADER_CONTRACT")

    def test_multi_output_default_must_belong_to_output_domain(self) -> None:
        suite_path = self.write_multi_decision_suite(lockfile_default="missing")
        self.write_registry([("multi-decision", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "DECISION.DEFAULT_OUTCOME")
        self.assertEqual(result.diagnostics[0].field, "expected_lockfile")

    def test_multi_output_rule_must_belong_to_output_domain(self) -> None:
        suite_path = self.write_multi_decision_suite(
            sbom_rule_outcome="typed-unavailable"
        )
        self.write_registry([("multi-decision", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "DECISION.RULE_OUTCOME")
        self.assertEqual(result.diagnostics[0].field, "expected_sbom")

    def test_exact_text_passes_for_identical_utf8_bytes(self) -> None:
        self.write("exact.md", "first\nsecond\n")
        suite_path = self.write_exact_text_suite()
        self.write_registry([("exact-text", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "passed")

    def test_exact_text_reports_first_raw_byte_mismatch(self) -> None:
        self.write("exact.md", "first\nsecond\nextra\n")
        suite_path = self.write_exact_text_suite()
        self.write_registry([("exact-text", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.diagnostics[0].code, "ASSERT.EXACT_TEXT")
        self.assertEqual(result.diagnostics[0].expected, "13 bytes")
        self.assertEqual(
            result.diagnostics[0].observed,
            "19 bytes; first mismatch at byte 13",
        )

    def test_exact_text_missing_input_is_unavailable(self) -> None:
        suite_path = self.write_exact_text_suite(path="missing.md")
        self.write_registry([("exact-text", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_exact_text_path_escape_is_invalid(self) -> None:
        suite_path = self.write_exact_text_suite(path="../outside.md")
        self.write_registry([("exact-text", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_exact_text_unknown_field_is_invalid(self) -> None:
        self.write("exact.md", "first\nsecond\n")
        suite_path = self.write_exact_text_suite(extra="normalize = true")
        self.write_registry([("exact-text", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")
        self.assertEqual(raised.exception.diagnostic.field, "normalize")

    def test_table_structure_and_projections_pass(self) -> None:
        self.write("rows.tsv", "id\tstate\ttags\na\tready\tbeta,alpha\nb\tdone\tgamma\n")
        suite_path = self.write_table_suite()
        self.write_registry([("table", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "passed")

    def test_table_projection_mismatch_has_stable_diagnostic(self) -> None:
        self.write("rows.tsv", "id\tstate\ttags\na\tready\tbeta,alpha\nb\tdone\tgamma\n")
        suite_path = self.write_table_suite(expected_state="ready")
        self.write_registry([("table", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "ASSERT.TABLE_PROJECTION")

    def test_malformed_table_row_is_invalid(self) -> None:
        self.write("rows.tsv", "id\tstate\ttags\na\tready\n")
        suite_path = self.write_table_suite()
        self.write_registry([("table", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "TABLE.ROW_WIDTH")
        self.assertEqual(result.diagnostics[0].row, 2)

    def test_table_unknown_predicate_field_is_invalid(self) -> None:
        self.write("rows.tsv", "id\tstate\ttags\na\tready\tbeta,alpha\nb\tdone\tgamma\n")
        suite_path = self.write_table_suite(predicate_field="missing")
        self.write_registry([("table", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.TABLE_COLUMN")

    def test_missing_table_is_unavailable(self) -> None:
        suite_path = self.write_table_suite(path="missing.tsv")
        self.write_registry([("table", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_table_path_escape_is_invalid(self) -> None:
        suite_path = self.write_table_suite(path="../outside.tsv")
        self.write_registry([("table", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_acceptance_claim_sets_pass(self) -> None:
        suite_path = self.write_acceptance_claims_suite()
        self.write_registry([("claims", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "passed")

    def test_acceptance_claim_mismatch_has_stable_diagnostic(self) -> None:
        suite_path = self.write_acceptance_claims_suite(expected="unsatisfied")
        self.write_registry([("claims", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "ASSERT.ACCEPTANCE_CLAIMS")

    def test_malformed_acceptance_claim_is_invalid(self) -> None:
        suite_path = self.write_acceptance_claims_suite()
        self.write(
            "claims.tsv",
            "case\trequired_claims\tobserved_claims\texpected\n"
            "bad\tfocused@not-applicable\tfocused@not-applicable@automated\t"
            "unsatisfied\n",
        )
        self.write_registry([("claims", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "CLAIM.INVALID")

    def test_unknown_acceptance_claim_field_is_invalid(self) -> None:
        suite_path = self.write_acceptance_claims_suite(extra="unknown = true")
        self.write_registry([("claims", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")

    def test_missing_acceptance_claim_table_is_unavailable(self) -> None:
        suite_path = self.write_acceptance_claims_suite(path="missing.tsv")
        self.write_registry([("claims", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_acceptance_claim_path_escape_is_invalid(self) -> None:
        suite_path = self.write_acceptance_claims_suite(path="../claims.tsv")
        self.write_registry([("claims", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_table_relation_with_split_passes(self) -> None:
        suite_path = self.write_relation_suite()
        self.write_registry([("relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "passed")

    def test_table_relation_mismatch_has_stable_diagnostic(self) -> None:
        suite_path = self.write_relation_suite()
        self.write("right.tsv", "scope\tvalues\nselected\ta\nselected\tc\n")
        self.write_registry([("relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "ASSERT.TABLE_RELATION")

    def test_malformed_relation_row_is_invalid(self) -> None:
        suite_path = self.write_relation_suite()
        self.write("right.tsv", "scope\tvalues\nselected\n")
        self.write_registry([("relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "TABLE.ROW_WIDTH")

    def test_unknown_relation_field_is_invalid(self) -> None:
        suite_path = self.write_relation_suite(extra="unknown = true")
        self.write_registry([("relation", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")

    def test_relation_side_parser_retains_stable_diagnostic(self) -> None:
        self.write(
            "right.tsv",
            "scope\tvalues\nselected\ta\n",
        )
        self.write(
            "suites/relation.toml",
            """
            schema_version = 1
            id = "relation"
            owner = "test.owner"
            description = "Relation suite"

            [[checks]]
            id = "relation"
            type = "relation"
            mode = "set"
            left = true

            [checks.right]
            path = "right.tsv"
            header = ["scope", "values"]
            columns = ["values"]
            order = "source"
            """,
        )
        self.write_registry([("relation", "suites/relation.toml", [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        diagnostic = raised.exception.diagnostic
        self.assertEqual(diagnostic.code, "CONFIG.RELATION_SIDE")
        self.assertEqual(diagnostic.message, "relation side must be a TOML table")
        self.assertEqual(diagnostic.field, "left")

    def test_missing_relation_input_is_unavailable(self) -> None:
        suite_path = self.write_relation_suite(right_path="missing.tsv")
        self.write_registry([("relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_relation_path_escape_is_invalid(self) -> None:
        suite_path = self.write_relation_suite(right_path="../outside.tsv")
        self.write_registry([("relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_table_inclusion_with_filter_split_and_extra_container_rows_passes(
        self,
    ) -> None:
        suite_path = self.write_inclusion_suite()
        self.write_registry([("inclusion", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "passed")

    def test_table_inclusion_missing_member_has_stable_diagnostic(self) -> None:
        suite_path = self.write_inclusion_suite()
        self.write(
            "container.tsv",
            "scope\tvalue\nselected\ta\nselected\tc\n",
        )
        self.write_registry([("inclusion", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        diagnostic = result.diagnostics[0]
        self.assertEqual(diagnostic.code, "ASSERT.TABLE_INCLUSION")
        self.assertEqual(diagnostic.expected, "all members present in container")
        self.assertEqual(diagnostic.observed, "(('b',),)")

    def test_table_inclusion_rejects_duplicate_members(self) -> None:
        suite_path = self.write_inclusion_suite()
        self.write(
            "members.tsv",
            "group\titems\nselected\ta,a\n",
        )
        self.write_registry([("inclusion", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        diagnostic = result.diagnostics[0]
        self.assertEqual(diagnostic.code, "ASSERT.INCLUSION_DUPLICATE")
        self.assertEqual(diagnostic.observed, "members=2/1,container=3/3")

    def test_table_inclusion_rejects_duplicate_container_rows(self) -> None:
        suite_path = self.write_inclusion_suite()
        self.write(
            "container.tsv",
            "scope\tvalue\nselected\ta\nselected\tb\nselected\tb\n",
        )
        self.write_registry([("inclusion", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        diagnostic = result.diagnostics[0]
        self.assertEqual(diagnostic.code, "ASSERT.INCLUSION_DUPLICATE")
        self.assertEqual(diagnostic.observed, "members=2/2,container=3/2")

    def test_malformed_inclusion_collection_is_invalid(self) -> None:
        self.write(
            "container.tsv",
            "scope\tvalue\nselected\ta\n",
        )
        self.write(
            "suites/inclusion.toml",
            """
            schema_version = 1
            id = "inclusion"
            owner = "test.owner"
            description = "Inclusion suite"

            [[checks]]
            id = "inclusion"
            type = "inclusion"
            members = true

            [checks.container]
            path = "container.tsv"
            header = ["scope", "value"]
            columns = ["value"]
            order = "source"
            """,
        )
        suite_path = "suites/inclusion.toml"
        self.write_registry([("inclusion", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        diagnostic = raised.exception.diagnostic
        self.assertEqual(diagnostic.code, "CONFIG.INCLUSION_COLLECTION")
        self.assertEqual(diagnostic.field, "members")

    def test_unknown_inclusion_field_is_invalid(self) -> None:
        suite_path = self.write_inclusion_suite(extra="unknown = true")
        self.write_registry([("inclusion", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")

    def test_inclusion_rejects_relation_side_aliases(self) -> None:
        suite_path = self.write_inclusion_suite(extra="left = true")
        self.write_registry([("inclusion", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        diagnostic = raised.exception.diagnostic
        self.assertEqual(diagnostic.code, "CONFIG.UNKNOWN_FIELD")
        self.assertEqual(diagnostic.field, "left")

    def test_missing_inclusion_input_is_unavailable(self) -> None:
        suite_path = self.write_inclusion_suite(container_path="missing.tsv")
        self.write_registry([("inclusion", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_inclusion_path_escape_is_invalid(self) -> None:
        suite_path = self.write_inclusion_suite(container_path="../outside.tsv")
        self.write_registry([("inclusion", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_inclusion_projection_width_mismatch_is_invalid(self) -> None:
        suite_path = self.write_inclusion_suite(
            container_columns='columns = ["scope", "value"]'
        )
        self.write_registry([("inclusion", suite_path, [])])

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        diagnostic = raised.exception.diagnostic
        self.assertEqual(diagnostic.code, "CONFIG.INCLUSION_WIDTH")
        self.assertEqual(diagnostic.expected, "1")
        self.assertEqual(diagnostic.observed, "2")

    def test_keyed_relation_derives_keys_and_ignores_unrelated_reordered_rows(
        self,
    ) -> None:
        suite_path = self.write_keyed_relation_suite()
        self.write_registry([("keyed-relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "passed")

    def test_keyed_relation_reports_missing_expected_and_observed_records(self) -> None:
        suite_path = self.write_keyed_relation_suite()
        self.write(
            "expected.tsv",
            "id\towner\tdisposition\na\towner-a\tmove\n",
        )
        self.write(
            "observed.tsv",
            "id\tsource\ttarget\tdisposition\n"
            "b\tlegacy\towner-b\trefine\n",
        )
        self.write_registry([("keyed-relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(
            [(item.code, item.field, item.expected) for item in result.diagnostics],
            [
                ("ASSERT.KEYED_RELATION_MISSING", "expected", "b"),
                ("ASSERT.KEYED_RELATION_MISSING", "observed", "a"),
            ],
        )

    def test_keyed_relation_reports_duplicate_derived_keys(self) -> None:
        suite_path = self.write_keyed_relation_suite()
        self.write("keys.tsv", "row\titems\nselected\ta,a\n")
        self.write_registry([("keyed-relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(
            result.diagnostics[0].code,
            "ASSERT.KEYED_RELATION_DUPLICATE_KEY",
        )
        self.assertEqual(result.diagnostics[0].observed, "2/1")

    def test_keyed_relation_reports_duplicate_records_by_role(self) -> None:
        suite_path = self.write_keyed_relation_suite()
        self.write(
            "expected.tsv",
            "id\towner\tdisposition\na\towner-a\tmove\n"
            "a\towner-a\tmove\nb\towner-b\trefine\n",
        )
        self.write(
            "observed.tsv",
            "id\tsource\ttarget\tdisposition\n"
            "a\tlegacy\towner-a\tmove\n"
            "b\tlegacy\towner-b\trefine\n"
            "b\tlegacy\towner-b\trefine\n",
        )
        self.write_registry([("keyed-relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(
            [(item.code, item.field, item.observed) for item in result.diagnostics],
            [
                ("ASSERT.KEYED_RELATION_DUPLICATE_RECORD", "observed", "b:2"),
                ("ASSERT.KEYED_RELATION_DUPLICATE_RECORD", "expected", "a:2"),
            ],
        )

    def test_keyed_relation_reports_value_mismatch(self) -> None:
        suite_path = self.write_keyed_relation_suite()
        self.write(
            "observed.tsv",
            "id\tsource\ttarget\tdisposition\n"
            "a\tlegacy\twrong-owner\tmove\n"
            "b\tlegacy\towner-b\trefine\n",
        )
        self.write_registry([("keyed-relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        diagnostic = result.diagnostics[0]
        self.assertEqual(diagnostic.code, "ASSERT.KEYED_RELATION_MISMATCH")
        self.assertEqual(diagnostic.field, "a")
        self.assertEqual(diagnostic.expected, "('owner-a', 'move')")
        self.assertEqual(diagnostic.observed, "('wrong-owner', 'move')")

    def test_keyed_relation_requires_nonempty_unique_keys(self) -> None:
        suite_path = self.write_keyed_relation_suite()
        self.write("keys.tsv", "row\titems\nignored\tz\n")
        self.write_registry([("keyed-relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(
            result.diagnostics[0].code,
            "ASSERT.KEYED_RELATION_EMPTY_KEYS",
        )

    def test_keyed_relation_record_filters_are_explicit(self) -> None:
        suite_path = self.write_keyed_relation_suite(
            expected_extra='where = { field = "owner", op = "ne", value = "ignored" }',
            observed_extra='where = { field = "target", op = "ne", value = "ignored" }',
        )
        self.write_registry([("keyed-relation", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "passed")

    def test_keyed_relation_rejects_configuration_errors(self) -> None:
        cases = (
            ({"key_columns": '["row", "items"]'}, "CONFIG.KEYED_RELATION_KEY_WIDTH"),
            ({"expected_values": '["id"]'}, "CONFIG.KEYED_RELATION_VALUES"),
            ({"observed_values": '["missing"]'}, "CONFIG.KEYED_RELATION_VALUES"),
            ({"expected_values": '[]'}, "CONFIG.STRING_LIST"),
            ({"observed_values": '["target"]'}, "CONFIG.KEYED_RELATION_VALUE_WIDTH"),
            ({"extra": 'mode = "set"'}, "CONFIG.UNKNOWN_FIELD"),
            ({"expected_extra": 'columns = ["owner"]'}, "CONFIG.UNKNOWN_FIELD"),
            ({"observed_extra": 'left = true'}, "CONFIG.UNKNOWN_FIELD"),
            (
                {"expected_extra": 'where = { field = "missing", op = "eq", value = "x" }'},
                "CONFIG.TABLE_COLUMN",
            ),
        )
        for options, code in cases:
            with self.subTest(options=options, code=code):
                suite_path = self.write_keyed_relation_suite(**options)
                self.write_registry([("keyed-relation", suite_path, [])])
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, self.registry)
                self.assertEqual(raised.exception.diagnostic.code, code)

    def test_keyed_relation_input_failures_are_typed(self) -> None:
        suite_path = self.write_keyed_relation_suite(expected_path="missing.tsv")
        self.write_registry([("keyed-relation", suite_path, [])])
        result = Verifier(self.root, self.registry).run()[0]
        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

        suite_path = self.write_keyed_relation_suite(observed_path="../outside.tsv")
        self.write_registry([("keyed-relation", suite_path, [])])
        result = Verifier(self.root, self.registry).run()[0]
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

        suite_path = self.write_keyed_relation_suite()
        (self.root / "expected.tsv").write_bytes(b"id\towner\tdisposition\n\xff")
        self.write_registry([("keyed-relation", suite_path, [])])
        result = Verifier(self.root, self.registry).run()[0]
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "INPUT.INVALID_UTF8")

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

    def test_dependency_graph_resolves_registered_suite_ids_and_paths(self) -> None:
        self.write("evidence.md", "required\n")
        suite_path = self.write_text_suite("text")
        self.write_registry([("text", suite_path, [])])

        verifier = Verifier(self.root, self.registry)

        self.assertEqual(verifier.dependency_graph.resolve("text"), "text")
        self.assertEqual(verifier.dependency_graph.resolve(suite_path), "text")

    def test_decision_mismatch_has_stable_diagnostic(self) -> None:
        suite_path = self.write_decision_suite(expected="allow")
        self.write_registry([("decision", suite_path, [])])

        result = Verifier(self.root, self.registry).run()[0]

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.diagnostics[0].code, "ASSERT.DECISION_OUTCOME")
        self.assertEqual(result.diagnostics[0].row, 3)

    def test_engine_errors_derive_exit_status_from_the_typed_outcome(self) -> None:
        for outcome, expected_exit in (
            ("invalid", 2),
            ("unavailable", 3),
            ("unsupported", 4),
        ):
            with self.subTest(outcome=outcome):
                error = EngineError(Diagnostic("TEST.OUTCOME", outcome, "test"))
                self.assertEqual(error.exit_code, expected_exit)

        with self.assertRaisesRegex(ValueError, "contradicts"):
            EngineError(Diagnostic("TEST.OUTCOME", "unavailable", "test"), 2)

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
        self.assertEqual(repository_path("directory/item.md").as_posix(), "directory/item.md")
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

    def test_cli_formats_preserve_assertion_exit_classification(self) -> None:
        suite_path = self.write_decision_suite(expected="allow")
        self.write_registry([("decision", suite_path, [])])

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
                self.assertIn("ASSERT.DECISION_OUTCOME", output.getvalue())


if __name__ == "__main__":
    unittest.main()
