# Launcher Standards

Requirements for `launcher.sh`, the default entry point for all apps.

## Scope

Every application must expose a root-level `launcher.sh` script as the primary
entry point for local development, CI, and operator workflows.

`launcher.sh` must:

- Be executable (`chmod +x launcher.sh`)
- Use Bash (`#!/usr/bin/env bash`)
- Support only long-form `--` options
- Implement `--run`, `--run-release`, `--build`, `--build-release`, `--install`,
  and `--help`

---

## Core CLI Contract

### Required Flags

| Flag | Purpose | Required Behavior |
|---|---|---|
| `--run` | Run the app in development mode | Launches the dev build path and forwards app args |
| `--run-release` | Run the compiled release binary | Executes the release artifact and forwards app args |
| `--build` | Compile development build | Produces development build artifacts |
| `--build-release` | Compile release build | Produces optimized release artifacts |
| `--install` | Install app dependencies | Checks each dependency and skips already-satisfied ones |
| `--help` | Show usage | Prints usage, flags, and examples, then exits `0` |

### Parsing Rules

1. Exactly one action flag must be selected.
2. Valid actions are `--run`, `--run-release`, `--build`, `--build-release`,
   `--install`, `--help`.
3. Unknown flags must fail with exit code `2` and print usage.
4. `--` marks the start of app args and is valid only with `--run` or `--run-release`.
5. No positional args are allowed.

### Canonical Usage

```bash
./launcher.sh --help
./launcher.sh --install
./launcher.sh --build
./launcher.sh --build-release
./launcher.sh --run
./launcher.sh --run -- --port 8080 --log-level debug
./launcher.sh --run-release
./launcher.sh --run-release -- --port 8080
```

---

## Dependency Installation Standards (`--install`)

### Per-Dependency Idempotent Behavior

For each declared dependency, `launcher.sh --install` must:

1. Run a dependency-specific check.
2. Skip install if already satisfied.
3. Install only the missing dependency.
4. Re-check after installation to verify success.
5. Fail fast if install or verification fails.

This guarantees incremental installs and avoids reinstalling dependencies that
already exist.

### Dependency Model

Define dependencies as named units with:

- `check_<name>` function: returns `0` when satisfied
- `install_<name>` function: performs installation

Do not combine all dependencies into one monolithic check.

### Output Requirements

`--install` output should be explicit per dependency:

- `[ok] <dep> already satisfied`
- `[install] <dep> missing; installing`
- `[done] <dep> installed`
- `[error] <dep> install failed`

---

## Build Standards (`--build`)

`--build` is required for apps that need compilation.

1. `--build` compiles development artifacts.
2. `--build-release` compiles optimized release artifacts.
3. Build commands must select the target binary explicitly when the toolchain
   can be ambiguous (for example Cargo workspaces with multiple binaries).
4. If the app has no compile step, `--build` and `--build-release` must still
   be accepted and return success with a clear no-op message.

Cargo example:

```bash
cargo build --bin "$APP_BIN"
cargo build --release --bin "$APP_BIN"
```

---

## Runtime Standards (`--run`, `--run-release`)

### `--run` (Development Runtime)

`--run` must:

1. Validate required runtime dependencies before launch.
2. Use the development run path.
3. Explicitly select the app target when using toolchains like Cargo.
4. Forward args after `--` unchanged.
5. Use `exec` so signals reach the app directly.

Cargo example:

```bash
exec cargo run --bin "$APP_BIN" -- "${RUN_ARGS[@]}"
```

### `--run-release` (Release Runtime)

`--run-release` must:

1. Validate required runtime dependencies before launch.
2. Execute the release binary artifact (not the dev run path).
3. Fail with an actionable message if the release binary is missing and tell the
   operator to run `--build-release`.
4. Forward args after `--` unchanged.
5. Use `exec` so signals reach the app directly.

Artifact example:

```bash
exec "./target/release/${APP_BIN}" "${RUN_ARGS[@]}"
```

---

## Help Standards (`--help`)

`--help` must include:

- Script purpose
- Usage synopsis
- Required flags
- Build mode syntax (`--build` and `--build-release`)
- Arg forwarding syntax (`--run -- <args>`, `--run-release -- <args>`)
- At least one install, build, and run example
- Exit code meaning

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Operation failed (install/build/run error) |
| `2` | Usage error (invalid flags/arguments) |
| `3` | Missing dependency during runtime preflight |
| `4` | Missing release artifact for `--run-release` |
| `130` | Interrupted (SIGINT) |

---

## Bash Implementation Rules

1. Enable strict mode: `set -euo pipefail`
2. Quote variable expansions (`"$var"`, `"${arr[@]}"`)
3. Use arrays for forwarded args
4. Use functions; keep top-level flow small and readable
5. Avoid `eval`
6. Use `command -v` for binary presence checks
7. Keep dependency checks side-effect free
8. Do not silently auto-escalate privileges (`sudo`) without explicit operator intent
9. Escape untrusted values before writing generated scripts or desktop entries

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

---

## Reference Template

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_NAME="$(basename "$0")"
APP_BIN="my-app"
RELEASE_BIN_PATH="./target/release/${APP_BIN}"
NEEDS_BUILD="true"  # Set to "false" for interpreted apps with no compile step.
DEPENDENCIES=("cargo")

