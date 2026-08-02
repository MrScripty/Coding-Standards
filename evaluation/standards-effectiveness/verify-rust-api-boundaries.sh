#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/rust/api-boundary-decisions.tsv"
readonly PROFILE="$R/profiles/languages/rust/api.md"
readonly LEGACY="$R/languages/rust/RUST-API-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case_id architecture public_surface platform mechanism \
  capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$architecture" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$architecture" == missing || "$public_surface" == missing ]]; then
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

for text in '## Crate And Module Boundary Mechanisms' \
  'After Architecture selects responsibility, dependency direction' \
  'and toolchain capability. Conditional compilation must preserve one coherent' \
  'Crates, modules, visibility modifiers, re-exports, and `cfg` are mechanisms' \
  'not architecture defaults. Do not prescribe `core`, `contracts`, `adapter`' \
  'without the accepted architecture and consumer facts'; do
  rg -F -q "$text" "$PROFILE"
done

! rg -F -q 'Common roles:' "$LEGACY"
! rg -F -q 'crate_name/' "$LEGACY"
! rg -F -q 'Keep `cfg()` in thin platform modules' "$LEGACY"
rg -F -q '[Architecture](../../topics/architecture.md)' "$LEGACY"

expected=(
  $'STD-0709\tlanguages/rust/RUST-API-STANDARDS.md\tprofiles/languages/rust/api.md\tsplit'
  $'STD-0710\tlanguages/rust/RUST-API-STANDARDS.md\tprofiles/languages/rust/api.md\tsplit'
)
mapfile -t actual < <(
  awk -F '\t' '$1 == "STD-0709" || $1 == "STD-0710" {
    print $1 "\t" $2 "\t" $3 "\t" $4
  }' "$DISPOSITIONS"
)
[[ "${actual[*]}" == "${expected[*]}" ]]

printf 'Rust API boundaries passed: 16 decisions, 2 exact dispositions\n'
