# Final — q-vercel-latency

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-vercel-latency](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-vercel-latency)

## How to solve (for a teammate)

> Values are seeded from your email, and your JSON differs, so deploy your own copy.

Needs Node.js (for `npx`) and a free Vercel account.

1. Create an empty folder `latency-app`. Download the telemetry JSON from the question into it and rename it `telemetry.json`.
2. Add `main.py` (copy the code below as-is) and `requirements.txt` with two lines, `fastapi` and `pydantic`. Don't add `vercel.json`.
   <details><summary>main.py (click to expand)</summary>

   ```python
   """POST latency analytics: {"regions": [...], "threshold_ms": N} -> per-region avg/p95 latency, avg uptime, breaches.

   - p95 uses linear interpolation (same as the grader and numpy's default): idx = (n-1)*0.95.
   - breaches = records with latency_ms > threshold (strict).
   - Served at "/" and "/api/latency"; CORS * for POST, with Access-Control-Allow-Origin exposed to JS.
   """
   import json
   import math
   from pathlib import Path
   from typing import List

   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   from pydantic import BaseModel

   app = FastAPI()
   # expose_headers: browsers hide Access-Control-Allow-Origin from cross-origin JS unless it is exposed,
   # and the grader reads it with response.headers.get("access-control-allow-origin").
   app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
                      expose_headers=["Access-Control-Allow-Origin"])

   TELEMETRY = json.loads((Path(__file__).resolve().parent / "telemetry.json").read_text())


   class LatencyRequest(BaseModel):
       regions: List[str]
       threshold_ms: float


   def percentile(values: List[float], q: float) -> float:
       s = sorted(values)
       pos = (len(s) - 1) * q
       lo = math.floor(pos)
       frac = pos - lo
       return s[lo] + frac * (s[lo + 1] - s[lo]) if lo + 1 < len(s) else s[lo]


   def region_stats(region: str, threshold: float) -> dict:
       rows = [r for r in TELEMETRY if r["region"] == region]
       if not rows:
           return {"region": region, "avg_latency": None, "p95_latency": None, "avg_uptime": None, "breaches": 0}
       lat = [r["latency_ms"] for r in rows]
       up = [r["uptime_pct"] for r in rows]
       return {
           "region": region,
           "avg_latency": round(sum(lat) / len(lat), 2),
           "p95_latency": round(percentile(lat, 0.95), 2),
           "avg_uptime": round(sum(up) / len(up), 3),
           "breaches": sum(1 for x in lat if x > threshold),
       }


   @app.post("/")
   @app.post("/api/latency")
   def latency(req: LatencyRequest) -> dict:
       return {"regions": [region_stats(r, req.threshold_ms) for r in req.regions]}


   @app.get("/")
   def health() -> dict:
       return {"status": "ok", "endpoint": "POST / or /api/latency"}
   ```

   </details>

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

## Reproduction steps (needs a clone of this repo)

See [deploy.md](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-vercel-latency/deploy.md): copy the JSON to [`src/telemetry.json`](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-vercel-latency/src/telemetry.json) → local check → `npx vercel --prod` → live check → submit.

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
