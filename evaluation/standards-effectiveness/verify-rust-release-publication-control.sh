#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r id contract unit channel capability evidence fallback expected extra; do
 [[ "$id" == case ]]&&continue; [[ -z "${extra:-}" ]]; if [[ "$fallback" != none || "$contract" == contradictory ]];then actual=typed-invalid;elif [[ "$contract" == missing || "$unit" == unknown || "$channel" == unknown || "$evidence" == incomplete ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi; [[ "$actual" == "$expected" ]]
done < "$S/fixtures/rust/release-publication-control-decisions.tsv"
for t in '## Cargo Publication-Control Mechanisms' 'express the accepted decision' 'does not decide whether a binary';do rg -F -q "$t" "$R/profiles/languages/rust/release.md";done
for t in '## Publication-Control Example' 'publish = false' 'does not make `publish = false` a default';do rg -F -q "$t" "$R/reference/recipes/rust-release.md";done
! rg -F -q 'Use `publish = false` for' "$R/languages/rust/RUST-RELEASE-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0814"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")"; [[ "$actual" == $'STD-0814\tprofiles/languages/rust/release.md\tsplit' ]]
printf 'Rust release publication control passed: 15 decisions, 1 exact disposition\n'
