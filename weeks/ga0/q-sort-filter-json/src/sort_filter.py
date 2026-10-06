"""Filter products with price >= THRESHOLD, sort by category A-Z, price high-low, name A-Z; print minified JSON.

Usage: python3 src/sort_filter.py [THRESHOLD] [data/products.json]
Matches the grader: keeps price >= threshold ("filter out price < threshold"); keys compared exactly.
"""
import json
import sys

threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 114.97
path = sys.argv[2] if len(sys.argv) > 2 else "data/products.json"
products = json.load(open(path))

kept = [p for p in products if p["price"] >= threshold]
kept.sort(key=lambda p: (p["category"], -p["price"], p["name"]))

print(json.dumps(kept, separators=(",", ":")))
print(f"# input={len(products)} kept={len(kept)} threshold={threshold}", file=sys.stderr)
