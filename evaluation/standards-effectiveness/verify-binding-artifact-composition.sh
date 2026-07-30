#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly B="$S/fixtures/release/binding-artifact-composition"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly RELEASE="$R/workflows/release.md"
readonly LEGACY="$R/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

"$S/check-decision-table.sh" "$B-schema.tsv" "$B-decisions.tsv" "$B-observed.tsv"

while IFS=$'\t' read -r case_id contract roles composition identity \
  relationships consumer_info evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ||
        "$roles" == contradictory ||
        "$identity" =~ ^(framework-default|ambiguous)$ ]]; then
    actual=typed-invalid
  elif [[ "$contract" == missing || "$roles" == missing ||
          "$composition" == unknown || "$identity" == missing ||
          "$relationships" == missing || "$consumer_info" == missing ||
          "$evidence" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$B-decisions.tsv"

expected=(STD-0763 STD-0764 STD-0765 STD-0766)
mapfile -t actual < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0763" && $1 <= "STD-0766" {
    print $1
  }' "$DISPOSITIONS"
)
[[ "${actual[*]}" == "${expected[*]}" ]]

for text in \
  '### Binding Artifact Roles And Composition' \
  'internal adapter, wrapper, generator, schema, or build input' \
  'Record which items are release artifacts' \
  'separate or bundled composition' \
  'not the product identity' \
  'compatibility and version relationships remain Contracts-owned' \
  'unresolved artifact-plan diagnostic' \
  'Do not assume one native library per target' \
  'Do not publish an internal build input'; do
  rg -F -q "$text" "$RELEASE"
done

legacy="$(sed -n '/^## Product-Native Artifact Model$/,/^### Compatibility Notes$/p' "$LEGACY")"
rg -F -q 'workflows/release.md#binding-artifact-roles-and-composition' \
  <<< "$legacy"
for removed in \
  'Ship one product-native shared library' \
  'Package generated host-language bindings separately' \
  'pantograph-headless-native-linux-x64.zip' \
  'optional secondary artifacts'; do
  ! rg -F -q "$removed" <<< "$legacy"
done

rg -F -q '`7.4b8y` (`Accepted`)' "$PLAN"
"$S/verify-native-artifact-release.sh"
"$S/verify-milestone-7-row-7-decomposition.sh"
"$S/verify-milestone-7-execution-train.sh"

printf 'Binding artifact composition passed: %s decisions, 4 exact dispositions\n' \
  "$(( $(wc -l < "$B-decisions.tsv") - 1 ))"
