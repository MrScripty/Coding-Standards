#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/planning/admission-decisions.tsv";P="$R/workflows/planning.md";I="$R/workflows/implementation.md"
while IFS=$'\t' read -r id path operation state revision transition compatibility mechanism fallback expected extra;do
  [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]]
  if [[ "$fallback" != none ]];then actual=typed-invalid
  elif [[ "$path" == missing || "$operation" == missing || "$state" == Blocked || "$revision" == missing || "$transition" == missing || "$compatibility" == dependency-blocked ]];then actual=typed-unavailable
  elif [[ "$path" == escape || "$revision" == stale || "$transition" == malformed || "$compatibility" == overlap || "$compatibility" == contradictory || "$state" == Accepted || ( "$operation" == start && "$state" != Planned ) || ( "$operation" == continue && "$state" != Active ) || ( "$operation" == verify && "$state" != Implemented && "$state" != Verifying ) ]];then actual=typed-invalid
  elif [[ "$mechanism" == unsupported ]];then actual=typed-unsupported
  else actual=allow;fi
  [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s, derived %s\n' "$id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for t in '## Explicit Plan Admission' '`start` accepts only `Planned`' '`continue` accepts only `Active`' '`verify` accepts `Implemented` or `Verifying`' '`planning-admission-v1`' '`planning-transition-v1`' 'exact affected scope and bounded write set' '## Concurrent Preparation And Serial Integration' 'Disjoint files' 'complete-transition' 'restore-prior-state' 'supersede-transition' 'reservations, leases, queues, heartbeats';do rg -F -q "$t" "$P";done
for t in 'explicit canonical' 'Consume the Planning workflow' 'Do not' 'scan for a plan' 'infer an operation';do rg -F -q "$t" "$I";done
printf 'Planning admission passed: %s decisions\n' "$(( $(wc -l < "$F") - 1 ))"
