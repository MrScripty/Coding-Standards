#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/release/binding-generation-procedure-decisions.tsv"
readonly WORKFLOW="$R/workflows/release.md"
readonly LEGACY="$R/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case_id plan authority generator toolchain claims outputs evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$authority" == compiled-artifact ]]; then
    actual=typed-invalid
  elif [[ "$plan" == missing || "$authority" == missing || "$generator" == missing ||
          "$toolchain" == missing || "$claims" == missing || "$outputs" == missing ||
          "$evidence" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || { printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2; exit 1; }
done < "$FIXTURE"

awk -F '\t' 'NR > 1 && $1 >= "STD-0785" && $1 <= "STD-0788" { print $2 ":" $3 ":" $4 }' "$DISPOSITIONS" |
  awk 'BEGIN { expected[1]="languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:workflows/release.md:refine"; expected[2]=expected[1]; expected[3]="languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:workflows/release.md:remove"; expected[4]=expected[3] } { if ($0 != expected[NR]) exit 1 } END { exit NR != 4 }'

for text in 'Binding Generation Procedures' 'Contracts-selected generation authority' 'generator capability and version' 'reproducibility controls' 'typed `release-procedure`' 'typed `invalid`'; do
  rg -F -q "$text" "$WORKFLOW"
done
legacy="$(sed -n '/^### Generation Commands$/,/^---$/p' "$LEGACY")"
rg -F -q 'workflows/release.md#binding-generation-procedures' <<< "$legacy"
for removed in 'cargo build -p mylib-uniffi' 'Generate Python bindings' 'Generate C# bindings' 'uniffi_bindgen_main'; do
  ! rg -F -q "$removed" <<< "$legacy"
done

"$S/verify-release-procedure-policy.sh"
"$S/verify-milestone-7-row-8-decomposition.sh"
printf 'Release binding generation procedure passed: 11 decisions, 4 exact dispositions\n'
