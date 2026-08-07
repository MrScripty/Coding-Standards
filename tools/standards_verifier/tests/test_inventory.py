from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.inventory import (
    OUTPUT_PATH,
    check_inventory,
    collect_inventory,
    render_inventory,
    write_inventory,
)


class InventoryTest(unittest.TestCase):
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

    def test_collects_dependencies_references_and_mechanisms(self) -> None:
        self.write(
            "evaluation/standards-effectiveness/verify-owner.sh",
            "#!/usr/bin/env bash\nsed -n '1p' file | awk '{print}'\nrg value file\n./verify-base.sh\n./check-decision-table.sh\n",
        )
        self.write(
            "evaluation/standards-effectiveness/verify-base.sh",
            "#!/usr/bin/env bash\nprintf 'pass\\n'\n",
        )
        self.write("report.md", "Uses verify-owner.sh as evidence.\n")

        records = collect_inventory(self.root)

        self.assertEqual([record.checker for record in records], [
            "evaluation/standards-effectiveness/verify-base.sh",
            "evaluation/standards-effectiveness/verify-owner.sh",
        ])
        owner = records[1]
        self.assertEqual(owner.inbound_files, ("report.md",))
        self.assertEqual(owner.executable_inbound_files, ())
        self.assertEqual(owner.contract_inbound_files, ())
        self.assertEqual(owner.documentation_inbound_files, ("report.md",))
        self.assertEqual(owner.verifier_dependencies, ("verify-base.sh",))
        self.assertEqual(owner.helper_dependencies, ("check-decision-table.sh",))
        self.assertTrue(owner.uses_sed)
        self.assertTrue(owner.uses_awk)
        self.assertTrue(owner.uses_rg)
        self.assertTrue(owner.uses_decision_table)

    def test_render_is_deterministic_and_excludes_generated_output(self) -> None:
        self.write(
            "evaluation/standards-effectiveness/verify-owner.sh",
            "#!/usr/bin/env bash\nprintf 'pass\\n'\n",
        )
        first = render_inventory(collect_inventory(self.root))
        self.write(OUTPUT_PATH.as_posix(), "stale verify-owner.sh\n")
        second = render_inventory(collect_inventory(self.root))

        self.assertEqual(first, second)
        self.assertTrue(first.startswith("checker\tlines\tinbound_count"))

    def test_write_then_check_detects_staleness(self) -> None:
        checker = "evaluation/standards-effectiveness/verify-owner.sh"
        self.write(checker, "#!/usr/bin/env bash\nprintf 'pass\\n'\n")

        self.assertEqual(write_inventory(self.root), 0)
        self.assertEqual(check_inventory(self.root), 0)
        self.write(checker, "#!/usr/bin/env bash\nsed -n '1p' file\nprintf 'pass\\n'\n")
        self.assertEqual(check_inventory(self.root), 1)


if __name__ == "__main__":
    unittest.main()
