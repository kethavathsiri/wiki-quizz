Render deployment notes for the backend

1) Overview

This repository includes a `render.yaml` manifest that configures a Render Web Service for the backend. The service builds from the Dockerfile in `backend/` and expects the app to listen on port 8000 and expose a `/api/health` endpoint.

2) Required environment variables (set these as Render dashboard secrets)

- `DATABASE_URL` — Postgres connection string (e.g. `postgres://user:pass@host:5432/dbname`). If you use Render Managed Postgres, copy the Database URL after creating the database.
- `JWT_SECRET_KEY` — strong random string used to sign JWTs.
- `ACCESS_TOKEN_EXPIRE_MINUTES` — token lifetime in minutes (default: 60).
- `GEMINI_API_KEY` — if using the LLM service that requires this key. Otherwise leave blank.

3) How to deploy (quick steps)

- Push this branch to GitHub (main).
- On Render dashboard:
  - Create a new Web Service → Connect to the GitHub repo `kethavathsiri/wiki-quizz`.
  - Render will detect the `render.yaml` manifest; confirm the service settings.
  - In the service "Environment" settings, add the environment variables listed above as Secrets.
  - (Optional) Create a Render Managed PostgreSQL database and copy its DATABASE_URL into the service secrets.
  - Trigger a deploy (Render will auto-deploy on push because `autoDeploy: true`).

4) Notes & troubleshooting

- The Dockerfile in `backend/` exposes port 8000 and runs `python main.py`.
- The manifest uses `env: docker` so Render will build the Docker image from `backend/` using the included Dockerfile.
- If you need a custom build or start command, edit `render.yaml` or set them in the Render service settings.
- Monitor logs in the Render dashboard to see migration/errors on startup.

5) Local testing commands (optional)

Build and run locally with Docker (example):

```bash
cd backend
docker build -t wiki-quizz-backend .
docker run -e DATABASE_URL="postgres://..." -e JWT_SECRET_KEY="secret" -p 8000:8000 wiki-quizz-backend
```

6) After deploy

- Visit the Render service URL and check `https://<service>.onrender.com/api/health` to confirm the backend is up.
- Update your frontend production `REACT_APP_API_URL` to point to the Render service URL (or set it as a secret in the frontend CI workflow).
