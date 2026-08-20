from __future__ import annotations

import contextlib
import io
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ENGINE_ROOT))

from graph_engine.cli import Row, main, render_tsv
from graph_engine.errors import UnsafeOutputError


class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write("a.md", "a")
        self.write("b.md", "b")
        self.write(
            "registry.toml",
            '''
            schema_version = 1
            [[sources]]
            id = "sample"
            kind = "manifest"
            path = "graph.toml"
            ''',
        )
        self.write(
            "graph.toml",
            '''
            schema_version = 1
            source_id = "sample"

            [[nodes]]
            id = "a"
            aliases = ["a.md"]

            [[nodes]]
            id = "b"
            aliases = ["b.md"]

            [[groups]]
            id = "semantic"
            purpose = "Semantic edges."
            directions = ["incoming", "outgoing"]
            transitive = true

            [[edges]]
            id = "a-b"
            source = "a"
            target = "b"
            relation = "projects"
            groups = ["semantic"]
            traversable = true
            metadata = { evidence = "suite:test" }
            ''',
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def run_cli(self, *args: str) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(
                ["--repo-root", str(self.root), "--registry", "registry.toml", *args],
                default_repo_root=self.root,
            )
        return code, output.getvalue()

    def test_node_query_reports_identity_direction_groups_metadata_and_provenance(self) -> None:
        code, output = self.run_cli("--node", "a.md")

        self.assertEqual(code, 0)
        row = output.splitlines()[1].split("\t")
        self.assertIn("a-b", row)
        self.assertIn("outgoing", row)
        self.assertIn("semantic", row)
        self.assertIn("evidence=suite:test", row)
        self.assertIn("manifest:sample:graph.toml", row)

    def test_exact_and_group_traversal_require_explicit_direction(self) -> None:
        code, output = self.run_cli("--edge", "a-b", "--traverse")
        self.assertEqual(code, 1)
        self.assertIn("requires explicit direction", output)

        code, output = self.run_cli(
            "--node", "a", "--group", "semantic", "--traverse"
        )
        self.assertEqual(code, 1)
        self.assertIn("requires explicit direction", output)

    def test_transitive_group_query_reports_explanatory_path(self) -> None:
        code, output = self.run_cli(
            "--node",
            "a",
            "--group",
            "semantic",
            "--direction",
            "outgoing",
            "--transitive",
        )

        self.assertEqual(code, 0)
        self.assertIn("a -> b", output)

    def test_hostile_control_characters_are_rejected_not_emitted(self) -> None:
        row = Row(*("safe",) * 13, "unsafe\nrecord")

        with self.assertRaises(UnsafeOutputError):
            render_tsv((row,))

    def test_list_groups_is_deterministic(self) -> None:
        code, output = self.run_cli("--list-groups")

        self.assertEqual(code, 0)
        self.assertEqual(output.count("\n"), 2)
        self.assertIn("Semantic edges.", output)
