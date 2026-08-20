#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/dependencies/population-decisions.tsv"
readonly OWNER="$R/topics/dependencies.md"
readonly LEGACY="$R/LAUNCHER-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"

while IFS=$'\t' read -r case_id requirement satisfaction authority procedure \
  postcheck identity fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$requirement" == contradictory ||
        "$authority" == missing ]]; then
    actual=typed-invalid
  elif [[ "$requirement" == missing || "$satisfaction" == unknown ||
          "$procedure" == missing || "$postcheck" != complete ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

required_owner=(
  '### Provisioning Procedure'
  'independently identifiable unit'
  'already satisfied requirement is not mutated'
  'preserves per-requirement'
  're-evaluate the same satisfaction contract'
  'Function names, process exit codes'
  'cannot create missing authority'
  'reinterpret failure as success'
)
for text in "${required_owner[@]}"; do
  rg -F -q "$text" "$OWNER"
done

rg -F -q '[Dependencies](topics/dependencies.md)' "$LEGACY"
! rg -F -q '## Dependency Installation Standards' "$LEGACY"
! rg -F -q 'check_<name>' "$LEGACY"
! rg -F -q 'install_<name>' "$LEGACY"
! rg -F -q 'monolithic check' "$LEGACY"

expected=(
  $'STD-0496\tLAUNCHER-STANDARDS.md\tLAUNCHER-STANDARDS.md\tindex'
  $'STD-0497\tLAUNCHER-STANDARDS.md\ttopics/dependencies.md\trefine'
  $'STD-0498\tLAUNCHER-STANDARDS.md\ttopics/dependencies.md\trefine'
)
mapfile -t actual < <(
  awk -F '\t' '$1 >= "STD-0496" && $1 <= "STD-0498" {
    print $1 "\t" $2 "\t" $3 "\t" $4
  }' "$DISPOSITIONS"
)
[[ "${actual[*]}" == "${expected[*]}" ]]


"$S/verify-dependencies-owner-contract.sh"
"$S/verify-launcher-population.sh"
"$S/verify-milestone-7-row-14-decomposition.sh"
"$S/verify-milestone-7-execution-train.sh"

printf 'Dependencies population passed: 14 decisions, 3 exact dispositions, row 14 complete\n'
