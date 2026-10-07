# Final — q-vercel-latency

> Goal: the answer can be reproduced from this file alone.

## How to solve (for a teammate)

> Values are seeded from your email, and your JSON differs, so deploy your own copy.

Needs Node.js (for `npx`) and a free Vercel account.

1. Create an empty folder `latency-app`. Download the telemetry JSON from the question into it and rename it `telemetry.json`.
2. Add `main.py` (copy [src/main.py](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-vercel-latency/src/main.py) as-is) and `requirements.txt` with two lines, `fastapi` and `pydantic`. Don't add `vercel.json`.
3. Deploy: in that folder run `npx vercel login` (once), then `npx vercel --prod --yes`. Copy the URL printed after **Aliased:** (`https://<project>.vercel.app`). Don't use the long unique URL: it returns 401.
4. Test it (should return per-region numbers):
   ```bash
   curl -s -X POST https://<project>.vercel.app/ -H "Content-Type: application/json" -d '{"regions":["apac"],"threshold_ms":180}'
   ```
5. Submit `https://<project>.vercel.app/`, then Check and Save.

`main.py` sets `expose_headers=["Access-Control-Allow-Origin"]`. Without it, the browser grader can't read the CORS header and fails.

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

See [deploy.md](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-vercel-latency/deploy.md): copy the JSON to `src/telemetry.json` → local check → `npx vercel --prod` → live check → submit.

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
