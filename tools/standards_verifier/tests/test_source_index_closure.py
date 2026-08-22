from __future__ import annotations

import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.diagnostics import EngineError
from standards_verifier.engine import Verifier


class SourceIndexClosureTest(unittest.TestCase):
    def write(self, root: Path, path: str, content: str) -> None:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def build_repository(
        self,
        root: Path,
        *,
        fixture_root: str = "fixtures/source-closure",
        extra_config: str = "",
    ) -> None:
        self.write(
            root,
            "registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "source-index"
            path = "suite.toml"
            requires = []
            """,
        )
        self.write(
            root,
            "suite.toml",
            f"""
            schema_version = 1
            id = "source-index"
            owner = "test.owner"
            description = "Source-index closure"

            [[checks]]
            id = "closure"
            type = "source_index_closure"
            fixture_root = {fixture_root!r}
            manifest_path = "manifest.tsv"
            corpus_path = "corpus.tsv"
            owner_map_path = "owner-map.tsv"
            dispositions_path = "dispositions.tsv"
            router_path = "ROUTER.md"
            {extra_config}
            """,
        )
        self.write(root, "OWNER.md", "# Owner\n")
        self.write(root, "ROUTER.md", "# Router\n\nCanonical routes only.\n")
        self.write(
            root,
            "legacy/INDEX.md",
            """
            # Legacy Index

            This index provides non-normative navigation and owns no policy.
            It has no fallback authority. Use the Router's typed selection
            instead of using prior wording.

            ## Routes

            - [Owner](../OWNER.md)
            """,
        )
        self.write(
            root,
            "manifest.tsv",
            """
            order\tsource\tcanonical_owner\tcurrent_shape\ttreatment\tretention_evidence\trisk\tconcurrency\tgate
            1\tlegacy/INDEX.md\tOWNER.md\tconcise\tretain-index\tfrozen\tmechanical\tisolated\tfull
            """,
        )
        self.write(
            root,
            "corpus.tsv",
            """
            path\tkind\tnormative\ttarget_role\tpreliminary_disposition\tbaseline_source
            legacy/INDEX.md\tstandard\tderived\tindex\tretain\tlegacy
            """,
        )
        self.write(
            root,
            "owner-map.tsv",
            """
            id\tcurrent_path\tline\tfuture_owner\tdisposition\theading
            STD-1\tlegacy/INDEX.md\t1\tOWNER.md\tindex\tOne
            STD-2\tlegacy/INDEX.md\t2\tOWNER.md\tindex\tTwo
            """,
        )
        self.write(
            root,
            "dispositions.tsv",
            """
            id\tsource\ttarget\tdisposition\trationale
            STD-1\tlegacy/INDEX.md\tOWNER.md\tindex\tone
            STD-2\tlegacy/INDEX.md\tOWNER.md\tindex\ttwo
            """,
        )
        fixture = "fixtures/source-closure/legacy"
        self.write(
            root,
            f"{fixture}/contract.tsv",
            """
            field\tvalue
            source\tlegacy/INDEX.md
            title\t# Legacy Index
            max_lines\t20
            """,
        )
        self.write(
            root,
            f"{fixture}/headings.tsv",
            """
            heading
            # Legacy Index
            ## Routes
            """,
        )
        self.write(
            root,
            f"{fixture}/routes.tsv",
            """
            route\ttarget\thref
            owner\tOWNER.md\t../OWNER.md
            """,
        )
        self.write(
            root,
            f"{fixture}/prohibited.tsv",
            """
            literal
            old authority
            """,
        )

    def run_check(self, root: Path):
        return Verifier(root, "registry.toml").run()[0]

    def test_valid_nested_source_and_exact_identifier_membership_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.build_repository(root)
            result = self.run_check(root)

        self.assertEqual(result.status, "passed")
        self.assertEqual(result.check_count, 1)
        self.assertEqual(result.diagnostics, [])

    def test_existing_contract_failures_are_typed(self) -> None:
        cases = {
            "loose-entry": ("SOURCE_INDEX.UNREGISTERED_ENTRY", 2),
            "partial-fixture": ("SOURCE_INDEX.FIXTURE_SHAPE", 2),
            "contract-header": ("TABLE.HEADER_CONTRACT", 2),
            "contract-field": ("SOURCE_INDEX.CONTRACT_FIELDS", 2),
            "line-value": ("SOURCE_INDEX.INVALID_LINE_BUDGET", 2),
            "absent-manifest": ("ASSERT.SOURCE_INDEX_MEMBERSHIP", 1),
            "normative-corpus": ("ASSERT.SOURCE_INDEX_CORPUS", 1),
            "heading-drift": ("ASSERT.SOURCE_INDEX_HEADINGS", 1),
            "line-budget": ("ASSERT.SOURCE_INDEX_LINE_BUDGET", 1),
            "duplicate-route": ("TABLE.DUPLICATE_VALUE", 2),
            "unresolved-target": ("INPUT.UNAVAILABLE", 3),
            "mismatched-href": ("ASSERT.SOURCE_INDEX_ROUTE", 1),
            "escaping-href": ("PATH.OUTSIDE_REPOSITORY", 2),
            "absent-href": ("ASSERT.SOURCE_INDEX_ROUTE", 1),
            "legacy-authority": ("ASSERT.SOURCE_INDEX_PROHIBITED", 1),
            "missing-non-authority": ("ASSERT.SOURCE_INDEX_NON_AUTHORITY", 1),
            "identifier-disagreement": ("ASSERT.SOURCE_INDEX_IDENTIFIERS", 1),
            "duplicate-identifier": ("TABLE.DUPLICATE_KEY", 2),
            "router-selection": ("ASSERT.SOURCE_INDEX_ROUTER", 1),
        }
        for mutation, (expected_code, expected_exit) in cases.items():
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.build_repository(root)
                self.apply_mutation(root, mutation)
                result = self.run_check(root)

                self.assertEqual(result.status, "failed")
                self.assertEqual(result.diagnostics[0].code, expected_code)
                self.assertEqual(result.exit_code, expected_exit)

    def apply_mutation(self, root: Path, mutation: str) -> None:
        fixture = root / "fixtures/source-closure/legacy"
        source = root / "legacy/INDEX.md"
        if mutation == "loose-entry":
            self.write(root, "fixtures/source-closure/loose.tsv", "value\n")
        elif mutation == "partial-fixture":
            (fixture / "headings.tsv").unlink()
        elif mutation == "contract-header":
            (fixture / "contract.tsv").write_text("name\tvalue\n", encoding="utf-8")
        elif mutation == "contract-field":
            contract = (fixture / "contract.tsv").read_text(encoding="utf-8")
            (fixture / "contract.tsv").write_text(
                contract.replace("title\t# Legacy Index\n", ""), encoding="utf-8"
            )
        elif mutation == "line-value":
            contract = (fixture / "contract.tsv").read_text(encoding="utf-8")
            (fixture / "contract.tsv").write_text(
                contract.replace("max_lines\t20", "max_lines\t0"), encoding="utf-8"
            )
        elif mutation == "absent-manifest":
            (root / "manifest.tsv").write_text(
                "\t".join(
                    (
                        "order",
                        "source",
                        "canonical_owner",
                        "current_shape",
                        "treatment",
                        "retention_evidence",
                        "risk",
                        "concurrency",
                        "gate",
                    )
                )
                + "\n",
                encoding="utf-8",
            )
        elif mutation == "normative-corpus":
            content = (root / "corpus.tsv").read_text(encoding="utf-8")
            (root / "corpus.tsv").write_text(
                content.replace("\tderived\t", "\tyes\t"), encoding="utf-8"
            )
        elif mutation == "heading-drift":
            source.write_text(
                source.read_text(encoding="utf-8").replace("## Routes", "## Changed"),
                encoding="utf-8",
            )
        elif mutation == "line-budget":
            contract = (fixture / "contract.tsv").read_text(encoding="utf-8")
            (fixture / "contract.tsv").write_text(
                contract.replace("max_lines\t20", "max_lines\t3"), encoding="utf-8"
            )
        elif mutation == "duplicate-route":
            with (fixture / "routes.tsv").open("a", encoding="utf-8") as handle:
                handle.write("owner-copy\tOWNER.md\t../OWNER-copy.md\n")
        elif mutation == "unresolved-target":
            content = (fixture / "routes.tsv").read_text(encoding="utf-8")
            (fixture / "routes.tsv").write_text(
                content.replace("OWNER.md", "ABSENT.md"), encoding="utf-8"
            )
        elif mutation == "mismatched-href":
            self.write(root, "OTHER.md", "# Other\n")
            content = (fixture / "routes.tsv").read_text(encoding="utf-8")
            (fixture / "routes.tsv").write_text(
                content.replace("../OWNER.md", "../OTHER.md"), encoding="utf-8"
            )
        elif mutation == "escaping-href":
            content = (fixture / "routes.tsv").read_text(encoding="utf-8")
            (fixture / "routes.tsv").write_text(
                content.replace("../OWNER.md", "../../outside.md"), encoding="utf-8"
            )
        elif mutation == "absent-href":
            source.write_text(
                source.read_text(encoding="utf-8").replace(
                    "[Owner](../OWNER.md)", "Owner"
                ),
                encoding="utf-8",
            )
        elif mutation == "legacy-authority":
            with source.open("a", encoding="utf-8") as handle:
                handle.write("old authority\n")
        elif mutation == "missing-non-authority":
            source.write_text(
                source.read_text(encoding="utf-8").replace("owns no", "contains no"),
                encoding="utf-8",
            )
        elif mutation == "identifier-disagreement":
            content = (root / "dispositions.tsv").read_text(encoding="utf-8")
            (root / "dispositions.tsv").write_text(
                content.replace("STD-2\t", "STD-3\t"), encoding="utf-8"
            )
        elif mutation == "duplicate-identifier":
            with (root / "owner-map.tsv").open("a", encoding="utf-8") as handle:
                handle.write("STD-1\tlegacy/INDEX.md\t3\tOWNER.md\tindex\tThree\n")
        elif mutation == "router-selection":
            with (root / "ROUTER.md").open("a", encoding="utf-8") as handle:
                handle.write("legacy/INDEX.md\n")
        else:
            self.fail(f"unknown mutation: {mutation}")

    def test_duplicate_source_registration_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.build_repository(root)
            shutil.copytree(
                root / "fixtures/source-closure/legacy",
                root / "fixtures/source-closure/second",
            )
            result = self.run_check(root)

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.diagnostics[0].code, "SOURCE_INDEX.DUPLICATE_SOURCE")

    def test_configuration_is_exact_and_repository_contained(self) -> None:
        for fixture_root, extra, expected_code in (
            ("fixtures/source-closure", 'command = "bash"', "CONFIG.UNKNOWN_FIELD"),
            ("../outside", "", "PATH.OUTSIDE_REPOSITORY"),
        ):
            with self.subTest(
                fixture_root=fixture_root, extra=extra
            ), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.build_repository(
                    root, fixture_root=fixture_root, extra_config=extra
                )
                with self.assertRaises(EngineError) as raised:
                    Verifier(root, "registry.toml")

                self.assertEqual(raised.exception.diagnostic.code, expected_code)


if __name__ == "__main__":
    unittest.main()
