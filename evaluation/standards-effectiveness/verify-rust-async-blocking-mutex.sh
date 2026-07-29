#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/async-blocking-mutex-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/async.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-ASYNC-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"

while IFS=$'\t' read -r case_id operation execution isolation capacity guard \
  critical invariant mutex fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$operation" =~ ^(nonblocking|blocking-io|cpu-heavy)$ ]]
  [[ "$execution" =~ ^(direct|async-equivalent|isolated|inline-blocking)$ ]]
  [[ "$isolation" =~ ^(not-required|available|unavailable)$ ]]
  [[ "$capacity" =~ ^(not-required|bounded|unbounded|unavailable)$ ]]
  [[ "$guard" =~ ^(none|released|held-supported|held-unsupported)$ ]]
  [[ "$critical" =~ ^(none|synchronous|suspending)$ ]]
  [[ "$invariant" =~ ^(not-required|preserved|split)$ ]]
  [[ "$mutex" =~ ^(not-required|sync-capable|suspend-capable|unavailable)$ ]]
  [[ "$fallback" =~ ^(none|alternate-executor|new-thread|universal-mutex)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != 'none' ||
        ("$operation" != 'nonblocking' &&
          "$execution" =~ ^(direct|inline-blocking)$) ||
        ("$execution" == 'isolated' && "$capacity" == 'unbounded') ||
        ("$operation" != 'nonblocking' &&
          "$guard" =~ ^held-(supported|unsupported)$) ||
        "$guard" == 'held-unsupported' ||
        "$invariant" == 'split' ||
        ("$critical" == 'suspending' && "$guard" == 'held-supported' &&
          "$mutex" != 'suspend-capable') ||
        ("$critical" == 'synchronous' && "$guard" == 'held-supported' &&
          "$mutex" != 'sync-capable') ]]; then
    actual='typed-invalid'
  elif [[ ("$operation" != 'nonblocking' && "$execution" == 'isolated' &&
            ("$isolation" == 'unavailable' ||
              "$capacity" == 'unavailable')) ||
          ("$critical" != 'none' && "$mutex" == 'unavailable') ]]; then
    actual='typed-unavailable'
  else
    actual='allow'
  fi
  [[ "$actual" == "$expected" ]]
done < "$FIXTURE"

expected_ids=(STD-0722 STD-0723)
mapfile -t inventory_ids < <(
  awk -F '\t' '$1 >= "STD-0722" && $1 <= "STD-0723" { print $1 }' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0722" && $1 <= "STD-0723" { print $1 }' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in STD-0722|STD-0723) ;; *) continue ;; esac
  [[ "$source" == 'languages/rust/RUST-ASYNC-STANDARDS.md' ]]
  [[ "$target" == 'profiles/languages/rust/async.md' ]]
  [[ "$disposition" == 'refine' ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/concurrency.md" \
  "$REPO_ROOT/profiles/languages/rust/README.md" \
  "$PROFILE"

required_profile=(
  '## Isolate Blocking Work'
  'async capability only when it preserves'
  'lifecycle boundary owns the isolation capability'
  'Isolation without a bounded or otherwise governed capacity contract'
  '## Select Synchronization From Contract'
  'whether the protected critical section can suspend'
  'A guard crosses suspension only when the selected mechanism'
  'Do not select one synchronization implementation as a universal'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_mechanisms="$(sed -n '/^## Blocking Work$/,/^## Cancellation Safety$/p' "$LEGACY")"
for pattern in 'spawn_blocking' 'parking_lot::Mutex' 'tokio::sync::Mutex' \
  'tokio::sync::RwLock' 'std::sync::Mutex'; do
  if rg -F -q "$pattern" <<< "$legacy_mechanisms" || rg -F -q "$pattern" "$PROFILE"; then
    printf 'legacy Rust async blocking/mutex default remains: %s\n' "$pattern" >&2
    exit 1
  fi
done
for heading in '## Blocking Work' '## Mutex Selection' '## Cancellation Safety' \
  '## Observability'; do
  rg -F -q "$heading" "$LEGACY"
done

rg -F -q '| F045 | Partially resolved in Milestone 7.4b4f |' "$FINDINGS"
rg -F -q '`7.4b4f` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-rust-async-decomposition.sh"
"$SCRIPT_DIR/verify-milestone-7-trust-lifecycle-replan.sh"

printf 'Rust async blocking/mutex policy passed: %s decisions, 2 exact dispositions\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
