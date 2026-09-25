# Process-owned pure reuse: bounded implementation admission

Base: `b81a5aae2eb72fb976b0570a4dab76d30e531fe4`.
Branch: `implementation/purpose-separated-standards-engine`.

## Objective and authority

The user requested the next measured performance optimizations and a ZIP.
Improve repeated explicit-snapshot MCP calls while preserving per-call store,
lifecycle, content-integrity, purpose, input-validation and authorization checks.
First reuse the installed interface contract at server lifetime. Admit bounded
pure snapshot compilation reuse only after measuring the residual cost.

Applicable guidance: Core/Router, Performance, Verification and oracles,
Development Proportionality, Architecture and Immutable Results And Replay,
Contracts, Security, Implementation, Commit and Documentation. This code change
uses the agreed positive, proportionate practices and preserves normative text.

## Owned boundaries and allowed writes

- `tools/standards_engine/standards_engine/tools.py`: optional trusted precompiled
  interface injection; normal standalone construction remains a real consumer.
- `tools/standards_engine/standards_engine/mcp.py`: process-owned pure resources,
  schema discovery from the same interface, per-call stores, terminal cleanup.
- `tools/standards_engine/standards_engine/compiled_cache.py` and `engine.py`:
  conditional bounded compilation reuse after full durable validation.
- Focused new Engine tests and only concretely affected existing tests.
- `tools/standards_engine/PURPOSE-SEPARATION.md`, relevant implementation README,
  this report/evidence directory, and the existing generated suite-input index.

Production schemas, persisted formats, identity encoding, Git reader behavior,
SQLite settings, normative guidance and installed configuration are preserved.
The scope contains no test-parallelism framework or persistent cache service.

## Composed design

The installed interface and immutable standards compilation have independent
owners and keys. MCP only owns their lifetime and supplies them to per-call
facades. Each Engine continues to own and close its store. Capture retains two
fresh independent compiler passes. Publication/recovery and decision evaluation
retain current checks. The cache (if admitted) holds only a verified frozen
capture and pure compilation; results, access decisions and mutable heads are
fresh. It is local to a fixed repository/purpose and installed implementation.

Removing interface retention restores a repeated schema compile. Removing
snapshot retention restores the existing correct verified cold path. Neither
optimization is an authority dependency; both can fail admission without changing
the result's meaning. Normal misses and budget overflow perform verified work.
No unrelated adapter or version is introduced for either mechanism.

## Evidence and stopping conditions

Baseline: three serial sequences of server initialization and explicit-snapshot
read/route calls against one unchanged disposable candidate-main fixture.
Record facade-interface time, full compilation, full content load, operation
wall/CPU and catalog timing separately; do not add inclusive spans.

Verify correct and malformed requests, result/schema parity, fixed-purpose
isolation, fresh authorization, closed/replaced/corrupt stores, cold replacement,
main advancement and historical snapshots. For any compilation cache, also test
entry/byte bounds, eviction, uncacheable entries, lifecycle denial after warming,
response mutation isolation, independent capture passes and cleanup. Existing
real Git/SQLite publication/recovery tests remain required.

Use exact baseline/candidate inputs and report the supported-environment limit.
Tests and a structural checkpoint prove separate claims. Final evidence records
all run outcomes; package checks do not imply configured-client qualification.
Stop at the measured pure-reuse scope; runtime semantics or owner changes require
an explicit revision of this admission. Ordinary defects are repaired within it.

## Residual-cost decision

Three local explicit-snapshot sweeps measured approximately 0.279 seconds of
interface compilation and 0.196 seconds of full standards compilation per
repeated 0.676-second MCP-dispatched read. Interface-only reuse reduced repeated
reads to approximately 0.371 seconds. The residual compilation remains about
half that time, justifying the bounded two-entry pure cache in this increment.
Initial cache admission accounts for approximately 6.5 MB per representative
capture; retain the proposed 32 MiB budget and measure it in final evidence.
This does not claim installed Codex timings or a whole-suite speedup.
