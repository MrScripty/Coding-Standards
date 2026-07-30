#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/rust/binding-annotation-placement-decisions.tsv"
readonly PROFILE="$R/profiles/languages/rust/language-bindings.md"
readonly LEGACY="$R/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case_id mechanism placement core_contract coupling fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$placement" =~ (proc-macro-default|definition-file-default) ||
        ( "$placement" == core && ( "$core_contract" != unchanged || "$coupling" != absent ) ) ]]; then
    actual=typed-invalid
  elif [[ "$mechanism" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || { printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2; exit 1; }
done < "$FIXTURE"

awk -F '\t' 'NR > 1 && $1 == "STD-0784" { print $2 ":" $3 ":" $4 }' "$DISPOSITIONS" |
  grep -Fx 'languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:profiles/languages/rust/language-bindings.md:refine'

for text in 'Select annotation placement' 'independent of framework behavior' 'separate schema or interface definition' 'Do not prefer co-located proc'; do
  rg -F -q "$text" "$PROFILE"
done
legacy="$(sed -n '/^### Annotation Approach$/,/^### Generation Commands$/p' "$LEGACY")"
rg -F -q 'language-bindings.md#core-and-adapter-boundary' <<< "$legacy"
for removed in 'Prefer proc-macro' '| UniFFI |' '| Tauri Commands |'; do
  ! rg -F -q "$removed" <<< "$legacy"
done

"$S/verify-rust-binding-architecture.sh"
"$S/verify-milestone-7-row-8-decomposition.sh"
printf 'Rust binding annotation placement passed: 9 decisions, 1 exact disposition\n'
