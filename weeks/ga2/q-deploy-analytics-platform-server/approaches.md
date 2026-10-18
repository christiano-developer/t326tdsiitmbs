# Approaches — q-deploy-analytics-platform-server

## Problem in one line

Constant-time key compare against an env var, then one pass over events summing positive amounts per user.

## Grader (from quiz JS)

Browser-side: wrong key → 401, missing key → 401, then a random 8–17 event batch (4–6 users, amounts −50…500); numbers compared with `Number(x) !== expected`.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| 401 must be readable | Genuine | CORSMiddleware is outermost so 401s carry CORS headers; otherwise the browser sees a network error, not 401. |
| Negative amounts | Genuine | Exclude ≤ 0 from revenue and from top_user totals. |
| API key | Secret-ish | Kept out of code: read from the `API_KEY` env var (repo root `.env` → `vercel -e`). |

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
