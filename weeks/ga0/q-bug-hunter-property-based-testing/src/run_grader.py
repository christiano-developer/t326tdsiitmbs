"""Local replica of the GA0 bug-hunter grader (ported from exam-tds-2026-09-ga0.js, functions Pa/Ma).

Loads the exam's own Hypothesis shim (data/hypothesis_shim.py), then for each of the buggy and
correct implementations: exec(target) + exec(student) into a fresh namespace, runs every test_*
callable, and applies the exam's verdict rule: PASS only if buggy -> failed AND correct -> passed.

Usage: python3 src/run_grader.py [src/test_dedupe.py]
"""
import json
import re
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "data"))
from variant import BUGGY, CORRECT  # noqa: E402

# Install the exam's shim as the `hypothesis` module (same as the grader's preamble).
exec((HERE / "data/hypothesis_shim.py").read_text(), {"__name__": "__exam_shim__"})

student_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "src/test_dedupe.py"
student_code = student_path.read_text()

# Pre-run text checks from the grader
if not re.search(r"@given\s*\(", student_code):
    sys.exit("FAIL: Your submission must include at least one @given(...) decorator.")
if not re.search(r"\btest_[a-zA-Z0-9_]*\s*\(", student_code):
    sys.exit("FAIL: Define at least one test function whose name starts with test_.")


def run_suite(target_code):
    ns = {"__name__": "__main__"}
    try:
        exec(target_code, ns, ns)
        exec(student_code, ns, ns)
    except Exception as exc:
        return {"status": "error", "error": f"Failed to import/define tests: {exc}",
                "traceback": traceback.format_exc()}
    tests = [(n, v) for n, v in sorted(ns.items()) if callable(v) and n.startswith("test_")]
    if not tests:
        return {"status": "error", "error": "No test function found."}
    if not any(getattr(fn, "_is_exam_given", False) for _, fn in tests):
        return {"status": "error", "error": "At least one test_* function must be decorated with @given(...)."}
    for name, fn in tests:
        try:
            fn()
        except Exception as exc:
            return {"status": "failed", "test": name, "error": str(exc),
                    "counterexample": getattr(exc, "_exam_counterexample", None)}
    return {"status": "passed", "tests": [n for n, _ in tests]}


buggy, correct = run_suite(BUGGY), run_suite(CORRECT)
print("buggy  :", json.dumps(buggy, default=str)[:400])
print("correct:", json.dumps(correct, default=str)[:400])

if buggy["status"] == "error":
    sys.exit(f"FAIL: Test setup error: {buggy['error']}")
if correct["status"] == "error":
    sys.exit(f"FAIL: could not run against the reference function: {correct['error']}")
b_failed, c_failed = buggy["status"] == "failed", correct["status"] == "failed"
if b_failed and not c_failed:
    print("PASS: property fails on buggy code and passes on the reference implementation")
    sys.exit(0)
if not b_failed and not c_failed:
    sys.exit("FAIL: Hypothesis did not discover the bug within 1000 generated examples.")
if b_failed and c_failed:
    sys.exit("FAIL: Your property also fails on the correct implementation.")
sys.exit(f"FAIL: Unexpected outcome. buggy={buggy['status']} correct={correct['status']}")
