# Final — q-docker-build-cache-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-docker-build-cache-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-docker-build-cache-server)

## How to solve (for a teammate)

The step logic is the same for everyone; only the costs (L2/L4/L5 seconds) are seeded by email, so read yours off the page.

1. Apply Docker's cache rules:
   - `COPY` is keyed on a checksum of the copied files' **contents** (and mode/owner) — **not mtime**. Files in `.dockerignore` never reach the build, so changing them changes nothing.
   - `RUN` is keyed on its **instruction text** (and the parent layer).
   - The first step whose key changes misses; every later step re-runs (the question states this).
2. Per case, find the first miss:
   - A `src/app.py` content → L3 (`COPY src/`) misses → L3, L4, L5.
   - B `requirements.txt` content → L1 misses → L1…L5.
   - C `touch` only (mtime) → no miss → `[]`.
   - D `README.md` (dockerignored) → no miss → `[]`.
   - E L4 text changed (`-q`) → L4, L5.
3. Seconds = sum of costs of listed steps (COPY = 0). Include re-run COPY steps in `steps` even though they cost 0.
4. Write the JSON, e.g. with this script (pass your three costs):

<details><summary>cache_model.py (click to expand)</summary>

```python
"""Model Docker layer-cache invalidation for the GA2 Dockerfile.

Rule: the first step whose cache key changes misses; every later step re-runs.
COPY keys = checksum of copied file contents (+ mode/owner), NOT mtime, and only
files that survive .dockerignore. RUN keys = the instruction text (+ parent layer).
Usage: python3 cache_model.py [install compile test] > answer.json
"""
import json
import sys

install, compile_, test = (int(x) for x in sys.argv[1:4]) if len(sys.argv) > 3 else (55, 10, 15)
STEPS = ["L1", "L2", "L3", "L4", "L5"]
COST = {"L1": 0, "L2": install, "L3": 0, "L4": compile_, "L5": test}

# first step whose own cache key changes (None = everything hits cache)
FIRST_MISS = {
    "A": "L3",  # src/app.py content -> COPY src/ checksum changes
    "B": "L1",  # requirements.txt content -> COPY requirements.txt checksum changes
    "C": None,  # touch: mtime is not part of the COPY checksum
    "D": None,  # README.md is in .dockerignore -> not in the build context
    "E": "L4",  # RUN instruction text changed
}

out = {}
for case, first in FIRST_MISS.items():
    steps = [] if first is None else STEPS[STEPS.index(first):]
    out[case] = {"steps": steps, "seconds": sum(COST[s] for s in steps)}
print(json.dumps(out, indent=2))
```

</details>

   `python3 cache_model.py <L2> <L4> <L5> > answer.json`
5. Host as raw JSON: put `answer.json` alone in a folder (e.g. `tds-ga2-docker-cache`), `cd` into it, `vercel deploy --prod --yes`; submit the **Aliased** URL + `/answer.json`. Check, then Save.

## Final prompt

```text
Dockerfile: FROM python:3.12-slim / WORKDIR /app / L1 COPY requirements.txt ./ / L2 RUN pip install -r
requirements.txt / L3 COPY src/ ./src/ / L4 RUN python -m compileall src / L5 RUN python -m unittest discover -s src.
README.md is in .dockerignore. Using BuildKit cache rules (COPY keyed on file content checksum, not mtime;
RUN keyed on instruction text; after the first miss all later steps re-run), for each independent case
A) edit src/app.py content B) edit requirements.txt C) touch src/app.py only D) edit README.md
E) change L4 to "RUN python -m compileall -q src", list re-executed steps L1–L5 in order (include
zero-cost COPY) and total seconds with costs L2=<a>, L4=<b>, L5=<c>, COPY=0. Output only
{"A":{"steps":[...],"seconds":N},...,"E":{...}}.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

```bash
cd weeks/ga2/q-docker-build-cache-server
python3 src/cache_model.py 55 10 15 > data/answer.json
cp data/answer.json src/tds-ga2-docker-cache/answer.json
cd src/tds-ga2-docker-cache && vercel deploy --prod --yes
curl -sS https://<your-project>.vercel.app/answer.json
```

## Expected output

Costs for ROLL_NUMBER: L2 = 55, L4 = 10, L5 = 15.

```json
{"A":{"steps":["L3","L4","L5"],"seconds":25},"B":{"steps":["L1","L2","L3","L4","L5"],"seconds":80},
 "C":{"steps":[],"seconds":0},"D":{"steps":[],"seconds":0},"E":{"steps":["L4","L5"],"seconds":25}}
```

## Answer submitted

```
https://<your-project>.vercel.app/answer.json
```
