#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
INDEX="$R/languages/rust/RUST-STANDARDS.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"
OWNER_MAP="$S/generated/rule-owner-map.tsv"

source="$(awk -F '\t' '$1 == "STD-0827" { print $2 }' "$OWNER_MAP")"
owner="$(awk -F '\t' '$1 == "STD-0827" { print $4 }' "$OWNER_MAP")"
[[ "$INDEX" == "$R/$source" ]]

expected_outcomes=(index index split split)
offset=0
for id in STD-0827 STD-0828 STD-0829 STD-0830; do
  expected="${expected_outcomes[$offset]}"
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { print $2 FS $3 FS $4 }' "$DISPOSITIONS")" == "$source"$'\t'"$owner"$'\t'"$expected" ]]
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 1 ]]
  offset=$((offset + 1))
done

mapfile -t source_ids < <(
  awk -F '\t' -v source="$source" '$2 == source { print $1 }' "$OWNER_MAP"
)
[[ "${source_ids[*]}" == 'STD-0827 STD-0828 STD-0829 STD-0830' ]]

expected_headings=('# Rust Standards Migration Index' '## Canonical Route')
mapfile -t headings < <(rg '^#{1,6} ' "$INDEX")
[[ "${headings[*]}" == "${expected_headings[*]}" ]]
[[ "$(wc -l < "$INDEX")" -le 16 ]]

for text in 'non-normative migration navigation' \
  'does not establish applicability, precedence, or a default mechanism' \
  '[canonical Rust profile]' 'routing to specialized owners' \
  'typed `unavailable`' 'typed `invalid`' 'typed `unsupported`' \
  'fallback authority'; do
  rg -F -q "$text" "$INDEX"
done
for text in '## Documents' '## Relationship To Generic Standards' \
  '## Default Rust Position' '| Document | Purpose | When to Use |' \
  'Criterion' 'rule wins for Rust crates' 'retain authority' \
  'RUST-API-STANDARDS.md' 'RUST-TOOLING-STANDARDS.md'; do
  ! rg -F -q "$text" "$INDEX"
done

"$S/verify-rust-profile-authority-closure.sh"
"$S/verify-rust-adoption-notes-retirement.sh"
"$S/verify-milestone-7-row-46-decomposition.sh"
printf 'Rust index closure passed: 4 exact dispositions, concise non-normative route, no legacy fallback\n'
