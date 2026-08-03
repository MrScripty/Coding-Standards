#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)"
while IFS=$'\t' read -r id contract verification tooling capability fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$contract" == contradictory ]];then actual=typed-invalid;elif [[ "$contract" == missing || "$verification" == missing || "$tooling" == missing ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/tooling-property-test-decisions.tsv"
for t in '## Property-Test Harness Adapter Mechanisms' 'After Contracts accepts the invariant and domain authority' 'cannot select property testing';do rg -F -q "$t" "$R/profiles/languages/rust/tooling.md";done
for t in '## Property-Test Harness Examples' 'generated graph and edge values' 'do not select proptest';do rg -F -q "$t" "$R/reference/recipes/rust-tooling.md";done
! rg -F -q 'Use property tests for:' "$R/languages/rust/RUST-TOOLING-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0838"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0838\tprofiles/languages/rust/tooling.md\tsplit' ]]
printf 'Rust tooling property-test adapters passed: 16 decisions, 1 exact disposition\n'
