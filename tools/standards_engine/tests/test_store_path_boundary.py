"""Composed store admission preserves the selected final path component."""
from __future__ import annotations

from contextlib import chdir
from pathlib import Path
import tempfile
import unittest

from tools.standards_engine.standards_engine import StandardsEngine
from tools.standards_engine.standards_engine.engine import DEFAULT_STORE
from tools.standards_snapshots.standards_snapshots import SnapshotModule, SnapshotError
from tools.standards_snapshots.tests.test_module import capture

ROOT = Path(__file__).resolve().parents[3]


class StorePathBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.database = self.root / 'store.sqlite3'
        with SnapshotModule.open(self.database) as store:
            self.snapshot = store.create_snapshot(capture(b'preserved')).snapshot
        self.before = self.database.read_bytes()

    def assert_rejected(self, path):
        for purpose in ('authoring', 'application'):
            with self.subTest(purpose=purpose), self.assertRaises(SnapshotError) as caught:
                with StandardsEngine.open_repository(ROOT, store_path=path, purpose=purpose):
                    self.fail('nonregular selected path was admitted')
            self.assertEqual(caught.exception.failure.code, 'SNAPSHOT_STORE.UNSUPPORTED_PATH')
        with self.assertRaises(SnapshotError) as caught:
            SnapshotModule.open(path.absolute())
        self.assertEqual(caught.exception.failure.code, 'SNAPSHOT_STORE.UNSUPPORTED_PATH')
        self.assertEqual(self.database.read_bytes(), self.before)

    def test_existing_final_symlink_is_rejected_before_touching_database(self):
        alias = self.root / 'alias.sqlite3'
        alias.symlink_to(self.database)
        self.assert_rejected(alias)
        self.assertTrue(alias.is_symlink())

    def test_dangling_final_symlink_does_not_create_a_database_at_its_target(self):
        missing = self.root / 'missing.sqlite3'
        alias = self.root / 'dangling.sqlite3'
        alias.symlink_to(missing)
        self.assert_rejected(alias)
        self.assertFalse(missing.exists())
        self.assertTrue(alias.is_symlink())

    def test_directory_is_rejected_and_regular_store_reopens(self):
        self.assert_rejected(self.root)
        for purpose in ('authoring', 'application'):
            with StandardsEngine.open_repository(ROOT, store_path=self.database, purpose=purpose) as engine:
                self.assertEqual(engine._snapshots.load_content(self.snapshot), capture(b'preserved'))
        self.assertEqual(self.database.read_bytes(), self.before)

    def test_relative_selection_preserves_engine_convenience_and_final_admission(self):
        alias = self.root / 'relative.sqlite3'
        alias.symlink_to(self.database)
        with chdir(self.root):
            with StandardsEngine.open_repository(ROOT, store_path=Path('store.sqlite3'), purpose='authoring') as engine:
                self.assertEqual(engine._snapshots.load_content(self.snapshot), capture(b'preserved'))
            self.assert_rejected(Path('relative.sqlite3'))
            with self.assertRaises(SnapshotError) as caught:
                SnapshotModule.open(Path('store.sqlite3'))
            self.assertEqual(caught.exception.failure.code, 'SNAPSHOT_STORE.RELATIVE_PATH')

    def test_intermediate_symlink_is_permitted_but_final_symlink_is_not(self):
        parent_alias = self.root / 'parent'
        parent_alias.symlink_to(self.root, target_is_directory=True)
        selected = parent_alias / self.database.name
        with SnapshotModule.open(selected) as store:
            self.assertEqual(store.load_content(self.snapshot), capture(b'preserved'))
        with StandardsEngine.open_repository(ROOT, store_path=selected, purpose='authoring') as engine:
            self.assertEqual(engine._snapshots.load_content(self.snapshot), capture(b'preserved'))
        final = self.root / 'final.sqlite3'
        final.symlink_to(self.database)
        self.assert_rejected(parent_alias / final.name)

    def test_default_selected_store_also_retains_final_component(self):
        selected = self.root / DEFAULT_STORE
        selected.parent.mkdir(parents=True)
        selected.symlink_to(self.database)
        # The failure occurs at store admission before any repository capture.
        with self.assertRaises(SnapshotError) as caught:
            with StandardsEngine.open_repository(self.root, purpose='authoring'):
                self.fail('default store alias was admitted')
        self.assertEqual(caught.exception.failure.code, 'SNAPSHOT_STORE.UNSUPPORTED_PATH')
        self.assertEqual(self.database.read_bytes(), self.before)

    def test_unavailable_parent_has_no_database_creation_or_authority_loss(self):
        parent = self.root / 'not-a-directory'
        parent.write_bytes(b'parent file')
        path = parent / 'new.sqlite3'
        for opening in (lambda: SnapshotModule.open(path),
                        lambda: StandardsEngine.open_repository(ROOT, store_path=path, purpose='authoring')):
            with self.assertRaises(OSError):
                opening()
        self.assertEqual(parent.read_bytes(), b'parent file')
        self.assertEqual(self.database.read_bytes(), self.before)
