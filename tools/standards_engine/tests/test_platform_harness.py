from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.standards_engine.tests.platform_harness import (
    REPOSITORY_ROOT,
    HarnessError,
    _concurrent_probe,
    consume,
    produce,
)


class PlatformHarnessTest(unittest.TestCase):
    def test_closed_store_round_trip_uses_public_operations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            producer_store = root / "producer.sqlite3"
            producer_manifest = root / "manifest.json"
            produced = produce(REPOSITORY_ROOT, producer_store, producer_manifest)
            consumer_store = root / "consumer.sqlite3"
            shutil.copyfile(producer_store, consumer_store)

            consumed = consume(consumer_store, producer_manifest)

        self.assertEqual(produced["kind"], "a1c-platform-produce-result")
        self.assertEqual(consumed["kind"], "a1c-platform-consume-result")
        self.assertEqual(consumed["store_sha256"], produced["store_sha256"])
        self.assertEqual(
            consumed["concurrent_probe"],
            {
                "kind": "a1c-platform-concurrent-probe-result",
                "content_sha256": produced["content_sha256"],
            },
        )
        self.assertFalse(consumed["canonical_source_repository_used"])
        self.assertEqual(
            consumed["operations"],
            [
                "create-snapshot",
                "find-snapshots",
                "delete-snapshot",
                "undelete-snapshot",
                "query",
                "prepare",
                "resolve",
                "inspect",
            ],
        )

    def test_consume_rejects_changed_store_before_open(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            store = root / "standards.sqlite3"
            manifest = root / "manifest.json"
            store.write_bytes(b"changed")
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "producer": {},
                        "store": {"sha256": "sha256:invalid", "size": 7},
                        "snapshot": {},
                        "policy": {},
                        "analysis": {},
                        "analysis_child": {},
                        "resolved_analysis": {},
                        "read": {},
                        "operations": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(HarnessError, "bytes do not match"):
                consume(store, manifest)

    def test_concurrent_probe_rejects_mismatched_content(self) -> None:
        completed = subprocess.CompletedProcess(
            args=(),
            returncode=0,
            stdout=json.dumps(
                {
                    "kind": "a1c-platform-concurrent-probe-result",
                    "content_sha256": "sha256:other",
                }
            ),
            stderr="",
        )

        with (
            patch(
                "tools.standards_engine.tests.platform_harness.subprocess.run",
                return_value=completed,
            ),
            self.assertRaisesRegex(HarnessError, "mismatched evidence"),
        ):
            _concurrent_probe(
                Path("/repository"),
                Path("/store"),
                Path("/manifest"),
                "sha256:expected",
            )


if __name__ == "__main__":
    unittest.main()
