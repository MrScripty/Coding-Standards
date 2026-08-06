#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
V="$S/milestone-7-row-44-owner-validation.tsv"
D="$S/milestone-7-row-44-decomposition.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"
LEGACY="$R/languages/rust/RUST-SECURITY-STANDARDS.md"
PROFILE="$R/profiles/languages/rust/security.md"
EXISTING="$S/verify-security-index-closure.sh"

[[ "$(awk -F '\t' '$1 == 44 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 }' "$S/milestone-7-execution-train.tsv")" == $'reference-index-closure\tSTD-0821\tSTD-0821\tlanguages/rust/RUST-SECURITY-STANDARDS.md\tprofiles/languages/rust/security.md\texists\tfinal-closure\tfocused' ]]
[[ "$(awk -F '\t' '$1 == 44 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 FS $10 }' "$S/milestone-7-accelerated-packages.tsv")" == $'P36\tmechanical\tprofiles/languages/rust/security.md\tclosure-only\tmigration-structure\tserial-only\tfocused\trust-security-index-closure\tcore,workflow.verification,topic.security,profile.language.rust' ]]
[[ "$(awk -F '\t' 'NR > 1 { print $1 FS $2 FS $3 FS $4 }' "$V")" == $'STD-0821\tprofiles/languages/rust/security.md\tindex\tnone' ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 5 { n++ } END { print n+0 }' "$V")" -eq 0 ]]

for text in '## Owner Review' 'six frozen identifiers' '## Verifier Ownership' \
  'verify-rust-security-title-index-closure.sh' 'does not dispose `STD-0821`' \
  '## Exact Outcome' '`index` disposition' '## Ordered Child' '`44.1`' \
  '## Bounded Write Set' '## Verification Gates' 'focused package P36' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done

mapfile -t remaining < <(
  awk -F '\t' '
    NR == FNR { if ($1 != "id") disposed[$1] = 1; next }
    $2 == "languages/rust/RUST-SECURITY-STANDARDS.md" &&
      !($1 in disposed) { print $1 }
  ' "$S/consolidation-dispositions.tsv" "$S/generated/rule-owner-map.tsv"
)
[[ "${#remaining[@]}" -eq 0 ]]
[[ "$(awk -F '\t' '$2 == "languages/rust/RUST-SECURITY-STANDARDS.md" { n++ } END { print n+0 }' "$S/generated/rule-owner-map.tsv")" -eq 6 ]]

for text in '# Rust Security Standards' 'Security Standards' \
  'profiles/languages/rust/security.md' 'profiles/languages/rust/async.md' \
  'RUST-API-STANDARDS.md'; do
  rg -F -q "$text" "$LEGACY"
done
for metadata in 'ID: `profile.language.rust.security`' \
  'Requires: `core`, `workflow.verification`, `topic.security`, `profile.language.rust`' \
  'Canonical owner: `profiles/languages/rust/security.md`'; do
  rg -F -q "$metadata" "$PROFILE"
done
[[ -e "$R/CORE-STANDARDS.md" && -e "$R/workflows/verification.md" ]]
[[ -e "$R/topics/security.md" ]]
rg -F -q 'STD-0582' "$EXISTING"
! rg -F -q 'STD-0821' "$EXISTING"
rg -F -q '`7.4b33b` (`Accepted`)' "$P"
rg -F -q '`7.4b34a` (`Accepted`)' "$P"
rg -F -q '`7.4b34b` (`Accepted`)' "$P"
"$S/verify-security-index-closure.sh"
"$S/verify-rust-filesystem-authority.sh"
"$S/verify-rust-boundary-arithmetic.sh"
"$S/verify-rust-external-input-queue.sh"
"$S/verify-rust-listener-lifecycle.sh"
"$S/verify-rust-security-panic-boundary.sh"
"$S/verify-language-profile-routing.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-44 decomposition passed: STD-0821 has one Rust Security title-index closure child for P36\n'
