#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/architecture/composition-root-decisions.tsv"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
REFERENCE="$R/reference/patterns/architecture.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case responsibilities contracts lifecycle mechanisms fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$responsibilities" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$responsibilities" == missing || "$contracts" == missing || "$lifecycle" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$mechanisms" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$responsibilities" == one ]]; then
    actual=keep-together
  else
    actual=illustrate
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"

for text in '## Conditional Composition Root' \
  'After Architecture selects independently meaningful implementations' \
  'These labels do not require one composition module' \
  'or owned runtimes may require separate composition boundaries'; do
  rg -F -q "$text" "$REFERENCE"
done
for text in '[Runtime Composition](topics/architecture.md#runtime-composition)' \
  '[Conditional Composition Root](reference/patterns/architecture.md#conditional-composition-root)' \
  'not a required module'; do
  rg -F -q "$text" "$LEGACY"
done

for prohibited in 'Consumers depend on service contracts/facades' \
  'belongs in the composition root' 'swap them in the composition root' \
  'const userRepository = new SqlUserRepository' \
  'Feature module reaches outward and self-wires'; do
  if rg -F -i -q "$prohibited" "$LEGACY" "$REFERENCE"; then
    printf 'fixed composition-root default remains active: %s\n' "$prohibited" >&2
    exit 1
  fi
done

expected=(STD-{0069..0073})
mapfile -t ids < <(
  awk -F '\t' '$1 >= "STD-0069" && $1 <= "STD-0073" { print $1 }' "$DISPOSITIONS"
)
[[ "${ids[*]}" == "${expected[*]}" ]]
while IFS=$'\t' read -r id owner disposition reference_treatment rationale; do
  [[ "$id" == id || "$id" < STD-0069 || "$id" > STD-0073 ]] && continue
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++; row=$3 FS $4 } END { print n+0 FS row }' "$DISPOSITIONS")" == "1	$owner	$disposition" ]]
done < "$S/milestone-7-row-37-owner-validation.tsv"

"$S/verify-architecture-data-authority-pattern.sh"
printf 'Architecture composition-root pattern passed: 9 decisions and 5 exact dispositions\n'
