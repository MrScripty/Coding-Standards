# M6-I71 Documentation Projection Regression

## Status

Preserved regression evidence for the future evidence-oracle and projection-check
recovery. This report does not activate that recovery or broaden M6-I72 beyond
the narrow representation repair required to restore accepted verification.

## Exact Reproduction

- Accepted revision: `da65fddd80326a3d2b548ce59294fbfcc76bfe43`
- Accepted tree: `5b3f262e3139dcf7346f0a5b13cdf5196942cda2`
- Suite: `rust-binding-callback-task`
- Check: `documentation-projection`
- Diagnostic: `ASSERT.TEXT_REQUIRED [invalid]`
- Evidence path: `evaluation/standards-effectiveness/README.md`

Command:

```bash
python3 tools/standards_verifier/verify.py \
  --suite rust-binding-callback-task
```

Required representation:

```text
The registered `rust-binding-callback-task` suite checks selected task representation,
```

Accepted source representation:

```text
The registered `rust-binding-callback-task` suite checks selected task
representation, callback authority, checked input/output, response correlation, fresh
```

The accepted revision introduced both the declarative suite and the wrapped
README representation. The focused suite therefore fails at that exact
revision; the failure is not caused by the later M6-I72 migration.

## Property Assessment

The check intended to establish that the central evaluation documentation names
the registered suite and describes its responsibilities. It actually establishes
only that one explanatory byte sequence is adjacent in raw Markdown. Equivalent
rendered wrapping fails, while matching bytes do not establish that the surrounding
explanation remains semantically correct.

## Narrow Repair

The M6-I72 acceptance commit containing this report rejoins `task` and
`representation` on one source line. This representation-only change restores
the existing assertion without changing rendered meaning or introducing the
future evidence-oracle policy. The exact repair commit is the commit that first
adds this report and removes the failing wrapped representation; Plan B can
resolve it directly from repository history.

Plan B must retain this case as behavioral regression input and decide whether
the documentation projection is unnecessary, has a stronger deterministic
oracle, or requires change-triggered semantic review.
