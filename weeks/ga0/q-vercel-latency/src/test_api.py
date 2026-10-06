"""Compare an endpoint with the grader's exact JS formulas (computed by node from telemetry.json).
Usage: python3 src/test_api.py [url]   (default http://127.0.0.1:8003/)
Checks the grader's request ({"regions":["apac","amer"],"threshold_ms":174}) plus extra thresholds/regions, with the
grader's tolerances (avg/p95 +-0.5, uptime +-0.2, breaches exact) and the Access-Control-Allow-Origin header.
"""
import json, subprocess, sys, urllib.request
from pathlib import Path

url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8003/"
data = Path(__file__).resolve().parent / "telemetry.json"
JS = r"""
const l = JSON.parse(require('fs').readFileSync(process.argv[1], 'utf8')), s = JSON.parse(process.argv[2]);
function ns(t,o){let e=[...t].sort((s,a)=>s-a),r=(e.length-1)*o,n=Math.floor(r),q=r-n;return e[n+1]!==void 0?e[n]+q*(e[n+1]-e[n]):e[n]}
console.log(JSON.stringify(s.regions.map(d=>{let m=l.filter(f=>f.region===d),p=m.map(f=>f.latency_ms),h=m.map(f=>f.uptime_pct),
g=m.filter(f=>f.latency_ms>s.threshold_ms).length;return{region:d,avg_latency:Number((p.reduce((f,y)=>f+y,0)/p.length).toFixed(2)),
p95_latency:Number(ns(p,.95).toFixed(2)),avg_uptime:Number((h.reduce((f,y)=>f+y,0)/h.length).toFixed(3)),breaches:g}})));
"""
cases = [{"regions": ["apac", "amer"], "threshold_ms": 174}] + \
        [{"regions": ["apac", "emea", "amer"], "threshold_ms": t} for t in (150, 160, 170, 180, 190, 230.89)]
bad = 0
for c in cases:
    exp = json.loads(subprocess.run(["node", "-e", JS, str(data), json.dumps(c)], capture_output=True, text=True, check=True).stdout)
    req = urllib.request.Request(url, data=json.dumps(c).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "Origin": "https://exam.sanand.workers.dev",
                                          "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        acao = r.headers.get("access-control-allow-origin"); got = {x["region"]: x for x in json.load(r)["regions"]}
    for e in exp:
        g = got.get(e["region"], {})
        ok = (abs(g.get("avg_latency", 1e9) - e["avg_latency"]) <= .5 and abs(g.get("p95_latency", 1e9) - e["p95_latency"]) <= .5
              and abs(g.get("avg_uptime", 1e9) - e["avg_uptime"]) <= .2 and g.get("breaches") == e["breaches"] and acao == "*")
        bad += not ok
        if not ok or c["threshold_ms"] == 174:
            print(("PASS" if ok else "FAIL"), f"thr={c['threshold_ms']}", e["region"], "expected", e, "got", {k: g.get(k) for k in e}, "ACAO", acao)
print("ALL MATCH" if not bad else f"{bad} mismatches")
sys.exit(1 if bad else 0)
