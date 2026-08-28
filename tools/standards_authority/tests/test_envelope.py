from __future__ import annotations

import unittest

from tools.standards_authority.standards_authority import (
    AuthorityEnvelope,
    AuthorityError,
    AuthorityReference,
    decode_envelope,
    encode_envelope,
)
from tools.standards_authority.standards_authority.model import MAX_ENVELOPE_BYTES
from tools.standards_identity.standards_identity import IdentityObject


class EnvelopeTests(unittest.TestCase):
    def test_round_trip_preserves_codepoints_and_opaque_ids(self) -> None:
        envelope = AuthorityEnvelope(
            "κ-kind",
            "opaque:é:é",
            (AuthorityReference("child", "opaque-child"),),
            "payload.κ",
            IdentityObject((("value", "é"), ("other", "é"))),
        )
        encoded = encode_envelope(envelope)
        self.assertEqual(decode_envelope(encoded), envelope)

    def test_noncanonical_and_unknown_structural_contracts_reject(self) -> None:
        envelope = AuthorityEnvelope("kind", "id", (), "payload.v1", None)
        encoded = encode_envelope(envelope)
        with self.assertRaises(AuthorityError) as whitespace:
            decode_envelope(encoded.replace(b"{", b"{ ", 1))
        self.assertEqual(
            whitespace.exception.failure.code, "AUTHORITY.NONCANONICAL_ENVELOPE"
        )
        with self.assertRaises(AuthorityError) as version:
            decode_envelope(
                encoded.replace(b'"envelope_version":1', b'"envelope_version":2')
            )
        self.assertEqual(version.exception.failure.kind, "unsupported")

    def test_unsorted_duplicate_and_empty_values_reject(self) -> None:
        first = AuthorityReference("a", "1")
        second = AuthorityReference("b", "1")
        with self.assertRaises(AuthorityError):
            AuthorityEnvelope("kind", "id", (second, first), "payload", None)
        with self.assertRaises(AuthorityError):
            AuthorityEnvelope("kind", "id", (first, first), "payload", None)
        with self.assertRaises(AuthorityError):
            AuthorityEnvelope("", "id", (), "payload", None)

    def test_envelope_byte_bound_is_exact(self) -> None:
        empty = AuthorityEnvelope("kind", "id", (), "payload", "")
        overhead = len(encode_envelope(empty))
        at_bound = AuthorityEnvelope(
            "kind", "id", (), "payload", "x" * (MAX_ENVELOPE_BYTES - overhead)
        )
        self.assertEqual(len(encode_envelope(at_bound)), MAX_ENVELOPE_BYTES)
        above_bound = AuthorityEnvelope(
            "kind", "id", (), "payload", "x" * (MAX_ENVELOPE_BYTES - overhead + 1)
        )
        with self.assertRaises(AuthorityError) as raised:
            encode_envelope(above_bound)
        self.assertEqual(raised.exception.failure.kind, "unsupported")

    def test_arbitrary_length_integer_round_trips_without_global_limit_change(
        self,
    ) -> None:
        huge = 10**5000
        for value in (huge, -huge):
            with self.subTest(sign=value < 0):
                envelope = AuthorityEnvelope("kind", "id", (), "payload", value)
                self.assertEqual(decode_envelope(encode_envelope(envelope)), envelope)


if __name__ == "__main__":
    unittest.main()
