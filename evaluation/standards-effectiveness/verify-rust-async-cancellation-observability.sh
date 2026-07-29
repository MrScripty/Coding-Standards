#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/async-cancellation-observability-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/async.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-ASYNC-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"

while IFS=$'\t' read -r case_id polling external durability cleanup owner \
  terminal inspection capability fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$polling" =~ ^(active|dropped|completed)$ ]]
  [[ "$external" =~ ^(none|cancelled|continues|unknown)$ ]]
  [[ "$durability" =~ ^(not-required|transactional|idempotent|resumable|compensating|unprotected)$ ]]
  [[ "$cleanup" =~ ^(not-required|explicit-async|drop-sync|drop-async-assumed|detached)$ ]]
  [[ "$owner" =~ ^(lifecycle|leaf|missing|not-required)$ ]]
  [[ "$terminal" =~ ^(observed|silent|not-required)$ ]]
  [[ "$inspection" =~ ^(evidence|tool-only|not-required)$ ]]
  [[ "$capability" =~ ^(available|unavailable)$ ]]
  [[ "$fallback" =~ ^(none|assume-external-cancel|drop-cleanup|leaf-log|tool-availability)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != 'none' ||
        "$durability" == 'unprotected' ||
        "$cleanup" =~ ^(drop-async-assumed|detached)$ ||
        "$owner" =~ ^(leaf|missing)$ ||
        "$terminal" == 'silent' ||
        "$inspection" == 'tool-only' ]]; then
    actual='typed-invalid'
  elif [[ "$capability" == 'unavailable' ]]; then
    actual='typed-unavailable'
  else
    actual='allow'
  fi
  [[ "$actual" == "$expected" ]]
done < "$FIXTURE"

expected_ids=(STD-0724 STD-0725)
mapfile -t inventory_ids < <(
  awk -F '\t' '$1 >= "STD-0724" && $1 <= "STD-0725" { print $1 }' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0724" && $1 <= "STD-0725" { print $1 }' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in STD-0724|STD-0725) ;; *) continue ;; esac
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
  '## Prove Cancellation State'
  'does not prove that external I/O'
  '## Preserve Durable Work'
  'transactional, idempotent, resumable, or compensating design'
  '## Own Asynchronous Cleanup'
  'Synchronous destruction may release synchronous resources'
  '## Own Lifecycle Evidence'
  'leaf logging does not establish terminal-state ownership'
  'Tool availability is not evidence'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_policy="$(sed -n '/^## Cancellation Safety$/,$p' "$LEGACY")"
for pattern in 'Dropping a future cancels it' 'async fn close' \
  '`Drop` is only' '`tracing` spans' 'tokio-console'; do
  if rg -F -q "$pattern" <<< "$legacy_policy" || rg -F -q "$pattern" "$PROFILE"; then
    printf 'legacy Rust async cancellation/observation default remains: %s\n' \
      "$pattern" >&2
    exit 1
  fi
done
for heading in '## Cancellation Safety' '## Observability'; do
  rg -F -q "$heading" "$LEGACY"
done

rg -F -q '| F045 | Resolved in Milestone 7.4b4g |' "$FINDINGS"
rg -F -q '`7.4b4g` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-rust-async-decomposition.sh"
"$SCRIPT_DIR/verify-milestone-7-trust-lifecycle-replan.sh"

printf 'Rust async cancellation/observability policy passed: %s decisions, 2 exact dispositions\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
