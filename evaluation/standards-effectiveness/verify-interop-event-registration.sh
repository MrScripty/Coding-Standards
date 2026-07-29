#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/interop/event-registration-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/boundaries/interop.md"
readonly CONCURRENCY="$REPO_ROOT/topics/concurrency.md"
readonly LEGACY="$REPO_ROOT/INTEROP-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

order_is_complete_and_safe() {
  local order="$1"
  local -a steps
  local -A seen=()
  local index quiesce_index=0 release_index=0

  IFS='>' read -r -a steps <<< "$order"
  [[ "${#steps[@]}" -eq 5 ]] || return 1
  for index in "${!steps[@]}"; do
    case "${steps[$index]}" in
      delivery-stop|quiesce|unregister|release|provider-shutdown) ;;
      *) return 1 ;;
    esac
    [[ -z "${seen[${steps[$index]}]:-}" ]] || return 1
    seen["${steps[$index]}"]=1
    [[ "${steps[$index]}" == 'quiesce' ]] && quiesce_index=$((index + 1))
    [[ "${steps[$index]}" == 'release' ]] && release_index=$((index + 1))
  done
  [[ "${#seen[@]}" -eq 5 && "$quiesce_index" -lt "$release_index" ]]
}

while IFS=$'\t' read -r case_id phase provider_delivery local_work work_owner \
  input_scope in_flight unregister_action unregister_contract \
  unregister_outcome order_contract selected_order observed_order release \
  capability fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$phase" =~ ^(pre-registration|active|unregistering|released)$ ]]
  [[ "$provider_delivery" =~ ^(not-started|synchronous|asynchronous|stopped)$ ]]
  [[ "$local_work" =~ ^(none|inline|outliving)$ ]]
  [[ "$work_owner" =~ ^(not-required|callback-scope|concurrency-owner|missing)$ ]]
  [[ "$input_scope" =~ ^(none|current|retained-prior)$ ]]
  [[ "$in_flight" =~ ^(not-started|none|drain-complete|cancel-complete|incomplete|unknown)$ ]]
  [[ "$unregister_action" =~ ^(none|single|repeated|concurrent)$ ]]
  [[ "$unregister_contract" =~ ^(not-required|selected|missing)$ ]]
  [[ "$unregister_outcome" =~ ^(not-required|success|provider-idempotent|provider-reject|shared-result|incomplete|unknown)$ ]]
  [[ "$order_contract" =~ ^(not-required|selected|missing)$ ]]
  [[ "$release" =~ ^(not-required|complete|incomplete|unavailable)$ ]]
  [[ "$capability" =~ ^(available|unsupported|unavailable)$ ]]
  [[ "$fallback" =~ ^(none|destruction-cleanup|finalizer-cleanup|gc-cleanup|silent-drop|stale-registration|wrong-thread-retry|alternate-event|detached-work|carry-forward|assume-idempotent|universal-order|claim-cleanup)$ ]]
  [[ "$expected" =~ ^(allow|preserve-provider-outcome|typed-invalid|typed-unsupported|typed-unavailable|typed-incomplete)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$selected_order" != 'not-required' ]]; then
    order_is_complete_and_safe "$selected_order" || {
      printf '%s: selected lifecycle order is incomplete or unsafe\n' \
        "$case_id" >&2
      exit 1
    }
  fi
  if [[ ! "$observed_order" =~ ^(not-required|unknown|incomplete)$ ]]; then
    order_is_complete_and_safe "$observed_order" || {
      printf '%s: observed lifecycle order is incomplete or unsafe\n' \
        "$case_id" >&2
      exit 1
    }
  fi

  if [[ "$input_scope" == 'retained-prior' ||
        ( "$local_work" == 'outliving' &&
          "$work_owner" != 'concurrency-owner' ) ||
        ( "$local_work" == 'inline' &&
          "$work_owner" != 'callback-scope' ) ||
        ( ! "$observed_order" =~ ^(not-required|unknown|incomplete)$ &&
          "$observed_order" != "$selected_order" ) ||
        ( "$phase" == 'released' &&
          ( "$provider_delivery" != 'stopped' || "$release" != 'complete' ) ) ]]; then
    actual='typed-invalid'
  elif [[ "$phase" == 'pre-registration' ]]; then
    if [[ "$capability" == 'unsupported' ]]; then
      actual='typed-unsupported'
    elif [[ "$capability" == 'unavailable' ||
            "$unregister_contract" != 'selected' ||
            "$order_contract" != 'selected' ]]; then
      actual='typed-unavailable'
    elif [[ "$fallback" != 'none' ]]; then
      actual='typed-invalid'
    else
      actual='allow'
    fi
  elif [[ "$capability" != 'available' ||
          "$unregister_contract" != 'selected' ||
          "$order_contract" != 'selected' ||
          "$in_flight" =~ ^(incomplete|unknown)$ ||
          "$unregister_outcome" =~ ^(incomplete|unknown)$ ||
          "$release" =~ ^(incomplete|unavailable)$ ||
          "$observed_order" =~ ^(unknown|incomplete)$ ||
          ( "$unregister_action" != 'none' &&
            "$observed_order" == 'not-required' ) ]]; then
    actual='typed-incomplete'
  elif [[ "$fallback" != 'none' ]]; then
    actual='typed-invalid'
  elif [[ "$unregister_outcome" == 'provider-reject' ]]; then
    actual='preserve-provider-outcome'
  else
    actual='allow'
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

[[ "$(awk -F '\t' '$1 == "STD-0473" { count += 1 } END { print count + 0 }' \
  "$INVENTORY")" -eq 1 ]]
[[ "$(awk -F '\t' 'NR > 1 && $1 == "STD-0473" { count += 1 } END { print count + 0 }' \
  "$DISPOSITIONS")" -eq 1 ]]
awk -F '\t' '
  NR > 1 && $1 == "STD-0473" {
    if ($2 != "INTEROP-STANDARDS.md" ||
        $3 != "profiles/boundaries/interop.md" ||
        $4 != "refine" || $5 == "" || NF != 5) {
      exit 1
    }
    found = 1
  }
  END { exit !found }
' "$DISPOSITIONS"

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$REPO_ROOT/topics/security.md" \
  "$PROFILE"

metadata="$(
  sed -n '/^\*\*Standards metadata\*\*$/,/^## Foreign Authority$/p' "$PROFILE"
)"
if rg -F -q 'topic.concurrency' <<< "$metadata"; then
  printf 'Interop metadata makes conditional Concurrency selection unconditional\n' >&2
  exit 1
fi

required_profile=(
  '## Event Registration Lifecycle'
  '`pre-registration`, `active`, `unregistering`, and `released`'
  'missing required capability before registration is `unavailable`'
  'typed incomplete-cleanup outcome'
  'does not determine whether work created by the callback outlives'
  'topics/concurrency.md#own-work-failure-and-cancellation'
  'only its current callback input'
  'retaining prior callback input'
  'provider contract selects the valid result of repeated or concurrent'
  'idempotent success, a shared terminal result'
  'typed rejection; no one outcome is universal'
  'selects the valid order'
  'Do not report successful cleanup'
  '## No Fallback'
  'detaching outliving callback work from Concurrency ownership'
  'Rejecting an attempted fallback does not replace the diagnostic'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE" || {
    printf 'missing event-registration profile requirement: %s\n' "$text" >&2
    exit 1
  }
done
rg -F -q '## Own Work, Failure, And Cancellation' "$CONCURRENCY"

legacy_event="$(
  sed -n '/^### 6\. Event Subscription Lifecycle$/,/^## Cross-Language Contract Maintenance$/p' \
    "$LEGACY"
)"
rg -F -q 'profiles/boundaries/interop.md#event-registration-lifecycle' \
  <<< "$legacy_event"
