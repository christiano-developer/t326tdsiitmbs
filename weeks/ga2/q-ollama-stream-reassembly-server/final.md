# Final — q-ollama-stream-reassembly-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-ollama-stream-reassembly-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-ollama-stream-reassembly-server)

## How to solve (for a teammate)

The hex chunks on your page are seeded by your email (the text contains `job-<your hash>`), so compute your own answer.

1. Copy the "Captured byte chunks" JSON from the question into a file `chunks.json` (keys `A`, `B`, `C`, each an array of hex strings).
2. Save this as `reassemble.py` next to it:

<details><summary>reassemble.py (click to expand)</summary>

```python
"""Rebuild Ollama-style NDJSON streams from hex-encoded byte chunks.

Usage: python3 reassemble.py chunks.json > answer.json
"""
import codecs
import json
import sys


def reassemble(chunks):
    decoder = codecs.getincrementaldecoder("utf-8")()  # keeps split multibyte chars
    buf, text = "", []
    for hx in chunks:
        buf += decoder.decode(bytes.fromhex(hx))
        while "\n" in buf:  # only complete newline-terminated records
            line, buf = buf.split("\n", 1)
            if not line.strip():
                continue
            rec = json.loads(line)
            if "error" in rec:  # keep earlier text, stop
                return {"text": "".join(text), "complete": False, "error": rec["error"]}
            text.append(rec.get("response", ""))  # ignore "thinking"
            if rec.get("done") is True:
                return {"text": "".join(text), "complete": True, "error": None}
    # EOF without a terminal record; any trailing partial record is dropped
    return {"text": "".join(text), "complete": False, "error": None}


if __name__ == "__main__":
    streams = json.load(open(sys.argv[1]))
    print(json.dumps({k: reassemble(v) for k, v in streams.items()}, ensure_ascii=False, indent=2))
```

</details>

3. Run `python3 reassemble.py chunks.json > answer.json`.
   - The key trick: decode bytes with an **incremental** UTF-8 decoder. Chunks are cut right after UTF-8 lead bytes, so `é` (`c3|a9`) and `✓` (`e2|9c93`) are split across chunks; decoding chunk-by-chunk corrupts them.
   - Only parse a record once its `\n` arrives; ignore `thinking`; stop at the first `done: true` (complete) or `error` record (incomplete, keep earlier text); at EOF drop the half-written trailing record (`complete: false, error: null`).
4. Host `answer.json` as raw JSON. Easiest: put it alone in a folder named e.g. `tds-ga2-stream`, `cd` into it and run `vercel deploy --prod --yes`. Submit the **Aliased** URL + `/answer.json` (e.g. `https://<your-project>.vercel.app/answer.json`). GitHub "blob" pages are HTML, so they fail.
5. Paste the URL, press Check, then Save.

## Final prompt

```text
I have three Ollama native NDJSON streams given as arrays of hex-encoded byte chunks (JSON below).
Write a Python script that, per stream: decodes the hex with an incremental UTF-8 decoder (multibyte
chars are split across chunks), buffers until "\n" to get complete JSON records, concatenates only the
"response" fields (ignore "thinking"), stops at the first done:true record (include its response,
complete:true, error:null) or at the first {"error":...} record (keep earlier text, complete:false,
error:<string>, ignore later records); at EOF without a terminal record return complete:false,
error:null and drop any incomplete trailing record. Print {"A":{"text","complete","error"},"B":...,"C":...}
with ensure_ascii=False.
<paste chunks JSON>
```

- **Tool / model used:** Claude (Opus 5.5) — script written directly, verified against the generator in the quiz JS.

## Reproduction steps (needs a clone of this repo)

```bash
cd weeks/ga2/q-ollama-stream-reassembly-server
python3 src/reassemble.py data/chunks.json > data/answer.json
cp data/answer.json src/tds-ga2-stream/answer.json
cd src/tds-ga2-stream && vercel deploy --prod --yes
curl -sS https://<your-project>.vercel.app/answer.json
```

Files: [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-ollama-stream-reassembly-server/src/reassemble.py](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-ollama-stream-reassembly-server/src/reassemble.py), [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-ollama-stream-reassembly-server/data/chunks.json](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-ollama-stream-reassembly-server/data/chunks.json)

## Expected output

```json
{"A": {"text": "Report job-48c9d2a0: café\nReady ✓", "complete": true, "error": null},
 "B": {"text": "Partial job-48c9d2a0", "complete": false, "error": null},
 "C": {"text": "Draft job-48c9d2a0", "complete": false, "error": "model unloaded"}}
```

(`\n` is a real newline inside `text`.)

## Answer submitted

```
https://<your-project>.vercel.app/answer.json
```
