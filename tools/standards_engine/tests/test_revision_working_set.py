"""A focused successor retains useful pure material, never live authority."""
from __future__ import annotations

from collections import Counter
from contextlib import closing, contextmanager
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine.compiled_cache import CompiledSnapshotCache
from tools.standards_engine.standards_engine.tools import LocalAlwaysAllowAuthorizer
from tools.standards_engine.tests.test_agent_workflow import prepare_repository, reference_change
from tools.standards_snapshots.standards_snapshots import SnapshotModule


@contextmanager
def count_pure_work():
    """Count original functions without changing cache-eligible function identity."""
    counts = Counter()
    observed = {StandardsEngine._compile.__code__: 'compile',
                SnapshotModule._content_id.__code__: 'content_id'}
    previous = sys.getprofile()
    def record(frame, event, argument):
        if event == 'call' and frame.f_code in observed:
            counts[observed[frame.f_code]] += 1
    sys.setprofile(record)
    try:
        yield counts
    finally:
        sys.setprofile(previous)


class RevisionWorkingSetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(prefix='revision-working-set-')
        cls.addClassCleanup(cls.fixture.cleanup)
        cls.root = Path(cls.fixture.name)/'repository'
        prepare_repository(cls.root)
        cls.interface = AgentToolFacade.load_interface(cls.root)
        cls.main = subprocess.check_output(['git','-C',str(cls.root),'rev-parse','main'],text=True)
        with AgentToolFacade.open_repository(cls.root,purpose='authoring',interface=cls.interface) as facade:
            cls.first = facade.propose({'change_set':reference_change(cls.root,'working-set')})
            assert cls.first['status']=='complete',cls.first
        cls.seed = cls.root/'.standards-engine/snapshots-v1.sqlite3'

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='working-set-observation-')
        self.addCleanup(self.temporary.cleanup)
        self.counter = 0

    @contextmanager
    def facade(self, *, entries=2, budget=32*1024*1024):
        self.counter += 1
        store = Path(self.temporary.name)/f'{self.counter}.sqlite3'
        self.store = store
        with closing(sqlite3.connect(self.seed)) as source, closing(sqlite3.connect(store)) as copy:
            source.backup(copy)
        cache = CompiledSnapshotCache(self.root,'authoring',max_entries=entries,max_bytes=budget)
        try:
            with StandardsEngine.open_repository(self.root,purpose='authoring',store_path=store,
                    compiled_cache=cache,execution_context=AnalysisExecutionContext(LocalAlwaysAllowAuthorizer(self.root))) as engine:
                yield AgentToolFacade(engine,self.interface), cache
        finally:
            cache.close()
            self.assertEqual(cache.statistics['entries'],0)
            self.assertEqual(cache.statistics['accounted_bytes'],0)

    def revise(self, facade, *, native=False):
        change = reference_change(self.root,'working-set',revision=True)
        if native:
            result = facade.revise_proposal({'kind':'revise-proposal',
                'expected_revision':self.first['revision'],'change_set':change})
            self.assertEqual(result['kind'],'revise-proposal-result',result)
            return result['revision']
        result = facade.revise({'context':self.first['context'],'change_set':change})
        self.assertEqual(result['status'],'complete',result)
        return result['context']

    def test_focused_successor_keeps_base_and_successor_in_default_budget(self):
        with self.facade() as (facade,cache):
            before = facade.workflow_status({'context':self.first['context']})
            self.assertEqual(before['status'],'complete')
            context = self.revise(facade)
            retained = cache.statistics.copy()
            with count_pure_work() as counts:
                status = facade.workflow_status({'context':context})
            self.assertEqual(status['status'],'complete',status)
            self.assertEqual(counts['compile'],0)
            self.assertEqual(counts['content_id'],0)
            self.assertEqual(retained['entries'],2)
            self.assertLessEqual(retained['accounted_bytes'],32*1024*1024)
            self.assertEqual(sorted(key[0] for key in cache._entries),['proposal','snapshot'])
            self.assertEqual(facade.workflow_status({'context':context}),status)
            # Evicted computational predecessors remain readable; they are not
            # destroyed or treated as the latest proposal head.
            old = facade.query_proposal({'revision':self.first['revision'],
                'request':{'kind':'read','target':'reference.testing.working-set'}})
            self.assertEqual(old['kind'],'proposal-read-result',old)
            self.assertNotIn('Revised fixture text.',old['content'])
            self.assertEqual(facade.workflow_status({'context':self.first['context']})['status'],'stale')
        self.assertEqual(subprocess.check_output(['git','-C',str(self.root),'rev-parse','main'],text=True),self.main)

    def test_native_and_focused_paths_each_match_cold_status_without_base_rework(self):
        for native in (True,False):
            with self.subTest(native=native), self.facade() as (facade,cache):
                facade.workflow_status({'context':self.first['context']})
                context = self.revise(facade,native=native)
                with count_pure_work() as counts:
                    result = facade.workflow_status({'context':context})
                self.assertEqual(counts['compile'],0)
                self.assertEqual(counts['content_id'],0)
                self.assertEqual(cache.statistics['entries'],2)
                with StandardsEngine.open_repository(self.root,purpose='authoring',store_path=self.store,
                        execution_context=AnalysisExecutionContext(LocalAlwaysAllowAuthorizer(self.root))) as cold:
                    fresh = AgentToolFacade(cold,self.interface).workflow_status({'context':context})
                    self.assertEqual(result,fresh)

    def test_capacity_pressure_changes_retention_not_result_meaning(self):
        expected = None
        for entries,budget in ((2,32*1024*1024),(3,32*1024*1024),(1,32*1024*1024),(0,32*1024*1024),(2,1)):
            with self.subTest(entries=entries,budget=budget), self.facade(entries=entries,budget=budget) as (facade,cache):
                facade.workflow_status({'context':self.first['context']})
                context = self.revise(facade)
                result = facade.workflow_status({'context':context})
                expected = result if expected is None else expected
                self.assertEqual(result,expected)
                self.assertLessEqual(cache.statistics['entries'],entries)
                self.assertLessEqual(cache.statistics['accounted_bytes'],budget)

    def test_rejected_focused_successor_does_not_replace_valid_material_or_head(self):
        with self.facade() as (facade,cache):
            original = facade.workflow_status({'context':self.first['context']})
            keys = set(cache._entries)
            change = reference_change(self.root,'working-set',revision=True)
            change['edits'][0]['standard']['body'] = reference_change(self.root,'working-set')['edits'][0]['standard']['body']
            rejected = facade.revise({'context':self.first['context'],'change_set':change})
            self.assertEqual(rejected['kind'],'workflow-result',rejected)
            self.assertEqual(rejected['status'],'rejected',rejected)
            self.assertEqual(rejected['outcome']['code'],'AUTHORING.NO_EFFECT',rejected)
            self.assertEqual(set(cache._entries),keys)
            with count_pure_work() as counts:
                restored = facade.workflow_status({'context':self.first['context']})
            self.assertEqual(restored,original)
            self.assertEqual(counts['compile'],0)
            self.assertEqual(counts['content_id'],0)
