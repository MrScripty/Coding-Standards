#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/rust/api-failure-decisions.tsv"
readonly PROFILE="$R/profiles/languages/rust/api.md"
readonly LEGACY="$R/languages/rust/RUST-API-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case_id contract resilience outcome mechanism \
  capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ||
        "$resilience" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$contract" == missing || "$resilience" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then
    actual=typed-unsupported
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

for text in '## Failure Expression Mechanisms' \
  'After Contracts selects expected absence, invariant, validation' \
  'after Resilience selects every applicable' \
  'express those decisions with supported Rust mechanisms. The Rust profile does' \
  'not infer whether a condition is absent, failed, invalid, impossible' \
  'not replace a missing proof, recovery decision, or typed outcome' \
  'These are language mechanisms, not situation defaults'; do
  rg -F -q "$text" "$PROFILE"
done

! rg -F -q '| Situation | Use |' "$LEGACY"
! rg -F -q 'Allowed exceptions:' "$LEGACY"
! rg -F -q 'Prefer `expect(' "$LEGACY"
rg -F -q '[Contracts](../../topics/contracts.md)' "$LEGACY"
rg -F -q '[Resilience](../../topics/resilience.md)' "$LEGACY"

expected=(
  $'STD-0711\tlanguages/rust/RUST-API-STANDARDS.md\tprofiles/languages/rust/api.md\tsplit'
  $'STD-0712\tlanguages/rust/RUST-API-STANDARDS.md\tprofiles/languages/rust/api.md\tsplit'
)
mapfile -t actual < <(
  awk -F '\t' '$1 == "STD-0711" || $1 == "STD-0712" {
    print $1 "\t" $2 "\t" $3 "\t" $4
  }' "$DISPOSITIONS"
)
[[ "${actual[*]}" == "${expected[*]}" ]]

printf 'Rust API failures passed: 18 decisions, 2 exact dispositions\n'
