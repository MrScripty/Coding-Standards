"""Exact proof reuse never substitutes for durable reads or current authority."""
from __future__ import annotations

from contextlib import closing
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_snapshots.standards_snapshots import (
    AggregateChild, CapturedContent, SnapshotError, SnapshotFile, SnapshotModule,
)
from tools.standards_snapshots.standards_snapshots import module as snapshot_module
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine.authoring import (
    AuthoringError, AuthoringModule, RevisionDecoding,
)
from tools.standards_engine.standards_engine.compiled_cache import CompiledSnapshotCache
from tools.standards_engine.standards_engine.logical_authoring import StandardsChangeSet
from tools.standards_engine.standards_engine.operation_materials import ProposalMaterials
from tools.standards_engine.tests.test_authoring import _authoring, _capture, _change_set
from tools.standards_engine.tests.test_agent_workflow import prepare_repository, reference_change
from tools.standards_engine.tests.test_mcp import request

ROOT = Path(__file__).resolve().parents[3]


def alternative_identity(capture):
    return "alternative:" + SnapshotModule._content_id(capture)


def small_compilation(source):
    # This cache-only unit test supplies an immutable stand-in, not an Engine oracle.
    return source.files


def different_small_compilation(source):
    return ("different-compiler", source.files)


def failed_identity(capture):
    raise RuntimeError("fixture codec failure")


class ContentIdentityReuseTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="identity-reuse-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.path = self.root / "store.sqlite3"
        self.snapshots = SnapshotModule.open(self.path)
        self.addCleanup(self.snapshots.close)
        self.capture = _capture()
        self.snapshot = self.snapshots.create_snapshot(self.capture).snapshot
        self.cache = CompiledSnapshotCache(self.root, "authoring")
        self.addCleanup(self.cache.close)

    def read(self, snapshot=None):
        return self.snapshots.load_content(snapshot or self.snapshot, identity_reuse=self.cache)

    def test_exact_reloaded_captures_share_codec_proof_not_reads(self):
        with (
            patch.object(snapshot_module, "hash_identity", wraps=snapshot_module.hash_identity) as codec,
            patch.object(self.snapshots._store, "load_content", wraps=self.snapshots._store.load_content) as load,
        ):
            first, second = self.read(), self.read()
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertEqual(load.call_count, 2)
        self.assertEqual(codec.call_count, 1)
        self.assertEqual(self.cache.statistics["identity_hits"], 1)

    def test_identity_and_compilation_share_one_budgeted_entry(self):
        self.read()
        size = self.cache.statistics["accounted_bytes"]
        expected = self.cache.compile_verified(self.capture, small_compilation)
        enlarged = self.cache.statistics["accounted_bytes"]
        self.assertGreater(enlarged, size)
        self.assertEqual(self.cache.compile_verified(self.capture, small_compilation), expected)
        self.assertEqual(self.read(), self.capture)
        self.assertEqual(self.cache.statistics["entries"], 1)
        self.assertEqual(self.cache.statistics["accounted_bytes"], enlarged)
        self.assertEqual(self.cache.statistics["evictions"], 0)
        self.assertLessEqual(enlarged, 32 * 1024 * 1024)

    def test_compiler_change_cannot_reuse_another_compiled_product(self):
        self.read()
        first = self.cache.compile_verified(self.capture, small_compilation)
        second = self.cache.compile_verified(self.capture, different_small_compilation)
        self.assertNotEqual(first, second)
        self.assertEqual(self.cache.compile_verified(self.capture, small_compilation), first)
        self.assertEqual(self.cache.statistics["misses"], 3)
        self.assertEqual(self.cache.statistics["hits"], 0)
        self.assertEqual(self.cache.statistics["entries"], 1)
        self.assertEqual(self.read(), self.capture)
        self.assertEqual(self.cache.statistics["identity_hits"], 1)

    def test_changed_bytes_with_identical_source_label_and_hash_collision_miss(self):
        other = CapturedContent(self.capture.source_revision, (
            SnapshotFile(self.capture.files[0].path, b"changed exact bytes"),
            *self.capture.files[1:],
        ))
        calculate = SnapshotModule._content_id
        with patch.object(CapturedContent, "__hash__", return_value=7):
            a = self.cache.identify_content(self.capture, calculate)
            b = self.cache.identify_content(other, calculate)
            self.assertNotEqual(a, b)
            self.assertEqual(a, calculate(self.capture))
            self.assertEqual(b, calculate(other))
            self.assertEqual(self.cache.identify_content(self.capture, calculate), a)
        self.assertEqual(self.cache.statistics["identity_misses"], 2)

    def test_incorrect_expected_content_id_rejects_on_a_warm_hit(self):
        self.read()
        with patch.object(self.snapshots._store, "load_content", return_value=("wrong-stored-id", self.capture)):
            with self.assertRaises(SnapshotError) as raised:
                self.read()
        self.assertEqual(raised.exception.failure.code, "SNAPSHOT.CONTENT_ID_MISMATCH")
        self.assertEqual(self.cache.statistics["identity_hits"], 1)

    def test_rewritten_durable_bytes_with_matching_file_digest_do_not_reuse_proof(self):
        self.read()
        data = b"changed-durable-content"
        with closing(sqlite3.connect(self.path)) as connection, connection:
            ddl = connection.execute("SELECT sql FROM sqlite_schema WHERE name='content_files_no_update'").fetchone()[0]
            connection.execute("DROP TRIGGER content_files_no_update")
            connection.execute(
                "UPDATE content_files SET raw_bytes=?, byte_length=?, sha256=? WHERE logical_path=?",
                (data, len(data), hashlib.sha256(data).hexdigest(), str(self.capture.files[0].path)),
            )
            connection.execute(ddl)
        with self.assertRaises(SnapshotError) as raised:
            self.read()
        self.assertEqual(raised.exception.failure.code, "SNAPSHOT.CONTENT_ID_MISMATCH")
        self.assertEqual(self.cache.statistics["identity_hits"], 0)

    def test_quarantine_purge_and_equal_content_roots_keep_independent_lifecycle(self):
        second = self.snapshots.create_snapshot(self.capture).snapshot
        self.read()
        deletion = self.snapshots.delete_snapshot(self.snapshot)
        with self.assertRaises(SnapshotError):
            self.read()
        self.assertEqual(self.cache.statistics["identity_hits"], 0)
        self.assertEqual(self.read(second), self.capture)
        with patch.object(self.snapshots, "_now", return_value=deletion.purge_deadline):
            with self.assertRaises(SnapshotError):
                self.read()
            self.assertEqual(self.read(second), self.capture)
        self.assertEqual(self.cache.statistics["identity_hits"], 2)

    def test_disabled_evicted_and_oversized_entries_recompute_without_semantic_change(self):
        calculate = SnapshotModule._content_id
        other = CapturedContent("other-source", self.capture.files)
        for entries, budget in ((0, 1024 * 1024), (2, 1), (1, 1024 * 1024)):
            with self.subTest(entries=entries, budget=budget):
                cache = CompiledSnapshotCache(self.root, "authoring", max_entries=entries, max_bytes=budget)
                try:
                    for capture in (self.capture, other, self.capture):
                        self.assertEqual(cache.identify_content(capture, calculate), calculate(capture))
                    self.assertEqual(cache.statistics["identity_hits"], 0)
                    self.assertEqual(cache.statistics["identity_misses"], 3)
                    self.assertLessEqual(cache.statistics["entries"], entries)
                    self.assertLessEqual(cache.statistics["accounted_bytes"], budget)
                finally:
                    cache.close()
                self.assertEqual(cache.statistics["accounted_bytes"], 0)

    def test_calculator_identity_and_stateful_callers_have_distinct_dispositions(self):
        original = SnapshotModule._content_id
        self.assertEqual(self.cache.identify_content(self.capture, original), original(self.capture))
        self.assertEqual(self.cache.identify_content(self.capture, alternative_identity), alternative_identity(self.capture))
        self.assertEqual(self.cache.identify_content(self.capture, original), original(self.capture))
        observed = []
        def stateful(capture):
            observed.append(capture)
            return original(capture)
        for _ in range(2):
            self.assertEqual(self.cache.identify_content(self.capture, stateful), original(self.capture))
        self.assertEqual(len(observed), 2)
        self.assertEqual(self.cache.statistics["identity_uncached"], 2)

    def test_failed_calculation_and_closed_owner_do_not_supply_proofs(self):
        with self.assertRaisesRegex(RuntimeError, "fixture codec failure"):
            self.cache.identify_content(self.capture, failed_identity)
        self.assertEqual(self.cache.statistics["entries"], 0)
        self.read()
        self.cache.close()
        with self.assertRaisesRegex(ValueError, "closed"):
            self.read()
        self.assertEqual(self.cache.statistics["entries"], 0)

    def test_cold_module_does_not_require_or_retain_a_reuse_owner(self):
        self.read()
        with patch.object(snapshot_module, "hash_identity", wraps=snapshot_module.hash_identity) as codec:
            self.assertEqual(self.snapshots.load_content(self.snapshot), self.capture)
            self.assertEqual(self.snapshots.load_content(self.snapshot), self.capture)
        self.assertEqual(codec.call_count, 2)


class RevisionDecodingTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="revision-decoding-")
        self.addCleanup(self.temporary.cleanup)
        self.snapshots = SnapshotModule.open(Path(self.temporary.name) / "store.sqlite3")
        self.addCleanup(self.snapshots.close)
        self.snapshot = self.snapshots.create_snapshot(_capture()).snapshot
        self.author = _authoring(self.snapshots)
        _, self.revision = self.author.create_proposal(self.snapshot, _change_set("first"))
        self.decoding = RevisionDecoding()
        self.addCleanup(self.decoding.clear)

    def test_repeated_exact_record_decodes_once_and_rechecks_every_root(self):
        with (
            patch.object(AuthoringModule, "_revision_from_record", wraps=AuthoringModule._revision_from_record) as decode,
            patch.object(self.snapshots, "load_aggregate", wraps=self.snapshots.load_aggregate) as load,
            patch.object(self.snapshots, "load_aggregate_root", wraps=self.snapshots.load_aggregate_root) as roots,
        ):
            first = self.author.read_revision(self.revision.revision_id, decoding=self.decoding)
            second = self.author.read_revision(self.revision.revision_id, decoding=self.decoding)
            current = self.author.current_revision(self.revision.proposal, decoding=self.decoding)
        self.assertEqual(first, second)
        self.assertEqual(first, current)
        self.assertEqual(decode.call_count, 1)
        self.assertEqual(load.call_count, 3)
        self.assertEqual(roots.call_count, 4)

    def test_current_revision_without_reuse_also_decodes_head_once(self):
        with patch.object(AuthoringModule, "_revision_from_record", wraps=AuthoringModule._revision_from_record) as decode:
            self.assertEqual(self.author.current_revision(self.revision.proposal), self.revision)
        self.assertEqual(decode.call_count, 1)

    def test_changed_head_is_observed_and_historical_material_remains_historical(self):
        self.author.read_revision(self.revision.revision_id, decoding=self.decoding)
        _, newer = self.author.revise_proposal(self.revision.revision_id, _change_set("second"))
        self.assertEqual(self.author.current_revision(self.revision.proposal, decoding=self.decoding), newer)
        self.assertEqual(self.author.read_revision(self.revision.revision_id, decoding=self.decoding), self.revision)
        self.assertEqual(self.author.current_revision(self.revision.proposal, decoding=self.decoding), newer)

    def test_same_claimed_identity_with_changed_record_cannot_hit(self):
        record = self.revision.aggregate()
        self.decoding.decode(record)
        other_snapshot = self.snapshots.create_snapshot(_capture()).snapshot
        for corrupt in (
            replace(record, payload=b"{}"),
            replace(record, kind="other"),
            replace(record, snapshots=(other_snapshot,)),
            replace(record, children=(AggregateChild("unexpected", "child", b"bytes"),)),
        ):
            with self.subTest(corrupt=corrupt), self.assertRaises(AuthoringError) as raised:
                self.decoding.decode(corrupt)
            self.assertEqual(raised.exception.failure.code, "AUTHORING.INVALID_STORED_REVISION")
        self.assertEqual(self.decoding.decode(record), self.revision)

    def test_changed_aggregate_id_cannot_reuse_decoded_material(self):
        record = self.revision.aggregate()
        cached = self.decoding.decode(record)
        _, successor = self.author.revise_proposal(
            self.revision.revision_id, _change_set("distinct identity"),
        )
        # Use an actual well-formed revision ID; only the aggregate's claimed
        # identity changes, not its canonical payload, kind or relationships.
        altered = replace(record, aggregate_id=successor.aggregate().aggregate_id)
        self.assertNotEqual(altered.aggregate_id, record.aggregate_id)
        self.assertEqual(replace(altered, aggregate_id=record.aggregate_id), record)
        with patch.object(AuthoringModule, "_revision_from_record",
                          wraps=AuthoringModule._revision_from_record) as decode:
            with self.assertRaises(AuthoringError) as caught:
                self.decoding.decode(altered)
            self.assertEqual(caught.exception.failure.code, "AUTHORING.INVALID_STORED_REVISION")
            self.assertEqual(caught.exception.failure.outcome, "invalid")
            self.assertEqual(caught.exception.failure.message,
                             "stored proposal revision authority disagrees with its identity")
            self.assertEqual(decode.call_count, 1)
            self.assertIs(self.decoding.decode(record), cached)
            self.assertEqual(decode.call_count, 1)
        self.assertEqual(self.snapshots.load_aggregate(record.aggregate_id), record)

    def test_current_root_membership_is_not_reused(self):
        self.author.read_revision(self.revision.revision_id, decoding=self.decoding)
        root = self.snapshots.load_aggregate_root(str(self.revision.proposal))
        second = self.snapshots.create_snapshot(_capture()).snapshot
        with patch.object(self.snapshots, "load_aggregate_root", return_value=replace(root, snapshots=(second,))):
            with self.assertRaises(AuthoringError) as raised:
                self.author.read_revision(self.revision.revision_id, decoding=self.decoding)
        self.assertEqual(raised.exception.failure.code, "AUTHORING.INVALID_STORED_REVISION")

    def test_quarantine_after_decode_still_denies_read(self):
        self.author.read_revision(self.revision.revision_id, decoding=self.decoding)
        self.snapshots.delete_snapshot(self.snapshot)
        with self.assertRaises(SnapshotError):
            self.author.read_revision(self.revision.revision_id, decoding=self.decoding)

    def test_semantic_intent_and_exported_contract_maps_are_not_mutable_reuse_state(self):
        raw = _change_set("semantic").as_contract()
        raw['edits'] = [{
            'kind':'revise-policy-unit', 'policy':'policy.core.example',
            'title':'Example', 'body':'Existing exact policy body.',
            'semantics':{'kind':'preserve','semantic_revision':1,'intent':'Keep meaning.'},
        }]
        _, revision = self.author.create_proposal(self.snapshot, StandardsChangeSet.from_mapping(raw))
        decoded = self.author.read_revision(revision.revision_id, decoding=self.decoding)
        with self.assertRaises(TypeError):
            decoded.change_sets[0].edits[0].semantics['intent'] = 'changed'
        exported = decoded.change_sets[0].as_contract()
        exported['edits'][0]['semantics']['intent'] = 'changed'
        again = self.author.read_revision(revision.revision_id, decoding=self.decoding)
        self.assertEqual(again.aggregate(), revision.aggregate())

    def test_operation_exit_clears_decoded_material_on_success_and_failure(self):
        engine = StandardsEngine(object(), self.snapshots, purpose="authoring")
        for fail in (False, True):
            materials = ProposalMaterials(engine)
            try:
                with materials:
                    materials.read_revision(self.revision.revision_id)
                    self.assertIsNotNone(materials.revision_decoding._entry)
                    if fail:
                        raise RuntimeError('fixture operation failed')
            except RuntimeError:
                pass
            self.assertIsNone(materials.revision_decoding._entry)


class ImmutableWorkPublicPathTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="immutable-public-")
        cls.root = Path(cls.temporary.name) / "repository"
        prepare_repository(cls.root)
        cls.cache = CompiledSnapshotCache(cls.root, "authoring")
        cls.facade = AgentToolFacade.open_repository(cls.root, purpose="authoring", compiled_cache=cls.cache)
        cls.engine = cls.facade._engine
        routed = cls.facade.route({'facts':{}})
        cls.snapshot = routed['snapshot']
        cls.proposed = cls.facade.propose({'snapshot':cls.snapshot, 'change_set':reference_change(cls.root,'reuse-public')})
        assert cls.proposed['status']=='complete',cls.proposed

    @classmethod
    def tearDownClass(cls):
        cls.facade.close()
        cls.cache.close()
        cls.temporary.cleanup()

    def test_status_decodes_once_per_operation_not_once_per_process(self):
        with patch.object(AuthoringModule, "_revision_from_record", wraps=AuthoringModule._revision_from_record) as decode:
            first = self.facade.workflow_status({'context':self.proposed['context']})
            self.assertEqual(first['status'],'complete',first)
            self.assertEqual(decode.call_count,1)
            second = self.facade.workflow_status({'context':self.proposed['context']})
            self.assertEqual(first,second)
            self.assertEqual(decode.call_count,2)

    def test_status_observes_record_change_after_binding(self):
        load = self.engine._snapshots.load_aggregate
        selected = self.proposed['revision']['id']
        calls = 0
        def changed_record(identifier):
            nonlocal calls
            record = load(identifier)
            if identifier == selected:
                calls += 1
                if calls > 1:
                    return replace(record, payload=b'{}')
            return record
        with patch.object(self.engine._snapshots,'load_aggregate',side_effect=changed_record):
            rejected = self.facade.workflow_status({'context':self.proposed['context']})
        self.assertEqual(rejected['code'],'AUTHORING.INVALID_STORED_REVISION',rejected)
        self.assertEqual(self.facade.workflow_status({'context':self.proposed['context']})['status'],'complete')

    def test_stdio_cold_restarts_and_warm_calls_preserve_results(self):
        messages = [
            request('initialize', {'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'immutable-test','version':'1'}}),
            {'jsonrpc':'2.0','method':'notifications/initialized'},
        ]
        for ident, (name, args) in enumerate((
            ('read',{'snapshot':self.snapshot,'target':'core'}),
            ('read',{'snapshot':self.snapshot,'target':'core'}),
            ('workflow_status',{'context':self.proposed['context']}),
            ('workflow_status',{'context':self.proposed['context']}),
        ), 2):
            messages.append(request('tools/call',{'name':name,'arguments':args},identifier=ident))
        results=[]
        for _ in range(2):
            process=subprocess.run(
                [sys.executable,'-P','-m','tools.standards_engine.standards_engine.mcp','--repo-root',str(self.root),'--purpose','authoring','--output-schemas','on-demand'],
                input=''.join(json.dumps(item)+'\n' for item in messages),text=True,capture_output=True,check=True,
                env={**os.environ,'PYTHONPATH':str(ROOT)},cwd=self.temporary.name,
            )
            items=[json.loads(line) for line in process.stdout.splitlines()]
            values=[]
            for item in items[1:]:
                self.assertNotIn('error',item)
                response=item['result']; self.assertFalse(response['isError'])
                self.assertEqual(response['structuredContent'],json.loads(response['content'][0]['text']))
                values.append(response['structuredContent'])
            self.assertEqual(values[0],values[1]); self.assertEqual(values[2],values[3])
            results.append(values)
        self.assertEqual(results[0],results[1])
