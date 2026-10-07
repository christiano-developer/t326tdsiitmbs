# Final — q-code-interpreter-ai-analysis

> Goal: the answer can be reproduced from this file alone.

## How to solve (for a teammate)

> Values are seeded from your email, but the same app works for everyone (see "Answer submitted").

Needs Node.js (for `npx`) and a free Vercel account.

1. Create an empty folder `code-interpreter` with three files and no `vercel.json`:
   - `api/index.py`: copy [src/api/index.py](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-code-interpreter-ai-analysis/src/api/index.py) as-is.
   - `main.py`: one line, `from api.index import app`.
   - `requirements.txt`: two lines, `fastapi` and `pydantic`.
2. Deploy: in that folder run `npx vercel login` (once), then `npx vercel --prod --yes`. Copy the URL printed after **Aliased:** (`https://<project>.vercel.app`). Don't use the long unique URL: it returns 401.
3. Test it (should print `{"error":[],"result":"2\n"}`):
   ```bash
   curl -s -X POST https://<project>.vercel.app/code-interpreter -H "Content-Type: application/json" -d '{"code":"print(1+1)"}'
   ```
4. Submit the base URL `https://<project>.vercel.app`, then Check and Save.

Optional: `npx vercel env add AIPIPE_TOKEN` enables an LLM fallback for unusual errors. It wasn't needed to pass.

## Final prompt

```text
Write a FastAPI app for Vercel (app in api/index.py, root main.py doing `from api.index import app`, NO vercel.json rewrite) with CORS "*" and
POST /code-interpreter {code} -> {error: [int], result: str}:
- execute with compile(code, "<string>", "exec") + exec in a fresh namespace, stdout captured via redirect_stdout;
  on success return error=[] and the exact stdout
- on exception return traceback.format_exc() as result; error lines = SyntaxError.lineno if it's a SyntaxError in
  "<string>", else the lineno of the LAST traceback frame whose filename is "<string>"
- only if no line is found, call an LLM (AIPipe OpenAI-compatible, json_schema structured output parsed with a
  Pydantic model {error_lines: List[int]}); send a non-default User-Agent header.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

See [deploy.md](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-code-interpreter-ai-analysis/deploy.md): local venv → `src/test_all.py` (60/60) → `npx vercel --prod --yes` → test the deployed URL →
submit the base URL.

## Expected output

```
PASS #10 (yours) expected='120\n' got_error=[]
PASS #36 (yours) expected='3\n6\n' got_error=[]
PASS #43 (yours) expected=[2] got_error=[2]

60/60 passed
```

## Answer submitted (✅ passed, attempt 1)

```
https://tds-ga0-code-interpreter.vercel.app
```
