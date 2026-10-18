#!/usr/bin/env bash
# Single-source updater for the Google review count across the whole site.
# Usage:  bash tools/update-reviews.sh 1250
# Replaces the current count (from tools/reviews.txt) with the new one,
# in each locale's number format: EN "1,250", CS "1 250", DE "1.250",
# and in the calculator (EN+CZ). Keeps title/meta/visible text in sync.
set -euo pipefail
cd "$(dirname "$0")/.."

NEW="${1:-}"
if ! [[ "$NEW" =~ ^[0-9]{3,}$ ]]; then
  echo "Usage: bash tools/update-reviews.sh <number>   (e.g. 1250)"; exit 1
fi
OLD="$(tr -dc '0-9' < tools/reviews.txt)"
if [[ -z "$OLD" ]]; then echo "tools/reviews.txt is empty"; exit 1; fi
if [[ "$OLD" == "$NEW" ]]; then echo "Count is already $NEW — nothing to do."; exit 0; fi

group(){ local n="$1" s="$2" out=""; while [ ${#n} -gt 3 ]; do out="${s}${n: -3}${out}"; n="${n:0:${#n}-3}"; done; printf '%s%s' "$n" "$out"; }

O_COMMA="$(group "$OLD" ,)"; N_COMMA="$(group "$NEW" ,)"
O_SPACE="$(group "$OLD" ' ')"; N_SPACE="$(group "$NEW" ' ')"
O_DOT="$(group "$OLD" .)";   N_DOT="$(group "$NEW" .)"

repl(){ perl -i -pe "s/\Q$1\E/$2/g" "$3"; }   # \Q..\E = literal match (safe for the dot)

repl "$O_COMMA" "$N_COMMA" index.html
repl "$O_SPACE" "$N_SPACE" cs/index.html
repl "$O_DOT"   "$N_DOT"   de/index.html
repl "$O_COMMA" "$N_COMMA" catering-calculator/index.html
repl "$O_SPACE" "$N_SPACE" catering-calculator/index.html

printf '%s\n' "$NEW" > tools/reviews.txt
echo "Review count: $OLD -> $NEW"
echo "  EN  $O_COMMA -> $N_COMMA"
echo "  CS  $O_SPACE -> $N_SPACE"
echo "  DE  $O_DOT   -> $N_DOT"
echo "Done. Review changes with 'git diff', then commit & push."
