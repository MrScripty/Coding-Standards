#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
V="$S/milestone-7-row-41-owner-validation.tsv"
D="$S/milestone-7-row-41-decomposition.md"
LEGACY="$R/DOCUMENTATION-STANDARDS.md"

[[ "$(awk -F '\t' '$1 == 41 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 }' "$S/milestone-7-execution-train.tsv")" == $'reference-index-closure\tSTD-0349\tSTD-0349\tDOCUMENTATION-STANDARDS.md\tworkflows/documentation.md\texists\tfinal-closure\tfocused' ]]
[[ "$(awk -F '\t' '$1 == 41 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 FS $10 }' "$S/milestone-7-accelerated-packages.tsv")" == $'P33\tmechanical\tworkflows/documentation.md\tclosure-only\tmigration-structure\tserial-only\tfocused\tdocumentation-index-closure\tcore' ]]
[[ "$(awk -F '\t' 'NR > 1 { print $1 FS $2 FS $3 FS $4 }' "$V")" == $'STD-0349\tworkflows/documentation.md\tindex\tnone' ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 5 { n++ } END { print n+0 }' "$V")" -eq 0 ]]

for text in '## Owner Review' '`STD-0349`' 'independent normative rule' \
  '## Exact Outcome' '`index` disposition' 'retained-diff' \
  '## Ordered Child' '`41.1`' '## Bounded Write Set' \
  '## Verification Gates' 'focused P33' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done

for text in '# Documentation Standards' \
  '[Documentation Workflow](workflows/documentation.md)' \
  '[Documentation Recipe](reference/recipes/documentation.md)' \
  '[Release Workflow](workflows/release.md)' \
  'This index has no independent normative authority'; do
  rg -F -q "$text" "$LEGACY"
done

obsolete_source_assertion='This file is a migration ''index'
if rg -F -q "$obsolete_source_assertion" "$0"; then
  printf 'invalid: row 41 checker owns obsolete Documentation source wording\n' >&2
  exit 1
fi

[[ -e "$R/workflows/documentation.md" ]]
"$S/verify-documentation-decisions.sh"
"$S/verify-documentation-policy-consolidation.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-41 decomposition passed: STD-0349 has one Documentation index-closure child for P33\n'
