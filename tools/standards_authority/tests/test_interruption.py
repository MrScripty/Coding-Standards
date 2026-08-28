from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.standards_authority.standards_authority import (
    AuthorityEnvelope,
    AuthorityError,
    SQLiteObjectStore,
    encode_envelope,
)


class PublicationInterruptionTests(unittest.TestCase):
    def test_application_stage_interruptions_reopen_to_absent_or_complete(self) -> None:
        for stage, expected_present in (
            ("before-begin", False),
            ("after-begin", False),
            ("after-insert", False),
            ("before-commit", False),
            ("after-commit", True),
        ):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "authority.sqlite3"
                with SQLiteObjectStore(path):
                    pass
                result = subprocess.run(
                    (sys.executable, "-c", _worker_script(path, stage)), check=False
                )
                self.assertEqual(result.returncode, 73)
                envelope = AuthorityEnvelope(
                    "fixture", "interrupted", (), "fixture.v1", None
                )
                encoded = encode_envelope(envelope)
                with SQLiteObjectStore(path) as reopened:
                    if expected_present:
                        self.assertEqual(reopened.get(envelope.handle), encoded)
                    else:
                        with self.assertRaises(AuthorityError) as missing:
                            reopened.get(envelope.handle)
                        self.assertEqual(missing.exception.failure.kind, "unavailable")
                    self.assertIn(
                        reopened.put_if_absent(envelope.handle, encoded),
                        {"inserted", "existing-identical"},
                    )

    @unittest.skipUnless(
        os.environ.get("STANDARDS_REQUIRED_REAL_SQLITE") == "1",
        "required-real strace oracle is run explicitly",
    )
    def test_real_sqlite_commit_sync_is_interrupted_by_admitted_strace(self) -> None:
        self.assertEqual(
            hashlib.sha256(Path("/usr/bin/strace").read_bytes()).hexdigest(),
            "28f957c227012de0b18d1bd7fff2d396cb693ea60ed8013be68de071e84b5001",
        )
        self.assertEqual(
            hashlib.sha256(
                Path("/usr/share/doc/strace/copyright").read_bytes()
            ).hexdigest(),
            "40e4ca01654c733c06fabee65168da4c177117b1bd084f3a752bc8a989736e04",
        )
        self.assertEqual(
            hashlib.sha256(
                Path("/usr/share/common-licenses/LGPL-2.1").read_bytes()
            ).hexdigest(),
            "dc626520dcd53a22f727af3ee42c770e56c97a64fe3adb063799d8ab032fe551",
        )
        package = subprocess.run(
            ("dpkg-query", "-W", "-f=${Version}", "strace"),
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout
        self.assertEqual(package, "6.8-0ubuntu2")
        architecture = subprocess.run(
            ("dpkg-query", "-W", "-f=${Architecture}", "strace"),
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout
        self.assertEqual(architecture, "amd64")
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            probe_path = root / "probe.sqlite3"
            probe_marker = root / "probe-before-commit"
            probe_trace = root / "probe-trace.log"
            with SQLiteObjectStore(probe_path):
                pass
            probe = subprocess.run(
                (
                    "/usr/bin/strace",
                    "-e",
                    "trace=fsync,fdatasync",
                    "-o",
                    str(probe_trace),
                    sys.executable,
                    "-c",
                    _strace_worker_script(probe_path, probe_marker, "sync-probe"),
                ),
                check=False,
            )
            self.assertEqual(probe.returncode, 0)
            self.assertTrue(probe_marker.is_file())
            selected = next(
                (
                    syscall
                    for line in probe_trace.read_text().splitlines()
                    for syscall in ("fsync", "fdatasync")
                    if line.startswith(f"{syscall}(")
                ),
                None,
            )
            self.assertIn(selected, {"fsync", "fdatasync"})
            path = root / "authority.sqlite3"
            marker = root / "before-commit"
            trace = root / "trace.log"
            with SQLiteObjectStore(path):
                pass
            worker = _strace_worker_script(path, marker, "sync-kill")
            result = subprocess.run(
                (
                    "/usr/bin/strace",
                    "-e",
                    "trace=fsync,fdatasync",
                    f"--inject={selected}:signal=SIGKILL:when=1",
                    "-o",
                    str(trace),
                    sys.executable,
                    "-c",
                    worker,
                ),
                check=False,
            )
            self.assertTrue(marker.is_file(), "worker did not reach pre-commit barrier")
            trace_text = trace.read_text()
            self.assertIn(f"{selected}(", trace_text)
            self.assertIn("SIGKILL", trace_text)
            self.assertNotEqual(result.returncode, 0)
            envelope = AuthorityEnvelope("fixture", "sync-kill", (), "fixture.v1", None)
            encoded = encode_envelope(envelope)
            with SQLiteObjectStore(path) as reopened:
                self.assertEqual(
                    reopened.put_if_absent(envelope.handle, encoded), "inserted"
                )


def _worker_script(path: Path, stage: str) -> str:
    return f"""
import os
from pathlib import Path
from tools.standards_authority.standards_authority import *
class Interrupted(SQLiteObjectStore):
    def _publication_stage(self, current):
        if current == {stage!r}:
            os._exit(73)
store = Interrupted(Path({str(path)!r}))
envelope = AuthorityEnvelope('fixture', 'interrupted', (), 'fixture.v1', None)
store.put_if_absent(envelope.handle, encode_envelope(envelope))
raise AssertionError('interruption stage was not reached')
"""


def _strace_worker_script(path: Path, marker: Path, semantic_id: str) -> str:
    return f"""
from pathlib import Path
from tools.standards_authority.standards_authority import *
class Barrier(SQLiteObjectStore):
    def _publication_stage(self, current):
        if current == 'before-commit':
            Path({str(marker)!r}).write_text('reached')
store = Barrier(Path({str(path)!r}))
envelope = AuthorityEnvelope('fixture', {semantic_id!r}, (), 'fixture.v1', None)
store.put_if_absent(envelope.handle, encode_envelope(envelope))
"""


if __name__ == "__main__":
    unittest.main()
