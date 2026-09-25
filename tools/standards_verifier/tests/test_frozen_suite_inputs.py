"""Filesystem/frozen input parity at the canonical manifest compiler boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_metadata.standards_metadata import FrozenContentSource
from standards_verifier.diagnostics import EngineError
from standards_verifier.model import absent_inputs, present_inputs
from standards_verifier.suite_inputs import (
    suite_input_projection_bytes,
    suite_input_projection_bytes_from_content,
)

REGISTRY = "evaluation/standards-effectiveness/suite-registry.toml"
SUITE = "evaluation/standards-effectiveness/suites/example.toml"


class FrozenSuiteInputsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write(REGISTRY, f'schema_version = 1\n[[suites]]\nid="example"\npath="{SUITE}"\nrequires=[]\n')
        self.write(SUITE, 'schema_version=1\nid="example"\nowner="test"\ndescription="fixture"\n'
                         '[[checks]]\nid="links"\ntype="markdown_links"\npaths=["docs/readme.md"]\n')
        self.write("docs/readme.md", "[Target](../target.md#part)\n[Local](#heading)\n")
        self.write("target.md", "# Part\n")
        self.write("uncaptured.txt", "Membership is distinct from input content.\n")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "--all"], cwd=self.root, check=True)

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content.encode() if isinstance(content, str) else content)

    def population(self):
        return tuple(subprocess.check_output(["git", "ls-files", "-z"], cwd=self.root).decode().rstrip("\0").split("\0"))

    def files(self):
        return {p: (self.root / p).read_bytes() for p in self.population() if (self.root / p).is_file()}

    def frozen(self, files=None, paths=None):
        return suite_input_projection_bytes_from_content(
            FrozenContentSource(self.files() if files is None else files),
            repository_paths=self.population() if paths is None else paths,
        )

    def failure(self, action):
        with self.assertRaises(EngineError) as caught:
            action()
        return caught.exception.diagnostic

    def test_filesystem_and_frozen_have_exact_bytes_without_filesystem_work(self):
        expected = suite_input_projection_bytes(self.root)
        files = self.files()
        # The indexed but unused file is genuinely absent from captured content.
        files.pop("uncaptured.txt")
        source = FrozenContentSource(files)
        paths = self.population()
        with patch("pathlib.Path.read_bytes", side_effect=AssertionError("filesystem read")), \
             patch("subprocess.run", side_effect=AssertionError("child process")), \
             patch("pathlib.Path.exists", side_effect=AssertionError("ambient membership")), \
             patch("tempfile.TemporaryDirectory", side_effect=AssertionError("staging")):
            actual = suite_input_projection_bytes_from_content(source, repository_paths=paths)
        self.assertEqual(actual, expected)

    def test_repository_corpus_covers_all_real_check_declarations(self):
        root = Path(__file__).resolve().parents[3]
        expected = suite_input_projection_bytes(root)
        projection = json.loads(expected)
        paths = tuple(subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().rstrip("\0").split("\0"))
        required = {projection["registry"]["path"], *(x["path"] for x in projection["suites"]),
                    *(x["path"] for x in projection["files"] if x["state"] == "present")}
        files = {p: (root / p).read_bytes() for p in required}
        actual = suite_input_projection_bytes_from_content(FrozenContentSource(files), repository_paths=paths)
        self.assertEqual(actual, expected)

    def test_index_membership_does_not_supply_missing_content(self):
        files = self.files()
        files.pop("target.md")
        diagnostic = self.failure(lambda: self.frozen(files))
        self.assertEqual((diagnostic.code, diagnostic.outcome, diagnostic.path),
                         ("INPUT.UNAVAILABLE", "unavailable", "target.md"))
        self.assertIn("not captured", diagnostic.message)

    def test_empty_content_remains_present_and_hashed(self):
        self.write("target.md", b"")
        result = json.loads(self.frozen())
        target = next(x for x in result["files"] if x["path"] == "target.md")
        self.assertEqual(target["digest"], "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
        self.assertEqual(self.frozen(), suite_input_projection_bytes(self.root))

    def test_invalid_configuration_preserves_diagnostic(self):
        for content, code in (("broken = [", "CONFIG.INVALID_TOML"),
                              ('schema_version=2\nsuites=[]\n', "CONFIG.SCHEMA_VERSION")):
            self.write(REGISTRY, content)
            physical = self.failure(lambda: suite_input_projection_bytes(self.root))
            frozen = self.failure(self.frozen)
            self.assertEqual(physical, frozen)
            self.assertEqual(physical.code, code)

    def test_markdown_newline_and_utf8_semantics_are_preserved(self):
        target = "target\nname.md"
        self.write(target, "# Target\n")
        subprocess.run(["git", "add", "--", target], cwd=self.root, check=True)
        for newline in ("\r\n", "\r", "\n"):
            self.write("docs/readme.md", "[Target](../target" + newline + "name.md)")
            frozen = self.frozen()
            self.assertEqual(frozen, suite_input_projection_bytes(self.root))
            self.assertIn(target, {item["path"] for item in json.loads(frozen)["files"]})
        self.write("docs/readme.md", b"\xff")
        physical = self.failure(lambda: suite_input_projection_bytes(self.root))
        frozen = self.failure(self.frozen)
        self.assertEqual(physical, frozen)
        self.assertEqual(frozen.code, "INPUT.INVALID_UTF8")

    def test_escaping_links_preserve_diagnostics(self):
        for link in ("../../outside.md", "/absolute.md"):
            self.write("docs/readme.md", f"[Outside]({link})")
            physical = self.failure(lambda: suite_input_projection_bytes(self.root))
            frozen = self.failure(self.frozen)
            self.assertEqual(physical, frozen)
            self.assertEqual(frozen.code, "PATH.LINK_OUTSIDE_REPOSITORY")

    def test_directory_and_missing_inputs_preserve_classification(self):
        for link, code in (("../docs", "INPUT.NOT_FILE"), ("../missing", "INPUT.UNAVAILABLE")):
            self.write("docs/readme.md", f"[Target]({link})")
            physical = self.failure(lambda: suite_input_projection_bytes(self.root))
            frozen = self.failure(self.frozen)
            self.assertEqual((physical.code, physical.path, physical.outcome),
                             (frozen.code, frozen.path, frozen.outcome))
            self.assertEqual(frozen.code, code)

    def test_absence_and_contradictory_declarations_are_shared(self):
        from standards_verifier.checks.markdown_links import MarkdownLinksCheck
        for declarations, code in ((absent_inputs("required", "uncaptured.txt"), "INPUT.EXPECTED_ABSENT"),
                                   ((*present_inputs("a", "target.md"), *absent_inputs("b", "target.md")), "INPUT.CONTRADICTORY_STATE")):
            with patch.object(MarkdownLinksCheck, "authority_inputs", return_value=declarations):
                physical = self.failure(lambda: suite_input_projection_bytes(self.root))
                frozen = self.failure(self.frozen)
            self.assertEqual(physical, frozen)
            self.assertEqual(frozen.code, code)

    def test_frozen_source_and_index_stay_independent_of_current_files(self):
        source = FrozenContentSource(self.files())
        paths = self.population()
        expected = suite_input_projection_bytes_from_content(source, repository_paths=paths)
        self.write("target.md", "Changed ambient bytes")
        self.assertEqual(suite_input_projection_bytes_from_content(source, repository_paths=paths), expected)
        self.assertNotEqual(suite_input_projection_bytes(self.root), expected)

    def test_rejects_invalid_or_contradictory_membership(self):
        files = self.files()
        for paths, code in (([*self.population(), self.population()[0]], "INPUT.INVALID_REPOSITORY_PATHS"),
                            ([*self.population(), "../escape"], "INPUT.INVALID_REPOSITORY_PATH"),
                            ([*self.population(), "docs"], "INPUT.CONTRADICTORY_MEMBERSHIP"),
                            ([p for p in self.population() if p != "target.md"], "INPUT.CONTRADICTORY_MEMBERSHIP")):
            self.assertEqual(self.failure(lambda: self.frozen(files, paths)).code, code)

    def test_physical_symlink_checks_remain_at_filesystem_boundary(self):
        outside = self.root.parent / (self.root.name + "-outside")
        outside.write_text("private")
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        (self.root / "escape.md").symlink_to(outside)
        self.write("docs/readme.md", "[Escape](../escape.md)")
        diagnostic = self.failure(lambda: suite_input_projection_bytes(self.root))
        self.assertEqual(diagnostic.code, "PATH.LINK_OUTSIDE_REPOSITORY")
