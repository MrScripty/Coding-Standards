#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/rust/api-owner-decisions.tsv"
readonly PROFILE="$R/profiles/languages/rust/api.md"
readonly LEGACY="$R/languages/rust/RUST-API-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case_id contract consumer mechanism semantics ownership \
  capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ||
        "$semantics" == contradictory || "$ownership" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$contract" == missing || "$consumer" == unknown ]]; then
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

"$S/check-metadata.sh" "$R" "$R/CORE-STANDARDS.md" \
  "$R/workflows/verification.md" "$R/workflows/release.md" \
  "$R/topics/contracts.md" "$R/topics/architecture.md" \
  "$R/topics/resilience.md" "$R/topics/dependencies.md" \
  "$R/workflows/documentation.md" "$R/profiles/applications/library.md" \
  "$R/profiles/languages/rust/README.md" "$PROFILE"

for text in '## API Mechanism Authority' \
  'Generic owners select invariants' '## Public Contract Trait Mechanisms' \
  'are mechanisms, not baseline requirements' \
  '## Parameter And Ownership Mechanisms' '## Typed Outcomes' \
  'Do not fall back to an incumbent signature' '## Verification'; do
  rg -F -q "$text" "$PROFILE"
done

rg -F -q '[Rust API profile](../../profiles/languages/rust/api.md)' "$LEGACY"
! sed -n '/^## Public Contract Traits$/,/^## Parameter Ergonomics$/p' "$LEGACY" |
  rg -F -q 'Implement or derive'
! sed -n '/^## Parameter Ergonomics$/,/^## Feature Contracts$/p' "$LEGACY" |
  rg -F -q 'Use `impl AsRef'

expected=(
  $'STD-0706\tlanguages/rust/RUST-API-STANDARDS.md\tprofiles/languages/rust/api.md\tindex'
  $'STD-0713\tlanguages/rust/RUST-API-STANDARDS.md\tprofiles/languages/rust/api.md\trefine'
  $'STD-0714\tlanguages/rust/RUST-API-STANDARDS.md\tprofiles/languages/rust/api.md\trefine'
)
mapfile -t actual < <(
  awk -F '\t' '$1 == "STD-0706" || $1 == "STD-0713" || $1 == "STD-0714" {
    print $1 "\t" $2 "\t" $3 "\t" $4
  }' "$DISPOSITIONS"
)
[[ "${actual[*]}" == "${expected[*]}" ]]

printf 'Rust API owner contract passed: 14 decisions, 3 exact dispositions\n'
