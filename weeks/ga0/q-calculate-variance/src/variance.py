"""Sample variance (N-1) of the GA0 measurements, with sanity checks.

Usage: python3 src/variance.py [data/q-calculate-variance.json]
"""
import json
import math
import statistics
import sys
from pathlib import Path

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "data/q-calculate-variance.json"
data = json.loads(path.read_text())

# Sanity: flat list of real numbers, no NaN (the question says "no missing values"; verify anyway)
assert isinstance(data, list), "expected a JSON array"
assert all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in data), "non-numeric values"
assert not any(isinstance(x, float) and math.isnan(x) for x in data), "NaN values"

n = len(data)
mean = sum(data) / n
sample = statistics.variance(data)                     # N-1 (Bessel), same as Excel VAR.S
manual = sum((x - mean) ** 2 for x in data) / (n - 1)  # independent cross-check
population = statistics.pvariance(data)                # N: the wrong one, shown for contrast

assert math.isclose(sample, manual, rel_tol=1e-12)
print(f"n={n} min={min(data)} max={max(data)} mean={mean:.4f}")
print(f"population variance (N, wrong): {population:.2f}")
print(f"ANSWER sample variance (N-1): {sample:.2f}")
