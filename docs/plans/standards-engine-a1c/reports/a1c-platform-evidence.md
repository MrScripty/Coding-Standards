# A1c Required-Platform Evidence

**Evidence status:** `satisfied for the A1c Linux platform contract`

**Implementation baseline:** `0911c079054185abca8ffe6973d26cdee34dedf7`

**Harness:** `tools/standards_engine/tests/platform_harness.py`

## Claim Boundary

This report records executable system and agent-workflow evidence. The static
`a1c-snapshot-lifecycle` decision table remains policy-projection evidence and
does not substitute for runtime execution.

The harness uses only generated public Standards Engine calls. Its producer
creates a canonical snapshot, discovers and reads it, inspects a policy,
prepares and resolves analysis work, and closes the SQLite store. The portable
manifest binds the closed store bytes, opaque handles, and expected read
content. Its consumer verifies the store before opening it, uses an unrelated
Git repository, performs a concurrent cold-process probe, inspects the stored
snapshot and analysis children, and exercises aggregate quarantine and
undelete.

No SQLite file or manifest is committed. File copying models administrative
transport and does not add a product backup or transfer Interface.

## Linux Results

| Python | Environment | SQLite | Produce store digest | Consume result |
| --- | --- | --- | --- | --- |
| CPython 3.11.14 | Linux 7.0.0-28-generic, x86_64 | 3.50.4 | `sha256:5a6651fa01b352d7f23d8b468c629e8f8d6b80a98c3dda8ce3f7608175ddd1b8` | pass |
| CPython 3.12.3 | Linux 7.0.0-28-generic, x86_64 | 3.45.1 | `sha256:e15cdeaea935cfc7e52be4fde32f5b2f74e5e0e77b4eb37aba2b1ddcaea1bdf1` | pass |

The exact CPython 3.11 commands were:

```text
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 /tmp/coding-standards-a1c-py311/bin/python3 -P tools/standards_engine/tests/platform_harness.py produce --repository . --store /tmp/a1c-platform-311/producer.sqlite3 --manifest /tmp/a1c-platform-311/manifest.json
cp -f /tmp/a1c-platform-311/producer.sqlite3 /tmp/a1c-platform-311/consumer.sqlite3
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 /tmp/coding-standards-a1c-py311/bin/python3 -P tools/standards_engine/tests/platform_harness.py consume --store /tmp/a1c-platform-311/consumer.sqlite3 --manifest /tmp/a1c-platform-311/manifest.json
```

The exact CPython 3.12 commands were:

```text
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 /tmp/coding-standards-a1c-py312/bin/python3 -P tools/standards_engine/tests/platform_harness.py produce --repository . --store /tmp/a1c-platform-312/producer.sqlite3 --manifest /tmp/a1c-platform-312/manifest.json
cp -f /tmp/a1c-platform-312/producer.sqlite3 /tmp/a1c-platform-312/consumer.sqlite3
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 /tmp/coding-standards-a1c-py312/bin/python3 -P tools/standards_engine/tests/platform_harness.py consume --store /tmp/a1c-platform-312/consumer.sqlite3 --manifest /tmp/a1c-platform-312/manifest.json
```

The focused regression command was:

```text
PYTHONPATH=. PYTHONPYCACHEPREFIX=/tmp/coding-standards-pycache /tmp/coding-standards-a1c-py312/bin/python3 -m unittest tools.standards_engine.tests.test_platform_harness
```

Result: two tests passed. The complete round trip took 50.002 seconds.

## Operation And Boundary Results

| Claim | Result |
| --- | --- |
| All eight generated public operations were exercised | pass |
| Opaque snapshot, policy, analysis, and child handles crossed process boundaries | pass |
| Closed-store bytes matched the manifest before consumer open | pass |
| Cold query and inspection did not use the canonical source repository | pass |
| A second process opened and read the same store while the consumer remained open | pass |
| Quarantined access returned a typed unavailable result | pass |
| Quarantine discovery and aggregate undelete restored reads and analysis inspection | pass |
| A changed store was rejected before engine open | pass |

This satisfies A1C-A8 and the complete Linux-scoped A1C-A7 claim.

## Unavailable Required Evidence

| Target | CPython 3.11 | CPython 3.12 | Status |
| --- | --- | --- | --- |
| Windows | unavailable | unavailable | deferred, support not claimed |
| macOS | unavailable | unavailable | deferred, support not claimed |

The current development environment supplies neither real target. The
repository also contains no selected provider integration from which those
facts can be obtained. Simulation, cross-compilation, and the Linux runs do not
establish either platform. A1c therefore claims Linux support only; Windows and
macOS require equivalent real evidence before a future plan or release may
promote them to supported status.
