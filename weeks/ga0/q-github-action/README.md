# q-github-action

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes (GitHub Actions run + repository variable) |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 |

## Question

**Create a GitHub Action**: background: *CI/CD: GitHub Actions* (YAML, marketplace actions, secrets, triggers, free
tier, caching), with a sample daily ISS-location workflow and tools (gh CLI, Super-Linter, Release Drafter, act).

> Create a GitHub action on one of your GitHub repositories. Make sure one of the steps in the action has a name that
> contains your email address `<my-exam-email>`. For example:
>
> ```yaml
> jobs:
>   test:
>     steps:
>       - name: <my-exam-email>
>         run: echo "Hello, world!"
> ```
>
> Trigger the action and make sure it is the most recent action.
>
> What is your repository URL? It will look like: https://github.com/USER/REPO

## Inputs / given data

- Repo: this one (public, default branch `main`).
- Repository variable `EXAM_EMAIL` (set with `gh variable set`) holds the email, so it isn't committed.

## Final answer

```
https://github.com/christiano-developer/t326tdsiitmbs
```

Workflow: [`.github/workflows/ga0-email-step.yml`](../../../.github/workflows/ga0-email-step.yml)
(copy in [src/ga0-email-step.yml](src/ga0-email-step.yml)). It runs on every push to `ga0` and on manual dispatch.

## Status notes

- The run is triggered by pushing the commit that adds the workflow. Verify with the grader's own API logic (deploy.md §4).
- **Keep it the most recent run:** later pushes to `ga0` re-run this same workflow (still passes). Don't add other
  workflows that run after it until GA0 is graded.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [deploy.md](deploy.md) — commands + guide: variable, workflow, trigger, verify, teardown
- [src/ga0-email-step.yml](src/ga0-email-step.yml) — copy of the workflow
- [src/check_latest_run.sh](src/check_latest_run.sh) — the grader's check, via the public API
