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
