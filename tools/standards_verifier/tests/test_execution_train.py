from __future__ import annotations

import csv
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.diagnostics import EngineError
from standards_verifier.engine import Verifier


class ExecutionTrainTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write("owners/one.md", "one\n")
        self.write("owners/two.md", "two\n")
        self.write(
            "train.tsv",
            "order\twave\tstart_id\tend_id\tsource\towner\towner_state\t"
            "activation\tcheckpoint\n"
            "1\ttrust-boundaries\tSTD-0001\tSTD-0002\tlegacy-one.md\t"
            "owners/one.md\texists\tpre-slice-review\tfocused\n"
            "2\tapplication-boundaries\tSTD-0003\tSTD-0003\tlegacy-two.md\t"
            "owners/two.md\tmissing\towner-review\tfull-suite\n",
        )
        self.write(
            "decomposition.tsv",
            "baseline_order\tchild_order\tids\tsource\towner\towner_state\t"
            "activation\tcheckpoint\trationale\towner_transition\n"
            "2\t1\tSTD-0003\tlegacy-two.md\towners/two.md\texists\towner-review\t"
            "focused\tcreate owner\tmissing-to-exists\n",
        )
        self.write(
            "owner-map.tsv",
            """
            id\tcurrent_path\tline\tfuture_owner\tdisposition\theading
            STD-0001\tlegacy-one.md\t1\towners/one.md\treplace\tone
            STD-0002\tlegacy-one.md\t2\towners/one.md\treplace\ttwo
            STD-0003\tlegacy-two.md\t3\towners/two.md\treplace\tthree
            """,
        )
        self.write(
            "dispositions.tsv",
            """
            id\tsource\ttarget\tdisposition\trationale
            STD-0001\tlegacy-one.md\towners/one.md\treplace\tone
            STD-0002\tlegacy-one.md\towners/one.md\treplace\ttwo
            STD-0003\tlegacy-two.md\towners/two.md\treplace\tthree
            """,
        )
        self.write_suite()
        self.write(
            "registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "execution-train"
            path = "suite.toml"
            requires = []
            """,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_suite(self, extra: str = "") -> None:
        self.write(
            "suite.toml",
            f"""
            schema_version = 1
            id = "execution-train"
            owner = "migration.parent-plan"
            description = "Execution train test"

            [[checks]]
            id = "state"
            type = "execution_train"
            train_path = "train.tsv"
            decomposition_path = "decomposition.tsv"
            owner_map_path = "owner-map.tsv"
            dispositions_path = "dispositions.tsv"
            expected_train_rows = 2
            expected_baseline_ids = 3
            expected_checkpoints = 1
            {extra}
            """,
        )

    def rows(self, path: str) -> list[list[str]]:
        with (self.root / path).open(encoding="utf-8", newline="") as source:
            return list(csv.reader(source, delimiter="\t"))

    def write_rows(self, path: str, rows: list[list[str]]) -> None:
        with (self.root / path).open("w", encoding="utf-8", newline="") as target:
            csv.writer(target, delimiter="\t", lineterminator="\n").writerows(rows)

    def mutate(self, path: str, row: int, column: int, value: str) -> None:
        rows = self.rows(path)
        rows[row][column] = value
        self.write_rows(path, rows)

    def result(self):
        return Verifier(self.root, "registry.toml").run(("execution-train",))[0]

    def assert_code(self, expected: str) -> None:
        result = self.result()
        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, expected)

    def test_complete_train_passes(self) -> None:
        self.assertEqual(self.result().status, "passed")

    def test_noncontiguous_train_order_is_invalid(self) -> None:
        self.mutate("train.tsv", 2, 0, "3")
        self.assert_code("ASSERT.EXECUTION_TRAIN.ORDER")

    def test_owner_map_source_drift_is_invalid(self) -> None:
        self.mutate("owner-map.tsv", 2, 1, "wrong.md")
        self.assert_code("ASSERT.EXECUTION_TRAIN.OWNER_ALIGNMENT")

    def test_partial_cluster_is_invalid(self) -> None:
        rows = self.rows("dispositions.tsv")
        del rows[2]
        self.write_rows("dispositions.tsv", rows)
        self.assert_code("ASSERT.EXECUTION_TRAIN.PARTIAL_CLUSTER")

    def test_duplicate_decomposition_identifier_is_invalid(self) -> None:
        self.mutate("decomposition.tsv", 1, 2, "STD-0003,STD-0003")
        self.assert_code("ASSERT.EXECUTION_TRAIN.DECOMPOSITION_COVERAGE")

    def test_contradictory_creation_transition_is_invalid(self) -> None:
        self.mutate("train.tsv", 2, 6, "exists")
        self.assert_code("ASSERT.EXECUTION_TRAIN.OWNER_TRANSITION")

    def test_missing_child_owner_requires_owner_review(self) -> None:
        self.mutate("train.tsv", 2, 6, "exists")
        self.mutate("decomposition.tsv", 1, 4, "owners/missing.md")
        self.mutate("decomposition.tsv", 1, 5, "missing")
        self.mutate("decomposition.tsv", 1, 6, "pre-slice-review")
        self.mutate("decomposition.tsv", 1, 9, "none")
        self.assert_code("ASSERT.EXECUTION_TRAIN.OWNER_STATE")

    def test_effective_owner_path_must_exist(self) -> None:
        (self.root / "owners/two.md").unlink()
        self.assert_code("ASSERT.EXECUTION_TRAIN.OWNER_PATH")

    def test_remaining_owner_map_id_must_belong_to_train(self) -> None:
        rows = self.rows("owner-map.tsv")
        rows.append(
            ["STD-0004", "legacy-three.md", "4", "owners/one.md", "replace", "four"]
        )
        self.write_rows("owner-map.tsv", rows)
        self.assert_code("ASSERT.EXECUTION_TRAIN.REMAINING_COVERAGE")

    def test_reversed_identifier_range_is_invalid(self) -> None:
        self.mutate("train.tsv", 2, 2, "STD-0004")
        self.assert_code("ASSERT.EXECUTION_TRAIN.RANGE")

    def test_unknown_configuration_field_is_invalid(self) -> None:
        self.write_suite('unexpected = "value"')
        with self.assertRaises(EngineError) as raised:
            self.result()
        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")

    def test_boolean_count_is_invalid(self) -> None:
        suite = (self.root / "suite.toml").read_text(encoding="utf-8")
        self.write(
            "suite.toml",
            suite.replace("expected_train_rows = 2", "expected_train_rows = true"),
        )
        with self.assertRaises(EngineError) as raised:
            self.result()
        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.INTEGER")


if __name__ == "__main__":
    unittest.main()
