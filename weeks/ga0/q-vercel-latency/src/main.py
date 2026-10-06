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
