# Engine Python Environment

Use Python 3.11 or newer. Prefer an existing isolated environment that was
installed from `tools/standards_contracts/requirements.lock` with hashes
enforced.

When no such environment exists, create one outside the repository:

```bash
python3 -m venv /tmp/coding-standards-engine
/tmp/coding-standards-engine/bin/python -m pip install \
  --require-hashes --only-binary=:all: \
  -r tools/standards_contracts/requirements.lock
```

Then substitute `/tmp/coding-standards-engine/bin/python` for `python3` in the
skill commands. Dependency installation may require network or package-cache
authorization; request it when required. If the locked environment cannot be
created, report the dependency boundary as unavailable. Do not install into the
repository, relax hashes, choose alternate versions, or implement a fallback
validator.
