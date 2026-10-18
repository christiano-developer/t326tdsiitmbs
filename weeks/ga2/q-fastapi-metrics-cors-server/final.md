# Final — q-fastapi-metrics-cors-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-fastapi-metrics-cors-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-fastapi-metrics-cors-server)

## How to solve (for a teammate)

The assigned values in the code (email, origins, keys, limits, layer values) are **seeded per email** — replace them with yours from the exam page.

**Approach:** Starlette `CORSMiddleware(allow_origins=[ASSIGNED])` + an outer `@app.middleware("http")` that adds `X-Request-ID`/`X-Process-Time`; compute stats from the parsed ints.

1. Make a folder named after the Vercel project you want (e.g. `tds-ga2-stats`) with this layout:
   ```
   tds-ga2-stats/
     app.py              # from api.index import app
     api/__init__.py     # empty
     api/index.py        # the app below
     requirements.txt    # fastapi
   ```
2. `app.py` contains exactly: `from api.index import app  # noqa: F401`
3. `api/index.py`:

<details><summary>api/index.py (click to expand)</summary>

```python
"""CORS-aware descriptive stats API (TDS GA2 q-fastapi-metrics-cors-server).

GET /stats?values=1,2,3 -> {email, count, sum, min, max, mean}
CORS: only ALLOWED_ORIGIN gets Access-Control-Allow-Origin (no wildcard); preflights
from other origins are rejected by Starlette's CORSMiddleware (400, no ACAO).
Every response (incl. preflights and errors) carries X-Request-ID and X-Process-Time.
"""
import time
import uuid

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = "ROLL_NUMBER@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-ufy2p7.example.com"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)


@app.middleware("http")  # registered last -> outermost: wraps CORS responses too
async def request_meta(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


@app.get("/stats")
def stats(values: str = Query("")):
    try:
        nums = [int(v) for v in values.replace(" ", "").split(",") if v != ""]
    except ValueError:
        return JSONResponse({"error": "values must be comma-separated integers"}, status_code=400)
    if not nums:
        return JSONResponse({"error": "no values given"}, status_code=400)
    total = sum(nums)
    return {"email": EMAIL, "count": len(nums), "sum": total, "min": min(nums), "max": max(nums),
            "mean": total / len(nums)}


@app.get("/")
def root():
    return {"ok": True, "endpoint": "/stats?values=1,2,3"}
```

</details>

4. Deploy from inside the folder: `vercel deploy --prod --yes`. **No `vercel.json`** (rewrites make every route 404).
5. Submit the **Aliased** URL from the output (`https://<project>.vercel.app`), press Check, then Save.

Gotchas: `*` fails: the evil-origin preflight must get no ACAO. Register the header middleware *after* CORSMiddleware so it is outermost and also stamps preflight/rejected responses. Starlette returns 400 with no ACAO — that is the required rejection.

## Final prompt

```text
Deploy a CORS-Aware Metrics API (1.5 marks)
<paste the full question text with your assigned values>
Write a FastAPI app for Vercel zero-config deployment (app.py re-exporting `app` from api/index.py,
requirements.txt, no vercel.json). Return JSON errors (never a bare 500). Starlette `CORSMiddleware(allow_origins=[ASSIGNED])` + an outer `@app.middleware("http")` that adds `X-Request-ID`/`X-Process-Time`; compute stats from the parsed ints.
Also give a pytest/TestClient script that replays exactly what the grader checks.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

```bash
cd ~/developer/t326tdsiitmbs && set -a && source .env && set +a
cd weeks/ga2/q-fastapi-metrics-cors-server/src/tds-ga2-stats
vercel deploy --prod --yes
```

Source: [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-fastapi-metrics-cors-server/src/tds-ga2-stats/api/index.py](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-fastapi-metrics-cors-server/src/tds-ga2-stats/api/index.py)

## Expected output

Exam **Check** shows the question as correct.

## Answer submitted

```
https://<your-project>.vercel.app
```
