#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/rust/api-validation-decisions.tsv"
readonly PROFILE="$R/profiles/languages/rust/api.md"
readonly LEGACY="$R/languages/rust/RUST-API-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case_id contract enforcement proof source mechanism \
  capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ||
        "$proof" == stale ]]; then
    actual=typed-invalid
  elif [[ "$contract" == missing || "$enforcement" == missing ]]; then
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

for text in '## Validated Type And Conversion Mechanisms' \
  'selects an invariant owner, enforcement point, proof lifetime' \
  'invalidates its invariant; re-establish proof at the canonical enforcement' \
  'are mechanisms, not defaults' 'a parse-once slogan' \
  'mandate one conversion trait by input category' \
  'complete operation-specific validation'; do
  rg -F -q "$text" "$PROFILE"
done

! rg -F -q 'if this bug ships, how bad is it' "$LEGACY"
! rg -F -q 'pub struct Port' "$LEGACY"
! rg -F -q 'Use `TryFrom`' "$LEGACY"
rg -F -q 'topics/contracts.md' "$LEGACY"
rg -F -q 'topics/security.md' "$LEGACY"

expected=(
  $'STD-0707\tlanguages/rust/RUST-API-STANDARDS.md\tprofiles/languages/rust/api.md\tsplit'
  $'STD-0708\tlanguages/rust/RUST-API-STANDARDS.md\tprofiles/languages/rust/api.md\tsplit'
)
mapfile -t actual < <(
  awk -F '\t' '$1 == "STD-0707" || $1 == "STD-0708" {
    print $1 "\t" $2 "\t" $3 "\t" $4
  }' "$DISPOSITIONS"
)
[[ "${actual[*]}" == "${expected[*]}" ]]

printf 'Rust API validation passed: 15 decisions, 2 exact dispositions\n'
