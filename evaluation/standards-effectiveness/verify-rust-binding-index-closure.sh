#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly LEGACY="$R/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

awk -F '\t' 'NR > 1 && $1 == "STD-0789" { print $2 ":" $3 ":" $4 ":" $5 }' "$DISPOSITIONS" |
  grep -Fx 'languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:index:convert the Build System Organization heading into a non-normative routing index while preserving separately owned child references'

! rg -F -q '^## Build System Organization$' "$LEGACY"
rg -F -q '## Build System Organization Index' "$LEGACY"
for text in 'non-normative migration index' 'Rust Language Binding Profile' 'Binding Generation Procedures' 'separately owned migration references' 'does not add a package'; do
  rg -F -q "$text" "$LEGACY"
done
for heading in '### Feature Flags for Optional Binding Support' '### cdylib Configuration'; do
  rg -F -q "$heading" "$LEGACY"
done
rg -F -q '`7.4b8af` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ag` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'row 25'* ]]

"$S/verify-milestone-7-row-8-decomposition.sh"
printf 'Rust binding legacy-index closure passed: STD-0789 exact index disposition\n'
