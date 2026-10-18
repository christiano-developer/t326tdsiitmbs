# q-docker-build-cache-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 1.5 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Diagnose Docker build cache misses (1.5 marks)**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
# L1
COPY requirements.txt ./
# L2
RUN pip install --no-cache-dir -r requirements.txt
# L3
COPY src/ ./src/
# L4
RUN python -m compileall src
# L5
RUN python -m unittest discover -s src
```

Build context: requirements.txt, src/, README.md, Dockerfile. README.md is in .dockerignore. Unchanged build is cached; base digest, platform, build args fixed; no cache mounts. The pip flag affects pip's cache, not Docker's.

Cases (each independent vs the original cached build):

- A. Change the contents of src/app.py.
- B. Change the contents of requirements.txt.
- C. Only change src/app.py's mtime with `touch`.
- D. Change the contents of the excluded README.md.
- E. Change only L4 to `RUN python -m compileall -q src`.

Once a step misses, all later steps run. List steps in build order. Costs: L2 55 s, L4 10 s, L5 15 s; COPY and cache hits 0.

Serve `{"A":{"steps":["L3",...],"seconds":N},...,"E":{...}}` at a public URL (raw JSON). Include zero-cost COPY steps that re-run; empty array for all-cache-hit cases.

## Inputs / given data

Costs are seeded per email: `install = 40 + h%31`, `compile = 10 + h%11`, `test = 15 + h%16` (h = FNV-1a of email). For ROLL_NUMBER: 55 / 10 / 15.

## Final answer

```
https://<your-project>.vercel.app/answer.json
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
