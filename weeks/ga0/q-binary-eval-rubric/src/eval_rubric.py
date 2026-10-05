"""Local replica of the GA0 binary-eval-rubric grader (ported from exam-tds-2026-09-ga0.js).

Runs each rubric check against the 20 hidden examples with the SAME judge as the exam
(gpt-4.1-mini via AIPipe, temperature 0, same system/user prompt), then applies the same
pass rule: Pearson corr(pred, label) > 0.7 and not degenerate; >= 4 checks must pass.

Usage:
  python3 src/eval_rubric.py --validate            # format checks only, no API calls
  AIPIPE_TOKEN=... python3 src/eval_rubric.py      # full run: 5 x 20 = 100 AIPipe calls
Options:
  --rubric PATH     default src/rubric.txt
  --examples PATH   default data/hidden_examples.json
  --out PATH        write per-example predictions as JSON (default data/eval_results.json)
Token is read from $AIPIPE_TOKEN or from a git-ignored .env file next to this folder.
"""
import argparse
import json
import math
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # question folder
URL = "https://aipipe.org/openai/v1/chat/completions"
REQUIRED_CHECKS = 5  # this student's variant (seeded from email); grader picks 5, 6 or 7
CONCURRENCY = 8      # same as the exam


def load_token():
    tok = os.environ.get("AIPIPE_TOKEN", "").strip()
    env = HERE / ".env"
    if not tok and env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("AIPIPE_TOKEN="):
                tok = line.split("=", 1)[1].strip().strip('"').strip("'")
    return tok


def validate(checks):
    """Pre-API format rules from the grader. Raises ValueError with the grader's message."""
    if len(checks) != REQUIRED_CHECKS:
        raise ValueError(f"You must submit exactly {REQUIRED_CHECKS} binary checks, one per line. You submitted {len(checks)}.")
    for i, c in enumerate(checks, 1):
        if not c.endswith("?"):
            raise ValueError(f"Line {i} must end with '?'.")
        if len(c) < 24:
            raise ValueError(f"Line {i} is too short. Write a complete, specific question.")
    if len({c.lower() for c in checks}) != len(checks):
        raise ValueError("Duplicate checks detected. Each line must be meaningfully different.")


def judge(check, output, judge_cfg, token):
    """One judge call. Mirrors the exam: retry once on HTTP error, YES->1, NO->0."""
    body = json.dumps({
        "model": judge_cfg["model"],
        "temperature": 0,
        "messages": [
            {"role": "system", "content": judge_cfg["system"]},
            {"role": "user", "content": judge_cfg["user_template"].format(check=check, output=output)},
        ],
    }).encode()
    for attempt in range(2):
        req = urllib.request.Request(URL, data=body, headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                text = (json.load(r)["choices"][0]["message"]["content"] or "").strip().upper()
        except urllib.error.HTTPError as e:
            if attempt == 0:
                continue
            raise RuntimeError(f"AIPipe judge call failed ({e.code}): {e.read()[:200]!r}")
        if text.startswith("YES"):
            return 1
        if text.startswith("NO"):
            return 0
        if attempt == 1:
            raise RuntimeError(f"Judge returned non-binary output: {text!r}")
    return 0


def pearson(a, b):
    """Same as the exam's correlation (0 when either side has zero variance)."""
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    return 0.0 if va == 0 or vb == 0 else cov / math.sqrt(va * vb)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rubric", default=str(HERE / "src/rubric.txt"))
    ap.add_argument("--examples", default=str(HERE / "data/hidden_examples.json"))
    ap.add_argument("--out", default=str(HERE / "data/eval_results.json"))
    ap.add_argument("--validate", action="store_true", help="format checks only, no API calls")
    args = ap.parse_args()

    checks = [l.strip() for l in Path(args.rubric).read_text().splitlines() if l.strip()]
    validate(checks)
    print(f"Format OK: {len(checks)} checks")
    if args.validate:
        return 0

    data = json.loads(Path(args.examples).read_text())
    examples, judge_cfg = data["hiddenExamples"], data["judge"]
    labels = [e["label"] for e in examples]
    token = load_token()
    if not token:
        sys.exit("Set AIPIPE_TOKEN (env or .env) to run the judge.")

    jobs = [(ci, ei) for ci in range(len(checks)) for ei in range(len(examples))]
    print(f"Running {len(jobs)} judge calls ({CONCURRENCY} in parallel)...")
    with ThreadPoolExecutor(CONCURRENCY) as pool:
        preds = list(pool.map(lambda j: judge(checks[j[0]], examples[j[1]]["output"], judge_cfg, token), jobs))

    matrix = [[0] * len(examples) for _ in checks]
    for (ci, ei), p in zip(jobs, preds):
        matrix[ci][ei] = p

    results, passed = [], 0
    for ci, check in enumerate(checks):
        row = matrix[ci]
        degenerate = all(row) or not any(row)
        corr = pearson(row, labels)
        ok = not degenerate and corr > 0.7
        passed += ok
        misses = [examples[i]["id"] for i in range(len(row)) if row[i] != labels[i]]
        results.append({"check": check, "corr": round(corr, 3), "degenerate": degenerate,
                        "yesRate": sum(row) / len(row), "pass": ok, "mismatched_example_ids": misses,
                        "preds": row})
        print(f"#{ci+1} {'PASS' if ok else 'FAIL'} corr={corr:.2f} yes={sum(row)}/{len(row)} "
              f"mismatches={misses or '-'}\n    {check}")

    verdict = passed >= 4
    print(f"\n{passed}/{len(checks)} checks passed -> {'PASS' if verdict else 'FAIL'} (need >= 4)")
    Path(args.out).write_text(json.dumps({"passed": passed, "verdict": verdict, "checks": results}, indent=2))
    print(f"Saved per-example predictions to {args.out}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
