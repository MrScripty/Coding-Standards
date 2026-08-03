#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd -- "$S/../.." && pwd)"
OVERLAY="$S/milestone-7-execution-decomposition.tsv"
VALIDATION="$S/milestone-7-row-22-owner-validation.tsv"
REPORT="$S/milestone-7-row-22-decomposition.md"
PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"
mapfile -t ids < <(awk -F '\t' '$1 == 22 {n=split($3,a,","); for(i=1;i<=n;i++) print a[i]}' "$OVERLAY" | sort)
expected=(STD-{0810..0820}); [[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1 == 22 {print $2}' "$OVERLAY" | paste -sd ' ' -)" == '1 2 3 4 5 6 7' ]]
[[ "$(awk -F '\t' '$1 == 22 && NF != 9 {n++} END {print n+0}' "$OVERLAY")" -eq 0 ]]
mapfile -t validated < <(awk -F '\t' 'NR>1 {print $1}' "$VALIDATION")
[[ "${validated[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR>1 && NF!=4 {n++} END {print n+0}' "$VALIDATION")" -eq 0 ]]
[[ "$(awk -F '\t' '$3=="index" {n++} END {print n+0}' "$VALIDATION")" -eq 1 ]]
[[ "$(awk -F '\t' '$3=="split" {n++} END {print n+0}' "$VALIDATION")" -eq 6 ]]
[[ "$(awk -F '\t' '$3=="move" {n++} END {print n+0}' "$VALIDATION")" -eq 4 ]]
for text in '## Owner Contract' 'narrow Rust and Cargo release' 'does not own release boundaries' '## Exact Dispositions' 'Four manifest and configuration examples move' '## Ordered Children' '## Child 22.2 Lockfile Ownership Replan' 'Rust Dependency owns Cargo resolver metadata' 'Rust Release owns only Rust toolchain declaration mechanisms' 'No alias, shared lockfile owner' '## Re-plan Triggers'; do rg -F -q "$text" "$REPORT"; done
rg -F -q '`7.4b12a` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12b` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12c` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12d` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12e` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12f` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12g` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12h` (`Planned`)' "$PLAN"
next="$(awk '/^\*\*Next slice:\*\*/{c=1} c&&/^$/{exit} c{print}' "$PLAN")"
[[ "$next" == *'row 22 child 22.7'* && "$next" == *'STD-0820'* ]]
[[ -e "$R/profiles/languages/rust/release.md" ]]
[[ -e "$R/reference/recipes/rust-release.md" ]]
mapfile -t disposed < <(awk -F '\t' '$1 >= "STD-0810" && $1 <= "STD-0820" {print $1}' "$S/consolidation-dispositions.tsv")
[[ "${disposed[*]}" == 'STD-0810 STD-0811 STD-0812 STD-0813 STD-0814 STD-0815 STD-0816 STD-0817 STD-0818 STD-0819' ]]
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-22 decomposition passed: 11 IDs across 7 children, zero premature dispositions\n'
