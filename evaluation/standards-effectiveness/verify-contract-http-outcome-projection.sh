#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/contracts/http-outcome-projection-decisions.tsv";D="$R/topics/contracts.md";A="$R/ARCHITECTURE-PATTERNS.md";H="$R/reference/recipes/http.md"
count=0
while IFS=$'\t' read -r case_id scope authority outcome protocol projection status body disclosure fallback expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$fallback" != none || "$status" == contradictory || "$body" == contradictory || "$disclosure" == unsafe ]];then actual=typed-invalid
 elif [[ "$outcome" == unsupported || "$protocol" == unsupported || "$projection" == unsupported ]];then actual=typed-unsupported
 elif [[ "$scope" == selected && ( "$authority" == missing || "$outcome" == missing || "$protocol" == missing || "$projection" == missing || "$status" == missing || "$body" == missing || "$disclosure" == missing ) ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in '## Protocol Outcome Projection' 'authoritative operation outcome' 'transport-level success may carry a rejected application outcome' 'Status, headers or equivalent control metadata' 'Security selects what may be disclosed' 'Do not guess a status or envelope' '[HTTP projection recipes]';do rg -F -q "$text" "$D";done
for text in 'ID: `reference.recipes.http`' 'This material is non-normative' '## Illustrative Projection Record' '## Illustrative Response Shapes' 'These values are not defaults' 'default an unknown' 'failure to `500`';do rg -F -q "$text" "$H";done
section="$(awk '/^## HTTP API Error Convention/{capture=1} /^### Server Implementation/{capture=0} capture{print}' "$A")"
for text in '[Protocol Outcome Projection]' '[HTTP Projection Mechanism Recipes]' 'This is a migration index';do [[ "$section" == *"$text"* ]];done
for text in '### The Pattern' '### Error Response Format' '### Status Code Usage' 'Human-readable description' '| 500 |';do [[ "$section" != *"$text"* ]];done
"$S/check-metadata.sh" "$R" "$R/CORE-STANDARDS.md" "$R/workflows/verification.md" "$R/topics/security.md" "$D" "$H"
expected_ids=(STD-{0126..0129});mapfile -t disposed < <(awk -F '\t' '$1>="STD-0126"&&$1<="STD-0129"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == "${expected_ids[*]}" ]]
printf 'Contract HTTP outcome projection passed: %s decisions, 4 exact dispositions\n' "$count"
