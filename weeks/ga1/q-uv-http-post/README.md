# q-uv-http-post

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 0.5 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-09 |
| Closed    | 2026-10-09 |

## Question

**Case Study: eShopCo API Health Check.** POST a JSON payload to `https://httpbin.org/post` containing
your `email` and a unique `request_id`. Run:

```
uv run --with httpie -- http --json POST https://httpbin.org/post email=<email> request_id=<id>
```

HTTPie returns a JSON object; your payload appears under the `json` field.
Paste the **full** response.

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

`request_id` = 8 hex chars, seeded from `email#q-uv-http-post` (shown on the page).

## Final answer

```
Single-line httpbin JSON body (request_id 20a60e2a); not stored, contains email + IP
```

## Status notes

<!-- Required for set-aside (where I stopped, what's next)
     and cant-approach (the blocker). -->

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
