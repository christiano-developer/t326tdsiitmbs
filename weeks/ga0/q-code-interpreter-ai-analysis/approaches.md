# Approaches — q-code-interpreter-ai-analysis

## Problem in one line

Public FastAPI `POST /code-interpreter`: exact stdout for clean code; exact error line(s) + traceback for failing code.

## Grader (from quiz JS)

- A bank of **60 snippets** (30 clean with `expectedOutput`, 30 failing with `errorLines` + `errorType`), shuffled with
  `seedrandom(email#q-code-interpreter-ai-analysis)`; the first 3 are sent. **Mine: #43, #36, #10.**
- URL: must start with http(s); `/code-interpreter` is appended unless already present.
- Per test: HTTP OK; `content-type` includes `application/json`; `error` is an array; `result` is a string.
  - error case: `sorted(error) == sorted(errorLines)` **and** result contains "Traceback" or "Error"
  - clean case: `error == []` **and** `result === expectedOutput` (byte-exact)
- **All 3 must pass.** Browser `fetch`, so CORS is required.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "AI must identify exact error lines" | **Distractor** | Unverifiable by the grader. The expected line is always the deepest `<string>` frame (or the SyntaxError line), which is deterministic. An LLM risks e.g. answering 4 for `divide(10, 0)` where expected is **2** (inside the function) |
| Gemini sample (`google.genai`, `GEMINI_API_KEY`, `gemini-2.0-flash-exp`) | Distractor | Not required; the AI fallback uses AIPipe (OpenAI-compatible) structured output |
| Sample `execute_python_code` | Trap | `exec(code)` in the server's globals leaks state between requests; manual `sys.stdout` swap. Use a fresh namespace + `redirect_stdout` |
| Clean output must be byte-exact | Genuine | No extra prints/logging into stdout |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Error-line method | Verdict |
|---|-------------------|---------|
| A | Parse the traceback only | exact, but drops the "AI" element entirely |
| B | LLM only (AIPipe structured output) | literal spec, but nondeterministic, costs, can miss inner-frame lines |
| C | **Hybrid: parse the traceback; call the LLM only if no user-code line is found** | **chosen (user's pick)**: exact, free in practice, keeps "AI only when needed" |

| # | Hosting | Verdict |
|---|---------|---------|
| 1 | Local + Cloudflare quick tunnel (Docker) | quick, temporary |
| 2 | **Vercel, one project per question** | **chosen**: permanent; same login/CLI/config pattern reused for q-fastapi / q-vercel-latency; separate projects so redeploys can't break graded endpoints |

## Gotchas

- **Vercel FastAPI preset: no `vercel.json` rewrite.** Rewrites to `/api/index` change the path FastAPI sees, giving 404. Use a root `main.py` exporting `app`.
- **Submit the production alias**, not the unique deployment URL (protected by Vercel Authentication, 401).

- Compile with filename `"<string>"` so user frames are identifiable; `SyntaxError` comes from `compile()` with `.lineno`.
- Error line = **last** `<string>` frame (`divide(10,0)` → 2; `add(1,2,3)` TypeError → 4 at the call; recursion → 2).
- AIPipe blocks Python's default User-Agent (403), so set a custom UA (lesson from q-get-llm-to-say-yes).

## Verification

- Local uvicorn + `src/test_all.py` → **60/60** (incl. #10, #36, #43); CORS preflight → `access-control-allow-origin: *`.
- AI fallback: not triggered by any of the 60 cases (no AIPipe cost).
- Live https://tds-ga0-code-interpreter.vercel.app: `src/test_all.py` → **60/60**; CORS preflight 200 with `*`.
- First deploy returned 404 everywhere (vercel.json rewrite under the FastAPI preset), fixed with a `main.py` entrypoint and no rewrite.
- Exam "Check": ✅ passed on attempt 1 (2026-10-07).
