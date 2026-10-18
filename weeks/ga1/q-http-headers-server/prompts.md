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

---

## P2 (2026-10-18)

- **Tool / model:** Claude (Claude Opus 5.5) via Claude in Chrome.
- **Goal:** keep a valid code on the page until the GA is re-saved.

```text
(redo the solved questions in Chrome; refresh the hourly code before saving)
```

- **Result:** worked. Fetched the header from inside the exam tab (`fetch(url).headers.get('x-exam-code')`, same
  origin, no curl needed): `5ZCFF24A` → `X2AWMU92` → `VPATUKMK` as the UTC hour rolled over; each passed Check.
- **Next:** none.
