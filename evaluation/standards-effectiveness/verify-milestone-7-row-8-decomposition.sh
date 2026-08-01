#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"
readonly PACKAGES="$S/milestone-7-accelerated-packages.tsv"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly REPORT="$S/milestone-7-row-8-decomposition.md"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

expected_rows=(
  $'8\t1\tSTD-0782,STD-0783\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\ttopics/contracts.md\texists\tpre-slice-review\tfocused'
  $'8\t2\tSTD-0784\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\tprofiles/languages/rust/language-bindings.md\texists\tpre-slice-review\tfocused'
  $'8\t3\tSTD-0785,STD-0786,STD-0787,STD-0788\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\tworkflows/release.md\texists\tpre-slice-review\tfocused'
  $'8\t4\tSTD-0789\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\texists\tpre-slice-review\tfocused'
)
mapfile -t actual_rows < <(awk -F '\t' '$1 == 8 { print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $7 "\t" $8 }' "$OVERLAY")
[[ "${actual_rows[*]}" == "${expected_rows[*]}" ]]

expected_ids=(STD-{0782..0789})
mapfile -t actual_ids < <(awk -F '\t' '$1 == 8 { n = split($3, ids, ","); for (i = 1; i <= n; i += 1) print ids[i] }' "$OVERLAY")
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

mapfile -t dispositions < <(awk -F '\t' 'NR > 1 && $1 >= "STD-0782" && $1 <= "STD-0789" { print $1 }' "$DISPOSITIONS")
[[ "${dispositions[*]}" == 'STD-0782 STD-0783 STD-0784 STD-0785 STD-0786 STD-0787 STD-0788 STD-0789' ]]

package_row="$(awk -F '\t' '$1 == 8 { print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $9 "\t" $10 }' "$PACKAGES")"
[[ "$package_row" == $'8\tP04\trefinement\tprofiles/languages/rust/language-bindings.md\trust-binding-generation-and-build-decomposition\tcore,workflow.verification,workflow.release,profile.language.rust,profile.boundary.language-bindings,topic.contracts' ]]

for text in \
  'generation authority, Rust' \
  '## Ordered Children' \
  'Contracts-owned generation authority' \
  'Rust Language Binding-owned annotation placement' \
  'Release-owned build and generation' \
  'legacy-index closure' \
  'hand-maintained bindings' \
  'This planning slice changes only'; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '`7.4b8ab` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ac` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ad` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ae` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b9c'* ]]

"$S/verify-milestone-7-accelerated-execution-replan.sh"
"$S/verify-milestone-7-execution-train.sh"

printf 'Milestone 7 row-8 decomposition passed: all four children accepted; row 8 disposition coverage is complete\n'
