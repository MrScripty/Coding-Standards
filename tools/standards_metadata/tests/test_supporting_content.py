from __future__ import annotations

import json
import unittest

from tools.standards_metadata.standards_metadata import (
    APPLICATION_CONTENT, DECISION_PROVENANCE, FrozenContentSource,
    DecisionProvenance, MetadataError, load_supporting_content,
)


def inline(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ", ".join(inline(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{ " + ", ".join(f"{key} = {inline(item)}" for key, item in value.items()) + " }"
    return str(value)


def source(records=(), entries=()):
    return FrozenContentSource({
        DECISION_PROVENANCE: ("schema_version = 1\nrecords = " + inline(list(records)) + "\n").encode(),
        APPLICATION_CONTENT: ("schema_version = 1\nentries = " + inline(list(entries)) + "\n").encode(),
    })


def record(**changes):
    return {"id": "provenance.fixture", "subject": "core",
            "subject_binding": "sha256:" + "1" * 64, "origin": "current-justification",
            "rationale": "The selected operation preserves the required property.", "evidence": [], **changes}


class SupportingContentTest(unittest.TestCase):
    def test_empty_registration_is_an_honest_unreviewed_state(self):
        support = load_supporting_content(source())
        self.assertEqual(dict(support.provenance), {})
        self.assertEqual(support.exposure_state("core", "sha256:" + "1" * 64), "unreviewed")

    def test_binding_controls_current_and_stale_states(self):
        support = load_supporting_content(source(entries=[{"target": "core", "binding": "sha256:" + "1" * 64}]))
        self.assertEqual(support.exposure_state("core", "sha256:" + "1" * 64), "current")
        self.assertEqual(support.exposure_state("core", "sha256:" + "2" * 64), "needs-review")
        with self.assertRaises(TypeError):
            support.exposure["other"] = support.exposure["core"]

    def test_unknown_history_does_not_require_a_fabricated_reason(self):
        support = load_supporting_content(source(records=[record(origin="unrecorded", rationale="")]))
        self.assertEqual(support.provenance["provenance.fixture"].rationale, "")
        self.assertEqual(support.provenance["provenance.fixture"].evidence, ())

    def test_historical_claim_has_reference_shape_and_preserves_unicode(self):
        evidence = {"id": "evidence:case", "digest": "sha256:" + "a" * 64,
                    "provider_contract": "repository-content", "provider_contract_version": "1"}
        original = record(origin="documented-original", evidence=[evidence], rationale="Propriété 日本語 e\u0301")
        observed = load_supporting_content(source(records=[original])).provenance["provenance.fixture"]
        self.assertEqual(observed.rationale, original["rationale"])
        self.assertEqual(dict(observed.evidence[0]), evidence)
        for malformed in [record(origin="documented-original"), record(evidence=[evidence, evidence]),
                          record(subject_binding="guessed"), record(rationale="\ud800"),
                          record(extra="unknown"), record(retired=1)]:
            with self.subTest(malformed=malformed), self.assertRaises(MetadataError):
                DecisionProvenance.from_mapping(malformed)

    def test_supersession_uses_retained_distinct_records(self):
        older = record(retired=True)
        newer = record(id="provenance.newer", supersedes=[older["id"]])
        self.assertEqual(len(load_supporting_content(source(records=[newer, older])).provenance), 2)
        for rows in [[record(supersedes=["provenance.missing"])],
                     [record(supersedes=["provenance.newer"]), newer], [older, older]]:
            with self.assertRaises(MetadataError):
                load_supporting_content(source(records=rows))

    def test_unsupported_capture_does_not_become_an_empty_manifest(self):
        with self.assertRaises(MetadataError) as caught:
            load_supporting_content(FrozenContentSource({}))
        self.assertEqual(caught.exception.failure.code, "SUPPORT.UNSUPPORTED_CAPTURE")
        for data in [b"schema_version = true\nentries = []", b"schema_version = 99\nentries = []",
                     b"schema_version = 1\nentries = {}", b"not toml", b"\xff"]:
            files = dict(source().files)
            files[APPLICATION_CONTENT] = data
            with self.subTest(data=data), self.assertRaises(MetadataError):
                load_supporting_content(FrozenContentSource(files))
