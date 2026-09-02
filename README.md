# LiveOps Agent

LiveOps Agent is an incident-response project with a FastAPI backend, a React frontend, and a curated knowledge base for retrieval-backed diagnosis and remediation.

## Setup

Use a project virtual environment instead of the Homebrew-managed system Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

In VS Code, select the same interpreter:

```text
Cmd+Shift+P -> Python: Select Interpreter -> ./.venv/bin/python
```

If Pylance still shows missing imports, run `Pylance: Restart Language Server`.

## Environment

Create `backend/.env` with:

```bash
APP_NAME=LiveOps Agent
APP_ENV=development
API_PREFIX=/api
DATABASE_URL=postgresql+psycopg2:///liveops
CORS_ORIGINS=http://localhost:5173
```

## Run The Backend

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --app-dir backend
```

The API runs at `http://127.0.0.1:8000`.

## Knowledge Base

The repository includes a small retrieval knowledge base:

- `knowledge_base/runbooks/`: operational runbooks
- `knowledge_base/architecture/`: system and dependency notes
- `knowledge_base/incidents/`: historical incidents with similar but not identical failures

To regenerate the JSONL chunks used by retrieval:

```bash
source .venv/bin/activate
python backend/scripts/ingest_documents.py
```

The ingestion pipeline is:

```text
load -> clean -> chunk -> metadata -> write
```

Output is written to:

```text
backend/data/knowledge_chunks.jsonl
```

You can override paths or chunk settings:

```bash
python backend/scripts/ingest_documents.py \
  --knowledge-base-path knowledge_base \
  --output-path backend/data/knowledge_chunks.jsonl \
  --chunk-size 50 \
  --chunk-overlap 5
```

## Vector Retrieval

Day 6 retrieval lives in:

- `backend/app/retrieval/embeddings.py`
- `backend/app/retrieval/vector_store.py`
- `backend/tests/test_vector_retrieval.py`

The retrieval flow is:

```text
documents -> embeddings -> FAISS index -> semantic search -> ranked metadata
```

Run the focused retrieval test from the project root:

```bash
.venv/bin/python -m unittest -v backend/tests/test_vector_retrieval.py
```

The test indexes four small fake documents, searches for:

```text
payment service database connection pool exhausted
```

and verifies that payment/database documents rank above unrelated authentication and cache documents. The printed score is FAISS L2 distance, so lower is more relevant.
