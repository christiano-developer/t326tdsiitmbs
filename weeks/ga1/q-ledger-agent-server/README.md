# q-ledger-agent-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 4 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

Acme Appliances has an undocumented order-ledger API (yours alone). Start at
`<exam-origin>/questionData?email=…&quizSign=…&questionId=q-ledger-agent-server&path=/`.
Build a public HTTPS endpoint: `POST {"question": "..."}` → `{"answer": ...}`.
Questions about revenue, refunds, products, customers, e.g. *"What was the total revenue in USD from the North
region in March 2026?"*. Money in USD to the cent; product names as the API spells them.
Graded with several unseen, differently-worded questions; each must be correct within 15 s; stops at first failure.

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

Per-student API at `questionData?…&path=/` (needs `quizSign`). Explore from there.

## Final answer

```
https://<your-project>.vercel.app/
```

## Status notes

Checked ✅ on 2026-10-18 (6/6). Live-graded: keep the Vercel project `tds-ga1-ledger` and its env vars until the deadline.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [deploy.md](deploy.md) — commands + guide to deploy / boot / configure
- `src/` — code · `data/` — inputs/outputs
