from __future__ import annotations

import unittest

from tools.standards_authority.standards_authority import (
    AuthorityError,
    AuthorityRepository,
    CodecSet,
    ContentSnapshot,
    ContentSnapshotCodec,
    CaptureRequest,
    MemoryObjectStore,
    RepositoryPath,
    SnapshotFile,
)


class ContentSnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.codec = ContentSnapshotCodec()
        self.repository = AuthorityRepository(
            MemoryObjectStore(), (CodecSet("test", (self.codec,)),)
        )

    def test_path_and_input_order_do_not_change_identity(self) -> None:
        first = SnapshotFile(RepositoryPath(("a", "b.txt")), b"one")
        second = SnapshotFile(RepositoryPath(("z.txt",)), b"two")
        left = ContentSnapshot((second, first))
        right = ContentSnapshot((first, second))
        self.assertEqual(
            self.codec.semantic_id(left, self.repository),  # type: ignore[arg-type]
            self.codec.semantic_id(right, self.repository),  # type: ignore[arg-type]
        )
        self.repository.publish(self.codec, left)

    def test_codepoint_and_exact_byte_changes_change_identity(self) -> None:
        composed = ContentSnapshot((SnapshotFile(RepositoryPath(("é",)), b"x"),))
        decomposed = ContentSnapshot((SnapshotFile(RepositoryPath(("é",)), b"x"),))
        changed = ContentSnapshot((SnapshotFile(RepositoryPath(("é",)), b"y"),))
        ids = {
            self.codec.semantic_id(value, self.repository)  # type: ignore[arg-type]
            for value in (composed, decomposed, changed)
        }
        self.assertEqual(len(ids), 3)

    def test_path_contract_rejects_control_values(self) -> None:
        for components in ((), (".",), ("..",), (".git",), ("a/b",), ("a\0b",)):
            with self.subTest(components=components), self.assertRaises(AuthorityError):
                RepositoryPath(components)
        with self.assertRaises(AuthorityError):
            RepositoryPath(("x" * 256,))
        with self.assertRaises(AuthorityError):
            RepositoryPath(("\ud800",))
        with self.assertRaises(AuthorityError):
            CaptureRequest((RepositoryPath(("same",)), RepositoryPath(("same",))))
        self.assertEqual(
            RepositoryPath(("A", "back\\slash")).components, ("A", "back\\slash")
        )


if __name__ == "__main__":
    unittest.main()
