from __future__ import annotations

import stat
import os
import tempfile
import unittest
from pathlib import Path

from tools.standards_authority.standards_authority import (
    AuthorityError,
    open_default_store,
)


class PlatformStoreTests(unittest.TestCase):
    def test_default_store_is_private_local_ext4_state(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            with open_default_store(root) as store:
                self.assertEqual(
                    store.path, root / ".standards-engine" / "authority.sqlite3"
                )
            self.assertEqual(
                stat.S_IMODE((root / ".standards-engine").stat().st_mode), 0o700
            )
            self.assertEqual(
                stat.S_IMODE(
                    (root / ".standards-engine" / "authority.sqlite3").stat().st_mode
                ),
                0o600,
            )

    def test_redirected_or_nonprivate_store_roots_reject(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            target = root / "target"
            target.mkdir()
            os.symlink(target, root / "redirected")
            with self.assertRaises(AuthorityError) as redirected:
                open_default_store(root / "redirected")
            self.assertEqual(redirected.exception.failure.kind, "unsupported")

            state = target / ".standards-engine"
            state.mkdir(mode=0o755)
            with self.assertRaises(AuthorityError) as mode:
                open_default_store(target)
            self.assertEqual(mode.exception.failure.code, "STORE.ROOT_MODE")


if __name__ == "__main__":
    unittest.main()
