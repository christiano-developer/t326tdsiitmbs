"""GA5 Q2: nomic-embed-text vs mxbai-embed-large via Ollama, FAISS IndexFlatIP, Spearman rho.
Mirrors the exam's starter script exactly (plain /api/embeddings, no task prefixes).
Run: python3 rank_corr.py ../data/dataset.json  -> prints the 10x7 matrix and writes answer.json
"""
import json, sys
import numpy as np, faiss, requests
from scipy.stats import spearmanr

OLLAMA = "http://localhost:11434/api/embeddings"
path = sys.argv[1] if len(sys.argv) > 1 else "dataset.json"
data = json.load(open(path))
sentences, queries = data["sentences"], data["queries"]

def emb(model, texts):
    arr = np.array([requests.post(OLLAMA, json={"model": model, "prompt": t}).json()["embedding"] for t in texts],
                   dtype=np.float32)
    faiss.normalize_L2(arr)
    return arr

A, B = emb("nomic-embed-text", sentences), emb("mxbai-embed-large", sentences)
ia, ib = faiss.IndexFlatIP(A.shape[1]), faiss.IndexFlatIP(B.shape[1])
ia.add(A); ib.add(B)
QA, QB = emb("nomic-embed-text", queries), emb("mxbai-embed-large", queries)

matrix = []
for q in range(len(queries)):
    Da, Ia = ia.search(QA[q:q+1], 50)
    Db, Ib = ib.search(QB[q:q+1], 50)
    sa, sb = np.zeros(50), np.zeros(50)
    sa[Ia[0]] = Da[0]; sb[Ib[0]] = Db[0]
    rho, _ = spearmanr(sa, sb)
    matrix.append([*map(int, Ia[0][:3]), *map(int, Ib[0][:3]), round(float(rho), 4)])

out = json.dumps(matrix)
print(out)
json.dump(matrix, open("answer.json", "w"))
assert all(r[6] < 0.95 for r in matrix), "rho >= 0.95: same model twice?"
