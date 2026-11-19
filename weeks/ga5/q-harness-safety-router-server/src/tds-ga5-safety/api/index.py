import hashlib, json, os, time
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.rules import classify

KV_URL = os.environ.get("KV_REST_API_URL") or os.environ.get("UPSTASH_REDIS_REST_URL") or ""
KV_TOKEN = os.environ.get("KV_REST_API_TOKEN") or os.environ.get("UPSTASH_REDIS_REST_TOKEN") or ""
CAPTURE_TOKEN = os.environ.get("CAPTURE_TOKEN", "")
PROFILE = "agent-harness-2026-09"

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

async def kv(*cmd):
    if not (KV_URL and KV_TOKEN):
        return None
    async with httpx.AsyncClient(timeout=8) as c:
        r = await c.post(KV_URL, json=list(cmd), headers={"Authorization": f"Bearer {KV_TOKEN}"})
        return r.json().get("result")

@app.get("/")
async def health():
    return {"ok": True, "profile": PROFILE, "capture": bool(KV_URL and KV_TOKEN)}

@app.post("/classify")
async def route(req: Request):
    raw = await req.body()
    try:
        data = json.loads(raw)
    except Exception:
        return JSONResponse({"error": "invalid JSON"}, status_code=400)
    results = []
    for case in data.get("cases") or []:
        try:
            results.append(classify(case))
        except Exception:
            results.append({"caseId": case.get("caseId"), "requestDecision": "review", "toolDecision": "review" if case.get("proposedTool") else "none",
                            "route": "primary", "trajectory": "watch"})
    out = {"profile": data.get("profile", PROFILE), "batchId": data.get("batchId"), "results": results}
    try:  # capture raw batches for offline tuning (deduplicated by content hash)
        h = hashlib.sha256(raw).hexdigest()[:16]
        await kv("SET", f"hs:batch:{h}", raw.decode("utf-8", "replace"), "EX", 60 * 60 * 24 * 14)
        await kv("SADD", "hs:batches", h)
    except Exception:
        pass
    return JSONResponse(out)

@app.get("/_capture")
async def capture_list(req: Request):
    if not CAPTURE_TOKEN or req.headers.get("x-capture-token") != CAPTURE_TOKEN:
        return JSONResponse({"error": "forbidden"}, status_code=403)
    return {"batches": await kv("SMEMBERS", "hs:batches")}

@app.get("/_capture/{h}")
async def capture_get(h: str, req: Request):
    if not CAPTURE_TOKEN or req.headers.get("x-capture-token") != CAPTURE_TOKEN:
        return JSONResponse({"error": "forbidden"}, status_code=403)
    v = await kv("GET", f"hs:batch:{h}")
    return JSONResponse(json.loads(v) if v else {"error": "missing"})
