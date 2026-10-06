# q-vercel-latency

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes (Vercel) |
| Started   | 2026-10-07 |
| Closed    | 2026-10-07 (passed on attempt 2) |

## Question

**Deploy a POST analytics endpoint to Vercel**: background: *Serverless hosting: Vercel* (functions, requirements.txt,
legacy `vercel.json` builds/routes, env vars).

> eShopCo streams latency pings from every storefront. Download the sample telemetry bundle and deploy a Python endpoint
> on Vercel. It must accept POST `{"regions": [...], "threshold_ms": 180}` and return per-region `avg_latency` (mean),
> `p95_latency` (95th percentile), `avg_uptime` (mean) and `breaches` (records above threshold). Enable CORS for POST
> from any origin. We'll send `{"regions":["apac","amer"],"threshold_ms":174}` and verify (order doesn't matter).
> What is the POST endpoint URL?

Per-user variant: 36 records (apac/emea/amer × 12) seeded from the student email.

## Inputs / given data

- [data/q-vercel-latency.json](data/q-vercel-latency.json): downloaded telemetry (bundled as [src/telemetry.json](src/telemetry.json)).

## Final answer

```
https://tds-ga0-latency.vercel.app/
```

(also served at `https://tds-ga0-latency.vercel.app/api/latency`)

Expected for the grader request: apac avg 181.12 · p95 223.13 · uptime 98.163 · breaches 8; amer avg 165.3 · p95 214.99 ·
uptime 98.339 · breaches 6.

## Status notes

- Matches the grader's own JS formulas exactly (grader request + 6 extra thresholds), locally and live.
- Attempt 1 ❌ "Enable CORS…": ACAO wasn't exposed to JS → added `Access-Control-Expose-Headers: Access-Control-Allow-Origin`;
  real-Chrome check now reads `*`. Attempt 2 ✅ **passed**.

## Files

- [prompts.md](prompts.md) · [approaches.md](approaches.md) · [final.md](final.md) · [deploy.md](deploy.md)
- [src/main.py](src/main.py) — FastAPI app · [src/test_api.py](src/test_api.py) — compares an endpoint with the grader's JS formulas
- [src/browser_check.html](src/browser_check.html) — real-browser replica of the grader's fetch + header read
