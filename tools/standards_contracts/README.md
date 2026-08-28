# Standards Contracts

`standards_contracts` is the A1b boundary for canonical contract validation and
public projection compilation. Draft 2020-12 behavior is delegated unchanged
to `jsonschema.Draft202012Validator`; immutable same-resource reference
resolution is delegated to `referencing`.

Milestone 0 establishes only the exact dependency boundary and reproducible
lock. The compiler and public package Interface are introduced in Milestone 1.

Install the complete admitted dependency closure with:

```sh
python -m pip install \
  --require-hashes \
  --only-binary=:all: \
  -r tools/standards_contracts/requirements.lock
```

Runtime retrieval, custom vocabularies, validator keyword overrides, and a
repository implementation of JSON Schema are outside this module.
