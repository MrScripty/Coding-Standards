#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/diagnostics/activity-context-decisions.tsv";D="$R/topics/diagnostics.md";A="$R/ARCHITECTURE-PATTERNS.md"
count=0
while IFS=$'\t' read -r case_id workflow identity parent lifecycle terminal context channel fallback expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$fallback" != none || "$parent" == contradictory || "$terminal" == duplicate || "$context" == raw || "$lifecycle" == synchronous-wrapper ]];then actual=typed-invalid
 elif [[ "$channel" == unsupported ]];then actual=typed-unsupported
 elif [[ "$workflow" == cross-boundary && "$identity" == missing ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in 'An activity context contains only' 'need correlation merely to satisfy a tracing shape' 'including asynchronous completion' 'that context remains valid through another lifecycle';do rg -F -q "$text" "$D";done
for text in '## Illustrative TypeScript Logger Adapter' 'This example is not valid for asynchronous completion' 'must not log raw';do rg -F -q "$text" "$R/reference/recipes/diagnostics.md";done
if rg -q 'Track operations across layers using correlation IDs|interface ActivityContext|logger\.debug\(`Starting' "$A";then printf 'Architecture retains legacy activity mechanism authority\n' >&2;exit 1;fi
expected=(STD-{0090..0092});mapfile -t disposed < <(awk -F '\t' '$1>="STD-0090"&&$1<="STD-0092"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == "${expected[*]}" ]]
printf 'Diagnostics activity context passed: %s decisions, 3 exact dispositions\n' "$count"
