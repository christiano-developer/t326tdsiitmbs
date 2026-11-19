# Prompts — q-harness-safety-router-server

1. Read the policy from the exam JS; wrote a keyword + resolved-metadata engine with Upstash capture of raw batches.
2. Check #1 (capture): 34/96 exact. Pulled the 4 batches (`../pull-q4-cases.sh <base-url>`).
3. Clustered cases by user-message template (≈ 60 templates), labelled each per policy, rewrote `rules.py`
   (revocation, resolved-path escapes, task-scoped credentials, host mounts, destination drift, preflight +
   rollback for production, owned/confined security tests).
4. Check #2: 94/96 → kept. Save used the third check.
