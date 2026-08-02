#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/rust/api-rustdoc-decisions.tsv"
readonly PROFILE="$R/profiles/languages/rust/api.md"
readonly LEGACY="$R/languages/rust/RUST-API-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case_id documentation contracts resilience dependencies \
  unsafe library mechanism capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$documentation" == contradictory ||
        "$contracts" == contradictory || "$resilience" == contradictory ||
        "$dependencies" == contradictory || "$unsafe" == contradictory ||
        "$library" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$documentation" == missing || "$contracts" == missing ||
          "$resilience" == missing || "$dependencies" == missing ||
          "$unsafe" == missing || "$library" == missing ]]; then
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

for text in '## Rustdoc Expression Mechanisms' \
  'After Documentation selects the documentation trigger, artifact, placement' \
  'audience, and quality contract, and after each content owner supplies its' \
  'toolchain, and evidence claim. Rustdoc form cannot create or weaken the fact it' \
  'Rustdoc forms are not documentation defaults' \
  'applicable owner decision. The Rust Unsafe profile remains authoritative for'; do
  rg -F -q "$text" "$PROFILE"
done

rg -F -q 'non-normative migration index' "$LEGACY"
! rg -q '^## ' "$LEGACY"
[[ "$(wc -l < "$LEGACY")" -le 20 ]]
for route in 'profiles/languages/rust/api.md' 'topics/contracts.md' \
  'topics/security.md' 'topics/architecture.md' 'topics/resilience.md' \
  'topics/dependencies.md' 'workflows/documentation.md' \
  'workflows/verification.md' 'profiles/applications/library.md' \
  'profiles/languages/rust/unsafe.md'; do
  rg -F -q "$route" "$LEGACY"
done
! rg -F -q 'Required documentation:' "$LEGACY"
! rg -F -q '# Safety' "$LEGACY"

expected=$'STD-0716\tlanguages/rust/RUST-API-STANDARDS.md\tprofiles/languages/rust/api.md\tsplit'
actual="$(awk -F '\t' '$1 == "STD-0716" {
  print $1 "\t" $2 "\t" $3 "\t" $4
}' "$DISPOSITIONS")"
[[ "$actual" == "$expected" ]]

printf 'Rust API Rustdoc passed: 18 decisions, 1 exact disposition, legacy closed\n'
