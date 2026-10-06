"""Replay the grader: N rounds of 10 random bank sentences in one POST; need >= 7 correct, order + echo exact.
Usage: python3 src/test_api.py [sentiment_url] [rounds]   (default http://127.0.0.1:8002/sentiment, 50)
"""
import json, random, sys, urllib.request
from pathlib import Path

url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8002/sentiment"
rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 50
bank = json.loads((Path(__file__).resolve().parent.parent / "data/grader_sentences.json").read_text())
worst = 10
for _ in range(rounds):
    pick = random.sample(bank, 10)
    req = urllib.request.Request(url, data=json.dumps({"sentences": [p["text"] for p in pick]}).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)["results"]
    assert len(res) == 10 and all(res[i]["sentence"] == pick[i]["text"] for i in range(10)), "order/echo broken"
    worst = min(worst, sum(res[i]["sentiment"].strip().lower() == pick[i]["sentiment"] for i in range(10)))
print(f"{rounds} rounds, worst score {worst}/10 -> {'PASS' if worst >= 7 else 'FAIL'}")
sys.exit(0 if worst >= 7 else 1)
