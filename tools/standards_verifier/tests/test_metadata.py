from __future__ import annotations

import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.diagnostics import EngineError
from standards_verifier.engine import Verifier
from standards_verifier.graph_adapters import (
    METADATA_DEPENDENCIES,
    metadata_dependency_registry,
)
from standards_verifier.checks.metadata import load_module_metadata


class MetadataGraphTest(unittest.TestCase):
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
        if not values:
            return "`none`"
        return ", ".join(f"`{value}`" for value in values)

    def write_module(
        self,
        path: str,
        *,
        module_id: str,
        role: str = "workflow",
        level: str = "MUST",
        requires: tuple[str, ...] = (),
        specializes: tuple[str, ...] = (),
        applies: str = "The metadata graph is selected.",
        excludes: str = "The metadata graph is not selected.",
        verification: str = "Focused `metadata_graph` evidence.",
        owner: str | None = None,
        raw: dict[str, str] | None = None,
        omit: str | None = None,
        duplicate: str | None = None,
    ) -> None:
        values = {
            "ID": f"`{module_id}`",
            "Role": f"`{role}`",
            "Level": f"`{level}`",
            "Applies when": applies,
            "Does not apply when": excludes,
            "Requires": self.relation(requires),
            "Specializes": self.relation(specializes),
            "Verification": verification,
            "Canonical owner": f"`{owner or path}`",
        }
        values.update(raw or {})
        lines = ["# Fixture", "", "**Standards metadata**", ""]
        for field, value in values.items():
            if field != omit:
                separator = " " if value else ""
                lines.append(f"- {field}:{separator}{value}")
                if field == duplicate:
                    lines.append(f"- {field}:{separator}{value}")
        self.write(path, "\n".join(lines) + "\n")

    def write_registry(self) -> None:
        self.write(
            "registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "metadata"
            path = "suite.toml"
            requires = []
            """,
        )

    def write_direct_suite(self, paths: tuple[str, ...]) -> None:
        encoded = ", ".join(json.dumps(path) for path in paths)
        self.write(
            "suite.toml",
            f"""
            schema_version = 1
            id = "metadata"
            owner = "metadata.schema"
            description = "Metadata graph"

            [[checks]]
            id = "graph"
            type = "metadata_graph"
            paths = [{encoded}]
            """,
        )
        self.write_registry()

    def result(self, paths: tuple[str, ...]):
        self.write_direct_suite(paths)
        return Verifier(self.root, "registry.toml").run(("metadata",))[0]

    def codes(self, paths: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(item.code for item in self.result(paths).diagnostics)

    def test_valid_module_and_profile_graph_passes(self) -> None:
        self.write_module("core.md", module_id="core", role="core")
        self.write_module(
            "profile.md",
            module_id="profile.test",
            role="profile",
            level="PROFILE",
            requires=("core",),
            specializes=("core",),
            verification="Evidence preserves embedded `inline code`.",
        )

        self.assertEqual(self.result(("core.md", "profile.md")).status, "passed")

    def test_metadata_adapter_resolves_ids_paths_and_named_groups(self) -> None:
        self.write_module("core.md", module_id="core", role="core")
        self.write_module(
            "profile.md",
            module_id="profile.test",
            role="profile",
            level="PROFILE",
            requires=("core",),
        )
        modules = tuple(
            load_module_metadata(self.root, path, suite="metadata", check="graph")
            for path in ("core.md", "profile.md")
        )

        graph = metadata_dependency_registry(self.root, modules)

        self.assertEqual(graph.resolve("profile.md"), "profile.test")
        self.assertEqual(
            tuple(edge.relation for edge in graph.edges_for_group(METADATA_DEPENDENCIES)),
            ("requires",),
        )

    def test_field_count_is_exact(self) -> None:
        self.write_module("missing.md", module_id="missing", omit="Verification")
        self.assertEqual(
            self.codes(("missing.md",)),
            ("METADATA.FIELD_COUNT",),
        )
        self.write_module(
            "duplicate.md",
            module_id="duplicate",
            duplicate="Verification",
        )
        self.assertEqual(
            self.codes(("duplicate.md",)),
            ("METADATA.FIELD_COUNT",),
        )

    def test_symbolic_values_require_one_backticked_token(self) -> None:
        self.write_module(
            "module.md",
            module_id="module",
            raw={"ID": "module"},
        )
        self.assertEqual(
            self.codes(("module.md",)),
            ("METADATA.SYMBOLIC_FORMAT",),
        )

    def test_prose_is_preserved_and_must_not_be_empty(self) -> None:
        self.write_module(
            "module.md",
            module_id="module",
            raw={"Verification": ""},
        )
        self.assertEqual(
            self.codes(("module.md",)),
            ("METADATA.PROSE_EMPTY",),
        )

    def test_relation_grammar_rejects_empty_and_mixed_none_items(self) -> None:
        for value in (
            "`core`, , `other`",
            "`none`, `core`",
            "`Invalid`",
        ):
            with self.subTest(value=value):
                self.write_module(
                    "module.md",
                    module_id="module",
                    raw={"Requires": value},
                )
                self.assertEqual(
                    self.codes(("module.md",)),
                    ("METADATA.RELATION_FORMAT",),
                )

    def test_relation_targets_must_be_unique(self) -> None:
        self.write_module(
            "module.md",
            module_id="module",
            raw={"Requires": "`core`, `core`"},
        )
        self.assertEqual(
            self.codes(("module.md",)),
            ("METADATA.RELATION_DUPLICATE",),
        )

    def test_module_id_role_and_level_domains_are_typed(self) -> None:
        cases = (
            ({"ID": "`Invalid`"}, "METADATA.ID_FORMAT"),
            ({"Role": "`unknown`"}, "METADATA.ROLE"),
            ({"Level": "`MANDATORY`"}, "METADATA.LEVEL"),
        )
        for raw, expected in cases:
            with self.subTest(expected=expected):
                self.write_module("module.md", module_id="module", raw=raw)
                self.assertEqual(self.codes(("module.md",)), (expected,))

    def test_role_specific_level_is_enforced(self) -> None:
        self.write_module(
            "module.md",
            module_id="profile.test",
            role="profile",
            level="MUST",
        )
        self.assertEqual(
            self.codes(("module.md",)),
            ("METADATA.ROLE_LEVEL",),
        )

    def test_canonical_owner_must_equal_normalized_path(self) -> None:
        self.write_module(
            "module.md",
            module_id="module",
            owner="./module.md",
        )
        self.assertEqual(
            self.codes(("module.md",)),
            ("METADATA.CANONICAL_OWNER",),
        )

    def test_self_edges_and_specialization_role_are_rejected(self) -> None:
        self.write_module(
            "self.md",
            module_id="self",
            requires=("self",),
        )
        self.assertEqual(self.codes(("self.md",)), ("METADATA.SELF_EDGE",))
        self.write_module("core.md", module_id="core", role="core")
        self.write_module(
            "workflow.md",
            module_id="workflow.test",
            specializes=("core",),
        )
        self.assertEqual(
            self.codes(("core.md", "workflow.md")),
            ("METADATA.SPECIALIZATION_ROLE",),
        )

    def test_applicability_and_exclusion_cannot_both_be_none(self) -> None:
        self.write_module(
            "module.md",
            module_id="module",
            applies="none",
            excludes="none",
        )
        self.assertEqual(
            self.codes(("module.md",)),
            ("METADATA.APPLICABILITY",),
        )

    def test_duplicate_module_ids_are_rejected(self) -> None:
        self.write_module("a.md", module_id="duplicate")
        self.write_module("b.md", module_id="duplicate")
        self.assertEqual(
            self.codes(("a.md", "b.md")),
            ("METADATA.DUPLICATE_ID",),
        )

    def test_unresolved_targets_are_rejected(self) -> None:
        self.write_module(
            "module.md",
            module_id="module",
            requires=("missing",),
        )
        self.assertEqual(
            self.codes(("module.md",)),
            ("METADATA.UNRESOLVED_TARGET",),
        )

    def test_requires_cycle_and_combined_cycle_are_reported(self) -> None:
        self.write_module("a.md", module_id="a", requires=("b",))
        self.write_module("b.md", module_id="b", requires=("a",))
        self.assertEqual(
            self.codes(("a.md", "b.md")),
            ("METADATA.REQUIRES_CYCLE", "METADATA.COMBINED_CYCLE"),
        )

    def test_specialization_cycle_and_combined_cycle_are_reported(self) -> None:
        self.write_module(
            "a.md",
            module_id="profile.a",
            role="profile",
            level="PROFILE",
            specializes=("profile.b",),
        )
        self.write_module(
            "b.md",
            module_id="profile.b",
            role="profile",
            level="PROFILE",
            specializes=("profile.a",),
        )
        self.assertEqual(
            self.codes(("a.md", "b.md")),
            ("METADATA.SPECIALIZES_CYCLE", "METADATA.COMBINED_CYCLE"),
        )

    def test_cross_relation_cycle_is_reported(self) -> None:
        self.write_module(
            "a.md",
            module_id="profile.a",
            role="profile",
            level="PROFILE",
            requires=("profile.b",),
        )
        self.write_module(
            "b.md",
            module_id="profile.b",
            role="profile",
            level="PROFILE",
            specializes=("profile.a",),
        )
        self.assertEqual(
            self.codes(("a.md", "b.md")),
            ("METADATA.COMBINED_CYCLE",),
        )

    def test_missing_input_is_unavailable(self) -> None:
        result = self.result(("missing.md",))
        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_fixture_corpus_compares_exact_diagnostic_sequences(self) -> None:
        self.write_module("valid.md", module_id="valid")
        self.write_module(
            "invalid.md",
            module_id="invalid",
            raw={"Level": "`MANDATORY`"},
        )
        self.write(
            "suite.toml",
            """
            schema_version = 1
            id = "metadata"
            owner = "metadata.schema"
            description = "Metadata fixtures"

            [[checks]]
            id = "fixtures"
            type = "metadata_graph"
            cases = [
              { id = "valid", paths = ["valid.md"], expected = [] },
              { id = "invalid", paths = ["invalid.md"], expected = ["METADATA.LEVEL"] },
            ]
            """,
        )
        self.write_registry()

        result = Verifier(self.root, "registry.toml").run(("metadata",))[0]

        self.assertEqual(result.status, "passed")

    def test_fixture_corpus_mismatch_is_typed(self) -> None:
        self.write_module("valid.md", module_id="valid")
        self.write(
            "suite.toml",
            """
            schema_version = 1
            id = "metadata"
            owner = "metadata.schema"
            description = "Metadata fixtures"

            [[checks]]
            id = "fixtures"
            type = "metadata_graph"
            cases = [
              { id = "wrong", paths = ["valid.md"], expected = ["METADATA.LEVEL"] },
            ]
            """,
        )
        self.write_registry()

        result = Verifier(self.root, "registry.toml").run(("metadata",))[0]

        self.assertEqual(
            result.diagnostics[0].code,
            "ASSERT.METADATA_FIXTURE",
        )

    def test_config_requires_exactly_one_mode(self) -> None:
        self.write(
            "suite.toml",
            """
            schema_version = 1
            id = "metadata"
            owner = "metadata.schema"
            description = "Metadata graph"

            [[checks]]
            id = "graph"
            type = "metadata_graph"
            """,
        )
        self.write_registry()

        with self.assertRaisesRegex(EngineError, "exactly one"):
            Verifier(self.root, "registry.toml").run()


if __name__ == "__main__":
    unittest.main()
