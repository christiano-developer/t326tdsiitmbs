# q-ollama

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes (local Ollama + ngrok tunnel; must stay running until graded) |
| Started   | 2026-10-07 |
| Closed    | 2026-10-07 (passed after one host-header fix) |

## Question

**Local LLM Runner: Ollama** + **Tunneling: ngrok**: case study *eShopCo AI Chat Diagnostics*.

> 1. Enable CORS for Ollama: `export OLLAMA_ORIGINS="*"` then `ollama serve`.
> 2. Expose it via ngrok, injecting your email in a header:
>    `ngrok http 11434 --response-header-add "X-Email: <my-exam-email>" --response-header-add 'Access-Control-Expose-Headers: *'
>    --response-header-add 'Access-Control-Allow-Headers: Authorization,Content-Type,User-Agent,Accept,Ngrok-skip-browser-warning'`
> 3. Note the HTTPS forwarding URL. Verify CORS `Access-Control-Allow-Origin: *`, the email header, and a valid Ollama JSON body.
> Paste your ngrok forwarding URL. (We'll automatically fetch and verify the response headers and body.)

## Inputs / given data

None. Local Ollama 0.17.5 (already installed); ngrok 3.39.11 (installed via brew); free ngrok account + authtoken.

## Final answer

```
https://unluckily-barber-cultivate.ngrok-free.dev
```

(The free-tier URL changes on every ngrok restart; this one was graded.)

## Status notes

- First attempt: GET via the tunnel returned **403 from Ollama** (Host-header / DNS-rebinding check) → exam showed
  "Unexpected end of JSON input". Fixed with `ngrok … --host-header=rewrite`. All 8 replica checks pass; exam ✅ passed.
- **Keep both processes running until grading closes** (`ollama serve` + `ngrok`). Teardown: see deploy.md.
- Reminder: the ngrok authtoken was pasted into the chat log, so reset it on the ngrok dashboard after grading.

## Files

- [prompts.md](prompts.md) · [approaches.md](approaches.md) · [final.md](final.md) · [deploy.md](deploy.md)
- [src/check_ngrok.sh](src/check_ngrok.sh) — grader replica (preflight + GET + headers + body)
- [src/traffic-policy.example.yml](src/traffic-policy.example.yml) — ngrok response headers (real copy `traffic-policy.local.yml` is git-ignored)
