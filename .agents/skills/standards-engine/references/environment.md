# Agent Tool Connection

Use Python 3.11 or 3.12. Prefer an existing isolated environment that was
installed from `tools/standards_contracts/requirements.lock` with hashes
enforced.

When no such environment exists, create one outside the repository:

```bash
python3 -m venv /tmp/coding-standards-engine
/tmp/coding-standards-engine/bin/python -m pip install \
  --require-hashes --only-binary=:all: \
  -r tools/standards_contracts/requirements.lock
```

Use that environment’s Python executable in the MCP server configuration. Dependency installation may require network or package-cache
authorization; request it when required. If the locked environment cannot be
created, report the dependency boundary as unavailable. Do not install into the
repository, relax hashes, choose alternate versions, or implement a fallback
validator.

## MCP Stdio Server

Register a local stdio server named `standards-engine` in the agent client's
MCP settings. Replace the absolute paths below with the installed interpreter
and repository checkout. `PYTHONPATH` selects the code; `--repo-root` selects
the standards repository, independently of the client's working directory.

```json
{
  "mcpServers": {
    "standards-engine": {
      "command": "/tmp/coding-standards-engine/bin/python",
      "args": [
        "-P", "-m", "tools.standards_engine.standards_engine.mcp",
        "--repo-root", "/absolute/path/to/Coding-Standards"
      ],
      "env": {"PYTHONPATH": "/absolute/path/to/Coding-Standards"}
    }
  }
}
```

For Codex, the equivalent entry in `config.toml` is:

```toml
[mcp_servers.standards-engine]
command = "/absolute/path/to/engine-environment/bin/python"
args = ["-P", "-m", "tools.standards_engine.standards_engine.mcp", "--repo-root", "/absolute/path/to/Coding-Standards"]
env = { PYTHONPATH = "/absolute/path/to/Coding-Standards" }
tool_timeout_sec = 600
```

Use a persistent isolated environment for an ongoing installation; `/tmp` is
suitable for a temporary trial. The longer call timeout accommodates proposal
verification and application. See [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

Client configuration formats differ; preserve the command, arguments, and
environment when translating these examples. Reconnect the client after
registration or an Engine contract update. Confirm that `create_snapshot` and
`query` are available before starting a standards workflow.

The server supports MCP protocol `2025-11-25` over newline-delimited stdio,
with initialization, ping, tool discovery, and tool calls. It needs no additional
Python dependencies. It runs requests serially and opens the durable Engine
facade for each call; snapshots and proposal handles survive reconnection.
Only protocol messages go to stdout; diagnostics go to stderr. No network
listener or remote publication is introduced.

Tool schemas are derived from the generated Engine contract, with only reachable
definitions included. Domain results are preserved as `structuredContent` and
JSON text for client compatibility. Rejections set `isError`; pending and
recovery-required states remain typed domain results. Transport failures are
errors with unknown domain outcome, never permission to retry a mutation.

This is the existing owner-operated local always-allow authorization adapter.
Connecting the server exposes the full authoring interface as well as reading;
user authorization for the requested operation still governs agent behavior.
The server does not supply semantic decisions or implicit review approval.

For debugging without an MCP client, run the existing `scripts/invoke.py`
transport from the repository root with `PYTHONPATH=.`. Its `--list`, `--schema`,
and `--example` options remain available; routine MCP use needs none of them.

Protocol references: [tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools),
[stdio transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports),
and [lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle).
