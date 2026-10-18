# Final — q-local-llm-structured-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-local-llm-structured-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-local-llm-structured-server)

## How to solve (for a teammate)

Assigned values (tags, IDs, parameters) are **seeded per email**: use the ones on your exam page.

**Approach:** Ollama `/api/chat` with a JSON-schema `format` and temperature 0 picks the fields; the model copies the amount *as written* and code parses it locale-aware and reconciles it with the numbers in the text; Pydantic validates; bad input → 422, LLM down → 503.

1. Run Ollama and pull a small model: `ollama serve`, `ollama pull qwen2.5:3b`.
2. Create `requirements.txt` (`fastapi`, `uvicorn`, `httpx`) and this `app.py`:

<details><summary>app.py (click to expand)</summary>

```python
"""Local-LLM invoice extractor (TDS GA2 q-local-llm-structured-server).

POST /extract {"text": "..."} -> {"vendor", "amount", "currency", "date"}  (Pydantic-validated)
- The local model (Ollama, default qwen2.5:3b) is called with a JSON-schema `format`, temperature 0.
- The model copies the amount *as written*; code parses it locale-aware ("129,25" -> 129.25,
  "1.234,50" -> 1234.5) and reconciles it with the numbers in the text; symbols -> ISO codes; dates -> YYYY-MM-DD
  and validated by the Pydantic response model.
- Empty / garbage input -> 422 (never 500). LLM down -> 503 JSON.
Run: uv run --with fastapi --with uvicorn --with httpx uvicorn app:app --port 8010
"""
import json
import os
import re
from datetime import datetime

import httpx
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "qwen2.5:3b")


class ExtractRequest(BaseModel):
    text: str = Field(min_length=1)


class Invoice(BaseModel):
    vendor: str = Field(min_length=1)
    amount: float
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")


SCHEMA = {
    "type": "object",
    "properties": {
        "vendor": {"type": "string"},
        "amount": {"type": "string"},
        "currency": {"type": "string"},
        "date": {"type": "string"},
    },
    "required": ["vendor", "amount", "currency", "date"],
}

SYSTEM = (
    "You extract fields from invoice text and reply with JSON only.\n"
    "vendor: the company that issued the invoice (full name, e.g. 'Acme-1a2b Industries Ltd.').\n"
    "amount: the TOTAL AMOUNT DUE copied exactly as written in the text (keep its digits, commas and dots; "
    "e.g. '129,25' or '1,234.50'). Ignore subtotals, tax lines and previously paid amounts.\n"
    "currency: 3-letter uppercase ISO code (USD, EUR, GBP, ...).\n"
    "date: the PAYMENT DUE date (not the invoice/issue date) as YYYY-MM-DD."
)

SYMBOLS = {"$": "USD", "US$": "USD", "€": "EUR", "£": "GBP", "¥": "JPY", "₹": "INR"}
MONTHS = "%d %B %Y|%d %b %Y|%B %d, %Y|%b %d, %Y|%B %d %Y|%b %d %Y|%Y/%m/%d|%d/%m/%Y|%Y.%m.%d|%d.%m.%Y".split("|")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.exception_handler(RequestValidationError)
async def bad_request(_: Request, exc: RequestValidationError):
    return JSONResponse({"error": "invalid input", "detail": exc.errors()[:3]}, status_code=422)


NUM_RE = re.compile(r"\d[\d.,\u00a0\u202f']*\d|\d")  # digits with . , NBSP/thin-space/' separators


def parse_amount(s) -> float:
    """Parse '1,234.50', '1.234,50', '129,25', 'EUR 129,25', 129.25 -> float (locale-aware)."""
    if isinstance(s, (int, float)):
        return float(s)
    m = NUM_RE.search(str(s))
    if not m:
        raise ValueError(f"no number in {s!r}")
    t = re.sub(r"[\u00a0\u202f']", "", m.group(0))
    last = max(t.rfind("."), t.rfind(","))
    if last != -1 and len(t) - last - 1 in (1, 2):  # last separator + 1-2 digits = decimal point
        return float(re.sub(r"[.,]", "", t[:last]) + "." + t[last + 1:])
    return float(re.sub(r"[.,]", "", t))  # otherwise separators are thousands


def norm_amount(llm_value, text: str) -> float:
    """Trust the LLM's choice of WHICH amount, but fix separator mistakes against the text itself
    (e.g. the model turns '129,25' into 12925)."""
    v = parse_amount(llm_value)
    found = [m.group(0) for m in NUM_RE.finditer(text)]
    vals = []
    for f in found:
        try:
            vals.append(parse_amount(f))
        except ValueError:
            pass
    if any(abs(v - c) < 0.005 for c in vals):
        return v
    as_written = str(llm_value)
    if isinstance(llm_value, float) and llm_value.is_integer():
        as_written = str(int(llm_value))
    digits = re.sub(r"\D", "", as_written).lstrip("0")
    for f in found:
        if re.sub(r"\D", "", f).lstrip("0") == digits:
            return parse_amount(f)
    return v


def norm_currency(v, text: str) -> str:
    c = str(v or "").strip().upper()
    c = SYMBOLS.get(c, c)
    if re.fullmatch(r"[A-Z]{3}", c):
        return c
    for code in re.findall(r"\b(USD|EUR|GBP|INR|JPY|AUD|CAD|CHF)\b", text.upper()):
        return code
    for sym, code in SYMBOLS.items():
        if sym in text:
            return code
    return c


def norm_date(v) -> str:
    s = str(v or "").strip()
    m = re.search(r"\d{4}-\d{2}-\d{2}", s)
    if m:
        return m.group(0)
    for fmt in MONTHS:
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return s


async def ask_llm(text: str) -> dict:
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}],
        "format": SCHEMA,
        "stream": False,
        "options": {"temperature": 0},
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
        r.raise_for_status()
        return json.loads(r.json()["message"]["content"])


@app.post("/extract", response_model=Invoice)
async def extract(req: ExtractRequest):
    text = req.text.strip()
    if len(re.findall(r"[A-Za-z0-9]", text)) < 3:
        return JSONResponse({"error": "text has no extractable content"}, status_code=422)
    try:
        raw = await ask_llm(text)
    except (httpx.HTTPError, KeyError, json.JSONDecodeError) as e:
        return JSONResponse({"error": f"local LLM unavailable or returned bad JSON: {e}"}, status_code=503)
    try:
        return Invoice(
            vendor=str(raw.get("vendor", "")).strip(),
            amount=norm_amount(raw.get("amount"), text),
            currency=norm_currency(raw.get("currency"), text),
            date=norm_date(raw.get("date")),
        )
    except (ValidationError, ValueError, TypeError) as e:
        return JSONResponse({"error": "could not extract all fields", "llm_output": raw, "detail": str(e)[:300]},
                            status_code=422)


@app.get("/")
def root():
    return {"ok": True, "endpoint": "POST /extract", "model": MODEL}
```

