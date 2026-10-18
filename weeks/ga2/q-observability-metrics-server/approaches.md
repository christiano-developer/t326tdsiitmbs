# Approaches — q-observability-metrics-server

## Problem in one line

One HTTP middleware increments a counter and appends a JSON log entry (also printed to stdout) to a ring buffer; endpoints read them.

## Grader (from quiz JS)

Server-side (`/backendVerify`).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Static metrics file | Trap | Counter must be live — increment in middleware. |
| Serverless state | Risk | Counter and logs live in process memory; the grader's quick burst hits one warm instance. Retry Check if it ever flips. |

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
