# Prompt log — q-http-headers-server

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** read the hourly X-Exam-Code header.

```text
Find the code in the response headers: curl -i "<questionData URL with quizSign>"
```

- **Result:** worked. `x-exam-code: NNUEPJHP`; the body was plain text with no injected instructions. Submitted 3 min before the hour rolled over and passed on attempt 1.
- **Next:** none.
