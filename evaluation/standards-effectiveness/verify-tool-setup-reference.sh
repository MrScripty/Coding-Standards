#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/tooling/tool-setup-reference-decisions.tsv"
readonly REFERENCE="$R/reference/recipes/tooling.md"
readonly LEGACY="$R/TOOLING-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case_id role authority fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$role" == normative ||
        "$authority" != none ]]; then
    actual=typed-invalid
  else
    actual=allow-reference
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

for text in '## Legacy Tool Setup And Package Script Example' \
  'historical illustration only' '"lint:critical"' \
  '"prepare": "lefthook install"' 'none of this example is a default'; do
  rg -F -q "$text" "$REFERENCE"
done

rg -F -q 'legacy setup and package-script examples' "$LEGACY"
! rg -F -q '### Minimum Setup' "$LEGACY"
! rg -F -q '### Commands to Add' "$LEGACY"
! rg -F -q '"lint:critical"' "$LEGACY"

expected=(
  $'STD-0701\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove'
  $'STD-0702\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove'
)
mapfile -t actual < <(
  awk -F '\t' '$1 >= "STD-0701" && $1 <= "STD-0702" {
    print $1 "\t" $2 "\t" $3 "\t" $4
  }' "$DISPOSITIONS"
)
[[ "${actual[*]}" == "${expected[*]}" ]]

printf 'Tool setup reference passed: 10 decisions, 2 exact dispositions\n'
