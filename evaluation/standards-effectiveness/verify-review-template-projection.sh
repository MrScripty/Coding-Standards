#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/implementation/review-template-decisions.tsv";T="$R/templates/PULL_REQUEST_TEMPLATE.md";D="$S/consolidation-dispositions.tsv"
while IFS=$'\t' read -r id summary selection verification conditional copied checklist fallback expected extra;do
  [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];actual=allow
  if [[ "$fallback" != none || "$conditional" != yes || "$copied" != no || "$checklist" != no || "$selection" == all ]];then actual=typed-invalid
  elif [[ "$summary" != yes || "$verification" != yes ]];then actual=typed-unavailable;fi
  [[ "$actual" == "$expected" ]]
done < "$F"
for t in '## Summary' 'observable behavior or standards outcome' '## Selected Evidence' 'Omit categories that are not material' 'Link durable' '## Verification' 'is not acceptance evidence';do rg -F -q "$t" "$T";done
for t in '## Decision Impact' '### Problem' '### Constraints' '### Alternatives' '### Simplicity Review' '### Traceability Links' '## Checklist' '- [ ]' '/media/' '/home/';do ! rg -F -q -- "$t" "$T";done
expected=(STD-{0888..0898});mapfile -t actual < <(awk -F '\t' '$1>="STD-0888"&&$1<="STD-0898"{print $1"\t"$2"\t"$3"\t"$4}' "$D")
for i in {0..10};do [[ "${actual[$i]}" == "${expected[$i]}"$'\ttemplates/PULL_REQUEST_TEMPLATE.md\tworkflows/implementation.md\tindex' ]];done
printf 'Review template projection passed: %s decisions, 11 exact dispositions\n' "$(( $(wc -l < "$F")-1 ))"
