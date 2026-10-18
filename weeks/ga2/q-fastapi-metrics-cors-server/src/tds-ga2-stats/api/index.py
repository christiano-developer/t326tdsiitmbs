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
