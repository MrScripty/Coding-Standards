#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case material source terms activity obligations artifact_evidence fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$material" == project-owned ]]; then actual=not-applicable
  elif [[ "$fallback" != none ]]; then actual=typed-invalid
  elif [[ "$source" == conflicting ]]; then actual=typed-invalid
  elif [[ "$activity" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$source" == missing || "$terms" == missing ||
          "$activity" == missing || "$obligations" == missing ||
          "$artifact_evidence" == missing ]]; then actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/licensing/owner-contract-decisions.tsv"
for text in 'ID: `topic.licensing`' '## Authority And Ownership' \
  '## Compatibility And Obligations' '## Attribution And Provenance' \
  'authoritative terms' 'fixed license-name matrix' \
  'designated legal or licensing owner' 'Do not require one copied'; do
  rg -F -q "$text" "$R/topics/licensing.md"
done
rg -F -q '[topics/licensing.md](topics/licensing.md)' "$R/README.md"
rg -F -q '[Licensing](topics/licensing.md)' "$R/STANDARDS-ROUTER.md"
rg -F -q '[Licensing](topics/licensing.md)' "$R/CODING-STANDARDS.md"
! rg -F -q '| GPL | GPL projects only | Viral license |' "$R/CODING-STANDARDS.md"
! rg -F -q 'Priority Queue with Decrease-Key' "$R/CODING-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0179"&&$1<="STD-0182"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0179 STD-0180 STD-0181 STD-0182' ]]
rg -F -q '`7.4b8bn` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8cd` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Licensing owner contract passed: 16 decisions, 4 dispositions\n'
