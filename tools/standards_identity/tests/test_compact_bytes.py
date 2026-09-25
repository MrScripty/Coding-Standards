"""Exact identity-v2 byte-array behavior, independent of the compact encoder."""
from __future__ import annotations

import hashlib
import random
import struct
import unittest
from dataclasses import FrozenInstanceError
from unittest import mock

from tools.standards_identity.standards_identity import (
    IdentityArray, IdentityError, IdentityObject, encode_identity_value,
    frame_path_byte_set, frame_path_bytes, hash_identity,
)
from tools.standards_identity.standards_identity import encoding


class CompactByteEncodingTest(unittest.TestCase):
    def test_exact_preimages_and_hashes_across_chunk_boundaries(self):
        rng = random.Random(73129)
        cases = [b"", bytes(range(256)), b"\x00", b"\xff"]
        for size in (65535, 65536, 65537, 131072, 131073):
            cases.append(rng.randbytes(size))
        for content in cases:
            with self.subTest(length=len(content)):
                expected = b"[" + b",".join(str(byte).encode("ascii") for byte in content) + b"]"
                compact = IdentityArray(content)
                self.assertEqual(encode_identity_value(compact), expected)
                domain, prefix = b"test.bytes", b"bytes"
                frame = (b"coding-standards:identity:v2\0"
                         + struct.pack(">I", len(domain)) + domain
                         + struct.pack(">I", len(prefix)) + prefix
                         + struct.pack(">Q", len(expected)) + expected)
                self.assertEqual(hash_identity("test.bytes", "bytes", compact),
                                 "bytes:sha256:" + hashlib.sha256(frame).hexdigest())

    def test_observation_equality_and_hash_remain_sequence_based(self):
        content = bytes(range(256))
        compact = IdentityArray(content)
        ordinary = IdentityArray(tuple(content))
        self.assertEqual(compact, ordinary)
        self.assertEqual(ordinary, compact)
        self.assertEqual(compact.values, tuple(content))
        self.assertIs(type(compact.values), tuple)
        self.assertEqual(hash(compact), hash(ordinary))
        self.assertEqual(repr(compact), repr(ordinary))
        self.assertNotEqual(compact, IdentityArray(content[::-1]))
        with self.assertRaises((FrozenInstanceError, TypeError, AttributeError)):
            compact.values = ()

    def test_mutable_and_subclass_iterables_retain_validation(self):
        mutable = bytearray(b"abc")
        selected = IdentityArray(mutable)
        mutable[0] = 0
        self.assertEqual(encode_identity_value(selected), b"[97,98,99]")

        class InvalidBytes(bytes):
            def __iter__(self):
                return iter((0.5,))

        with self.assertRaises(IdentityError) as caught:
            IdentityArray(InvalidBytes(b"abc"))
        self.assertEqual(caught.exception.failure.code, "IDENTITY.INVALID_VALUE")
        for value in (mutable, memoryview(b"abc"), InvalidBytes(b"abc")):
            with self.assertRaises(IdentityError) as caught:
                frame_path_bytes(("file",), value)
            self.assertEqual(caught.exception.failure.code, "IDENTITY.INVALID_BYTES_FRAME")
        with self.assertRaises(IdentityError) as caught:
            encode_identity_value(b"abc")
        self.assertEqual(caught.exception.failure.code, "IDENTITY.INVALID_VALUE")

    def test_path_framing_keeps_order_unicode_and_arbitrary_integer_behavior(self):
        entries = [(("é", "a"), b"\xff"), (("e\u0301",), b"\x00"), (("a",), b"")]
        frames = frame_path_byte_set(entries)
        ordinary = IdentityArray(
            IdentityObject((("path", IdentityArray(path)), ("bytes", IdentityArray(tuple(content)))))
            for path, content in sorted(entries)
        )
        self.assertEqual(frames, ordinary)
        self.assertEqual(encode_identity_value(frames), encode_identity_value(ordinary))
        huge = 10**5000
        mixed = IdentityArray((IdentityArray(b"\x00\xff"), True, huge, -huge))
        number = b"1" + b"0" * 5000
        self.assertEqual(encode_identity_value(mixed), b"[[0,255],true," + number + b",-" + number + b"]")

    def test_byte_input_avoids_per_element_validation_and_dispatch(self):
        payload = bytes(range(256)) * 1024
        with mock.patch.object(encoding, "_validate_value", wraps=encoding._validate_value) as validation:
            value = frame_path_bytes(("payload",), payload)
        self.assertLess(validation.call_count, 10)
        with mock.patch.object(encoding, "_encode", wraps=encoding._encode) as encode:
            result = encode_identity_value(value)
        self.assertLess(encode.call_count, 10)
        self.assertTrue(result.endswith(b',"path":["payload"]}'))
