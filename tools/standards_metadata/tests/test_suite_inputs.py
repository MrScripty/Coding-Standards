from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from tools.standards_metadata.standards_metadata import (
    MetadataError,
    RepositoryIndexObservation,
    SuiteDefinitionInput,
    SuiteFileInput,
    SuiteInputManifest,
    SuiteInputUse,
    file_digest,
    load_suite_input_manifest,
    suite_input_manifest_bytes,
)


class SuiteInputManifestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.write(
            "registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "base"
            path = "suites/base.toml"
            requires = []

            [[suites]]
            id = "selected"
            path = "suites/selected.toml"
            requires = ["base"]

            [[suites]]
            id = "unrelated"
            path = "suites/unrelated.toml"
            requires = []
            """,
        )
        for suite_id in ("base", "selected", "unrelated"):
            self.write(
                f"suites/{suite_id}.toml",
                f"""
                schema_version = 1
                id = "{suite_id}"
                owner = "test"
                description = "{suite_id} fixture."
                checks = [{{ id = "fixture", type = "text" }}]
                """,
            )
            self.write(f"inputs/{suite_id}.txt", f"{suite_id}\n")
        self.write_manifest()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def manifest(self) -> SuiteInputManifest:
        definitions = tuple(
            SuiteDefinitionInput(
                suite_id,
                f"suites/{suite_id}.toml",
                file_digest((self.root / f"suites/{suite_id}.toml").read_bytes()),
                ("base",) if suite_id == "selected" else (),
            )
            for suite_id in ("base", "selected", "unrelated")
        )
        files = tuple(
            SuiteFileInput(
                f"inputs/{suite_id}.txt",
                "present",
                file_digest((self.root / f"inputs/{suite_id}.txt").read_bytes()),
                (SuiteInputUse(suite_id, "fixture", "content"),),
            )
            for suite_id in ("base", "selected", "unrelated")
        )
        return SuiteInputManifest(
            "registry.toml",
            file_digest((self.root / "registry.toml").read_bytes()),
            definitions,
            files,
            RepositoryIndexObservation(
                "sha256:" + "1" * 64,
                (SuiteInputUse("unrelated", "fixture", "repository-index"),),
            ),
        )

    def write_manifest(self) -> None:
        (self.root / "suite-inputs.json").write_bytes(
            suite_input_manifest_bytes(self.manifest())
        )

    def test_loads_validated_manifest_and_derives_transitive_projection(self) -> None:
        manifest = load_suite_input_manifest(self.root, "suite-inputs.json")

        dependency = manifest.dependency("selected")

        self.assertEqual(dependency.suites, ("base", "selected"))
        self.assertEqual(
            dependency.files,
            ("inputs/base.txt", "inputs/selected.txt"),
        )
        self.assertFalse(dependency.observes_repository_index)

    def test_unrelated_suite_change_preserves_selected_fingerprint(self) -> None:
        first = load_suite_input_manifest(
            self.root, "suite-inputs.json"
        ).dependency("selected")
        self.write("inputs/unrelated.txt", "unrelated changed\n")
        self.write_manifest()

        second = load_suite_input_manifest(
            self.root, "suite-inputs.json"
        ).dependency("selected")

        self.assertEqual(first.fingerprint, second.fingerprint)

    def test_transitive_suite_change_updates_selected_fingerprint(self) -> None:
        first = load_suite_input_manifest(
            self.root, "suite-inputs.json"
        ).dependency("selected")
        self.write("inputs/base.txt", "base changed\n")
        self.write_manifest()

        second = load_suite_input_manifest(
            self.root, "suite-inputs.json"
        ).dependency("selected")

        self.assertNotEqual(first.fingerprint, second.fingerprint)

    def test_stale_input_is_rejected(self) -> None:
        self.write("inputs/selected.txt", "stale\n")

        with self.assertRaises(MetadataError) as caught:
            load_suite_input_manifest(self.root, "suite-inputs.json")

        self.assertEqual(caught.exception.failure.code, "SUITE_INPUT.STALE_FILE")

    def test_dependency_cycle_is_rejected(self) -> None:
        registry = (self.root / "registry.toml").read_text(encoding="utf-8")
        self.write("registry.toml", registry.replace('requires = []', 'requires = ["selected"]', 1))
        self.write_manifest()

        with self.assertRaises(MetadataError) as caught:
            load_suite_input_manifest(self.root, "suite-inputs.json")

        self.assertEqual(
            caught.exception.failure.code,
            "SUITE_INPUT.DEPENDENCY_CYCLE",
        )


if __name__ == "__main__":
    unittest.main()
