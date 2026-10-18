"""Minimal stateless MCP server over Streamable HTTP (TDS GA1 q-mcp-server-live-server).

One tool, solve_challenge (no arguments). On every tools/call it reads X-Exam-Challenge from the HTTP request
headers and returns the first 16 hex chars of SHA-256("<challenge>:<email>"), email trimmed + lowercased.
JSON-RPC over POST /mcp (also /), JSON responses (allowed by the spec), no sessions needed.
"""
from __future__ import annotations

import hashlib
import os

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = os.environ.get("EXAM_EMAIL", "ROLL_NUMBER@ds.study.iitm.ac.in").strip().lower()  # env var overrides
SUPPORTED = ["2025-06-18", "2025-03-26", "2024-11-05"]
TOOL = {
    "name": "solve_challenge",
    "description": "Return sha256('<X-Exam-Challenge header>:<registered email>')[:16] for this call.",
    "inputSchema": {"type": "object", "properties": {}, "required": []},
}

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
                   expose_headers=["Mcp-Session-Id"])


def answer(challenge: str) -> str:
    return hashlib.sha256(f"{challenge}:{EMAIL}".encode()).hexdigest()[:16]


def handle(msg: dict, headers) -> dict | None:
    mid, method = msg.get("id"), msg.get("method")
    if mid is None:  # notification (e.g. notifications/initialized): no response
        return None
    ok = lambda result: {"jsonrpc": "2.0", "id": mid, "result": result}
    err = lambda code, text: {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": text}}
    if method == "initialize":
        want = (msg.get("params") or {}).get("protocolVersion")
        return ok({"protocolVersion": want if want in SUPPORTED else SUPPORTED[0],
                   "capabilities": {"tools": {"listChanged": False}},
                   "serverInfo": {"name": "tds-ga1-mcp", "version": "1.0.0"}})
    if method == "ping":
        return ok({})
    if method == "tools/list":
        return ok({"tools": [TOOL]})
    if method == "tools/call":
        name = (msg.get("params") or {}).get("name")
        if name != "solve_challenge":
            return err(-32602, f"Unknown tool: {name}")
        challenge = (headers.get("x-exam-challenge") or "").strip()
        if not challenge:
            return ok({"content": [{"type": "text", "text": "missing X-Exam-Challenge header"}], "isError": True})
        return ok({"content": [{"type": "text", "text": answer(challenge)}], "isError": False})
    if method in ("resources/list", "prompts/list"):
        return ok({method.split("/")[0]: []})
    return err(-32601, f"Method not found: {method}")


async def mcp_post(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}, 400)
    if isinstance(body, list):
        out = [r for r in (handle(m, request.headers) for m in body) if r is not None]
        return JSONResponse(out) if out else Response(status_code=202)
    res = handle(body, request.headers)
    return JSONResponse(res) if res is not None else Response(status_code=202)


for path in ("/mcp", "/"):
    app.add_api_route(path, mcp_post, methods=["POST"])
    app.add_api_route(path, lambda: Response(status_code=405, headers={"Allow": "POST"}), methods=["GET"])
    app.add_api_route(path, lambda: Response(status_code=200), methods=["DELETE"])
