# Final — q-compose-redis-tunnel-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-compose-redis-tunnel-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-compose-redis-tunnel-server)

## How to solve (for a teammate)

Assigned values (tags, IDs, parameters) are **seeded per email**: use the ones on your exam page.

**Approach:** Compose file with a healthchecked Redis and a FastAPI api that only uses `INCR`/`GET`/`PING`; publish only port 8000 and put a cloudflared quick tunnel in front.

1. Create this layout and files:

<details><summary>docker-compose.yml (click to expand)</summary>

```yaml
# TDS GA2 q-compose-redis-tunnel-server: FastAPI api + Redis on the internal compose network.
# Run:  docker compose up --build -d   then tunnel port 8000.
services:
  api:
    build: ./api
    ports:
      - "8000:8000"          # only the api is published; redis stays internal
    environment:
      REDIS_HOST: redis
    depends_on:
      redis:
        condition: service_healthy
    restart: unless-stopped
  redis:
    image: redis:7-alpine
    command: ["redis-server", "--appendonly", "yes"]   # counts survive container restarts
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 2s
      timeout: 2s
      retries: 15
    restart: unless-stopped
volumes:
  redis-data:
```

</details>

`api/Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py ./
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

`api/requirements.txt`: `fastapi`, `uvicorn`, `redis`

<details><summary>main.py (click to expand)</summary>

```python
"""Redis-backed hit counter (TDS GA2 q-compose-redis-tunnel-server).

POST /hit/{key}   -> {"key", "count"}   (atomic Redis INCR)
GET  /count/{key} -> {"key", "count"}   (0 for unseen keys)
GET  /healthz     -> {"status": "ok", "redis": "up"}  (real PING)
All state lives in Redis, so counts survive api restarts and are shared by every uvicorn worker.
"""
import os

import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=int(os.getenv("REDIS_PORT", "6379")),
                decode_responses=True, socket_timeout=3)
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def rkey(key: str) -> str:
    return f"hits:{key}"


@app.post("/hit/{key}")
def hit(key: str):
    return {"key": key, "count": int(r.incr(rkey(key)))}


@app.get("/count/{key}")
def count(key: str):
    return {"key": key, "count": int(r.get(rkey(key)) or 0)}


@app.get("/healthz")
def healthz():
    try:
        r.ping()
        return {"status": "ok", "redis": "up"}
    except redis.RedisError:
        return JSONResponse({"status": "degraded", "redis": "down"}, status_code=503)
```

</details>

2. `docker compose up --build -d` and check `curl -s localhost:8000/healthz` → `{"status":"ok","redis":"up"}`.
3. Install cloudflared (`brew install cloudflared`) and run `cloudflared tunnel --url http://localhost:8000`; copy the `https://….trycloudflare.com` URL it prints.
4. Submit that base URL, Check, and keep Docker + the tunnel running until you Save (the URL changes if cloudflared restarts).

Gotchas: Fails with multiple uvicorn workers/restarts; state must live in Redis. Must actually `PING` Redis. Quick-tunnel URLs die with the process; keep it running until Save (Save re-checks).

## Final prompt

```text
Multi-Container App via Compose, Exposed by Tunnel (2 marks)
<paste the full question with your assigned values>
Give me the exact files and terminal commands for macOS (zsh) to satisfy every grader check, including
how to expose it publicly / package it, plus a quick local test for each check.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

See the steps above; code lives in [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-compose-redis-tunnel-server/src](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-compose-redis-tunnel-server/src).

## Expected output

Exam **Check** marks the question solved.

## Answer submitted

```
https://<random-words>.trycloudflare.com (cloudflared quick tunnel; changes every run)
```
