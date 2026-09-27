"""The three validated evidence representations share exact digest syntax."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
from tools.standards_analysis.standards_analysis import (
    AnalysisError, EvidenceReference as AnalysisEvidence, ResolvedEvidence,
)
from tools.standards_contracts.standards_contracts import ContractError
from tools.standards_engine.standards_engine import _generated_contract as generated
from tools.standards_engine.standards_engine.logical_authoring import EvidenceReference as AuthoringEvidence
from tools.standards_engine.standards_engine.authoring import AuthoringError


class EvidenceDigestBoundaryTest(unittest.TestCase):
    def test_shared_digest_corpus_agrees_at_all_validated_boundaries(self):
        cases = (
            ('sha256:' + '0'*64, True), ('sha256:' + 'abcdef0123456789'*4, True),
            ('sha256:' + 'g'*64, False), ('sha256:' + 'A'*64, False),
            ('sha256:' + '0'*63, False), ('sha256:' + '0'*65, False),
            ('sha256:' + '0'*64 + '\n', False), ('sha256:' + '0'*64 + '\r\n', False),
            (' sha256:' + '0'*64, False), ('SHA256:' + '0'*64, False),
            ('sha512:' + '0'*64, False), ('sha256:' + '\u0660'*64, False),
            ('', False), (None, False), (123, False), (True, False), (b'sha256:' + b'0'*64, False),
        )
        schema = json.loads((Path(__file__).resolve().parents[1] /
            "contracts/a1-contract.schema.json").read_text())
        oracle = Draft202012Validator(schema["$defs"]["Digest"])
        constructors = (
            ('generated', generated.EvidenceReference.from_value, ContractError),
            ('analysis', lambda v: AnalysisEvidence(**v), AnalysisError),
            ('authoring', AuthoringEvidence.from_mapping, AuthoringError),
        )
        for digest, valid in cases:
            self.assertEqual(oracle.is_valid(digest), valid, repr(digest))
            payload = {'id': 'fixture', 'digest': digest,
                       'provider_contract': 'repository-content', 'provider_contract_version': '1'}
            for name, create, error_type in constructors:
                with self.subTest(digest=digest, boundary=name):
                    if valid:
                        self.assertEqual(create(payload).as_contract(), payload)
                    else:
                        with self.assertRaises(error_type) as caught:
                            create(payload)
                        self.assertEqual(caught.exception.failure.outcome, 'invalid')

    def test_digest_syntax_does_not_replace_actual_content_verification(self):
        data = b'real fixture bytes'
        reference = AnalysisEvidence('fixture', 'sha256:' + hashlib.sha256(data).hexdigest(),
                                     'repository-content', '1')
        self.assertEqual(ResolvedEvidence(reference, data).content, data)
        with self.assertRaises(AnalysisError) as caught:
            ResolvedEvidence(reference, b'tampered fixture bytes')
        self.assertEqual(caught.exception.failure.code, 'ANALYSIS.EVIDENCE_DIGEST_MISMATCH')
