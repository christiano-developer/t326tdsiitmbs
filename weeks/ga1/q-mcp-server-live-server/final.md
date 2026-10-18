# Final — q-mcp-server-live-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-mcp-server-live-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-mcp-server-live-server)

## How to solve (for a teammate)

> Per email: the answer depends on your exam email, which the server reads from an env var. Live-graded: the
> server must stay up and correct until the deadline.

**Approach:** MCP over Streamable HTTP is JSON-RPC sent by POST. The grader only needs four messages, so a small
stateless FastAPI handler is enough: answer `initialize`, return HTTP 202 for the `notifications/initialized`
notification, list one tool with an empty input schema, and on `tools/call` read `X-Exam-Challenge` **from the
request headers** and return `sha256("<challenge>:<email>")[:16]` as one text block. Deploy on Vercel; set your email as the code default or
via the `EXAM_EMAIL` env var.

1. Create `src/api/index.py` (below), `src/api/__init__.py` (empty), `src/app.py` containing
   `from api.index import app`, and `src/requirements.txt` containing `fastapi`.
2. Test locally: `EXAM_EMAIL=<your exam email> uv run --with fastapi --with uvicorn uvicorn app:app --port 8000`,
   then run the test client (below) against `http://localhost:8000/mcp`; expect `correct: 5 / 5`.
3. Deploy from `src/`: `vercel link --yes --project <name>`, `vercel deploy --prod` (put your email in the code default, or
   `vercel env add EXAM_EMAIL production` first). Don't add a `vercel.json` rewrite.
4. Run the test client against `https://<Aliased URL>/mcp`, then submit that URL, Check, Save. Keep the project
   alive until the deadline.

<details><summary>src/api/index.py (click to expand)</summary>

```python
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
```

</details>

<details><summary>src/test_client.py — grader-like check (click to expand)</summary>

```python
"""Check a deployed MCP endpoint like the grader does: 5 fresh challenges via the official MCP client.
Usage: EXAM_EMAIL=<your exam email> uv run --with mcp python test_client.py https://<project>.vercel.app/mcp
(Written against mcp 2.x: streamable_http_client + create_mcp_http_client.)"""
import asyncio, hashlib, os, secrets, sys

from mcp import ClientSession
from mcp.client.streamable_http import create_mcp_http_client, streamable_http_client

EMAIL = os.environ["EXAM_EMAIL"].strip().lower()
URL = sys.argv[1]


async def main():
    ok = 0
    for _ in range(5):
        ch = secrets.token_hex(16)
        async with create_mcp_http_client(headers={"X-Exam-Challenge": ch}) as hc:
            async with streamable_http_client(URL, http_client=hc) as streams:
                async with ClientSession(streams[0], streams[1]) as s:
                    await s.initialize()
                    tools = await s.list_tools()
                    res = await s.call_tool("solve_challenge", {})
                    ok += res.content[0].text == hashlib.sha256(f"{ch}:{EMAIL}".encode()).hexdigest()[:16]
    print("tools:", [t.name for t in tools.tools], "| correct:", ok, "/ 5")


asyncio.run(main())
```

</details>

## Final prompt

```text
Write a stateless MCP server (Streamable HTTP, JSON responses, no sessions) as a FastAPI app for Vercel:
POST /mcp handles JSON-RPC initialize (echo a supported protocolVersion, tools capability), returns HTTP 202 for
notifications, tools/list with one tool solve_challenge (empty input schema), and tools/call that reads the
X-Exam-Challenge HTTP header and returns one text content block with sha256("<challenge>:<email>")[:16], where
email = EXAM_EMAIL env var (default: my exam email) trimmed and lowercased. Export the app from app.py; no vercel.json rewrites.
```

- **Tool / model used:** Claude (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

See [deploy.md](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga1/q-mcp-server-live-server/deploy.md).

## Expected output

```
tools: ['solve_challenge'] | correct: 5 / 5
```

## Answer submitted (✅ Check passed)

The deployed alias URL + `/mcp` (see README).
