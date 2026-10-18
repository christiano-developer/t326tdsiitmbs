# Prompt log — q-termlog-ollama-modelfile-server

## P1

- **Tool / model:** Claude (Opus 5.5), in chat; commands run by the user in their terminal.
- **Goal:** Heredoc a Modelfile inside the recording, `ollama create`, print it back between markers with `ollama show --modelfile`, exit, tar without macOS metadata, host as a GitHub release asset.
- **Result:** passed after one fix (see approaches.md gotchas).
