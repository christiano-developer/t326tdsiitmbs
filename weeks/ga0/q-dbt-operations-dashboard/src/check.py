"""Local replica of the GA0 dbt grader (ported from exam-tds-2026-09-ga0.js) for this variant:
intermediate model, daily grain, metric percent_refunded, business term "return", 14 days.

Usage: python3 src/check.py src/int_returns_daily.sql
Checks run in the grader's order; the first failure is the error the exam would show.
"""
import re
import sys

sql = open(sys.argv[1]).read().strip()
low = sql.lower()

checks = [
    ("non-empty", bool(sql)),
    ("uses Jinja {{ }}", "{{" in sql),
    ("intermediate: {{ ref(", bool(re.search(r"{{\s*ref\(", sql, re.I))),
    ("intermediate: CTE (with)", bool(re.search(r"\bwith\b", sql, re.I))),
    ("daily: date_trunc('day' or ::date",
     bool(re.search(r"date_trunc\s*\(\s*'day'", sql, re.I) or re.search(r"\b::date\b", sql, re.I))),
    ("percent_refunded logic: sum|refund|amount", any(p in low for p in ["sum", "refund", "amount"])),
    ("business term 'return'", "return" in low),
    # '.' does not cross newlines: the WHERE condition must be on ONE line with a standalone word 'date'
    ("14-day filter: where ... \\bdate\\b ... >=|between (single line)",
     bool(re.search(r"where\s+.+\bdate\b.+(>=|between)", sql, re.I))),
    ("SELECT and FROM", bool(re.search("select", sql, re.I) and re.search("from", sql, re.I))),
    ("NULL handling: coalesce|ifnull|0)", bool(re.search(r"coalesce|ifnull|0\)", sql, re.I))),
    ("{{ config(", bool(re.search(r"{{\s*config\s*\(", sql, re.I))),
]
for name, ok in checks:
    print(("PASS " if ok else "FAIL ") + name)
sys.exit(0 if all(ok for _, ok in checks) else 1)
