#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd "$S/../.."&&pwd)"
while IFS=$'\t' read -r c claim authority environment scope fallback expected extra;do
 [[ "$c" == case ]]&&continue;[[ -z "${extra:-}" ]]
 if [[ "$fallback" != none || "$claim" == contradictory ]];then actual=typed-invalid
 elif [[ "$claim" == missing || "$authority" == missing || "$environment" == missing || "$scope" == missing ]];then actual=typed-unavailable
 elif [[ "$environment" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi
 [[ "$actual" == "$expected" ]]
done < "$S/fixtures/verification/quality-gate-decisions.tsv"
for t in '## Quality Gates And Execution Location' 'no catalog' 'Execution location does not create' 'prove only their selected scope' '`invalid`' '`unavailable`' '`unsupported`';do rg -F -q "$t" "$R/workflows/verification.md";done
for id in STD-0688 STD-0695;do awk -F '\t' -v id="$id" '$1==id&&$3=="workflows/verification.md"&&$4=="refine"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv";done
! rg -F -q '| Gate | What it catches | Non-negotiable? |' "$R/TOOLING-STANDARDS.md"
printf 'Verification quality gates passed: 11 decisions, 2 exact dispositions\n'
