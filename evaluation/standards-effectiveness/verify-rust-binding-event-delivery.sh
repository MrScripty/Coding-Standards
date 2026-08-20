#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/binding-event-delivery-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/language-bindings.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"

count=0
while IFS=$'\t' read -r case_id contract mode authority capacity overflow \
  ordering thread input_state cancellation shutdown capability evidence \
  delivery fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ "$contract" =~ ^(selected|missing|contradictory)$ ]]
  [[ "$mode" =~ ^(push|pull|stream|unsupported)$ ]]
  [[ "$authority" =~ ^(selected|missing|wrong)$ ]]
  [[ "$capacity" =~ ^(governed|unbounded)$ ]]
  [[ "$overflow" =~ ^(selected|silent)$ ]]
  [[ "$ordering" =~ ^(selected|contradictory)$ ]]
  [[ "$thread" =~ ^(valid|wrong)$ ]]
  [[ "$input_state" =~ ^(current|carried)$ ]]
  [[ "$cancellation" =~ ^(owned|lost)$ ]]
  [[ "$shutdown" =~ ^(owned|unresolved)$ ]]
  [[ "$capability" =~ ^(available|unavailable)$ ]]
  [[ "$evidence" =~ ^(native-host|native-only|missing)$ ]]
  [[ "$delivery" =~ ^(success|failure)$ ]]
  [[ "$fallback" =~ ^(none|push-to-pull|pull-to-push|alternate-runtime|detached-work|default-success)$ ]]
  [[ "$expected" =~ ^(allow|preserve-failure|typed-invalid|typed-unsupported|typed-unavailable|typed-incomplete)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ||
        "$contract" == contradictory ||
        "$authority" == wrong ||
        "$capacity" == unbounded ||
        "$overflow" == silent ||
        "$ordering" == contradictory ||
        "$thread" == wrong ||
        "$input_state" == carried ||
        "$cancellation" == lost ]]; then
    actual=typed-invalid
  elif [[ "$mode" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$contract" == missing ||
          "$authority" == missing ||
          "$capability" == unavailable ||
          "$evidence" != native-host ]]; then
    actual=typed-unavailable
  elif [[ "$shutdown" == unresolved ]]; then
    actual=typed-incomplete
  elif [[ "$delivery" == failure ]]; then
    actual=preserve-failure
  else
    actual=allow
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
  ((count += 1))
done < "$FIXTURE"
[[ "$count" -eq 21 ]]

for id in STD-0778 STD-0779; do
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { count++ } END { print count + 0 }' \
    "$INVENTORY")" -eq 1 ]]
  awk -F '\t' -v id="$id" '
    NR > 1 && $1 == id {
      count += 1
      if ($2 != "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" ||
          $3 != "profiles/languages/rust/language-bindings.md" ||
          $4 != "refine" || $5 == "" || NF != 5) {
        exit 1
      }
    }
    END { exit count != 1 }
  ' "$DISPOSITIONS"
done

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/concurrency.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$REPO_ROOT/topics/security.md" \
  "$REPO_ROOT/profiles/boundaries/interop.md" \
  "$REPO_ROOT/profiles/boundaries/language-bindings.md" \
  "$REPO_ROOT/profiles/languages/rust/README.md" \
  "$PROFILE"

required_profile=(
  '## Host Event Delivery'
  'push, pull, stream, or another declared delivery mode'
  'Push and pull are peer contract choices'
  'does not authorize carrying an earlier event'
  'Do not retain events'
  'without a bound or discard them silently'
  'outside synchronization guards'
  'Concurrency work ownership'
  'Interop event-registration contract'
  'Preserve provider and host delivery failures'
  'Return `invalid`'
  '`unsupported`'
  '`unavailable`'
  'selected typed incomplete outcome'
  'Do not substitute push for pull or pull for push'
  'report default success'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_event="$(
  sed -n '/^## Host-Language Callbacks and Event Delivery$/,/^### Callback-Based Task Execution$/p' \
    "$LEGACY"
)"
rg -F -q \
  'profiles/languages/rust/language-bindings.md#host-event-delivery' \
  <<< "$legacy_event"
for pattern in \
  'Prefer push-based delivery' \
  'Use pull-based delivery as a fallback' \
  'BufferedEventSink' \
  'BeamEventSink' \
  'drain_events' \
  'events may lag' \
  '```'; do
  ! rg -F -q "$pattern" <<< "$legacy_event"
done

rg -F -q '### Callback-Based Task Execution' "$LEGACY"

"$SCRIPT_DIR/verify-interop-event-registration.sh"
"$SCRIPT_DIR/verify-concurrency-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"
printf 'Rust binding event delivery passed: %s decisions, 2 exact dispositions\n' \
  "$count"
