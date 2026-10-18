# Prompt log — q-local-llm-structured-server

## P1

- **Tool / model:** Claude (Opus 5.5), in chat; commands run by the user in their terminal.
- **Goal:** Ollama `/api/chat` with a JSON-schema `format` and temperature 0 picks the fields; the model copies the amount *as written* and code parses it locale-aware and reconciles it with the numbers in the text; Pydantic validates; bad input → 422, LLM down → 503.
- **Result:** passed after one fix (see approaches.md gotchas).
