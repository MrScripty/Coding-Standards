"""The loader, authoring projection and readable routing share one representation."""
from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from tools.standards_engine.standards_engine import ReadRequest, SnapshotHandle, StandardsEngine
from tools.standards_engine.standards_engine.logical_authoring import _project_route_guidance, _refresh_suite_input_projection
from tools.standards_engine.tests import test_logical_authoring as fixture
from tools.standards_metadata.standards_metadata import FrozenContentSource
from tools.standards_snapshots.standards_snapshots import CapturedContent, SnapshotFile, SnapshotPath
from tools.standards_analysis.standards_analysis import parse_router_guidance


class RouterConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.LogicalAuthoringTests.setUpClass()
        cls.base = fixture.LogicalAuthoringTests.base
        cls.repository_paths = fixture.LogicalAuthoringTests.repository_paths
        cls.files = dict(cls.base.files)
        text = cls.files['STANDARDS-ROUTER.md'].decode()
        # Exercise a changed display title without requiring the live corpus to
        # retain this historical heading or a particular following section.
        text = text.replace('## S1 Rust Library Bug-Fix Route', '## Optional routing example')
        cls.files['STANDARDS-ROUTER.md'] = text.encode()
        cls.refresh(cls.files)
        cls.compiled = StandardsEngine._compile(FrozenContentSource(cls.files))

    @classmethod
    def refresh(cls, files):
        return _refresh_suite_input_projection(files, frozenset(dict(cls.base.files)), cls.repository_paths)

    def test_readable_routing_uses_the_changed_display_without_old_heading(self):
        with tempfile.TemporaryDirectory() as temporary:
            with StandardsEngine.open_repository(Path(temporary), durable=False, purpose='authoring') as engine:
                summary = engine._snapshots.create_snapshot(CapturedContent('router-display-fixture', (
                    SnapshotFile(SnapshotPath.parse(path), data) for path, data in self.files.items())))
                result = engine._read(SnapshotHandle.from_value(engine._snapshot_handle(summary.snapshot)), self.compiled,
                                      ReadRequest.from_value({'kind': 'read', 'target': 'router', 'include_routing': True}))
                value = result.as_contract()
                self.assertEqual(value['kind'], 'read-result', value)
                self.assertEqual(len(value['routing']['rules']), len(self.compiled.router.rules))
                self.assertNotIn('S1 Rust', value['content'])

    def test_edit_preserves_nonselection_content_and_remains_compilable(self):
        files = dict(self.files)
        before = files['STANDARDS-ROUTER.md'].decode()
        guidance = parse_router_guidance(before, self.compiled.corpus.module_corpus)
        target = 'workflow.implementation'
        row, = [row for row in guidance.rows if target in row.targets]
        _project_route_guidance(files, [(target, target, 'Update A | B explicitly.')])
        after = files['STANDARDS-ROUTER.md'].decode()
        self.assertTrue(after.startswith(before[:row.start]))
        self.assertTrue(after.endswith(before[row.end:]))
        self.refresh(files)
        compiled = StandardsEngine._compile(FrozenContentSource(files))
        changed = next(row for row in parse_router_guidance(after, compiled.corpus.module_corpus).rows if target in row.targets)
        self.assertEqual(changed.condition, 'Update A | B explicitly.')

    def test_retarget_swap_and_removal_are_simultaneous_row_edits(self):
        files = dict(self.files)
        targets = ('workflow.implementation', 'workflow.verification')
        _project_route_guidance(files, [(targets[0], targets[1], 'First decision'), (targets[1], targets[0], 'Second decision')])
        text = files['STANDARDS-ROUTER.md'].decode()
        rows = parse_router_guidance(text, self.compiled.corpus.module_corpus).rows
        self.assertEqual(next(row.condition for row in rows if targets[1] in row.targets), 'First decision')
        self.assertEqual(next(row.condition for row in rows if targets[0] in row.targets), 'Second decision')
        _project_route_guidance(files, [(targets[0], None, None)])
        self.assertNotIn(targets[0], parse_router_guidance(files['STANDARDS-ROUTER.md'].decode(), self.compiled.corpus.module_corpus).targets)
        _project_route_guidance(files, [(None, targets[0], 'Restored explicit route')])
        self.refresh(files)
        self.assertIsNotNone(StandardsEngine._compile(FrozenContentSource(files)))
