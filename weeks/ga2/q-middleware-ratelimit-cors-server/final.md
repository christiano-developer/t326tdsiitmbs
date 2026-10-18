# Final — q-middleware-ratelimit-cors-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-middleware-ratelimit-cors-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-middleware-ratelimit-cors-server)

## How to solve (for a teammate)

The assigned values in the code (email, origins, keys, limits, layer values) are **seeded per email** — replace them with yours from the exam page.

**Approach:** Two `@app.middleware("http")` functions (rate limit registered first = innermost, then request context) and `CORSMiddleware` added last (outermost).

1. Make a folder named after the Vercel project you want (e.g. `tds-ga2-ping`) with this layout:
   ```
   tds-ga2-ping/
     app.py              # from api.index import app
     api/__init__.py     # empty
     api/index.py        # the app below
     requirements.txt    # fastapi
   ```
2. `app.py` contains exactly: `from api.index import app  # noqa: F401`
3. `api/index.py`:

<details><summary>api/index.py (click to expand)</summary>

```python
"""Middleware stack: CORS + request context + per-client rate limit
(TDS GA2 q-middleware-ratelimit-cors-server).

GET /ping -> {email, request_id}
Order (outermost first): CORS -> request context -> rate limit -> route.
 - CORS: only the assigned origin (+ the exam page origin for verification); no wildcard.
 - Request context: reuse inbound X-Request-ID or generate a UUID4; echo in body + header.
 - Rate limit: BUCKET requests / 10 s per X-Client-Id -> 429 + Retry-After.
"""
import math
import threading
import time
import uuid
from collections import defaultdict, deque

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = "ROLL_NUMBER@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://app-nbggbq.example.com"
EXAM_ORIGIN = "https://exam.sanand.workers.dev"
BUCKET = 11
WINDOW = 10.0

app = FastAPI()
HITS = defaultdict(deque)
LOCK = threading.Lock()


@app.middleware("http")  # innermost: rate limit
async def rate_limit(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)
    client = request.headers.get("x-client-id") or (request.client.host if request.client else "anon")
    now = time.monotonic()
    with LOCK:
        q = HITS[client]
        while q and now - q[0] >= WINDOW:
            q.popleft()
        if len(q) >= BUCKET:
            retry = max(1, math.ceil(WINDOW - (now - q[0])))
            return JSONResponse({"error": "rate limit exceeded"}, status_code=429,
                                headers={"Retry-After": str(retry)})
        q.append(now)
    return await call_next(request)


@app.middleware("http")  # middle: request context
async def request_context(request: Request, call_next):
    rid = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = rid
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response


app.add_middleware(  # outermost: CORS
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN, EXAM_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["X-Request-ID", "X-Client-Id", "Content-Type"],
    expose_headers=["X-Request-ID", "Retry-After"],
)


@app.get("/ping")
def ping(request: Request):
    return {"email": EMAIL, "request_id": request.state.request_id}


@app.get("/")
def root():
    return {"ok": True, "endpoint": "/ping"}
```

</details>

4. Deploy from inside the folder: `vercel deploy --prod --yes`. **No `vercel.json`** (rewrites make every route 404).
5. Submit the **Aliased** URL from the output (`https://<project>.vercel.app`), press Check, then Save.

Gotchas: Without it the browser grader cannot read anything. `expose_headers=["X-Request-ID","Retry-After"]`. Outermost → innermost: CORS → request context → rate limit, so 429s still carry CORS + X-Request-ID.

## Final prompt

```text
Middleware Stack: Rate-Limit + CORS + Request Context (1.5 marks)
<paste the full question text with your assigned values>
Write a FastAPI app for Vercel zero-config deployment (app.py re-exporting `app` from api/index.py,
requirements.txt, no vercel.json). Return JSON errors (never a bare 500). Two `@app.middleware("http")` functions (rate limit registered first = innermost, then request context) and `CORSMiddleware` added last (outermost).
Also give a pytest/TestClient script that replays exactly what the grader checks.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

```bash
cd ~/developer/t326tdsiitmbs && set -a && source .env && set +a
cd weeks/ga2/q-middleware-ratelimit-cors-server/src/tds-ga2-ping
vercel deploy --prod --yes
```

Source: [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-middleware-ratelimit-cors-server/src/tds-ga2-ping/api/index.py](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-middleware-ratelimit-cors-server/src/tds-ga2-ping/api/index.py)

## Expected output

Exam **Check** shows the question as correct.

## Answer submitted

```
https://<your-project>.vercel.app
```
