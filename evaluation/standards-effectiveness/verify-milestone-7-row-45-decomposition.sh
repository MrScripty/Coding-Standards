#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
V="$S/milestone-7-row-45-owner-validation.tsv"
D="$S/milestone-7-row-45-decomposition.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"
M="$S/milestone-7-row-35-readme-consumers.tsv"
A="$S/verify-root-readme-consumer-audit.sh"
ROW35="$S/verify-milestone-7-row-35-decomposition.sh"
TRAIN="$S/milestone-7-execution-train.tsv"

row="$(awk -F '\t' '$1 == 45 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 }' "$TRAIN")"
IFS=$'\t' read -r wave start_id end_id source owner owner_state activation checkpoint <<< "$row"
[[ "$wave" == reference-index-closure ]]
[[ "$start_id" == STD-0704 && "$end_id" == STD-0705 ]]
[[ "$source" == "$(awk -F '\t' '$1 == "STD-0704" { print $2 }' "$S/generated/rule-owner-map.tsv")" ]]
[[ "$source" == "$(awk -F '\t' '$1 == "STD-0705" { print $2 }' "$S/generated/rule-owner-map.tsv")" ]]
[[ "$owner" == STANDARDS-ROUTER.md && "$owner_state" == exists ]]
[[ "$activation" == final-closure && "$checkpoint" == focused ]]
[[ "$(awk -F '\t' '$1 == 45 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 FS $10 }' "$S/milestone-7-accelerated-packages.tsv")" == $'P37\tmechanical\tSTANDARDS-ROUTER.md\tclosure-only\tmigration-structure\tserial-only\tfocused\tlanguage-index-closure\tcore' ]]
[[ "$(awk -F '\t' 'NR > 1 { print $1 FS $2 FS $3 FS $4 }' "$V")" == $'STD-0704\tSTANDARDS-ROUTER.md\tindex\tnone\nSTD-0705\tSTANDARDS-ROUTER.md\tindex\tnone' ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 5 { n++ } END { print n+0 }' "$V")" -eq 0 ]]

for text in '## Owner Review' 'not yet a valid non-normative index' \
  '## Exact Outcomes' '`STD-0704`' '`STD-0705`' \
  '## Consumer Audit Impact' '32 to 33 classified consumers' \
  '## Ordered Child' '`45.1`' 'does not dispose either identifier' \
  '## Bounded Write Set' '## Verification Gates' \
  'complete fail-fast suite' '## Typed Outcomes And No Fallback' \
  '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done

mapfile -t remaining < <(
  awk -F '\t' -v source="$source" '
    NR == FNR { if ($1 != "id") disposed[$1] = 1; next }
    $2 == source && !($1 in disposed) { print $1 }
  ' "$S/consolidation-dispositions.tsv" "$S/generated/rule-owner-map.tsv"
)
[[ "${remaining[*]}" == 'STD-0704 STD-0705' ]]
[[ "$(awk -F '\t' -v source="$source" '$2 == source { n++ } END { print n+0 }' "$S/generated/rule-owner-map.tsv")" -eq 2 ]]

legacy="$R/$source"
for text in '# Language-Specific Standards' '## Languages' \
  'They do not replace Core' 'should not live inline' \
  'legacy [Rust index]'; do
  rg -F -q "$text" "$legacy"
done
for metadata in 'ID: `router`' 'Requires: `core`' \
  'Canonical owner: `STANDARDS-ROUTER.md`'; do
  rg -F -q "$metadata" "$R/STANDARDS-ROUTER.md"
done
rg -F -q '## Language Profiles' "$R/STANDARDS-ROUTER.md"

[[ ! -e "$S/verify-language-index-closure.sh" ]]
[[ "$(awk -F '\t' 'NR > 1 { n++ } END { print n+0 }' "$M")" -eq 32 ]]
! rg -F -q 'verify-language-index-closure.sh' "$M"
rg -F -q '"$(awk -F '\''\t'\'' '\''NR > 1 { n++ } END { print n+0 }'\'' "$M")" -eq 32' "$A"
rg -F -q '"$(awk -F '\''\t'\'' '\''NR > 1 { n++ } END { print n+0 }'\'' "$M")" -eq 32' "$ROW35"

rg -F -q '`7.4b34b` (`Accepted`)' "$P"
rg -F -q '`7.4b35a` (`Accepted`)' "$P"
rg -F -q '`7.4b35b` (`Planned`)' "$P"
"$S/verify-language-profile-routing.sh"
"$S/verify-root-router-evidence.sh"
"$S/verify-root-readme-consumer-audit.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-45 decomposition passed: 2 language-index IDs in one P37 closure child with one bounded README-consumer addition\n'
