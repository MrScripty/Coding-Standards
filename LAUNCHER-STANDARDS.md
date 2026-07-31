# Launcher Standards Legacy Index

This file is a migration index. Launcher command projection, action decoding,
procedure delegation, process and state lifecycle, help, implementation
mechanism, and terminal outcomes are canonical in the
[Launcher Application Profile](profiles/applications/launcher.md).

The remaining sections retain legacy authority only until their recorded
owner-specific migration children complete. They do not grant Launcher
authority over verification acceptance, dependency policy, release procedure,
or generated-command security.

Acceptance authority remains canonical in
[Verification](workflows/verification.md). A launcher action transports its
selected procedure and does not upgrade the procedure's evidence kind.

Dependency requirement, satisfaction, provisioning, and lifecycle authority is
canonical in [Dependencies](topics/dependencies.md). Launcher only exposes the
selected procedure and preserves its diagnostics and terminal outcome.

### Output Requirements

`--install` output should be explicit per dependency:

- `[ok] <dep> already satisfied`
- `[install] <dep> missing; installing`
- `[done] <dep> installed`
- `[error] <dep> install failed`

Build-procedure authority is canonical in
[Release](workflows/release.md#build-procedure-selection). Launcher only
exposes a selected procedure and preserves its diagnostics and outcome.

Generated command and configuration-text authority is canonical in
[Security](topics/security.md#generated-command-and-configuration-text).
Launcher only projects output accepted by that contract.
