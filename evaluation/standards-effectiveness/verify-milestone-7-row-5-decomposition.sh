#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly OVERLAY="$SCRIPT_DIR/milestone-7-execution-decomposition.tsv"
readonly PACKAGES="$SCRIPT_DIR/milestone-7-accelerated-packages.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-row-5-decomposition.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"

expected_rows=(
  $'5\t1\tSTD-0804\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\tprofiles/languages/rust/language-bindings.md\texists\tpre-slice-review\tfocused'
  $'5\t2\tSTD-0805,STD-0806\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\tprofiles/boundaries/language-bindings.md\texists\tpre-slice-review\tfocused'
  $'5\t3\tSTD-0807,STD-0808\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\ttopics/contracts.md\texists\tpre-slice-review\tfocused'
  $'5\t4\tSTD-0809\tlanguages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md\tprofiles/languages/rust/language-bindings.md\texists\tpre-slice-review\tfocused'
)
mapfile -t actual_rows < <(
  awk -F '\t' '$1 == 5 {
    print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $7 "\t" $8
  }' "$OVERLAY"
)
[[ "${actual_rows[*]}" == "${expected_rows[*]}" ]]

row_count=0
while IFS=$'\t' read -r baseline child ids source owner owner_state activation \
  checkpoint rationale extra; do
  [[ "$baseline" == baseline_order ]] && continue
  [[ "$baseline" -eq 5 ]] || continue
  [[ "$child" -eq $((row_count + 1)) ]]
  [[ -n "$ids" && -n "$rationale" && -z "${extra:-}" ]]
  [[ "$source" == languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md ]]
  [[ -e "$REPO_ROOT/$owner" && "$owner_state" == exists ]]
  [[ "$activation" == pre-slice-review && "$checkpoint" == focused ]]
  ((row_count += 1))
done < "$OVERLAY"
[[ "$row_count" -eq 4 ]]

expected_ids=(STD-{0804..0809})
mapfile -t actual_ids < <(
  awk -F '\t' '$1 == 5 { count = split($3, ids, ","); for (i = 1; i <= count; i += 1) print ids[i] }' \
    "$OVERLAY"
)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

awk -F '\t' '
  NR > 1 && $1 >= "STD-0804" && $1 <= "STD-0808" {
    count += 1
    if ($2 != "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" ||
        ($1 == "STD-0804" &&
         $3 != "profiles/languages/rust/language-bindings.md") ||
        ($1 != "STD-0804" &&
         $1 <= "STD-0806" &&
         $3 != "profiles/boundaries/language-bindings.md") ||
        ($1 >= "STD-0807" &&
         $3 != "topics/contracts.md") ||
        $4 != "refine" || $5 == "" || NF != 5) {
      exit 1
    }
  }
  END { exit count != 5 }
' "$DISPOSITIONS"
awk -F '\t' '
  NR > 1 && $1 == "STD-0809" {
    count++
    if ($2 != "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" ||
        $3 != "profiles/languages/rust/language-bindings.md" ||
        $4 != "refine" || $5 == "" || NF != 5) exit 1
  }
  END { exit count != 1 }
' "$DISPOSITIONS"

package_row="$(
  awk -F '\t' '$1 == 5 { print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $9 }' \
    "$PACKAGES"
)"
[[ "$package_row" == $'5\tP01\trefinement\tprofiles/languages/rust/language-bindings.md\trust-binding-row-decomposition' ]]

required_report=(
  'contains four independently changeable outcomes'
  '### Child 5.1: Rust Core And Adapter Testability'
  '### Child 5.2: Boundary Mechanism Selection'
  '### Child 5.3: Binding Contract Evolution'
  '### Child 5.4: Rust Contract Discovery Adaptation'
  'All children must receive exact dispositions in order'
  'target-count or host-label mechanism defaults'
  'blanket additive compatibility'
  'universal runtime version export'
  'typed diagnostic'
  'changes no normative or legacy standard'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '| F072 | Resolved in Milestone 7.4b8n |' "$FINDINGS"
rg -F -q '`7.4b8n` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8o` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8p` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8q` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8r` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8s` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8t` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8u` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8v` (`Planned`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b8v'* ]]
[[ "$next_slice_line" == *'STD-0298'* ]]
[[ "$next_slice_line" == *'STD-0299'* ]]

"$SCRIPT_DIR/verify-milestone-7-accelerated-execution-replan.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"

printf 'Milestone 7 row-5 decomposition passed: all 6 IDs accepted across 4 ordered children\n'
