#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
V="$S/milestone-7-row-43-owner-validation.tsv"
D="$S/milestone-7-row-43-decomposition.md"
LEGACY="$R/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
PROFILE="$R/profiles/languages/rust/language-bindings.md"
EXISTING="$S/verify-rust-binding-index-closure.sh"

[[ "$(awk -F '\t' '$1 == 43 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 }' "$S/milestone-7-execution-train.tsv")" == $'reference-index-closure\tSTD-0758\tSTD-0758\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\tprofiles/languages/rust/language-bindings.md\texists\tfinal-closure\tfocused' ]]
[[ "$(awk -F '\t' '$1 == 43 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 FS $10 }' "$S/milestone-7-accelerated-packages.tsv")" == $'P35\tmechanical\tprofiles/languages/rust/language-bindings.md\tclosure-only\tmigration-structure\tserial-only\tfocused\trust-binding-index-closure\tcore,workflow.verification,profile.language.rust,profile.boundary.language-bindings' ]]
[[ "$(awk -F '\t' 'NR > 1 { print $1 FS $2 FS $3 FS $4 }' "$V")" == $'STD-0758\tprofiles/languages/rust/language-bindings.md\tindex\tnone' ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 5 { n++ } END { print n+0 }' "$V")" -eq 0 ]]

for text in '## Owner Review' '52 frozen identifiers' '## Verifier Ownership' \
  'verify-rust-binding-title-index-closure.sh' 'does not dispose `STD-0758`' \
  '## Exact Outcome' '`index` disposition' '## Ordered Child' '`43.1`' \
  '## Bounded Write Set' '## Verification Gates' 'focused package P35' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done

mapfile -t remaining < <(
  awk -F '\t' '
    NR == FNR { if ($1 != "id") disposed[$1] = 1; next }
    $2 == "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" &&
      !($1 in disposed) { print $1 }
  ' "$S/consolidation-dispositions.tsv" "$S/generated/rule-owner-map.tsv"
)
[[ "${#remaining[@]}" -eq 0 ]]
[[ "$(awk -F '\t' '$2 == "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" { n++ } END { print n+0 }' "$S/generated/rule-owner-map.tsv")" -eq 52 ]]

for text in '# Rust Language Bindings Standards' \
  'RUST-INTEROP-STANDARDS.md' 'RUST-CROSS-PLATFORM-STANDARDS.md' \
  'Contract Evolution And Degraded Outcomes' \
  'profiles/languages/rust/language-bindings.md'; do
  rg -F -q "$text" "$LEGACY"
done

for metadata in 'ID: `profile.language.rust.language-bindings`' \
  'Requires: `core`, `workflow.verification`, `profile.language.rust`, `profile.boundary.language-bindings`' \
  'Canonical owner: `profiles/languages/rust/language-bindings.md`'; do
  rg -F -q "$metadata" "$PROFILE"
done
[[ -e "$R/CORE-STANDARDS.md" && -e "$R/workflows/verification.md" ]]
[[ -e "$R/profiles/boundaries/language-bindings.md" ]]

rg -F -q 'STD-0789' "$EXISTING"
! rg -F -q 'STD-0758' "$EXISTING"
"$S/verify-rust-binding-index-closure.sh"
"$S/verify-rust-binding-architecture.sh"
"$S/verify-language-profile-routing.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-43 decomposition passed: STD-0758 has one title-index closure child for P35\n'
