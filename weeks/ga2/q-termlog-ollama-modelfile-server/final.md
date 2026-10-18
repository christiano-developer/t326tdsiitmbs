# Final — q-termlog-ollama-modelfile-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-termlog-ollama-modelfile-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-termlog-ollama-modelfile-server)

## How to solve (for a teammate)

Assigned values (tags, IDs, parameters) are **seeded per email**: use the ones on your exam page.

**Approach:** Heredoc a Modelfile inside the recording, `ollama create`, print it back between markers with `ollama show --modelfile`, exit, tar without macOS metadata, host as a GitHub release asset.

1. Install Ollama, start it, pull a small model: `ollama pull qwen2.5:3b` (any small text model works; keep its default template).
2. `termlog login` (exam email), widen the terminal, `termlog rec model.cast`, then inside the recording (your seeded values):

```bash
cat > Modelfile <<'EOF'
FROM qwen2.5:3b
SYSTEM """You are the deployment assistant for project <ID>. Give concise answers and never invent commands."""
PARAMETER temperature <T>
PARAMETER num_ctx <CTX>
PARAMETER seed <SEED>
PARAMETER num_predict <N>
EOF
ollama create ga2-assistant-<ID> -f Modelfile      # wait for "success"
printf '\nMODELFILE_BEGIN ga2-assistant-<ID>\n'
ollama show --modelfile ga2-assistant-<ID>
printf '\nMODELFILE_END ga2-assistant-<ID>\n'
exit
```
3. `COPYFILE_DISABLE=1 tar --no-mac-metadata --no-xattrs -czf submission.tar.gz model.cast model.cast.jwt` (verify with `tar -tzf`).
4. `gh release create <tag-name> submission.tar.gz`; submit `https://github.com/<you>/<repo>/releases/download/<tag-name>/submission.tar.gz`.

Gotchas: Same `atob()` failure as Q1; use `COPYFILE_DISABLE=1 tar --no-mac-metadata --no-xattrs`. Base model `qwen2.5:3b` sets none of the four, so `ollama show` lists each once. Widen the terminal; run the three commands separately. Only the saved config is graded; no inference needed.

## Final prompt

```text
Create a custom Ollama model (termlog) (2 marks)
<paste the full question with your assigned values>
Give me the exact files and terminal commands for macOS (zsh) to satisfy every grader check, including
how to expose it publicly / package it, plus a quick local test for each check.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

See the steps above; code lives in [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-termlog-ollama-modelfile-server/src](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-termlog-ollama-modelfile-server/src).

## Expected output

Exam **Check** marks the question solved.

## Answer submitted

```
https://github.com/<you>/<repo>/releases/download/ga2-termlog-modelfile/submission.tar.gz
```
