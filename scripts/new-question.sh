#!/usr/bin/env bash
# Scaffold a question folder from templates/.
#
# Usage:
#   scripts/new-question.sh <section-dir> <question-id> [--deploy] [--marks N]
#
# Examples:
#   scripts/new-question.sh weeks/week-00 q-sort-filter-json --marks 0.5
#   scripts/new-question.sh weeks/week-00 q-vercel-latency --deploy --marks 3
#   scripts/new-question.sh roe q01
#   scripts/new-question.sh projects/p1 r01-api --deploy
#
# Creates <section-dir>/<question-id>/ with README, prompts, approaches, final
# (+ deploy.md and .env.example with --deploy), src/, data/, and appends a
# tracking row to <section-dir>/README.md. Never overwrites an existing folder.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TPL="$ROOT/templates"

usage() { sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }

[[ $# -lt 2 ]] && usage
SECTION="${1%/}"; ID="$2"; shift 2
DEPLOY=no; MARKS="?"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --deploy) DEPLOY=yes; shift ;;
    --marks)  MARKS="${2:?--marks needs a value}"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

DIR="$ROOT/$SECTION/$ID"
if [[ -e "$DIR" ]]; then
  echo "Exists, not touching: $SECTION/$ID" >&2
  exit 1
fi
mkdir -p "$DIR/src" "$DIR/data"
touch "$DIR/src/.gitkeep" "$DIR/data/.gitkeep"

DEPLOY_LINK=""
[[ $DEPLOY == yes ]] && DEPLOY_LINK="- [deploy.md](deploy.md) — commands + guide to deploy / boot / configure"

# Fill {{PLACEHOLDERS}} (perl behaves the same on macOS and Linux)
render() {
  ID="$ID" SECTION="$SECTION" MARKS="$MARKS" DEPLOY="$DEPLOY" DEPLOY_LINK="$DEPLOY_LINK" \
    perl -pe 's/\{\{(ID|SECTION|MARKS|DEPLOY|DEPLOY_LINK)\}\}/$ENV{$1}/g' "$1" > "$2"
}

for f in README.md prompts.md approaches.md final.md; do
  render "$TPL/question/$f" "$DIR/$f"
done

if [[ $DEPLOY == yes ]]; then
  render "$TPL/deploy/deploy.md" "$DIR/deploy.md"
  cp "$TPL/deploy/.env.example" "$DIR/.env.example"
fi

# Section index: create if missing, then add a tracking row
INDEX="$ROOT/$SECTION/README.md"
if [[ ! -f "$INDEX" ]]; then
  {
    echo "# $(basename "$SECTION")"
    echo
    echo "| Question | Marks | Deploy | Status | Answer |"
    echo "|----------|-------|--------|--------|--------|"
  } > "$INDEX"
fi
echo "| [$ID]($ID/) | $MARKS | $DEPLOY | todo | |" >> "$INDEX"

echo "Created $SECTION/$ID (deploy=$DEPLOY, marks=$MARKS)"
