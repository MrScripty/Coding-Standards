#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/persistence/durable-mutation-decisions.tsv";D="$R/profiles/boundaries/persistence.md";A="$R/ARCHITECTURE-PATTERNS.md"
count=0
while IFS=$'\t' read -r case_id scope invariant source destination capability staging publication proof fallback expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$fallback" != none || "$staging" == authoritative || "$publication" == partial || "$proof" =~ ^(debug-only|incomplete)$ ]];then actual=typed-invalid
 elif [[ "$capability" == unsupported ]];then actual=typed-unsupported
 elif [[ "$scope" == selected && ( "$invariant" == missing || "$source" == missing || "$destination" == missing || "$capability" == missing || "$publication" == unknown || "$proof" == missing ) ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in '## Durable Mutation Contract' 'authoritative precondition' 'isolated staging' 'mandatory five-phase' 'temporarily invalid representation' 'prohibited partial state' 'production path.' 'guessed state';do rg -F -q "$text" "$D";done
for text in '## Illustrative Staged Publication' 'This material is non-normative' 'do not authorize placeholders' 'authoritative publication.';do rg -F -q "$text" "$R/reference/recipes/persistence.md";done
section="$(awk '/^## Phased Mutation Pattern/{capture=1} /^## Schema Versioning and Migration/{capture=0} capture{print}' "$A")"
for text in '[Persistence boundary profile]' '[Persistence Mechanism Recipes]' 'Generic process-local mutation remains outside';do [[ "$section" == *"$text"* ]];done
for text in 'function merge_nodes' '### The Pattern' 'Use placeholder values' 'debug builds' 'append only';do [[ "$section" != *"$text"* ]];done
expected=(STD-{0107..0112});mapfile -t disposed < <(awk -F '\t' '$1>="STD-0107"&&$1<="STD-0112"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == "${expected[*]}" ]]
printf 'Persistence durable mutation passed: %s decisions, 6 exact dispositions\n' "$count"
