#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/diagnostics/owner-contract-decisions.tsv";D="$R/topics/diagnostics.md"
count=0
while IFS=$'\t' read -r case_id purpose audience outcome context disclosure capability fallback expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$fallback" != none || "$outcome" == swallowed || "$context" == raw || "$disclosure" == unauthorized ]];then actual=typed-invalid
 elif [[ "$capability" == unsupported ]];then actual=typed-unsupported
 elif [[ "$purpose" == missing || "$audience" == missing ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in 'ID: `topic.diagnostics`' '## Diagnostic Authority' '## Diagnostic Selection' '## Causal Identity And Context' '## Lifecycle And Failure' '## Responsibility Boundaries' '## Typed Outcomes' 'not universal requirements' 'does not mandate a telemetry product';do rg -F -q "$text" "$D";done
for text in 'ID: `reference.recipes.diagnostics`' 'This material is non-normative' '## Adapting A Mechanism';do rg -F -q "$text" "$R/reference/recipes/diagnostics.md";done
rg -F -q '[topics/diagnostics.md](topics/diagnostics.md)' "$R/README.md";rg -F -q '[Diagnostics](topics/diagnostics.md)' "$R/STANDARDS-ROUTER.md";rg -F -q '[Diagnostics](topics/diagnostics.md)' "$R/ARCHITECTURE-PATTERNS.md"
rg -F -q $'STD-0089\tARCHITECTURE-PATTERNS.md\ttopics/diagnostics.md\tindex' "$S/consolidation-dispositions.tsv"
printf 'Diagnostics owner contract passed: %s decisions, 1 disposition\n' "$count"
