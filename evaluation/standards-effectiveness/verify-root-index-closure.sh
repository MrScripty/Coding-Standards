#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
README="$R/README.md"
F="$S/fixtures/router/root-index-resources.tsv"
D="$S/consolidation-dispositions.tsv"

expected_headings=(
  '# Standards Library'
  '## Start Here'
  '## Resources'
  '## License'
)
mapfile -t headings < <(rg '^#{1,6} ' "$README")
[[ "${headings[*]}" == "${expected_headings[*]}" ]]
[[ "$(wc -l < "$README")" -le 32 ]]

count=0
while IFS=$'\t' read -r resource target role extra; do
  [[ "$resource" == resource ]] && continue
  [[ "$role" =~ ^(canonical-foundation|canonical-routing|non-normative-resource|authoritative-license)$ ]]
  [[ -z "${extra:-}" ]]
  [[ -e "$R/$target" ]]
  rg -F -q "($target)" "$README"
  ((count += 1))
done < "$F"
[[ "$count" -eq 6 ]]

for text in 'repository entrypoint' 'does not select modules' \
  'Unknown applicability is a Router diagnostic' \
  'non-normative repository resources' \
  'establish applicability or ownership.' \
  'Repository license terms are in [LICENSE](LICENSE).'; do
  rg -F -q "$text" "$README"
done

for text in '## Documents' '## Templates' '## Customization' \
  '| Document | Purpose | When to Use |' 'Ready-to-use configuration' \
  'Replace placeholders' 'Add tech-specific rules' 'Define your scopes' \
  'Configure tooling' 'provided as-is for free use' 'scheduled for closure'; do
  ! rg -F -q "$text" "$README"
done

expected=(STD-{0001..0006})
mapfile -t disposed < <(
  awk -F '\t' '$1 >= "STD-0001" && $1 <= "STD-0006" { print $1 }' "$D"
)
[[ "${disposed[*]}" == "${expected[*]}" ]]
awk -F '\t' '$1 == "STD-0004" && $2 == "README.md" && $3 == "STANDARDS-ROUTER.md" && $4 == "index" { found = 1 } END { exit !found }' "$D"
awk -F '\t' '$1 == "STD-0005" && $2 == "README.md" && $3 == "STANDARDS-ROUTER.md" && $4 == "index" { found = 1 } END { exit !found }' "$D"
awk -F '\t' '$1 == "STD-0006" && $2 == "README.md" && $3 == "LICENSE" && $4 == "index" { found = 1 } END { exit !found }' "$D"

"$S/verify-root-router-evidence.sh"
"$S/verify-root-readme-consumer-audit.sh"
printf 'Root index closure passed: 6 resources, 6 exact dispositions\n'
