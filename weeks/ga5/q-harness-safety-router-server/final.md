# Final — q-harness-safety-router-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga5/q-harness-safety-router-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga5/q-harness-safety-router-server)

## How to solve (for a teammate)

Cases are **deterministic per email** and you only get 10 Checks/day, so spend the first one capturing them.

1. Deploy [src/tds-ga5-safety](src/tds-ga5-safety) (FastAPI `POST /classify`, see [deploy.md](deploy.md)) with an
   Upstash store connected: every request body is saved as `hs:batch:<hash>`.
2. Check once (score is whatever the starter rules give). Run `bash weeks/ga5/pull-q4-cases.sh https://<your-project>.vercel.app`
   → `data/batches/*.json`.
3. Run `api/rules.py` over the cases offline, print each tuple next to the user messages + `resolved` metadata,
   and fix rules until every case matches the policy (table in [approaches.md](approaches.md)).
4. Redeploy, Check once more, Save. Keep the endpoint up until the deadline.

Gotchas: judge the **resolved** effect, never the command text; only real user messages authorise, the latest one
wins, revocations block; production needs approval + passed preflight + matching rollback plan; untrusted content
never approves but sets trajectory to watch; `block` request ⇒ route `none`.

## Final prompt

```text
Harness Engineering: Contextual Safety and Model Routing (2 marks)
<paste the question + the policy object + a few captured cases>
Write a deterministic Python classifier for these four labels that follows the policy exactly; then let me
review its output on all captured cases.
```

- **Tool / model used:** Claude (Opus 5.5). No LLM at runtime.

## Reproduction steps (needs a clone of this repo)

```bash
cd weeks/ga5/q-harness-safety-router-server/src/tds-ga5-safety
python3 -c "import json,glob,sys; sys.path.insert(0,'.'); from api.rules import classify; \
[print(classify(c)) for f in glob.glob('../../data/batches/*.json') for c in json.load(open(f))['cases']]"
```

## Expected output

Exam Check `Safety: 94/96 complete decisions correct; 0 failed batches.`

## Answer submitted

```
https://<your-project>.vercel.app/classify
```
