#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/binding-runtime-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/language-bindings.md"
readonly GENERIC="$REPO_ROOT/profiles/boundaries/language-bindings.md"
readonly RUST_INDEX="$REPO_ROOT/profiles/languages/rust/README.md"
readonly CONCURRENCY="$REPO_ROOT/topics/concurrency.md"
readonly ASYNC_PROFILE="$REPO_ROOT/profiles/languages/rust/async.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id runtime_owner runtime_capability handle_owner \
  request_state execution task_owner fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$runtime_owner" =~ ^(composition|binding|request|missing)$ ]]
  [[ "$runtime_capability" =~ ^(shared-injected|call-injected|unavailable)$ ]]
  [[ "$handle_owner" =~ ^(declared|missing|not-required)$ ]]
  [[ "$request_state" =~ ^(current-only|retained-input|retained-cancellation|retained-result|not-required)$ ]]
  [[ "$execution" =~ ^(scoped-await|tracked-submit|sync-drive|create-runtime|detached|not-required)$ ]]
  [[ "$task_owner" =~ ^(lifecycle|scope|missing|not-required)$ ]]
  [[ "$fallback" =~ ^(none|embedded-runtime|alternate-runtime|block|carry-forward|detach|alternate-binding)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  invalid_adaptation=0
  if [[ "$runtime_owner" =~ ^(binding|request)$ ||
        "$handle_owner" == 'missing' ||
        "$request_state" =~ ^retained- ||
        "$execution" =~ ^(sync-drive|create-runtime|detached)$ ]]; then
    invalid_adaptation=1
  elif [[ "$execution" == 'tracked-submit' &&
          "$task_owner" != 'lifecycle' ]]; then
    invalid_adaptation=1
  elif [[ "$execution" == 'scoped-await' && "$task_owner" != 'scope' ]]; then
    invalid_adaptation=1
  fi

  if [[ "$fallback" != 'none' || "$invalid_adaptation" -eq 1 ]]; then
    actual='typed-invalid'
  elif [[ "$runtime_owner" == 'missing' ||
          "$runtime_capability" == 'unavailable' ]]; then
    actual='typed-unavailable'
  else
    actual='allow'
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

expected_ids=(STD-0798 STD-0799 STD-0800)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    $1 == "STD-0798" || $1 == "STD-0799" || $1 == "STD-0800" { print $1 }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 && ($1 == "STD-0798" || $1 == "STD-0799" ||
               $1 == "STD-0800") { print $1 }
  ' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0798|STD-0799|STD-0800)
      [[ "$source:$target:$disposition" == \
        'languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:profiles/languages/rust/language-bindings.md:refine' ]]
      [[ -n "$rationale" && -z "${extra:-}" ]]
      ;;
  esac
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" "$REPO_ROOT/topics/security.md" \
  "$CONCURRENCY" \
  "$REPO_ROOT/profiles/boundaries/interop.md" "$GENERIC" \
  "$RUST_INDEX" "$ASYNC_PROFILE" "$PROFILE"

required_profile=(
  '## Handle And Runtime Adaptation'
  'Distinguish a host-visible handle from runtime and task lifecycle.'
  'composition owner'
  'across calls or workflow runs without making'
  'Each call creates fresh input, cancellation, result, and failure state.'
  'persistence or keep-alive request'
  'owner before submission'
  'does not synchronously drive'
  'typed `unsupported` or `unavailable`'
  '## Verification'
  '## No Fallback'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done
rg -F -q '(async.md)' "$PROFILE"
rg -F -q '## Runtime Composition' "$ASYNC_PROFILE"
rg -F -q '## Own Spawned Work' "$ASYNC_PROFILE"
rg -F -q '## Coordinate Shutdown' "$ASYNC_PROFILE"

legacy_memory="$(
  sed -n '/^## Memory Ownership Model$/,/^## Async Bridging$/p' "$LEGACY"
)"
legacy_async="$(
  sed -n '/^## Async Bridging$/,/^## Testing Strategy$/p' "$LEGACY"
)"
for text in 'EngineResource' 'tokio::runtime::Runtime' \
  'embed the tokio runtime' 'ResourceArc<>'; do
  if rg -F -q "$text" <<< "$legacy_memory"; then
    printf 'legacy binding-owned runtime guidance remains: %s\n' \
      "$text" >&2
    exit 1
  fi
done
for text in 'async_runtime = "tokio"' 'spawn_blocking' \
  'runtime.block_on' 'DirtyCpu'; do
  if rg -F -q "$text" <<< "$legacy_async"; then
    printf 'legacy binding async fallback remains: %s\n' "$text" >&2
    exit 1
  fi
done
rg -F -q 'language-bindings.md#handle-and-runtime-adaptation' \
  <<< "$legacy_memory"
rg -F -q 'language-bindings.md#handle-and-runtime-adaptation' \
  <<< "$legacy_async"
rg -F -q 'profiles/languages/rust/async.md' <<< "$legacy_async"

for heading in '## Testing Strategy' '### NIF Pure-Logic Separation'; do
  rg -F -q "$heading" "$LEGACY"
done

rg -F -q '| F025 | Resolved in Milestone 7.4b5c |' "$FINDINGS"
rg -F -q '`7.4b5c` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-f025-f026-decomposition.sh"

printf 'Rust binding runtime policy passed: %s decisions, 3 exact dispositions\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
