#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$R/reference/recipes/tooling.md"
D="$S/consolidation-dispositions.tsv"
L="$R/TOOLING-STANDARDS.md"

for text in '# Tooling Recipes' 'Role: `reference`' 'Level: `REFERENCE`' \
  'This material is non-normative' '../../workflows/tooling.md' \
  '../../topics/dependencies.md' 'do not define a fallback configuration'; do
  rg -F -q "$text" "$F"
done

for row in \
  $'STD-0656\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tretire' \
  $'STD-0657\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove' \
  $'STD-0658\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove' \
  $'STD-0659\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove' \
  $'STD-0661\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove'; do
  rg -F -q "$row" "$D"
done

rg -F -q '[Tooling recipe](reference/recipes/tooling.md#hook-feedback)' "$L"
rg -F -q '[Tooling recipe](reference/recipes/tooling.md#lefthook-example)' "$L"
rg -F -q '[reference/recipes/tooling.md](reference/recipes/tooling.md)' "$R/README.md"
! rg -F -q '### Recommended Tool: Lefthook' "$L"
! rg -F -q 'npm install lefthook --save-dev' "$L"
! rg -F -q 'curl -sSfL https://get.lh.run | sh' "$L"
! rg -F -q 'See [templates/lefthook.yml]' "$L"
printf 'Tooling reference recipes passed: non-normative examples with 5 exact dispositions\n'
