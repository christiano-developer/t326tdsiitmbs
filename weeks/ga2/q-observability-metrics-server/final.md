# Final — q-observability-metrics-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-observability-metrics-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-observability-metrics-server)

## How to solve (for a teammate)

The assigned values in the code (email, origins, keys, limits, layer values) are **seeded per email** — replace them with yours from the exam page.

**Approach:** One HTTP middleware increments a counter and appends a JSON log entry (also printed to stdout) to a ring buffer; endpoints read them.

1. Make a folder named after the Vercel project you want (e.g. `tds-ga2-observe`) with this layout:
   ```
   tds-ga2-observe/
     app.py              # from api.index import app
     api/__init__.py     # empty
     api/index.py        # the app below
     requirements.txt    # fastapi
   ```
2. `app.py` contains exactly: `from api.index import app  # noqa: F401`
3. `api/index.py`:

<details><summary>api/index.py (click to expand)</summary>

```python
"""Observability demo: Prometheus counter, health, structured JSON logs (TDS GA2
q-observability-metrics-server).

GET /work?n=K       -> {email, done: K}
GET /metrics        -> Prometheus text; http_requests_total counts every request
GET /healthz        -> {status: ok, uptime_s}
GET /logs/tail?limit=N -> last N JSON log entries {level, ts, path, request_id, ...}
State lives in process memory (one warm serverless instance serves the grader's burst).
"""
import json
import threading
import time
import uuid
from collections import deque
from datetime import datetime, timezone

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

EMAIL = "ROLL_NUMBER@ds.study.iitm.ac.in"
STARTED = time.monotonic()
LOGS = deque(maxlen=1000)
LOCK = threading.Lock()
COUNTS = {"total": 0}

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
                   expose_headers=["X-Request-ID"])


@app.middleware("http")
async def observe(request, call_next):
    rid = request.headers.get("x-request-id") or str(uuid.uuid4())
    with LOCK:
        COUNTS["total"] += 1  # count before handling so /metrics includes itself
    start = time.perf_counter()
    status, level = 500, "error"
    try:
        response = await call_next(request)
        status = response.status_code
        level = "info" if status < 400 else "warning" if status < 500 else "error"
        response.headers["X-Request-ID"] = rid
        return response
    finally:
        entry = {
            "level": level,
            "ts": datetime.now(timezone.utc).isoformat(),
            "path": request.url.path,
            "request_id": rid,
            "method": request.method,
            "status": status,
            "duration_ms": round((time.perf_counter() - start) * 1000, 3),
        }
        with LOCK:
            LOGS.append(entry)
        print(json.dumps(entry), flush=True)  # structured log line to stdout


@app.get("/work")
def work(n: int = Query(1, ge=0, le=100000)):
    acc = 0
    for i in range(n):  # K units of (trivial) work
        acc += i * i
    return {"email": EMAIL, "done": n}


@app.get("/metrics")
def metrics():
    with LOCK:
        total = COUNTS["total"]
    body = (
        "# HELP http_requests_total Total HTTP requests received.\n"
        "# TYPE http_requests_total counter\n"
        f"http_requests_total {total}\n"
    )
    return PlainTextResponse(body, media_type="text/plain; version=0.0.4; charset=utf-8")


@app.get("/healthz")
def healthz():
    return {"status": "ok", "uptime_s": round(time.monotonic() - STARTED, 3)}


@app.get("/logs/tail")
def logs_tail(limit: int = Query(20, ge=1, le=1000)):
    with LOCK:
        return list(LOGS)[-limit:]


@app.get("/")
def root():
    return {"ok": True, "endpoints": ["/work?n=K", "/metrics", "/healthz", "/logs/tail?limit=N"]}
```

</details>

4. Deploy from inside the folder: `vercel deploy --prod --yes`. **No `vercel.json`** (rewrites make every route 404).
5. Submit the **Aliased** URL from the output (`https://<project>.vercel.app`), press Check, then Save.

Gotchas: Counter must be live — increment in middleware. Counter and logs live in process memory; the grader's quick burst hits one warm instance. Retry Check if it ever flips.

## Final prompt

```text
Production Observability: Metrics, Health & Structured Logs (1.5 marks)
<paste the full question text with your assigned values>
Write a FastAPI app for Vercel zero-config deployment (app.py re-exporting `app` from api/index.py,
requirements.txt, no vercel.json). Return JSON errors (never a bare 500). One HTTP middleware increments a counter and appends a JSON log entry (also printed to stdout) to a ring buffer; endpoints read them.
Also give a pytest/TestClient script that replays exactly what the grader checks.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

```bash
cd ~/developer/t326tdsiitmbs && set -a && source .env && set +a
cd weeks/ga2/q-observability-metrics-server/src/tds-ga2-observe
vercel deploy --prod --yes
```

Source: [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-observability-metrics-server/src/tds-ga2-observe/api/index.py](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-observability-metrics-server/src/tds-ga2-observe/api/index.py)

## Expected output

Exam **Check** shows the question as correct.

## Answer submitted

```
https://<your-project>.vercel.app
```
