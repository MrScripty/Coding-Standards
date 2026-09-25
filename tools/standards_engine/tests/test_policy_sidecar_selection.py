"""A registered declaration file is storage, not exclusive module ownership."""
from __future__ import annotations

import tomllib
import unittest

from tools.standards_engine.standards_engine.authoring import AuthoringError
from tools.standards_engine.standards_engine.logical_authoring import (
    _ensure_policy_sidecar,
    _policy_sidecar,
    _policy_sidecar_path,
    _render_policy_sidecar,
    _set_registry_list,
)
from tools.standards_metadata.standards_metadata import POLICY_UNIT_REGISTRY


OWNER = "topic.sidecar-origin"
DESTINATION = "topic.sidecar-destination"


def declaration(identity: str, module: str) -> dict[str, object]:
    return {
        "id": identity,
        "module": module,
        "heading_path": ["Selected Scope"],
        "semantic_revision": 2,
        "aliases": [identity + ".alias"],
    }


class PolicySidecarSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.path = _policy_sidecar_path(OWNER)
        self.files = {POLICY_UNIT_REGISTRY: b"schema_version = 1\nsources = []\n"}
        self.moved = declaration(OWNER + ".moved", DESTINATION)
        self.retired = {
            "id": OWNER + ".retired",
            "retired_semantic_revision": 3,
            "successors": [],
            "evidence": "evidence:sidecar-retirement",
        }

    def install(self, path: str, units, tombstones=()) -> None:
        self.files[path] = _render_policy_sidecar(units, tombstones)
        _set_registry_list(self.files, POLICY_UNIT_REGISTRY, "sources", path, present=True)

    def assert_selection_preserves_files(self, module: str, path: str) -> None:
        before = dict(self.files)
        self.assertEqual(_ensure_policy_sidecar(self.files, module), path)
        self.assertEqual(self.files, before)

    def test_registered_derived_path_preserves_a_moved_policy(self) -> None:
        self.install(self.path, [self.moved])
        self.assert_selection_preserves_files(OWNER, self.path)

    def test_registered_derived_path_preserves_moved_policy_and_tombstones(self) -> None:
        self.install(self.path, [self.moved], [self.retired])
        self.assert_selection_preserves_files(OWNER, self.path)
        active, retired = _policy_sidecar(self.files[self.path])
        self.assertEqual(active, [self.moved])
        self.assertEqual(retired, [self.retired])

    def test_shared_storage_preserves_every_declared_owner(self) -> None:
        third = declaration("topic.third.existing", "topic.third")
        self.install(self.path, [self.moved, third], [self.retired])
        self.assert_selection_preserves_files(OWNER, self.path)
        self.assert_selection_preserves_files(DESTINATION, self.path)
        self.assert_selection_preserves_files("topic.third", self.path)

    def test_existing_module_storage_remains_preferred_over_derived_storage(self) -> None:
        alternate = _policy_sidecar_path("topic.shared-storage")
        self.install(self.path, [self.moved])
        self.install(alternate, [declaration(OWNER + ".current", OWNER)])
        self.assert_selection_preserves_files(OWNER, alternate)

    def test_existing_module_storage_is_used_without_creating_derived_path(self) -> None:
        alternate = _policy_sidecar_path("topic.shared-storage")
        self.install(alternate, [declaration(OWNER + ".current", OWNER)])
        self.assert_selection_preserves_files(OWNER, alternate)
        self.assertNotIn(self.path, self.files)

    def test_registered_empty_and_tombstone_only_storage_remain_usable(self) -> None:
        for retired in ([], [self.retired]):
            with self.subTest(tombstones=bool(retired)):
                self.setUp()
                self.install(self.path, [], retired)
                self.assert_selection_preserves_files(OWNER, self.path)

    def test_new_storage_is_created_and_registered_once(self) -> None:
        self.files["topics/unrelated.md"] = b"Unrelated source remains intact.\n"
        self.assertEqual(_ensure_policy_sidecar(self.files, OWNER), self.path)
        self.assertEqual(_policy_sidecar(self.files[self.path]), ([], []))
        self.assert_selection_preserves_files(OWNER, self.path)
        sources = tomllib.loads(self.files[POLICY_UNIT_REGISTRY].decode())["sources"]
        self.assertEqual(sources, [self.path])
        self.assertEqual(self.files["topics/unrelated.md"], b"Unrelated source remains intact.\n")

    def test_unregistered_occupied_path_is_preserved_and_rejected(self) -> None:
        self.files[self.path] = _render_policy_sidecar([self.moved], [self.retired])
        before = dict(self.files)
        with self.assertRaises(AuthoringError) as raised:
            _ensure_policy_sidecar(self.files, OWNER)
        self.assertEqual(raised.exception.failure.code, "AUTHORING.PROJECTION_DISAGREEMENT")
        self.assertEqual(self.files, before)

    def test_invalid_registered_storage_is_preserved_and_rejected(self) -> None:
        self.install(self.path, [self.moved])
        for content in (b"not toml", b"schema_version = 99\n", b"schema_version = 1\npolicy_unit = 7\n"):
            with self.subTest(content=content):
                self.files[self.path] = content
                before = dict(self.files)
                with self.assertRaises(AuthoringError) as raised:
                    _ensure_policy_sidecar(self.files, OWNER)
                self.assertEqual(raised.exception.failure.code, "AUTHORING.PROJECTION_DISAGREEMENT")
                self.assertEqual(self.files, before)

    def test_append_preserves_foreign_identity_alias_revision_and_retirement(self) -> None:
        self.install(self.path, [self.moved], [self.retired])
        registry_before = self.files[POLICY_UNIT_REGISTRY]
        selected = _ensure_policy_sidecar(self.files, OWNER)
        active, retired = _policy_sidecar(self.files[selected])
        added = declaration(OWNER + ".new", OWNER)
        active.append(added)
        self.files[selected] = _render_policy_sidecar(active, retired)
        active_after, retired_after = _policy_sidecar(self.files[selected])
        self.assertEqual({item["id"]: item for item in active_after}, {
            self.moved["id"]: self.moved, added["id"]: added,
        })
        self.assertEqual(retired_after, [self.retired])
        self.assertEqual(self.files[POLICY_UNIT_REGISTRY], registry_before)
        self.assert_selection_preserves_files(OWNER, self.path)
        self.assert_selection_preserves_files(DESTINATION, self.path)


if __name__ == "__main__":
    unittest.main()
