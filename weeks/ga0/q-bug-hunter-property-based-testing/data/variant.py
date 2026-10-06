# Seeded variant "dedupe-3 / Topic Dedupe", copied verbatim from exam-tds-2026-09-ga0.js
# (function Ee). The grader exec()s ONE of these into the test namespace, then the student code.

BUGGY = '''def dedupe_topics(items):
  seen = set()
  out = []
  for item in items:
    key = str(item).lower()
    if key in seen:
      continue
    seen.add(key)
    out.append(item)
  return out
'''

CORRECT = '''def dedupe_topics(items):
  seen = set()
  out = []
  for item in items:
    if item in seen:
      continue
    seen.add(item)
    out.append(item)
  return out
'''
