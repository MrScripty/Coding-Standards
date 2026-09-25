"""Preparation preserves the validated manifest's dependency and wire contracts."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError, replace
import hashlib
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.standards_metadata.standards_metadata.errors import MetadataError
from tools.standards_metadata.standards_metadata.source import FrozenContentSource
from tools.standards_metadata.standards_metadata import suite_inputs as inputs


def manifest_fixture(payload: bytes = b"shared input\n"):
    """A diamond prerequisite graph, overlapping uses, absence and index input."""
    requirements = {"common": (), "left": ("common",),
                    "right": ("common",), "top": ("left", "right"), "other": ()}
    files = {f"suites/{name}.toml": f'id = "{name}"\n'.encode()
             for name in requirements}
    registry = "schema_version = 1\n" + "".join(
        f'[[suites]]\nid = "{name}"\npath = "suites/{name}.toml"\n'
        f'requires = {json.dumps(list(required))}\n'
        for name, required in requirements.items()
    )
    files["registry.toml"] = registry.encode()
    files.update({"inputs/shared.txt": payload, "inputs/left.txt": b"left\n",
                  "inputs/other.txt": b"other\n"})
    use = inputs.SuiteInputUse
    declarations = (
        inputs.SuiteFileInput("inputs/absent.txt", "absent", None,
                             (use("top", "absent", "absence"),)),
        inputs.SuiteFileInput("inputs/left.txt", "present",
                             inputs.file_digest(files["inputs/left.txt"]),
                             (use("left", "left", "content"),)),
        inputs.SuiteFileInput("inputs/other.txt", "present",
                             inputs.file_digest(files["inputs/other.txt"]),
                             (use("other", "other", "content"),)),
        inputs.SuiteFileInput("inputs/shared.txt", "present", inputs.file_digest(payload),
                             (use("common", "shared", "content"),
                              use("right", "shared", "content"))),
    )
    manifest = inputs.SuiteInputManifest(
        "registry.toml", inputs.file_digest(files["registry.toml"]),
        tuple(inputs.SuiteDefinitionInput(name, f"suites/{name}.toml",
              inputs.file_digest(files[f"suites/{name}.toml"]), required)
              for name, required in requirements.items()),
        declarations,
        inputs.RepositoryIndexObservation(inputs.file_digest(b"membership"),
                                           (use("right", "index", "membership"),)),
    )
    files["manifest.json"] = inputs.suite_input_manifest_bytes(manifest)
    return files, manifest


def load_fixture(payload: bytes = b"shared input\n"):
    files, direct = manifest_fixture(payload)
    return inputs.load_suite_input_manifest(FrozenContentSource(files), "manifest.json"), direct


class PreparedSuiteDependenciesTest(unittest.TestCase):
    def test_diamond_projection_has_exact_files_uses_and_fingerprint(self):
        loaded, direct = load_fixture()
        result = loaded.dependency("top")
        selected = {"common", "left", "right", "top"}
        self.assertEqual(result.suites, tuple(sorted(selected)))
        self.assertEqual(result.files, ("inputs/absent.txt", "inputs/left.txt", "inputs/shared.txt"))
        self.assertTrue(result.observes_repository_index)
        # This ASCII-only fixture's literal JSON preimage independently specifies
        # the unchanged identity-v1 dependency shape, ordering and filtered uses.
        preimage = {
            "contract": inputs.SUITE_INPUT_CONTRACT, "schema_version": 1, "suite": "top",
            "suites": [entry.as_projection() for entry in sorted(direct.suites, key=lambda item: item.id)
                       if entry.id in selected],
            "files": [{"path": item.path, "state": item.state, "digest": item.digest,
                       "uses": [use.as_projection() for use in item.uses if use.suite in selected]}
                      for item in direct.files if any(use.suite in selected for use in item.uses)],
            "repository_index": direct.repository_index.as_projection(),
        }
        expected = "sha256:" + hashlib.sha256(
            json.dumps(preimage, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(result.fingerprint, expected)
        self.assertEqual(result, direct.dependency("top"))

    def test_loader_derives_each_suite_once_with_one_definition_table(self):
        files, direct = manifest_fixture()
        original = inputs.SuiteInputManifest._derive_dependency
        observations = []
        def observed(manifest, suite_id, definitions):
            observations.append((suite_id, definitions))
            return original(manifest, suite_id, definitions)
        with patch.object(inputs.SuiteInputManifest, "_derive_dependency", observed):
            loaded = inputs.load_suite_input_manifest(FrozenContentSource(files), "manifest.json")
            for _ in range(4):
                for definition in direct.suites:
                    loaded.dependency(definition.id)
        self.assertEqual([name for name, _ in observations], [item.id for item in direct.suites])
        self.assertEqual(len({id(table) for _, table in observations}), 1)

    def test_lookup_is_read_only_and_result_is_immutable(self):
        loaded, _ = load_fixture()
        selected = loaded.dependency("top")
        self.assertIs(loaded.dependency("top"), selected)
        with self.assertRaises(TypeError):
            loaded._dependencies["top"] = None
        with self.assertRaises(FrozenInstanceError):
            selected.fingerprint = "changed"
        with self.assertRaises(FrozenInstanceError):
            loaded._dependencies = {}

    def test_unknown_suite_preserves_key_error_without_growing_index(self):
        loaded, direct = load_fixture()
        keys = tuple(loaded._dependencies)
        for manifest in (loaded, direct):
            with self.assertRaises(KeyError) as error:
                manifest.dependency("missing")
            self.assertEqual(error.exception.args, ("missing",))
        self.assertEqual(tuple(loaded._dependencies), keys)

    def test_wire_equality_hash_and_representation_ignore_preparation(self):
        loaded, direct = load_fixture()
        self.assertEqual(inputs.suite_input_manifest_bytes(loaded), inputs.suite_input_manifest_bytes(direct))
        self.assertEqual(loaded, direct)
        self.assertEqual(hash(loaded), hash(direct))
        self.assertEqual(repr(loaded), repr(direct))

    def test_replacement_discards_derived_state_for_every_input_change(self):
        loaded, _ = load_fixture()
        changed_files = tuple(replace(item, digest=inputs.file_digest(b"changed"))
                              if item.path == "inputs/shared.txt" else item for item in loaded.files)
        changed_requires = tuple(replace(item, requires=("left",))
                                 if item.id == "top" else item for item in loaded.suites)
        changed_definition = tuple(replace(item, digest=inputs.file_digest(b"definition"))
                                   if item.id == "common" else item for item in loaded.suites)
        cases = (
            replace(loaded, files=changed_files),
            replace(loaded, suites=changed_requires),
            replace(loaded, suites=changed_definition),
            replace(loaded, repository_index=replace(loaded.repository_index,
                                                     digest=inputs.file_digest(b"new index"))),
        )
        for changed in cases:
            with self.subTest(manifest=changed):
                self.assertIsNone(changed._dependencies)
                self.assertNotEqual(changed.dependency("top"), loaded.dependency("top"))
        self.assertIsNone(replace(loaded)._dependencies)
        with self.assertRaises((TypeError, ValueError)):
            replace(loaded, _dependencies={})

    def test_independent_manifests_with_same_suite_ids_do_not_share_results(self):
        first, _ = load_fixture(b"first")
        second, _ = load_fixture(b"second")
        self.assertNotEqual(first.dependency("top"), second.dependency("top"))
        self.assertEqual(first.dependency("other"), second.dependency("other"))
        self.assertIsNot(first._dependencies, second._dependencies)

    def test_reload_rechecks_live_files_even_after_a_successful_load(self):
        files, _ = manifest_fixture()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, content in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            retained = inputs.load_suite_input_manifest(root, "manifest.json")
            prior = retained.dependency("top")
            (root / "inputs/shared.txt").write_bytes(b"changed behind manifest")
            with self.assertRaises(MetadataError) as error:
                inputs.load_suite_input_manifest(root, "manifest.json")
            self.assertEqual(error.exception.failure.code, "SUITE_INPUT.STALE_FILE")
            self.assertEqual(error.exception.failure.path, "inputs/shared.txt")
            self.assertIs(retained.dependency("top"), prior)

    def test_invalid_material_rejects_before_dependency_preparation(self):
        original, _ = manifest_fixture()
        for path, replacement, code in (
            ("registry.toml", b"changed", "SUITE_INPUT.STALE_REGISTRY"),
            ("suites/common.toml", b'id = "common"\n# changed\n', "SUITE_INPUT.STALE_SUITES"),
            ("inputs/shared.txt", b"changed", "SUITE_INPUT.STALE_FILE"),
            ("inputs/absent.txt", b"present", "SUITE_INPUT.PRESENT_ABSENCE"),
            ("manifest.json", b"{}", "SUITE_INPUT.INVALID_FIELDS"),
        ):
            with self.subTest(path=path):
                files = {**original, path: replacement}
                with patch.object(inputs.SuiteInputManifest, "_derive_dependency",
                                  side_effect=AssertionError("prepared before validation")):
                    with self.assertRaises(MetadataError) as error:
                        inputs.load_suite_input_manifest(FrozenContentSource(files), "manifest.json")
                self.assertEqual(error.exception.failure.code, code)

    def test_invalid_graph_keeps_cycle_and_missing_prerequisite_diagnostics(self):
        for requires, code in ((["unknown"], "SUITE_INPUT.INVALID_DEPENDENCY"),
                               (["top"], "SUITE_INPUT.DEPENDENCY_CYCLE")):
            files, direct = manifest_fixture()
            text = files["registry.toml"].decode().replace('requires = []',
                  f'requires = {json.dumps(requires)}', 1)
            files["registry.toml"] = text.encode()
            changed = replace(direct, registry_digest=inputs.file_digest(files["registry.toml"]))
            files["manifest.json"] = inputs.suite_input_manifest_bytes(changed)
            with self.subTest(requires=requires), self.assertRaises(MetadataError) as error:
                inputs.load_suite_input_manifest(FrozenContentSource(files), "manifest.json")
            self.assertEqual(error.exception.failure.code, code)

    def test_absence_membership_and_unrelated_files_have_distinct_dependency_effects(self):
        loaded, _ = load_fixture()
        without_absence = replace(loaded, files=tuple(item for item in loaded.files if item.state != "absent"))
        without_index = replace(loaded, repository_index=None)
        self.assertNotEqual(loaded.dependency("top"), without_absence.dependency("top"))
        self.assertNotEqual(loaded.dependency("top"), without_index.dependency("top"))
        self.assertEqual(loaded.dependency("common"), without_index.dependency("common"))
        self.assertEqual(loaded.dependency("other"), without_absence.dependency("other"))

    def test_parallel_reads_neither_recompute_nor_change_the_prepared_index(self):
        loaded, _ = load_fixture()
        expected = loaded.dependency("top")
        with patch.object(inputs.SuiteInputManifest, "_derive_dependency",
                          side_effect=AssertionError("unexpected lazy mutation")):
            with ThreadPoolExecutor(max_workers=4) as pool:
                results = list(pool.map(loaded.dependency, ["top"] * 32))
        self.assertTrue(all(result is expected for result in results))


if __name__ == "__main__":
    unittest.main()
