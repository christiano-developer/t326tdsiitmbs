# Prompt log — q-github-action

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** understand the task and how to do it within this repo

```text
Create a GitHub Action
<GitHub Actions background + ISS sample + task: see README.md>
how can i do it within this repo scope
what exactly is it asking me to do
```

- **Result:** read the grader (unauthenticated API, most-recent run only, step-name substring match). Confirmed the repo
  is public with 0 runs and `gh` is logged in. Flagged the invalid example YAML (no `runs-on`). Proposed a
  workflow in this repo with the step name from a repository variable.
- **Next:** approval for the outward-facing steps (variable, push).

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** set it up and trigger it

```text
yes go ahead
```

- **Result:** set `EXAM_EMAIL` via `gh variable set`, added `.github/workflows/ga0-email-step.yml`
  (`name: ${{ vars.EXAM_EMAIL }}`), wrote `src/check_latest_run.sh` (grader replica), committed and pushed `ga0` to
  trigger the run.
- **Next:** verify the latest run with the replica; user submits the repo URL.
