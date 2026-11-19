# q-harness-safety-router-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga5 |
| Marks     | 2 |
| Status    | solved (1.98/2) |
| Deploy?   | yes |
| Started   | 2026-11-19 |
| Closed    | 2026-11-19 |

## Question

> **Harness Engineering: Contextual Safety and Model Routing** (2 marks)
>
> Build the safety layer of a hypothetical agent harness. Deploy a public HTTPS POST endpoint. The server selects
> 96 cases from a 2880-case pool for your email and sends 4 batches of 24 (≤ 2 concurrent, 60 s each, 2 MiB).
> Each request carries the authoritative `policy` and `cases` (user messages, environment, memory, repository
> instructions, tool results, optional rollback plan, proposed tool with trusted `resolved` metadata).
> Return per case `requestDecision` (allow/block/review), `toolDecision` (allow/block/review/none),
> `route` (primary/restricted/none), `trajectory` (normal/watch/intervene).
> Grading: 4 axes × 20 % macro-F1 + 20 % exact tuples; > 10 % unsafe approvals on must-block cases caps at 50 %.
> 10 Checks per 24 h (each Check/Save uses one; keep one for Save).

## Inputs / given data

- Policy: the `Ce` object in the exam JS (authority / content / tools / routing).
- Captured batches (this email's 96 cases): [data/batches/](data/batches/) — used as an offline test set.

## Final answer

```
https://<your-project>.vercel.app/classify
```

Check: **94/96 complete decisions correct** (1.98/2). Checks used: 3 of 10 (capture, rules v2, Save).
