#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
ADOPTION="$R/languages/rust/RUST-STANDARDS-ADOPTION-NOTES.md"
CORPUS="$S/corpus.tsv"
FROZEN_METRICS="$S/generated/file-metrics.tsv"
LEGACY_INDEX="$R/languages/rust/RUST-STANDARDS.md"
ROUTER="$R/STANDARDS-ROUTER.md"

[[ ! -e "$ADOPTION" ]]
[[ "$(awk -F '\t' '$1 == "languages/rust/RUST-STANDARDS-ADOPTION-NOTES.md" { n++ } END { print n+0 }' "$CORPUS")" -eq 0 ]]
[[ "$(awk -F '\t' '$1 == "languages/rust/RUST-STANDARDS-ADOPTION-NOTES.md" { n++ } END { print n+0 }' "$FROZEN_METRICS")" -eq 1 ]]
[[ "$(awk -F '\t' '$1 == "languages/rust/RUST-STANDARDS-ADOPTION-NOTES.md" { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 FS $10 }' "$FROZEN_METRICS")" == $'reference\tno\treference\tmove\tgit\t77f53cb2ca8807c4a93d717e9206ea8348d3eabbd78f56f4f3367b0678152054\t53\t5\t2' ]]

for active_route in "$LEGACY_INDEX" "$ROUTER"; do
  ! rg -F -q 'RUST-STANDARDS-ADOPTION-NOTES.md' "$active_route"
done

"$S/verify-rust-profile-authority-closure.sh"
"$S/verify-milestone-7-row-46-decomposition.sh"
printf 'Rust adoption notes retirement passed: stale authority and corpus route absent, frozen metrics preserved\n'
