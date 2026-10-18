"""Orders API: idempotent POST, cursor pagination, per-client rate limit
(TDS GA2 q-api-idempotency-pagination-server).

POST /orders + Idempotency-Key -> 201 {"id", ...}; same key -> same id. The id is derived
from the key (sha256), so it is stable even across serverless instances.
GET /orders?limit=P&cursor=C -> {"items": [...], "next_cursor": opaque or null} over ids 1..TOTAL.
Rate limit: RATE requests / 10 s per X-Client-Id (sliding window) -> 429 + Retry-After.
"""
import base64
import hashlib
import math
import threading
import time
import uuid
from collections import defaultdict, deque

from fastapi import FastAPI, Header, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

TOTAL = 60
RATE = 17
WINDOW = 10.0

app = FastAPI()
HITS = defaultdict(deque)
LOCK = threading.Lock()
ORDERS = {}


@app.middleware("http")  # inner: rate limit (CORS below is added later -> outermost)
async def rate_limit(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)
    client = request.headers.get("x-client-id") or (request.client.host if request.client else "anon")
    now = time.monotonic()
    with LOCK:
        q = HITS[client]
        while q and now - q[0] >= WINDOW:
            q.popleft()
        if len(q) >= RATE:
            retry = max(1, math.ceil(WINDOW - (now - q[0])))
            return JSONResponse({"error": "rate limit exceeded", "limit": RATE, "window_s": WINDOW},
                                status_code=429, headers={"Retry-After": str(retry)})
        q.append(now)
    return await call_next(request)


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
                   expose_headers=["Retry-After"])


def order(i: int) -> dict:
    return {"id": i, "item": f"item-{i}", "amount": 10 * i}


def enc(offset: int) -> str:
    return base64.urlsafe_b64encode(f"o:{offset}".encode()).decode().rstrip("=")


def dec(cursor: str) -> int:
    raw = base64.urlsafe_b64decode(cursor + "=" * (-len(cursor) % 4)).decode()
    if not raw.startswith("o:"):
        raise ValueError("bad cursor")
    return int(raw[2:])


@app.post("/orders")
async def create_order(request: Request, idempotency_key: str | None = Header(None)):
    try:
        body = await request.json()
    except Exception:
        body = {}
    key = idempotency_key or str(uuid.uuid4())
    oid = "ord_" + hashlib.sha256(key.encode()).hexdigest()[:16]
    with LOCK:
        replay = oid in ORDERS
        if not replay:
            ORDERS[oid] = {"id": oid, "idempotency_key": key, "status": "created",
                           "amount": body.get("amount") if isinstance(body, dict) else None}
        rec = ORDERS[oid]
    return JSONResponse(rec, status_code=200 if replay else 201,
                        headers={"Idempotent-Replayed": "true" if replay else "false"})


@app.get("/orders")
def list_orders(limit: int = Query(10, ge=1, le=100), cursor: str | None = None):
    try:
        start = dec(cursor) if cursor else 0
    except Exception:
        return JSONResponse({"error": "invalid cursor"}, status_code=400)
    ids = range(start + 1, min(start + limit, TOTAL) + 1)
    nxt = start + len(ids)
    return {"items": [order(i) for i in ids], "next_cursor": enc(nxt) if nxt < TOTAL else None}


@app.get("/")
def root():
    return {"ok": True, "endpoints": ["POST /orders", "GET /orders?limit=&cursor="]}
