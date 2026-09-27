"""Logical names resolve from their registered view, not the ambient worktree."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.graph_engine.graph_engine import (
    EdgeRegistry, GraphContribution, Node, PathEscapeError, Provenance, UnknownNodeError,
)


@dataclass(frozen=True)
class Source:
    id: str
    contribution: GraphContribution

    def load(self):
        return self.contribution


class LogicalResolutionTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        provenance = Provenance('logical', 'provider', 'fixture')
        self.source = Source('logical', GraphContribution(
            (Node('policy', ('registered', 'docs/policy.md'), provenance),), (), ()))
        self.registry = EdgeRegistry(self.root, (self.source,),
            logical_artifacts=('registered', 'docs/policy.md', 'unregistered'))

    def assert_unknown(self, name):
        with self.assertRaises(UnknownNodeError) as caught:
            self.registry.resolve(name)
        self.assertEqual(caught.exception.code, 'GRAPH.UNKNOWN_NODE')

    def test_bare_and_nested_names_ignore_created_and_removed_artifacts(self):
        for name in ('unregistered', 'docs/unregistered'):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            for kind in ('file', 'directory', 'symlink', 'dangling-symlink'):
                with self.subTest(name=name, kind=kind):
                    self.assert_unknown(name)
                    if kind == 'file':
                        target.write_text('unrelated')
                    elif kind == 'directory':
                        target.mkdir()
                    else:
                        target.symlink_to(self.root if kind == 'symlink' else self.root / 'missing')
                    try:
                        self.assert_unknown(name)
                    finally:
                        # Keep a failed regression independent of later cases.
                        if kind == 'directory':
                            target.rmdir()
                        else:
                            target.unlink()
                    self.assert_unknown(name)

    def test_logical_resolution_does_not_call_filesystem_after_construction(self):
        with patch.object(Path, 'exists', side_effect=AssertionError('live existence')), \
             patch.object(Path, 'resolve', side_effect=AssertionError('live resolution')):
            for name in ('policy', 'registered', 'docs/policy.md'):
                self.assertEqual(self.registry.resolve(name), 'policy')
            for name in ('unregistered', 'docs/unregistered'):
                self.assert_unknown(name)

    def test_logical_path_errors_and_registered_aliases_remain_stable(self):
        for name in ('../outside', '/absolute', './noncanonical', 'a//b'):
            with self.subTest(name=name), self.assertRaises(PathEscapeError):
                self.registry.resolve(name)
        (self.root / 'registered').symlink_to('/outside-the-logical-view')
        self.assertEqual(self.registry.resolve('registered'), 'policy')
        self.assertEqual(self.registry.resolve('policy'), 'policy')

    def test_filesystem_mode_preserves_unconnected_artifacts_and_containment(self):
        registry = EdgeRegistry(self.root, ())
        for name in ('unconnected', 'docs/unconnected'):
            target = self.root / name
            target.parent.mkdir(exist_ok=True)
            target.write_text('filesystem mode')
            self.assertEqual(registry.resolve(name), name)
            target.unlink()
        with self.assertRaises(UnknownNodeError):
            registry.resolve('unconnected')
        (self.root / 'outside').symlink_to(self.root.parent)
        with self.assertRaises(PathEscapeError):
            registry.resolve('outside')
