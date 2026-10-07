# Deploy guide — q-github-pages

> A static page on GitHub Pages. No secrets, no server.

## Target

| Field         | Value |
|---------------|-------|
| Platform      | GitHub Pages |
| Public URL    | `https://<user>.github.io/<repo>/` |
| Repo / branch | any **public** repo · `main` · `/ (root)` |
| Runtime       | none (static HTML) |
| Required env  | none |

## Prerequisites

- [ ] GitHub account
- [ ] The exam email shown in the question

## 1. Create the page

Put [`src/index.html`](src/index.html) at the repo root with `YOUR-EXAM-EMAIL` and `YOUR-GITHUB-USER` filled in.
The email must stay wrapped in `<!--email_off-->…<!--/email_off-->`.

## 2. Test locally

```bash
grep -c '<exam email>' index.html   # → 1
```

## 3. Deploy

Dashboard-only config:

- Repo → **Settings → Pages → Build and deployment → Source: Deploy from a branch → `main` → `/ (root)` → Save**.
- First deploy takes 1–2 minutes (Actions tab: "pages build and deployment").

## 4. Test deployed URL

```bash
curl -s https://<user>.github.io/<repo>/ | grep '<exam email>'
# What the grader actually fetches:
curl -s "https://exam.sanand.workers.dev/proxy/https://<user>.github.io/<repo>/" | grep -c '<exam email>'
```

- [ ] Email present in the HTML
- [ ] URL host is `github.io`

## 5. Keep alive until graded

- Pages stays up as long as the repo is public and Pages is enabled. Don't rename the repo: the old Pages URL doesn't redirect.

## Teardown (after grading)

Settings → Pages → Unpublish site (or delete the repo).

## Troubleshooting log

| Symptom | Cause | Fix |
|---------|-------|-----|
| 404 right after enabling | first deploy still running | wait for the green Actions run |
| Check fails after an edit | cached page | append `?v=1`, `?v=2` |
| "URL should be hosted on github.io" | custom domain or repo URL submitted | submit the `*.github.io` URL |
