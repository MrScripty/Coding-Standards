#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";L="$R/languages/rust/RUST-TOOLING-STANDARDS.md"
while IFS=$'\t' read -r id target consumer feature dependency evidence capability fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$target" == contradictory ]];then actual=typed-invalid;elif [[ "$target" == missing || "$consumer" == missing || "$feature" == missing || "$dependency" == missing || "$evidence" == missing ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/no-std-decisions.tsv"
for t in '## `no_std` Target Capability Contract' 'Select `no_std`, `alloc`, or `std` support only' 'do not substitute a host build';do rg -F -q "$t" "$R/profiles/languages/rust/cross-platform.md";done
for t in '## `no_std` Evidence Adapter Mechanisms' 'After Rust Cross-Platform accepts' 'cannot select default features';do rg -F -q "$t" "$R/profiles/languages/rust/tooling.md";done
for t in '## `no_std` Command Examples' 'cargo check --no-default-features' 'do not select `no_std` support';do rg -F -q "$t" "$R/reference/recipes/rust-tooling.md";done
[[ "$(rg -c '^## ' "$L" || true)" -eq 0 ]];rg -F -q 'non-normative migration index' "$L"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0831"&&$1<="STD-0842"{print $1}' "$S/consolidation-dispositions.tsv");expected=(STD-{0831..0842});[[ "${ids[*]}" == "${expected[*]}" ]]
actual="$(awk -F '\t' '$1=="STD-0842"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0842\tprofiles/languages/rust/cross-platform.md\tsplit' ]]
printf 'Rust no_std closure passed: 16 decisions, 12 exact dispositions, legacy source closed\n'
