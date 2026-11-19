#!/usr/bin/env bash
# Download every captured Q4 batch from the deployed router into data/batches/ (git-ignored data, no secrets).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
set -a; source "$ROOT/.env"; set +a
B="${1:?usage: pull-q4-cases.sh https://<your-project>.vercel.app}"
OUT="$ROOT/weeks/ga5/q-harness-safety-router-server/data/batches"; mkdir -p "$OUT"
H="x-capture-token: ${GA3_CAPTURE_TOKEN:?}"
for id in $(curl -sf -H "$H" "$B/_capture" | python3 -c 'import sys,json;print(" ".join(json.load(sys.stdin)["batches"] or []))'); do
  curl -sf -H "$H" "$B/_capture/$id" -o "$OUT/$id.json" && echo "saved $id ($(wc -c <"$OUT/$id.json") bytes)"
done
ls "$OUT" | wc -l
