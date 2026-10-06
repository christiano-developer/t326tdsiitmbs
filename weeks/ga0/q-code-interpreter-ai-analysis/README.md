# q-code-interpreter-ai-analysis

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes (Vercel) |
| Started   | 2026-10-07 |
| Closed    | 2026-10-07 (passed on attempt 1) |

## Question

**Code Interpreter with AI Error Analysis**: background: *Large Language Models* (AIPipe proxy, structured output).

> Create a FastAPI endpoint `POST /code-interpreter` that executes Python code and uses AI to analyze errors.
> Request `{"code": "..."}` → response `{"error": [line numbers], "result": "exact output or traceback"}`.
> Flow: tool `execute_python_code()` (exec, capture stdout/traceback) → if success return `{error: [], result}` → else an AI
> agent (structured output, Pydantic) returns the error line numbers. Requirements: exact output, AI only when needed,
> structured output, CORS enabled. Tested with 3 random snippets: exact stdout for clean code, exact error lines for errors.

(The page's sample uses Gemini `gemini-2.0-flash-exp` with `GEMINI_API_KEY`.)

## Inputs / given data

- [data/grader_tests.json](data/grader_tests.json): the grader's full bank of 60 tests (30 clean / 30 error), from the quiz JS.
  This student's seeded 3: **#43** (`int('abc')` → ValueError, line [2]), **#36** (`"3\n6\n"`), **#10** (`"120\n"`).

## Final answer

```
https://tds-ga0-code-interpreter.vercel.app
```

The grader appends `/code-interpreter`. Live check: **60/60** grader cases pass; CORS `*`.

## Status notes

- Local and live (https://tds-ga0-code-interpreter.vercel.app): **60/60**; CORS `*`. Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) · [approaches.md](approaches.md) · [final.md](final.md) · [deploy.md](deploy.md)
- [src/api/index.py](src/api/index.py) — FastAPI app (tool + deterministic line analysis + AI fallback)
- [src/main.py](src/main.py), [src/requirements.txt](src/requirements.txt), [src/.vercelignore](src/.vercelignore) — Vercel entrypoint/config
- [src/test_all.py](src/test_all.py) — runs all 60 grader tests against any base URL
