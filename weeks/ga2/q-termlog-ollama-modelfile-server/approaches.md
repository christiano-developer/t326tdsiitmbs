# Approaches — q-termlog-ollama-modelfile-server

## Problem in one line

Heredoc a Modelfile inside the recording, `ollama create`, print it back between markers with `ollama show --modelfile`, exit, tar without macOS metadata, host as a GitHub release asset.

## ⚠️ Distractors, gotchas and hidden text

| Item | Type | Reality |
|------|------|---------|
| macOS tar `._*` files | Gotcha (cost a Check) | Same `atob()` failure as Q1; use `COPYFILE_DISABLE=1 tar --no-mac-metadata --no-xattrs`. |
| "Each assigned parameter must appear once" | Genuine | Base model `qwen2.5:3b` sets none of the four, so `ollama show` lists each once. |
| Marker line wrapping | Genuine | Widen the terminal; run the three commands separately. |
| "not whether an LLM follows a prompt" | Note | Only the saved config is graded; no inference needed. |

Scanned the question HTML for hidden elements/comments: none found.

## Verification

- Exam **Check** passed on 2026-10-18 (run by the user on their Mac; tunnels/recordings are local).
