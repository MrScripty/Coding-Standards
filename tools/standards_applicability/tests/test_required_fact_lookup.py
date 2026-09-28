"""Shared lookup preserves the original canonical binder and diagnostic owner."""
import unittest
from tools.standards_applicability.standards_applicability import ApplicabilityError, compile_fact_schema
from tools.standards_applicability.tests.test_applicability import declaration


class RequiredFactLookupTest(unittest.TestCase):
    def test_known_alias_and_unknown_have_the_canonical_behavior(self):
        schema=compile_fact_schema(declaration([{'id':'enabled','type':'boolean','nullable':False,'aliases':['on']}]))
        self.assertIs(schema.require('enabled'),schema.require('on'))
        self.assertIsNone(schema.resolve('unknown'))
        errors=[]
        for operation in (lambda:schema.require('unknown'),lambda:schema.bind({'unknown':{'type':'boolean','state':'known','value':True}})):
            with self.assertRaises(ApplicabilityError) as caught:
                operation()
            errors.append(caught.exception.failure)
        self.assertEqual(errors[0],errors[1])
        self.assertEqual(errors[0].code,'APPLICABILITY.INVALID')
        self.assertEqual(errors[0].field,'unknown')
        with self.assertRaises(ApplicabilityError) as caught:
            schema.bind({'on':{'type':'boolean','state':'known','value':True},'enabled':{'type':'boolean','state':'known','value':True}})
        self.assertEqual(caught.exception.failure.message,'a fact and its alias cannot both be supplied')
