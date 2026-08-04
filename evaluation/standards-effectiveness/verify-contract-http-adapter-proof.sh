#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/contracts/http-adapter-proof-decisions.tsv";D="$R/topics/contracts.md";A="$R/ARCHITECTURE-PATTERNS.md";H="$R/reference/recipes/http.md"
count=0
while IFS=$'\t' read -r case_id scope direction authority protocol projection response disclosure proof claim fallback expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$fallback" != none || "$response" == contradictory || "$disclosure" == unsafe || "$proof" == incomplete || "$claim" == false ]];then actual=typed-invalid
 elif [[ "$direction" == unsupported || "$protocol" == unsupported || "$projection" == unsupported || "$response" == unsupported ]];then actual=typed-unsupported
 elif [[ "$scope" == selected && ( "$direction" == missing || "$authority" == missing || "$protocol" == missing || "$projection" == missing || "$response" == missing || "$disclosure" == missing || "$proof" == missing ) ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in '## Protocol Adapter Proof' 'producer adapter accepts an already authoritative operation outcome' 'consumer adapter treats the received response as unknown' 'neither status nor body alone proves the outcome' 'application error through successful HTTP transport' 'Adapters do not select disclosure' 'Do not substitute a generic error';do rg -F -q "$text" "$D";done
for text in '## Illustrative Producer Adapter' '## Illustrative Consumer Adapter' '## Selected HTTP Success And Error Representations' 'Neither example is universally good or bad' '## Conditional Interpretation Claims' 'claims, not automatic benefits';do rg -F -q "$text" "$H";done
section="$(awk '/^## HTTP API Error Convention/{capture=1} /^## Choosing Patterns/{capture=0} capture{print}' "$A")"
for text in '[Protocol Outcome Projection]' '[Protocol Adapter Proof]' '[HTTP Projection Mechanism Recipes]' 'This is a migration index';do [[ "$section" == *"$text"* ]];done
for text in '### Server Implementation' '### Client Implementation' '### Anti-Pattern' '### Benefits' 'ApiError:' 'Clients must check' '// BAD:' 'Uniform error handling';do [[ "$section" != *"$text"* ]];done
expected_ids=(STD-{0130..0133});mapfile -t disposed < <(awk -F '\t' '$1>="STD-0130"&&$1<="STD-0133"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == "${expected_ids[*]}" ]]
printf 'Contract HTTP adapter proof passed: %s decisions, 4 exact dispositions\n' "$count"
