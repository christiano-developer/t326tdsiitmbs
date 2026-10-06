# Prompt log — q-use-github

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** understand the task; check whether a new repo is really needed

```text
Use GitHub
<Git/GitHub background + task: see README.md>
what do i got to do here, note i already have a GH account, do i really have to create a new repo ? or can we do it of this
```

- **Result:** read the grader (host check + exact email match on fetched JSON only), so a new repo isn't needed.
  Proposed `email.json` in this repo with a commit-pinned raw URL; flagged that the email will be in a committed file.
- **Next:** approval to commit and push.

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** commit, push, verify

```text
yes go ahead
```

- **Result:** wrote `email.json`, committed and pushed `ga0`, built the commit-SHA raw URL, verified with `src/check_raw_url.sh`.
- **Next:** user submits the URL.
