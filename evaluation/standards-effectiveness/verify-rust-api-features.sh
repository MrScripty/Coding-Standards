#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/rust/api-feature-decisions.tsv"
readonly PROFILE="$R/profiles/languages/rust/api.md"
readonly LEGACY="$R/languages/rust/RUST-API-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case_id dependencies contracts library documentation \
  verification mechanism capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$dependencies" == contradictory ||
        "$contracts" == contradictory || "$library" == contradictory ||
        "$documentation" == contradictory || "$verification" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$dependencies" == missing || "$contracts" == missing ||
          "$library" == missing || "$documentation" == missing ||
          "$verification" == missing ]]; then
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

for text in '## Cargo Feature Expression Mechanisms' \
  'After Dependencies selects feature, optional-dependency, default, target' \
  'selects supported real consumer configurations; Documentation selects durable' \
  'artifacts; and Verification selects claim-matched evidence' \
  'Cargo mechanisms are not feature-policy defaults' \
  'generic owner decisions and capability evidence'; do
  rg -F -q "$text" "$PROFILE"
done

! rg -F -q 'Keep default features minimal' "$LEGACY"
! rg -F -q 'cargo check --workspace --all-features' "$LEGACY"
! rg -F -q 'Optional deeper checks with `cargo hack`' "$LEGACY"
for route in 'topics/dependencies.md' 'topics/contracts.md' \
  'profiles/applications/library.md' 'workflows/documentation.md' \
  'workflows/verification.md'; do
  rg -F -q "$route" "$LEGACY"
done

expected=$'STD-0715\tlanguages/rust/RUST-API-STANDARDS.md\tprofiles/languages/rust/api.md\tsplit'
actual="$(awk -F '\t' '$1 == "STD-0715" {
  print $1 "\t" $2 "\t" $3 "\t" $4
}' "$DISPOSITIONS")"
[[ "$actual" == "$expected" ]]

printf 'Rust API features passed: 19 decisions, 1 exact disposition\n'
