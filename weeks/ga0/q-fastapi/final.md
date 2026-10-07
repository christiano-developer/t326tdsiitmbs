# Final — q-fastapi

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-fastapi](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-fastapi)

## How to solve (for a teammate)

> Values are seeded from your email, and your CSV differs, so deploy your own copy.

Needs Node.js (for `npx`) and a free Vercel account.

1. Create an empty folder `fastapi-app`. Download the CSV from the question into it and rename it `students.csv`.
2. Add `main.py` (copy the code below as-is) and `requirements.txt` containing `fastapi`. Don't add `vercel.json`.
   <details><summary>main.py (click to expand)</summary>

   ```python
   """GET /api - serve students from students.csv, optionally filtered by one or more ?class= values.

   - Order: always the CSV row order (filtering scans rows in file order), never the order of the requested classes.
   - Types: studentId as int, class as str (the grader deep-compares with ===).
   - CORS: GET allowed from any origin.
   """
   import csv
   from pathlib import Path
   from typing import List, Optional

   from fastapi import FastAPI, Query
   from fastapi.middleware.cors import CORSMiddleware

   app = FastAPI()
   app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])

   CSV_PATH = Path(__file__).resolve().parent / "students.csv"
   with CSV_PATH.open(newline="", encoding="utf-8") as f:
       STUDENTS = [{"studentId": int(r["studentId"]), "class": r["class"]} for r in csv.DictReader(f)]


   @app.get("/api")
   def get_students(class_: Optional[List[str]] = Query(None, alias="class")) -> dict:
       if not class_:
           return {"students": STUDENTS}
       wanted = set(class_)
       return {"students": [s for s in STUDENTS if s["class"] in wanted]}


   @app.get("/")
   def health() -> dict:
       return {"status": "ok", "endpoint": "GET /api?class=..."}
   ```

   </details>

3. Deploy: in that folder run `npx vercel login` (once), then `npx vercel --prod --yes`. Copy the URL printed after **Aliased:** (`https://<project>.vercel.app`). Don't use the long unique URL: it returns 401.
4. Test by opening `https://<project>.vercel.app/api?class=<some class from the CSV>` in a browser. You should see `{"students":[...]}`.
5. Submit `https://<project>.vercel.app/api`, then Check and Save.

## Final prompt

```text
Write a FastAPI app (main.py, deployable on Vercel's FastAPI preset) that loads students.csv (studentId,class) at startup
with studentId as int, and serves GET /api -> {"students": [...]} in CSV order. Support repeated ?class= parameters via
List[str] = Query(None, alias="class"), filtering by scanning rows in CSV order. Enable CORS for GET from any origin.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

See [deploy.md](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-fastapi/deploy.md): copy the CSV to [`src/students.csv`](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-fastapi/src/students.csv) → local replay → `npx vercel --prod` → live replay → submit.

## Expected output

```
no filter: all 2000 rows in order + int ids: PASS
100/100 random 4-class rounds passed
```

## Answer submitted (✅ passed, attempt 1)

```
https://tds-ga0-fastapi.vercel.app/api
```
