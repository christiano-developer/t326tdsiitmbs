# Approaches — q-middleware-ratelimit-cors-server

## Problem in one line

Two `@app.middleware("http")` functions (rate limit registered first = innermost, then request context) and `CORSMiddleware` added last (outermost).

## Grader (from quiz JS)

Browser-side from the exam origin, so the exam origin must be allowed and `X-Request-ID` exposed.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "Also allow this exam page's origin" | Genuine | Without it the browser grader cannot read anything. |
| Header readability | Genuine | `expose_headers=["X-Request-ID","Retry-After"]`. |
| Middleware order | Genuine | Outermost → innermost: CORS → request context → rate limit, so 429s still carry CORS + X-Request-ID. |

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
