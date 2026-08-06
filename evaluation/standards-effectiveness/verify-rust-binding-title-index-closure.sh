#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
DISPOSITIONS="$S/consolidation-dispositions.tsv"
OWNER_MAP="$S/generated/rule-owner-map.tsv"
LEGACY="$R/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
EXISTING="$S/verify-rust-binding-index-closure.sh"

[[ "$(awk -F '\t' '$1 == "STD-0758" { print $2 FS $3 FS $4 }' "$DISPOSITIONS")" == $'languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\tprofiles/languages/rust/language-bindings.md\tindex' ]]
[[ "$(awk -F '\t' '$1 == "STD-0758" { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 1 ]]

mapfile -t source_ids < <(
  awk -F '\t' '
    $2 == "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" { print $1 }
  ' "$OWNER_MAP"
)
[[ "${#source_ids[@]}" -eq 52 ]]
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
for text in '# Rust Language Bindings Standards' \
  'RUST-INTEROP-STANDARDS.md' 'RUST-CROSS-PLATFORM-STANDARDS.md' \
  'Contract Evolution And Degraded Outcomes'; do
  rg -F -q "$text" <<< "$intro"
done
for prohibited in ' must ' ' always ' ' fallback' ' default framework' \
  ' default runtime' ' default ABI' ' default generator'; do
  ! rg -i -F -q "$prohibited" <<< "$intro"
done

rg -F -q 'STD-0789' "$EXISTING"
! rg -F -q 'STD-0758' "$EXISTING"
"$S/verify-rust-binding-index-closure.sh"
"$S/verify-language-binding-mechanism-selection.sh"
"$S/verify-rust-binding-architecture.sh"
"$S/verify-rust-binding-runtime.sh"
"$S/verify-rust-binding-conversions.sh"
"$S/verify-binding-generation-authority.sh"
"$S/verify-cross-language-contract.sh"
"$S/verify-milestone-7-row-43-decomposition.sh"
printf 'Rust binding title-index closure passed: STD-0758 exact index disposition, 52 source identifiers closed, P35 closed\n'
