#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/frontend/rendering-synchronization-decisions.tsv";D="$R/profiles/applications/frontend.md";L="$R/FRONTEND-STANDARDS.md";M="$R/reference/recipes/frontend.md"
count=0
while IFS=$'\t' read -r case_id scope authority output mechanism source capability lifecycle evidence fallback expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$fallback" != none || "$authority" == contradictory || "$lifecycle" == unsafe ]];then actual=typed-invalid
 elif [[ "$capability" == unsupported ]];then actual=typed-unsupported
 elif [[ "$scope" == selected && ( "$authority" == missing || "$source" == missing || "$mechanism" == missing || "$lifecycle" == missing || "$evidence" == missing ) ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in 'Select rendering from the authoritative state' 'Declarative bindings do not' 'none is a universal preference' 'pull-style FFI or message drain' 'Do not switch between declarative and imperative rendering' '[Frontend mechanism recipes]';do rg -F -q "$text" "$D";done
for text in 'ID: `reference.recipes.frontend`' 'This material is non-normative' '## Illustrative Rendering Mechanisms' '## Illustrative Synchronization Mechanisms' 'Neither mechanism is a default' 'do not select event delivery, polling';do rg -F -q "$text" "$M";done
render="$(awk '/^## Rendering and DOM Updates/{capture=1} /^## UI State Synchronization/{capture=0} capture{print}' "$L")";sync="$(awk '/^## UI State Synchronization/{capture=1} /^### Hook\/Composable Timer Management/{capture=0} capture{print}' "$L")"
for text in '[Rendering And Synchronization]' '[Frontend Mechanism Recipes]' 'Declarative and imperative rendering are selected mechanisms';do [[ "$render" == *"$text"* ]];done
for text in '[Rendering And Synchronization]' 'This index does not prefer event delivery or polling';do [[ "$sync" == *"$text"* ]];done
for text in 'container.innerHTML' 'appendChild' 'setInterval' 'syncLinkedInputsFromDom' 'drain_events()';do [[ "$render$sync" != *"$text"* ]];done
"$S/check-metadata.sh" "$R" "$R/CORE-STANDARDS.md" "$R/workflows/verification.md" "$R/topics/contracts.md" "$R/topics/accessibility.md" "$R/topics/concurrency.md" "$R/profiles/languages/typescript.md" "$R/profiles/languages/typescript/async.md" "$D" "$M"
expected_ids=(STD-{0451..0453});mapfile -t disposed < <(awk -F '\t' '$1>="STD-0451"&&$1<="STD-0453"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == "${expected_ids[*]}" ]]
printf 'Frontend rendering and synchronization passed: %s decisions, 3 exact dispositions\n' "$count"
