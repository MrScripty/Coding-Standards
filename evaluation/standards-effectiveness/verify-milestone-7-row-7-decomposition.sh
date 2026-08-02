#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly OVERLAY="$SCRIPT_DIR/milestone-7-execution-decomposition.tsv"
readonly PACKAGES="$SCRIPT_DIR/milestone-7-accelerated-packages.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-row-7-decomposition.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"

expected_rows=(
  $'7\t1\tSTD-0761,STD-0762\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\tprofiles/languages/rust/language-bindings.md\texists\tpre-slice-review\tfocused'
  $'7\t2\tSTD-0763,STD-0764,STD-0765,STD-0766\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\tworkflows/release.md\texists\tpre-slice-review\tfocused'
  $'7\t3\tSTD-0767\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\ttopics/contracts.md\texists\tpre-slice-review\tfocused'
  $'7\t4\tSTD-0768,STD-0769,STD-0770,STD-0771\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\tprofiles/boundaries/language-bindings.md\texists\tpre-slice-review\tfocused'
)
mapfile -t actual_rows < <(
  awk -F '\t' '$1 == 7 {
    print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $7 "\t" $8
  }' "$OVERLAY"
)
[[ "${actual_rows[*]}" == "${expected_rows[*]}" ]]

row_count=0
while IFS=$'\t' read -r baseline child ids source owner owner_state activation \
  checkpoint rationale extra; do
  [[ "$baseline" == baseline_order ]] && continue
  [[ "$baseline" -eq 7 ]] || continue
  [[ "$child" -eq $((row_count + 1)) ]]
  [[ -n "$ids" && -n "$rationale" && -z "${extra:-}" ]]
  [[ "$source" == languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md ]]
  [[ -e "$REPO_ROOT/$owner" && "$owner_state" == exists ]]
  [[ "$activation" == pre-slice-review && "$checkpoint" == focused ]]
  ((row_count += 1))
done < "$OVERLAY"
[[ "$row_count" -eq 4 ]]

expected_ids=(STD-{0761..0771})
mapfile -t actual_ids < <(
  awk -F '\t' '$1 == 7 {
    count = split($3, ids, ",")
    for (i = 1; i <= count; i += 1) print ids[i]
  }' "$OVERLAY"
)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

mapfile -t child_dispositions < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0761" && $1 <= "STD-0771" { print $1 }' \
    "$DISPOSITIONS"
)
expected_dispositions=(STD-{0761..0771})
[[ "${child_dispositions[*]}" == "${expected_dispositions[*]}" ]]

package_row="$(
  awk -F '\t' '$1 == 7 {
    print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $9 "\t" $10
  }' "$PACKAGES"
)"
[[ "$package_row" == $'7\tP03\tconsolidation\tprofiles/languages/rust/language-bindings.md\trust-binding-row-decomposition\tcore,workflow.verification,workflow.release,profile.language.rust,profile.boundary.language-bindings,topic.contracts' ]]

required_report=(
  'mixes Rust workspace and verification mechanics, release artifact composition'
  '### Child 7.1: Rust Binding Workspace And Evidence Boundary'
  '### Child 7.2: Binding Artifact Roles And Release Composition'
  '### Child 7.3: Binding Artifact Compatibility'
  '### Child 7.4: Binding Surface Contract'
  'All children must receive exact dispositions in order'
  '`default-members` exclusion as satisfaction'
  'same-build provenance as forced lockstep versioning'
  'automatic export of every technically available operation'
  'typed diagnostics'
  'changes no normative or legacy standard'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '| F074 | Resolved in Milestone 7.4b8w |' "$FINDINGS"
rg -F -q '`7.4b8w` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8x` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8y` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8z` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8aa` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ab` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ac` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b9r'* ]]

"$SCRIPT_DIR/verify-milestone-7-accelerated-execution-replan.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"

printf 'Milestone 7 row-7 decomposition passed: all 11 IDs accepted across 4 ordered children\n'
