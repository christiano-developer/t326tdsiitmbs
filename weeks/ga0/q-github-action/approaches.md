# Approaches — q-github-action

## Problem in one line

Have the most recent GitHub Actions run of a public repo include a step whose name contains the exam email.

## Grader (from quiz JS)

1. The URL must match `https://github.com/<user>/<repo>`.
2. `GET https://api.github.com/repos/<user>/<repo>/actions/runs` (**unauthenticated**, so the repo must be public).
3. Takes **only `workflow_runs[0]`** (most recent). Errors with "No runs found" if empty.
4. Fetches its `jobs_url`. Passes if any `steps[].name` **contains** the email. Otherwise errors with "No step matches <email>".

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Example YAML in the question | **Distractor** | The job has **no `runs-on:`**, which makes it an invalid workflow. Copied as-is, nothing runs |
| ISS sample workflow | Background (buggy) | Ends its heredoc with `'EOF'` in quotes (wouldn't terminate). Not needed |
| "make sure it is the most recent action" | Genuine | Any later run of **any** workflow in the repo replaces it in `workflow_runs[0]` |
| Step-name must "contain" the email | Note | Substring match, so extra text around it is fine |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Pros | Cons | Verdict |
|---|----------|------|------|---------|
| A | Hard-code the email in the step name | Simplest | Commits the email into a public repo's files and history | rejected |
| B | **Step name `${{ vars.EXAM_EMAIL }}` from a repository variable, in this repo** | Email not in files/history; the API returns the evaluated name; uses an existing public repo with 0 runs | The run itself is public, so the email is visible in the run UI/API (unavoidable: the grader reads it there) | **chosen** |
| C | A separate throwaway repo | Keeps this repo's Actions history clean | Another repo to manage | offered, not chosen |

## Chosen: B

**Why:** works within this repo, and keeps the email out of committed files. Triggers: `push` to `ga0` (the push of this
commit starts the run) and `workflow_dispatch` (manual re-runs once the file is on `main`).

## Gotchas

- `.github/workflows/` is the only place GitHub reads workflows, so this is the one file outside the question folder.
- Every later push to `ga0` re-runs this workflow. The newest run still has the email step, so it stays passing.
- If `EXAM_EMAIL` is missing, the step name renders empty (GitHub then shows `Run echo …`), so check passes fail.

## Verification

- `src/check_latest_run.sh christiano-developer/t326tdsiitmbs <exam-email>` reproduces the grader against the live API.
- Exam "Check" button: see Status / prompts.md.
