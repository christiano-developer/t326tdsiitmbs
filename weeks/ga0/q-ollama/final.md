# Final — q-ollama

> Goal: the answer can be reproduced from this file alone.

## How to solve (for a teammate)

> Values are seeded from your email, so use your own email and ngrok URL.

Needs Ollama, plus ngrok with a free account (`ngrok config add-authtoken <token>` once).

1. Terminal 1: start Ollama with browser access allowed, and leave it running:
   ```bash
   OLLAMA_ORIGINS="*" ollama serve
   ```
2. Create `traffic-policy.yml` with your email in it:
   ```yaml
   on_http_response:
     - actions:
         - type: add-headers
           config:
             headers:
               X-Email: "you@example.com"
               Access-Control-Expose-Headers: "*"
               Access-Control-Allow-Headers: "Authorization,Content-Type,User-Agent,Accept,Ngrok-skip-browser-warning"
   ```
3. Terminal 2, in the same folder (leave it running):
   ```bash
   ngrok http 11434 --host-header=rewrite --traffic-policy-file traffic-policy.yml
   ```
4. Copy the `https://...ngrok-free.dev` URL shown next to **Forwarding**. Test with `curl -s -H "ngrok-skip-browser-warning: 1" <url>/api/version`, which should print `{"version":"..."}`.
5. Submit that URL, then Check and Save. Keep both terminals running until it's graded.

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
