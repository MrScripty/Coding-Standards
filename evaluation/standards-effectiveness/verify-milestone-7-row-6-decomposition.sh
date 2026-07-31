#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly OVERLAY="$SCRIPT_DIR/milestone-7-execution-decomposition.tsv"
readonly PACKAGES="$SCRIPT_DIR/milestone-7-accelerated-packages.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-row-6-decomposition.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"

expected_rows=(
  $'6\t1\tSTD-0294,STD-0295\tCROSS-PLATFORM-STANDARDS.md\ttopics/cross-platform.md\texists\tpre-slice-review\tfocused'
  $'6\t2\tSTD-0296,STD-0297\tCROSS-PLATFORM-STANDARDS.md\tworkflows/release.md\texists\tpre-slice-review\tfocused'
  $'6\t3\tSTD-0298,STD-0299\tCROSS-PLATFORM-STANDARDS.md\tworkflows/verification.md\texists\tpre-slice-review\tfocused'
)
mapfile -t actual_rows < <(
  awk -F '\t' '$1 == 6 {
    print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $7 "\t" $8
  }' "$OVERLAY"
)
[[ "${actual_rows[*]}" == "${expected_rows[*]}" ]]

row_count=0
while IFS=$'\t' read -r baseline child ids source owner owner_state activation \
  checkpoint rationale extra; do
  [[ "$baseline" == baseline_order ]] && continue
  [[ "$baseline" -eq 6 ]] || continue
  [[ "$child" -eq $((row_count + 1)) ]]
  [[ -n "$ids" && -n "$rationale" && -z "${extra:-}" ]]
  [[ "$source" == CROSS-PLATFORM-STANDARDS.md ]]
  [[ -e "$REPO_ROOT/$owner" && "$owner_state" == exists ]]
  [[ "$activation" == pre-slice-review && "$checkpoint" == focused ]]
  ((row_count += 1))
done < "$OVERLAY"
[[ "$row_count" -eq 3 ]]

expected_ids=(STD-{0294..0299})
mapfile -t actual_ids < <(
  awk -F '\t' '$1 == 6 {
    count = split($3, ids, ",")
    for (i = 1; i <= count; i += 1) print ids[i]
  }' "$OVERLAY"
)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

expected_disposition_ids=(STD-{0294..0299})
mapfile -t actual_disposition_ids < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0294" && $1 <= "STD-0299" { print $1 }' \
    "$DISPOSITIONS"
)
[[ "${actual_disposition_ids[*]}" == "${expected_disposition_ids[*]}" ]]

package_row="$(
  awk -F '\t' '$1 == 6 { print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $9 }' \
    "$PACKAGES"
)"
[[ "$package_row" == $'6\tP02\tsafety-critical\ttopics/cross-platform.md\tcross-platform-row-decomposition' ]]

required_report=(
  'native artifact loading, release artifact presentation, and verification'
  '### Child 6.1: Native Artifact Loading'
  '### Child 6.2: Native Artifact Identity And Installation'
  '### Child 6.3: Platform Evidence Scheduling'
  'All children must receive exact dispositions in order'
  'Strategy as a mandatory native-loading abstraction'
  'guessed prefixes, extensions, platform names, or artifact identities'
  'fixed Linux/Windows target set'
  'alternate loader, artifact, target, or weaker evidence'
  'typed diagnostics'
  'changes no normative or legacy standard'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '| F073 | Resolved in Milestone 7.4b8s |' "$FINDINGS"
rg -F -q '`7.4b8s` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8t` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8u` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8v` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8w` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8x` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8y` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8z` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b8bf'* ]]

"$SCRIPT_DIR/verify-milestone-7-accelerated-execution-replan.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"

printf 'Milestone 7 row-6 decomposition passed: all 6 IDs accepted across 3 ordered children\n'
