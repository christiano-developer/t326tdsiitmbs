# Final — q-ollama

> Goal: the answer can be reproduced from this file alone.

## Final prompt

```text
Expose a local Ollama (port 11434) via ngrok 3.x so a browser page can fetch /api/version with header
ngrok-skip-browser-warning and read an X-Email response header. Give: the ollama serve command with CORS
(OLLAMA_ORIGINS=*), an ngrok traffic-policy YAML (add-headers: X-Email, Access-Control-Expose-Headers: *,
Access-Control-Allow-Headers incl. Ngrok-skip-browser-warning), and the ngrok command with --host-header=rewrite
(Ollama 403s non-localhost Host headers).
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

See [deploy.md](deploy.md): `OLLAMA_ORIGINS="*" ollama serve` → `ngrok http 11434 --host-header=rewrite
--traffic-policy-file traffic-policy.local.yml` → `src/check_ngrok.sh <url> <email>` → submit the forwarding URL.

## Expected output

```
PASS hostname contains ngrok
PASS preflight status 2xx
PASS preflight Allow-Origin *
PASS preflight allows ngrok-skip-browser-warning
body: {"version":"0.17.5"}
PASS JSON has version (Ollama)
PASS GET Allow-Origin *
PASS Expose-Headers * (JS can read X-Email)
PASS X-Email matches

ALL CHECKS PASS
```

## Answer submitted (✅ passed)

```
https://unluckily-barber-cultivate.ngrok-free.dev
```
