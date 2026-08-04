#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/contracts/artifact-selection-decisions.tsv";C="$R/topics/contracts.md";A="$R/ARCHITECTURE-PATTERNS.md"
count=0
while IFS=$'\t' read -r case_id purpose authority consumers placement capability expected extra;do
  [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
  if [[ "$authority" == missing || "$consumers" == unknown ]];then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]];then actual=typed-unsupported
  elif [[ "$purpose" == none || "$purpose" == convenience || "$authority" == duplicated || "$placement" == unrelated-implementation ]];then actual=typed-invalid
  else actual=allow;fi
  [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in '## Contract Artifact Necessity And Authority Placement' 'distinct purpose' 'dedicated package is not required' 'authority is `unavailable`' 'Do not fall back to an inferred mirror';do rg -F -q "$text" "$C";done
if rg -q '^### Packaging Guidance|^### Contract Cost Test' "$A";then printf 'Architecture retains duplicate contract artifact policy\n' >&2;exit 1;fi
expected=(STD-{0055..0057});mapfile -t disposed < <(awk -F '\t' '$1>="STD-0055"&&$1<="STD-0057"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == "${expected[*]}" ]]
printf 'Contract artifact selection passed: %s decisions, 3 exact dispositions\n' "$count"
