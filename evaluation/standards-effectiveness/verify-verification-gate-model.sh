#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";T="$S/milestone-7-execution-train.tsv";D="$S/milestone-7-execution-decomposition.tsv";P="$S/milestone-7-accelerated-packages.tsv"
[[ "$(awk -F '\t' 'NR>1&&$8!="focused"{n++}END{print n+0}' "$D")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR>1&&$10=="missing-to-exists"&&$7!="owner-review"{n++}END{print n+0}' "$D")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR>1&&$9=="full-suite"{n++}END{print n+0}' "$T")" -eq 5 ]]
[[ "$(awk -F '\t' 'NR>1&&$8=="full-suite"{n++}END{print n+0}' "$P")" -eq 23 ]]
awk -F '\t' 'NR==FNR{if(FNR>1)gate[$1]=$8;next} FNR>1&&$9=="full-suite"&&gate[$1]!="full-suite"{exit 1}' "$P" "$T"
awk -F '\t' 'NR>1&&$5=="create-before-populate"&&$8!="full-suite"{exit 1}' "$P"
printf 'Verification gate model passed: focused children, owner-reviewed creation, 23 package gates, 5 wave checkpoints\n'
