#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
V="$S/milestone-7-row-42-owner-validation.tsv"
D="$S/milestone-7-row-42-decomposition.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"
LEGACY="$R/SECURITY-STANDARDS.md"

[[ "$(awk -F '\t' '$1 == 42 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 }' "$S/milestone-7-execution-train.tsv")" == $'reference-index-closure\tSTD-0582\tSTD-0582\tSECURITY-STANDARDS.md\ttopics/security.md\texists\tfinal-closure\tfocused' ]]
[[ "$(awk -F '\t' '$1 == 42 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 FS $10 }' "$S/milestone-7-accelerated-packages.tsv")" == $'P34\tmechanical\ttopics/security.md\tclosure-only\tmigration-structure\tserial-only\tfocused\tsecurity-index-closure\tcore,workflow.verification' ]]
[[ "$(awk -F '\t' 'NR > 1 { print $1 FS $2 FS $3 FS $4 }' "$V")" == $'STD-0582\ttopics/security.md\tindex\tnone' ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 5 { n++ } END { print n+0 }' "$V")" -eq 0 ]]

for text in '## Owner Review' '`STD-0582`' 'title contributes no independent' \
  '## Exact Outcome' '`index` disposition' '## Ordered Child' '`42.1`' \
  '## Bounded Write Set' '## Verification Gates' 'focused P34' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done

for text in '# Security Standards' \
  'topics/contracts.md#validation-proof-lifetime' \
  'topics/security.md#filesystem-containment' \
  'topics/security.md#input-validation-authority' \
  'profiles/boundaries/ipc.md' \
  'topics/security.md#network-transport-boundary' \
  'topics/concurrency.md#own-work-failure-and-cancellation'; do
  rg -F -q "$text" "$LEGACY"
done

[[ -e "$R/topics/security.md" && -e "$R/workflows/verification.md" ]]
rg -F -q '`7.4b32a` (`Accepted`)' "$P"
rg -F -q '`7.4b32b` (`Blocked`)' "$P"
rg -F -q '`7.4b32br` (`Blocked`)' "$P"
rg -F -q '`7.4b32br1` (`Blocked`)' "$P"
rg -F -q '`7.4b32br2` (`Blocked`)' "$P"
rg -F -q '`7.4b32br3` (`Accepted`)' "$P"
rg -F -q '`7.4b32b2` (`Planned`)' "$P"
"$S/verify-historical-row-checker-ownership.sh"
"$S/verify-errexit-zero-accumulation.sh"
"$S/verify-input-validation-authority.sh"
"$S/verify-filesystem-containment-policy.sh"
"$S/verify-network-transport-policy.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-42 decomposition passed: STD-0582 has one Security index-closure child for P34\n'
