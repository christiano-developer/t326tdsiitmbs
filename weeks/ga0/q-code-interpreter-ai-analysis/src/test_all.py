"""Run all 60 grader tests (data/grader_tests.json) against an endpoint, with the grader's exact checks.
Usage: python3 src/test_all.py [base_url]   (default http://127.0.0.1:8000)
"""
import json, sys, urllib.request
from pathlib import Path

base = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")
url = base if base.endswith("/code-interpreter") else base + "/code-interpreter"
tests = json.loads((Path(__file__).resolve().parent.parent / "data/grader_tests.json").read_text())
mine = {43, 36, 10}  # this student's 3 seeded tests
fails = 0
for t in tests:
    req = urllib.request.Request(url, data=json.dumps({"code": t["code"]}).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        ctype = r.headers.get("content-type", ""); y = json.load(r)
    ok = "application/json" in ctype and isinstance(y.get("error"), list) and isinstance(y.get("result"), str)
    if t["hasError"]:
        ok = ok and sorted(y["error"]) == sorted(t["errorLines"]) and ("Traceback" in y["result"] or "Error" in y["result"])
    else:
        ok = ok and y["error"] == [] and y["result"] == t["expectedOutput"]
    fails += not ok
    if not ok or t["id"] in mine:
        print(f"{'PASS' if ok else 'FAIL'} #{t['id']:>2}{' (yours)' if t['id'] in mine else ''} "
              f"expected={t.get('errorLines') if t['hasError'] else repr(t['expectedOutput'])} got_error={y.get('error')}"
              + ("" if ok else f" result={y.get('result')!r:.120}"))
print(f"\n{len(tests) - fails}/{len(tests)} passed")
sys.exit(1 if fails else 0)
