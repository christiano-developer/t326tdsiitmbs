# Approaches — q-ollama

## Problem in one line

Expose local Ollama through an ngrok HTTPS URL so a browser on the exam page can read `/api/version` and an `X-Email` header.

## Grader (from quiz JS)

1. `new URL(answer).hostname` must include `ngrok`.
2. Browser `fetch(<url>/api/version, {headers: {"ngrok-skip-browser-warning": true}})`. The custom header triggers a
   **CORS preflight** (OPTIONS).
3. Body must be JSON with a truthy `version`.
4. `response.headers.get("x-email")` must equal the exam email (readable only with `Access-Control-Expose-Headers`).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Model commands (`ollama pull gemma3…`, `/api/chat`) | **Distractor** | `/api/version` needs no model |
| "Your **X-User-Email** header is echoed" | **Distractor** | The grader reads `X-Email` (what the ngrok command adds) |
| `uvx ngrok …` | Environment | uv isn't installed; used the brew `ngrok` binary |
| `--response-header-add '…Authorization,Content-Type,…'` (page command) | **Trap (ngrok 3.39)** | Deprecated flag splits values on commas → `ERROR: Malformed header: Content-Type`. Use a traffic policy file |
| Page doesn't mention Ollama's Host check | **Hidden trap** | Ollama 403s requests whose `Host` isn't localhost (DNS-rebinding protection). Through ngrok the Host is the ngrok domain → GET 403 with an empty body → "Unexpected end of JSON input". Needs `--host-header=rewrite` |
| Ollama desktop app running | Trap | Ignores a terminal `OLLAMA_ORIGINS`; run `ollama serve` yourself (the app wasn't running here) |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered (Host 403)

| # | Fix | Verdict |
|---|-----|---------|
| 1 | **`ngrok … --host-header=rewrite`** (rewrites Host to `localhost:11434`; the flag is hidden from 3.39's help but works) | **chosen, worked**: Ollama stays bound to localhost |
| 2 | `OLLAMA_HOST=0.0.0.0:11434 ollama serve` (non-loopback bind skips the Host check) | fallback; exposes Ollama on the LAN |

## Verification

- Local: Host=ngrok domain → 403, Host=localhost → 200 (proved the cause).
- `src/check_ngrok.sh <url> <email>` through the live tunnel → 8/8 PASS (preflight 2xx + Allow-Origin * + allows
  ngrok-skip-browser-warning; body `{"version":"0.17.5"}`; GET Allow-Origin *; Expose-Headers *; X-Email matches).
- Exam "Check": ✅ passed (2026-10-07).
