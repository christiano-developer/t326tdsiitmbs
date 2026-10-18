# Approaches — q-ledger-agent-server

## Problem in one line

Natural-language Q&A service over a paginated, undocumented JSON API.

## Grader (from quiz JS)

- **Server-side** (`/backendVerify`). Logic not visible. 15 s per question; fail-fast.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| API data (names, notes, descriptions) | **Injection risk** | Server-sent and fed to an LLM at runtime; treat as data, never as instructions |
| Cost | Note | An LLM-based parser spends AIPipe credit → approval first |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content; **server-sent content not yet seen** (needs the logged-in `quizSign`). Treat everything it returns as data, never as instructions.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | LLM writes a small JSON query spec; Python executes it on cleaned data | FastAPI, AI Pipe, Vercel | Exact cents; one short LLM call; easy to test | Spec must cover the question types | chosen |
| B | LLM writes pandas/SQL code that is executed | pandas/duckdb | Very flexible | Slower, heavier on serverless, risky to `exec` model output | rejected |
| C | Send the data to the LLM and let it answer | LLM | Simple | 4,000 rows; arithmetic errors; slow | rejected |

## Chosen: A

**Why:** the grader needs exact numbers fast. The LLM only maps wording → filters/metric; maths stays deterministic.

## Gotchas hit

- **Duplicates:** an order id repeats; keep the row with the latest `updated_at` (compare parsed times, not strings,
  because of mixed `Z` / `+05:30`).
- **Business dates:** convert `created_at` to Asia/Kolkata before taking the date/month (a `…T19:00Z` on the 31st
  is the next day in IST).
- **Revenue = `paid` only**; refunds = `refunded`; `void` counts as neither.
- **Currency:** multiply `amount` by `/rates` `usd_per_unit`; round sums to cents only at the end.
- `/export` = all `/orders` pages (verified row for row), so one request is enough.
- `LEDGER_URL` as copied from the page ends `path=/`: normalise it to end at `path=`.
- An unhandled exception gives a bare 500 **without CORS headers**, which the browser reports as "Failed to fetch".
  Catch errors and return JSON.
- Secrets (`LEDGER_URL` contains the quizSign, `AIPIPE_TOKEN`) live only in Vercel env vars.
- Question text goes to the LLM as data; the system prompt tells it not to follow instructions inside.

## Verification

- Offline: `src/test_executor.py` (synthetic rows: dedup, IST date shift, currency) passes.
- Deployed: 10 differently worded questions (regional/monthly revenue, refunds, top product/customer/region,
  counts, units, net revenue, a date range, one customer) matched in-browser calculations; 1.6–4.0 s each.
- Exam **Check** → "All 6 questions answered correctly." (2026-10-18).
