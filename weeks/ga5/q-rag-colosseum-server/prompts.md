# Prompts — q-rag-colosseum-server

1. **Plan:** read the exam JS → KB is generated client-side (`generateKB`), probes are server-side; decided on
   whole-KB-in-context (50 passages fit easily) instead of a vector store.
2. **First deploy (OpenAI direct):** `/_selftest` → 429 on every call; answers came from the TF-IDF fallback.
   *Failure:* key had $0 balance (expired prepaid credit). → provider chain via env (`LLM_*`, `LLM2_*`, `LLM3_*`).
3. **AI Pipe + Gemini:** 1.5 s/answer; hand probes (Redis port, SGD lr with injection, Kafka → null, Paxos vs Raft) all right.
4. **Gauntlet 1–3:** 1.8 → 1.9; R4 3/4. In-memory `/_recent` only caught 2/20 → log to Upstash.
5. **R3 synthesis:** one answer omitted ports/timeouts → prompt rule + code that appends missing token sentences.
   Stopped padding sources for multi-passage answers; strictly descending scores.
6. **R4:** found the false-premise probes. First fix (prompt: "ignore premise, answer") still 3/4 and broke R2
   (ARIES CLR answered). *Failure.* Final: deterministic `correct_premise()` + stricter abstain rule → **2/2**.
7. **Deploy accident:** a broken draft (syntax error) was uploaded because a staged file name was reused →
   gauntlet 0/2 until the fixed file was re-sent under a unique name and its md5 verified on the Mac.

Final system prompt: see `SYSTEM` in [src/tds-ga5-rag/api/index.py](src/tds-ga5-rag/api/index.py).
