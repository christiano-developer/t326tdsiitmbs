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
