# Approaches — q-config-precedence-server

## Problem in one line

Dict merge in precedence order with key normalisation + alias map, then type coercion, then mask `api_key` (same code as GA1, new layer values).

## Grader (from quiz JS)

Browser-side: random 1–2 `set=` overrides for port/workers/debug/log_level (always different from the base), then exact `===` comparison of all five keys including JS type.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| NUM_WORKERS alias | Genuine but unused | This email's `.env` has no NUM_WORKERS; the alias is still implemented. |
| `.env` file | Gotcha | Vercel/git ignore `.env*`, so the dotenv layer ships as `app.env`. |
| OS env layer | Genuine | Set as Vercel env vars at deploy (`-e`), not hardcoded. |

Scanned the question HTML for hidden elements/comments: none found.

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | FastAPI on Vercel (zero-config `app.py` → `api/index.py`), one project per question | chosen |
| B | One shared Vercel project for all GA2 services | rejected: one bad deploy breaks every question |

## Chosen: A

**Why:** same proven layout as GA1; isolated failures; folder name = Vercel project name.

## Verification

- Local: FastAPI `TestClient` tests replaying the grader's checks (all passed).
- Live: exam **Check** passed on 2026-10-18 (header went 3 → 14 / 25 for this batch of seven).
