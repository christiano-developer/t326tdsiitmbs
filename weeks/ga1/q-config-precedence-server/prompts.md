# Prompt log — q-config-precedence-server

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude (Claude Opus 5.5), Claude desktop app (files on this Mac) + Claude in Chrome.
- **Goal:** build and deploy the layered-config API.

```text
lets start with Q6 and 14
```

- **Result:** partial. FastAPI app with the 4 layers + `?set=` overrides, coercion, alias, masking and CORS
  passed every local curl test. First Vercel deploy used `vercel.json` with a rewrite to `/api/index`:
  **every path returned FastAPI's 404**, even `/docs`, because the rewrite hands the app the destination path.
- **Next:** drop the rewrite, use Vercel's native FastAPI entrypoint.

---

## P2

- **Tool / model:** same.
- **Goal:** fix routing.

```text
(continuation) all paths 404 on Vercel — switch to the FastAPI preset
```

- **Result:** worked. Added `src/app.py` re-exporting the app, removed `vercel.json`. Redeployed: base config and
  overrides correct from the browser; exam Check: "Config precedence, type coercion, alias, and secret masking
  all verified. ✅"
- **Next:** none.
