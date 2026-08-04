#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/frontend/typescript-tooling-decisions.tsv";L="$R/FRONTEND-STANDARDS.md";T="$R/profiles/languages/typescript.md";W="$R/workflows/tooling.md";M="$R/reference/recipes/tooling.md"
count=0
while IFS=$'\t' read -r case_id scope project runtime rule purpose compatibility evidence fallback expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$fallback" != none || "$rule" == contradictory ]];then actual=typed-invalid
 elif [[ "$compatibility" == unsupported ]];then actual=typed-unsupported
 elif [[ "$scope" == selected && ( "$project" == missing || "$runtime" == missing || "$rule" == missing || "$purpose" == missing || "$evidence" == missing ) ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in '## Static Analysis And Compiler Configuration' 'Select type-aware lint scope' 'Do not default to an' 'Missing project boundaries';do rg -F -q "$text" "$T";done
for text in '## Lint Policy And Orchestration' 'purpose' 'severity';do rg -F -q "$text" "$W";done
for text in '### Illustrative React Automatic JSX Lint Adapter' 'This snippet does not select React' 'version label cannot replace evidence';do rg -F -q "$text" "$M";done
section="$(awk '/^## Frontend Tooling Notes/{capture=1} /^## Frontend Testing/{capture=0} capture{print}' "$L")"
for text in '[TypeScript profile]' '[Tooling]' '[Tooling Recipes]' 'This index does not select React 19';do [[ "$section" == *"$text"* ]];done
for text in "'react/react-in-jsx-scope': 'off'" "'react/prop-types': 'off'" 'Configure ESLint to avoid outdated rules';do [[ "$section" != *"$text"* ]];done
expected_ids=(STD-0455 STD-0456);mapfile -t disposed < <(awk -F '\t' '$1>="STD-0455"&&$1<="STD-0456"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == "${expected_ids[*]}" ]]
printf 'Frontend TypeScript tooling passed: %s decisions, 2 exact dispositions\n' "$count"
