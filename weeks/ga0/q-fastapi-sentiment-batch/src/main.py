"""POST /sentiment - batch sentiment (happy / sad / neutral) with a rule-based lexicon classifier.
Request {"sentences": [...]} -> {"results": [{"sentence": s, "sentiment": label}, ...]} in input order. CORS *.
"""
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sentiment import classify

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class SentimentRequest(BaseModel):
    sentences: List[str]


@app.post("/sentiment")
def sentiment(req: SentimentRequest) -> dict:
    return {"results": [{"sentence": s, "sentiment": classify(s)} for s in req.sentences]}


@app.get("/")
def health() -> dict:
    return {"status": "ok", "endpoint": "POST /sentiment"}
