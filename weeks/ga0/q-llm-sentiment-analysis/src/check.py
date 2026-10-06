"""Offline replica of the GA0 q-llm-sentiment-analysis grader (ported from exam-tds-2026-09-ga0.js).

Installs the exam's mock `httpx` (records the request, returns "GOOD"; no network), runs the submission, then
applies the grader's checks in order. No API calls, no cost.

Usage: python3 src/check.py [src/sentiment.py]
"""
import json
import sys
from pathlib import Path

EXPECTED = "U8jxE atNpVd TsBW qZMGqx7  XJHhTji3 D9cZtLdOsqCgM"  # regenerated from the seed (seedrandom + se(50))


class MockResponse:
    _json = {"choices": [{"message": {"content": "GOOD"}}]}

    def __init__(self, method, url, kwargs):
        self.method, self.url, self.request_kwargs, self.status_code = method, url, kwargs, 200
        self.text = json.dumps(self._json)

    def raise_for_status(self):
        pass

    def json(self):
        return self._json


class MockHttpx:
    def __init__(self):
        self.request = None

    def get(self, url, **kwargs):
        self.request = {"method": "GET", "url": url, "kwargs": kwargs}
        return MockResponse("GET", url, kwargs)

    def post(self, url, json=None, headers=None, **kwargs):  # same signature as the exam's mock
        self.request = {"method": "POST", "url": url, "json": json, "headers": headers}
        return MockResponse("POST", url, kwargs)


mock = MockHttpx()
sys.modules["httpx"] = mock
src = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("sentiment.py")).read_text()
exec(compile(src, "<submission>", "exec"), {"__name__": "__main__"})

r = mock.request or {}
p = r.get("json") or {}
msgs = p.get("messages") or []
content = lambda m: (m.get("content") or "") if isinstance(m.get("content"), str) else (m.get("content") or {}).get("text", "")
checks = [
    ("httpx.post() request made", r.get("method") == "POST"),
    ("URL ends with /v1/chat/completions", str(r.get("url", "")).endswith("/v1/chat/completions")),
    ("Authorization header", bool((r.get("headers") or {}).get("Authorization"))),
    ("JSON body via json=", bool(p)),
    ("model == gpt-4o-mini", p.get("model") == "gpt-4o-mini"),
    ("exactly 2 messages", len(msgs) == 2),
    ("first message role system", len(msgs) > 0 and msgs[0].get("role") == "system"),
    ("second message role user", len(msgs) > 1 and msgs[1].get("role") == "user"),
    ("system mentions GOOD, BAD, NEUTRAL", len(msgs) > 0 and all(w in content(msgs[0]) for w in ("GOOD", "BAD", "NEUTRAL"))),
    ("user message == exact text (after trim)", len(msgs) > 1 and content(msgs[1]).strip() == EXPECTED),
]
for name, ok in checks:
    print(("PASS " if ok else "FAIL ") + name)
sys.exit(0 if all(ok for _, ok in checks) else 1)
