#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
DISPOSITIONS="$S/consolidation-dispositions.tsv"
OWNER_MAP="$S/generated/rule-owner-map.tsv"
LEGACY="$R/languages/rust/RUST-SECURITY-STANDARDS.md"
EXISTING="$S/verify-security-index-closure.sh"

[[ "$(awk -F '\t' '$1 == "STD-0821" { print $2 FS $3 FS $4 }' "$DISPOSITIONS")" == $'languages/rust/RUST-SECURITY-STANDARDS.md\tprofiles/languages/rust/security.md\tindex' ]]
[[ "$(awk -F '\t' '$1 == "STD-0821" { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 1 ]]

mapfile -t source_ids < <(
  awk -F '\t' '
    $2 == "languages/rust/RUST-SECURITY-STANDARDS.md" { print $1 }
  ' "$OWNER_MAP"
)
[[ "${#source_ids[@]}" -eq 6 ]]
for id in "${source_ids[@]}"; do
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 1 ]]
done

intro="$(
  awk '
    NR == 1 { capture = 1 }
    capture && NR > 1 && /^## / { exit }
    capture { print }
  ' "$LEGACY"
)"
for text in '# Rust Security Standards' \
  'Rust-specific security rules for validation, resource limits, network listeners,' \
  '[Security Standards](../../SECURITY-STANDARDS.md)'; do
  rg -F -q "$text" <<< "$intro"
done
for prohibited in ' must ' ' always ' ' fallback' ' default validator' \
  ' default limit' ' default queue' ' default listener' ' default runtime'; do
  ! rg -i -F -q "$prohibited" <<< "$intro"
done

rg -F -q 'STD-0582' "$EXISTING"
! rg -F -q 'STD-0821' "$EXISTING"
"$S/verify-security-index-closure.sh"
"$S/verify-rust-filesystem-authority.sh"
"$S/verify-rust-boundary-arithmetic.sh"
"$S/verify-rust-external-input-queue.sh"
"$S/verify-rust-listener-lifecycle.sh"
"$S/verify-rust-security-panic-boundary.sh"
"$S/verify-language-profile-routing.sh"
"$S/verify-milestone-7-row-44-decomposition.sh"
printf 'Rust Security title-index closure passed: STD-0821 exact index disposition, 6 source identifiers closed, P36 closed\n'
