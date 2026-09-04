# Draft 2020-12 Instance Equality Reproduction

**Status:** `complete reproduction; known nonconformance retained`

**Accepted A1 commit:**
`2359a98740b6035a0414bfaf5427ceaa1301a1c8`

**Accepted A1 tree:**
`97c850ab718287007c1e1daac538f40869f71a1d`

## Claim

This report distinguishes JSON Schema instance equality from the repository's
content-identity canonicalization. It records the accepted A1 behavior without
changing the validator, generator, generated models, schema, fixtures, or any
runtime package.

The selected external authority is:

- JSON Schema Core, Draft 2020-12, section 4.2.2, published as
  `draft-bhutton-json-schema-01`:
  <https://json-schema.org/draft/2020-12/json-schema-core#section-4.2.2>;
- JSON Schema Validation, Draft 2020-12, section 6.4.3, published as
  `draft-bhutton-json-schema-validation-01`:
  <https://json-schema.org/draft/2020-12/json-schema-validation#section-6.4.3>.

Core defines string equality codepoint-for-codepoint and keeps Boolean and
numeric instances in distinct primitive types. Validation requires every item
to be unique under that instance equality for `uniqueItems: true`.

## Reproduction Boundary

The accepted tree was exported to temporary storage with:

```bash
git archive 2359a98740b6035a0414bfaf5427ceaa1301a1c8 |
  tar -x -C /tmp/coding-standards-a1-2359a987
git rev-parse '2359a98740b6035a0414bfaf5427ceaa1301a1c8^{tree}'
```

The resolved tree was exactly
`97c850ab718287007c1e1daac538f40869f71a1d`. From that extracted-tree working
directory, the exact local-behavior invocation was:

```bash
PYTHONPATH=. python3 -m unittest -v \
  tools.standards_engine.tests.test_generated_contract.GeneratedContractTest.test_generated_unique_items_matches_canonical_serialization \
  tools.standards_engine.tests.test_generated_contract.GeneratedContractTest.test_generated_const_and_enum_use_canonical_serialization
```

Expected and actual exit status was `0`; both named tests passed. The tests use
only accepted A1 modules and the complete Boolean/integer and Unicode values
shown below. No external test corpus, dependency, copied vector, temporary
unretained procedure, or permanent fixture was added.

Environment: CPython `3.12.3`; Git `2.43.0`.

## Results

`canonical` is the accepted A1 canonical schema validator. `generated` is the
accepted generated-model decoder.

| Case | Draft 2020-12 result | A1 canonical | A1 generated | Disposition |
| --- | --- | --- | --- | --- |
| `const: "é"` with instance `"e\u0301"` | reject | accept | accept | known nonconformance |
| `enum: ["é"]` with instance `"e\u0301"` | reject | accept | accept | known nonconformance |
| `uniqueItems` over `["é", "e\u0301"]` | accept | reject | reject | known nonconformance |
| integer `const: 1` with Boolean `true` | reject | reject | reject | conforming selected case |
| Boolean `enum: [true]` with integer `1` | reject | reject | reject | conforming selected case |
| `uniqueItems` over `[1, true]` | accept | accept | accept | conforming selected case |

The Unicode disagreement is caused by using NFC-normalized identity bytes as
the local equality oracle. Agreement between the canonical and generated A1
entry points proves local consistency only; it does not prove Draft 2020-12
conformance.

## Authority Separation

| Domain | Required owner | Reproduction conclusion |
| --- | --- | --- |
| JSON Schema instance equality | selected Draft 2020-12 dialect and vocabularies | codepoint string equality; Boolean and number remain distinct |
| Repository content identity | the named domain-separated canonical serialization contract | NFC normalization may be valid only for that explicitly selected identity domain |
| Python runtime equality | Python implementation language | not an oracle for either contract |

## Unsupported Domain

This bounded reproduction does not establish full Draft 2020-12 conformance,
select a replacement implementation, choose supported vocabularies or
extensions, or define migration for persisted A1 handles. Those are A1b design
decisions. Standards recovery must preserve this nonconformance as evidence and
must not quietly correct it.
