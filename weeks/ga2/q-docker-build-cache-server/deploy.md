# Deploy guide — q-docker-build-cache-server

Static JSON on Vercel (no server code). Vercel serves `.json` as `application/json` with `Access-Control-Allow-Origin: *`.

## Target

| Field         | Value |
|---------------|-------|
| Platform      | Vercel (static, team `<your-team>`) |
| Vercel project| `tds-ga2-docker-cache` (named after the folder) |
| Public URL    | https://<your-project>.vercel.app/answer.json |
| Runtime       | none (static file) |
| Required env  | none |

## 1. Build the answer

```bash
cd weeks/ga2/q-docker-build-cache-server
python3 src/cache_model.py 55 10 15 > data/answer.json
cp data/answer.json src/tds-ga2-docker-cache/answer.json
```

## 2. Deploy

```bash
cd weeks/ga2/q-docker-build-cache-server/src/tds-ga2-docker-cache
pwd                        # must end in /src/tds-ga2-docker-cache
vercel deploy --prod --yes # first run creates project "tds-ga2-docker-cache"
```

Use the **Aliased** URL from the output (deployment URLs sit behind Vercel auth).
If `vercel` appended `.vercel`/`.env*` to the repo-root `.gitignore`, revert that (`git checkout -- .gitignore`).

## 3. Test

```bash
curl -sS -D - https://<your-project>.vercel.app/answer.json
```

- [ ] HTTP 200, `content-type: application/json`, body equals `data/answer.json`
- [ ] Works logged out / incognito

## 4. Keep alive until graded

Leave the project up until the GA2 deadline.

## Teardown (after grading)

```bash
vercel project rm tds-ga2-docker-cache
```

## Troubleshooting log

| Symptom | Cause | Fix |
|---------|-------|-----|
