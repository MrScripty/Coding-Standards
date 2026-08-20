#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/rust/binding-artifact-selection-decisions.tsv"
readonly PROFILE="$R/profiles/languages/rust/language-bindings.md"
readonly LEGACY="$R/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case_id boundary consumer deployment release_plan artifact crate_type fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$crate_type" == alternate-crate-type ||
        ( "$fallback" == default-artifact ) ]]; then
    actual=typed-invalid
  elif [[ "$boundary" == missing || "$consumer" == missing || "$release_plan" == missing ||
          "$artifact" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || { printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2; exit 1; }
done < "$FIXTURE"

awk -F '\t' 'NR > 1 && ($1 == "STD-0792" || $1 == "STD-0793") { print $2 ":" $3 ":" $4 }' "$DISPOSITIONS" |
  awk 'BEGIN { expected[1]="languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:profiles/languages/rust/language-bindings.md:refine"; expected[2]=expected[1] } { if ($0 != expected[NR]) exit 1 } END { exit NR != 2 }'

for text in 'Select native artifact kind and crate output types' '`cdylib`, `staticlib`, `rlib`' 'accepted boundary' 'Do not prescribe one crate name' 'typed `unavailable`' 'typed `invalid`'; do
  rg -F -q "$text" "$PROFILE"
done
legacy="$(sed -n '/^### cdylib Configuration$/,/^---$/p' "$LEGACY")"
rg -F -q 'language-bindings.md#package-and-workspace-placement' <<< "$legacy"
for removed in 'mylib-uniffi/Cargo.toml' 'crate-type = ["cdylib", "lib"]' 'cdylib produces'; do
  ! rg -F -q "$removed" <<< "$legacy"
done

"$S/verify-rust-binding-workspace-evidence.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Rust binding artifact selection passed: 10 decisions, 2 exact dispositions\n'
