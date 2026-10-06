# q-fastapi

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes (Vercel) |
| Started   | 2026-10-07 |
| Closed    | 2026-10-07 (passed on attempt 1) |

## Question

**Write a FastAPI server to serve data**: background: *Web Framework: FastAPI*, *REST APIs*, *CORS*.

> The CSV has 2 columns: `studentId` and `class` (e.g. 1A … 12Z). Write a FastAPI server that serves this data:
> `/api` returns all students (same row and column order as the CSV) as `{"students": [{"studentId": 1, "class": "1A"}, …]}`.
> With query parameter `class`, return only students in those classes: `/api?class=1A`, `/api?class=1A&class=1B`, any number
> of classes, in CSV order (not the order of the classes). Enable CORS for GET from any origin.
> What is the API URL endpoint? (e.g. `http://127.0.0.1:8000/api`). We'll request it with `?class=…` added.

Per-user variant: 2,000 students / 312 classes seeded from the student email.

## Inputs / given data

- [data/q-fastapi.csv](data/q-fastapi.csv): downloaded CSV (bundled for deploy as [src/students.csv](src/students.csv)).

## Final answer

```
https://tds-ga0-fastapi.vercel.app/api
```

## Status notes

- Local 200/200 and live 100/100 random 4-class rounds pass; CORS `*`. Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) · [approaches.md](approaches.md) · [final.md](final.md) · [deploy.md](deploy.md)
- [src/main.py](src/main.py) — FastAPI app · [src/test_api.py](src/test_api.py) — grader replay
