# Prompt log — q-mcp-server-live-server

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude (Claude Opus 5.5), Claude desktop app (files on this Mac) + Claude in Chrome.
- **Goal:** build and deploy a live MCP server.

```text
lets start with Q6 and 14
```

- **Result:** worked after one routing fix (shared with Q6). Hand-rolled stateless JSON-RPC over POST `/mcp`
  (initialize, notifications/initialized → 202, tools/list, tools/call reading `X-Exam-Challenge` from the HTTP
  headers). Locally: curl handshake OK and the official `mcp` Python client got 5/5. First deploy hit the same
  `vercel.json` rewrite 404 problem as Q6; fixed with `app.py`. Deployed alias tested from the exam page (5/5),
  exam Check: "Live MCP checks passed."
- **Next:** move the email out of code.

---

## P2

- **Tool / model:** same.
- **Goal:** keep credentials out of the repo.

```text
it should be a generalised way, my credentials must not be present
email is okay in commits and file; any other credential such as api token or login nope
```

- **Result:** the email stays as the code default with an `EXAM_EMAIL` env override (the deployed code is this
  exact version, so no redeploy needed). No tokens or logins anywhere in the folder.
- **Next:** none.

---

## P3

- **Tool / model:** same.
- **Goal:** find why the live server broke.

```text
something happened to Q14, can you check why the url doesn't work
```

- **Result:** the live server answered every call with "server misconfigured: EXAM_EMAIL not set". It had been
  redeployed from an intermediate version without the default email, and `vercel env add EXAM_EMAIL` had been run in
  the Q6 folder (wrong project). Redeployed the current code (email default in code): 5/5 again, exam Check
  "Live MCP checks passed." The browser's HTTP 405 on the URL is normal (MCP only accepts POST).
- **Next:** none. Lesson: re-run the 5-challenge check after **every** redeploy, and check `pwd` before `vercel` commands.
