#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r case coherence ownership axes invariants lifecycle failure metric fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$metric" != none ]]; then actual=typed-invalid
  elif [[ "$ownership" == unknown || "$invariants" == unknown ]]; then actual=typed-unavailable
  elif [[ "$coherence" == one && "$axes" == one ]]; then actual=keep-together
  else actual=separate
  fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/core/simplicity-decisions.tsv"
for text in 'reduction of entanglement and reasoning load' 'Keep one coherent concern together' \
  'More named components can be simpler' 'Do not select a design from a file-length threshold'; do
  rg -F -q "$text" "$R/CORE-STANDARDS.md"
done
rg -F -q '# Coding Standards Legacy Index' "$R/CODING-STANDARDS.md"
! rg -F -q '## Simplicity Principle' "$R/CODING-STANDARDS.md"
mapfile -t rows < <(awk -F '\t' '$1=="STD-0135"||$1=="STD-0136"{print $1}' "$S/consolidation-dispositions.tsv" | sort)
[[ "${rows[*]}" == 'STD-0135 STD-0136' ]]
rg -F -q '`7.4b8bc` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bd` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Core simplicity passed: 12 decisions, 2 exact dispositions, active child 15.2\n'
