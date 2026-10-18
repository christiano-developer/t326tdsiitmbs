# Prompt log — q-npx-prettier

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** the SHA-256 of prettier 3.4.2's output for the seeded README.md.

```text
Rebuild the seeded README.md from the quiz JS for my email, run npx -y prettier@3.4.2 README.md | shasum -a 256.
```

- **Result:** worked. The CLI hash matched the prettier Node API hash (what the browser grader computes). Passed on attempt 1.
- **Next:** none.
