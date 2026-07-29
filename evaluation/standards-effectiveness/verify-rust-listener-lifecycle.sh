#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/listener-lifecycle-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/security.md"
readonly ASYNC_PROFILE="$REPO_ROOT/profiles/languages/rust/async.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-SECURITY-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id exposure exposure_contract capacity admission \
  tracking outcome shutdown cancellation drain abort capability fallback \
  expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$exposure" =~ ^(local|remote|broad|unknown)$ ]]
  [[ "$exposure_contract" =~ ^(declared|missing)$ ]]
  [[ "$capacity" =~ ^(available|full|missing|default)$ ]]
  [[ "$admission" =~ ^(before-accept|after-accept|open|closed|not-required)$ ]]
  [[ "$tracking" =~ ^(registered|detached|discarded|missing|not-required)$ ]]
  [[ "$outcome" =~ ^(observed-success|observed-failure|observed-panic|observed-cancel|discarded|leaf-logged|not-required)$ ]]
  [[ "$shutdown" =~ ^(active|ordered|open-admission|not-required)$ ]]
  [[ "$cancellation" =~ ^(signalled|missing|not-required)$ ]]
  [[ "$drain" =~ ^(complete|incomplete|missing|not-required)$ ]]
  [[ "$abort" =~ ^(none|authorized-safe|authorized-unsafe|unauthorized)$ ]]
  [[ "$capability" =~ ^(available|unsupported|unavailable)$ ]]
  [[ "$fallback" =~ ^(none|broad-bind|default-capacity|accept-first|detached-work|discard-outcome|leaf-logging|open-admission|force-abort|alternate-runtime)$ ]]
  [[ "$expected" =~ ^(allow|typed-overload|typed-invalid|typed-unsupported|typed-unavailable|typed-incomplete)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != 'none' ||
        "$exposure" == 'broad' ||
        "$capacity" == 'default' ||
        "$admission" =~ ^(after-accept|open)$ ||
        "$tracking" =~ ^(detached|discarded)$ ||
        "$outcome" =~ ^(discarded|leaf-logged)$ ||
        "$shutdown" == 'open-admission' ||
        "$abort" =~ ^(authorized-unsafe|unauthorized)$ ]]; then
    actual='typed-invalid'
  elif [[ "$exposure" == 'unknown' ||
          "$exposure_contract" == 'missing' ||
          "$capacity" == 'missing' ||
          "$tracking" == 'missing' ||
          "$cancellation" == 'missing' ||
          "$drain" == 'missing' ||
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

[[ "$(awk -F '\t' '$1 == "STD-0825" { count += 1 } END { print count + 0 }' \
  "$INVENTORY")" -eq 1 ]]
[[ "$(awk -F '\t' 'NR > 1 && $1 == "STD-0825" { count += 1 } END { print count + 0 }' \
  "$DISPOSITIONS")" -eq 1 ]]
awk -F '\t' '
  NR > 1 && $1 == "STD-0825" {
    if ($2 != "languages/rust/RUST-SECURITY-STANDARDS.md" ||
        $3 != "profiles/languages/rust/security.md" ||
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
  "$REPO_ROOT/topics/security.md" \
  "$REPO_ROOT/topics/concurrency.md" \
  "$REPO_ROOT/profiles/languages/rust/README.md" \
  "$ASYNC_PROFILE" \
  "$PROFILE"

required_profile=(
  '## Listener Admission And Lifecycle'
  'service exposure contract'
  'before accepting work that would exceed the owned limit'
  'register connection work'
  'selected lifecycle owner before'
  'observe success, failure, panic, and'
  'cancellation; logging inside detached work is not ownership.'
  'close admission, signal cancellation, drain tracked work'
  'typed incomplete-shutdown outcome'
  'typed overload outcome before acceptance.'
  '## No Fallback'
  '## Verification'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

required_async=(
  '## Own Spawned Work'
  'observes success, failure, panic, and cancellation'
  '## Coordinate Shutdown'
  'closes admission for new owned work'
)
for text in "${required_async[@]}"; do
  rg -F -q "$text" "$ASYNC_PROFILE"
done

legacy_listener="$(
  sed -n '/^## Network Listener Limits$/,/^## Panic Policy$/p' "$LEGACY"
)"
for link in \
  'security.md#listener-admission-and-lifecycle' \
  'async.md#own-spawned-work' \
  'async.md#coordinate-shutdown'; do
  rg -F -q "$link" <<< "$legacy_listener"
done
for pattern in '0.0.0.0:9500' '127.0.0.1:9500' 'MAX_CONNECTIONS' \
  'Semaphore' 'acquire_owned' 'listener.accept()' 'tokio::spawn'; do
  if rg -F -q "$pattern" <<< "$legacy_listener"; then
    printf 'legacy listener mechanism remains: %s\n' "$pattern" >&2
    exit 1
  fi
done
rg -F -q '## Panic Policy' "$LEGACY"

rg -F -q '| F026 | Resolved in Milestone 7.4b5f |' "$FINDINGS"
rg -F -q '`7.4b5f` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-rust-async-lifecycle.sh"
"$SCRIPT_DIR/verify-milestone-7-f025-f026-decomposition.sh"

printf 'Rust listener lifecycle policy passed: %s decisions, 1 exact disposition\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
