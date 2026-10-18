# q-termlog-ollama-modelfile-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 2 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Create a custom Ollama model (termlog) (2 marks)**

Inside a signed `termlog rec model.cast` recording, write a Modelfile (FROM a small local model with its default template, SYSTEM, PARAMETER) for model `ga2-assistant-48c9d2a0` with exact values `temperature 0.2, num_ctx 2048, seed 428, num_predict 72` and SYSTEM `You are the deployment assistant for project 48c9d2a0. Give concise answers and never invent commands.` (all seeded per email). Run `ollama create … -f Modelfile`, then individually `printf` a MODELFILE_BEGIN marker, `ollama show --modelfile …`, a MODELFILE_END marker (markers on their own lines), `exit`, tar `model.cast model.cast.jwt`, submit a public URL. Each assigned parameter must appear once.

## Inputs / given data

Assigned values are seeded per email (`ROLL_NUMBER@ds.study.iitm.ac.in`) and shown on the exam page.

## Final answer

```
https://github.com/<you>/<repo>/releases/download/ga2-termlog-modelfile/submission.tar.gz
```

## Status notes

<!-- Required for set-aside (where I stopped, what's next)
     and cant-approach (the blocker). -->

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
