#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/contracts/semantic-preservation-decisions.tsv";C="$R/topics/contracts.md";A="$R/ARCHITECTURE-PATTERNS.md"
count=0
while IFS=$'\t' read -r case_id authority semantics action destination capability expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$authority" == missing || "$destination" == missing ]];then actual=typed-unavailable
 elif [[ "$capability" == unsupported ]];then actual=typed-unsupported
 elif [[ "$authority" == contradictory || "$action" == infer || "$action" == omit && "$semantics" != none ]];then actual=typed-invalid
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in '## Producer-Consumer Semantic Preservation' 'not only field names' 'new destination representation' 'destination contract authorizes that behavior' 'silently dropped selected meaning' 'Do not fall back to inferred defaults';do rg -F -q "$text" "$C";done
rg -F -q '[Producer-Consumer Semantic Preservation](topics/contracts.md#producer-consumer-semantic-preservation)' "$A"
if rg -q '^### Contract Semantics to Preserve|^### Consumer Responsibilities|Treat the following as part of the contract unless documented otherwise' "$A";then printf 'Architecture retains duplicate semantic-preservation policy\n' >&2;exit 1;fi
expected=(STD-{0058..0062});mapfile -t disposed < <(awk -F '\t' '$1>="STD-0058"&&$1<="STD-0062"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == "${expected[*]}" ]]
printf 'Contract semantic preservation passed: %s decisions, 5 exact dispositions\n' "$count"
