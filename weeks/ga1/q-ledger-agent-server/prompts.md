# Prompt log — q-ledger-agent-server

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude (Claude Opus 5.5), Claude desktop app (files on this Mac) + Claude in Chrome (API exploration, tests).
- **Goal:** explore the undocumented API and build the agent.

```text
now Q15
```

- **Result:** exploration from the exam tab: root lists `/orders` (85 pages × 50, `next` links), `/rates`
  (USD per unit: USD, EUR, INR) and `/export` (NDJSON, 4,236 rows, 4,000 unique ids), plus three rules
  (Asia/Kolkata business dates; latest `updated_at` wins per id; only `paid` is revenue). `/export` equals all
  `/orders` pages row for row. Timestamps mix `+05:30` and `Z`. Statuses paid/refunded/void; 5 regions, 8 products.
  Model latency on AI Pipe: gpt-4.1-mini ≈1.5 s (chosen), gpt-5-mini ≈3.3 s.
  Built: LLM → JSON query spec → deterministic executor; offline unit test with synthetic rows passed.
- **Next:** deploy.

---

## P2

- **Tool / model:** same.
- **Goal:** get the deployment working.

```text
(deploy) https://<your-project>.vercel.app
```

- **Result:** two fixes. (1) POST crashed without CORS headers → errors now return JSON. That showed
  `HTTP Error 404` fetching the data: (2) `LEDGER_URL` was pasted as shown on the page, ending `path=/`, so the code
  requested `path=//export`; the base URL is now normalised to end at `path=`. Then 10/10 self-written questions
  matched independent in-browser calculations (all < 4 s). Exam Check: "All 6 questions answered correctly."
- **Next:** none.
