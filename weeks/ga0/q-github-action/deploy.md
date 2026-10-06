# Deploy guide — q-github-action

> No secrets are needed. The email is a (non-secret) repository *variable*, not committed to the repo.

## Target

| Field         | Value |
|---------------|-------|
| Platform      | GitHub Actions |
| Public URL    | https://github.com/christiano-developer/t326tdsiitmbs/actions |
| Repo / branch | `christiano-developer/t326tdsiitmbs`, branch `ga0` |
| Runtime       | `ubuntu-latest` runner |
| Required env  | Repository variable `EXAM_EMAIL` |

## Prerequisites

- [x] Repo is **public** (the grader calls the API unauthenticated): `gh repo view --json visibility`
- [x] `gh` installed and logged in: `gh auth status`

## 1. Set the repository variable

```bash
gh variable set EXAM_EMAIL --body "<my-exam-email>" --repo christiano-developer/t326tdsiitmbs
gh variable list --repo christiano-developer/t326tdsiitmbs
```

Dashboard equivalent: repo → Settings → Secrets and variables → Actions → **Variables** → New repository variable.

## 2. Add the workflow

`.github/workflows/ga0-email-step.yml`:

```yaml
name: GA0 email step
on:
  push:
    branches: [ga0]
  workflow_dispatch:
jobs:
  ga0-email:
    runs-on: ubuntu-latest
    steps:
      - name: ${{ vars.EXAM_EMAIL }}
        run: echo "Hello, world!"
```

## 3. Trigger

```bash
git add .github/workflows/ga0-email-step.yml && git commit ... && git push origin ga0   # push trigger
# or, once the file is on the default branch:
gh workflow run ga0-email-step.yml --repo christiano-developer/t326tdsiitmbs
gh run list --repo christiano-developer/t326tdsiitmbs --limit 3
gh run watch --repo christiano-developer/t326tdsiitmbs        # wait for it to finish
```

## 4. Verify (same logic as the grader)

```bash
weeks/ga0/q-github-action/src/check_latest_run.sh christiano-developer/t326tdsiitmbs "<my-exam-email>"
```

- [ ] `latest run:` is the GA0 email step run
- [ ] `PASS: a step name contains the email`

## 5. Keep alive until graded

- Don't trigger runs of **other** workflows in this repo until GA0 is graded (Oct 11, 2026).
- Re-runs of this workflow are fine.

## Teardown (after grading)

```bash
gh variable delete EXAM_EMAIL --repo christiano-developer/t326tdsiitmbs
gh workflow disable ga0-email-step.yml --repo christiano-developer/t326tdsiitmbs   # optional
```

## Troubleshooting log

| Symptom | Cause | Fix |
|---------|-------|-----|
| "No runs found" | Workflow never triggered / invalid YAML (e.g. missing `runs-on`) | Check the Actions tab; validate YAML |
| "No step matches" | Variable missing (empty step name), or another workflow ran later | `gh variable list`; re-run this workflow |
