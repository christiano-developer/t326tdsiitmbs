# q-oauth-jwks-verify-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 2 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**OAuth 2.0 / OIDC Token Verification Service (2 marks)**

Deploy `POST /verify` taking `{"token": "<JWT>"}`. Valid → 200 `{"valid": true, "email", "sub", "aud"}` (claims echoed from the token); invalid → non-200 (401) `{"valid": false}`.

Reject unless: RS256 signature verifies with the given IdP public key, `iss` = `https://idp.exam.local`, `aud` = `tds-tlnbi78i.apps.exam.local` (seeded), `exp` in the future.

Grader mints four fresh tokens per check: valid, expired, wrong audience, tampered payload. Submit the full `/verify` URL.

## Inputs / given data

Assigned values are seeded per email (`ROLL_NUMBER@ds.study.iitm.ac.in`) and shown on the exam page.

## Final answer

```
https://<your-project>.vercel.app/verify
```

## Status notes

<!-- Required for set-aside (where I stopped, what's next)
     and cant-approach (the blocker). -->

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [deploy.md](deploy.md) — commands + guide to deploy / boot / configure
- `src/` — code · `data/` — inputs/outputs
