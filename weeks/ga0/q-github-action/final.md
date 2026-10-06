# Final — q-github-action

> Goal: the answer can be reproduced from this file alone.

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
