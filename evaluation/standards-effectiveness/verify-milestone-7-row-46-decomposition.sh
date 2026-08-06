#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
V="$S/milestone-7-row-46-owner-validation.tsv"
D="$S/milestone-7-row-46-decomposition.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"
M="$S/milestone-7-row-35-readme-consumers.tsv"
TRAIN="$S/milestone-7-execution-train.tsv"
CORPUS="$S/corpus.tsv"
FROZEN_METRICS="$S/generated/file-metrics.tsv"

row="$(awk -F '\t' '$1 == 46 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 }' "$TRAIN")"
IFS=$'\t' read -r wave start_id end_id source owner owner_state activation checkpoint <<< "$row"
[[ "$wave" == reference-index-closure ]]
[[ "$start_id" == STD-0827 && "$end_id" == STD-0830 ]]
[[ "$source" == "$(awk -F '\t' '$1 == "STD-0827" { print $2 }' "$S/generated/rule-owner-map.tsv")" ]]
[[ "$owner" == "$(awk -F '\t' '$1 == "STD-0827" { print $4 }' "$S/generated/rule-owner-map.tsv")" ]]
[[ "$owner_state" == exists && "$activation" == final-closure && "$checkpoint" == focused ]]
package="$(awk -F '\t' '$1 == 46 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 FS $10 }' "$S/milestone-7-accelerated-packages.tsv")"
IFS=$'\t' read -r package_id risk package_owner owner_action semantics concurrency gate outcome dependencies <<< "$package"
[[ "$package_id" == P38 && "$risk" == mechanical && "$package_owner" == "$owner" ]]
[[ "$owner_action" == closure-only && "$semantics" == migration-structure ]]
[[ "$concurrency" == serial-only && "$gate" == focused ]]
[[ "$outcome" == rust-index-closure && "$dependencies" == core ]]

[[ "$(awk -F '\t' 'NR > 1 { print $1 FS $3 FS $4 }' "$V")" == $'STD-0827\tindex\tnone\nSTD-0828\tindex\tnone\nSTD-0829\tsplit\tnone\nSTD-0830\tsplit\tnone' ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 5 { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' -v owner="$owner" 'NR > 1 && $2 != owner { n++ } END { print n+0 }' "$V")" -eq 0 ]]

for text in '## Re-plan Finding' 'cannot close as one mechanical index update' \
  '## Owner Contract' '## Exact Outcomes' '`STD-0827`' '`STD-0830`' \
  '## Ordered Children' '`46.1`' '`46.2`' '`46.3`' \
  '## Consumer Audit Impact' '33 to 34' 'only new direct README consumer' \
  '## Bounded Write Sets' '## Verification Gates' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done

mapfile -t remaining < <(
  awk -F '\t' -v source="$source" '
    NR == FNR { if ($1 != "id") disposed[$1] = 1; next }
    $2 == source && !($1 in disposed) { print $1 }
  ' "$S/consolidation-dispositions.tsv" "$S/generated/rule-owner-map.tsv"
)
[[ "${#remaining[@]}" -eq 0 ]]

while IFS=$'\t' read -r id expected_owner expected_outcome _reference _rationale; do
  [[ "$id" == id ]] && continue
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { print $2 FS $3 FS $4 }' "$S/consolidation-dispositions.tsv")" == "$source"$'\t'"$expected_owner"$'\t'"$expected_outcome" ]]
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++ } END { print n+0 }' "$S/consolidation-dispositions.tsv")" -eq 1 ]]
done < "$V"

legacy="$R/$source"
profile="$R/$owner"
for text in '# Rust Standards Migration Index' '## Canonical Route' \
  'non-normative migration navigation' '[canonical Rust profile]' \
  'typed `unavailable`' 'typed `invalid`' 'typed `unsupported`' \
  'fallback authority'; do
  rg -F -q "$text" "$legacy"
done
for text in '## Documents' '## Relationship To Generic Standards' \
  '## Default Rust Position' '| Document | Purpose | When to Use |' \
  'Criterion' 'rule wins for Rust crates' 'retain authority' \
  'RUST-API-STANDARDS.md' 'RUST-TOOLING-STANDARDS.md'; do
  ! rg -F -q "$text" "$legacy"
done
for metadata in 'ID: `profile.language.rust`' 'Requires: `core`' \
  "Canonical owner: \`$owner\`"; do
  rg -F -q "$metadata" "$profile"
done
for text in '## Canonical Routing And No Legacy Authority' \
  'non-normative migration indexes' 'typed `unavailable`' 'typed `invalid`' \
  'typed `unsupported`' 'Do not fall back to a legacy Rust file'; do
  rg -F -q "$text" "$profile"
done
for text in '## Detailed Guidance During Migration' \
  'remain canonical for specialized rules' 'legacy Rust rule conflicts' \
  '../../../languages/rust/'; do
  ! rg -F -q "$text" "$profile"
done

adoption="$R/languages/rust/RUST-STANDARDS-ADOPTION-NOTES.md"
[[ ! -e "$adoption" ]]
[[ "$(awk -F '\t' '$1 == "languages/rust/RUST-STANDARDS-ADOPTION-NOTES.md" { n++ } END { print n+0 }' "$CORPUS")" -eq 0 ]]
[[ "$(awk -F '\t' '$1 == "languages/rust/RUST-STANDARDS-ADOPTION-NOTES.md" { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 FS $10 }' "$FROZEN_METRICS")" == $'reference\tno\treference\tmove\tgit\t77f53cb2ca8807c4a93d717e9206ea8348d3eabbd78f56f4f3367b0678152054\t53\t5\t2' ]]

[[ -x "$S/verify-rust-profile-authority-closure.sh" ]]
[[ -x "$S/verify-rust-adoption-notes-retirement.sh" ]]
[[ -x "$S/verify-rust-index-closure.sh" ]]
[[ "$(awk -F '\t' 'NR > 1 { n++ } END { print n+0 }' "$M")" -eq 34 ]]
[[ "$(awk -F '\t' '$1 == "evaluation/standards-effectiveness/verify-rust-profile-authority-closure.sh" { print $2 FS $3 }' "$M")" == $'none\trust-profile-index' ]]

rg -F -q '`7.4b35b` (`Accepted`)' "$P"
rg -F -q '`7.4b36a` (`Accepted`)' "$P"
rg -F -q '`7.4b36b` (`Accepted`)' "$P"
rg -F -q '`7.4b36c` (`Accepted`)' "$P"
rg -F -q '`7.4b36d` (`Accepted`)' "$P"
"$S/verify-rust-api-owner-contract.sh"
"$S/verify-rust-async-boundary.sh"
"$S/verify-rust-unsafe-contracts.sh"
"$S/verify-rust-tooling-criterion.sh"
"$S/verify-language-profile-routing.sh"
"$S/verify-root-readme-consumer-audit.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-46 closure passed: 4 exact dispositions, P38 closed, row 47 active\n'
