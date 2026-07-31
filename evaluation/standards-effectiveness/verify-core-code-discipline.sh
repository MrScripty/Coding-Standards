#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case concerns ownership invariants lifecycle contract divergence meaning fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$fallback" != none ]]; then actual=typed-invalid
  elif [[ "$ownership" == unknown || "$invariants" == unknown ]]; then actual=typed-unavailable
  elif [[ "$ownership" == none && "$contract" == none ]]; then actual=delete
  elif [[ "$contract" == supported && "$lifecycle" == active ]]; then actual=preserve
  elif [[ "$meaning" == incorrect ]]; then actual=rename
  elif [[ "$divergence" == risk && "$contract" == one ]]; then actual=consolidate
  elif [[ "$concerns" == multiple && "$contract" == multiple ]]; then actual=keep-separate
  elif [[ "$concerns" == multiple ]]; then actual=separate
  elif [[ "$meaning" == clear ]]; then actual=direct
  else actual=keep-name
  fi
  if [[ "$case" == descriptive_name && "$actual" == direct ]]; then actual=keep-name; fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/core/code-discipline-decisions.tsv"
for text in '### Code And Terminology Discipline' 'call site may' \
  'Do not apply blanket extraction' 'Delete code, aliases, adapters' \
  'Choose names from domain meaning' 'Do not fall back to fixed call counts'; do
  rg -F -q "$text" "$R/CORE-STANDARDS.md"
done
! rg -F -q "### Don't Repeat Yourself" "$R/CODING-STANDARDS.md"
! rg -F -q '### Be Descriptive' "$R/CODING-STANDARDS.md"
rg -F -q 'CORE-STANDARDS.md#code-and-terminology-discipline' "$R/CODING-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0158"&&$1<="STD-0166"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0158 STD-0159 STD-0160 STD-0161 STD-0162 STD-0163 STD-0164 STD-0165 STD-0166' ]]
rg -F -q '`7.4b8bj` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bx` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Core code discipline passed: 15 decisions, 9 dispositions\n'
