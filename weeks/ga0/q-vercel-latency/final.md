# Final — q-vercel-latency

> Goal: the answer can be reproduced from this file alone.

## Final prompt

```text
Write a FastAPI app (main.py for Vercel's FastAPI preset, CORS * for all methods, and expose_headers=["Access-Control-Allow-Origin"]
so browser JS can read it) that loads telemetry.json
(records: region, latency_ms, uptime_pct) and serves POST / and POST /api/latency taking {"regions": [...],
"threshold_ms": N}. Return {"regions": [{region, avg_latency (mean, 2dp), p95_latency (linear interpolation,
idx=(n-1)*0.95, 2dp), avg_uptime (mean, 3dp), breaches (count latency_ms > N)}]}. Pure Python, no numpy.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

See [deploy.md](deploy.md): copy the JSON to `src/telemetry.json` → local check → `npx vercel --prod` → live check → submit.

## Expected output

```
PASS thr=174 apac … avg_latency 181.12, p95_latency 223.13, avg_uptime 98.163, breaches 8 … ACAO *
PASS thr=174 amer … avg_latency 165.3, p95_latency 214.99, avg_uptime 98.339, breaches 6 … ACAO *
ALL MATCH
```

## Answer submitted (✅ passed, attempt 2)

```
https://tds-ga0-latency.vercel.app/
```
