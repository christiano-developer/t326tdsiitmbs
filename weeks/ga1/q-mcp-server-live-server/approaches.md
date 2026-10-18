# Approaches — q-mcp-server-live-server

## Problem in one line

Stateless MCP endpoint whose one tool hashes a per-request header with the email.

## Grader (from quiz JS)

- Client: URL must start with `https://`. Then **server-side** `/backendVerify` (version `v1`) acts as an MCP client.
- Score reflects live behaviour at check time; downtime later loses it.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Worked example `8f4a2c6e1b90d735` | Distractor | Explicitly fake; don't use it as a test vector |
| Challenge in headers, not JSON body | Genuine | Tool args are empty; must read the HTTP request headers |
| Signature verification | Optional | Unscored |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Hand-written JSON-RPC handler in FastAPI, JSON responses, no sessions | FastAPI on Vercel | ~80 lines; stateless fits serverless; easy to read headers | Must follow the protocol shapes by hand | chosen |
| B | Official MCP SDK (`FastMCP`, streamable HTTP) | `mcp` package | Spec-complete | Session manager + lifespan are awkward on serverless; reading raw headers needs the request context | rejected |
| C | Long-running server (Render/Fly/HF) | Docker | No cold starts | More setup; must stay awake until the deadline | not needed |

## Chosen: A

**Why:** the grader only needs initialize → initialized → tools/list → tools/call; Streamable HTTP allows a plain
`application/json` response per POST, so a stateless handler is enough and survives serverless cold starts.

## Gotchas hit

- The challenge is in the **HTTP headers** of each `tools/call`, not in the tool arguments (input schema is empty).
- Notifications (no `id`) must get **no JSON-RPC response**: return HTTP 202.
- Echo the client's `protocolVersion` if supported, else answer with the newest supported one.
- Same Vercel routing trap as Q6: no `vercel.json` rewrite; export `app` from `app.py`.
- "Deployment Protection is on" only covers the one-off deployment URLs; submit the public **alias**.
- Keep it up until the deadline: the score is re-checked live on every Save.
- After any redeploy, re-run the 5-challenge check: a redeploy from a half-edited file silently broke it once.
  `vercel` acts on the folder you're in (`pwd` first); an env var added in the wrong folder lands on the wrong project.
- Opening the URL in a browser gives HTTP 405: normal, the endpoint only accepts POST.

## Verification

- Local: curl handshake; official `mcp` client (`src/test_client.py`) 5/5.
- Deployed alias from the exam page: initialize 200, notification 202, 5/5 correct hashes.
- Exam **Check** → "Live MCP checks passed." (2026-10-18).
