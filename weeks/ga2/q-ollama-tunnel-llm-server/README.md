# q-ollama-tunnel-llm-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 1 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Expose a Local LLM through a Tunnel (1 mark)**

Run Ollama (or any OpenAI-compatible server) so `POST /v1/chat/completions` works at a public tunnel URL with CORS enabled (`OLLAMA_ORIGINS=*`). Grader (from your browser) sends an echo test (repeat `TK<6-hex>`) and an arithmetic test (`What is A + B?`, 10–89). Submit JSON `{"url": "https://…/v1/chat/completions", "model": "<model>"}`.

## Inputs / given data

Assigned values are seeded per email (`ROLL_NUMBER@ds.study.iitm.ac.in`) and shown on the exam page.

## Final answer

```
{"url": "https://<random-words>.trycloudflare.com/v1/chat/completions", "model": "qwen2.5:3b"}
```

## Status notes

<!-- Required for set-aside (where I stopped, what's next)
     and cant-approach (the blocker). -->

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [deploy.md](deploy.md) — commands + guide to deploy / boot / configure
- `src/` — code · `data/` — inputs/outputs
