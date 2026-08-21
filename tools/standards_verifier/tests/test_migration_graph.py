from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.migration_graph import (
    COMPONENT_OUTPUT_PATH,
    EDGE_OUTPUT_PATH,
    NODE_OUTPUT_PATH,
    GraphDiagnostic,
    check_graph,
    collect_migration_graph,
    render_components,
    render_edges,
    render_nodes,
    write_graph,
)


class MigrationGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.evaluation = self.root / "evaluation/standards-effectiveness"
        self.evaluation.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def test_collects_typed_edges_and_strong_components(self) -> None:
        self.write(
            "evaluation/standards-effectiveness/verify-a.sh",
            "#!/usr/bin/env bash\n\"$S/verify-b.sh\"\n\"$S/check-shared.sh\"\n",
        )
        self.write(
            "evaluation/standards-effectiveness/verify-b.sh",
            "#!/usr/bin/env bash\n\"$S/verify-a.sh\"\n",
        )
        self.write(
            "evaluation/standards-effectiveness/check-shared.sh",
            "#!/usr/bin/env bash\nprintf 'ok\\n'\n",
        )
        self.write(
            "evaluation/standards-effectiveness/frozen.tsv",
            "checker\nevaluation/standards-effectiveness/verify-a.sh\n",
        )
        self.write(
            "scripts/run.sh",
            "#!/usr/bin/env bash\n$ROOT/evaluation/standards-effectiveness/verify-b.sh\n",
        )

        graph = collect_migration_graph(self.root)

        self.assertEqual(len(graph.nodes), 3)
        self.assertEqual(
            {
                (edge.edge_type, edge.source, edge.target)
                for edge in graph.edges
                if edge.edge_type.endswith("_dependency")
            },
            {
                (
                    "helper_dependency",
                    "evaluation/standards-effectiveness/verify-a.sh",
                    "evaluation/standards-effectiveness/check-shared.sh",
                ),
                (
                    "verifier_dependency",
                    "evaluation/standards-effectiveness/verify-a.sh",
                    "evaluation/standards-effectiveness/verify-b.sh",
                ),
                (
                    "verifier_dependency",
                    "evaluation/standards-effectiveness/verify-b.sh",
                    "evaluation/standards-effectiveness/verify-a.sh",
                ),
            },
        )
        cyclic = [component for component in graph.components if component.cyclic]
        self.assertEqual(len(cyclic), 1)
        self.assertEqual(
            cyclic[0].members,
            (
                "evaluation/standards-effectiveness/verify-a.sh",
                "evaluation/standards-effectiveness/verify-b.sh",
            ),
        )
        self.assertIn(
            "evaluation/standards-effectiveness/frozen.tsv",
            cyclic[0].contract_inbound_files,
        )

    def test_rejects_unresolved_target(self) -> None:
        self.write(
            "evaluation/standards-effectiveness/verify-a.sh",
            "#!/usr/bin/env bash\n\"$S/check-missing.sh\"\n",
        )

        with self.assertRaises(GraphDiagnostic) as context:
            collect_migration_graph(self.root)

        self.assertEqual(context.exception.code, "GRAPH.TARGET_UNAVAILABLE")
        self.assertEqual(context.exception.exit_code, 3)

    def test_incidental_checker_name_is_not_an_executable_dependency(self) -> None:
        self.write(
            "evaluation/standards-effectiveness/verify-a.sh",
            "#!/usr/bin/env bash\nfor expected in 'verify-b.sh'; do :; done\n",
        )
        self.write(
            "evaluation/standards-effectiveness/verify-b.sh",
            "#!/usr/bin/env bash\nprintf 'ok\\n'\n",
        )

        graph = collect_migration_graph(self.root)

        self.assertFalse(
            any(
                edge.edge_type.endswith("_dependency")
                for edge in graph.edges
            )
        )
        self.assertIn(
            (
                "executable_reference",
                "evaluation/standards-effectiveness/verify-a.sh",
                "evaluation/standards-effectiveness/verify-b.sh",
            ),
            {
                (edge.edge_type, edge.source, edge.target)
                for edge in graph.edges
            },
        )

    def test_rejects_ambiguous_target(self) -> None:
        self.write(
            "evaluation/standards-effectiveness/verify-a.sh",
            "#!/usr/bin/env bash\n\"$S/check-shared.sh\"\n",
        )
        self.write("one/check-shared.sh", "#!/usr/bin/env bash\n")
        self.write("two/check-shared.sh", "#!/usr/bin/env bash\n")

        with self.assertRaises(GraphDiagnostic) as context:
            collect_migration_graph(self.root)

        self.assertEqual(context.exception.code, "GRAPH.TARGET_AMBIGUOUS")
        self.assertEqual(context.exception.exit_code, 2)

    def test_render_is_deterministic_and_excludes_generated_outputs(self) -> None:
        self.write(
            "evaluation/standards-effectiveness/verify-a.sh",
            "#!/usr/bin/env bash\nprintf 'ok\\n'\n",
        )
        first = collect_migration_graph(self.root)
        rendered = (
            render_nodes(first),
            render_edges(first),
            render_components(first),
        )
        self.assertFalse(
            any(line.endswith("\t") for line in rendered[2].splitlines())
        )
        self.assertIn("\t-\t-\t-\t-\n", rendered[2])
        self.write(
            NODE_OUTPUT_PATH.as_posix(),
            "node\tkind\nverify-a.sh\tstale\n",
        )
        second = collect_migration_graph(self.root)

        self.assertEqual(
            rendered,
            (
                render_nodes(second),
                render_edges(second),
                render_components(second),
            ),
        )

    def test_component_ids_survive_unrelated_node_insertion_and_removal(self) -> None:
        for name in ("b", "c"):
            self.write(
                f"evaluation/standards-effectiveness/verify-{name}.sh",
                "#!/usr/bin/env bash\nprintf 'ok\\n'\n",
            )

        first = collect_migration_graph(self.root)
        first_ids = {component.members: component.component for component in first.components}

        self.write(
            "evaluation/standards-effectiveness/verify-a.sh",
            "#!/usr/bin/env bash\nprintf 'ok\\n'\n",
        )
        inserted = collect_migration_graph(self.root)
        inserted_ids = {
            component.members: component.component for component in inserted.components
        }

        self.assertEqual(
            {members: inserted_ids[members] for members in first_ids},
            first_ids,
        )
        (self.evaluation / "verify-a.sh").unlink()
        removed = collect_migration_graph(self.root)
        self.assertEqual(
            {component.members: component.component for component in removed.components},
            first_ids,
        )

    def test_component_id_changes_only_with_component_membership(self) -> None:
        self.write(
            "evaluation/standards-effectiveness/verify-a.sh",
            "#!/usr/bin/env bash\nprintf 'ok\\n'\n",
        )
        self.write(
            "evaluation/standards-effectiveness/verify-b.sh",
            "#!/usr/bin/env bash\nprintf 'ok\\n'\n",
        )
        independent = collect_migration_graph(self.root)
        independent_ids = {component.component for component in independent.components}

        self.write(
            "evaluation/standards-effectiveness/verify-a.sh",
            "#!/usr/bin/env bash\n\"$S/verify-b.sh\"\n",
        )
        self.write(
            "evaluation/standards-effectiveness/verify-b.sh",
            "#!/usr/bin/env bash\n\"$S/verify-a.sh\"\n",
        )
        cyclic = collect_migration_graph(self.root)

        self.assertEqual(len(cyclic.components), 1)
        self.assertTrue(cyclic.components[0].cyclic)
        self.assertEqual(
            cyclic.components[0].members,
            (
                "evaluation/standards-effectiveness/verify-a.sh",
                "evaluation/standards-effectiveness/verify-b.sh",
            ),
        )
        self.assertNotIn(cyclic.components[0].component, independent_ids)

    def test_write_and_check_detect_stale_and_malformed_outputs(self) -> None:
        self.write(
            "evaluation/standards-effectiveness/verify-a.sh",
            "#!/usr/bin/env bash\nprintf 'ok\\n'\n",
        )

        self.assertEqual(write_graph(self.root), 0)
        self.assertEqual(check_graph(self.root), 0)
        self.write(
            "evaluation/standards-effectiveness/verify-b.sh",
            "#!/usr/bin/env bash\nprintf 'ok\\n'\n",
        )
        self.assertEqual(check_graph(self.root), 1)
        self.assertEqual(write_graph(self.root), 0)
        self.write(EDGE_OUTPUT_PATH.as_posix(), "wrong\theader\n")
        self.assertEqual(check_graph(self.root), 2)
        self.assertTrue((self.root / COMPONENT_OUTPUT_PATH).is_file())


if __name__ == "__main__":
    unittest.main()
