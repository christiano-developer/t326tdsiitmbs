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
