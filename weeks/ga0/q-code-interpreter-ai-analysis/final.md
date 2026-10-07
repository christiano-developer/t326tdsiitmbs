# Final — q-code-interpreter-ai-analysis

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-code-interpreter-ai-analysis](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-code-interpreter-ai-analysis)

## How to solve (for a teammate)

> Values are seeded from your email, but the same app works for everyone (see "Answer submitted").

Needs Node.js (for `npx`) and a free Vercel account.

1. Create an empty folder `code-interpreter` with three files and no `vercel.json`:
   - `api/index.py`: copy the code below as-is.
     <details><summary>index.py (click to expand)</summary>

     ```python
     """POST /code-interpreter - run Python code; on error, report the error line numbers.

     Hybrid error analysis ("AI only when needed"):
       1. Deterministic: take the line from the traceback itself - the deepest frame in the user's code
          ("<string>"), or the SyntaxError's own line. Exact and free.
       2. AI fallback: only if (1) finds nothing, ask an LLM via AIPipe with structured output (Pydantic).
     Successful runs return stdout exactly; errors return the traceback.
     """
     import json
     import os
     import traceback
     import urllib.request
     from contextlib import redirect_stdout
     from io import StringIO
     from typing import List, Optional

     from fastapi import FastAPI
     from fastapi.middleware.cors import CORSMiddleware
     from pydantic import BaseModel

     app = FastAPI()
     app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

     USER_FILE = "<string>"  # filename the user's code is compiled under


     class CodeRequest(BaseModel):
         code: str


     class CodeResponse(BaseModel):
         error: List[int]
         result: str


     class ErrorAnalysis(BaseModel):
         error_lines: List[int]


     def execute_python_code(code: str) -> dict:
         """Tool: run the code in a fresh namespace, capture stdout exactly, or return the traceback."""
         buf = StringIO()
         try:
             with redirect_stdout(buf):
                 exec(compile(code, USER_FILE, "exec"), {"__name__": "__main__"})
             return {"success": True, "output": buf.getvalue(), "exc": None}
         except Exception as exc:  # includes SyntaxError from compile() and RecursionError
             return {"success": False, "output": traceback.format_exc(), "exc": exc}


     def error_lines_from_traceback(exc: BaseException) -> List[int]:
         """Deterministic analysis: the line in the user's code where the error was raised."""
         if isinstance(exc, SyntaxError) and exc.filename == USER_FILE and exc.lineno:
             return [exc.lineno]
         frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == USER_FILE]
         return [frames[-1].lineno] if frames else []


     def analyze_error_with_ai(code: str, tb: str) -> List[int]:
         """AI fallback (only used if the traceback has no user-code line): structured output via AIPipe."""
         token = os.environ.get("AIPIPE_TOKEN")
         if not token:
             return []
         numbered = "\n".join(f"{i}: {line}" for i, line in enumerate(code.splitlines(), 1))
         body = {
             "model": os.environ.get("AI_MODEL", "gpt-4.1-mini"),
             "temperature": 0,
             "messages": [
                 {"role": "system", "content": "You find the line numbers in Python code where an error occurred."},
                 {"role": "user", "content": f"CODE (numbered):\n{numbered}\n\nTRACEBACK:\n{tb}\n\n"
                                             "Return the line number(s) in CODE where the error is raised."},
             ],
             "response_format": {"type": "json_schema", "json_schema": {
                 "name": "error_analysis", "strict": True,
                 "schema": {"type": "object", "additionalProperties": False,
                            "properties": {"error_lines": {"type": "array", "items": {"type": "integer"}}},
                            "required": ["error_lines"]}}},
         }
         req = urllib.request.Request(
             "https://aipipe.org/openai/v1/chat/completions", data=json.dumps(body).encode(),
             headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}",
                      "User-Agent": "Mozilla/5.0 (code-interpreter)"})  # AIPipe 403s Python's default UA
         try:
             with urllib.request.urlopen(req, timeout=25) as r:
                 content = json.load(r)["choices"][0]["message"]["content"]
             return ErrorAnalysis.model_validate_json(content).error_lines
         except Exception:
             return []


     @app.post("/code-interpreter", response_model=CodeResponse)
     def code_interpreter(req: CodeRequest) -> CodeResponse:
         run = execute_python_code(req.code)
         if run["success"]:
             return CodeResponse(error=[], result=run["output"])
         lines: Optional[List[int]] = error_lines_from_traceback(run["exc"])
         if not lines:
             lines = analyze_error_with_ai(req.code, run["output"])
         return CodeResponse(error=sorted(set(lines)), result=run["output"])


     @app.get("/")
     def health() -> dict:
         return {"status": "ok", "endpoint": "POST /code-interpreter"}
     ```

     </details>

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

## Reproduction steps (needs a clone of this repo)

See [deploy.md](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-code-interpreter-ai-analysis/deploy.md): local venv → [`src/test_all.py`](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-code-interpreter-ai-analysis/src/test_all.py) (60/60) → `npx vercel --prod --yes` → test the deployed URL →
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
