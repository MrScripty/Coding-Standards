#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/security/network-transport-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/topics/security.md"
readonly CONCURRENCY="$REPO_ROOT/topics/concurrency.md"
readonly LEGACY="$REPO_ROOT/SECURITY-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id exposure exposure_contract capacity admission \
  tracking outcome shutdown cancellation drain termination liveness \
  liveness_contract capability fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$exposure" =~ ^(local|remote|broad|unknown)$ ]]
  [[ "$exposure_contract" =~ ^(declared|missing)$ ]]
  [[ "$capacity" =~ ^(available|full|missing|default)$ ]]
  [[ "$admission" =~ ^(before-accept|after-accept|closed|open)$ ]]
  [[ "$tracking" =~ ^(registered|detached|discarded|missing|not-required)$ ]]
  [[ "$outcome" =~ ^(observed-success|observed-failure|observed-cancel|discarded|leaf-logged|not-required)$ ]]
  [[ "$shutdown" =~ ^(active|ordered|open-admission)$ ]]
  [[ "$cancellation" =~ ^(signalled|missing|not-required)$ ]]
  [[ "$drain" =~ ^(complete|incomplete|missing|not-required)$ ]]
  [[ "$termination" =~ ^(none|authorized-safe|authorized-unsafe|unauthorized|default-force)$ ]]
  [[ "$liveness" =~ ^(protocol-close|keepalive|heartbeat|idle-deadline|none|default)$ ]]
  [[ "$liveness_contract" =~ ^(selected|missing|not-required)$ ]]
  [[ "$capability" =~ ^(available|unsupported|unavailable)$ ]]
  [[ "$fallback" =~ ^(none|broad-bind|default-address|default-capacity|accept-first|detached-work|discard-outcome|leaf-logging|open-admission|force-close|fixed-timeout|default-liveness|alternate-runtime|alternate-listener)$ ]]
  [[ "$expected" =~ ^(allow|typed-overload|typed-invalid|typed-unsupported|typed-unavailable|typed-incomplete)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != 'none' ||
        "$exposure" == 'broad' ||
        "$capacity" == 'default' ||
        "$admission" =~ ^(after-accept|open)$ ||
        "$tracking" =~ ^(detached|discarded)$ ||
        "$outcome" =~ ^(discarded|leaf-logged)$ ||
        "$shutdown" == 'open-admission' ||
        "$termination" =~ ^(authorized-unsafe|unauthorized|default-force)$ ||
        "$liveness" == 'default' ]]; then
    actual='typed-invalid'
  elif [[ "$exposure" == 'unknown' ||
          "$exposure_contract" == 'missing' ||
          "$capacity" == 'missing' ||
          "$tracking" == 'missing' ||
          "$cancellation" == 'missing' ||
          "$drain" == 'missing' ||
          "$liveness_contract" == 'missing' ||
          "$capability" == 'unavailable' ]]; then
    actual='typed-unavailable'
  elif [[ "$capability" == 'unsupported' ]]; then
    actual='typed-unsupported'
  elif [[ "$capacity" == 'full' ]]; then
    actual='typed-overload'
  elif [[ "$drain" == 'incomplete' ]]; then
    actual='typed-incomplete'
  else
    actual='allow'
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

expected_ids=(STD-0596 STD-0597 STD-0598 STD-0599 STD-0600)
mapfile -t inventory_ids < <(
  awk -F '\t' '$1 >= "STD-0596" && $1 <= "STD-0600" { print $1 }' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0596" && $1 <= "STD-0600" { print $1 }' \
    "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in STD-0596|STD-0597|STD-0598|STD-0599|STD-0600) ;; *) continue ;; esac
  [[ "$source" == 'SECURITY-STANDARDS.md' ]]
  [[ "$target" == 'topics/security.md' ]]
  [[ "$disposition" == 'refine' ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$CONCURRENCY" \
  "$REPO_ROOT/profiles/boundaries/ipc.md" \
  "$PROFILE"

required_profile=(
  '## Network Transport Boundary'
  'service and deployment contract'
  'Acquire admission before accepting work'
  'register the connection work with the selected lifecycle'
  'observes success, failure, and cancellation'
  'Close admission before signalling cancellation'
  'explicit authority'
  'proven interruption-safe'
  'Select connection-liveness behavior from protocol semantics'
  'typed `invalid`'
  '`unsupported`, `unavailable`, overload'
  '### No Fallback'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done
rg -F -q '## Own Work, Failure, And Cancellation' "$CONCURRENCY"

for link in \
  'topics/security.md#network-transport-boundary' \
  'topics/concurrency.md#own-work-failure-and-cancellation' \
  'topics/contracts.md#runtime-decoding-at-boundaries' \
  'profiles/boundaries/ipc.md'; do
  rg -F -q "$link" "$LEGACY"
done
for pattern in '127.0.0.1' '0.0.0.0' '::1' 'platform'\''s loopback address' \
  'Every listener must define' 'semaphore' 'bounded worker pool' \
  'force-close remaining' '30–60 seconds' \
  'Graceful Shutdown of Spawned Services'; do
  if rg -F -q "$pattern" "$LEGACY"; then
    printf 'legacy network transport default remains: %s\n' "$pattern" >&2
    exit 1
  fi
done

rg -F -q '| F016 | Resolved in Milestone 7.4b7a |' "$FINDINGS"
rg -F -q '`7.4b7a` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-concurrency-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-independent-trust-replan.sh"

printf 'Network transport policy passed: %s decisions, 5 exact dispositions\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
