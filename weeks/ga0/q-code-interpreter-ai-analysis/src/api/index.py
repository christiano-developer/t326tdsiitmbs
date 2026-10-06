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
