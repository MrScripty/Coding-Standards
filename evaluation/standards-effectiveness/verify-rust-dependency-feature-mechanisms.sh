#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/rust/dependency-feature-mechanism-decisions.tsv"
while IFS=$'\t' read -r case_id dependencies consumer resolver target mechanism capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$dependencies" == contradictory ]]; then actual=typed-invalid
  elif [[ "$dependencies" == missing || "$consumer" == unknown || "$resolver" == unknown || "$target" == unknown ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported
  else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$F"
DEPENDENCY="$R/profiles/languages/rust/dependencies.md"
API="$R/profiles/languages/rust/api.md"
LEGACY="$R/languages/rust/RUST-DEPENDENCY-STANDARDS.md"
RECIPE="$R/reference/recipes/rust-dependencies.md"
for text in '## Cargo Manifest Dependency Feature Mechanisms' \
  'dependency `features`' 'target-specific dependency declarations' \
  'public API exposure, and compile-time conflict diagnostics' \
  'Rust API profile.'; do rg -F -q "$text" "$DEPENDENCY"; done
for text in '## Rust Source Feature Expression Mechanisms' \
  'item-level or module-level `cfg`' \
  'Cargo manifest dependency mechanisms belong only' \
  'Dependency profile.'; do rg -F -q "$text" "$API"; done
! rg -F -q 'optional dependency declarations' "$API"
! rg -F -q 'target-specific dependency declarations' "$API"
for text in '## Dependency Feature Examples' 'features = ["full"]' 'optional = true' 'do not select broad or minimal features'; do rg -F -q "$text" "$RECIPE"; done
! rg -F -q 'features = ["full"]' "$LEGACY"
! rg -F -q '#[cfg(feature' "$LEGACY"
mapfile -t actual < <(awk -F '\t' '$1 >= "STD-0738" && $1 <= "STD-0740" {print $1 "\t" $3 "\t" $4}' "$S/consolidation-dispositions.tsv")
expected=($'STD-0738\tprofiles/languages/rust/dependencies.md\tsplit' $'STD-0739\treference/recipes/rust-dependencies.md\tmove' $'STD-0740\treference/recipes/rust-dependencies.md\tmove')
[[ "${actual[*]}" == "${expected[*]}" ]]
printf 'Rust dependency feature mechanisms passed: 15 decisions, 3 exact dispositions\n'
