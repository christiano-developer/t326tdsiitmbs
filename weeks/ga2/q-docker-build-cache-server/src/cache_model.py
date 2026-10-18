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
