#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/router/root-route-evidence.tsv"
ROUTER="$R/STANDARDS-ROUTER.md"
README="$R/README.md"
D="$S/consolidation-dispositions.tsv"

count=0
while IFS=$'\t' read -r concern owner extra; do
  [[ "$concern" == concern ]] && continue
  [[ -z "${extra:-}" ]]
  rg -F -q "($owner)" "$ROUTER"
  ((count += 1))
done < "$F"

for text in '[Standards Router](STANDARDS-ROUTER.md)' \
  'does not select modules or establish canonical ownership' \
  'Unknown applicability is a Router diagnostic'; do
  rg -F -q "$text" "$README"
done

for text in '## Documents' '| Document | Purpose | When to Use |' \
  'Remaining frontend mechanism' 'awaiting ordered canonical population' \
  '(topics/contracts.md)'; do
  ! rg -F -q "$text" "$README"
done

expected=(STD-0001 STD-0002 STD-0003)
mapfile -t disposed < <(
  awk -F '\t' '$1 >= "STD-0001" && $1 <= "STD-0003" { print $1 }' "$D"
)
[[ "${disposed[*]}" == "${expected[*]}" ]]

printf 'Root Router evidence passed: %s canonical routes, 3 exact dispositions\n' "$count"
