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
configuration format. Restart the Engine and reconnect after the interface-41
focused-routing result-shape update.
Inspect `runtime_info` to verify the actual running interface and catalog;
files on disk do not replace a running process. Preserve installed stores and
exact workflow handles. The update changes presentation, not retained state.
Verify the application catalog contains navigation and the authoring catalog contains the
required maintenance workflow. `--advanced` adds only operations admitted by the
configured purpose.

The local server remains synchronous MCP stdio with protocol `2025-11-25`;
requests execute serially and immutable Engine handles survive reconnection.
The current implementation is 0.2.0 and Engine interface 41. No network listener,
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

## Schema presentation (interface 39)

`--schema-mode compatibility` is the default. It retains inline input schemas and
schema text for the established nested-rendering workaround. Hosts with verified
support for local JSON Schema references may explicitly select `--schema-mode native`.
Native mode omits the duplicate description text and chooses the smaller complete
inline/reference input projection per tool. It is a lossless catalog presentation;
validation, output schemas, purpose, permissions and domain behavior are unchanged.

Select the mode in host configuration, then restart/reconnect. There is no guessed
client-name policy, automatic downgrade, or transport-session state. The existing
catalog digest reflects the actual tool definitions (identical projections share
a digest even across mode names); use `runtime_info` to detect a
stale client catalog. Preserve all stores, proposals, readiness and recovery handles.

Qualify the actual configured client before choosing native mode. The optional
`codex_navigation_client.py --schema-mode native` checks the already configured
registration; it does not reconfigure Codex or start a model turn. Passing schema
validation alone does not establish successful model-visible rendering. Retain
compatibility mode while that client qualification is unavailable.


## Input discovery and qualification (interface 40)

Both catalog modes expose `describe_input` with small, flat arguments. Discovery
returns exact input definitions as ordinary tool-result content and does not rely
on the client's schema renderer. Keep compatibility mode until each supported
client has a qualified direct or discovery path. This release does not assert that
native declarations no longer contain `unknown`.

The existing `codex_navigation_client.py` checks catalog/schema transport and
scripted discovery/navigation without a model turn. It is not model-visible
qualification. The separate opt-in `codex_discovery_client.py` starts an actual
model turn against a run-owned local MCP registration and a disposable repository.
It requires explicit model-use authorization, preserves its private transcript,
checks all five authoring operations and shared evidence, and stops at readiness.
See the [qualification procedure](../../../../tools/standards_engine/tests/INPUT-DISCOVERY-QUALIFICATION.md).
Neither harness reconfigures the user's installed MCP registration or authorizes
production publication. A passing baseline CI run is not qualification of a new
client/catalog pair. Preserve existing stores and handles when restarting.

For reference CLI or direct facade discovery, the observer uses the full
purpose-qualified compatibility catalog, matching the operations those surfaces
expose. Use the returned catalog identity; it may differ from focused MCP.


## Catalog Inventory and Retirement

Measure the actual purpose/mode before comparing catalog overhead. From the
repository root, use the supported locked Python:

```sh
PYTHONPATH=. python -m tools.standards_engine.tests.catalog_inventory --purpose authoring --schema-mode native
PYTHONPATH=. python -m tools.standards_engine.tests.catalog_inventory --catalog /private/tools-list.json
```

The input file may be a raw tool array, tools/list result or its JSON-RPC envelope.
Other host-rendered forms are rejected rather than guessed. The inventory reports
raw description characters/UTF-8 bytes, serialized input/output-schema bytes, and
complete catalog JSON. Its measurement hash binds that serializer's bytes; it is
not the runtime catalog digest. These are not model token or billing measurements.
The command does not open a store, invoke tools or reconfigure the host.

Ordinary development uses application purpose; authoring sessions explicitly use
its maintenance surface. Native removes embedded schema-description fallbacks but
retains exact `describe_input` access. Compatibility remains the default for
unqualified deployments. Record the concrete supported client/version set, native
workflow evidence and preserved-trace reconciliation, plus CI and independent
review. Retire compatibility only after those deployments have a qualified direct
or discovery path or have been explicitly retired. Hypothetical future clients do
not establish a permanent support obligation. Keep `describe_input` at retirement;
remove obsolete mode/flag/description branches in a coordinated configuration cutover.
