#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";D="$R/profiles/applications/frontend.md";C="$S/consolidation-dispositions.tsv"
"$S/verify-testing-frontend-evidence.sh"
for text in '## Evidence' 'Select interaction evidence from the user-observable contract' 'A selector or event-dispatch API is not evidence' 'representative browser environment' 'A successful update does not prove cleanup';do rg -F -q "$text" "$D";done
expected=(STD-{0457..0463});mapfile -t disposed < <(awk -F '\t' '$1>="STD-0457"&&$1<="STD-0463"{print $1}' "$C");[[ "${disposed[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1>="STD-0457"&&$1<="STD-0463"&&($3!="profiles/applications/frontend.md"||$4!="index"){n++}END{print n+0}' "$C")" -eq 0 ]]
rg -F -q $'STD-0641\tTESTING-STANDARDS.md\tprofiles/applications/frontend.md\trefine' "$C"
printf 'Frontend testing lineage passed: 7 exact indexes to accepted 15-decision evidence\n'
