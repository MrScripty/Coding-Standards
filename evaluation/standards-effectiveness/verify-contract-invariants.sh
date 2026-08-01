#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case owner contract caller outcomes enforcement evidence capability fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$fallback" != none || "$caller" == hidden || "$outcomes" == partial ]]; then actual=typed-invalid
  elif [[ "$contract" == violated ]]; then actual=typed-invalid
  elif [[ "$contract" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$owner" == unknown || "$capability" == unavailable ||
          "$enforcement" == missing || "$evidence" == missing ]]; then actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/contracts/invariant-decisions.tsv"
for text in '## Invariant Contracts' 'Preconditions describe facts' \
  'mode alone does not decide' 'Verification selects evidence' \
  'Do not require one test per sentence' 'debug-only enforcement'; do
  rg -F -q "$text" "$R/topics/contracts.md"
done
! rg -F -q '### Validation Strategy' "$R/CODING-STANDARDS.md"
! rg -F -q 'Every invariant should have corresponding tests' "$R/CODING-STANDARDS.md"
rg -F -q 'topics/contracts.md#invariant-contracts' "$R/CODING-STANDARDS.md"
rg -F -q 'workflows/verification.md#selecting-claims' "$R/CODING-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0167"&&$1<="STD-0173"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0167 STD-0168 STD-0169 STD-0170 STD-0171 STD-0172 STD-0173' ]]
rg -F -q '`7.4b8bk` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8cc` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Contract invariants passed: 15 decisions, 7 dispositions\n'
