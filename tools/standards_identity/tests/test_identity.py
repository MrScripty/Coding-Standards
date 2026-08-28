from __future__ import annotations

import hashlib
import struct
import unittest

from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityError,
    IdentityObject,
    encode_identity_value,
    hash_identity,
)


class IdentityEncodingTest(unittest.TestCase):
    def test_encodes_every_supported_value_with_exact_bytes(self) -> None:
        value = IdentityObject(
            (
                ("z", None),
                ("array", IdentityArray((False, True, -12, 0, 34))),
                ("text", 'quote" slash\\ controls\x00\x1f /'),
            )
        )

        self.assertEqual(
            encode_identity_value(value),
            b'{"array":[false,true,-12,0,34],'
            b'"text":"quote\\" slash\\\\ controls\\u0000\\u001f /",'
            b'"z":null}',
        )

    def test_preserves_unicode_codepoints_and_sorts_keys_by_codepoint(self) -> None:
        composed = "\u00e9"
        decomposed = "e\u0301"
        self.assertNotEqual(
            encode_identity_value(composed),
            encode_identity_value(decomposed),
        )
        self.assertEqual(
            encode_identity_value(
                IdentityObject(((composed, composed), (decomposed, decomposed)))
            ),
            b'{"e\xcc\x81":"e\xcc\x81","\xc3\xa9":"\xc3\xa9"}',
        )

    def test_preserves_array_order_and_rejects_duplicate_object_keys(self) -> None:
        self.assertNotEqual(
            encode_identity_value(IdentityArray((1, 2))),
            encode_identity_value(IdentityArray((2, 1))),
        )
        with self.assertRaises(IdentityError) as caught:
            IdentityObject((("same", 1), ("same", 1)))
        self.assertEqual(caught.exception.failure.code, "IDENTITY.DUPLICATE_OBJECT_KEY")

    def test_boolean_and_integer_are_distinct_and_unbounded(self) -> None:
        self.assertEqual(encode_identity_value(True), b"true")
        self.assertEqual(encode_identity_value(1), b"1")
        self.assertNotEqual(encode_identity_value(True), encode_identity_value(1))
        huge = 10**5000
        expected = b"1" + b"0" * 5000
        self.assertEqual(encode_identity_value(huge), expected)
        self.assertEqual(encode_identity_value(-huge), b"-" + expected)

        formerly_supported = (
            -(10**4299),
            -(10**18 + 1),
            -(10**9),
            -1,
            0,
            1,
            10**9 - 1,
            10**9,
            10**18 + 1,
            10**4299,
        )
        for value in formerly_supported:
            with self.subTest(value=value):
                self.assertEqual(
                    encode_identity_value(value), str(value).encode("ascii")
                )

    def test_rejects_mutable_floating_subclass_and_invalid_unicode_values(self) -> None:
        class IntegerSubclass(int):
            pass

        invalid_values = ([], {}, 1.0, IntegerSubclass(1), bytearray(b"x"))
        for value in invalid_values:
            with self.subTest(value=value), self.assertRaises(IdentityError):
                encode_identity_value(value)  # type: ignore[arg-type]

        with self.assertRaises(IdentityError) as caught:
            encode_identity_value("\ud800")
        self.assertEqual(caught.exception.failure.code, "IDENTITY.INVALID_UNICODE")
        with self.assertRaises(IdentityError):
            IdentityObject((("\udfff", 1),))

    def test_hash_uses_exact_domain_separated_length_frame(self) -> None:
        domain = "coding-standards:test.v2"
        prefix = "example"
        encoded = b'{"value":"\xc3\xa9"}'
        value = IdentityObject((("value", "\u00e9"),))
        frame = b"".join(
            (
                b"coding-standards:identity:v2\0",
                struct.pack(">I", len(domain)),
                domain.encode("ascii"),
                struct.pack(">I", len(prefix)),
                prefix.encode("ascii"),
                struct.pack(">Q", len(encoded)),
                encoded,
            )
        )

        self.assertEqual(
            hash_identity(domain, prefix, value),
            f"example:sha256:{hashlib.sha256(frame).hexdigest()}",
        )
        self.assertNotEqual(
            hash_identity(domain, prefix, value),
            hash_identity(f"{domain}.other", prefix, value),
        )

    def test_domain_and_prefix_grammar_is_closed(self) -> None:
        value = IdentityObject(())
        valid = hash_identity("a", "a", value)
        self.assertRegex(valid, r"\Aa:sha256:[0-9a-f]{64}\Z")

        for domain in ("", "A", "-a", "a/b", "\u00e9"):
            with self.subTest(domain=domain), self.assertRaises(IdentityError):
                hash_identity(domain, "valid", value)
        for prefix in ("", "A", "1a", "a:b", "\u00e9"):
            with self.subTest(prefix=prefix), self.assertRaises(IdentityError):
                hash_identity("valid", prefix, value)


if __name__ == "__main__":
    unittest.main()
