# Launcher Standards

Requirements for `launcher.sh`, the default entry point for all apps.

## Scope

Every application must expose a root-level `launcher.sh` script as the primary
entry point for local development, CI, and operator workflows.

`launcher.sh` must:

- Be executable (`chmod +x launcher.sh`)
- Use Bash (`#!/usr/bin/env bash`)
- Support only long-form `--` options
- Implement `--run`, `--install`, and `--help`

---

## Core CLI Contract

### Required Flags

| Flag | Purpose | Required Behavior |
|---|---|---|
| `--run` | Start the application | Launches app process and forwards app args |
| `--install` | Install app dependencies | Checks each dependency and skips already-satisfied ones |
| `--help` | Show usage | Prints usage, flags, and examples, then exits 0 |

### Parsing Rules

1. Exactly one action flag must be selected: `--run`, `--install`, or `--help`
2. Unknown flags must fail with exit code `2` and print usage
3. `--` marks the start of application args and is valid only with `--run`
4. No positional args are allowed before `--`

### Canonical Usage

```bash
./launcher.sh --help
./launcher.sh --install
./launcher.sh --run
./launcher.sh --run -- --port 8080 --log-level debug
```

---

## Dependency Installation Standards (`--install`)

### Per-Dependency Idempotent Behavior

For each declared dependency, `launcher.sh --install` must:

1. Run a dependency-specific check
2. Skip install if already satisfied
3. Install only missing dependency
4. Re-check after installation to verify success
5. Fail fast if install or verification fails

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

## Runtime Standards (`--run`)

`--run` must:

1. Validate required runtime dependencies before launch
2. Fail with actionable message if prerequisites are missing
3. Forward args after `--` to the app unchanged
4. Use `exec` when launching so signals reach the app directly

Example:

```bash
exec ./bin/my-app "${RUN_ARGS[@]}"
```

---

## Help Standards (`--help`)

`--help` must include:

- Script purpose
- Usage synopsis
- Required flags
- Arg forwarding syntax (`--run -- <args>`)
- At least one install and run example
- Exit code meaning

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Operation failed (install/run error) |
| `2` | Usage error (invalid flags/arguments) |
| `3` | Missing dependency during `--run` preflight |
| `130` | Interrupted (SIGINT) |

---

## Bash Implementation Rules

1. Enable strict mode: `set -euo pipefail`
2. Quote variable expansions (`"$var"`, `"${arr[@]}"`)
3. Use functions; keep top-level flow small and readable
4. Avoid `eval`
5. Use `command -v` for binary presence checks
6. Keep dependency checks side-effect free
7. Do not silently auto-escalate privileges (`sudo`) without explicit operator intent

---

## Reference Template

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_NAME="$(basename "$0")"
DEPENDENCIES=("node" "pnpm")

usage() {
  cat <<EOF
Default app launcher.

Usage:
  ./${SCRIPT_NAME} --help
  ./${SCRIPT_NAME} --install
  ./${SCRIPT_NAME} --run [-- <app args...>]

Examples:
  ./${SCRIPT_NAME} --install
  ./${SCRIPT_NAME} --run -- --port 8080

Exit codes:
  0 success
  1 operation failed
  2 usage error
  3 missing dependency for run
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

check_node() { command -v node >/dev/null 2>&1; }
install_node() { die "implement node installer for your platform"; }

check_pnpm() { command -v pnpm >/dev/null 2>&1; }
install_pnpm() { die "implement pnpm installer for your platform"; }

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

run_app() {
  local run_args=("$@")
  ensure_runtime_dependencies
  exec ./bin/my-app "${run_args[@]}"
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
      --run)
        [[ -z "$action" ]] || die_usage "only one action flag is allowed"
        action="run"
        shift
        ;;
      --)
        [[ "$action" == "run" ]] || die_usage "-- is only valid with --run"
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
    run)
      run_app "${run_args[@]}"
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
- Script supports only long-form options and includes required flags
- `--install` performs per-dependency check/skip/install/verify
- `--run` forwards app args via `--`
- `--help` documents usage, examples, and exit codes
- Script uses strict Bash mode and quoted expansions
