#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/release/build-procedure-decisions.tsv"
while IFS=$'\t' read -r case artifact target mode toolchain procedure evidence fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$artifact" == contradictory ]]; then actual=typed-invalid
  elif [[ "$artifact" == none ]]; then actual=allow
  elif [[ "$artifact" == missing || "$target" == missing || "$mode" == missing ||
          "$toolchain" == missing || "$procedure" == missing || "$evidence" == missing ]]; then
    actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"
for text in '### Build Procedure Selection' 'accepted artifact plan' 'has no build procedure' \
  'Do not invent universal build action names' 'select the exact planned artifact' \
  'compile implicitly through another action' 'report success for an inapplicable'; do
  rg -F -q "$text" "$R/workflows/release.md"
done
rg -F -q '[Release](workflows/release.md#build-procedure-selection)' "$R/LAUNCHER-STANDARDS.md"
! rg -F -q '## Build Standards' "$R/LAUNCHER-STANDARDS.md"
row="$(awk -F '\t' '$1=="STD-0500"{print $1"\t"$2"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")"
[[ "$row" == $'STD-0500\tLAUNCHER-STANDARDS.md\tworkflows/release.md\trefine' ]]
rg -F -q '`7.4b8az` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8ba` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-14-decomposition.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Release build procedure passed: 14 decisions, STD-0500 refined, row 14 complete\n'
