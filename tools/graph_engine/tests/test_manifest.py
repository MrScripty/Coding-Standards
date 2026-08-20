from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ENGINE_ROOT))

from graph_engine import InvalidSourceError, load_registry


class ManifestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write("a.md", "a")
        self.write("b.md", "b")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def manifest(self, *, relation: str = "projects") -> str:
        return f'''
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
            purpose = "Explicit semantic edges."
            directions = ["incoming", "outgoing"]
            transitive = false

            [[edges]]
            id = "a-b"
            source = "a"
            target = "b"
            relation = {relation!r}
            groups = ["semantic"]
            traversable = true
        '''.replace("'", '"')

    def registry(self, source_path: str = "graph.toml"):
        self.write(
            "registry.toml",
            f'''
            schema_version = 1

            [[sources]]
            id = "sample"
            kind = "manifest"
            path = "{source_path}"
            ''',
        )
        return load_registry(self.root, "registry.toml")

    def test_registered_manifest_loads_nodes_groups_edges_and_provenance(self) -> None:
        self.write("graph.toml", self.manifest())

        registry = self.registry()

        self.assertEqual(registry.resolve("a.md"), "a")
        self.assertEqual(registry.edge("a-b").provenance.source_id, "sample")
        self.assertEqual(registry.edge("a-b").provenance.locator, "graph.toml")

    def test_unregistered_manifest_file_contributes_nothing(self) -> None:
        self.write("graph.toml", self.manifest())
        self.write("registry.toml", "schema_version = 1\nsources = []\n")

        registry = load_registry(self.root, "registry.toml")

        self.assertEqual(len(registry.edges), 0)

    def test_unknown_source_kind_and_mismatched_identity_are_rejected(self) -> None:
        self.write("graph.toml", self.manifest())
        self.write(
            "registry.toml",
            '''
            schema_version = 1
            [[sources]]
            id = "sample"
            kind = "generator"
            path = "graph.toml"
            ''',
        )
        with self.assertRaises(InvalidSourceError):
            load_registry(self.root, "registry.toml")

        self.write("registry.toml", '''
            schema_version = 1
            [[sources]]
            id = "different"
            kind = "manifest"
            path = "graph.toml"
        ''')
        with self.assertRaises(InvalidSourceError):
            load_registry(self.root, "registry.toml")

    def test_strict_schema_rejects_unknown_fields(self) -> None:
        self.write("graph.toml", self.manifest() + "unknown = true\n")

        with self.assertRaises(InvalidSourceError):
            self.registry()
