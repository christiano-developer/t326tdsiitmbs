"""Run the SQL against the regenerated seeded table and apply the grader's check (col0=department, col1=avg, ±5).
Usage: python3 src/check.py [src/average_salary.sql] [data/employees.json]
"""
import json, sqlite3, sys
sql = open(sys.argv[1] if len(sys.argv) > 1 else "src/average_salary.sql").read()
d = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "data/employees.json"))
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE employees (employee_id INTEGER, name TEXT, department TEXT, salary INTEGER)")
db.executemany("INSERT INTO employees VALUES (?,?,?,?)", [(r["employee_id"], r["name"], r["department"], r["salary"]) for r in d["rows"]])
rows = db.execute(sql).fetchall()
for r in rows: print(r)
got = {r[0]: round(float(r[1])) for r in rows if len(r) >= 2}
ok = all(dep in got and abs(got[dep] - exp) <= 5 for dep, exp in d["expected"].items())
print("expected:", d["expected"]); print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
