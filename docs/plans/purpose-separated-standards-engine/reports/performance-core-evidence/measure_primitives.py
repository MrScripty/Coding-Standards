"""Measure exact identities and optional capture retention in disposable inputs."""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time
from unittest.mock import patch

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--store', type=Path, required=True)
parser.add_argument('--snapshot', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--capture', action='store_true')
a = parser.parse_args()
root = a.repo.resolve()
os.chdir(root)
sys.path.insert(0, str(root))
from tools.standards_engine.standards_engine import StandardsEngine
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_identity.standards_identity import encode_identity_value, frame_path_byte_set
from tools.standards_snapshots.standards_snapshots import SnapshotModule

rows = []

def timed(name, function):
    wall, cpu = time.perf_counter(), time.process_time()
    value = function()
    rows.append({'operation': name, 'wall_s': time.perf_counter() - wall,
                 'cpu_s': time.process_time() - cpu})
    return value

with StandardsEngine.open_repository(root, purpose='authoring', store_path=a.store.resolve()) as engine:
    handle = c.SnapshotHandle.from_value(json.loads(a.snapshot.read_text()))
    identity, capture = engine._snapshots._store.load_content(engine._snapshot_id(handle))
    entries = tuple((file.path.components, file.content) for file in capture.files)
    for repeat in range(5):
        frame = timed('frame', lambda: frame_path_byte_set(entries))
        encoded = timed('encode', lambda: encode_identity_value(frame))
        encoded_digest = hashlib.sha256(encoded).hexdigest()
        encoded_length = len(encoded)
        del frame, encoded
        gc.collect()
        observed = timed('complete_identity', lambda: SnapshotModule._content_id(capture))
        assert observed == identity, (observed, identity)
    result = {'measurements': rows, 'source_files': len(entries),
              'raw_bytes': sum(len(value) for _, value in entries),
              'content_identity': identity, 'encoded_sha256': encoded_digest,
              'encoded_bytes': encoded_length}

if a.capture:
    from tools.repository_git.repository_git import RevisionReadSession
    original_object = RevisionReadSession._object
    original_close = RevisionReadSession.close
    counts = {'requests': 0, 'peak_payload_bytes': 0, 'peak_entries': 0,
              'closed_payload_bytes': [], 'closed_entries': []}

    def observe_object(session, *args):
        value = original_object(session, *args)
        counts['requests'] += 1
        counts['peak_payload_bytes'] = max(counts['peak_payload_bytes'], session.cached_bytes)
        counts['peak_entries'] = max(counts['peak_entries'], session.cached_objects)
        return value

    def observe_close(session):
        original_close(session)
        counts['closed_payload_bytes'].append(session.cached_bytes)
        counts['closed_entries'].append(session.cached_objects)

    compiles = []
    original_compile = StandardsEngine._compile

    def observe_compile(source):
        compiles.append(source)
        return original_compile(source)

    with tempfile.TemporaryDirectory(prefix='capture-retention-') as temporary:
        with (patch.object(RevisionReadSession, '_object', observe_object),
              patch.object(RevisionReadSession, 'close', observe_close),
              patch.object(StandardsEngine, '_compile', staticmethod(observe_compile)),
              StandardsEngine.open_repository(root, purpose='authoring',
                  store_path=Path(temporary) / 'engine.sqlite3') as engine):
            created = engine.create_snapshot(c.CreateSnapshotCall(kind='create-snapshot'))
            assert isinstance(created, c.CreateSnapshotResult), created
            assert len(compiles) == 2 and compiles[0] is not compiles[1]
            assert compiles[0].requested_paths == compiles[1].requested_paths
    counts['independent_compiles'] = len(compiles)
    result['capture_retention'] = counts

a.output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