usage() {
  cat <<EOF
Default app launcher.

Usage:
  ./${SCRIPT_NAME} --help
  ./${SCRIPT_NAME} --install
  ./${SCRIPT_NAME} --build
  ./${SCRIPT_NAME} --build-release
  ./${SCRIPT_NAME} --run [-- <app args...>]
  ./${SCRIPT_NAME} --run-release [-- <app args...>]

Examples:
  ./${SCRIPT_NAME} --install
  ./${SCRIPT_NAME} --build
  ./${SCRIPT_NAME} --build-release
  ./${SCRIPT_NAME} --run -- --port 8080
  ./${SCRIPT_NAME} --run-release -- --port 8080

Exit codes:
  0 success
  1 operation failed
  2 usage error
  3 missing dependency for runtime
  4 missing release artifact
EOF
}

log() {
  printf '[launcher] %s\n' "$*"
}

die() {
  log "error: $*"
  exit 1
}

die_usage() {
  log "usage error: $*"
  usage
  exit 2
}

check_cargo() { command -v cargo >/dev/null 2>&1; }
install_cargo() { die "implement cargo installer for your platform"; }

check_dep() { "check_$1"; }
install_dep() { "install_$1"; }

install_dependencies() {
  local dep
  for dep in "${DEPENDENCIES[@]}"; do
    if check_dep "$dep"; then
      log "[ok] $dep already satisfied"
      continue
    fi
    log "[install] $dep missing; installing"
    install_dep "$dep"
    if check_dep "$dep"; then
      log "[done] $dep installed"
    else
      log "[error] $dep install failed verification"
      exit 1
    fi
  done
}

ensure_runtime_dependencies() {
  local dep
  for dep in "${DEPENDENCIES[@]}"; do
    if ! check_dep "$dep"; then
      log "missing dependency: $dep"
      log "run ./${SCRIPT_NAME} --install first"
      exit 3
    fi
  done
}

build_app() {
  local mode="$1"
  ensure_runtime_dependencies

  if [[ "$NEEDS_BUILD" != "true" ]]; then
    log "[ok] no build step required"
    return 0
  fi

  case "$mode" in
    dev)
      log "[build] compiling dev binary: $APP_BIN"
      cargo build --bin "$APP_BIN"
      ;;
    release)
      log "[build] compiling release binary: $APP_BIN"
      cargo build --release --bin "$APP_BIN"
      ;;
    *)
      die_usage "invalid build mode: $mode"
      ;;
  esac
}

run_dev_app() {
  local run_args=("$@")
  ensure_runtime_dependencies

  if [[ "$NEEDS_BUILD" == "true" ]]; then
    exec cargo run --bin "$APP_BIN" -- "${run_args[@]}"
  fi

  exec ./bin/my-app "${run_args[@]}"
}

run_release_app() {
  local run_args=("$@")
  ensure_runtime_dependencies

  if [[ "$NEEDS_BUILD" != "true" ]]; then
    exec ./bin/my-app "${run_args[@]}"
  fi

  if [[ ! -x "$RELEASE_BIN_PATH" ]]; then
    log "missing release binary: $RELEASE_BIN_PATH"
    log "run ./${SCRIPT_NAME} --build-release first"
    exit 4
  fi

  exec "$RELEASE_BIN_PATH" "${run_args[@]}"
}

main() {
  local action=""
  local run_args=()

  while (($#)); do
    case "$1" in
      --help)
        [[ -z "$action" ]] || die_usage "only one action flag is allowed"
        action="help"
        shift
        ;;
      --install)
        [[ -z "$action" ]] || die_usage "only one action flag is allowed"
        action="install"
        shift
        ;;
      --build)
        [[ -z "$action" ]] || die_usage "only one action flag is allowed"
        action="build"
        shift
        ;;
      --build-release)
        [[ -z "$action" ]] || die_usage "only one action flag is allowed"
        action="build-release"
        shift
        ;;
      --run)
        [[ -z "$action" ]] || die_usage "only one action flag is allowed"
        action="run"
        shift
        ;;
      --run-release)
        [[ -z "$action" ]] || die_usage "only one action flag is allowed"
        action="run-release"
        shift
        ;;
      --)
        [[ "$action" == "run" || "$action" == "run-release" ]] \
          || die_usage "-- is only valid with --run or --run-release"
        shift
        run_args=("$@")
        break
        ;;
      *)
        die_usage "unknown argument: $1"
        ;;
    esac
  done

  [[ -n "$action" ]] || die_usage "one action flag is required"

  case "$action" in
    help)
      usage
      ;;
    install)
      ((${#run_args[@]} == 0)) || die_usage "--install does not accept app args"
      install_dependencies
      ;;
    build)
      ((${#run_args[@]} == 0)) || die_usage "--build does not accept app args"
      build_app "dev"
      ;;
    build-release)
      ((${#run_args[@]} == 0)) || die_usage "--build-release does not accept app args"
      build_app "release"
      ;;
    run)
      run_dev_app "${run_args[@]}"
      ;;
    run-release)
      run_release_app "${run_args[@]}"
      ;;
    *)
      die_usage "invalid action: $action"
      ;;
  esac
}

main "$@"
```

---

## Compliance Checklist

- `launcher.sh` exists in project root and is executable
- Script supports required long-form flags
- `--install` performs per-dependency check/skip/install/verify
- `--build` compiles dev and `--build-release` compiles release
- `--run` uses the dev run path and explicit binary selection when needed
- `--run-release` executes the release artifact and handles missing binary clearly
- `--run` and `--run-release` forward app args via `--`
- `--help` documents usage, examples, and exit codes
- Script uses strict Bash mode and quoted expansions
- Generated scripts/desktop entries escape interpolated values safely
