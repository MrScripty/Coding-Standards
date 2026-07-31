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

## Desktop Entry and Script Generation Safety

If a launcher or installer generates `.desktop` files or helper shell scripts,
command construction must treat paths/URLs/labels as untrusted input.

Rules:
1. Do not concatenate raw user-provided values into command strings.
2. For `.desktop` files, build `Exec=` from a validated argument list and apply
   desktop-entry-safe escaping per argument.
3. For generated shell scripts, quote every interpolated value and avoid `eval`.
4. Validate URL schemes before embedding URL arguments into generated commands.
5. Add tests that cover spaces, quotes, and special characters in paths/tags/URLs.

```bash
# BAD: Raw interpolation into command string
printf 'Exec=%s --open "%s"\n' "$APP_BIN" "$USER_URL" > "$DESKTOP_FILE"

# GOOD: Validate first, then escape for destination format using shared helpers
validated_url="$(validate_external_url "$USER_URL")" || exit 1
exec_line="$(build_desktop_exec_line "$APP_BIN" "--open" "$validated_url")"
printf 'Exec=%s\n' "$exec_line" > "$DESKTOP_FILE"
```
