# Final — q-oauth-jwks-verify-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-oauth-jwks-verify-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-oauth-jwks-verify-server)

## How to solve (for a teammate)

The assigned values in the code (email, origins, keys, limits, layer values) are **seeded per email** — replace them with yours from the exam page.

**Approach:** PyJWT `jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], audience=AUD, issuer=ISS, options={"require": ["exp","iss","aud"]})` inside try/except.

1. Make a folder named after the Vercel project you want (e.g. `tds-ga2-jwt`) with this layout:
   ```
   tds-ga2-jwt/
     app.py              # from api.index import app
     api/__init__.py     # empty
     api/index.py        # the app below
     requirements.txt    # fastapi, pyjwt[crypto]
   ```
2. `app.py` contains exactly: `from api.index import app  # noqa: F401`
3. `api/index.py`:

<details><summary>api/index.py (click to expand)</summary>

```python
"""RS256 JWT verification service (TDS GA2 q-oauth-jwks-verify-server).

POST /verify {"token": "..."} -> 200 {valid: true, email, sub, aud} or 401 {valid: false}.
Checks: RS256 signature against the IdP public key, iss, aud, exp (all required).
"""
import jwt
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-tlnbi78i.apps.exam.local"
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuY
cxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMID
EkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXc
WyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfW
ed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfI
SI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----"""

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

INVALID = lambda: JSONResponse({"valid": False}, status_code=401)  # noqa: E731


@app.post("/verify")
async def verify(request: Request):
    try:
        body = await request.json()
        token = body.get("token") if isinstance(body, dict) else None
        if not isinstance(token, str) or not token:
            return INVALID()
        claims = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],  # pin the algorithm: no "none", no HS256 key-confusion
            audience=AUDIENCE,
            issuer=ISSUER,
            options={"require": ["exp", "iss", "aud"]},
        )
    except Exception:  # bad JSON, bad signature, expired, wrong aud/iss, malformed token
        return INVALID()
    return {"valid": True, "email": claims.get("email"), "sub": claims.get("sub"), "aud": claims.get("aud")}


@app.get("/")
def root():
    return {"ok": True, "endpoint": "POST /verify"}
```

</details>

4. Deploy from inside the folder: `vercel deploy --prod --yes`. **No `vercel.json`** (rewrites make every route 404).
5. Submit the **Aliased** URL from the output (`https://<project>.vercel.app/verify`), press Check, then Save.

Gotchas: Pin `algorithms=["RS256"]` (blocks `alg: none` / HS256 key-confusion). Signature check fails → 401; never decode without verification. Catch every exception (bad JSON, malformed token) and return 401 `{valid:false}`, not 500.

## Final prompt

```text
OAuth 2.0 / OIDC Token Verification Service (2 marks)
<paste the full question text with your assigned values>
Write a FastAPI app for Vercel zero-config deployment (app.py re-exporting `app` from api/index.py,
requirements.txt, no vercel.json). Return JSON errors (never a bare 500). PyJWT `jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], audience=AUD, issuer=ISS, options={"require": ["exp","iss","aud"]})` inside try/except.
Also give a pytest/TestClient script that replays exactly what the grader checks.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

```bash
cd ~/developer/t326tdsiitmbs && set -a && source .env && set +a
cd weeks/ga2/q-oauth-jwks-verify-server/src/tds-ga2-jwt
vercel deploy --prod --yes
```

Source: [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-oauth-jwks-verify-server/src/tds-ga2-jwt/api/index.py](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-oauth-jwks-verify-server/src/tds-ga2-jwt/api/index.py)

## Expected output

Exam **Check** shows the question as correct.

## Answer submitted

```
https://<your-project>.vercel.app/verify
```
