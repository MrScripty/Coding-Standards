#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r id performance tool evidence capability fallback expected extra; do
  [[ "$id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$performance" == contradictory ]]; then actual=typed-invalid
  elif [[ "$performance" == missing || "$tool" == missing || "$evidence" == missing ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/rust/tooling-criterion-decisions.tsv"
for text in '## Criterion Benchmark Adapter Mechanisms' 'After Performance accepts the claim' 'Tooling selects Criterion' 'cannot select Criterion'; do
  rg -F -q "$text" "$R/profiles/languages/rust/tooling.md"
done
for text in '## Criterion Benchmark Examples' 'criterion = { version = "0.5"' 'does not select Criterion'; do
  rg -F -q "$text" "$R/reference/recipes/rust-tooling.md"
done
! rg -F -q 'Criterion is required for Rust performance claims' "$R/languages/rust/RUST-TOOLING-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0834"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")"
[[ "$actual" == $'STD-0834\tprofiles/languages/rust/tooling.md\tsplit' ]]
printf 'Rust tooling Criterion adapter passed: 16 decisions, 1 exact disposition\n'
