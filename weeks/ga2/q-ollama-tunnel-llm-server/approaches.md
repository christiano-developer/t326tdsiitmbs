# Approaches — q-ollama-tunnel-llm-server

## Problem in one line

`OLLAMA_ORIGINS="*" ollama serve` + `cloudflared tunnel --url http://localhost:11434 --http-host-header localhost:11434`; submit the tunnel's `/v1/chat/completions` URL with the model name.

## ⚠️ Distractors, gotchas and hidden text

| Item | Type | Reality |
|------|------|---------|
| CORS | Genuine | Browser-side grader: without `OLLAMA_ORIGINS=*` the fetch fails. If the Ollama menu-bar app is running, quit it and run `ollama serve` yourself with the env var. |
| Host header | Gotcha | Ollama rejects unknown Host headers; `--http-host-header localhost:11434` fixes it for cloudflared. |
| Answer format | Genuine | JSON object with `url` (full path) and `model`, not just a URL. |

Scanned the question HTML for hidden elements/comments: none found.

## Verification

- Exam **Check** passed on 2026-10-18 (run by the user on their Mac; tunnels/recordings are local).
