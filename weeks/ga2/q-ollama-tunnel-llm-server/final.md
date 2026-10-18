# Final — q-ollama-tunnel-llm-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-ollama-tunnel-llm-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-ollama-tunnel-llm-server)

## How to solve (for a teammate)

Assigned values (tags, IDs, parameters) are **seeded per email**: use the ones on your exam page.

**Approach:** `OLLAMA_ORIGINS="*" ollama serve` + `cloudflared tunnel --url http://localhost:11434 --http-host-header localhost:11434`; submit the tunnel's `/v1/chat/completions` URL with the model name.

1. Quit the Ollama menu-bar app if it is running, then start the server with CORS open: `OLLAMA_ORIGINS="*" ollama serve`.
2. Pull a small model: `ollama pull qwen2.5:3b` (echo + 2-digit addition is easy for it).
3. `brew install cloudflared`, then `cloudflared tunnel --url http://localhost:11434 --http-host-header localhost:11434` (Ollama rejects other Host headers).
4. Optional check: `curl -s https://<tunnel>/v1/chat/completions -H 'content-type: application/json' -d '{"model":"qwen2.5:3b","messages":[{"role":"user","content":"What is 12 + 30?"}],"stream":false}'`.
5. Submit `{"url": "https://<tunnel>/v1/chat/completions", "model": "qwen2.5:3b"}`, Check, keep both running until Save.

Gotchas: Browser-side grader: without `OLLAMA_ORIGINS=*` the fetch fails. If the Ollama menu-bar app is running, quit it and run `ollama serve` yourself with the env var. Ollama rejects unknown Host headers; `--http-host-header localhost:11434` fixes it for cloudflared. JSON object with `url` (full path) and `model`, not just a URL.

## Final prompt

```text
Expose a Local LLM through a Tunnel (1 mark)
<paste the full question with your assigned values>
Give me the exact files and terminal commands for macOS (zsh) to satisfy every grader check, including
how to expose it publicly / package it, plus a quick local test for each check.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

See the steps above; code lives in [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-ollama-tunnel-llm-server/src](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-ollama-tunnel-llm-server/src).

## Expected output

Exam **Check** marks the question solved.

## Answer submitted

```
{"url": "https://<random-words>.trycloudflare.com/v1/chat/completions", "model": "qwen2.5:3b"}
```
