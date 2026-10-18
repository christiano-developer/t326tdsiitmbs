# Prompt log — q-ollama-tunnel-llm-server

## P1

- **Tool / model:** Claude (Opus 5.5), in chat; commands run by the user in their terminal.
- **Goal:** `OLLAMA_ORIGINS="*" ollama serve` + `cloudflared tunnel --url http://localhost:11434 --http-host-header localhost:11434`; submit the tunnel's `/v1/chat/completions` URL with the model name.
- **Result:** passed first time.
