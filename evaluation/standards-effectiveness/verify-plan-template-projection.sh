#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/planning/template-projection-decisions.tsv";T="$R/templates/PLAN-TEMPLATE.md";D="$S/consolidation-dispositions.tsv"
while IFS=$'\t' read -r id identity objective acceptance scope decisions milestones replan concurrency final optional fixed copied fallback expected extra;do
  [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];actual=allow
  if [[ "$fallback" != none || "$optional" != no || "$fixed" != no || "$copied" != no ]];then actual=typed-invalid
  elif [[ "$identity" != yes || "$objective" != yes || "$acceptance" != yes || "$scope" != yes || "$decisions" != yes || "$milestones" != yes || "$replan" != yes || "$final" != yes ]];then actual=typed-unavailable;fi
  [[ "$actual" == "$expected" ]]
done < "$F"
for t in '**Plan status:**' '**Current phase:**' '**Next slice:**' '**Acceptance status:**' '**Execution ledger:**' '**Issues:**' '## Objective' '## Objective Acceptance' '## Scope' '## Constraints And Assumptions' '## Binding Decisions' '## Simplicity And Ownership Review' '## Milestones' '**Allowed write set:**' '**Acceptance gate:**' '## Blockers' '## Re-Plan Triggers' '## Concurrent Work' '## Final Acceptance';do rg -F -q "$t" "$T";done
for t in '## Inputs' '## Clarifying Questions' '## Definition of Done' '## Execution Notes' '## Commit Cadence Notes' '## Optional Subagent Assignment' '## Recommendations' '## Completion Summary' '### Milestone 2:' '/media/' '/home/';do ! rg -F -q "$t" "$T";done
expected=(STD-{0859..0887});mapfile -t actual < <(awk -F '\t' '$1>="STD-0859"&&$1<="STD-0887"{print $1"\t"$2"\t"$3"\t"$4}' "$D")
for i in {0..28};do [[ "${actual[$i]}" == "${expected[$i]}"$'\ttemplates/PLAN-TEMPLATE.md\tworkflows/planning.md\tindex' ]];done
printf 'Plan template projection passed: %s decisions, 29 exact dispositions\n' "$(( $(wc -l < "$F")-1 ))"
