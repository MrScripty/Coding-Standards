#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/async-lifecycle-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/async.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-ASYNC-STANDARDS.md"

while IFS=$'\t' read -r case_id runtime_owner task_tracking failure admission \
  drain abort capability fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$runtime_owner" =~ ^(composition|library-global|missing)$ ]]
  [[ "$task_tracking" =~ ^(none|tracked|detached)$ ]]
  [[ "$failure" =~ ^(observed|discarded|leaf-logged|not-required)$ ]]
  [[ "$admission" =~ ^(closed|open|not-required)$ ]]
  [[ "$drain" =~ ^(complete|incomplete|not-required)$ ]]
  [[ "$abort" =~ ^(none|authorized-safe|authorized-unsafe|unauthorized)$ ]]
  [[ "$capability" =~ ^(available|unavailable)$ ]]
  [[ "$fallback" =~ ^(none|alternate-runtime|leaf-logging|force-abort)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$runtime_owner" == 'library-global' ||
        "$task_tracking" == 'detached' ||
        "$failure" =~ ^(discarded|leaf-logged)$ ||
        "$admission" == 'open' ||
        "$abort" =~ ^(authorized-unsafe|unauthorized)$ ||
        "$fallback" != 'none' ]]; then
    actual='typed-invalid'
  elif [[ "$runtime_owner" == 'missing' ||
          "$capability" == 'unavailable' ||
          ("$drain" == 'incomplete' && "$abort" != 'authorized-safe') ]]; then
    actual='typed-unavailable'
  else
    actual='allow'
  fi
  [[ "$actual" == "$expected" ]]
done < "$FIXTURE"

expected_ids=(STD-0719 STD-0720 STD-0721)
mapfile -t inventory_ids < <(
  awk -F '\t' '$1 >= "STD-0719" && $1 <= "STD-0721" { print $1 }' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0719" && $1 <= "STD-0721" { print $1 }' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in STD-0719|STD-0720|STD-0721) ;; *) continue ;; esac
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
  '## Runtime Composition'
  "composition root owns runtime construction"
  'process-global or alternate runtime to make an operation execute.'
  '## Own Spawned Work'
  'observes success, failure, panic, and cancellation'
  '## Coordinate Shutdown'
  'closes admission for new owned work'
  'A time limit does not itself authorize abort.'
  '## No Fallback'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_lifecycle="$(sed -n '/^## Runtime Boundaries$/,/^## Blocking Work$/p' "$LEGACY")"
for pattern in 'tokio::spawn' 'JoinHandle' 'JoinSet' 'TaskTracker' \
  'CancellationToken' 'tokio::sync::watch' 'force-aborting'; do
  if rg -F -q "$pattern" <<< "$legacy_lifecycle"; then
    printf 'legacy Rust async lifecycle default remains: %s\n' "$pattern" >&2
    exit 1
  fi
done
for heading in '## Runtime Boundaries' '## Task Lifecycle' '## Graceful Shutdown' \
  '## Blocking Work' '## Mutex Selection' '## Cancellation Safety' '## Observability'; do
  rg -F -q "$heading" "$LEGACY"
done

"$SCRIPT_DIR/verify-milestone-7-rust-async-decomposition.sh"
"$SCRIPT_DIR/verify-milestone-7-trust-lifecycle-replan.sh"

printf 'Rust async lifecycle policy passed: %s decisions, 3 exact dispositions\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
