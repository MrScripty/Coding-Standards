from __future__ import annotations

import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.engine import Verifier


MANIFEST_HEADER = (
    "package_id\tedge_type\tsource\ttarget\towner\tdisposition\t"
    "replacement\tevidence\trationale\tstate\n"
)
PACKAGE_HEADER = (
    "train_order\tpackage_id\tsubject\towner\trisk\tsemantic_outcome\t"
    "write_set\tprerequisites\tverification\tstate\n"
)
EDGE_HEADER = "edge_type\tsource\ttarget\n"


class EdgeDispositionsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write("evidence.md", "reviewed\n")
        self.write("target.sh", "#!/usr/bin/env bash\n")
        self.write_target_suite()
        self.write_suite()
        self.write_registry()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_registry(self) -> None:
        self.write(
            "registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "target"
            path = "suites/target.toml"
            requires = []

            [[suites]]
            id = "edges"
            path = "suites/edges.toml"
            requires = ["target"]
            """,
        )

    def write_target_suite(self) -> None:
        self.write(
            "suites/target.toml",
            """
            schema_version = 1
            id = "target"
            owner = "test.owner"
            description = "Target suite"

            [[checks]]
            id = "evidence"
            type = "exact_text"
            path = "evidence.md"
            expected = "reviewed\\n"
            """,
        )

    def write_suite(self, path: str = "edge-dispositions.tsv") -> None:
        self.write(
            "suites/edges.toml",
            f"""
            schema_version = 1
            id = "edges"
            owner = "test.owner"
            description = "Executable edge dispositions"

            [[checks]]
            id = "contract"
            type = "edge_dispositions"
            path = {json.dumps(path)}
            packages_path = "packages.tsv"
            edges_path = "edges.tsv"
            registry_path = "registry.toml"
            participation_token = "edge-dispositions"
            edge_free_token = "edge-free"
            """,
        )

    def write_package(
        self,
        *,
        package_id: str = "P1",
        source: str = "source.sh",
        owner: str = "owner.md",
        state: str = "admitted",
        verification: str = "focused,edge-dispositions",
    ) -> None:
        self.write(
            "packages.tsv",
            PACKAGE_HEADER
            + self.package_row(
                package_id=package_id,
                source=source,
                owner=owner,
                state=state,
                verification=verification,
            ),
        )

    def package_row(
        self,
        *,
        package_id: str = "P1",
        source: str = "source.sh",
        owner: str = "owner.md",
        state: str = "admitted",
        verification: str = "focused,edge-dispositions",
    ) -> str:
        return (
            "1\t"
            + package_id
            + "\tchecker:"
            + source
            + "\t"
            + owner
            + "\tconsolidation\toutcome\tsuites/edges.toml\tnone\t"
            + verification
            + "\t"
            + state
            + "\n"
        )

    def row(
        self,
        *,
        package_id: str = "P1",
        edge_type: str = "helper_dependency",
        source: str = "source.sh",
        target: str = "target.sh",
        owner: str = "owner.md",
        disposition: str = "native-engine",
        replacement: str = "assertion:suites/edges.toml#contract",
        evidence: str = "evidence.md",
        state: str = "admitted",
    ) -> str:
        return (
            f"{package_id}\t{edge_type}\t{source}\t{target}\t{owner}\t"
            f"{disposition}\t{replacement}\t{evidence}\treviewed\t{state}\n"
        )

    def run_contract(self):
        return next(
            result
            for result in Verifier(self.root, "registry.toml").run(("edges",))
            if result.id == "edges"
        )

    def admitted_contract(self) -> None:
        self.write("source.sh", "#!/usr/bin/env bash\n")
        self.write_package()
        self.write(
            "edges.tsv", EDGE_HEADER + "helper_dependency\tsource.sh\ttarget.sh\n"
        )
        self.write("edge-dispositions.tsv", MANIFEST_HEADER + self.row())

    def test_admitted_exact_edge_contract_passes(self) -> None:
        self.admitted_contract()

        self.assertEqual(self.run_contract().status, "passed")

    def test_accepted_absent_edge_contract_passes(self) -> None:
        self.write_package(state="accepted")
        self.write("edges.tsv", EDGE_HEADER)
        self.write(
            "edge-dispositions.tsv",
            MANIFEST_HEADER
            + self.row(
                disposition="suite-requires",
                replacement="suite:edges->target",
                state="accepted",
            ),
        )

        self.assertEqual(self.run_contract().status, "passed")

    def test_all_non_suite_replacement_forms_pass_while_admitted(self) -> None:
        self.write("source.sh", "#!/usr/bin/env bash\n")
        self.write("artifact.sh", "#!/usr/bin/env bash\n")
        self.write("other.sh", "#!/usr/bin/env bash\n")
        self.write("unresolved.sh", "#!/usr/bin/env bash\n")
        self.write(
            "packages.tsv",
            PACKAGE_HEADER
            + self.package_row()
            + self.package_row(
                package_id="P2",
                source="other.sh",
                verification="focused",
            ),
        )
        self.write(
            "edges.tsv",
            EDGE_HEADER
            + "helper_dependency\tsource.sh\ttarget.sh\n"
            + "executable_reference\tsource.sh\tartifact.sh\n"
            + "verifier_dependency\tsource.sh\tother.sh\n"
            + "helper_dependency\tsource.sh\tunresolved.sh\n",
        )
        self.write(
            "edge-dispositions.tsv",
            MANIFEST_HEADER
            + self.row(
                disposition="independent-gate",
                replacement="checker:target.sh",
            )
            + self.row(
                edge_type="executable_reference",
                target="artifact.sh",
                disposition="external-owned-artifact",
                replacement="artifact:artifact.sh",
            )
            + self.row(
                edge_type="verifier_dependency",
                target="other.sh",
                disposition="same-owner-package",
                replacement="package:P2",
            )
            + self.row(
                target="unresolved.sh",
                disposition="invalid/unresolved",
                replacement="unresolved:none",
            ),
        )

        self.assertEqual(self.run_contract().status, "passed")

    def test_malformed_manifest_schema_is_invalid(self) -> None:
        self.write_package()
        self.write("edges.tsv", EDGE_HEADER)
        self.write("edge-dispositions.tsv", "package_id\tsource\n")

        result = self.run_contract()

        self.assertEqual(result.diagnostics[0].code, "TABLE.HEADER_CONTRACT")

    def test_duplicate_edge_is_invalid(self) -> None:
        self.admitted_contract()
        row = self.row()
        self.write("edge-dispositions.tsv", MANIFEST_HEADER + row + row)

        result = self.run_contract()

        self.assertIn(
            "ASSERT.EDGE_DUPLICATE", {item.code for item in result.diagnostics}
        )

    def test_unknown_package_is_invalid(self) -> None:
        self.write_package()
        self.write("edges.tsv", EDGE_HEADER)
        self.write(
            "edge-dispositions.tsv",
            MANIFEST_HEADER + self.row(package_id="missing"),
        )

        result = self.run_contract()

        self.assertEqual(result.diagnostics[0].code, "ASSERT.EDGE_PACKAGE")

    def test_incomplete_outgoing_coverage_is_invalid(self) -> None:
        self.admitted_contract()
        self.write("other.sh", "#!/usr/bin/env bash\n")
        self.write(
            "edges.tsv",
            EDGE_HEADER
            + "helper_dependency\tsource.sh\ttarget.sh\n"
            + "verifier_dependency\tsource.sh\tother.sh\n",
        )

        result = self.run_contract()

        self.assertIn(
            "ASSERT.EDGE_INCOMPLETE_COVERAGE",
            {item.code for item in result.diagnostics},
        )

    def test_absent_admitted_edge_is_invalid(self) -> None:
        self.admitted_contract()
        self.write("edges.tsv", EDGE_HEADER)

        result = self.run_contract()

        self.assertIn(
            "ASSERT.EDGE_ADMITTED_ABSENT", {item.code for item in result.diagnostics}
        )

    def test_present_accepted_edge_is_invalid(self) -> None:
        self.write_package(state="accepted")
        self.write(
            "edges.tsv", EDGE_HEADER + "helper_dependency\tsource.sh\ttarget.sh\n"
        )
        self.write(
            "edge-dispositions.tsv",
            MANIFEST_HEADER
            + self.row(
                disposition="suite-requires",
                replacement="suite:edges->target",
                state="accepted",
            ),
        )

        result = self.run_contract()

        self.assertIn(
            "ASSERT.EDGE_ACCEPTED_PRESENT", {item.code for item in result.diagnostics}
        )

    def test_unresolved_accepted_edge_is_invalid(self) -> None:
        self.write_package(state="accepted")
        self.write("edges.tsv", EDGE_HEADER)
        self.write(
            "edge-dispositions.tsv",
            MANIFEST_HEADER
            + self.row(
                disposition="invalid/unresolved",
                replacement="unresolved:none",
                state="accepted",
            ),
        )

        result = self.run_contract()

        self.assertIn(
            "ASSERT.EDGE_UNRESOLVED_ACCEPTED",
            {item.code for item in result.diagnostics},
        )

    def test_wrong_replacement_kind_is_invalid(self) -> None:
        self.admitted_contract()
        self.write(
            "edge-dispositions.tsv",
            MANIFEST_HEADER
            + self.row(replacement="suite:edges->target"),
        )

        result = self.run_contract()

        self.assertIn(
            "ASSERT.EDGE_REPLACEMENT", {item.code for item in result.diagnostics}
        )

    def test_missing_native_assertion_is_invalid(self) -> None:
        self.admitted_contract()
        self.write(
            "edge-dispositions.tsv",
            MANIFEST_HEADER
            + self.row(replacement="assertion:suites/edges.toml#missing"),
        )

        result = self.run_contract()

        self.assertIn(
            "ASSERT.EDGE_REPLACEMENT", {item.code for item in result.diagnostics}
        )

    def test_missing_suite_requirement_is_invalid(self) -> None:
        self.write_package(state="accepted")
        self.write("edges.tsv", EDGE_HEADER)
        self.write_registry()
        registry = (self.root / "registry.toml").read_text(encoding="utf-8")
        self.write(
            "registry.toml",
            registry.replace('requires = ["target"]', "requires = []"),
        )
        self.write(
            "edge-dispositions.tsv",
            MANIFEST_HEADER
            + self.row(
                disposition="suite-requires",
                replacement="suite:edges->target",
                state="accepted",
            ),
        )

        result = self.run_contract()

        self.assertIn(
            "ASSERT.EDGE_REPLACEMENT", {item.code for item in result.diagnostics}
        )

    def test_evidence_path_escape_is_invalid(self) -> None:
        self.admitted_contract()
        self.write(
            "edge-dispositions.tsv",
            MANIFEST_HEADER + self.row(evidence="../outside.md"),
        )

        result = self.run_contract()

        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_participating_package_requires_rows(self) -> None:
        self.write_package()
        self.write("edges.tsv", EDGE_HEADER)
        self.write("edge-dispositions.tsv", MANIFEST_HEADER)

        result = self.run_contract()

        self.assertEqual(
            result.diagnostics[0].code, "ASSERT.EDGE_PACKAGE_COVERAGE"
        )

    def test_admitted_edge_free_package_passes(self) -> None:
        self.write("source.sh", "#!/usr/bin/env bash\n")
        self.write_package(verification="focused,edge-free")
        self.write("edges.tsv", EDGE_HEADER)
        self.write("edge-dispositions.tsv", MANIFEST_HEADER)

        self.assertEqual(self.run_contract().status, "passed")

    def test_accepted_edge_free_package_passes_when_source_is_absent(self) -> None:
        self.write_package(state="accepted", verification="focused,edge-free")
        self.write("edges.tsv", EDGE_HEADER)
        self.write("edge-dispositions.tsv", MANIFEST_HEADER)

        self.assertEqual(self.run_contract().status, "passed")

    def test_edge_free_package_rejects_graph_edges(self) -> None:
        self.write("source.sh", "#!/usr/bin/env bash\n")
        self.write_package(verification="focused,edge-free")
        self.write(
            "edges.tsv", EDGE_HEADER + "helper_dependency\tsource.sh\ttarget.sh\n"
        )
        self.write("edge-dispositions.tsv", MANIFEST_HEADER)

        result = self.run_contract()

        self.assertIn(
            "ASSERT.EDGE_FREE_PRESENT", {item.code for item in result.diagnostics}
        )

    def test_edge_free_package_rejects_disposition_rows(self) -> None:
        self.write("source.sh", "#!/usr/bin/env bash\n")
        self.write_package(verification="focused,edge-free")
        self.write(
            "edges.tsv", EDGE_HEADER + "helper_dependency\tsource.sh\ttarget.sh\n"
        )
        self.write("edge-dispositions.tsv", MANIFEST_HEADER + self.row())

        result = self.run_contract()

        self.assertIn(
            "ASSERT.EDGE_FREE_ROWS", {item.code for item in result.diagnostics}
        )

    def test_edge_participation_modes_are_mutually_exclusive(self) -> None:
        self.write("source.sh", "#!/usr/bin/env bash\n")
        self.write_package(
            verification="focused,edge-dispositions,edge-free"
        )
        self.write("edges.tsv", EDGE_HEADER)
        self.write("edge-dispositions.tsv", MANIFEST_HEADER)

        result = self.run_contract()

        self.assertIn("ASSERT.EDGE_MODE", {item.code for item in result.diagnostics})


if __name__ == "__main__":
    unittest.main()
