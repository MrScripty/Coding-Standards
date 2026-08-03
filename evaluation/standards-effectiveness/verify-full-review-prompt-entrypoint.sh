#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/planning/full-review-prompt-decisions.tsv";P="$R/prompts/full-codebase-standards-refactor.md";D="$S/consolidation-dispositions.tsv"
while IFS=$'\t' read -r case versioned router planning planning_only copied machine fallback expected extra;do
  [[ "$case" == case ]]&&continue;[[ -z "${extra:-}" ]];actual=allow
  if [[ "$fallback" != none ]];then actual=typed-invalid
  elif [[ "$versioned" != yes ]];then actual=typed-invalid
  elif [[ "$router" != yes || "$planning" != yes ]];then actual=typed-unavailable
  elif [[ "$planning_only" != yes || "$copied" != no || "$machine" != no ]];then actual=typed-invalid;fi
  [[ "$actual" == "$expected" ]]
done < "$F"
git -C "$R" ls-files --error-unmatch prompts/full-codebase-standards-refactor.md >/dev/null
for t in 'analysis only' '[`STANDARDS-ROUTER.md`](../STANDARDS-ROUTER.md)' '[`Planning Workflow`](../workflows/planning.md)' 'Preserve the requested' 'evidence that will accept it';do rg -F -q "$t" "$P";done
for t in '1. Route applicable' 'Write `plan.md`' 'docs/plans/<plan-slug>' 'sub-agent' '/media/' '/home/';do ! rg -F -q "$t" "$P";done
[[ "$(rg -c '^#' "$P")" -eq 1 ]]
expected=(STD-{0849..0851});mapfile -t actual < <(awk -F '\t' '$1>="STD-0849"&&$1<="STD-0851"{print $1"\t"$2"\t"$3"\t"$4}' "$D")
for i in 0 1 2;do [[ "${actual[$i]}" == "${expected[$i]}"$'\tprompts/full-codebase-standards-refactor.md\tworkflows/planning.md\tindex' ]];done
printf 'Full-review prompt entrypoint passed: %s decisions, 3 exact dispositions\n' "$(( $(wc -l < "$F")-1 ))"
