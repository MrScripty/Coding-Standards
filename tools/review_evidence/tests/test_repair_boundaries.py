"""Real Git and deterministic filesystem regressions for review findings F1-F4."""
from __future__ import annotations

import os
import unittest
import zipfile
from unittest.mock import patch

from tools.repository_git.repository_git import GitRepositoryError
from tools.review_evidence.review_evidence import packet
from tools.review_evidence.review_evidence.common import PacketError, check_names
from tools.review_evidence.tests import test_cli as fixture


class ReviewRepairTests(unittest.TestCase):
    setUp = fixture.PacketBuildTests.setUp
    git = fixture.PacketBuildTests.git
    write_request = fixture.PacketBuildTests.write_request
    build = fixture.PacketBuildTests.build

    def test_linked_worktree_common_gitdir_is_protected(self):
        linked = self.repo.parent / 'linked'
        self.git('worktree', 'add', '--detach', str(linked), self.candidate)
        self.write_request()
        for parent in (self.repo / '.git', self.repo / '.git/worktrees/linked'):
            output = parent / 'packet.zip'
            with self.subTest(parent=parent), self.assertRaises(PacketError):
                packet.build(linked, self.request_path, self.evidence, output)
            self.assertFalse(output.exists())
            self.assertEqual(list(parent.glob('.review-evidence-*')), [])
        self.assertEqual(packet.build(linked, self.request_path, self.evidence, self.out)['status'], 'built')

    def test_portable_file_directory_and_spelling_conflicts(self):
        for names in (['A', 'a/file'], ['a/file', 'A'], ['A/one', 'a/two'],
                      ['\u00e9/one', 'e\u0301/two'], ['same', 'SAME']):
            with self.subTest(names=names), self.assertRaises(PacketError):
                check_names(names)
        check_names(['shared/one', 'shared/two', 'separate/one'])

    def test_git_info_attributes_are_explicitly_unsupported(self):
        info = self.repo / '.git/info/attributes'
        info.write_text('*.txt -diff\n')
        original = info.read_bytes()
        with self.assertRaises(GitRepositoryError) as raised:
            self.build()
        self.assertEqual(raised.exception.failure.kind, 'unsupported')
        self.assertFalse(self.out.exists())
        self.assertEqual(info.read_bytes(), original)

    def test_local_diff_prefix_does_not_change_exact_patch(self):
        self.build()
        with zipfile.ZipFile(self.out) as z:
            expected = z.read('changes/baseline-candidate.patch')
        self.out.unlink()
        self.git('config', 'diff.noprefix', 'true')
        self.git('config', 'diff.mnemonicPrefix', 'true')
        self.build()
        with zipfile.ZipFile(self.out) as z:
            self.assertEqual(z.read('changes/baseline-candidate.patch'), expected)
        self.assertEqual(self.git('config', 'diff.noprefix').strip(), 'true')

    def test_output_swap_before_staging_does_not_follow_replacement(self):
        parent = self.repo.parent / 'output'
        parent.mkdir()
        old = self.repo.parent / 'old-output'
        self.out = parent / 'packet.zip'
        original = os.open
        interleaved = []

        def swapped(name, *args, **kwargs):
            if isinstance(name, str) and name.startswith('.review-evidence-'):
                parent.rename(old)
                parent.symlink_to(self.repo, target_is_directory=True)
                interleaved.append(name)
            return original(name, *args, **kwargs)

        with patch.object(packet.os, 'open', side_effect=swapped):
            with self.assertRaises(PacketError) as raised:
                self.build()
        self.assertEqual(raised.exception.kind, 'unavailable')
        self.assertEqual(len(interleaved), 1)
        self.assertFalse((self.repo / 'packet.zip').exists())
        self.assertEqual(list(self.repo.glob('.review-evidence-*')), [])
        self.assertEqual(list(old.iterdir()), [])

    def test_output_swap_after_validation_keeps_cleanup_in_original_directory(self):
        parent = self.repo.parent / 'output'
        parent.mkdir()
        old = self.repo.parent / 'old-output'
        self.out = parent / 'packet.zip'
        validate = packet._validate_staged
        interleaved = []

        def swapped(stream):
            result = validate(stream)
            names = [p.name for p in parent.glob('.review-evidence-*')]
            self.assertEqual(len(names), 1)
            parent.rename(old)
            parent.symlink_to(self.evidence, target_is_directory=True)
            (self.evidence / names[0]).write_bytes(b'not owned by builder')
            interleaved.extend(names)
            return result

        with patch.object(packet, '_validate_staged', side_effect=swapped):
            with self.assertRaises(PacketError) as raised:
                self.build()
        self.assertEqual(raised.exception.kind, 'unavailable')
        self.assertEqual(list(old.iterdir()), [])
        self.assertFalse((self.evidence / 'packet.zip').exists())
        self.assertEqual((self.evidence / interleaved[0]).read_bytes(), b'not owned by builder')

    def test_swap_inside_link_cannot_redirect_publication_or_rollback(self):
        parent = self.repo.parent / 'output'
        parent.mkdir()
        old = self.repo.parent / 'old-output'
        self.out = parent / 'packet.zip'
        link = os.link
        interleaved = []

        def swapped(source, destination, **kwargs):
            self.assertIn('src_dir_fd', kwargs)
            self.assertIn('dst_dir_fd', kwargs)
            parent.rename(old)
            parent.symlink_to(self.repo, target_is_directory=True)
            (self.repo / destination).write_bytes(b'other destination')
            interleaved.append(True)
            return link(source, destination, **kwargs)

        with patch.object(packet.os, 'link', side_effect=swapped):
            with self.assertRaises(PacketError) as raised:
                self.build()
        self.assertEqual(raised.exception.kind, 'unavailable')
        self.assertEqual(interleaved, [True])
        self.assertEqual((self.repo / 'packet.zip').read_bytes(), b'other destination')
        self.assertEqual(list(old.iterdir()), [])
        self.assertEqual(list(self.repo.glob('.review-evidence-*')), [])

    def test_evidence_root_ancestor_replacement_is_not_followed(self):
        from tools.review_evidence.review_evidence.local_files import LocalDirectory, read_regular
        ancestor = self.repo.parent / 'evidence-parent'
        ancestor.mkdir()
        selected = ancestor / 'selected'
        selected.mkdir()
        (selected / 'log').write_bytes(b'admitted bytes')
        replacement = self.repo.parent / 'other-evidence-parent'
        (replacement / 'selected').mkdir(parents=True)
        (replacement / 'selected/log').write_bytes(b'wrong bytes')
        old = self.repo.parent / 'old-evidence-parent'
        with LocalDirectory(selected) as directory:
            ancestor.rename(old)
            ancestor.symlink_to(replacement, target_is_directory=True)
            with self.assertRaises(PacketError) as raised:
                read_regular(directory, 'log', 1024)
        self.assertEqual(raised.exception.kind, 'unavailable')
        self.assertEqual((replacement / 'selected/log').read_bytes(), b'wrong bytes')

    def test_evidence_swap_between_check_and_leaf_open_cannot_supply_new_bytes(self):
        from tools.review_evidence.review_evidence.local_files import LocalDirectory, read_regular
        (self.evidence / 'log').write_bytes(b'admitted bytes')
        (self.repo / 'log').write_bytes(b'wrong bytes')
        old = self.repo.parent / 'old-evidence'
        original = os.open
        opened = []

        def swapped(name, *args, **kwargs):
            if name == 'log':
                self.evidence.rename(old)
                self.evidence.symlink_to(self.repo, target_is_directory=True)
                descriptor = original(name, *args, **kwargs)
                opened.append(os.read(descriptor, 100))
                os.lseek(descriptor, 0, os.SEEK_SET)
                return descriptor
            return original(name, *args, **kwargs)

        with LocalDirectory(self.evidence) as directory:
            with patch.object(os, 'open', side_effect=swapped):
                with self.assertRaises(PacketError) as raised:
                    read_regular(directory, 'log', 1024)
        self.assertEqual(raised.exception.kind, 'unavailable')
        self.assertEqual(opened, [b'admitted bytes'])

    def test_missing_evidence_still_rejects_a_replaced_root(self):
        from tools.review_evidence.review_evidence.local_files import LocalDirectory, read_regular
        old = self.repo.parent / 'old-evidence'
        original = os.open
        def swapped(name, *args, **kwargs):
            if name == 'missing.log':
                self.evidence.rename(old)
                self.evidence.symlink_to(self.repo, target_is_directory=True)
            return original(name, *args, **kwargs)
        with LocalDirectory(self.evidence) as directory:
            with patch.object(os, 'open', side_effect=swapped):
                with self.assertRaises(PacketError) as raised:
                    read_regular(directory, 'missing.log', 1024)
        self.assertEqual(raised.exception.kind, 'unavailable')

    def test_separate_git_directory_is_protected(self):
        control = self.repo.parent / 'control'
        self.git('init', '--quiet', '--separate-git-dir', str(control))
        self.write_request()
        self.out = control / 'packet.zip'
        with self.assertRaises(PacketError):
            self.build()
        self.assertFalse(self.out.exists())
        self.out = self.repo.parent / 'outside.zip'
        self.assertEqual(self.build()['status'], 'built')

    def test_actual_git_prefix_collision_fails_before_publication(self):
        (self.repo / 'A').write_bytes(b'file')
        (self.repo / 'a').mkdir()
        (self.repo / 'a/child').write_bytes(b'child')
        self.git('add', 'A', 'a')
        self.git('commit', '-qm', 'ambiguous portable namespace')
        self.request['revisions']['candidate'] = self.git('rev-parse', 'HEAD').strip()
        with self.assertRaises(PacketError):
            self.build()
        self.assertFalse(self.out.exists())
        self.assertEqual(list(self.out.parent.glob('.review-evidence-*')), [])

    def test_staged_validator_uses_prefix_occupancy_too(self):
        import warnings
        for names in (('A', 'a/child'), ('A/one', 'a/two'), ('é/one', 'e\u0301/two')):
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', UserWarning)
                with zipfile.ZipFile(self.out, 'w') as z:
                    for name in (*names, 'manifest.json'):
                        z.writestr(packet.zip_info(name), b'x')
            with self.subTest(names=names), self.assertRaises(PacketError) as raised:
                packet._validate_staged(self.out)
            self.assertIn('portable packet path', str(raised.exception))
            self.out.unlink()

    def test_configured_attributes_and_diff_presentation_are_neutralized(self):
        self.build()
        original_packet = self.out.read_bytes()
        self.out.unlink()
        attributes = self.repo.parent / 'attributes'
        attributes.write_text('*.txt -diff\n')
        order = self.repo.parent / 'order'
        order.write_text('new.txt\nchanged.bin\ngone.txt\n')
        for key, value in (
            ('core.attributesFile', str(attributes)), ('core.quotePath', 'false'),
            ('core.bigFileThreshold', '1'), ('diff.noprefix', 'true'),
            ('diff.mnemonicPrefix', 'true'), ('diff.srcPrefix', 'different/'),
            ('diff.dstPrefix', 'other/'), ('diff.context', '0'),
            ('diff.interHunkContext', '100'), ('diff.algorithm', 'histogram'),
            ('diff.indentHeuristic', 'false'), ('diff.orderFile', str(order)),
            ('diff.suppressBlankEmpty', 'true'), ('diff.relative', 'true'),
        ):
            self.git('config', key, value)
        configuration = (self.repo / '.git/config').read_bytes()
        self.build()
        self.assertEqual(self.out.read_bytes(), original_packet)
        self.assertEqual((self.repo / '.git/config').read_bytes(), configuration)
        self.assertEqual(attributes.read_text(), '*.txt -diff\n')

    def test_custom_diff_semantics_reject_without_invoking_driver(self):
        (self.repo / '.gitattributes').write_text('*.txt diff=custom\n')
        self.git('add', '.gitattributes')
        self.git('commit', '-qm', 'authored driver selection')
        self.request['revisions']['candidate'] = self.git('rev-parse', 'HEAD').strip()
        marker = self.repo.parent / 'executed'
        self.git('config', 'diff.custom.command', 'touch ' + str(marker))
        for key, value in (('binary', 'true'), ('xfuncname', '^other'), ('algorithm', 'patience')):
            self.git('config', 'diff.custom.' + key, value)
            with self.subTest(key=key), self.assertRaises(GitRepositoryError) as raised:
                self.build()
            self.assertEqual(raised.exception.failure.code, 'REPOSITORY_GIT.PATCH_CONFIGURATION')
            self.git('config', '--unset', 'diff.custom.' + key)
        self.assertFalse(marker.exists())
        self.assertFalse(self.out.exists())

    def test_committed_attributes_still_select_binary_representation(self):
        (self.repo / '.gitattributes').write_text('*.txt -diff\n')
        self.git('add', '.gitattributes')
        self.git('commit', '-qm', 'committed binary policy')
        self.request['revisions']['candidate'] = self.git('rev-parse', 'HEAD').strip()
        (self.repo / '.gitattributes').write_text('*.txt diff\n')
        self.build()
        with zipfile.ZipFile(self.out) as z:
            patch_bytes = z.read('changes/baseline-candidate.patch')
            start = patch_bytes.index(b'diff --git a/new.txt b/new.txt')
            self.assertIn(b'GIT binary patch', patch_bytes[start:])
            self.assertEqual(z.read('source/candidate/.gitattributes'), b'*.txt -diff\n')

    def test_new_directory_at_same_path_is_not_the_admitted_destination(self):
        parent = self.repo.parent / 'output'
        parent.mkdir()
        old = self.repo.parent / 'old-output'
        self.out = parent / 'packet.zip'
        validate = packet._validate_staged
        def changed(stream):
            result = validate(stream)
            parent.rename(old)
            parent.mkdir()
            return result
        with patch.object(packet, '_validate_staged', side_effect=changed):
            with self.assertRaises(PacketError) as raised:
                self.build()
        self.assertEqual(raised.exception.kind, 'unavailable')
        self.assertEqual(list(old.iterdir()), [])
        self.assertEqual(list(parent.iterdir()), [])

    def test_local_directory_closes_descriptors_on_success_and_failure(self):
        from pathlib import Path
        from tools.review_evidence.review_evidence.local_files import LocalDirectory, read_regular
        if not Path('/proc/self/fd').is_dir():
            self.skipTest('Linux descriptor observation required')
        before = len(list(Path('/proc/self/fd').iterdir()))
        for _ in range(3):
            with LocalDirectory(self.evidence) as directory:
                self.assertIsNone(read_regular(directory, 'not-present', 8))
                with self.assertRaises(PacketError):
                    directory.path = self.repo.parent / 'missing'
                    directory.assert_current()
            with self.assertRaises(PacketError):
                directory.assert_current()
        self.assertEqual(len(list(Path('/proc/self/fd').iterdir())), before)

    def test_portable_namespace_does_linear_component_work(self):
        from tools.review_evidence.review_evidence import common
        paths = ['/'.join(['nested'] * 128 + [leaf]) for leaf in ('one', 'two')]
        original = common.unicodedata.normalize
        with patch.object(common.unicodedata, 'normalize', wraps=original) as normalize:
            check_names(paths)
        self.assertEqual(normalize.call_count, 2 * 129)

    def test_cli_explains_unsupported_info_attributes_without_exposing_paths(self):
        import json
        import subprocess
        import sys
        from pathlib import Path
        attributes = self.repo / '.git/info/attributes'
        attributes.write_text('*.txt -diff\n')
        self.write_request()
        source_root = Path(__file__).resolve().parents[3]
        process = subprocess.run(
            [sys.executable, '-B', '-m', 'tools.review_evidence.review_evidence', 'build',
             '--repo-root', str(self.repo), '--request', str(self.request_path),
             '--output', str(self.out)], cwd=source_root,
            env={**os.environ, 'PYTHONPATH': str(source_root)}, capture_output=True, text=True,
        )
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stderr, '')
        result = json.loads(process.stdout)
        self.assertEqual(result, {'status': 'unsupported',
                                 'message': 'exact patch does not admit info attributes'})
        self.assertNotIn(str(self.repo), process.stdout)
        self.assertFalse(self.out.exists())
        self.assertEqual(attributes.read_text(), '*.txt -diff\n')
