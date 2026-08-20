#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/security/input-validation-authority-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly SECURITY="$REPO_ROOT/topics/security.md"
readonly CONTRACTS="$REPO_ROOT/topics/contracts.md"
readonly LEGACY="$REPO_ROOT/SECURITY-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"

count=0
while IFS=$'\t' read -r case_id applicability contract authority coverage \
  capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ "$applicability" =~ ^(untrusted|trusted)$ ]]
  [[ "$contract" =~ ^(selected|missing|unsupported|not-required)$ ]]
  [[ "$authority" =~ ^(selected|generated|conformant|global|multiple|missing|not-required)$ ]]
  [[ "$coverage" =~ ^(complete|partial|not-required)$ ]]
  [[ "$capability" =~ ^(available|unavailable)$ ]]
  [[ "$fallback" =~ ^(none|global-validator|fixed-regex|fixed-length|cast|inline-duplicate|original-input|permissive-default|weaker-validator)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ||
        "$authority" =~ ^(global|multiple)$ ||
        "$coverage" == partial ]]; then
    actual=typed-invalid
  elif [[ "$contract" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$contract" == missing ||
          "$authority" == missing ||
          "$capability" == unavailable ]]; then
    actual=typed-unavailable
  elif [[ "$applicability" == trusted &&
          "$contract:$authority:$coverage" == \
            not-required:not-required:not-required ]]; then
    actual=allow
  elif [[ "$applicability" == untrusted &&
          "$contract" == selected &&
          "$authority" =~ ^(selected|generated|conformant)$ &&
          "$coverage" == complete ]]; then
    actual=allow
  else
    actual=typed-invalid
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
  ((count += 1))
done < "$FIXTURE"
[[ "$count" -eq 17 ]]

expected_ids=(STD-0588 STD-0589 STD-0590 STD-0591)
mapfile -t inventory_ids < <(
  awk -F '\t' '$1 >= "STD-0588" && $1 <= "STD-0591" { print $1 }' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0588" && $1 <= "STD-0591" { print $1 }' \
    "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in STD-0588|STD-0589|STD-0590|STD-0591) ;; *) continue ;; esac
  [[ "$source" == SECURITY-STANDARDS.md ]]
  [[ "$target" == topics/security.md ]]
  [[ "$disposition" == refine ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$CONTRACTS" \
  "$SECURITY"

required_security=(
  '## Input Validation Authority'
  'complete operation contract'
  'one canonical validation authority'
  'does not mandate'
  'consume the same'
  'conformance evidence'
  'Different operation'
  'proof-bearing representation'
  'typed `invalid`'
  '`unsupported`'
  '`unavailable`'
  'Do not fall back to a global catch-all validator'
)
for text in "${required_security[@]}"; do
  rg -F -q "$text" "$SECURITY"
done

rg -F -q 'topics/security.md#input-validation-authority' "$LEGACY"
for pattern in 'InputValidator' 'SafeNamePattern' 'Regex' 'minLength' \
  'maxLength' 'Runtime type check before cast' 'Bounds check before use' \
  'single implementation' '```csharp'; do
  if rg -F -q "$pattern" "$LEGACY"; then
    printf 'legacy validation fallback remains: %s\n' "$pattern" >&2
    exit 1
  fi
done

rg -F -q '| F056 | Resolved in Milestone 7.4b8a |' "$FINDINGS"
"$SCRIPT_DIR/verify-runtime-decoding-policy.sh"
"$SCRIPT_DIR/verify-filesystem-containment-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-independent-trust-replan.sh"

printf 'Input validation authority passed: %s decisions, 4 exact dispositions\n' \
  "$count"
