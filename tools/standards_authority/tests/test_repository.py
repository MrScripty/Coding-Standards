from __future__ import annotations

import unittest

from tools.standards_authority.standards_authority import (
    AuthorityError,
    AuthorityHandle,
    AuthorityReference,
    AuthorityRepository,
    CodecSet,
    MemoryObjectStore,
    ContentSnapshotCodec,
)
from tools.standards_identity.standards_identity import IdentityObject
from tools.standards_authority.tests.support import FixtureCodec, FixtureValue
from tools.standards_authority.standards_authority import (
    AuthorityEnvelope,
    encode_envelope,
)


class AuthorityRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.child_codec = FixtureCodec("fixture-child", frozenset())
        self.root_codec = FixtureCodec("fixture-root", frozenset({"fixture-child"}))
        self.store = MemoryObjectStore()
        self.repository = AuthorityRepository(
            self.store, (CodecSet((self.child_codec, self.root_codec)),)
        )

    def test_publish_resolve_and_idempotence(self) -> None:
        child = FixtureValue("child")
        self.assertEqual(self.repository.publish(self.child_codec, child), "inserted")
        child_id = self.child_codec.semantic_id(child, self.repository)  # type: ignore[arg-type]
        child_ref = AuthorityReference("fixture-child", child_id)
        root = FixtureValue("root", (child_ref,))
        self.assertEqual(self.repository.publish(self.root_codec, root), "inserted")
        self.assertEqual(
            self.repository.publish(self.root_codec, root), "existing-identical"
        )
        root_id = self.root_codec.semantic_id(root, self.repository)  # type: ignore[arg-type]
        resolved = self.repository.resolve(AuthorityHandle("fixture-root", root_id))
        self.assertEqual(resolved.value, root)
        self.assertEqual(
            self.repository.transitive_dependencies((resolved.handle.reference,)),
            (child_ref, resolved.handle.reference),
        )

    def test_missing_dependency_is_unavailable(self) -> None:
        missing = AuthorityReference(
            "fixture-child", "fixture-child:sha256:" + "0" * 64
        )
        with self.assertRaises(AuthorityError) as raised:
            self.repository.publish(self.root_codec, FixtureValue("root", (missing,)))
        self.assertEqual(raised.exception.failure.kind, "unavailable")

    def test_disallowed_dependency_kind_is_invalid(self) -> None:
        child = FixtureValue("child")
        self.repository.publish(self.child_codec, child)
        child_id = self.child_codec.semantic_id(child, self.repository)  # type: ignore[arg-type]
        with self.assertRaises(AuthorityError) as raised:
            self.repository.publish(
                self.child_codec,
                FixtureValue("bad", (AuthorityReference("fixture-child", child_id),)),
            )
        self.assertEqual(
            raised.exception.failure.code, "AUTHORITY.DISALLOWED_DEPENDENCY_KIND"
        )

    def test_unknown_codec_is_unsupported(self) -> None:
        other = FixtureCodec("fixture-other", frozenset())
        with self.assertRaises(AuthorityError) as raised:
            self.repository.publish(other, FixtureValue("other"))
        self.assertEqual(raised.exception.failure.kind, "unsupported")

    def test_stored_unknown_owner_is_unsupported(self) -> None:
        store = MemoryObjectStore()
        envelope = AuthorityEnvelope("unknown-owner", "opaque", (), "unknown.v1", None)
        store.put_if_absent(envelope.handle, encode_envelope(envelope))
        repository = AuthorityRepository(store, (CodecSet(()),))
        with self.assertRaises(AuthorityError) as raised:
            repository.resolve(envelope.handle)
        self.assertEqual(raised.exception.failure.kind, "unsupported")

    def test_known_owner_rejects_invalid_payload(self) -> None:
        codec = ContentSnapshotCodec()
        store = MemoryObjectStore()
        repository = AuthorityRepository(store, (CodecSet((codec,)),))
        envelope = AuthorityEnvelope(
            codec.object_kind,
            "opaque-invalid",
            (),
            codec.payload_contract,
            IdentityObject((("unexpected", None),)),
        )
        store.put_if_absent(envelope.handle, encode_envelope(envelope))
        with self.assertRaises(AuthorityError) as raised:
            repository.resolve(envelope.handle)
        self.assertEqual(raised.exception.failure.kind, "invalid")

    def test_stored_cycle_is_invalid(self) -> None:
        class NameIdentityCodec(FixtureCodec):
            def semantic_id(self, value, context):  # type: ignore[no-untyped-def]
                del context
                return f"{self.object_kind}:{value.name}"

        codec = NameIdentityCodec("cycle", frozenset({"cycle"}))
        store = MemoryObjectStore()
        repository = AuthorityRepository(store, (CodecSet((codec,)),))
        one_ref = AuthorityReference("cycle", "cycle:one")
        two_ref = AuthorityReference("cycle", "cycle:two")
        one = FixtureValue("one", (two_ref,))
        two = FixtureValue("two", (one_ref,))
        for value in (one, two):
            envelope = AuthorityEnvelope(
                "cycle",
                codec.semantic_id(value, repository),  # type: ignore[arg-type]
                value.dependencies,
                codec.payload_contract,
                codec.encode(value),
            )
            store.put_if_absent(envelope.handle, encode_envelope(envelope))
        with self.assertRaises(AuthorityError) as raised:
            repository.resolve_reference(one_ref)
        self.assertEqual(raised.exception.failure.code, "AUTHORITY.DEPENDENCY_CYCLE")

    def test_storage_key_and_envelope_handle_must_agree(self) -> None:
        envelope = AuthorityEnvelope("fixture-child", "actual", (), "fixture.v1", None)
        wrong = AuthorityHandle("fixture-child", "wrong")
        self.store.put_if_absent(wrong, encode_envelope(envelope))
        with self.assertRaises(AuthorityError) as raised:
            self.repository.resolve(wrong)
        self.assertEqual(raised.exception.failure.code, "AUTHORITY.HANDLE_MISMATCH")

    def test_deep_closure_is_iterative(self) -> None:
        class NameIdentityCodec(FixtureCodec):
            def semantic_id(self, value, context):  # type: ignore[no-untyped-def]
                del context
                return f"{self.object_kind}:{value.name}"

        codec = NameIdentityCodec("deep", frozenset({"deep"}))
        store = MemoryObjectStore()
        repository = AuthorityRepository(store, (CodecSet((codec,)),))
        dependency: tuple[AuthorityReference, ...] = ()
        final_value: FixtureValue | None = None
        for index in range(1_500):
            value = FixtureValue(str(index), dependency)
            final_value = value
            envelope = AuthorityEnvelope(
                "deep",
                codec.semantic_id(value, repository),  # type: ignore[arg-type]
                dependency,
                codec.payload_contract,
                codec.encode(value),
            )
            store.put_if_absent(envelope.handle, encode_envelope(envelope))
            dependency = (envelope.handle.reference,)
        resolved = repository.resolve_reference(dependency[0])
        self.assertEqual(resolved.value, final_value)


if __name__ == "__main__":
    unittest.main()
