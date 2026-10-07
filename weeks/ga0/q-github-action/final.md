# Final — q-github-action

> Goal: the answer can be reproduced from this file alone.

## How to solve (for a teammate)

> Values are seeded from your email, so use your own email and repo.

Needs a GitHub account, a public repo cloned on your machine, and the `gh` CLI (`gh auth login`).

1. In the repo folder, store your email as a repo variable:
   ```bash
   gh variable set EXAM_EMAIL --body "you@example.com"
   ```
2. Create `.github/workflows/ga0-email-step.yml` with this content (change `main` to your branch):
   ```yaml
   name: GA0 email step
   on:
     push:
       branches: [main]
     workflow_dispatch:
   jobs:
     ga0-email:
       runs-on: ubuntu-latest
       steps:
         - name: ${{ vars.EXAM_EMAIL }}
           run: echo "Hello, world!"
   ```
3. Commit and push: `git add .github && git commit -m "add workflow" && git push`.
4. On GitHub, open the **Actions** tab. Wait for a green run whose step is named with your email.
5. Submit `https://github.com/<your-user>/<your-repo>`, then Check and Save.

## Final prompt

```text
Create a minimal GitHub Actions workflow file for a public repo. It must have runs-on: ubuntu-latest, trigger on
push to branch <BRANCH> and workflow_dispatch, and contain one step whose name is ${{ vars.EXAM_EMAIL }} and which
runs echo "Hello, world!". Also give the gh commands to set the EXAM_EMAIL repository variable, trigger the
workflow, and check that the most recent run's step names contain the email via the public GitHub API.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

Follow [deploy.md](deploy.md):

1. `gh variable set EXAM_EMAIL --body "<my-exam-email>"`.
2. Add `.github/workflows/ga0-email-step.yml` (see `src/ga0-email-step.yml`).
3. Commit and `git push origin ga0`, which triggers the run.
4. `src/check_latest_run.sh christiano-developer/t326tdsiitmbs "<my-exam-email>"` → PASS.
5. Submit the repo URL.

## Expected output

```
latest run: <id> GA0 email step ga0 completed success <timestamp>
step names: ['Set up job', '<email>', 'Complete job']
PASS: a step name contains the email
```

## Answer submitted

```
https://github.com/christiano-developer/t326tdsiitmbs
```
