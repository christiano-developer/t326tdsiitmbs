# Approaches — q-api-idempotency-pagination-server

## Problem in one line

Deterministic id = hash(Idempotency-Key); cursor = base64(offset); sliding-window deque per client id in an inner middleware, CORS (with exposed Retry-After) outermost.

## Grader (from quiz JS)

Browser-side: two POSTs with the same key (ids must match), a full scan with limit 6–10 as client `grader-pager`, then up to R+5 GETs as `grader-flood` (needs a 429 whose `Retry-After` is readable), then a fresh client must pass.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Retry-After readable | Genuine | Browser JS can only read it if listed in `Access-Control-Expose-Headers`. |
| Idempotency across instances | Gotcha | Derive the id from `sha256(key)` so a repeat landing on another serverless instance still gets the same id. |
| Back-to-back Checks | Risk | Two Checks within 10 s can exhaust the pager's bucket; wait 10 s and retry. |

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
