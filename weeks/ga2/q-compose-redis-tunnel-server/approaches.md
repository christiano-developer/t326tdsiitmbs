# Approaches — q-compose-redis-tunnel-server

## Problem in one line

Compose file with a healthchecked Redis and a FastAPI api that only uses `INCR`/`GET`/`PING`; publish only port 8000 and put a cloudflared quick tunnel in front.

## ⚠️ Distractors, gotchas and hidden text

| Item | Type | Reality |
|------|------|---------|
| In-memory dict | Trap | Fails with multiple uvicorn workers/restarts; state must live in Redis. |
| Static healthz | Trap | Must actually `PING` Redis. |
| Tunnel lifetime | Risk | Quick-tunnel URLs die with the process; keep it running until Save (Save re-checks). |

Scanned the question HTML for hidden elements/comments: none found.

## Verification

- Exam **Check** passed on 2026-10-18 (run by the user on their Mac; tunnels/recordings are local).
