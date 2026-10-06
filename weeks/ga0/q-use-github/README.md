# q-use-github

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no (file pushed to this public repo) |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 |

## Question

**Use GitHub**: background: *Version Control: Git, GitHub* (essential commands, commit-message format, branching
strategy, code review, tools).

> Create a GitHub account if you don't have one. Create a new public repository. Commit a single JSON file called
> `email.json` with the value `{"email": "<my-exam-email>"}` and push it.
>
> Enter the raw GitHub URL of email.json so we can verify it. (It will begin with
> `https://raw.githubusercontent.com/[GITHUB ID]/[REPO NAME]/...`.)

## Inputs / given data

- [email.json](email.json): `{"email": "<exam email>"}` (the real address; the grader reads this file).

## Final answer

Pinned to the commit that adds the file (immutable, survives branch merges/deletions):

```
https://raw.githubusercontent.com/christiano-developer/t326tdsiitmbs/<commit-sha>/weeks/ga0/q-use-github/email.json
```

`<commit-sha>` = the `solved(ga0/q-use-github)` commit (tag `ga0/q-use-github/solved`): `git rev-parse ga0/q-use-github/solved^{commit}`.
Branch form (works while `ga0` exists): `https://raw.githubusercontent.com/christiano-developer/t326tdsiitmbs/ga0/weeks/ga0/q-use-github/email.json`.

## Status notes

- Verified with `src/check_raw_url.sh` after pushing (same checks as the grader).

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [email.json](email.json) — the file the grader fetches
- [src/check_raw_url.sh](src/check_raw_url.sh) — the grader's check
