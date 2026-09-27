"""A successful capture shares proof-derived computation, never live authority."""
from __future__ import annotations

from collections import Counter
from contextlib import contextmanager, closing
from dataclasses import replace
import gc
import hashlib
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
import weakref
from unittest.mock import patch

from tools.standards_metadata.standards_metadata import FrozenContentSource, RecordingContentSource
from tools.standards_snapshots.standards_snapshots import (
    CapturedContent, SnapshotError, SnapshotFailure, SnapshotId, SnapshotModule,
)
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine.compiled_cache import CompiledSnapshotCache

ROOT = Path(__file__).resolve().parents[3]


def other_compiler(source):
    """A distinct stateless implementation identity for invalidation tests."""
    return StandardsEngine._compile(source)



@contextmanager
def capture_work():
    """Count original functions; mocking _compile would disable its reuse path."""
    counts = Counter()
    sources = []
    functions = {StandardsEngine._compile.__code__: 'compile',
                 SnapshotModule._content_id.__code__: 'identity'}
    old = sys.getprofile()
    def observe(frame, event, result):
        if event == 'call' and frame.f_code in functions:
            counts[functions[frame.f_code]] += 1
            if functions[frame.f_code] == 'compile':
                sources.append(frame.f_locals['source'])
    sys.setprofile(observe)
    try:
        yield counts, sources
    finally:
        sys.setprofile(old)


class CaptureHandoffTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.interface = AgentToolFacade.load_interface(ROOT)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='capture-handoff-')
        self.addCleanup(self.temporary.cleanup)
        self.store = Path(self.temporary.name)/'store.sqlite3'
        self.cache = CompiledSnapshotCache(ROOT, 'authoring')
        self.addCleanup(self.cache.close)
        self.engine = StandardsEngine.open_repository(ROOT, purpose='authoring', store_path=self.store,
                                                     compiled_cache=self.cache)
        self.addCleanup(self.engine.close)
        self.facade = AgentToolFacade(self.engine, self.interface)

    def test_first_route_uses_both_capture_proofs_without_third_compilation(self):
        with (capture_work() as (counts, sources),
              patch.object(self.engine._snapshots, 'load_content', wraps=self.engine._snapshots.load_content) as load):
            result = self.facade.route({'facts': {}})
        self.assertEqual(result['kind'], 'compact-route-result', result)
        self.assertEqual(counts['compile'], 2)
        self.assertEqual(counts['identity'], 2)
        self.assertEqual(load.call_count, 1)
        self.assertEqual(len(sources), 2)
        self.assertTrue(all(type(source) is RecordingContentSource for source in sources))
        self.assertIsNot(sources[0], sources[1])
        self.assertEqual(sources[0].requested_paths, sources[1].requested_paths)
        self.assertEqual(self.cache.statistics['entries'], 1)
        with StandardsEngine.open_repository(ROOT, purpose='authoring', store_path=self.store) as cold:
            expected = AgentToolFacade(cold, self.interface).route({'snapshot': result['snapshot'], 'facts': {}})
        self.assertEqual(result, expected)

    def capture(self):
        result = self.facade.create_snapshot({'kind': 'create-snapshot'})
        self.assertEqual(result['kind'], 'create-snapshot-result', result)
        return result['snapshot']['snapshot']

    def read(self, snapshot):
        return self.facade.read({'snapshot': snapshot, 'target': 'core'})

    def test_snapshot_is_published_before_frozen_compilation_retention(self):
        publish = self.engine._snapshots.create_snapshot
        retain = self.cache.retain_verified
        order = []
        weak_recorders = []
        original = StandardsEngine._compile.__code__
        def observe(frame, event, arg):
            if event == 'call' and frame.f_code is original:
                weak_recorders.append(weakref.ref(frame.f_locals['source']))
        def admitted(capture):
            self.assertEqual(len(weak_recorders), 2)
            self.assertEqual(self.cache.statistics['entries'], 0)
            summary = publish(capture)
            order.append(('published', summary.snapshot))
            return summary
        def retained(capture, compiler, compiled):
            self.assertEqual(order[0][0], 'published')
            self.assertEqual(self.engine._snapshots.snapshot(order[0][1]).snapshot, order[0][1])
            self.assertIs(compiler, StandardsEngine._compile)
            self.assertIs(type(compiled.source), FrozenContentSource)
            self.assertEqual(compiled.source.files,
                             tuple(sorted((str(item.path), item.content) for item in capture.files)))
            accepted = retain(capture, compiler, compiled)
            self.assertTrue(accepted)
            order.append(('retained', None))
            return accepted
        old = sys.getprofile()
        sys.setprofile(observe)
        try:
            with (patch.object(self.engine._snapshots, 'create_snapshot', side_effect=admitted),
                  patch.object(self.cache, 'retain_verified', side_effect=retained),
                  patch.object(self.engine._snapshots, 'load_content', side_effect=AssertionError('extra capture read'))):
                snapshot = self.capture()
        finally:
            sys.setprofile(old)
        gc.collect()
        self.assertEqual([step for step, _ in order], ['published', 'retained'])
        self.assertTrue(all(reference() is None for reference in weak_recorders))
        with capture_work() as (counts, _):
            read = self.read(snapshot)
        self.assertEqual(read['kind'], 'compact-read-result', read)
        self.assertEqual(counts['compile'], 0)
        # Normal identity checking is not satisfied by the capture's claimed ID.
        self.assertEqual(counts['identity'], 1)
        retained = next(iter(self.cache._entries.values()))[0].compilation[1]
        with StandardsEngine.open_repository(ROOT, purpose='authoring', store_path=self.store) as cold:
            rebuilt = cold._compiled_snapshot(SnapshotId(snapshot['id']))
        self.assertEqual(retained.semantic_signature(), rebuilt.semantic_signature())
        self.assertEqual(retained.source.files, rebuilt.source.files)

    def test_closure_and_semantic_mismatch_cannot_seed_or_publish(self):
        class Signature:
            def __init__(self, value):
                self.value = value
            def semantic_signature(self):
                return self.value
        for fault in ('extra-path', 'different-signature'):
            with self.subTest(fault=fault):
                calls = []
                def compile_fault(source):
                    calls.append(source)
                    source.read_bytes('CORE-STANDARDS.md')
                    if len(calls) == 2 and fault == 'extra-path':
                        source.read_bytes('STANDARDS-ROUTER.md')
                    return Signature(len(calls) if fault == 'different-signature' else 1)
                with (patch.object(self.engine, '_compile', side_effect=compile_fault),
                      patch.object(self.cache, 'retain_verified', side_effect=AssertionError('retention on failure')),
                      patch.object(self.engine._snapshots, 'create_snapshot', side_effect=AssertionError('publication on failure'))):
                    result = self.facade.create_snapshot({'kind': 'create-snapshot'})
                self.assertEqual(result['code'], 'SNAPSHOT.CLOSURE_MISMATCH')
                self.assertEqual(len(calls), 2)
                self.assertEqual(self.cache.statistics['entries'], 0)

    def test_failed_snapshot_admission_does_not_retain_proved_result(self):
        error = SnapshotError(SnapshotFailure('unavailable', 'SNAPSHOT_STORE.FIXTURE_FAILURE', 'Synthetic admission failure.'))
        with (capture_work() as (counts, _),
              patch.object(self.engine._snapshots._store, 'publish_snapshot', side_effect=error),
              patch.object(self.cache, 'retain_verified', side_effect=AssertionError('retention before admission'))):
            result = self.facade.create_snapshot({'kind': 'create-snapshot'})
        self.assertEqual(result['code'], error.failure.code)
        self.assertEqual(counts['compile'], 2)
        self.assertEqual(self.cache.statistics['entries'], 0)
        with closing(sqlite3.connect(self.store)) as connection:
            self.assertEqual(connection.execute('SELECT COUNT(*) FROM snapshot_roots').fetchone()[0], 0)
        # An ordinary retry succeeds; no failed result was remembered.
        self.assertEqual(self.read(self.capture())['kind'], 'compact-read-result')

    def test_disabled_tiny_and_one_entry_limits_preserve_exact_results(self):
        for entries, budget in ((0, 32*1024*1024), (2, 1), (1, 32*1024*1024)):
            with self.subTest(entries=entries, budget=budget):
                cache = CompiledSnapshotCache(ROOT, 'authoring', max_entries=entries, max_bytes=budget)
                try:
                    with StandardsEngine.open_repository(ROOT, purpose='authoring', store_path=self.store,
                                                        compiled_cache=cache) as engine:
                        facade = AgentToolFacade(engine, self.interface)
                        with capture_work() as (counts, _):
                            observed = facade.read({'target': 'core'})
                        self.assertEqual(observed['kind'], 'compact-read-result')
                        self.assertEqual(counts['compile'], 2 if entries and budget > 1 else 3)
                        with StandardsEngine.open_repository(ROOT, purpose='authoring', store_path=self.store) as cold:
                            expected = AgentToolFacade(cold, self.interface).read({'snapshot': observed['snapshot'], 'target': 'core'})
                        self.assertEqual(observed, expected)
                        self.assertLessEqual(cache.statistics['entries'], entries)
                        self.assertLessEqual(cache.statistics['accounted_bytes'], budget)
                finally:
                    cache.close()
                self.assertEqual(cache.statistics['accounted_bytes'], 0)

    def test_first_identity_proof_preserves_the_retained_capture_key(self):
        handle = self.capture()
        key_before = next(iter(self.cache._entries))
        size_before = self.cache.statistics['accounted_bytes']
        loaded = self.engine._snapshots.load_content(SnapshotId(handle['id']), identity_reuse=self.cache)
        self.assertEqual(loaded, key_before[1])
        self.assertIsNot(loaded, key_before[1])
        key_after = next(iter(self.cache._entries))
        self.assertTrue(key_after is key_before, 'Identity extension replaced the existing exact capture key.')
        # The added codec/digest proof must not retain a second full byte set.
        self.assertLess(self.cache.statistics['accounted_bytes'] - size_before, 4096)
        self.assertEqual(self.cache.statistics['entries'], 1)

    def test_quarantine_and_purge_override_the_capture_handoff(self):
        handle = self.capture()
        identity = SnapshotId(handle['id'])
        deleted = self.engine._snapshots.delete_snapshot(identity)
        with capture_work() as (counts, _):
            result = self.read(handle)
        self.assertEqual(result['outcome'], 'unavailable')
        self.assertEqual(counts['compile'], 0)
        self.assertEqual(self.cache.statistics['hits'], 0)
        with patch.object(self.engine._snapshots, '_now', return_value=deleted.purge_deadline):
            result = self.read(handle)
        self.assertEqual(result['outcome'], 'unavailable')
        self.assertEqual(self.cache.statistics['hits'], 0)

    def test_wrong_stored_identity_and_changed_durable_bytes_cannot_hit(self):
        handle = self.capture()
        identity = SnapshotId(handle['id'])
        capture = self.engine._snapshots.load_content(identity)
        with patch.object(self.engine._snapshots._store, 'load_content', return_value=('wrong-stored-id', capture)):
            rejected = self.read(handle)
        self.assertEqual(rejected['code'], 'SNAPSHOT.CONTENT_ID_MISMATCH')
        self.assertEqual(self.cache.statistics['hits'], 0)
        data = b'Changed durable bytes; the per-file digest is updated but content identity is not.'
        with closing(sqlite3.connect(self.store)) as connection, connection:
            ddl = connection.execute("SELECT sql FROM sqlite_schema WHERE name='content_files_no_update'").fetchone()[0]
            connection.execute('DROP TRIGGER content_files_no_update')
            connection.execute('UPDATE content_files SET raw_bytes=?,byte_length=?,sha256=? WHERE logical_path=?',
                               (data, len(data), hashlib.sha256(data).hexdigest(), 'CORE-STANDARDS.md'))
            connection.execute(ddl)
        rejected = self.read(handle)
        self.assertEqual(rejected['code'], 'SNAPSHOT.CONTENT_ID_MISMATCH')
        self.assertEqual(self.cache.statistics['hits'], 0)

    def test_eviction_and_new_process_owner_reconstruct_the_same_snapshot(self):
        cache = CompiledSnapshotCache(ROOT, 'authoring', max_entries=1)
        self.addCleanup(cache.close)
        with StandardsEngine.open_repository(ROOT, purpose='authoring', store_path=self.store, compiled_cache=cache) as engine:
            facade = AgentToolFacade(engine, self.interface)
            expected = facade.read({'target': 'core'})
            capture = engine._snapshots.load_content(SnapshotId(expected['snapshot']['id']))
            other = engine._snapshots.create_snapshot(CapturedContent('different-source-label', capture.files))
            facade.read({'snapshot': engine._snapshot_handle(other.snapshot), 'target': 'core'})
            with capture_work() as (counts, _):
                self.assertEqual(facade.read({'snapshot': expected['snapshot'], 'target': 'core'}), expected)
            self.assertEqual(counts['compile'], 1)
        cache.close()
        fresh = CompiledSnapshotCache(ROOT, 'authoring')
        self.addCleanup(fresh.close)
        with StandardsEngine.open_repository(ROOT, purpose='authoring', store_path=self.store, compiled_cache=fresh) as engine:
            with capture_work() as (counts, _):
                actual = AgentToolFacade(engine, self.interface).read({'snapshot': expected['snapshot'], 'target': 'core'})
            self.assertEqual(actual, expected)
            self.assertEqual(counts['compile'], 1)

    def test_compiler_identity_is_bound_at_capture_not_relabelled_on_publication(self):
        publish = self.engine._snapshots.create_snapshot
        def switch_compiler(capture):
            result = publish(capture)
            self.engine._compile = other_compiler
            return result
        with patch.object(self.engine._snapshots, 'create_snapshot', side_effect=switch_compiler):
            handle = self.capture()
        material = next(iter(self.cache._entries.values()))[0]
        self.assertIs(material.compilation[0], StandardsEngine._compile)
        with capture_work() as (counts, _):
            result = self.read(handle)
        self.assertEqual(result['kind'], 'compact-read-result')
        self.assertEqual(counts['compile'], 1)
        material = next(iter(self.cache._entries.values()))[0]
        self.assertIs(material.compilation[0], other_compiler)

    def test_stateful_or_foreign_source_compiler_keeps_ordinary_cold_behavior(self):
        calls = []
        def stateful(source):
            calls.append(source)
            return StandardsEngine._compile(source)
        with patch.object(self.engine, '_compile', new=stateful):
            handle = self.capture()
            self.assertEqual(self.cache.statistics['entries'], 0)
            result = self.read(handle)
        self.assertEqual(result['kind'], 'compact-read-result')
        self.assertEqual(len(calls), 3)
        self.assertTrue(all(material.compilation is None for material, _ in self.cache._entries.values()))
        # An adapter that substitutes its own source has not supplied the exact
        # frozen-source proof required by capture handoff, even if signatures agree.
        def foreign_source(source):
            compiled = StandardsEngine._compile(source)
            return replace(compiled, source=FrozenContentSource({}))
        with (patch.object(self.engine, '_compile', new=foreign_source),
              patch.object(self.cache, 'retain_verified', side_effect=AssertionError('foreign source retained'))):
            self.capture()

    def test_readonly_purpose_still_qualifies_current_material(self):
        cache = CompiledSnapshotCache(ROOT, 'application')
        self.addCleanup(cache.close)
        with StandardsEngine.open_repository(ROOT, purpose='application', store_path=self.store, compiled_cache=cache) as engine:
            facade = AgentToolFacade(engine, self.interface)
            with capture_work() as (counts, _):
                result = facade.read({'target': 'core'})
            self.assertEqual(counts['compile'], 2)
            self.assertEqual(cache.statistics['entries'], 1)
            # Publication qualification is not inferred from successful capture.
            with closing(sqlite3.connect(self.store)) as connection:
                snapshots = connection.execute('SELECT snapshot_id FROM snapshot_roots').fetchall()
            self.assertEqual(len(snapshots), 1)
            snapshot = snapshots[0][0]
            with StandardsEngine.open_repository(ROOT, purpose='application', store_path=self.store) as cold:
                expected = AgentToolFacade(cold, self.interface).read({
                    'snapshot': engine._snapshot_handle(SnapshotId(snapshot)), 'target': 'core'})
            self.assertEqual(result, expected)

    def test_warm_capture_reproves_independently_and_closed_owner_releases_material(self):
        first = self.capture()
        self.read(first)
        with capture_work() as (counts, _):
            second = self.capture()
        self.assertEqual(counts['compile'], 2)
        self.assertNotEqual(first, second)
        with capture_work() as (counts, _):
            self.read(second)
        self.assertEqual(counts['compile'], 0)
        self.cache.close()
        self.assertEqual(self.cache.statistics['entries'], 0)
        self.assertEqual(self.cache.statistics['accounted_bytes'], 0)
