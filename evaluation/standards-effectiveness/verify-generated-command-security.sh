#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r case contract validation grammar encoding arguments evidence fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$validation" == failed ]]; then actual=typed-invalid
  elif [[ "$contract" == missing || "$grammar" == missing || "$encoding" == missing ]]; then actual=typed-unavailable
  elif [[ "$encoding" == unsupported ]]; then actual=typed-unsupported
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/security/generated-command-decisions.tsv"
for text in '## Generated Command And Configuration Text' 'exact destination field' \
  'Validation and destination encoding are separate' 'Do not concatenate raw values' \
  'Negative evidence covers spaces' 'Do not emit a partial command'; do
  rg -F -q "$text" "$R/topics/security.md"
done
rg -F -q '[Security](topics/security.md#generated-command-and-configuration-text)' "$R/LAUNCHER-STANDARDS.md"
! rg -F -q 'Raw interpolation' "$R/LAUNCHER-STANDARDS.md"
mapfile -t rows < <(awk -F '\t' '$1>="STD-0508"&&$1<="STD-0510"{print $1}' "$S/consolidation-dispositions.tsv")
[[ "${rows[*]}" == 'STD-0508 STD-0509 STD-0510' ]]
rg -F -q '`7.4b8ba` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bb` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-14-decomposition.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Generated command security passed: 14 decisions, 3 exact dispositions, active row 15\n'
