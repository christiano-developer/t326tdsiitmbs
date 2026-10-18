"""Redis-backed hit counter (TDS GA2 q-compose-redis-tunnel-server).

POST /hit/{key}   -> {"key", "count"}   (atomic Redis INCR)
GET  /count/{key} -> {"key", "count"}   (0 for unseen keys)
GET  /healthz     -> {"status": "ok", "redis": "up"}  (real PING)
All state lives in Redis, so counts survive api restarts and are shared by every uvicorn worker.
"""
import os

import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=int(os.getenv("REDIS_PORT", "6379")),
                decode_responses=True, socket_timeout=3)
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def rkey(key: str) -> str:
    return f"hits:{key}"


@app.post("/hit/{key}")
def hit(key: str):
    return {"key": key, "count": int(r.incr(rkey(key)))}


@app.get("/count/{key}")
def count(key: str):
    return {"key": key, "count": int(r.get(rkey(key)) or 0)}


@app.get("/healthz")
def healthz():
    try:
        r.ping()
        return {"status": "ok", "redis": "up"}
    except redis.RedisError:
        return JSONResponse({"status": "degraded", "redis": "down"}, status_code=503)
