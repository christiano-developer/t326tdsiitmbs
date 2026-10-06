"""Expected answer for q-crawl-html, computed from the grader's own per-letter file counts.

The quiz JS (exam-tds-2026-09-ga0.js) hard-codes how many HTML files start with each letter (table `tn`)
and sums the letters in the student's seeded range. No crawl is needed to reproduce the answer.

Usage: python3 src/count_from_grader.py [START] [END]   (default A K)
"""
import sys

# Verbatim from the quiz JS: tn={t:9,n:4,s:12,i:3,w:8,e:7,a:6,p:10,f:8,m:7,h:5,c:3,y:1,o:7,v:3,r:3,d:4,l:2,b:2,q:1,u:1}
TN = {"t": 9, "n": 4, "s": 12, "i": 3, "w": 8, "e": 7, "a": 6, "p": 10, "f": 8, "m": 7, "h": 5,
      "c": 3, "y": 1, "o": 7, "v": 3, "r": 3, "d": 4, "l": 2, "b": 2, "q": 1, "u": 1}

start = (sys.argv[1] if len(sys.argv) > 1 else "A").upper()
end = (sys.argv[2] if len(sys.argv) > 2 else "K").upper()

in_range = {k.upper(): v for k, v in sorted(TN.items()) if start <= k.upper() <= end}
print("letters in range:", in_range)
print(f"ANSWER files starting {start}-{end}: {sum(in_range.values())}")
