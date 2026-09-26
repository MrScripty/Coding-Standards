# Agent Tool Connection

Use Python 3.11 or 3.12 and an isolated environment installed from
`tools/standards_contracts/requirements.lock` with hashes enforced. Preserve the
pins and select the environment explicitly:

```bash
python3 -m venv /absolute/path/to/engine-environment
/absolute/path/to/engine-environment/bin/python -m pip install \
  --require-hashes --only-binary=:all: \
  -r tools/standards_contracts/requirements.lock
```

Dependency installation requires the operator's available package cache or network
and its relevant authorization. An unavailable locked environment leaves that
qualification pending rather than selecting replacement versions.

## Purpose-specific MCP registrations

Choose purpose in host configuration. Application agents receive the application
registration; standards maintainers use a separate authoring registration. Use a
new application session after authoring. The Engine cannot erase prior context.

```json
{
  "mcpServers": {
    "standards": {
      "command": "/absolute/path/to/engine-environment/bin/python",
      "args": ["-P", "-m", "tools.standards_engine.standards_engine.mcp", "--repo-root", "/absolute/path/to/Coding-Standards", "--purpose", "application"],
      "env": {"PYTHONPATH": "/absolute/path/to/Coding-Standards"}
    },
    "standards-authoring": {
      "command": "/absolute/path/to/engine-environment/bin/python",
      "args": ["-P", "-m", "tools.standards_engine.standards_engine.mcp", "--repo-root", "/absolute/path/to/Coding-Standards", "--purpose", "authoring"],
      "env": {"PYTHONPATH": "/absolute/path/to/Coding-Standards"}
    }
  }
}
```

These are separate intended audiences, not two registrations every agent should
receive. Translate the command, arguments and environment to the client's actual
configuration format. Restart the Engine and reconnect after the interface-38
result-shape update.
Inspect `runtime_info` to verify the actual running interface and catalog;
files on disk do not replace a running process. Preserve installed stores and
exact workflow handles. The update changes presentation, not retained state.
Verify the application catalog contains navigation and the authoring catalog contains the
required maintenance workflow. `--advanced` adds only operations admitted by the
configured purpose.

The local server remains synchronous MCP stdio with protocol `2025-11-25`;
requests execute serially and immutable Engine handles survive reconnection.
The current implementation is 0.2.0 and Engine interface 38. No network listener,
paid model turn, remote publication or extra server dependency is introduced.
The existing local authoring authorization adapter is owner-operated and
always-allow; explicit user authorization still governs requested changes.

The canonical checkout, store and private logs belong behind the host boundary.
An application agent with separate filesystem or database access could bypass
Engine-mediated exposure. This release supplies neither OS sandboxing nor a
remote multi-user permission service.

## Bootstrap and cutover

New automatic snapshots read accepted local `main`. The code release initially
contains empty application-approval and provenance manifests. Application reads
therefore return a bounded unavailable result until the separate content work
reviews and publishes the required material. Authoring can read the unchanged
standards once the code candidate is integrated into accepted main.

Use a disposable clone with candidate `main` for pre-merge qualification. Preserve
active installed proposals and recovery obligations before cutover. Old Analysis
records/captures outside the new supported contract are explicitly unsupported;
there is no automatic store deletion or conversion. See the complete
[implementation contract and cutover guide](../../../../tools/standards_engine/PURPOSE-SEPARATION.md).

## Reference CLI

The same purpose boundary applies to list, schema, example and invocation:

```bash
PYTHONPATH=. /absolute/path/to/engine-environment/bin/python -P \
  .agents/skills/standards-engine/scripts/invoke.py \
  --purpose application --list

printf '%s\n' '{"target":"core"}' | \
  PYTHONPATH=. /absolute/path/to/engine-environment/bin/python -P \
  .agents/skills/standards-engine/scripts/invoke.py \
  --purpose application read
```

Use `--purpose authoring` only in the authorized maintenance environment. Inspect
returned domain outcomes; CLI exit zero means the structured invocation completed,
not that a pending claim or rejected operation was accepted. Malformed/unsupported
CLI selection exits with a bounded error.

## Client qualification

The real stdio/CLI tests use actual processes and SQLite. The optional official
MCP SDK harness requires the SDK in a separate client environment and the locked
Engine Python supplied through `--engine-python`. The optional Codex test uses
`--server standards-authoring` (or the actual configured authoring name) and does
not start a model turn. These checks do not certify the content's editorial quality.
