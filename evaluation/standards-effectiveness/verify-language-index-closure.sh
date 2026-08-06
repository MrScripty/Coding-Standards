#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
D="$S/consolidation-dispositions.tsv"
OWNER_MAP="$S/generated/rule-owner-map.tsv"
INDEX="$R/languages/README.md"

for id in STD-0704 STD-0705; do
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { print $2 FS $3 FS $4 }' "$D")" == $'languages/README.md\tSTANDARDS-ROUTER.md\tindex' ]]
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++ } END { print n+0 }' "$D")" -eq 1 ]]
done

mapfile -t source_ids < <(
  awk -F '\t' '$2 == "languages/README.md" { print $1 }' "$OWNER_MAP"
)
[[ "${source_ids[*]}" == 'STD-0704 STD-0705' ]]
for id in "${source_ids[@]}"; do
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++ } END { print n+0 }' "$D")" -eq 1 ]]
done

expected_headings=('# Language-Specific Standards' '## Available Profiles')
mapfile -t headings < <(rg '^#{1,6} ' "$INDEX")
[[ "${headings[*]}" == "${expected_headings[*]}" ]]
[[ "$(wc -l < "$INDEX")" -le 14 ]]

for text in 'non-normative navigation' \
  '[Language Profiles](../STANDARDS-ROUTER.md#language-profiles)' \
  'not select a profile or establish applicability or ownership' \
  '[Rust profile](../profiles/languages/rust/README.md)' \
  'Unknown applicability is a Router diagnostic' 'fallback authority'; do
  rg -F -q "$text" "$INDEX"
done
for text in '## Languages' 'They do not replace Core' \
  'should not live inline' 'legacy [Rust index]' 'rust/RUST-STANDARDS.md' \
  '| Language | Standards |'; do
  ! rg -F -q "$text" "$INDEX"
done

"$S/verify-root-router-evidence.sh"
"$S/verify-language-profile-routing.sh"
"$S/verify-root-readme-consumer-audit.sh"
"$S/verify-milestone-7-row-45-decomposition.sh"
printf 'Language index closure passed: 2 exact Router dispositions, concise non-normative navigation, P37 closed\n'
