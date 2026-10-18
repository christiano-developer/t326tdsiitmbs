# q-local-llm-structured-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 2 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Local LLM Structured-Output Service (2 marks)**

Wrap a local LLM in FastAPI `POST /extract` taking `{"text": "<invoice text>"}` and returning exactly `{"vendor", "amount", "currency", "date"}` (vendor substring match, amount ±0.01, 3-letter uppercase currency, `YYYY-MM-DD` due date). Malformed/empty input must not return 500 (422 or best-effort JSON). Use a Pydantic response model. Grader sends two randomized invoices (planted vendor like `Acme-xxxx Industries Ltd.`, amount 50–9050, USD/EUR/GBP, 2026 date) plus garbage input. Submit the `/extract` URL.

## Inputs / given data

Assigned values are seeded per email (`ROLL_NUMBER@ds.study.iitm.ac.in`) and shown on the exam page.

## Final answer

```
https://<random-words>.trycloudflare.com/extract (cloudflared quick tunnel; changes every run)
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
