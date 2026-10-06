# Final — q-fastapi

> Goal: the answer can be reproduced from this file alone.

## Final prompt

```text
Write a FastAPI app (main.py, deployable on Vercel's FastAPI preset) that loads students.csv (studentId,class) at startup
with studentId as int, and serves GET /api -> {"students": [...]} in CSV order. Support repeated ?class= parameters via
List[str] = Query(None, alias="class"), filtering by scanning rows in CSV order. Enable CORS for GET from any origin.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

See [deploy.md](deploy.md): copy the CSV to `src/students.csv` → local replay → `npx vercel --prod` → live replay → submit.

## Expected output

```
no filter: all 2000 rows in order + int ids: PASS
100/100 random 4-class rounds passed
```

## Answer submitted (✅ passed, attempt 1)

```
https://tds-ga0-fastapi.vercel.app/api
```
