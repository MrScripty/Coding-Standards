from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    load_router_projection,
)
from tools.standards_metadata.standards_metadata import load_canonical_module_corpus


REPO_ROOT = Path(__file__).resolve().parents[3]


class RouterProjectionTest(unittest.TestCase):
    def test_repository_projection_compiles_registered_modules_and_programs(self) -> None:
        modules = load_canonical_module_corpus(REPO_ROOT)
        projection = load_router_projection(REPO_ROOT, modules)

        self.assertEqual(projection.owner, "router")
        self.assertEqual(projection.base_modules, ("router",))
        self.assertEqual(len(projection.facts), 7)
        self.assertEqual(len(projection.rules), 38)
        self.assertTrue(all(rule.program.referenced_facts for rule in projection.rules))

    def test_projection_rejects_target_drift_from_router_tables(self) -> None:
        modules = load_canonical_module_corpus(REPO_ROOT)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evaluation/standards-effectiveness").mkdir(parents=True)
            shutil.copy2(REPO_ROOT / "STANDARDS-ROUTER.md", root / "STANDARDS-ROUTER.md")
            projection = root / "evaluation/standards-effectiveness/router-projection.toml"
            shutil.copy2(
                REPO_ROOT / "evaluation/standards-effectiveness/router-projection.toml",
                projection,
            )
            text = projection.read_text(encoding="utf-8")
            marker = '\n[[rules]]\nid = "route.topic.security"'
            projection.write_text(text.split(marker, 1)[0] + "\n", encoding="utf-8")

            with self.assertRaises(AnalysisError) as caught:
                load_router_projection(root, modules)
            self.assertEqual(caught.exception.failure.code, "ROUTER_PROJECTION.INVALID")


if __name__ == "__main__":
    unittest.main()
