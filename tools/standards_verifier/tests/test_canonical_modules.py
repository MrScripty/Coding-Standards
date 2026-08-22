from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.canonical_modules import load_canonical_module_corpus
from standards_verifier.diagnostics import EngineError


class CanonicalModuleCorpusTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    @staticmethod
    def relation(values: tuple[str, ...]) -> str:
        return "`none`" if not values else ", ".join(f"`{item}`" for item in values)

    def write_module(
        self,
        path: str,
        module_id: str,
        *,
        role: str = "workflow",
        requires: tuple[str, ...] = (),
        specializes: tuple[str, ...] = (),
        owner: str | None = None,
    ) -> None:
        level = {"core": "MUST", "profile": "PROFILE", "reference": "REFERENCE"}.get(
            role,
            "MUST",
        )
        self.write(
            path,
            f"""
            # Canonical module

            **Standards metadata**

            - ID: `{module_id}`
            - Role: `{role}`
            - Level: `{level}`
            - Applies when: The fixture applies.
            - Does not apply when: The fixture does not apply.
            - Requires: {self.relation(requires)}
            - Specializes: {self.relation(specializes)}
            - Verification: Focused corpus evidence.
            - Canonical owner: `{owner or path}`
            """,
        )

    def write_manifest(
        self,
        members: tuple[str, ...],
        *,
        prefix: str = "schema_version = 1",
    ) -> None:
        encoded = ", ".join(f'"{member}"' for member in members)
        self.write("corpus.toml", f"{prefix}\nmembers = [{encoded}]\n")

    def error_code(self) -> str:
        with self.assertRaises(EngineError) as caught:
            load_canonical_module_corpus(self.root, "corpus.toml")
        return caught.exception.diagnostic.code

    def test_loads_without_suite_registry_and_derives_normative_membership(self) -> None:
        self.write_module("core.md", "core", role="core")
        self.write_module("workflow.md", "workflow.example", requires=("core",))
        self.write_module("reference.md", "reference.example", role="reference")
        self.write_manifest(("core.md", "reference.md", "workflow.md"))

        corpus = load_canonical_module_corpus(self.root, "corpus.toml")

        self.assertEqual(tuple(module.path for module in corpus.modules), corpus.members)
        self.assertEqual(
            tuple(module.module_id for module in corpus.normative_modules),
            ("core", "workflow.example"),
        )

    def test_manifest_schema_is_strict_and_members_are_non_empty_unique_paths(self) -> None:
        cases = (
            ("schema_version = 2", ("module.md",), "CONFIG.SCHEMA_VERSION"),
            ("schema_version = 1\nextra = true", ("module.md",), "CONFIG.CANONICAL_CORPUS_FIELDS"),
            ("schema_version = 1", (), "CONFIG.CANONICAL_CORPUS_MEMBERS"),
            ("schema_version = 1", ("module.md", "module.md"), "CONFIG.CANONICAL_CORPUS_DUPLICATE"),
            ("schema_version = 1", ("./module.md",), "PATH.OUTSIDE_REPOSITORY"),
            ("schema_version = 1", ("../module.md",), "PATH.OUTSIDE_REPOSITORY"),
        )
        self.write_module("module.md", "module")
        for prefix, members, expected in cases:
            with self.subTest(expected=expected):
                self.write_manifest(members, prefix=prefix)
                self.assertEqual(self.error_code(), expected)

    def test_malformed_manifest_and_missing_member_are_typed(self) -> None:
        self.write("corpus.toml", "schema_version = [\n")
        self.assertEqual(self.error_code(), "CONFIG.INVALID_TOML")

        self.write_manifest(("missing.md",))
        self.assertEqual(self.error_code(), "INPUT.UNAVAILABLE")

    def test_member_symlink_cannot_escape_repository(self) -> None:
        outside = self.root.with_name(f"{self.root.name}-outside.md")
        outside.write_text("outside\n", encoding="utf-8")
        self.addCleanup(outside.unlink, missing_ok=True)
        (self.root / "linked.md").symlink_to(outside)
        self.write_manifest(("linked.md",))

        self.assertEqual(self.error_code(), "PATH.OUTSIDE_REPOSITORY")

    def test_metadata_identity_and_relation_failures_are_not_hidden(self) -> None:
        self.write_module("a.md", "duplicate")
        self.write_module("b.md", "duplicate")
        self.write_manifest(("a.md", "b.md"))
        self.assertEqual(self.error_code(), "METADATA.DUPLICATE_ID")

        self.write_module("a.md", "a", requires=("missing",))
        self.write_manifest(("a.md",))
        self.assertEqual(self.error_code(), "METADATA.UNRESOLVED_TARGET")

        self.write_module("a.md", "a", requires=("b",))
        self.write_module("b.md", "b", requires=("a",))
        self.write_manifest(("a.md", "b.md"))
        self.assertEqual(self.error_code(), "METADATA.REQUIRES_CYCLE")

        self.write_module("a.md", "a", owner="other.md")
        self.write_manifest(("a.md",))
        self.assertEqual(self.error_code(), "METADATA.CANONICAL_OWNER")


if __name__ == "__main__":
    unittest.main()
