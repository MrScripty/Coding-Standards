#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/async-boundary-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/async.md"
readonly RUST_INDEX="$REPO_ROOT/profiles/languages/rust/README.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-ASYNC-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id language suspends async_contract capability \
  fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$language" =~ ^(rust|other)$ ]]
  [[ "$suspends" =~ ^(yes|no|unknown)$ ]]
  [[ "$async_contract" =~ ^(yes|no|unknown)$ ]]
  [[ "$capability" =~ ^(available|unavailable)$ ]]
  [[ "$fallback" =~ ^(none|async-for-caller|sync-default|create-runtime|block|detach)$ ]]
  [[ "$expected" =~ ^(sync|async|not-applicable|typed-invalid|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$language" != 'rust' ]]; then
    actual='not-applicable'
  elif [[ "$fallback" != 'none' ]]; then
    actual='typed-invalid'
  elif [[ "$suspends" == 'unknown' || "$async_contract" == 'unknown' ||
          "$capability" == 'unavailable' ]]; then
    actual='typed-unavailable'
  elif [[ "$suspends" == 'yes' && "$async_contract" == 'yes' ]]; then
    actual='async'
  else
    actual='sync'
  fi
  [[ "$actual" == "$expected" ]]
done < "$FIXTURE"

expected_ids=(STD-0717 STD-0718)
mapfile -t inventory_ids < <(
  awk -F '\t' '$1 == "STD-0717" || $1 == "STD-0718" { print $1 }' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && ($1 == "STD-0717" || $1 == "STD-0718") { print $1 }' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0717) expected_disposition='move' ;;
    STD-0718) expected_disposition='refine' ;;
    *) continue ;;
  esac
  [[ "$source" == 'languages/rust/RUST-ASYNC-STANDARDS.md' ]]
  [[ "$target" == 'profiles/languages/rust/async.md' ]]
  [[ "$disposition" == "$expected_disposition" ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/concurrency.md" \
  "$REPO_ROOT/profiles/languages/rust/README.md" \
  "$PROFILE"

for file in "$REPO_ROOT/README.md" "$REPO_ROOT/STANDARDS-ROUTER.md" "$LEGACY"; do
  rg -F -q 'profiles/languages/rust/async.md' "$file"
done
rg -F -q '(async.md)' "$RUST_INDEX"

required_profile=(
  '## Select The Execution Contract'
  'Do not add `async` merely because a caller is asynchronous.'
  '## Preserve Genuine Async Contracts'
  'typed `unsupported` or `unavailable`'
  '## No Fallback'
  'Runtime construction, task ownership, shutdown'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_foundation="$(sed -n '1,/^## Runtime Boundaries$/p' "$LEGACY")"
if rg -q 'Default to synchronous|Libraries should default|```rust|fetch_user' \
  <<< "$legacy_foundation"; then
  printf 'legacy Rust async boundary default remains active\n' >&2
  exit 1
fi
for heading in '## Runtime Boundaries' '## Task Lifecycle' '## Graceful Shutdown' \
  '## Blocking Work' '## Mutex Selection' '## Cancellation Safety' '## Observability'; do
  rg -F -q "$heading" "$LEGACY"
done

rg -F -q '`7.4b4d` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-rust-async-decomposition.sh"

printf 'Rust async boundary policy passed: %s decisions, 2 exact dispositions\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
