"""Stateless POST /analytics endpoint (TDS GA2 q-deploy-analytics-platform-server).

Auth: X-API-Key must equal the API_KEY env var (set in Vercel), else 401.
Body {"events": [{"user", "amount", "ts"}]} ->
  {email, total_events, unique_users, revenue (sum of amount > 0), top_user (max positive total)}
"""
import os
import secrets

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = "ROLL_NUMBER@ds.study.iitm.ac.in"

app = FastAPI()
# CORS is outermost, so 401 responses also carry CORS headers and the browser can read the status
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


@app.post("/analytics")
async def analytics(request: Request):
    expected = os.environ.get("API_KEY", "")
    given = request.headers.get("x-api-key", "")
    if not expected or not secrets.compare_digest(given, expected):
        return JSONResponse({"error": "invalid or missing X-API-Key"}, status_code=401)
    try:
        body = await request.json()
        events = body.get("events", []) if isinstance(body, dict) else []
    except Exception:
        return JSONResponse({"error": "body must be JSON {events: [...]}"}, status_code=400)
    if not isinstance(events, list):
        events = []
    events = [e for e in events if isinstance(e, dict)]
    per_user = {}
    revenue = 0.0
    for e in events:
        amt = num(e.get("amount"))
        if amt > 0:
            revenue += amt
            per_user[e.get("user")] = per_user.get(e.get("user"), 0.0) + amt
    top_user = max(per_user, key=per_user.get) if per_user else None
    tidy = lambda v: int(v) if float(v).is_integer() else round(v, 6)  # noqa: E731
    return {
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len({e.get("user") for e in events}),
        "revenue": tidy(revenue),
        "top_user": top_user,
    }


@app.get("/")
def root():
    return {"ok": True, "endpoint": "POST /analytics (X-API-Key)"}
