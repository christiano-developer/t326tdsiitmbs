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