for pattern in '```' 'destroyed' 'Dispose' 'cleanup/unmount' \
  '_sourceNode' 'eventBus.on' 'eventBus.off'; do
  if rg -F -q "$pattern" <<< "$legacy_event"; then
    printf 'legacy event-registration guidance remains: %s\n' "$pattern" >&2
    exit 1
  fi
done
for heading in '## Cross-Language Contract Maintenance' \
  '## Serialization Format Alignment' '## When These Rules Apply'; do
  rg -F -q "$heading" "$LEGACY"
done

for phase in pre-registration active unregistering released; do
  awk -F '\t' -v phase="$phase" 'NR > 1 && $2 == phase { found = 1 } END { exit !found }' \
    "$FIXTURE"
done
for tuple in \
  $'synchronous\tinline' \
  $'asynchronous\tinline' \
  $'synchronous\toutliving' \
  $'asynchronous\toutliving'; do
  delivery="${tuple%%$'\t'*}"
  work="${tuple#*$'\t'}"
  awk -F '\t' -v delivery="$delivery" -v work="$work" '
    NR > 1 && $3 == delivery && $4 == work { found = 1 }
    END { exit !found }
  ' "$FIXTURE"
done
awk -F '\t' '
  NR > 1 && $8 == "repeated" && $9 == "selected" &&
  $10 == "provider-idempotent" && $17 == "allow" { idempotent = 1 }
  NR > 1 && $8 == "repeated" && $9 == "selected" &&
  $10 == "provider-reject" && $17 == "preserve-provider-outcome" {
    repeated_reject = 1
  }
  NR > 1 && $8 == "concurrent" && $9 == "selected" &&
  $10 == "shared-result" && $17 == "allow" { shared = 1 }
  NR > 1 && $8 == "concurrent" && $9 == "selected" &&
  $10 == "provider-reject" && $17 == "preserve-provider-outcome" {
    concurrent_reject = 1
  }
  END { exit !(idempotent && repeated_reject && shared && concurrent_reject) }
' "$FIXTURE"
[[ "$(
  awk -F '\t' '
    NR > 1 && $12 == $13 &&
    ($17 == "allow" || $17 == "preserve-provider-outcome") &&
    $12 != "not-required" { orders[$12] = 1 }
    END { print length(orders) }
  ' "$FIXTURE"
)" -ge 4 ]]
awk -F '\t' '
  NR > 1 && $2 == "pre-registration" && $15 == "unavailable" &&
  $17 == "typed-unavailable" { found = 1 }
  END { exit !found }
' "$FIXTURE"
awk -F '\t' '
  NR > 1 && $2 != "pre-registration" && $15 == "unavailable" &&
  $17 == "typed-incomplete" { found = 1 }
  END { exit !found }
' "$FIXTURE"
awk -F '\t' '
  NR > 1 && $2 == "pre-registration" && $16 != "none" &&
  $17 == "typed-unavailable" { pre_fallback = 1 }
  NR > 1 && $2 != "pre-registration" && $16 != "none" &&
  $17 == "typed-incomplete" { active_fallback = 1 }
  END { exit !(pre_fallback && active_fallback) }
' "$FIXTURE"
awk -F '\t' '
  NR > 1 && ($8 == "repeated" || $8 == "concurrent") &&
  $9 != "selected" && $17 == "typed-incomplete" { found = 1 }
  END { exit !found }
' "$FIXTURE"

rg -F -q '| F049 | Resolved in Milestone 7.4b7g |' "$FINDINGS"
rg -F -q '`7.4b7g` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-concurrency-policy.sh"
"$SCRIPT_DIR/verify-interop-boundary-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-independent-trust-replan.sh"

printf 'Interop event registration passed: %s decisions, 1 exact disposition\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
