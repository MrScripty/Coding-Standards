"""Independent Git oracles for the opt-in committed patch boundary."""
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.repository_git.repository_git import GitRepository, GitRepositoryError, RepositoryRevision
from tools.repository_git.repository_git import repository as implementation


class ExactPatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'source'
        self.root.mkdir()
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        (self.root / 'text').write_bytes(b'before\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'before')
        self.before = RepositoryRevision(self.git('rev-parse', 'HEAD').strip())
        (self.root / 'text').write_bytes(b'after\n')
        self.git('commit', '-qam', 'after')
        self.after = RepositoryRevision(self.git('rev-parse', 'HEAD').strip())
        self.repository = GitRepository(self.root)

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True)

    def test_literal_patch_and_control_directory(self):
        before_blob = self.git('rev-parse', self.before.oid + ':text').strip()
        after_blob = self.git('rev-parse', self.after.oid + ':text').strip()
        expected = (f'diff --git a/text b/text\nindex {before_blob}..{after_blob} 100644\n'
                    '--- a/text\n+++ b/text\n@@ -1 +1 @@\n-before\n+after\n').encode()
        self.assertEqual(self.repository.revision_patch(self.before, self.after), expected)
        self.assertEqual(self.repository.control_directories(local_only=True), (self.root / '.git',))
        self.assertEqual(self.repository.revision_patch(self.after, self.after), b'')

    def test_linked_layout_returns_both_roots(self):
        linked = self.root.parent / 'linked'
        self.git('worktree', 'add', '--detach', str(linked), self.after.oid)
        other = GitRepository(linked)
        self.assertEqual(other.control_directories(local_only=True),
                         (self.root / '.git/worktrees/linked', self.root / '.git'))
        self.assertEqual(other.revision_patch(self.before, self.after),
                         self.repository.revision_patch(self.before, self.after))
        (self.root / '.git/info/attributes').write_text('* -diff\n')
        with self.assertRaises(GitRepositoryError) as raised:
            other.revision_patch(self.before, self.after)
        self.assertEqual(raised.exception.failure.code, 'REPOSITORY_GIT.PATCH_CONFIGURATION')

    def test_tree_ids_and_unbounded_requests_reject(self):
        tree = RepositoryRevision(self.git('rev-parse', 'HEAD^{tree}').strip())
        for args in ((tree, self.after), (self.before, tree), ('HEAD', self.after)):
            with self.subTest(args=args), self.assertRaises(GitRepositoryError) as raised:
                self.repository.revision_patch(*args)
            self.assertEqual(raised.exception.failure.kind, 'invalid')
        for limit in (0, -1, True):
            with self.subTest(limit=limit), self.assertRaises(GitRepositoryError) as raised:
                self.repository.revision_patch(self.before, self.after, max_output_bytes=limit)
            self.assertEqual(raised.exception.failure.code, 'REPOSITORY_GIT.INVALID_BOUND')
        with self.assertRaises(GitRepositoryError) as raised:
            self.repository.revision_patch(self.before, self.after, max_output_bytes=1)
        self.assertEqual(raised.exception.failure.code, 'REPOSITORY_GIT.OUTPUT_LIMIT')

    def test_patch_environment_is_local_and_attributes_are_fixed(self):
        observed = []
        original = implementation._git_output_with_environment
        def capture(root, arguments, environment, **kwargs):
            observed.append((arguments, environment))
            return original(root, arguments, environment, **kwargs)
        with patch.object(implementation, '_git_output_with_environment', side_effect=capture), \
             patch.dict(os.environ, {'GIT_EXTERNAL_DIFF': 'false', 'GIT_DIFF_OPTS': '-U90',
                                     'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'diff.noprefix',
                                     'GIT_CONFIG_VALUE_0': 'true', 'GIT_ATTR_SOURCE': self.before.oid}):
            self.repository.revision_patch(self.before, self.after)
        self.assertEqual(len(observed), 1)
        args, env = observed[0]
        for key in ('GIT_NO_LAZY_FETCH', 'GIT_NO_REPLACE_OBJECTS', 'GIT_ATTR_NOSYSTEM'):
            self.assertEqual(env[key], '1')
        self.assertEqual(env['GIT_ATTR_SOURCE'], self.after.oid)
        self.assertNotIn('GIT_CONFIG_COUNT', env)
        self.assertNotIn('GIT_EXTERNAL_DIFF', env)
        self.assertNotIn('GIT_DIFF_OPTS', env)
        self.assertIn('core.attributesFile=' + os.devnull, args)
        self.assertIn('core.ignoreCase=false', args)

    def test_info_attributes_appearing_during_patch_rejects_result(self):
        original = implementation._git_output_with_environment
        def changed(*args, **kwargs):
            output = original(*args, **kwargs)
            (self.root / '.git/info/attributes').write_text('* -diff\n')
            return output
        with patch.object(implementation, '_git_output_with_environment', side_effect=changed):
            with self.assertRaises(GitRepositoryError) as raised:
                self.repository.revision_patch(self.before, self.after)
        self.assertEqual(raised.exception.failure.code, 'REPOSITORY_GIT.PATCH_CONFIGURATION')

    def test_info_symlink_is_not_followed(self):
        outside = self.root.parent / 'outside-info'
        outside.mkdir()
        (outside / 'attributes').write_text('unchanged\n')
        (self.root / '.git/info').rename(self.root / '.git/old-info')
        (self.root / '.git/info').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(GitRepositoryError) as raised:
            self.repository.revision_patch(self.before, self.after)
        self.assertEqual(raised.exception.failure.kind, 'unsupported')
        self.assertEqual((outside / 'attributes').read_text(), 'unchanged\n')

    def test_context_order_and_quoting_ignore_local_diff_preferences(self):
        name = "é.txt"
        original = "\n".join(str(i) if i % 4 else "" for i in range(40)) + "\n"
        (self.root / name).write_text(original)
        self.git('add', name)
        self.git('commit', '-qm', 'multiline before')
        baseline = RepositoryRevision(self.git('rev-parse', 'HEAD').strip())
        (self.root / name).write_text(original.replace('7\n', 'seven\n').replace('31\n', 'thirty-one\n'))
        self.git('commit', '-qam', 'multiline after')
        candidate = RepositoryRevision(self.git('rev-parse', 'HEAD').strip())
        expected = self.repository.revision_patch(baseline, candidate)
        self.assertIn(b'@@ -', expected)
        self.assertIn(b'\\303\\251.txt', expected)
        for key, value in (('core.quotePath', 'false'), ('diff.context', '0'),
                           ('diff.interHunkContext', '100'), ('diff.suppressBlankEmpty', 'true')):
            self.git('config', key, value)
        ambient = subprocess.check_output(['git', '-C', str(self.root), 'diff',
                                          '--full-index', baseline.oid, candidate.oid])
        self.assertNotEqual(ambient, expected)
        self.assertEqual(self.repository.revision_patch(baseline, candidate), expected)


    def test_attribute_case_policy_is_fixed_without_reconfiguring_repository(self):
        (self.root / '.gitattributes').write_bytes(b'*.TXT -diff\n')
        names = ('data.txt', 'MATCH.TXT')
        for name in names:
            (self.root / name).write_bytes(b'before\n')
        self.git('add', '.gitattributes', *names)
        self.git('commit', '-qm', 'case-policy baseline')
        baseline = RepositoryRevision(self.git('rev-parse', 'HEAD').strip())
        for name in names:
            (self.root / name).write_bytes(b'after\n')
        self.git('commit', '-qam', 'case-policy candidate')
        candidate = RepositoryRevision(self.git('rev-parse', 'HEAD').strip())
        before_blob = self.git('rev-parse', baseline.oid + ':data.txt').strip()
        after_blob = self.git('rev-parse', candidate.oid + ':data.txt').strip()
        expected_text = (f'diff --git a/data.txt b/data.txt\n'
                         f'index {before_blob}..{after_blob} 100644\n'
                         '--- a/data.txt\n+++ b/data.txt\n@@ -1 +1 @@\n-before\n+after\n').encode()
        observed = []
        for configured in ('false', 'true'):
            self.git('config', 'core.ignoreCase', configured)
            protected = ('.git/config', '.git/index', '.git/HEAD', '.gitattributes', *names)
            original = {name: (self.root / name).read_bytes() for name in protected}
            refs = self.git('show-ref')
            value = self.repository.revision_patch(baseline, candidate)
            self.assertEqual({name: (self.root / name).read_bytes() for name in protected}, original)
            self.assertEqual(self.git('show-ref'), refs)
            self.assertEqual(self.git('config', '--get', 'core.ignoreCase').strip(), configured)
            binary, text = value.split(b'diff --git a/data.txt b/data.txt\n', 1)
            self.assertEqual(b'diff --git a/data.txt b/data.txt\n' + text, expected_text)
            self.assertTrue(binary.startswith(b'diff --git a/MATCH.TXT b/MATCH.TXT\n'))
            self.assertIn(b'GIT binary patch\n', binary)
            self.assertNotIn(b'@@', binary)
            observed.append(value)
        self.assertEqual(observed[0], observed[1])
