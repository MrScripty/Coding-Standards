from __future__ import annotations

import unittest

from tools.standards_authority.standards_authority import (
    AuthorityHandle,
    AuthorityReference,
    AuthorityRepository,
    CodecSet,
    ExecutionAuthorityRoot,
    ExecutionClosure,
    ExecutionClosureCodec,
    MemoryObjectStore,
)
from tools.standards_authority.tests.support import FixtureCodec, FixtureValue


class ExecutionClosureTests(unittest.TestCase):
    def test_roots_only_payload_binds_derived_transitive_closure(self) -> None:
        leaf_codec = FixtureCodec("fixture-leaf", frozenset())
        root_codec = FixtureCodec("fixture-root", frozenset({"fixture-leaf"}))
        closure_codec = ExecutionClosureCodec({"fixture-root", "fixture-leaf"})
        repository = AuthorityRepository(
            MemoryObjectStore(),
            (CodecSet((leaf_codec, root_codec, closure_codec)),),
        )
        leaf = FixtureValue("leaf")
        repository.publish(leaf_codec, leaf)
        leaf_ref = AuthorityReference(
            "fixture-leaf",
            leaf_codec.semantic_id(leaf, repository),  # type: ignore[arg-type]
        )
        root = FixtureValue("root", (leaf_ref,))
        repository.publish(root_codec, root)
        root_ref = AuthorityReference(
            "fixture-root",
            root_codec.semantic_id(root, repository),  # type: ignore[arg-type]
        )
        closure = ExecutionClosure(
            "read", (ExecutionAuthorityRoot("current", "metadata", root_ref),)
        )
        repository.publish(closure_codec, closure)
        closure_id = closure_codec.semantic_id(closure, repository)  # type: ignore[arg-type]
        resolved = repository.resolve(AuthorityHandle("execution-closure", closure_id))
        self.assertEqual(resolved.value, closure)
        self.assertEqual(resolved.envelope.direct_dependencies, (root_ref,))
        payload = closure_codec.encode(closure)
        self.assertNotIn("transitive_dependencies", dict(payload.members))  # type: ignore[union-attr]

    def test_root_order_is_not_identity(self) -> None:
        one = AuthorityReference("kind", "one")
        two = AuthorityReference("kind", "two")
        first = ExecutionAuthorityRoot("current", "a", one)
        second = ExecutionAuthorityRoot("current", "b", two)
        self.assertEqual(
            ExecutionClosure("route", (second, first)),
            ExecutionClosure("route", (first, second)),
        )


if __name__ == "__main__":
    unittest.main()
