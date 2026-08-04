#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/frontend/applicability-decisions.tsv";D="$R/profiles/applications/frontend.md";L="$R/FRONTEND-STANDARDS.md"
count=0
while IFS=$'\t' read -r case_id ui_change projection interaction state evidence platform facts fallback expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$fallback" != none || "$projection" == contradictory ]];then actual=typed-invalid
 elif [[ "$platform" == unsupported ]];then actual=typed-unsupported
 elif [[ "$ui_change" == yes && ( "$facts" == missing || "$projection" == missing || "$state" == missing ) ]];then actual=typed-unavailable
 elif [[ "$ui_change" == no ]];then actual=not-applicable
 else actual=apply;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in '## Applicability Decision' 'changed responsibility and observable behavior' 'automatically in scope' 'hosted outside a conventional' 'infer scope from Electron, Tauri, WebView';do rg -F -q "$text" "$D";done
section="$(awk '/^# Frontend Standards/{capture=1} /^## Rendering and DOM Updates/{capture=0} capture{print}' "$L")"
for text in '[Frontend application profile]' '[Applicability Decision]' 'This legacy source is a migration index';do [[ "$section" == *"$text"* ]];done
for text in 'These standards apply to browser UIs' 'They complement:' '[CODING-STANDARDS.md]';do [[ "$section" != *"$text"* ]];done
expected_ids=(STD-0449 STD-0450);mapfile -t disposed < <(awk -F '\t' '$1>="STD-0449"&&$1<="STD-0450"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == "${expected_ids[*]}" ]]
printf 'Frontend applicability passed: %s decisions, 2 exact dispositions\n' "$count"
