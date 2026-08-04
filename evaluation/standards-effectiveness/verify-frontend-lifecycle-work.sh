#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/frontend/lifecycle-work-decisions.tsv";D="$R/profiles/applications/frontend.md";L="$R/FRONTEND-STANDARDS.md";M="$R/reference/recipes/frontend.md"
count=0
while IFS=$'\t' read -r case_id scope owner identity mechanism start terminal cleanup evidence fallback expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$fallback" != none || "$terminal" =~ ^(duplicate|stale|unobserved)$ || "$cleanup" == incomplete ]];then actual=typed-invalid
 elif [[ "$mechanism" == unsupported ]];then actual=typed-unsupported
 elif [[ "$scope" == selected && ( "$owner" == missing || "$identity" == missing || "$mechanism" == missing || "$cleanup" == missing || "$evidence" == missing ) ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in '## Lifecycle-Owned Frontend Work' 'Concurrency owns generic work lifecycle' 'Select a resource holder and cleanup trigger' 'mechanism, not a default' 'Prevent duplicate active work and stale result application' 'Do not' 'stale-result discard';do rg -F -q "$text" "$D";done
for text in '## Illustrative React Timer Adapter' 'This example does not select React' 'duplicate exclusion' 'stale-result rejection';do rg -F -q "$text" "$M";done
section="$(awk '/^### Hook\/Composable Timer Management/{capture=1} /^## Frontend Tooling Notes/{capture=0} capture{print}' "$L")"
for text in '[Lifecycle-Owned Frontend Work]' '[Concurrency]' '[TypeScript Async profile]' '[Frontend Mechanism Recipes]';do [[ "$section" == *"$text"* ]];done
for text in 'timerRef.current' 'useEffect' 'Store interval/timeout handles' 'Add deterministic cleanup tests';do [[ "$section" != *"$text"* ]];done
mapfile -t disposed < <(awk -F '\t' '$1=="STD-0454"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == STD-0454 ]]
printf 'Frontend lifecycle-owned work passed: %s decisions, 1 exact disposition\n' "$count"
