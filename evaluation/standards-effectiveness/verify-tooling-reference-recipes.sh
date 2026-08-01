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

for text in '## EditorConfig Example' 'only one possible transport' \
  '../../workflows/tooling.md#editor-and-file-configuration' \
  'not recommended defaults'; do
  rg -F -q "$text" "$F"
done
for text in '## Linter Category Examples' 'taxonomy and products are illustrative only' \
  '../../workflows/tooling.md#lint-policy-and-orchestration'; do
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
rg -F -q $'STD-0676\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove' "$D"

for row in \
  $'STD-0667\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tretire' \
  $'STD-0668\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove' \
  $'STD-0669\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove' \
  $'STD-0670\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove' \
  $'STD-0671\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove' \
  $'STD-0672\tTOOLING-STANDARDS.md\treference/recipes/tooling.md\tmove'; do
  rg -F -q "$row" "$D"
done

rg -F -q '[Tooling recipe](reference/recipes/tooling.md#hook-feedback)' "$L"
rg -F -q '[Tooling recipe](reference/recipes/tooling.md#lefthook-example)' "$L"
rg -F -q '[reference/recipes/tooling.md](reference/recipes/tooling.md)' "$R/README.md"
! rg -F -q '### Recommended Tool: Lefthook' "$L"
! rg -F -q 'npm install lefthook --save-dev' "$L"
! rg -F -q 'curl -sSfL https://get.lh.run | sh' "$L"
! rg -F -q 'See [templates/lefthook.yml]' "$L"
! rg -F -q 'See [templates/.editorconfig]' "$L"
! rg -F -q '# Web files typically use 2-space indent' "$L"
! rg -F -q '| Category | Purpose | Examples |' "$L"
printf 'Tooling reference recipes passed: non-normative examples with 12 exact dispositions\n'
