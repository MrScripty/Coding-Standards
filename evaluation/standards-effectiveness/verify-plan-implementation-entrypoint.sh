#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/implementation/plan-entrypoint-decisions.tsv";P="$R/prompts/implement-plan.md";D="$S/consolidation-dispositions.tsv"
while IFS=$'\t' read -r id versioned path operation router implementation planning copied fallback expected extra;do
  [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];actual=allow
  if [[ "$fallback" != none || "$versioned" != yes || "$copied" != no ]];then actual=typed-invalid
  elif [[ "$path" != yes || "$operation" == missing || "$router" != yes || "$implementation" != yes || "$planning" != yes ]];then actual=typed-unavailable;fi
  [[ "$actual" == "$expected" ]]
done < "$F"
git -C "$R" ls-files --error-unmatch prompts/implement-plan.md >/dev/null
for t in 'explicitly admitted plan transition' 'repository-relative `plan.md` path' '`start`, `continue`, or `verify`' '[`STANDARDS-ROUTER.md`](../STANDARDS-ROUTER.md)' '[`Implementation Workflow`](../workflows/implementation.md)' '[`Planning Workflow`](../workflows/planning.md)' 'owning typed diagnostic';do rg -F -q "$t" "$P";done
for t in 'Inspect repository status' 'exact write set' 'Concurrent Workers' 'atomic conventional commit' 'active plan' '/media/' '/home/';do ! rg -F -q "$t" "$P";done
[[ "$(rg -c '^#' "$P")" -eq 1 ]]
expected=(STD-{0852..0858});mapfile -t actual < <(awk -F '\t' '$1>="STD-0852"&&$1<="STD-0858"{print $1"\t"$2"\t"$3"\t"$4}' "$D")
for i in {0..6};do [[ "${actual[$i]}" == "${expected[$i]}"$'\tprompts/implement-plan.md\tworkflows/implementation.md\tindex' ]];done
printf 'Plan implementation entrypoint passed: %s decisions, 7 exact dispositions\n' "$(( $(wc -l < "$F")-1 ))"
