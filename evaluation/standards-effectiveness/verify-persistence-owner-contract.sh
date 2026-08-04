#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/persistence/owner-contract-decisions.tsv";D="$R/profiles/boundaries/persistence.md"
count=0
while IFS=$'\t' read -r case_id scope authority source destination invariant capability version coordination evidence publication state fallback expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$fallback" != none || "$publication" == partial || "$state" =~ ^(contradictory|corrupt)$ || "$evidence" == incomplete ]];then actual=typed-invalid
 elif [[ "$version" == unsupported || "$capability" == unsupported ]];then actual=typed-unsupported
 elif [[ "$scope" == selected && ( "$authority" == missing || "$source" == missing || "$destination" == missing || "$invariant" == missing || "$capability" == missing || "$coordination" == missing || "$evidence" == missing ) ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in 'ID: `profile.boundary.persistence`' '## Durable Boundary Authority' '## Select The Durable Mechanism' '## Responsibility Boundaries' 'does not own every in-memory mutation' '## Typed Outcomes And No Fallback' 'nearby weaker store' '## Verification';do rg -F -q "$text" "$D";done
for text in 'ID: `reference.recipes.persistence`' 'This material is non-normative' '## Adapting A Mechanism' 'examples rather than defaults';do rg -F -q "$text" "$R/reference/recipes/persistence.md";done
"$S/check-metadata.sh" "$R" "$R/CORE-STANDARDS.md" "$R/workflows/verification.md" "$R/topics/contracts.md" "$D" "$R/reference/recipes/persistence.md"
rg -F -q '[profiles/boundaries/persistence.md](profiles/boundaries/persistence.md)' "$R/README.md";rg -F -q '[Persistence boundary profile](profiles/boundaries/persistence.md)' "$R/STANDARDS-ROUTER.md";rg -F -q '[Persistence boundary profile](profiles/boundaries/persistence.md)' "$R/ARCHITECTURE-PATTERNS.md"
rg -F -q $'STD-0106\tARCHITECTURE-PATTERNS.md\tprofiles/boundaries/persistence.md\tindex' "$S/consolidation-dispositions.tsv"
printf 'Persistence owner contract passed: %s decisions, 1 disposition\n' "$count"
