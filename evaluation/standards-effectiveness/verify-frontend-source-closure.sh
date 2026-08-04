#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/frontend/index-routes.tsv"
D="$S/consolidation-dispositions.tsv"
L="$R/FRONTEND-STANDARDS.md"
A="$R/topics/accessibility.md"

count=0
while IFS=$'\t' read -r concern owner extra; do
  [[ "$concern" == concern ]] && continue
  [[ -z "${extra:-}" ]]
  rg -F -q "($owner)" "$L"
  ((count += 1))
done < "$F"

for text in 'non-normative compatibility index' 'defines no frontend' \
  'selects no' 'never this' '[Accessibility](topics/accessibility.md)'; do
  rg -F -q "$text" "$L"
done

for text in '## Scope' '## Rendering and DOM Updates' \
  '## UI State Synchronization' '### Hook/Composable Timer Management' \
  '## Frontend Tooling Notes' '## Frontend Testing' '## Accessibility' \
  'getByRole' 'userEvent' 'fireEvent' 'setInterval' 'eslint-plugin'; do
  ! rg -F -q "$text" "$L"
done

for text in '## Accessibility Authority' '## Outcome And Modality Selection' \
  '## Responsibility Boundaries' '## Typed Outcomes' \
  'Do not continue by assuming a web interface'; do
  rg -F -q "$text" "$A"
done

expected=(STD-{0449..0464})
mapfile -t disposed < <(
  awk -F '\t' '$1 >= "STD-0449" && $1 <= "STD-0464" { print $1 }' "$D"
)
[[ "${disposed[*]}" == "${expected[*]}" ]]
rg -F -q $'STD-0464\tFRONTEND-STANDARDS.md\ttopics/accessibility.md\tindex' "$D"

"$S/verify-accessibility-owner-contract.sh"
printf 'Frontend source closure passed: %s canonical routes, 16 exact dispositions\n' "$count"
