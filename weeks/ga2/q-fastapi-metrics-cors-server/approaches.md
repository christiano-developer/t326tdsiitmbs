# Approaches — q-fastapi-metrics-cors-server

## Problem in one line

Starlette `CORSMiddleware(allow_origins=[ASSIGNED])` + an outer `@app.middleware("http")` that adds `X-Request-ID`/`X-Process-Time`; compute stats from the parsed ints.

## Grader (from quiz JS)

Server-side (`/backendVerify`): sends preflights with `Origin` headers itself, so browser CORS does not matter; the exam page cannot fetch the service (expected).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Wildcard CORS | Trap | `*` fails: the evil-origin preflight must get no ACAO. |
| "every response" headers | Genuine | Register the header middleware *after* CORSMiddleware so it is outermost and also stamps preflight/rejected responses. |
| Evil-origin preflight status | Genuine | Starlette returns 400 with no ACAO — that is the required rejection. |

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
