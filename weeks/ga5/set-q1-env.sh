#!/usr/bin/env bash
# Q1 RAG: AI Pipe (gpt-4.1-mini) first, Gemini flash-lite second, OpenAI direct third; then redeploy.
# Keys come from the repo .env (never printed). Run: bash weeks/ga5/set-q1-env.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
set -a; source "$ROOT/.env"; set +a
cd "$ROOT/weeks/ga5/q-rag-colosseum-server/src/tds-ga5-rag"
rmv()  { vercel env rm "$1" production --yes >/dev/null 2>&1 || true; }
setv() { rmv "$1"; printf %s "$2" | vercel env add "$1" production >/dev/null; echo "  set $1"; }
setv LLM_BASE_URL  "https://aipipe.org/openai/v1"; setv LLM_API_KEY  "${AIPIPE_TOKEN:?}"; setv LLM_MODEL  "gpt-4.1-mini"
setv LLM2_BASE_URL "https://generativelanguage.googleapis.com/v1beta/openai"; setv LLM2_API_KEY "${GEMINI_API_KEY_2:?}"; setv LLM2_MODEL "gemini-3.1-flash-lite"
setv LLM3_BASE_URL "https://api.openai.com/v1"; setv LLM3_API_KEY "${OPENAI_API_KEY:?}"; setv LLM3_MODEL "gpt-4.1-mini"
vercel deploy --prod --yes | tail -2
