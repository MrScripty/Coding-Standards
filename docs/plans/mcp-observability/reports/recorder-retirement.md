# Raw recorder retirement and sanitized recorder activation

Date: 2026-10-22.

The user selected the newer sanitized recorder as the sole supported
implementation, requested preservation of the historical raw database, and
authorized migration of the existing launch configuration. This supersedes the
temporary compatibility decision in synchronization merge `bc7d9efd`.

## Source and configuration

The raw `interaction_observation` implementation, its two test modules, the
`observation_db` constructor argument and the `--observation-db` launch option
were removed. Historical O1 qualification records remain; that plan is now
Superseded. Interface 47, generated agent-tool contracts and normative standards
are unchanged. `interaction_observer` is the remaining recorder owner.

Only the Standards Engine argument list in `/home/jeremy/.codex/config.toml`
changed. All other parsed configuration values were preserved. The new arguments
select `--observe-database` at
`/home/jeremy/.local/share/standards-engine/observations/sanitized.sqlite3` and
`--observe-deployment codex-local`. The destination directory is mode 0700;
the new database is mode 0600, outside the repository and separate from domain
stores. Recording uses the sanitized recorder's existing defaults and schema.

The original `.standards-engine/interaction-observations.sqlite3` remains in
place. A consistent SQLite backup and the original configuration are retained
in a private operator recovery directory outside the repository. No raw rows,
configuration secrets or live observation payloads accompany this report.

## Activation and checks

The running Codex daemon acknowledged `config/mcpServer/reload`. A subsequent
`runtime_info` call through this thread's configured server returned interface
47 and installation state `current`. A process check observed 28 Standards
Engine MCP launches with the sanitized options and none with the raw option.
The new database contains `sessions`, `interactions` and `events`, with new
observations present. The preserved old database still had its original 135
sessions and 885 interactions at the post-reload check.

The supported configuration and reload boundaries are described in
[OpenAI's MCP configuration documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
and [app-server documentation](https://learn.chatgpt.com/docs/app-server).
The daemon was not restarted; loaded connections were refreshed through its
configuration operation.

The sanitized recorder, existing MCP behavior, runtime identity, schema
presentation, snapshot handoff and incoming Analysis fixture passed all 49
targeted tests on the retired-source candidate. Engine repository verification
passed 73 suites and 121 checks. A separate negative CLI probe confirmed the
retired flag is rejected before opening a preserved database copy, whose digest
remained unchanged. The historical raw recorder's earlier tests and acceptance
are evidence for its original source only.
