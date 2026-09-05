# Milestone 1: Focused Navigation Acceptance

The generated Interface now exposes `route`, `read`, and `related` with direct
arguments and optional snapshot capture. Native `query` remains supported.
The Engine composes capture and query; MCP contains no snapshot/session state.

## Evidence

- Python 3.12 with the repository's hash-locked Engine dependencies.
- The generated-contract, MCP, and focused navigation suites cover 29 tests.
  The original capture test incorrectly equated independently minted snapshot
  handles. It was corrected to compare native and focused routing against the
  same returned snapshot, while asserting that a fresh capture has a distinct
  identity. The corrected test passes separately; the other 28 passed together.
- All 20 `standards_contracts` tests pass; generated projection checks pass.
- Engine `verify_repository` with refreshed inputs passes 73 suites / 121 checks.
- Skill validation, focused Ruff checks, and diff whitespace checks pass.

## Real MCP Client Walkthrough

Official MCP Python SDK 1.29.1 was installed in a separate temporary client
environment. Its `ClientSession` initialized the stdio server, discovered the
22 generated tools, validated results, and called the focused tools against an
isolated repository clone. The clone retained accepted canonical standards;
the working contract files selected the new transport surface.

| Scenario | Observed result |
| --- | --- |
| Known Rust implementation facts | One focused `route` call; selections match native snapshot/query routing against the same snapshot |
| Planning policy with substantial relationships | Full result: 32,834 serialized bytes; compact result: 19,205 bytes; exact content: 17,601 UTF-8 bytes |
| Authority and text fidelity | `content` and `policy` exactly equal in full and compact results |
| Missing facts | Unresolved questions retained |
| Interleaved independent read and resumed task | Earlier snapshot remains explicit and produces the same compact policy result |
| Related policy consumer | Focused tests preserve the snapshot-bound authoring target and reject unregistered relationship groups |

The walkthrough used the official SDK's actual stdio client and schema
validation. It does not claim a model-generated coding session or completion of
the later authoring client scenarios. The SDK is acceptance tooling only; no
Engine dependency or user client configuration changed.
