#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/rust/dependency-workspace-inheritance-decisions.tsv"
while IFS=$'\t' read -r case_id ownership consumers resolution support fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$ownership" == contradictory ]]; then actual=typed-invalid
  elif [[ "$ownership" == missing || "$consumers" == unknown || "$resolution" == missing ]]; then actual=typed-unavailable
  elif [[ "$support" == unsupported ]]; then actual=typed-unsupported
  else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$F"
for text in '## Workspace Inheritance Mechanisms' \
  'inheritance coordinates selected manifest facts' \
  'not transfer ownership to the workspace root' 'Member count'; do
  rg -F -q "$text" "$R/profiles/languages/rust/dependencies.md"
done
for text in '## Workspace Inheritance Examples' 'workspace = true' \
  'make member count, root placement'; do
  rg -F -q "$text" "$R/reference/recipes/rust-dependencies.md"
done
! rg -F -q 'two or more workspace members' "$R/languages/rust/RUST-DEPENDENCY-STANDARDS.md"
! rg -F -q 'serde = { workspace = true }' "$R/languages/rust/RUST-DEPENDENCY-STANDARDS.md"
mapfile -t actual < <(awk -F '\t' '$1 >= "STD-0735" && $1 <= "STD-0737" {print $1 "\t" $3 "\t" $4}' "$S/consolidation-dispositions.tsv")
expected=($'STD-0735\tprofiles/languages/rust/dependencies.md\tsplit' $'STD-0736\treference/recipes/rust-dependencies.md\tmove' $'STD-0737\treference/recipes/rust-dependencies.md\tmove')
[[ "${actual[*]}" == "${expected[*]}" ]]
printf 'Rust dependency workspace inheritance passed: 11 decisions, 3 exact dispositions\n'
