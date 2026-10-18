# q-mcp-server-live-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 3 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

Deploy a public HTTPS **MCP server** with one tool `solve_challenge` (no required inputs).
On each `tools/call`, read headers `X-Exam-Challenge` (32 hex), `X-Exam-Timestamp`, `X-Exam-Signature`
(HMAC, optional to verify). Return one text block: first 16 hex chars of
`SHA-256("<challenge>:<normalizedEmail>")` (email trimmed + lowercased).
Grader: `initialize` → `notifications/initialized` → `tools/list` → 5 × `solve_challenge`. All 5 must pass.
**Live grading**: keep it up and correct until the deadline.

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

Exam email (normalised). No downloads.

## Final answer

```
https://<your-project>.vercel.app/mcp
```

## Status notes

Checked ✅ on 2026-10-18. **Live grading**: keep the Vercel project `tds-ga1-mcp` up until the GA1 deadline.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [deploy.md](deploy.md) — commands + guide to deploy / boot / configure
- `src/` — code · `data/` — inputs/outputs
