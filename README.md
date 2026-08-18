# LiveOps Agent

Day 1 backend for a LiveOps incident-response project.

## Run The Backend

```bash
source venv/bin/activate
uvicorn app.main:app --reload --app-dir backend
```

The API runs at `http://127.0.0.1:8000`.

## Environment

Create `backend/.env` with:

```bash
APP_NAME=LiveOps Agent
APP_ENV=development
API_PREFIX=/api
DATABASE_URL=postgresql+psycopg2:///liveops
CORS_ORIGINS=http://localhost:5173
```

## Day 1 Flow

Frontend calls FastAPI routes, FastAPI delegates to service modules, and the health endpoint verifies database connectivity.
