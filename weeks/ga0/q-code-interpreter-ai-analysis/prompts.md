# Prompt log — q-code-interpreter-ai-analysis

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** scaffold and plan

```text
Code Interpreter with AI Error Analysis
<LLM/AIPipe background + task, flow, sample code, examples, testing notes: see README.md>
scaffold and guide the approach
```

- **Result:** read the grader: 60-test bank in the JS, 3 seeded (mine #43, #36, #10), exact checks. Flagged that the
  "AI must identify lines" requirement is unverifiable and deterministic, plus the Gemini/sample-code distractors. Offered
  error-line options A/B/C and hosting via tunnel vs Vercel. Tools: no uv/vercel/cloudflared; docker + npx present.
- **Next:** user picks.

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** build option C, host on Vercel

```text
option C, should we vercel, since its reusable for other qs
```

- **Result:** Vercel, one project per question. Created a git-ignored venv (fastapi, uvicorn). Wrote `src/api/index.py`
  (fresh-namespace exec + redirect_stdout; deepest `<string>` frame / SyntaxError line; AIPipe structured-output fallback
  only when no line is found), `vercel.json`, `requirements.txt`, `src/test_all.py`. Local: **60/60**, CORS `*`.
- **Next:** user runs `npx vercel login`; approve deploy (+ optional AIPIPE_TOKEN env var).

---

## P3

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** deploy to Vercel

```text
i logged in, whats should i run next
<vercel link output: project created; GitHub link failed (no login connection)>
<vercel --prod output: Production …-gs15qujh6-… ; Aliased https://tds-ga0-code-interpreter.vercel.app; "Deployment Protection is on">
```

- **Result:** confirmed login (`vercel whoami`). Gave link → deploy → test steps. GitHub-link failure is harmless (CLI-only
  deploys). Added `.vercelignore`. First deploy: the alias returned **404** (the vercel.json rewrite under the FastAPI
  preset routes by the rewritten path) and the unique URL was protected (401). Replaced vercel.json with a `main.py`
  entrypoint and redeployed. Live `https://tds-ga0-code-interpreter.vercel.app` → **60/60**, CORS `*`.
- **Next:** user submits the URL.

---

## P4

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** record the result

```text
correct
```

- **Result:** ✅ passed on the first submission. Status → `solved`, committed and tagged. Keep the Vercel project up until grading closes.
- **Next:** none (teardown after grading: see deploy.md).
