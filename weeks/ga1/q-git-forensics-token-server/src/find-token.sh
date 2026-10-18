#!/usr/bin/env bash
# Rebuild the repo from history.fastimport and print the leaked token + the commit that introduced it.
# Usage: bash find-token.sh path/to/history.fastimport
set -euo pipefail
src="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
work="$(mktemp -d)"; cd "$work"
git init -q && git fast-import --quiet < "$src" && git checkout -q -f main

echo "commits that add or remove an stg_ string (oldest first):"
git log -S stg_ --reverse --format='  %h %s'

first="$(git log -S stg_ --reverse --format=%H | head -n1)"
token="$(git show "$first" | grep -o '^+.*stg_[A-Za-z0-9_-]*' | grep -o 'stg_[A-Za-z0-9_-]*' | head -n1)"
subject="$(git log -1 --format=%s "$first")"
printf '{"token": "%s", "commit_subject": "%s"}\n' "$token" "$subject"
