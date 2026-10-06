# Approaches — q-vercel-latency

## Problem in one line

Vercel POST endpoint computing per-region mean/p95 latency, mean uptime and threshold breaches from bundled telemetry.

## Grader (from quiz JS)

- Data: `seedrandom(email#q-vercel-latency)` → 3 regions × 12 records (`latency_ms`, `uptime_pct`); the download is that array.
- Request: `{"regions":["apac","amer"],"threshold_ms":174}` POSTed to the submitted URL **as-is**; host must include `vercel.app`.
- Requires HTTP OK and `access-control-allow-origin: *` on the POST response. `regions` may be a list of `{region,…}` or an
  object keyed by region (aliases accepted: `average_latency`, `p95`, `uptime`, `violation_count`).
- Tolerances: avg ±0.5, p95 ±0.5, uptime ±0.2, **breaches exact** (`latency_ms > threshold`, strict).
- **p95 = linear interpolation:** `s[i] + f·(s[i+1]−s[i])`, `i = (n−1)·0.95` (numpy's default).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Page's `vercel.json` with `builds` / `routes` | **Distractor (legacy)** | Vercel's FastAPI preset needs no `vercel.json`; the proven pattern is a root `main.py` exporting `app` (a rewrite broke routing in q-code-interpreter) |
| "You can't read or write files from the file system" | Half-true | Bundled files are **readable** (telemetry.json); only writing is unavailable |
| "p95 (95th percentile)" | Trap | Nearest-rank or other percentile definitions can miss ±0.5; use linear interpolation |
| "breaches (count of records above threshold)" | Detail | Strict `>`; tested with a threshold equal to a data point (230.89) |
| "Enable CORS for POST requests" (grader reads `headers.get("access-control-allow-origin")` in JS) | **Hidden trap** | `Access-Control-Allow-Origin` is **not** a CORS-safelisted response header, so cross-origin JS gets `null` even when CORS passes. Add `Access-Control-Expose-Headers: Access-Control-Allow-Origin` (FastAPI `expose_headers=[...]`). curl can't reveal this; only a real browser can |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | numpy/pandas on Vercel | heavier cold start/bundle for 36 rows |
| B | **Pure-Python FastAPI (stdlib math), JSON bundled, served at `/` and `/api/latency`** | **chosen** |

## Gotchas

- **Verify CORS in a browser, not just curl**, when the grader reads response headers from JS: only safelisted headers
  (Content-Type, Content-Length, Cache-Control, …) are readable unless listed in `Access-Control-Expose-Headers`.
- zsh: never name a shell variable `path` (it's tied to `$PATH`).

## Verification

- `src/test_api.py` computes expected values with the grader's exact JS (node) from `telemetry.json` and compares (tolerances
  and ACAO): grader request + 6 thresholds × 3 regions → **ALL MATCH** locally and live (both paths).
- CORS preflight on the live URL → 200 with `*`.
- **Attempt 1 ❌** "Enable CORS with Access-Control-Allow-Origin: *": header present (curl), but JS read `null`. Reproduced in
  headless Chrome with `src/browser_check.html` (`acao=null`).
- Fix: `expose_headers=["Access-Control-Allow-Origin"]`, redeployed. Real Chrome → `acao="*"` on `/` and `/api/latency`;
  formulas still ALL MATCH.
- Exam "Check": attempt 2 ✅ passed (2026-10-07).
