#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case authority projection synchronization interaction evidence fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$fallback" != none ]]; then actual=typed-invalid
  elif [[ "$authority" == contradictory || "$interaction" == ambiguous ||
          "$interaction" == inaccessible ]]; then actual=typed-invalid
  elif [[ "$interaction" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$authority" == missing || "$evidence" == missing ]]; then
    actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/frontend/owner-contract-decisions.tsv"
for text in 'ID: `profile.application.frontend`' '## Projection Authority' \
  '## Rendering And Synchronization' '## Interaction And Accessibility' \
  'infer domain authority' \
  'source contract is' \
  'not interaction proof'; do
  rg -F -q "$text" "$R/profiles/applications/frontend.md"
done
rg -F -q '[profiles/applications/frontend.md](profiles/applications/frontend.md)' \
  "$R/README.md"
rg -F -q '[Frontend application profile](profiles/applications/frontend.md)' \
  "$R/STANDARDS-ROUTER.md"
rg -F -q '[Frontend application profile](profiles/applications/frontend.md)' \
  "$R/CODING-STANDARDS.md"
! rg -F -q '[FRONTEND-STANDARDS.md](FRONTEND-STANDARDS.md)' \
  "$R/CODING-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1=="STD-0187"{print $1}' \
  "$S/consolidation-dispositions.tsv")
[[ "${ids[*]}" == 'STD-0187' ]]
rg -F -q '`7.4b8bq` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bz` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8ca` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Frontend owner contract passed: 17 decisions, 1 disposition\n'
