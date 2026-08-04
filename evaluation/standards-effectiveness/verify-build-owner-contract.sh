#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";O="$R/workflows/build.md"
while IFS=$'\t' read -r id authority inputs outputs invalidation environment capability fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$authority" == contradictory ]];then actual=typed-invalid;elif [[ "$authority" == missing || "$inputs" == missing || "$outputs" == missing || "$invalidation" == missing || "$environment" == missing ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/build/owner-contract-decisions.tsv"
for t in 'ID: `workflow.build`' '## Build Authority' '## Inputs, Outputs, And Side Effects' '## Invalidation And Incrementality' '## Environment And External Effects' '## Determinism And Reproducibility' '## Typed Outcomes';do rg -F -q "$t" "$O";done
rg -F -q '[Build](workflows/build.md)' "$R/STANDARDS-ROUTER.md"
rg -F -q '[Build workflow](workflows/build.md)' "$R/CODING-STANDARDS.md"
printf 'Build owner contract passed: 16 decisions, canonical routes\n'
