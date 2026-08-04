#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/architecture/monorepo-role-decisions.tsv"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
REFERENCE="$R/reference/patterns/architecture.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case responsibilities owners contracts changes fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$owners" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$owners" == missing || "$contracts" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$responsibilities" == one || "$changes" == layout-only ]]; then
    actual=keep-together
  else
    actual=illustrate
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"

for text in '## Conditional Monorepo Role Catalog' \
  'These are descriptive labels, not required package kinds' \
  'The arrows follow selected stable contracts' \
  '### Conditional Schema-Sharing Example'; do
  rg -F -q "$text" "$REFERENCE"
done
for text in '[Architecture](topics/architecture.md)' \
  '[Contracts](topics/contracts.md)' \
  '[Architecture Pattern Reference](reference/patterns/architecture.md#conditional-monorepo-role-catalog)'; do
  rg -F -q "$text" "$LEGACY"
done

for prohibited in 'assign each package a stable architectural role' \
  'App packages may compose other roles' \
  'Tooling/config packages should support development workflows' \
  'place it in a contracts package' \
  'shared utilities ─'; do
  if rg -F -i -q "$prohibited" "$LEGACY" "$REFERENCE"; then
    printf 'fixed monorepo default remains active: %s\n' "$prohibited" >&2
    exit 1
  fi
done

expected=(STD-{0034..0039})
mapfile -t ids < <(
  awk -F '\t' '$1 >= "STD-0034" && $1 <= "STD-0039" { print $1 }' "$DISPOSITIONS"
)
[[ "${ids[*]}" == "${expected[*]}" ]]
while IFS=$'\t' read -r id owner disposition reference_treatment rationale; do
  [[ "$id" == id || "$id" < STD-0034 || "$id" > STD-0039 ]] && continue
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++; row=$3 FS $4 } END { print n+0 FS row }' "$DISPOSITIONS")" == "1	$owner	$disposition" ]]
done < "$S/milestone-7-row-36-owner-validation.tsv"

"$S/verify-architecture-layered-pattern.sh"
printf 'Architecture monorepo pattern passed: 8 decisions and 6 exact dispositions\n'
