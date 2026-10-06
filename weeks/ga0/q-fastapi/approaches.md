# Approaches — q-fastapi

## Problem in one line

Public `GET /api` returning the CSV as `{"students": [...]}`, filterable by repeated `?class=`, CSV order, CORS `*`.

## Grader (from quiz JS)

- Data: `seedrandom(email#q-fastapi)` → 2,000 students (the downloaded CSV is that data; 312 distinct classes here).
- Picks **4 random classes** (`Math.random`, so a new set every Check), fetches `<URL>?class=a&class=b&class=c&class=d`
  (the URL is used **exactly as submitted**, so it must include `/api`).
- Deep-compares `response.students` with the expected rows: same length, same order, and `===` on every value
  (`studentId` must be a **number**).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Example answer `http://127.0.0.1:8000/api` | **Trap** | An https exam page calling localhost can be blocked by Chrome's Private Network Access, and it needs the laptop server running. Deployed to Vercel instead |
| Repeated `?class=` | Trap | A plain `str` param keeps only one value. Use `List[str] = Query(None, alias="class")` (`class` is a Python keyword) |
| CSV values are strings | Trap | `studentId` must be an int (strict `===` compare) |
| "order of the classes" | Trap | Return CSV order; filter by scanning rows |
| REST/CORS background (items API, pagination, versioning) | Background | Not checked |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | Local uvicorn + submit `http://127.0.0.1:8000/api` | risky (PNA), and must stay running |
| B | **Vercel project `tds-ga0-fastapi` (same pattern as q-code-interpreter: `main.py`, no `vercel.json`), CSV bundled** | **chosen** |

## Verification

- `src/test_api.py` local → full list PASS + **200/200** random 4-class rounds; CORS `*`.
- Live `https://tds-ga0-fastapi.vercel.app/api` → full list PASS + **100/100**; CORS `*`.
- Exam "Check": ✅ passed on attempt 1 (2026-10-07).
