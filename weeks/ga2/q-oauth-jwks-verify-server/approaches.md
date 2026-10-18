# Approaches — q-oauth-jwks-verify-server

## Problem in one line

PyJWT `jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], audience=AUD, issuer=ISS, options={"require": ["exp","iss","aud"]})` inside try/except.

## Grader (from quiz JS)

Server-side (`/backendVerify`) mints tokens with the IdP private key and posts them.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Algorithm | Genuine | Pin `algorithms=["RS256"]` (blocks `alg: none` / HS256 key-confusion). |
| Tampered payload | Genuine | Signature check fails → 401; never decode without verification. |
| Error shape | Genuine | Catch every exception (bad JSON, malformed token) and return 401 `{valid:false}`, not 500. |

Scanned the question HTML for hidden elements/comments: none found.

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | FastAPI on Vercel (zero-config `app.py` → `api/index.py`), one project per question | chosen |
| B | One shared Vercel project for all GA2 services | rejected: one bad deploy breaks every question |

## Chosen: A

**Why:** same proven layout as GA1; isolated failures; folder name = Vercel project name.

## Verification

- Local: FastAPI `TestClient` tests replaying the grader's checks (all passed).
- Live: exam **Check** passed on 2026-10-18 (header went 3 → 14 / 25 for this batch of seven).
