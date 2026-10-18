# Prompt log — q-uv-http-post

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** the httpbin echo of {email, request_id} in the form the grader parses.

```text
Compute my seeded request_id from the quiz JS, POST it with my email to httpbin.org/post, and give me the
body only as single-line JSON (the grader JSON.parses the answer).
```

- **Result:** worked. uv/HTTPie weren't installed, so the POST used `curl --json` (httpbin echoes the same fields). Grader logic was checked locally, and it passed on attempt 1.
- **Next:** none.
