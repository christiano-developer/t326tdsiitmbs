# Final — q-config-precedence-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-config-precedence-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-config-precedence-server)

## How to solve (for a teammate)

The assigned values in the code (email, origins, keys, limits, layer values) are **seeded per email** — replace them with yours from the exam page.

**Approach:** Dict merge in precedence order with key normalisation + alias map, then type coercion, then mask `api_key` (same code as GA1, new layer values).

1. Make a folder named after the Vercel project you want (e.g. `tds-ga2-config`) with this layout:
   ```
   tds-ga2-config/
     app.py              # from api.index import app
     api/__init__.py     # empty
     api/index.py        # the app below
     requirements.txt    # fastapi, pyyaml
   ```
2. `app.py` contains exactly: `from api.index import app  # noqa: F401`
3. `api/index.py`:

<details><summary>api/index.py (click to expand)</summary>

```python
"""12-factor config precedence service (TDS GA2 q-config-precedence-server).

Layers, low -> high precedence:
  1. defaults (hardcoded)
  2. config.<APP_ENV>.yaml          (APP_ENV defaults to "development")
  3. dotenv file (app.env here)     (APP_* keys; NUM_WORKERS is an alias for workers)
  4. OS environment (APP_* prefix)  (set as Vercel env vars: APP_WORKERS, APP_API_KEY)
  5. ?set=key=value query params    (CLI-style overrides, repeatable)
api_key is always masked as "****". The dotenv file is named app.env because
Vercel and git ignore ".env*" files.
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parent.parent

DEFAULTS = {"port": 8000, "workers": 1, "debug": False, "log_level": "info", "api_key": "default-secret-000"}
TRUE = {"true", "1", "yes", "on"}
ALIASES = {"num_workers": "workers"}


def coerce(key: str, value):
    if key in ("port", "workers"):
        return int(str(value).strip())
    if key == "debug":
        return value if isinstance(value, bool) else str(value).strip().lower() in TRUE
    return str(value)


def norm_key(key: str) -> str:
    k = key.strip().lower()
    return ALIASES.get(k, k)


def read_dotenv(path: Path) -> dict:
    out = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k.startswith("APP_"):
            out[norm_key(k[4:])] = v
        elif k.upper() == "NUM_WORKERS":
            out["workers"] = v
    return out


def env_layer() -> dict:
    return {norm_key(k[4:]): v for k, v in os.environ.items() if k.startswith("APP_") and k != "APP_ENV"}


def effective(overrides: list[str]) -> dict:
    cfg = dict(DEFAULTS)
    env_name = os.environ.get("APP_ENV", "development")
    yml = ROOT / f"config.{env_name}.yaml"
    layers = [
        yaml.safe_load(yml.read_text(encoding="utf-8")) if yml.exists() else {},
        read_dotenv(ROOT / "app.env"),
        env_layer(),
    ]
    for layer in layers:
        for k, v in (layer or {}).items():
            cfg[norm_key(k)] = v
    for item in overrides:
        if "=" in item:
            k, v = item.split("=", 1)
            cfg[norm_key(k)] = v
    out = {k: coerce(k, v) for k, v in cfg.items() if k in DEFAULTS}
    out["api_key"] = "****"
    return out


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/effective-config")
def effective_config(request: Request):
    return effective(request.query_params.getlist("set"))


@app.get("/")
def root():
    return {"ok": True, "endpoint": "/effective-config?set=key=value"}
```

</details>

`app.env`:

```
APP_PORT=8051
APP_DEBUG=true
```

`config.development.yaml`:

```
port: 8385
debug: false
log_level: debug
```

4. Deploy from inside the folder: `vercel deploy --prod --yes -e APP_WORKERS=11 -e APP_API_KEY=<your APP_API_KEY>`. **No `vercel.json`** (rewrites make every route 404).
5. Submit the **Aliased** URL from the output (`https://<project>.vercel.app/effective-config`), press Check, then Save.

Gotchas: This email's `.env` has no NUM_WORKERS; the alias is still implemented. Vercel/git ignore `.env*`, so the dotenv layer ships as `app.env`. Set as Vercel env vars at deploy (`-e`), not hardcoded.

## Final prompt

```text
Resolve 12-Factor Config Precedence (1 mark)
<paste the full question text with your assigned values>
Write a FastAPI app for Vercel zero-config deployment (app.py re-exporting `app` from api/index.py,
requirements.txt, no vercel.json). Return JSON errors (never a bare 500). Dict merge in precedence order with key normalisation + alias map, then type coercion, then mask `api_key` (same code as GA1, new layer values).
Also give a pytest/TestClient script that replays exactly what the grader checks.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

```bash
cd ~/developer/t326tdsiitmbs && set -a && source .env && set +a
cd weeks/ga2/q-config-precedence-server/src/tds-ga2-config
vercel deploy --prod --yes -e APP_WORKERS=11 -e APP_API_KEY="$GA2_CONFIG_APP_API_KEY"
```

Source: [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-config-precedence-server/src/tds-ga2-config/api/index.py](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-config-precedence-server/src/tds-ga2-config/api/index.py)

## Expected output

Exam **Check** shows the question as correct.

## Answer submitted

```
https://<your-project>.vercel.app/effective-config
```
