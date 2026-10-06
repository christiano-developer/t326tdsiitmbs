# Prompt log — q-fastapi

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** scaffold; user adds the CSV

```text
Write a FastAPI server to serve data
<FastAPI / REST / CORS background + task: see README.md>
scaffold then ill add the csv
```

- **Result:** scaffolded. Read the grader (4 random classes per Check, URL used as-is, strict deep compare incl. int ids).
  Flagged the repeated-param, int-type, CSV-order and localhost/PNA traps.
- **Next:** user adds the CSV.

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** build, test, deploy

```text
sure proceed
added the csv
```

- **Result:** 2,000 rows / 312 classes. `src/main.py` (int ids, `List[str]` alias `class`, CSV-order filter, CORS) + bundled CSV.
  Local replay 200/200; deployed to Vercel `tds-ga0-fastapi`; live replay 100/100; CORS `*`.
- **Next:** user submits `https://tds-ga0-fastapi.vercel.app/api`.

---

## P3

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** record the result

```text
correct
```

- **Result:** ✅ passed on the first submission. Status → `solved`, committed and tagged. Keep the Vercel project up until grading closes.
- **Next:** none.
