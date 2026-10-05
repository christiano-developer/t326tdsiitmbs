# Deploy guide — {{ID}}

> For questions that need a live URL, a running server, or external setup.
> Secrets go in `.env` (git-ignored). Commit `.env.example` with key names only.

## Target

| Field         | Value |
|---------------|-------|
| Platform      | <!-- Vercel / HF Spaces / GitHub Pages / Cloudflare / local + ngrok / Docker --> |
| Public URL    | |
| Repo / branch | |
| Runtime       | <!-- Python 3.12 + uv, Node 22, Docker image ... --> |
| Required env  | <!-- AIPROXY_TOKEN, ... (names only) --> |

## Prerequisites

- [ ] Accounts: <!-- GitHub, Vercel, HF ... -->
- [ ] CLIs installed: <!-- gh, vercel, docker, uv, ollama ... --> (check with `--version`)
- [ ] Logged in: <!-- `gh auth login`, `vercel login` -->
- [ ] `.env` filled from `.env.example`

## 1. Run locally

```bash
cd src
uv run ...            # start server
```

## 2. Test locally

```bash
curl -s "http://localhost:8000/..." | jq
```

Expected:

```json
```

## 3. Deploy

```bash
# e.g. vercel --prod
```

Dashboard-only config (not captured by commands):

- <!-- e.g. Vercel → Settings → Environment Variables → AIPROXY_TOKEN -->

## 4. Test deployed URL

```bash
curl -s "https://<url>/..." | jq
```

- [ ] Returns expected output
- [ ] CORS allows `*` (if the grader calls from a browser)
- [ ] Works from a fresh terminal / incognito (no local state)

## 5. Keep alive until graded

- <!-- free tiers sleep/expire: note the deadline and when teardown is safe -->

## Teardown (after grading)

```bash
```

## Troubleshooting log

| Symptom | Cause | Fix |
|---------|-------|-----|
