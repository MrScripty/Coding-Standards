#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/frontend/view-model-lineage-decisions.tsv"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
FRONTEND="$R/profiles/applications/frontend.md"
RECIPE="$R/reference/recipes/frontend.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case authority source_contract projection interaction lifecycle fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$authority" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$authority" == missing || "$source_contract" == missing || "$interaction" == missing || "$lifecycle" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$projection" == unsupported ]]; then
    actual=typed-unsupported
  else
    actual=route
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"

for text in '[Frontend application profile](profiles/applications/frontend.md#projection-authority)' \
  '[Architecture](topics/architecture.md#data-and-state-authority)' \
  '[Verification](workflows/verification.md#selecting-claims)' \
  '[Frontend mechanism recipes](reference/recipes/frontend.md)' \
  'does not require a dedicated class'; do
  rg -F -q "$text" "$LEGACY"
done
for text in '## Projection Authority' '## Rendering And Synchronization'; do
  rg -F -q "$text" "$FRONTEND"
done
rg -F -q '## Illustrative Synchronization Mechanisms' "$RECIPE"

for prohibited in 'Separate data management from presentation using dedicated view model objects' \
  'Subscribe to data source' "Don't duplicate backend-owned data" \
  'class UserListViewModel' 'Forward action to backend' \
  'Same view model for different view implementations'; do
  if rg -F -i -q "$prohibited" "$LEGACY" "$RECIPE"; then
    printf 'fixed view-model default remains active: %s\n' "$prohibited" >&2
    exit 1
  fi
done

expected=(STD-{0081..0086})
mapfile -t ids < <(
  awk -F '\t' '$1 >= "STD-0081" && $1 <= "STD-0086" { print $1 }' "$DISPOSITIONS"
)
[[ "${ids[*]}" == "${expected[*]}" ]]
while IFS=$'\t' read -r id owner disposition reference_treatment rationale; do
  [[ "$id" == id || "$id" < STD-0081 || "$id" > STD-0086 ]] && continue
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++; row=$3 FS $4 } END { print n+0 FS row }' "$DISPOSITIONS")" == "1	$owner	$disposition" ]]
done < "$S/milestone-7-row-37-owner-validation.tsv"

"$S/verify-frontend-rendering-synchronization.sh"
"$S/verify-architecture-durable-workflow-pattern.sh"
printf 'Frontend view-model lineage passed: 12 decisions and 6 exact dispositions\n'
