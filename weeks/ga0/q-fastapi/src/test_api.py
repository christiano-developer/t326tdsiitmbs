"""Replay the grader: N rounds of 4 random classes, deep-compare response.students with the CSV (order + types).
Usage: python3 src/test_api.py [api_url] [rounds]   (default http://127.0.0.1:8000/api, 50)
"""
import csv, json, random, sys, urllib.parse, urllib.request
from pathlib import Path

url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/api"
rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 50
rows = [{"studentId": int(r["studentId"]), "class": r["class"]}
        for r in csv.DictReader(open(Path(__file__).resolve().parent / "students.csv", newline=""))]
classes = sorted({r["class"] for r in rows})

def get(q):
    req = urllib.request.Request(url + ("?" + q if q else ""), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

ok = get("")["students"] == rows
print("no filter: all", len(rows), "rows in order + int ids:", "PASS" if ok else "FAIL")
fails = 0
for _ in range(rounds):
    pick = random.sample(classes, 4)
    got = get(urllib.parse.urlencode([("class", c) for c in pick]))["students"]
    exp = [r for r in rows if r["class"] in pick]
    if got != exp or any(type(g["studentId"]) is not int for g in got):
        fails += 1; print("FAIL", pick, len(got), "vs", len(exp))
print(f"{rounds - fails}/{rounds} random 4-class rounds passed")
sys.exit(0 if ok and not fails else 1)