</details>

3. `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn app:app --port 8010`
4. Test: `curl -s localhost:8010/extract -H 'content-type: application/json' -d '{"text":"Invoice from Acme-1a2b Industries Ltd. Total due: EUR 129,25. Payment due by 2026-03-05."}'` → amount `129.25`.
5. `cloudflared tunnel --url http://localhost:8010`; submit `https://<tunnel>/extract`, Check, keep everything running until Save.

Gotchas: An invoice wrote `129,25`; asking the model for a "plain number" produced `12925`. Fixed by having it copy the amount as written and parsing `,`/`.` in code (last separator + 1–2 digits = decimal). Prompt asks explicitly for the *payment due* date and the *total due* amount. Custom `RequestValidationError` handler + empty/symbol-only check → 422, never 500.

## Final prompt

```text
Local LLM Structured-Output Service (2 marks)
<paste the full question with your assigned values>
Give me the exact files and terminal commands for macOS (zsh) to satisfy every grader check, including
how to expose it publicly / package it, plus a quick local test for each check.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

See the steps above; code lives in [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-local-llm-structured-server/src](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-local-llm-structured-server/src).

## Expected output

Exam **Check** marks the question solved.

## Answer submitted

```
https://<random-words>.trycloudflare.com/extract (cloudflared quick tunnel; changes every run)
```
